"""
广告层级查询 API — Campaign / Ad 粒度的数据查询
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.models.metrics import MetricsSnapshot

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


# ---------------------------------------------------------------------------
# GET /campaigns
# ---------------------------------------------------------------------------

@router.get("")
async def list_campaigns(
    advertiser_id: Optional[str] = None,
    shop_id: Optional[str] = None,
    days: int = Query(7, ge=1, le=90),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """查询 Campaign 列表，按 campaign_id 聚合近 N 天数据"""
    since = date.today() - timedelta(days=days)

    conditions = [
        MetricsSnapshot.stat_date >= since,
        MetricsSnapshot.data_level.in_(["CAMPAIGN", "GMVMAX_CAMPAIGN"]),
    ]
    if advertiser_id:
        conditions.append(MetricsSnapshot.advertiser_id == advertiser_id)
    _has_shop_id = hasattr(MetricsSnapshot, "shop_id")
    if shop_id:
        if _has_shop_id:
            conditions.append(MetricsSnapshot.shop_id == shop_id)
        else:
            conditions.append(MetricsSnapshot.advertiser_id == shop_id)

    # 聚合查询（含 GMVMax 字段）
    # 注意：object_name 不放进 GROUP BY，改用 MAX() 取最新名称，避免同一 campaign_id 出现多行
    query = (
        select(
            MetricsSnapshot.object_id.label("campaign_id"),
            func.max(MetricsSnapshot.object_name).label("campaign_name"),
            MetricsSnapshot.advertiser_id,
            MetricsSnapshot.data_level,
            func.sum(MetricsSnapshot.spend).label("total_spend"),
            func.sum(MetricsSnapshot.impressions).label("total_impressions"),
            func.sum(MetricsSnapshot.clicks).label("total_clicks"),
            func.sum(MetricsSnapshot.conversion).label("total_conversion"),
            func.avg(MetricsSnapshot.ctr).label("avg_ctr"),
            func.avg(MetricsSnapshot.cpc).label("avg_cpc"),
            func.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
        )
        .where(and_(*conditions))
        .group_by(
            MetricsSnapshot.object_id,
            MetricsSnapshot.advertiser_id,
            MetricsSnapshot.data_level,
        )
        .order_by(func.sum(MetricsSnapshot.spend).desc())
    )

    # 总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页
    offset = (page - 1) * page_size
    paginated = query.offset(offset).limit(page_size)
    result = await db.execute(paginated)
    rows = result.all()

    def _calc_roi(spend, revenue):
        """ROI = GMV / Spend，不用 AVG(roi) 避免被零值行拉低"""
        s = float(spend or 0)
        r = float(revenue or 0)
        return round(r / s, 4) if s > 0 else 0.0

    return {
        "days": days,
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": [
            {
                "campaign_id": r.campaign_id,
                "campaign_name": r.campaign_name,
                "advertiser_id": r.advertiser_id,
                "campaign_type": "GMVMAX" if r.data_level == "GMVMAX_CAMPAIGN" else "AUCTION",
                "total_spend": round(r.total_spend or 0, 2),
                "total_impressions": r.total_impressions or 0,
                "total_clicks": r.total_clicks or 0,
                "total_conversion": r.total_conversion or 0,
                "total_revenue": round(r.total_revenue or 0, 2),
                "avg_roi": _calc_roi(r.total_spend, r.total_revenue),
                "avg_ctr": round(r.avg_ctr or 0, 4),
                "avg_cpc": round(r.avg_cpc or 0, 4),
            }
            for r in rows
        ],
    }


# ---------------------------------------------------------------------------
# GET /campaigns/ads/top  ← 必须在 /{campaign_id}/ads 之前注册，避免路由冲突
# ---------------------------------------------------------------------------

@router.get("/ads/top")
async def top_ads(
    advertiser_id: Optional[str] = None,
    shop_id: Optional[str] = None,
    metric: str = Query("spend", description="排序指标: spend / conversion / ctr"),
    limit: int = Query(20, ge=1, le=100),
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
):
    """获取 Top N 广告（按指定指标降序）"""
    since = date.today() - timedelta(days=days)

    allowed_metrics = {"spend", "conversion", "ctr"}
    if metric not in allowed_metrics:
        metric = "spend"

    conditions = [
        MetricsSnapshot.stat_date >= since,
        MetricsSnapshot.data_level == "AD",
    ]
    if advertiser_id:
        conditions.append(MetricsSnapshot.advertiser_id == advertiser_id)
    _has_shop_id = hasattr(MetricsSnapshot, "shop_id")
    if shop_id:
        if _has_shop_id:
            conditions.append(MetricsSnapshot.shop_id == shop_id)
        else:
            conditions.append(MetricsSnapshot.advertiser_id == shop_id)

    # 按 ad 聚合
    agg_spend = func.sum(MetricsSnapshot.spend).label("spend")
    agg_impressions = func.sum(MetricsSnapshot.impressions).label("impressions")
    agg_clicks = func.sum(MetricsSnapshot.clicks).label("clicks")
    agg_conversion = func.sum(MetricsSnapshot.conversion).label("conversion")
    agg_ctr = func.avg(MetricsSnapshot.ctr).label("ctr")
    agg_cpc = func.avg(MetricsSnapshot.cpc).label("cpc")
    agg_cvr = func.avg(MetricsSnapshot.conversion_rate).label("conversion_rate")

    sort_map = {
        "spend": func.sum(MetricsSnapshot.spend).desc(),
        "conversion": func.sum(MetricsSnapshot.conversion).desc(),
        "ctr": func.avg(MetricsSnapshot.ctr).desc(),
    }

    query = (
        select(
            MetricsSnapshot.object_id.label("ad_id"),
            MetricsSnapshot.object_name.label("ad_name"),
            MetricsSnapshot.adgroup_id,
            MetricsSnapshot.campaign_id,
            MetricsSnapshot.advertiser_id,
            agg_spend,
            agg_impressions,
            agg_clicks,
            agg_conversion,
            agg_ctr,
            agg_cpc,
            agg_cvr,
        )
        .where(and_(*conditions))
        .group_by(
            MetricsSnapshot.object_id,
            MetricsSnapshot.object_name,
            MetricsSnapshot.adgroup_id,
            MetricsSnapshot.campaign_id,
            MetricsSnapshot.advertiser_id,
        )
        .order_by(sort_map[metric])
        .limit(limit)
    )

    result = await db.execute(query)
    rows = result.all()

    return {
        "days": days,
        "metric": metric,
        "limit": limit,
        "items": [
            {
                "ad_id": r.ad_id,
                "ad_name": r.ad_name,
                "adgroup_id": r.adgroup_id,
                "campaign_id": r.campaign_id,
                "advertiser_id": r.advertiser_id,
                "spend": round(r.spend or 0, 2),
                "impressions": r.impressions or 0,
                "clicks": r.clicks or 0,
                "ctr": round(r.ctr or 0, 4),
                "cpc": round(r.cpc or 0, 4),
                "conversion": r.conversion or 0,
                "conversion_rate": round(r.conversion_rate or 0, 4),
                "roas": None,  # 暂无 GMV 字段，返回 null
            }
            for r in rows
        ],
    }


# ---------------------------------------------------------------------------
# GET /campaigns/{campaign_id}/trend
# ---------------------------------------------------------------------------

@router.get("/{campaign_id}/trend")
async def campaign_trend(
    campaign_id: str,
    days: int = Query(14, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
):
    """获取单个 Campaign 的每日趋势数据"""
    since = date.today() - timedelta(days=days)

    query = (
        select(
            MetricsSnapshot.stat_date,
            func.sum(MetricsSnapshot.spend).label("spend"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
            func.sum(MetricsSnapshot.impressions).label("impressions"),
            func.sum(MetricsSnapshot.clicks).label("clicks"),
        )
        .where(
            and_(
                MetricsSnapshot.object_id == campaign_id,
                MetricsSnapshot.data_level.in_(["CAMPAIGN", "GMVMAX_CAMPAIGN"]),
                MetricsSnapshot.stat_date >= since,
            )
        )
        .group_by(MetricsSnapshot.stat_date)
        .order_by(MetricsSnapshot.stat_date.asc())
    )

    result = await db.execute(query)
    rows = result.all()

    def _roi(spend, gmv):
        s = float(spend or 0)
        g = float(gmv or 0)
        return round(g / s, 4) if s > 0 else 0.0

    return {
        "campaign_id": campaign_id,
        "days": days,
        "trend": [
            {
                "date": str(r.stat_date),
                "spend": round(r.spend or 0, 2),
                "gmv": round(r.gmv or 0, 2),
                "orders": r.orders or 0,
                "impressions": r.impressions or 0,
                "clicks": r.clicks or 0,
                "roi": _roi(r.spend, r.gmv),
            }
            for r in rows
        ],
    }


# ---------------------------------------------------------------------------
# GET /campaigns/ads/{ad_id}/trend
# ---------------------------------------------------------------------------

@router.get("/ads/{ad_id}/trend")
async def ad_trend(
    ad_id: str,
    days: int = Query(14, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
):
    """获取单条广告的每日趋势数据"""
    since = date.today() - timedelta(days=days)

    query = (
        select(
            MetricsSnapshot.stat_date,
            func.sum(MetricsSnapshot.spend).label("spend"),
            func.sum(MetricsSnapshot.impressions).label("impressions"),
            func.sum(MetricsSnapshot.clicks).label("clicks"),
            func.sum(MetricsSnapshot.conversion).label("conversion"),
            func.avg(MetricsSnapshot.ctr).label("ctr"),
            func.avg(MetricsSnapshot.cpc).label("cpc"),
            func.avg(MetricsSnapshot.cpm).label("cpm"),
            func.avg(MetricsSnapshot.conversion_rate).label("conversion_rate"),
        )
        .where(
            and_(
                MetricsSnapshot.object_id == ad_id,
                MetricsSnapshot.data_level == "AD",
                MetricsSnapshot.stat_date >= since,
            )
        )
        .group_by(MetricsSnapshot.stat_date)
        .order_by(MetricsSnapshot.stat_date.asc())
    )

    result = await db.execute(query)
    rows = result.all()

    return {
        "ad_id": ad_id,
        "days": days,
        "data": [
            {
                "date": str(r.stat_date),
                "spend": round(r.spend or 0, 2),
                "impressions": r.impressions or 0,
                "clicks": r.clicks or 0,
                "conversion": r.conversion or 0,
                "ctr": round(r.ctr or 0, 4),
                "cpc": round(r.cpc or 0, 4),
                "cpm": round(r.cpm or 0, 4),
                "conversion_rate": round(r.conversion_rate or 0, 4),
                "roas": None,  # 暂无 GMV 字段，返回 null
            }
            for r in rows
        ],
    }


# ---------------------------------------------------------------------------
# GET /campaigns/{campaign_id}/ads
# ---------------------------------------------------------------------------

@router.get("/{campaign_id}/ads")
async def campaign_ads(
    campaign_id: str,
    days: int = Query(7, ge=1, le=90),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """查询某 Campaign 下所有 Ad 的聚合数据（跳过 adgroup 层级）"""
    since = date.today() - timedelta(days=days)

    conditions = [
        MetricsSnapshot.campaign_id == campaign_id,
        MetricsSnapshot.data_level == "AD",
        MetricsSnapshot.stat_date >= since,
    ]

    query = (
        select(
            MetricsSnapshot.object_id.label("ad_id"),
            MetricsSnapshot.object_name.label("ad_name"),
            MetricsSnapshot.adgroup_id,
            MetricsSnapshot.campaign_id,
            func.sum(MetricsSnapshot.spend).label("spend"),
            func.sum(MetricsSnapshot.impressions).label("impressions"),
            func.sum(MetricsSnapshot.clicks).label("clicks"),
            func.sum(MetricsSnapshot.conversion).label("conversion"),
            func.avg(MetricsSnapshot.ctr).label("ctr"),
            func.avg(MetricsSnapshot.cpc).label("cpc"),
            func.avg(MetricsSnapshot.conversion_rate).label("conversion_rate"),
        )
        .where(and_(*conditions))
        .group_by(
            MetricsSnapshot.object_id,
            MetricsSnapshot.object_name,
            MetricsSnapshot.adgroup_id,
            MetricsSnapshot.campaign_id,
        )
        .order_by(func.sum(MetricsSnapshot.spend).desc())
    )

    # 总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页
    offset = (page - 1) * page_size
    paginated = query.offset(offset).limit(page_size)
    result = await db.execute(paginated)
    rows = result.all()

    return {
        "campaign_id": campaign_id,
        "days": days,
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": [
            {
                "ad_id": r.ad_id,
                "ad_name": r.ad_name,
                "adgroup_id": r.adgroup_id,
                "campaign_id": r.campaign_id,
                "spend": round(r.spend or 0, 2),
                "impressions": r.impressions or 0,
                "clicks": r.clicks or 0,
                "ctr": round(r.ctr or 0, 4),
                "cpc": round(r.cpc or 0, 4),
                "conversion": r.conversion or 0,
                "conversion_rate": round(r.conversion_rate or 0, 4),
                "roas": None,  # 暂无 GMV 字段，返回 null
            }
            for r in rows
        ],
    }
