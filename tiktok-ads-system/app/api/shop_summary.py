"""
店铺汇总接口（shop_summary）

GET /shop-summary/list          获取当前账户下绑定的店铺 id/名称列表
GET /shop-summary/overview      按店铺维度聚合大盘数据（spend/gmv/orders/roi/top_campaigns）
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.metrics import MetricsSnapshot

router = APIRouter(prefix="/shop-summary", tags=["Shop Summary"])


@router.get("/list")
async def shop_list(db: AsyncSession = Depends(get_db)):
    """
    返回店铺列表（优先从 stores 表读取，前端全局筛选器使用）
    返回格式：{id, name, advertiser_id} — 前端 globalFilterStore 需要 id/name
    """
    from app.models.store import Store
    from app.models.advertiser import Advertiser

    # 优先从 stores 表读
    result = await db.execute(select(Store).where(Store.is_active == True))
    stores = result.scalars().all()

    if stores:
        return {
            "total": len(stores),
            "shops": [
                {"id": s.store_id, "name": s.store_name or s.store_id, "advertiser_id": s.advertiser_id}
                for s in stores
            ],
        }

    # Fallback: 从 advertisers 表生成（没有 stores 数据时）
    result = await db.execute(
        select(Advertiser).where(Advertiser.is_active == True, Advertiser.is_token_valid == True)
    )
    advertisers = result.scalars().all()
    return {
        "total": len(advertisers),
        "shops": [
            {"id": a.advertiser_id, "name": a.advertiser_name or a.advertiser_id, "advertiser_id": a.advertiser_id}
            for a in advertisers
        ],
    }


@router.get("/overview")
async def shop_overview(
    shop_id: Optional[str] = Query(None, description="店铺 ID，为空时返回全部汇总"),
    days: int = Query(7, ge=1, le=90, description="统计天数"),
    db: AsyncSession = Depends(get_db),
):
    """
    按店铺维度聚合大盘数据
    返回：spend, gmv, orders, roi, top_campaigns[]
    """
    since = date.today() - timedelta(days=days)
    today = date.today()

    has_shop_id = hasattr(MetricsSnapshot, "shop_id")

    # ---- 基础聚合条件 ----
    base_conditions = [
        MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
        MetricsSnapshot.stat_date >= since,
        MetricsSnapshot.stat_date <= today,
    ]

    if shop_id and has_shop_id:
        base_conditions.append(MetricsSnapshot.shop_id == shop_id)
    elif shop_id and not has_shop_id:
        # 无 shop_id 列时，把 shop_id 当 advertiser_id 处理（降级）
        base_conditions.append(MetricsSnapshot.advertiser_id == shop_id)

    # ---- 汇总数据 ----
    summary_result = await db.execute(
        select(
            func.sum(MetricsSnapshot.spend).label("spend"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
        ).where(*base_conditions)
    )
    summary = summary_result.one()
    spend = float(summary.spend or 0)
    gmv = float(summary.gmv or 0)
    orders = int(summary.orders or 0)
    roi = round(gmv / spend, 4) if spend > 0 else 0.0

    # ---- Top Campaigns（按 GMV 倒序，今日数据）----
    top_conditions = [
        MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
        MetricsSnapshot.stat_date == today,
    ]
    if shop_id and has_shop_id:
        top_conditions.append(MetricsSnapshot.shop_id == shop_id)
    elif shop_id and not has_shop_id:
        top_conditions.append(MetricsSnapshot.advertiser_id == shop_id)

    top_result = await db.execute(
        select(
            MetricsSnapshot.object_id.label("campaign_id"),
            MetricsSnapshot.object_name.label("campaign_name"),
            func.sum(MetricsSnapshot.spend).label("spend"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
        )
        .where(*top_conditions)
        .group_by(MetricsSnapshot.object_id, MetricsSnapshot.object_name)
        .order_by(func.sum(MetricsSnapshot.gross_revenue).desc())
        .limit(10)
    )
    top_rows = top_result.all()
    top_campaigns = []
    for r in top_rows:
        c_spend = float(r.spend or 0)
        c_gmv = float(r.gmv or 0)
        c_orders = int(r.orders or 0)
        top_campaigns.append({
            "campaign_id": r.campaign_id,
            "campaign_name": r.campaign_name or "",
            "spend": round(c_spend, 2),
            "gmv": round(c_gmv, 2),
            "orders": c_orders,
            "roi": round(c_gmv / c_spend, 4) if c_spend > 0 else 0.0,
        })

    return {
        "shop_id": shop_id,
        "days": days,
        "spend": round(spend, 2),
        "gmv": round(gmv, 2),
        "orders": orders,
        "roi": roi,
        "top_campaigns": top_campaigns,
    }
