"""
店铺管理与分析接口

GET    /shops/list                    获取所有店铺列表及汇总指标
GET    /shops/{store_id}/detail       获取单个店铺的详细信息（商品列表 + 每日趋势）
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy import select, func, and_, distinct, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.models.metrics import MetricsSnapshot
from app.models.store import Store
from app.services.tiktok_client import TikTokClient

router = APIRouter(prefix="/shops", tags=["Shop Management"])


def _safe_div(numerator, denominator, default=0.0):
    """安全除法，避免除零错误"""
    if not denominator:
        return default
    return round(numerator / denominator, 6)


@router.get("/list")
async def list_shops(
    days: int = Query(30, ge=1, le=90, description="统计天数"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取所有店铺列表及汇总指标

    从活跃广告主获取关联店铺，并从 metrics_snapshots 聚合各层级指标。
    """
    since = date.today() - timedelta(days=days)

    # 1. 获取所有活跃广告主
    adv_result = await db.execute(
        select(Advertiser).where(
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertisers = adv_result.scalars().all()

    if not advertisers:
        return {"total": 0, "days": days, "shops": []}

    shops = []

    # 优先从 DB stores 表读取（同步任务会定期写入）
    db_stores_result = await db.execute(select(Store).where(Store.is_active == True))
    db_stores = db_stores_result.scalars().all()

    if not db_stores:
        # DB 没有店铺数据，尝试实时调 API（首次使用或同步还没跑过）
        for adv in advertisers:
            client = TikTokClient(access_token=adv.access_token, advertiser_id=adv.advertiser_id)
            try:
                api_stores = await client.get_gmvmax_store_list()
                for s in (api_stores or []):
                    sid = str(s.get("store_id") or "")
                    if sid:
                        db_stores.append(Store(
                            store_id=sid,
                            store_name=s.get("store_name", ""),
                            store_type=s.get("store_type", ""),
                            advertiser_id=adv.advertiser_id,
                            store_authorized_bc_id=str(s.get("store_authorized_bc_id") or ""),
                            region=",".join(s.get("targeting_region_codes", [])),
                        ))
            except Exception as e:
                logger.warning(f"[Shops] API failed for {adv.advertiser_id}: {e}")
            finally:
                await client.close()

    for store in db_stores:
        store_id = store.store_id
        store_name = store.store_name or ""
        store_type = store.store_type or ""
        region = store.region or ""
        bc_id = store.store_authorized_bc_id or ""
        adv_id = store.advertiser_id or ""

        # --- 聚合 GMVMAX_CAMPAIGN 指标 ---
        campaign_result = await db.execute(
            select(
                func.coalesce(func.sum(MetricsSnapshot.spend), 0.0).label("total_spend"),
                func.coalesce(func.sum(MetricsSnapshot.conversion), 0).label("total_orders"),
                func.coalesce(func.sum(MetricsSnapshot.gross_revenue), 0.0).label("total_revenue"),
            ).where(and_(
                MetricsSnapshot.advertiser_id == adv_id,
                MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
                MetricsSnapshot.stat_date >= since,
            ))
        )
        cr = campaign_result.one()
        total_spend = float(cr.total_spend or 0)
        total_orders = int(cr.total_orders or 0)
        total_revenue = float(cr.total_revenue or 0)

        # --- 聚合 GMVMAX_ITEM 指标 ---
        item_result = await db.execute(
            select(func.count(distinct(MetricsSnapshot.object_id)).label("n")).where(and_(
                MetricsSnapshot.advertiser_id == adv_id,
                MetricsSnapshot.data_level == "GMVMAX_ITEM",
                MetricsSnapshot.stat_date >= since,
            ))
        )
        total_products = int(item_result.scalar() or 0)

        # --- 聚合 GMVMAX_CREATIVE 指标 ---
        creative_result = await db.execute(
            select(
                func.count(distinct(MetricsSnapshot.object_id)).label("total_creatives"),
                func.coalesce(func.sum(MetricsSnapshot.impressions), 0).label("total_impressions"),
                func.coalesce(func.sum(MetricsSnapshot.clicks), 0).label("total_clicks"),
            ).where(and_(
                MetricsSnapshot.advertiser_id == adv_id,
                MetricsSnapshot.data_level == "GMVMAX_CREATIVE",
                MetricsSnapshot.stat_date >= since,
            ))
        )
        ccr = creative_result.one()
        total_creatives = int(ccr.total_creatives or 0)
        total_impressions = int(ccr.total_impressions or 0)
        total_clicks = int(ccr.total_clicks or 0)

        shops.append({
            "store_id": store_id,
            "store_name": store_name,
            "store_type": store_type,
            "region": region,
            "bc_id": bc_id,
            "advertiser_id": adv_id,
            "total_spend": round(total_spend, 2),
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "overall_roi": round(_safe_div(total_revenue, total_spend), 4),
            "total_products": total_products,
            "total_creatives": total_creatives,
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "click_rate": round(_safe_div(total_clicks, total_impressions) * 100, 2),
            "order_rate": round(_safe_div(total_orders, total_clicks) * 100, 2),
            "impression_to_order_rate": round(_safe_div(total_orders, total_impressions) * 100, 4),
        })

    return {"total": len(shops), "days": days, "shops": shops}


@router.get("/{store_id}/detail")
async def shop_detail(
    store_id: str,
    days: int = Query(30, ge=1, le=90, description="统计天数"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取单个店铺的详细信息

    包含：店铺基础信息、商品列表（含指标）、每日趋势数据
    """
    since = date.today() - timedelta(days=days)

    # 1. 查找与该 store 关联的广告主（遍历活跃广告主，调用 API 匹配 store_id）
    adv_result = await db.execute(
        select(Advertiser).where(
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertisers = adv_result.scalars().all()

    matched_adv = None
    store_info = None

    for adv in advertisers:
        client = TikTokClient(access_token=adv.access_token, advertiser_id=adv.advertiser_id)
        try:
            stores = await client.get_gmvmax_store_list()
            for s in (stores or []):
                if str(s.get("store_id") or "") == store_id:
                    matched_adv = adv
                    store_info = s
                    break
        except Exception as e:
            logger.warning(f"[Shops] Failed to get store list for {adv.advertiser_id}: {e}")
        finally:
            await client.close()
        if matched_adv:
            break

    # Fallback: 如果 store_id 是 inferred_ 开头，直接用广告主信息
    if not matched_adv and store_id.startswith("inferred_"):
        real_adv_id = store_id.replace("inferred_", "")
        for adv in advertisers:
            if adv.advertiser_id == real_adv_id:
                matched_adv = adv
                store_info = {
                    "store_id": store_id,
                    "store_name": adv.advertiser_name or real_adv_id,
                    "store_type": "TIKTOK_SHOP",
                    "targeting_region_codes": [],
                    "store_authorized_bc_id": "",
                }
                break

    if not matched_adv or not store_info:
        raise HTTPException(status_code=404, detail=f"Store {store_id} not found")

    store_name = store_info.get("store_name", "")
    store_type = store_info.get("store_type", "")
    region_codes = store_info.get("targeting_region_codes", [])
    region = ",".join(region_codes) if isinstance(region_codes, list) else str(region_codes or "")
    bc_id = store_info.get("store_authorized_bc_id", "")

    # 2. 获取商品列表（从 TikTok API 获取名称/图片等信息）
    product_info_map = {}  # item_group_id -> {title, image_url, ...}
    if bc_id:
        client = TikTokClient(access_token=matched_adv.access_token, advertiser_id=matched_adv.advertiser_id)
        try:
            api_products = await client.get_all_store_products(store_id=store_id, bc_id=bc_id)
            for p in (api_products or []):
                gid = str(p.get("item_group_id") or "")
                if gid:
                    product_info_map[gid] = {
                        "title": p.get("title", ""),
                        "image_url": p.get("product_image_url") or p.get("image_url", ""),
                        "min_price": p.get("min_price"),
                        "max_price": p.get("max_price"),
                    }
        except Exception as e:
            logger.warning(f"[Shops] Failed to get store products for {store_id}: {e}")
        finally:
            await client.close()

    # 3. 从 DB 聚合每个商品（GMVMAX_ITEM）的指标
    item_metrics_result = await db.execute(
        select(
            MetricsSnapshot.object_id,
            MetricsSnapshot.object_name,
            func.coalesce(func.sum(MetricsSnapshot.spend), 0.0).label("spend"),
            func.coalesce(func.sum(MetricsSnapshot.conversion), 0).label("orders"),
            func.coalesce(func.sum(MetricsSnapshot.gross_revenue), 0.0).label("revenue"),
        ).where(
            and_(
                MetricsSnapshot.advertiser_id == matched_adv.advertiser_id,
                MetricsSnapshot.data_level == "GMVMAX_ITEM",
                MetricsSnapshot.stat_date >= since,
            )
        ).group_by(
            MetricsSnapshot.object_id,
            MetricsSnapshot.object_name,
        )
    )
    item_rows = item_metrics_result.all()

    products = []
    for row in item_rows:
        item_group_id = row.object_id
        spend = float(row.spend or 0)
        revenue = float(row.revenue or 0)
        orders = int(row.orders or 0)
        roi = _safe_div(revenue, spend)

        # 用 API 数据补充商品信息
        api_info = product_info_map.get(item_group_id, {})

        products.append({
            "item_group_id": item_group_id,
            "name": api_info.get("title") or row.object_name or "",
            "image_url": api_info.get("image_url", ""),
            "min_price": api_info.get("min_price"),
            "max_price": api_info.get("max_price"),
            "spend": round(spend, 2),
            "orders": orders,
            "revenue": round(revenue, 2),
            "roi": round(roi, 4),
        })

    # 按 spend 降序排列
    products.sort(key=lambda x: x["spend"], reverse=True)

    # 4. 每日趋势数据（GMVMAX_CAMPAIGN + GMVMAX_CREATIVE 合并）
    # Campaign 层面：spend, revenue, orders
    daily_campaign_result = await db.execute(
        select(
            MetricsSnapshot.stat_date,
            func.coalesce(func.sum(MetricsSnapshot.spend), 0.0).label("spend"),
            func.coalesce(func.sum(MetricsSnapshot.gross_revenue), 0.0).label("revenue"),
            func.coalesce(func.sum(MetricsSnapshot.conversion), 0).label("orders"),
        ).where(
            and_(
                MetricsSnapshot.advertiser_id == matched_adv.advertiser_id,
                MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
                MetricsSnapshot.stat_date >= since,
            )
        ).group_by(MetricsSnapshot.stat_date).order_by(MetricsSnapshot.stat_date)
    )
    campaign_daily = {str(r.stat_date): {"spend": float(r.spend), "revenue": float(r.revenue), "orders": int(r.orders)} for r in daily_campaign_result.all()}

    # Creative 层面：impressions, clicks
    daily_creative_result = await db.execute(
        select(
            MetricsSnapshot.stat_date,
            func.coalesce(func.sum(MetricsSnapshot.impressions), 0).label("impressions"),
            func.coalesce(func.sum(MetricsSnapshot.clicks), 0).label("clicks"),
        ).where(
            and_(
                MetricsSnapshot.advertiser_id == matched_adv.advertiser_id,
                MetricsSnapshot.data_level == "GMVMAX_CREATIVE",
                MetricsSnapshot.stat_date >= since,
            )
        ).group_by(MetricsSnapshot.stat_date).order_by(MetricsSnapshot.stat_date)
    )
    creative_daily = {str(r.stat_date): {"impressions": int(r.impressions), "clicks": int(r.clicks)} for r in daily_creative_result.all()}

    # 合并两个数据源
    all_dates = sorted(set(list(campaign_daily.keys()) + list(creative_daily.keys())))
    daily_trend = []
    for d in all_dates:
        c = campaign_daily.get(d, {})
        cr = creative_daily.get(d, {})
        daily_trend.append({
            "date": d,
            "spend": round(c.get("spend", 0), 2),
            "revenue": round(c.get("revenue", 0), 2),
            "orders": c.get("orders", 0),
            "impressions": cr.get("impressions", 0),
            "clicks": cr.get("clicks", 0),
        })

    return {
        "store_id": store_id,
        "store_name": store_name,
        "store_type": store_type,
        "region": region,
        "bc_id": bc_id,
        "advertiser_id": matched_adv.advertiser_id,
        "days": days,
        "products": products,
        "daily_trend": daily_trend,
    }
