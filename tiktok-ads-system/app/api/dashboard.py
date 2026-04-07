"""
Dashboard 统计接口 — 给前端提供数据
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.models.metrics import MetricsSnapshot
from app.models.decision import Decision
from app.models.alert import Alert

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview")
async def overview(
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """系统总览：账户数、今日花费、告警数、待处理决策数"""
    today = date.today()

    # 账户统计
    adv_result = await db.execute(
        select(
            func.count(Advertiser.id).label("total"),
            func.sum(func.IF(Advertiser.is_active == True, 1, 0)).label("active"),
            func.sum(func.IF(Advertiser.is_token_valid == False, 1, 0)).label("token_expired"),
        )
    )
    adv_stats = adv_result.one()

    # shop_id 过滤辅助
    _has_shop_id = hasattr(MetricsSnapshot, "shop_id")

    def _shop_filter(q):
        if not shop_id:
            return q
        if _has_shop_id:
            return q.where(MetricsSnapshot.shop_id == shop_id)
        return q.where(MetricsSnapshot.advertiser_id == shop_id)

    # 今日总花费（普通 Ad + GMVMax）
    spend_result = await db.execute(
        _shop_filter(
            select(func.sum(MetricsSnapshot.spend))
            .where(
                MetricsSnapshot.stat_date == today,
                MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
            )
        )
    )
    today_spend = spend_result.scalar() or 0.0

    # 今日 GMVMax 收入
    gmvmax_result = await db.execute(
        _shop_filter(
            select(
                func.sum(MetricsSnapshot.gross_revenue).label("revenue"),
                func.sum(MetricsSnapshot.conversion).label("orders"),
            )
            .where(
                MetricsSnapshot.stat_date == today,
                MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
            )
        )
    )
    gmvmax_stats = gmvmax_result.one()
    today_gmvmax_revenue = gmvmax_stats.revenue or 0.0
    today_gmvmax_orders = gmvmax_stats.orders or 0

    # 未解决告警
    alert_result = await db.execute(
        select(
            func.count(Alert.id).label("total"),
            func.sum(func.IF(Alert.severity == "CRITICAL", 1, 0)).label("critical"),
            func.sum(func.IF(Alert.severity == "WARNING", 1, 0)).label("warning"),
        ).where(Alert.is_resolved == False)
    )
    alert_stats = alert_result.one()

    # 待处理决策
    pending_result = await db.execute(
        select(func.count(Decision.id)).where(Decision.status == "PENDING")
    )
    pending_decisions = pending_result.scalar() or 0

    return {
        "advertisers": {
            "total": adv_stats.total or 0,
            "active": adv_stats.active or 0,
            "token_expired": adv_stats.token_expired or 0,
        },
        "today_spend": round(today_spend, 2),
        "gmvmax": {
            "today_revenue": round(today_gmvmax_revenue, 2),
            "today_orders": today_gmvmax_orders,
        },
        "alerts": {
            "unresolved": alert_stats.total or 0,
            "critical": alert_stats.critical or 0,
            "warning": alert_stats.warning or 0,
        },
        "pending_decisions": pending_decisions,
    }


@router.get("/spend-trend")
async def spend_trend(
    days: int = Query(7, le=30),
    advertiser_id: Optional[str] = None,
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """最近 N 天的每日花费趋势"""
    since = date.today() - timedelta(days=days)

    query = (
        select(
            MetricsSnapshot.stat_date,
            func.sum(MetricsSnapshot.spend).label("total_spend"),
            func.sum(MetricsSnapshot.impressions).label("total_impressions"),
            func.sum(MetricsSnapshot.clicks).label("total_clicks"),
            func.sum(MetricsSnapshot.conversion).label("total_conversion"),
            func.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
        )
        .where(
            MetricsSnapshot.stat_date >= since,
            MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
        )
        .group_by(MetricsSnapshot.stat_date)
        .order_by(MetricsSnapshot.stat_date.asc())
    )

    if advertiser_id:
        query = query.where(MetricsSnapshot.advertiser_id == advertiser_id)
    if shop_id:
        _has_sid = hasattr(MetricsSnapshot, "shop_id")
        if _has_sid:
            query = query.where(MetricsSnapshot.shop_id == shop_id)
        else:
            query = query.where(MetricsSnapshot.advertiser_id == shop_id)

    result = await db.execute(query)
    rows = result.all()

    return {
        "days": days,
        "data": [
            {
                "date": str(r.stat_date),
                "spend": round(r.total_spend or 0, 2),
                "impressions": r.total_impressions or 0,
                "clicks": r.total_clicks or 0,
                "conversion": r.total_conversion or 0,
                "revenue": round(r.total_revenue or 0, 2),
                "ctr": round((r.total_clicks or 0) / (r.total_impressions or 1) * 100, 2),
            }
            for r in rows
        ],
    }


@router.get("/gmvmax-overview")
async def gmvmax_overview(
    advertiser_id: Optional[str] = None,
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    GMVMax 专属总览
    返回今日、昨日、近7日汇总数据，以及趋势和 Top Campaigns
    data_level='GMVMAX_CAMPAIGN'
    """
    today = date.today()
    yesterday = today - timedelta(days=1)
    seven_days_ago = today - timedelta(days=7)

    _has_shop_id = hasattr(MetricsSnapshot, "shop_id")

    def _base_query(start: date, end: date):
        q = (
            select(
                func.sum(MetricsSnapshot.spend).label("spend"),
                func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
                func.sum(MetricsSnapshot.conversion).label("orders"),
            )
            .where(
                MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
                MetricsSnapshot.stat_date >= start,
                MetricsSnapshot.stat_date <= end,
            )
        )
        if advertiser_id:
            q = q.where(MetricsSnapshot.advertiser_id == advertiser_id)
        if shop_id:
            if _has_shop_id:
                q = q.where(MetricsSnapshot.shop_id == shop_id)
            else:
                q = q.where(MetricsSnapshot.advertiser_id == shop_id)
        return q

    def _calc_period(spend, gmv, orders):
        spend = float(spend or 0)
        gmv = float(gmv or 0)
        orders = int(orders or 0)
        roi = round(gmv / spend, 4) if spend > 0 else 0.0
        cost_per_order = round(spend / orders, 4) if orders > 0 else 0.0
        return {
            "spend": round(spend, 2),
            "gmv": round(gmv, 2),
            "orders": orders,
            "roi": roi,
            "cost_per_order": cost_per_order,
        }

    # 今日
    r_today = (await db.execute(_base_query(today, today))).one()
    # 昨日
    r_yesterday = (await db.execute(_base_query(yesterday, yesterday))).one()
    # 近7天
    r_7d = (await db.execute(_base_query(seven_days_ago, today))).one()

    # 趋势（近7天每日）
    trend_query = (
        select(
            MetricsSnapshot.stat_date,
            func.sum(MetricsSnapshot.spend).label("spend"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
        )
        .where(
            MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
            MetricsSnapshot.stat_date >= seven_days_ago,
            MetricsSnapshot.stat_date <= today,
        )
        .group_by(MetricsSnapshot.stat_date)
        .order_by(MetricsSnapshot.stat_date.asc())
    )
    if advertiser_id:
        trend_query = trend_query.where(MetricsSnapshot.advertiser_id == advertiser_id)
    if shop_id:
        if _has_shop_id:
            trend_query = trend_query.where(MetricsSnapshot.shop_id == shop_id)
        else:
            trend_query = trend_query.where(MetricsSnapshot.advertiser_id == shop_id)
    trend_rows = (await db.execute(trend_query)).all()

    trend = []
    for row in trend_rows:
        spend = float(row.spend or 0)
        gmv = float(row.gmv or 0)
        orders = int(row.orders or 0)
        trend.append({
            "date": str(row.stat_date),
            "spend": round(spend, 2),
            "gmv": round(gmv, 2),
            "orders": orders,
            "roi": round(gmv / spend, 4) if spend > 0 else 0.0,
        })

    # Top Campaigns（今日，按 GMV 倒序）
    top_query = (
        select(
            MetricsSnapshot.object_id.label("campaign_id"),
            MetricsSnapshot.object_name,
            func.sum(MetricsSnapshot.spend).label("spend"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
        )
        .where(
            MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
            MetricsSnapshot.stat_date == today,
        )
        .group_by(MetricsSnapshot.object_id, MetricsSnapshot.object_name)
        .order_by(func.sum(MetricsSnapshot.gross_revenue).desc())
        .limit(10)
    )
    if advertiser_id:
        top_query = top_query.where(MetricsSnapshot.advertiser_id == advertiser_id)
    if shop_id:
        if _has_shop_id:
            top_query = top_query.where(MetricsSnapshot.shop_id == shop_id)
        else:
            top_query = top_query.where(MetricsSnapshot.advertiser_id == shop_id)
    top_rows = (await db.execute(top_query)).all()

    top_campaigns = []
    for row in top_rows:
        spend = float(row.spend or 0)
        gmv = float(row.gmv or 0)
        orders = int(row.orders or 0)
        top_campaigns.append({
            "campaign_id": row.campaign_id,
            "campaign_name": row.object_name or "",
            "spend": round(spend, 2),
            "gmv": round(gmv, 2),
            "orders": orders,
            "roi": round(gmv / spend, 4) if spend > 0 else 0.0,
        })

    return {
        "today": _calc_period(r_today.spend, r_today.gmv, r_today.orders),
        "yesterday": _calc_period(r_yesterday.spend, r_yesterday.gmv, r_yesterday.orders),
        "last_7d": _calc_period(r_7d.spend, r_7d.gmv, r_7d.orders),
        "trend": trend,
        "top_campaigns": top_campaigns,
    }


@router.get("/top-ads")
async def top_ads(
    metric: str = Query("spend", description="排序指标: spend/conversion/ctr/cpm"),
    date_str: Optional[str] = Query(None, description="日期 YYYY-MM-DD，默认今天"),
    limit: int = Query(20, le=100),
    shop_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """今日 Top Ad 排行"""
    target_date = date.fromisoformat(date_str) if date_str else date.today()

    allowed = {"spend", "conversion", "ctr", "cpm", "clicks", "impressions"}
    if metric not in allowed:
        metric = "spend"

    sort_col = getattr(MetricsSnapshot, metric)

    _top_q = (
        select(MetricsSnapshot)
        .where(
            MetricsSnapshot.stat_date == target_date,
            MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
        )
        .order_by(sort_col.desc())
        .limit(limit)
    )
    if shop_id:
        _has_sid = hasattr(MetricsSnapshot, "shop_id")
        if _has_sid:
            _top_q = _top_q.where(MetricsSnapshot.shop_id == shop_id)
        else:
            _top_q = _top_q.where(MetricsSnapshot.advertiser_id == shop_id)
    result = await db.execute(_top_q)
    ads = result.scalars().all()

    return {
        "date": str(target_date),
        "sort_by": metric,
        "items": [
            {
                "advertiser_id": a.advertiser_id,
                "object_id": a.object_id,
                "object_name": a.object_name,
                "data_level": a.data_level,
                "spend": a.spend,
                "impressions": a.impressions,
                "clicks": a.clicks,
                "ctr": a.ctr,
                "cpm": a.cpm,
                "conversion": a.conversion,
                "cost_per_conversion": a.cost_per_conversion,
                "gross_revenue": a.gross_revenue,
                "roi": a.roi,
            }
            for a in ads
        ],
    }
