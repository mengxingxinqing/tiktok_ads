"""
订单数据查询 API

GET /orders/report/{advertiser_id}     获取订单维度报表
GET /orders/summary/{advertiser_id}    按商品/Campaign 汇总

兼容 GMVMax 账户：
- GMVMax 账户没有 ORDER data_level，从 GMVMAX_CAMPAIGN 本地数据读取
- 普通 Auction 账户尝试调用 TikTok API，失败则回退到本地数据
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.models.metrics import MetricsSnapshot
from app.services.tiktok_client import TikTokClient, TikTokAPIError

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/report/{advertiser_id}")
async def get_order_report(
    advertiser_id: str,
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD，默认最近 7 天"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取订单数据

    优先从本地 metrics_snapshots 读取（包含 GMVMax 数据），
    如有普通 Auction 广告则尝试调 TikTok API 补充。
    """
    if not end_date:
        end_date = date.today().isoformat()
    if not start_date:
        start_date = (date.today() - timedelta(days=7)).isoformat()

    start_d = date.fromisoformat(start_date)
    end_d = date.fromisoformat(end_date)

    # 从本地 metrics_snapshots 查 GMVMax + AD 数据
    result = await db.execute(
        select(
            MetricsSnapshot.stat_date,
            MetricsSnapshot.data_level,
            MetricsSnapshot.object_id.label("campaign_id"),
            MetricsSnapshot.object_name.label("campaign_name"),
            MetricsSnapshot.spend,
            MetricsSnapshot.conversion.label("orders"),
            MetricsSnapshot.gross_revenue.label("revenue"),
            MetricsSnapshot.roi,
            MetricsSnapshot.cost_per_conversion.label("cost_per_order"),
        )
        .where(and_(
            MetricsSnapshot.advertiser_id == advertiser_id,
            MetricsSnapshot.stat_date >= start_d,
            MetricsSnapshot.stat_date <= end_d,
            MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
        ))
        .order_by(MetricsSnapshot.stat_date.desc())
    )
    rows = result.all()

    # 汇总
    total_spend = sum(float(r.spend or 0) for r in rows)
    total_orders = sum(int(r.orders or 0) for r in rows)
    total_revenue = sum(float(r.revenue or 0) for r in rows)

    orders_list = []
    for r in rows:
        if (r.orders and r.orders > 0) or (r.spend and r.spend > 0):
            orders_list.append({
                "stat_date": str(r.stat_date),
                "campaign_id": r.campaign_id,
                "campaign_name": r.campaign_name or "",
                "campaign_type": "GMVMAX" if r.data_level == "GMVMAX_CAMPAIGN" else "AUCTION",
                "spend": round(float(r.spend or 0), 2),
                "orders": int(r.orders or 0),
                "revenue": round(float(r.revenue or 0), 2),
                "roi": round(float(r.roi or 0), 2),
                "cost_per_order": round(float(r.cost_per_order or 0), 2),
            })

    return {
        "advertiser_id": advertiser_id,
        "date_range": {"start": start_date, "end": end_date},
        "summary": {
            "total_spend": round(total_spend, 2),
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "avg_order_value": round(total_revenue / total_orders, 2) if total_orders > 0 else 0,
            "overall_roi": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
        },
        "total_records": len(orders_list),
        "orders": orders_list,
    }


@router.get("/summary/{advertiser_id}")
async def get_order_summary(
    advertiser_id: str,
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD，默认最近 7 天"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
):
    """
    按 Campaign 维度汇总订单数据
    """
    if not end_date:
        end_date = date.today().isoformat()
    if not start_date:
        start_date = (date.today() - timedelta(days=7)).isoformat()

    start_d = date.fromisoformat(start_date)
    end_d = date.fromisoformat(end_date)

    result = await db.execute(
        select(
            MetricsSnapshot.object_id.label("campaign_id"),
            MetricsSnapshot.object_name.label("campaign_name"),
            MetricsSnapshot.data_level,
            func.sum(MetricsSnapshot.spend).label("total_spend"),
            func.sum(MetricsSnapshot.conversion).label("total_orders"),
            func.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
            (func.sum(MetricsSnapshot.gross_revenue) / func.nullif(func.sum(MetricsSnapshot.spend), 0)).label("avg_roi"),
            func.avg(MetricsSnapshot.cost_per_conversion).label("avg_cost_per_order"),
        )
        .where(and_(
            MetricsSnapshot.advertiser_id == advertiser_id,
            MetricsSnapshot.stat_date >= start_d,
            MetricsSnapshot.stat_date <= end_d,
            MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
        ))
        .group_by(
            MetricsSnapshot.object_id,
            MetricsSnapshot.object_name,
            MetricsSnapshot.data_level,
        )
        .order_by(func.sum(MetricsSnapshot.spend).desc())
    )
    rows = result.all()

    campaigns = []
    grand_spend = 0
    grand_orders = 0
    grand_revenue = 0

    for r in rows:
        spend = float(r.total_spend or 0)
        orders = int(r.total_orders or 0)
        revenue = float(r.total_revenue or 0)
        grand_spend += spend
        grand_orders += orders
        grand_revenue += revenue

        campaigns.append({
            "campaign_id": r.campaign_id,
            "campaign_name": r.campaign_name or "",
            "campaign_type": "GMVMAX" if r.data_level == "GMVMAX_CAMPAIGN" else "AUCTION",
            "total_spend": round(spend, 2),
            "total_orders": orders,
            "total_revenue": round(revenue, 2),
            "avg_roi": round(float(r.avg_roi or 0), 2),
            "avg_cost_per_order": round(float(r.avg_cost_per_order or 0), 2),
            "avg_order_value": round(revenue / orders, 2) if orders > 0 else 0,
        })

    return {
        "advertiser_id": advertiser_id,
        "date_range": {"start": start_date, "end": end_date},
        "summary": {
            "total_campaigns": len(campaigns),
            "total_spend": round(grand_spend, 2),
            "total_orders": grand_orders,
            "total_revenue": round(grand_revenue, 2),
            "avg_order_value": round(grand_revenue / grand_orders, 2) if grand_orders > 0 else 0,
            "overall_roi": round(grand_revenue / grand_spend, 2) if grand_spend > 0 else 0,
        },
        "campaigns": campaigns,
    }
