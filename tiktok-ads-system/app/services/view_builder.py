"""
视图构建器 — 同步完成后触发，将原始数据聚合到业务视图表
前端只查视图表，不依赖实时 API
"""
from datetime import date, timedelta
from typing import Dict, Any, Optional

from loguru import logger
from sqlalchemy import select, func, and_, distinct, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metrics import MetricsSnapshot
from app.models.creative import Creative
from app.models.store import Store
from app.models.views import ProductView, CreativeView, DailySummary


# ===================== Product View =====================

async def build_product_view(db: AsyncSession, days: int = 60):
    """
    构建商品视图：
    1. 从 TikTok Shop API 拿商品名/图片（通过 stores 表的 bc_id）
    2. 从 GMVMAX_ITEM 聚合投放指标
    3. UPSERT 到 product_view 表
    """
    since = date.today() - timedelta(days=days)

    # 1. 从 GMVMAX_ITEM 聚合
    result = await db.execute(
        select(
            MetricsSnapshot.object_id.label("item_group_id"),
            MetricsSnapshot.advertiser_id,
            func.sum(MetricsSnapshot.spend).label("total_spend"),
            func.sum(MetricsSnapshot.conversion).label("total_orders"),
            func.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
            func.count(distinct(MetricsSnapshot.stat_date)).label("active_days"),
            func.min(MetricsSnapshot.stat_date).label("first_seen"),
            func.max(MetricsSnapshot.stat_date).label("last_seen"),
        )
        .where(and_(
            MetricsSnapshot.data_level == "GMVMAX_ITEM",
            MetricsSnapshot.stat_date >= since,
        ))
        .group_by(MetricsSnapshot.object_id, MetricsSnapshot.advertiser_id)
    )
    item_rows = result.all()

    if not item_rows:
        logger.debug("[ViewBuilder] No GMVMAX_ITEM data, skip product_view build")
        return

    # 2. 获取商品信息（从 TikTok Shop API，带容错）
    product_info_map = await _fetch_product_info_safe(db)

    # 3. 获取每个商品的创意数
    creative_count_result = await db.execute(
        select(
            MetricsSnapshot.product_id,
            func.count(distinct(MetricsSnapshot.object_id)).label("cnt"),
        )
        .where(and_(
            MetricsSnapshot.data_level == "GMVMAX_CREATIVE",
            MetricsSnapshot.product_id.isnot(None),
            MetricsSnapshot.stat_date >= since,
        ))
        .group_by(MetricsSnapshot.product_id)
    )
    creative_counts = {r.product_id: r.cnt for r in creative_count_result.all()}

    # 4. 获取 store_id
    store_result = await db.execute(select(Store).where(Store.is_active == True))
    stores = store_result.scalars().all()
    adv_store_map = {s.advertiser_id: s.store_id for s in stores}

    # 5. UPSERT
    count = 0
    for r in item_rows:
        igid = r.item_group_id
        spend = float(r.total_spend or 0)
        revenue = float(r.total_revenue or 0)
        pinfo = product_info_map.get(igid, {})

        existing = await db.execute(select(ProductView).where(ProductView.item_group_id == igid))
        pv = existing.scalar_one_or_none()
        if not pv:
            pv = ProductView(item_group_id=igid)
            db.add(pv)

        pv.title = pinfo.get("title") or pv.title
        pv.image_url = pinfo.get("image_url") or pv.image_url
        pv.min_price = pinfo.get("min_price") or pv.min_price
        pv.max_price = pinfo.get("max_price") or pv.max_price
        pv.currency = pinfo.get("currency") or pv.currency
        pv.status = pinfo.get("status") or pv.status
        pv.advertiser_id = r.advertiser_id
        pv.store_id = adv_store_map.get(r.advertiser_id, "")
        pv.total_spend = round(spend, 2)
        pv.total_orders = int(r.total_orders or 0)
        pv.total_revenue = round(revenue, 2)
        pv.roi = round(revenue / spend, 4) if spend > 0 else 0
        pv.active_days = r.active_days
        pv.first_seen = r.first_seen
        pv.last_seen = r.last_seen
        pv.creative_count = creative_counts.get(igid, 0)
        count += 1

    await db.flush()
    logger.info(f"[ViewBuilder] product_view: upserted {count} products")


# ===================== Creative View =====================

async def build_creative_view(db: AsyncSession, days: int = 60):
    """
    构建创意视图：
    1. 从 GMVMAX_CREATIVE 聚合投放指标
    2. 关联 product_view 拿商品名/图片
    3. 关联 creatives 表拿视频信息
    4. 计算生命周期
    5. UPSERT 到 creative_view 表
    """
    since = date.today() - timedelta(days=days)

    # 1. 聚合 GMVMAX_CREATIVE
    result = await db.execute(
        select(
            MetricsSnapshot.object_id.label("item_id"),
            MetricsSnapshot.advertiser_id,
            func.sum(MetricsSnapshot.spend).label("total_spend"),
            func.max(MetricsSnapshot.conversion).label("total_orders"),
            func.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
            func.sum(MetricsSnapshot.impressions).label("total_impressions"),
            func.sum(MetricsSnapshot.clicks).label("total_clicks"),
            func.count(distinct(MetricsSnapshot.stat_date)).label("active_days"),
            func.min(MetricsSnapshot.stat_date).label("first_seen"),
            func.max(MetricsSnapshot.stat_date).label("last_seen"),
            func.max(MetricsSnapshot.product_id).label("item_group_id"),
            func.max(MetricsSnapshot.campaign_id).label("campaign_id"),
            func.max(MetricsSnapshot.object_name).label("obj_name"),
        )
        .where(and_(
            MetricsSnapshot.data_level == "GMVMAX_CREATIVE",
            MetricsSnapshot.stat_date >= since,
        ))
        .group_by(MetricsSnapshot.object_id, MetricsSnapshot.advertiser_id)
    )
    rows = result.all()

    if not rows:
        logger.debug("[ViewBuilder] No GMVMAX_CREATIVE data, skip creative_view build")
        return

    # 2. 读 product_view 拿商品信息
    pv_result = await db.execute(select(ProductView))
    product_map = {pv.item_group_id: pv for pv in pv_result.scalars().all()}

    # 3. 读 creatives 表拿视频信息
    cr_result = await db.execute(select(Creative).where(Creative.product_id.isnot(None)))
    video_by_product = {}
    for c in cr_result.scalars().all():
        video_by_product[c.product_id] = c

    # 4. 生命周期分析（复用现有逻辑）
    lifecycle_map = await _analyze_lifecycle(db, since)

    # 5. UPSERT
    count = 0
    for r in rows:
        item_id = r.item_id
        spend = float(r.total_spend or 0)
        revenue = float(r.total_revenue or 0)
        igid = r.item_group_id or ""
        is_auto = item_id == "-1"

        existing = await db.execute(select(CreativeView).where(CreativeView.item_id == item_id))
        cv = existing.scalar_one_or_none()
        if not cv:
            cv = CreativeView(item_id=item_id)
            db.add(cv)

        cv.is_auto_selected = 1 if is_auto else 0
        cv.item_group_id = igid
        cv.advertiser_id = r.advertiser_id
        cv.campaign_id = r.campaign_id or ""
        cv.total_spend = round(spend, 2)
        cv.total_orders = int(r.total_orders or 0)
        cv.total_revenue = round(revenue, 2)
        cv.total_impressions = int(r.total_impressions or 0)
        cv.total_clicks = int(r.total_clicks or 0)
        cv.roi = round(revenue / spend, 4) if spend > 0 else 0
        cv.avg_cost_per_order = round(spend / int(r.total_orders or 1), 2) if int(r.total_orders or 0) > 0 else 0
        cv.active_days = r.active_days
        cv.first_seen = r.first_seen
        cv.last_seen = r.last_seen

        # 商品信息
        pv = product_map.get(igid)
        if pv:
            cv.product_name = pv.title or ""
            cv.product_image_url = pv.image_url or ""
        elif r.obj_name:
            cv.product_name = r.obj_name

        # 视频信息
        creative = video_by_product.get(igid) or video_by_product.get(item_id)
        if creative:
            cv.video_id = creative.video_id
            cv.video_url = creative.video_url
            cv.cover_url = creative.cover_url
            cv.creative_name = creative.creative_name
            cv.duration = creative.duration

        # 生命周期
        lc = lifecycle_map.get(item_id, {})
        if is_auto:
            cv.stage = "AUTO"
            cv.recommendation = "observe"
            cv.reason = "系统自动选品"
        else:
            cv.stage = lc.get("stage", "UNKNOWN")
            cv.trend = lc.get("trend", "")
            cv.recommendation = lc.get("recommendation", "")
            cv.reason = lc.get("reason", "")
            cv.daily_avg_spend = lc.get("daily_avg_spend", 0)

        count += 1

    await db.flush()
    logger.info(f"[ViewBuilder] creative_view: upserted {count} creatives")


# ===================== Daily Summary =====================

async def build_daily_summary(db: AsyncSession, days: int = 60):
    """
    构建每日汇总：
    1. 从 GMVMAX_CAMPAIGN 按天聚合
    2. 从 GMVMAX_CREATIVE 按天聚合
    3. 计算周期对比
    4. UPSERT 到 daily_summary 表
    """
    since = date.today() - timedelta(days=days)

    # 1. Campaign 级按天聚合
    camp_result = await db.execute(
        select(
            MetricsSnapshot.stat_date,
            MetricsSnapshot.advertiser_id,
            func.count(distinct(MetricsSnapshot.object_id)).label("campaign_count"),
            func.sum(MetricsSnapshot.spend).label("total_spend"),
            func.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
            func.sum(MetricsSnapshot.conversion).label("total_orders"),
        )
        .where(and_(
            MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
            MetricsSnapshot.stat_date >= since,
        ))
        .group_by(MetricsSnapshot.stat_date, MetricsSnapshot.advertiser_id)
        .order_by(MetricsSnapshot.stat_date)
    )
    camp_daily = {}  # (date, adv_id) -> {spend, revenue, orders, count}
    for r in camp_result.all():
        key = (r.stat_date, r.advertiser_id)
        camp_daily[key] = {
            "campaign_count": r.campaign_count,
            "spend": float(r.total_spend or 0),
            "revenue": float(r.total_revenue or 0),
            "orders": int(r.total_orders or 0),
        }

    # 2. Creative 级按天聚合
    cre_result = await db.execute(
        select(
            MetricsSnapshot.stat_date,
            MetricsSnapshot.advertiser_id,
            func.count(distinct(MetricsSnapshot.object_id)).label("active_creatives"),
            func.sum(MetricsSnapshot.impressions).label("total_impressions"),
            func.sum(MetricsSnapshot.clicks).label("total_clicks"),
        )
        .where(and_(
            MetricsSnapshot.data_level == "GMVMAX_CREATIVE",
            MetricsSnapshot.stat_date >= since,
        ))
        .group_by(MetricsSnapshot.stat_date, MetricsSnapshot.advertiser_id)
    )
    cre_daily = {}
    for r in cre_result.all():
        key = (r.stat_date, r.advertiser_id)
        cre_daily[key] = {
            "active_creatives": r.active_creatives,
            "impressions": int(r.total_impressions or 0),
            "clicks": int(r.total_clicks or 0),
        }

    # 3. 合并 + 计算对比 + UPSERT
    all_keys = sorted(set(list(camp_daily.keys()) + list(cre_daily.keys())))
    count = 0
    for (stat_d, adv_id) in all_keys:
        c = camp_daily.get((stat_d, adv_id), {})
        cr = cre_daily.get((stat_d, adv_id), {})
        spend = c.get("spend", 0)
        revenue = c.get("revenue", 0)

        # 找昨日和上周同天数据
        yesterday = stat_d - timedelta(days=1)
        last_week = stat_d - timedelta(days=7)
        y = camp_daily.get((yesterday, adv_id), {})
        w = camp_daily.get((last_week, adv_id), {})

        def pct(cur, prev):
            if not prev:
                return None
            return round((cur - prev) / prev * 100, 2)

        existing = await db.execute(
            select(DailySummary).where(
                DailySummary.stat_date == stat_d,
                DailySummary.advertiser_id == adv_id,
            )
        )
        ds = existing.scalar_one_or_none()
        if not ds:
            ds = DailySummary(stat_date=stat_d, advertiser_id=adv_id)
            db.add(ds)

        ds.campaign_count = c.get("campaign_count", 0)
        ds.total_spend = round(spend, 2)
        ds.total_revenue = round(revenue, 2)
        ds.total_orders = c.get("orders", 0)
        ds.roi = round(revenue / spend, 4) if spend > 0 else 0
        ds.active_creatives = cr.get("active_creatives", 0)
        ds.total_impressions = cr.get("impressions", 0)
        ds.total_clicks = cr.get("clicks", 0)

        # 周期对比
        ds.spend_vs_yesterday = pct(spend, y.get("spend", 0))
        ds.revenue_vs_yesterday = pct(revenue, y.get("revenue", 0))
        y_roi = y.get("revenue", 0) / y.get("spend", 1) if y.get("spend", 0) > 0 else 0
        ds.roi_vs_yesterday = pct(ds.roi, y_roi) if y_roi > 0 else None
        ds.spend_vs_last_week = pct(spend, w.get("spend", 0))
        ds.revenue_vs_last_week = pct(revenue, w.get("revenue", 0))

        count += 1

    await db.flush()
    logger.info(f"[ViewBuilder] daily_summary: upserted {count} rows")


# ===================== 全量构建入口 =====================

async def build_all_views(db: AsyncSession, days: int = 60):
    """同步完成后调用，依次构建三张视图表"""
    logger.info("[ViewBuilder] === Building all views ===")
    await build_product_view(db, days)
    await build_creative_view(db, days)
    await build_daily_summary(db, days)
    logger.info("[ViewBuilder] === All views built ===")


# ===================== 辅助函数 =====================

async def _fetch_product_info_safe(db: AsyncSession) -> Dict[str, Dict[str, Any]]:
    """从 TikTok Shop API 获取商品信息，失败时返回空 dict（不阻塞构建）"""
    from app.models.advertiser import Advertiser
    from app.services.tiktok_client import TikTokClient

    product_map = {}
    store_result = await db.execute(select(Store).where(Store.is_active == True))
    stores = store_result.scalars().all()

    for store in stores:
        if not store.store_authorized_bc_id or not store.advertiser_id:
            continue
        adv_result = await db.execute(
            select(Advertiser).where(Advertiser.advertiser_id == store.advertiser_id)
        )
        adv = adv_result.scalar_one_or_none()
        if not adv:
            continue

        client = TikTokClient(access_token=adv.access_token, advertiser_id=adv.advertiser_id)
        try:
            products = await client.get_all_store_products(
                store_id=store.store_id, bc_id=store.store_authorized_bc_id,
            )
            for p in products:
                igid = p.get("item_group_id", "")
                if igid:
                    product_map[igid] = {
                        "title": p.get("title", ""),
                        "image_url": p.get("product_image_url", ""),
                        "min_price": p.get("min_price"),
                        "max_price": p.get("max_price"),
                        "currency": p.get("currency", ""),
                        "status": p.get("status", ""),
                    }
            if products:
                logger.info(f"[ViewBuilder] Fetched {len(products)} products from store {store.store_id}")
        except Exception as e:
            logger.warning(f"[ViewBuilder] Failed to fetch products from store {store.store_id}: {e}")
        finally:
            await client.close()

    # Fallback: 如果 API 失败，从磁盘缓存读
    if not product_map:
        import json
        from pathlib import Path
        cache_file = Path(__file__).resolve().parent.parent / ".cache" / "product_map.json"
        if cache_file.exists():
            try:
                product_map = json.loads(cache_file.read_text(encoding="utf-8"))
                logger.info(f"[ViewBuilder] Loaded {len(product_map)} products from disk cache")
            except Exception:
                pass

    # 写磁盘缓存
    if product_map:
        import json
        from pathlib import Path
        cache_file = Path(__file__).resolve().parent.parent / ".cache" / "product_map.json"
        try:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps(product_map, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    return product_map


async def _analyze_lifecycle(db: AsyncSession, since: date) -> Dict[str, Dict]:
    """简化版生命周期分析（复用 creatives.py 的逻辑）"""
    from collections import defaultdict

    result = await db.execute(
        select(
            MetricsSnapshot.object_id,
            MetricsSnapshot.stat_date,
            MetricsSnapshot.spend,
            MetricsSnapshot.conversion,
        )
        .where(and_(
            MetricsSnapshot.data_level == "GMVMAX_CREATIVE",
            MetricsSnapshot.stat_date >= since,
            MetricsSnapshot.object_id != "-1",
        ))
        .order_by(MetricsSnapshot.object_id, MetricsSnapshot.stat_date)
    )

    daily_data: Dict[str, list] = defaultdict(list)
    for r in result.all():
        daily_data[r.object_id].append({
            "date": r.stat_date,
            "spend": float(r.spend or 0),
            "orders": int(r.conversion or 0),
        })

    today = date.today()
    lifecycle = {}

    for item_id, days_data in daily_data.items():
        spends = [d["spend"] for d in days_data]
        total_spend = sum(spends)
        total_orders = sum(d["orders"] for d in days_data)
        active_days = len([s for s in spends if s > 0])
        dates = [d["date"] for d in days_data]
        last_date = max(dates) if dates else today
        days_since_last = (today - last_date).days

        mid = len(spends) // 2 if len(spends) > 1 else 1
        first_half = sum(spends[:mid])
        second_half = sum(spends[mid:])
        trend_ratio = second_half / first_half if first_half > 0 else (2.0 if second_half > 0 else 0)
        trend = "up" if trend_ratio > 1.2 else ("down" if trend_ratio < 0.8 else "stable")
        daily_avg = total_spend / max(active_days, 1)

        # 最近几天的花费（用于判断是否停投）
        recent_spends = spends[-2:] if len(spends) >= 2 else spends
        last_day_spend = spends[-1] if spends else 0

        if days_since_last >= 2:
            stage, rec, reason = "DEAD", "drop", f"已{days_since_last}天无花费"
        elif last_day_spend == 0 and total_spend > 1 and len(spends) >= 2:
            # 之前有花费但最近一天为 0 → 可能被停投/排除
            stage, rec, reason = "DEAD", "drop", "最近无花费，可能已停投"
        elif active_days <= 2 and total_spend < 0.5:
            stage, rec, reason = "WARM_UP", "observe", "冷启动阶段"
        elif active_days >= 5 and total_orders == 0 and trend == "down":
            stage, rec, reason = "FATIGUE", "drop", f"投放{active_days}天无转化"
        elif trend == "up" and daily_avg > 0.1:
            stage, rec, reason = "GROWTH", "boost", f"花费趋势上升"
        elif trend == "stable" and daily_avg > 0.5:
            stage, rec, reason = "PEAK", "observe", f"花费稳定(日均${daily_avg:.2f})"
        elif trend == "down":
            stage, rec, reason = "DECAY", "reduce", "花费趋势下降"
        else:
            stage, rec, reason = "WARM_UP", "observe", "数据积累中"

        if total_orders > 0:
            if stage in ("FATIGUE", "DEAD"):
                stage = "DECAY"
            rec = "boost" if trend != "down" else "observe"
            reason = f"有{total_orders}笔转化! " + reason

        lifecycle[item_id] = {
            "stage": stage, "trend": trend, "recommendation": rec,
            "reason": reason, "daily_avg_spend": round(daily_avg, 2),
        }

    return lifecycle
