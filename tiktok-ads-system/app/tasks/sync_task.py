"""
数据同步任务 — 每 30 分钟跑一次
批量采集所有广告账户的 Campaign/AdGroup/Ad 数据和报表
"""
import asyncio
from datetime import datetime, timedelta, timezone, date
from typing import List, Optional

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.advertiser import Advertiser
from app.models.metrics import MetricsSnapshot
from app.services.tiktok_client import TikTokClient, TikTokAPIError


async def refresh_expired_tokens():
    """刷新即将过期的 access_token（过期前 2 小时）"""
    async with AsyncSessionLocal() as db:
        threshold = datetime.now(timezone.utc) + timedelta(hours=2)
        result = await db.execute(
            select(Advertiser).where(
                Advertiser.is_active == True,
                Advertiser.access_token_expire_at <= threshold,
                Advertiser.is_token_valid == True,
            )
        )
        advertisers = result.scalars().all()

        if not advertisers:
            return

        logger.info(f"Refreshing tokens for {len(advertisers)} advertisers")
        for adv in advertisers:
            try:
                new_token_data = await TikTokClient.refresh_token(adv.refresh_token)
                adv.access_token = new_token_data["access_token"]
                adv.access_token_expire_at = datetime.now(timezone.utc) + timedelta(hours=23, minutes=30)
                adv.last_token_refresh_at = datetime.now(timezone.utc)
                logger.info(f"Token refreshed: {adv.advertiser_id}")
            except TikTokAPIError as e:
                logger.error(f"Token refresh failed for {adv.advertiser_id}: {e}")
                adv.is_token_valid = False

        await db.commit()


async def sync_creatives(advertiser_id: str, access_token: str, db: AsyncSession):
    """同步素材级数据"""
    from app.services.creative_sync import CreativeSyncService
    client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
    try:
        svc = CreativeSyncService(client=client, db=db)
        await svc.sync(advertiser_id)
    except Exception as e:
        logger.exception(f"Creative sync failed for {advertiser_id}: {e}")
    finally:
        await client.close()


async def sync_advertiser(advertiser_id: str, access_token: str, db: AsyncSession):
    """同步单个广告账户的数据"""
    client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
    today = date.today()
    # 拉近 3 天数据（TikTok 报表有延迟，补拉历史）
    start_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    snapshot_time = datetime.now(timezone.utc)

    try:
        # 第一步：拉取 Ad 级别报表（最细粒度）
        report_data = await client.get_report(
            data_level="AUCTION_AD",
            start_date=start_date,
            end_date=end_date,
        )

        rows = report_data.get("list", [])
        if not rows:
            logger.debug(f"No report data for {advertiser_id}")
            return

        # 第二步：拉取广告详情，建立 ad_id → product_id 映射
        ad_ids = [row.get("dimensions", {}).get("ad_id") for row in rows]
        ad_ids = [aid for aid in ad_ids if aid]  # 去空
        
        ad_product_map = {}  # ad_id → product_id
        if ad_ids:
            try:
                # 分批获取（TikTok API 可能有单次请求大小限制）
                batch_size = 100
                for i in range(0, len(ad_ids), batch_size):
                    batch = ad_ids[i:i+batch_size]
                    ad_details = await client.get_ads_batch(batch)
                    for ad in ad_details.get("data", []):
                        ad_id = ad.get("ad_id")
                        product_id = ad.get("product_id")
                        if ad_id and product_id:
                            ad_product_map[ad_id] = product_id
                
                if ad_product_map:
                    logger.info(f"Built product_id map for {len(ad_product_map)}/{len(ad_ids)} ads")
            except Exception as e:
                logger.warning(f"Failed to get ad details for product mapping: {e}")

        # 第三步：合并报表 + 广告详情，创建 snapshot
        snapshots = []
        for row in rows:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})
            ad_id = dims.get("ad_id", "")

            # 优先使用报表本身的 product_id，其次用映射表补充
            product_id = dims.get("product_id") or ad_product_map.get(ad_id)
            
            snapshot = MetricsSnapshot(
                advertiser_id=advertiser_id,
                data_level="AD",
                object_id=ad_id,
                object_name=dims.get("ad_name", ""),  # 保存广告名称便于追踪
                stat_date=datetime.strptime(dims.get("stat_time_day", str(today)).split(" ")[0], "%Y-%m-%d").date(),
                snapshot_time=snapshot_time,
                
                # 商品关联（新增）
                product_id=product_id,  # 从报表或广告详情获取
                sku_id=dims.get("sku_id"),  # TikTok API 暂时未提供，可后续补充
                
                # 投放指标
                spend=float(metrics.get("spend", 0) or 0),
                impressions=int(metrics.get("impressions", 0) or 0),
                clicks=int(metrics.get("clicks", 0) or 0),
                ctr=float(metrics.get("ctr", 0) or 0),
                cpm=float(metrics.get("cpm", 0) or 0),
                cpc=float(metrics.get("cpc", 0) or 0),
                
                # 转化指标
                conversion=int(metrics.get("conversion", 0) or 0),
                cost_per_conversion=float(metrics.get("cost_per_conversion", 0) or 0),
                conversion_rate=float(metrics.get("conversion_rate", 0) or 0),
                real_time_conversion=int(metrics.get("real_time_conversion", 0) or 0),
                real_time_cost_per_conversion=float(metrics.get("real_time_cost_per_conversion", 0) or 0),
                
                # 视频指标
                video_play_actions=int(metrics.get("video_play_actions", 0) or 0),
                video_watched_2s=int(metrics.get("video_watched_2s", 0) or 0),
                video_watched_6s=int(metrics.get("video_watched_6s", 0) or 0),
                average_video_play=float(metrics.get("average_video_play", 0) or 0),
            )
            snapshots.append(snapshot)

        db.add_all(snapshots)
        logger.info(f"Synced {len(snapshots)} ad snapshots for {advertiser_id}")

    except TikTokAPIError as e:
        if e.code == 40105:
            # token 过期，标记
            result = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == advertiser_id))
            adv = result.scalar_one_or_none()
            if adv:
                adv.is_token_valid = False
        logger.error(f"API error syncing {advertiser_id}: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error syncing {advertiser_id}: {e}")
    finally:
        await client.close()


async def sync_gmvmax(
    advertiser_id: str,
    access_token: str,
    db: AsyncSession,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """同步单个广告账户的 GMVMax 数据（专用端点 + 专用 metrics）"""
    client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
    today = date.today()
    if start_date is None:
        start_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = today.strftime("%Y-%m-%d")
    snapshot_time = datetime.now(timezone.utc)

    try:
        # 1. 获取关联店铺（合并 API 返回和 DB 已存）
        store_ids = await _get_active_store_ids(advertiser_id, client, db)
        if not store_ids:
            logger.debug(f"No stores linked to {advertiser_id}, skip GMVMax sync")
            return

        # 取 stores 列表用于 campaign name 查询
        stores_api = await client.get_gmvmax_store_list() or []

        # 2. 每个 store 单独拉取 GMVMax 报表（API 限制 store_ids 最多 1 个）
        rows = []  # [(row_dict, store_id)]
        for sid in store_ids:
            try:
                report_data = await client.get_gmvmax_report(
                    store_ids=[sid],
                    start_date=start_date,
                    end_date=end_date,
                )
                for r in (report_data.get("list") or []):
                    rows.append((r, sid))
            except Exception as e:
                logger.warning(f"GMVMax report failed for {advertiser_id} store={sid}: {e}")

        if not rows:
            logger.debug(f"No GMVMax data for {advertiser_id}")
            return

        # 2.5. 获取 campaign 名称映射（用 GMVMax 专属接口 /gmv_max/campaign/get/）
        campaign_name_map = {}  # campaign_id -> campaign_name
        try:
            import json as _json
            for promo_type in ["PRODUCT_GMV_MAX", "LIVE_GMV_MAX"]:
                page = 1
                while True:
                    camp_data = await client._request("GET", "/open_api/v1.3/gmv_max/campaign/get/", params={
                        "advertiser_id": advertiser_id,
                        "store_id": store_ids[0] if store_ids else "",
                        "store_authorized_bc_id": stores_api[0].get("store_authorized_bc_id", "") if stores_api else "",
                        "filtering": _json.dumps({"gmv_max_promotion_types": [promo_type]}),
                        "page": page,
                        "page_size": 100,
                    })
                    for c in camp_data.get("list", []):
                        cid = str(c.get("campaign_id", ""))
                        cname = c.get("campaign_name", "")
                        if cid and cname:
                            campaign_name_map[cid] = cname
                    total_page = camp_data.get("page_info", {}).get("total_page", 1)
                    if page >= total_page:
                        break
                    page += 1
            if campaign_name_map:
                logger.info(f"Fetched names for {len(campaign_name_map)} GMVMax campaigns")
        except Exception as e:
            logger.warning(f"Failed to fetch GMVMax campaign names for {advertiser_id}: {e}")

        # 3. 写入 MetricsSnapshot，data_level = "GMVMAX_CAMPAIGN"
        snapshots = []
        for row, store_id in rows:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})
            campaign_id = dims.get("campaign_id", "")

            snapshot = MetricsSnapshot(
                advertiser_id=advertiser_id,
                data_level="GMVMAX_CAMPAIGN",
                object_id=campaign_id,
                object_name=campaign_name_map.get(campaign_id, ""),
                stat_date=datetime.strptime(
                    dims.get("stat_time_day", str(today)),
                    "%Y-%m-%d %H:%M:%S" if " " in dims.get("stat_time_day", "") else "%Y-%m-%d",
                ).date(),
                snapshot_time=snapshot_time,
                campaign_id=campaign_id,
                store_id=store_id,

                # GMVMax metrics → 复用已有字段 + 新字段
                spend=float(metrics.get("cost", 0) or 0),             # cost → spend
                conversion=int(metrics.get("orders", 0) or 0),        # orders → conversion
                cost_per_conversion=float(metrics.get("cost_per_order", 0) or 0),
                gross_revenue=float(metrics.get("gross_revenue", 0) or 0),
                roi=float(metrics.get("roi", 0) or 0),
                live_views=int(metrics.get("live_views", 0) or 0),
            )
            snapshots.append(snapshot)

        db.add_all(snapshots)
        logger.info(f"Synced {len(snapshots)} GMVMax snapshots for {advertiser_id} (stores: {store_ids})")

        # 4. 额外拉订单来源拆分数据（ORDER_SOURCE 级别）
        # GMVMax 报表不支持 order_source 维度，改用 get_order_report() 拉取后聚合
        await _sync_order_source(
            client=client,
            advertiser_id=advertiser_id,
            db=db,
            start_date=start_date,
            end_date=end_date,
            snapshot_time=snapshot_time,
            gmvmax_rows=rows,  # 传入 GMVMax 数据用于 spend 按比例分配
        )

    except TikTokAPIError as e:
        if e.code == 40105:
            result = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == advertiser_id))
            adv = result.scalar_one_or_none()
            if adv:
                adv.is_token_valid = False
        logger.error(f"GMVMax sync API error for {advertiser_id}: {e}")
    except Exception as e:
        logger.exception(f"GMVMax sync failed for {advertiser_id}: {e}")
    finally:
        await client.close()


async def _sync_order_source(
    client: "TikTokClient",
    advertiser_id: str,
    db: AsyncSession,
    start_date: str,
    end_date: str,
    snapshot_time: datetime,
    gmvmax_rows: list,
):
    """
    从 get_order_report() 拉取订单数据，按 order_source + stat_time_day 分组聚合，
    写入 MetricsSnapshot（data_level='ORDER_SOURCE'）。
    spend 字段从 GMVMax 报表按 GMV 比例分配。
    """
    try:
        order_data = await client.get_order_report(
            start_date=start_date,
            end_date=end_date,
            include_affiliate=True,
        )
        order_rows = order_data.get("list", [])
        if not order_rows:
            logger.debug(f"No order report data for {advertiser_id}, skip ORDER_SOURCE sync")
            return

        # 构建 GMVMax spend 按日期汇总（用于比例分配）
        # key: stat_date_str → total_spend, total_gmv
        gmvmax_daily: dict = {}
        for row in gmvmax_rows:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})
            day = dims.get("stat_time_day", "")
            day_key = day.split(" ")[0] if day else ""
            if not day_key:
                continue
            if day_key not in gmvmax_daily:
                gmvmax_daily[day_key] = {"spend": 0.0, "gmv": 0.0}
            gmvmax_daily[day_key]["spend"] += float(metrics.get("cost", 0) or 0)
            gmvmax_daily[day_key]["gmv"] += float(metrics.get("gross_revenue", 0) or 0)

        # 按 (stat_date, order_source) 聚合订单数据
        from collections import defaultdict
        agg: dict = defaultdict(lambda: {
            "gmv": 0.0,
            "orders": 0,
            "commission_amount": 0.0,
            "commission_rate_sum": 0.0,
            "commission_rate_count": 0,
            "affiliate_ids": set(),
            "affiliate_names": set(),
        })

        for row in order_rows:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})

            day_raw = dims.get("stat_time_day", "")
            day_key = day_raw.split(" ")[0] if day_raw else ""
            order_source = (
                dims.get("order_source")
                or metrics.get("order_source")
                or "SELF_OWNED"
            )
            key = (day_key, order_source)

            agg[key]["gmv"] += float(metrics.get("order_amount", 0) or 0)
            agg[key]["orders"] += 1

            if order_source == "AFFILIATE":
                agg[key]["commission_amount"] += float(metrics.get("commission_amount", 0) or 0)
                cr = float(metrics.get("commission_rate", 0) or 0)
                if cr > 0:
                    agg[key]["commission_rate_sum"] += cr
                    agg[key]["commission_rate_count"] += 1
                aff_id = metrics.get("affiliate_id") or dims.get("affiliate_id")
                aff_name = metrics.get("affiliate_name") or dims.get("affiliate_name")
                if aff_id:
                    agg[key]["affiliate_ids"].add(str(aff_id))
                if aff_name:
                    agg[key]["affiliate_names"].add(str(aff_name))

        # 写入 MetricsSnapshot（data_level='ORDER_SOURCE'）
        snapshots = []
        for (day_key, order_source), data in agg.items():
            if not day_key:
                continue

            # 按 GMV 比例分配 spend
            daily = gmvmax_daily.get(day_key, {})
            total_gmv = daily.get("gmv", 0.0)
            total_spend = daily.get("spend", 0.0)
            gmv_val = data["gmv"]
            spend_allocated = (
                total_spend * (gmv_val / total_gmv) if total_gmv > 0 else 0.0
            )

            # 平均佣金率
            avg_commission_rate = (
                data["commission_rate_sum"] / data["commission_rate_count"]
                if data["commission_rate_count"] > 0
                else 0.0
            )

            try:
                stat_date = datetime.strptime(day_key, "%Y-%m-%d").date()
            except ValueError:
                continue

            snapshot = MetricsSnapshot(
                advertiser_id=advertiser_id,
                data_level="ORDER_SOURCE",
                object_id=f"{advertiser_id}_{order_source}_{day_key}",
                object_name=order_source,
                stat_date=stat_date,
                snapshot_time=snapshot_time,

                # 渠道来源字段
                source_type=order_source,
                affiliate_id=",".join(sorted(data["affiliate_ids"]))[:64] if data["affiliate_ids"] else None,
                affiliate_name=",".join(sorted(data["affiliate_names"]))[:256] if data["affiliate_names"] else None,
                commission_amount=data["commission_amount"],
                commission_rate=avg_commission_rate,

                # 指标
                gross_revenue=gmv_val,
                conversion=data["orders"],
                spend=spend_allocated,
                roi=round(gmv_val / spend_allocated, 4) if spend_allocated > 0 else 0.0,
                cost_per_conversion=round(spend_allocated / data["orders"], 4) if data["orders"] > 0 else 0.0,
            )
            snapshots.append(snapshot)

        if snapshots:
            db.add_all(snapshots)
            logger.info(
                f"Synced {len(snapshots)} ORDER_SOURCE snapshots for {advertiser_id}"
            )

    except Exception as e:
        logger.warning(f"ORDER_SOURCE sync failed for {advertiser_id}: {e}")


async def sync_gmvmax_items(
    advertiser_id: str,
    access_token: str,
    db: AsyncSession,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """同步单个广告账户的 GMVMax 商品组级别数据"""
    client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
    today = date.today()
    if start_date is None:
        start_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = today.strftime("%Y-%m-%d")
    snapshot_time = datetime.now(timezone.utc)

    try:
        # 1. 获取关联店铺（合并 API + DB）
        store_ids = await _get_active_store_ids(advertiser_id, client, db)
        if not store_ids:
            logger.debug(f"No stores linked to {advertiser_id}, skip GMVMax item sync")
            return

        # 2. 从数据库获取该广告主已有的 GMVMAX_CAMPAIGN campaign_ids
        result = await db.execute(
            select(MetricsSnapshot.object_id)
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
            )
            .distinct()
        )
        campaign_ids = [row[0] for row in result.fetchall() if row[0]]

        if not campaign_ids:
            logger.debug(f"No GMVMAX_CAMPAIGN records for {advertiser_id}, skip item sync")
            return

        # 3. 每个 store 单独拉取 GMVMax 商品组报表
        all_rows = []  # [(row, store_id)]
        for sid in store_ids:
            try:
                report_data = await client.get_gmvmax_item_report(
                    store_ids=[sid],
                    campaign_ids=campaign_ids,
                    start_date=start_date,
                    end_date=end_date,
                )
                for r in (report_data.get("list") or []):
                    all_rows.append((r, sid))
            except Exception as e:
                logger.warning(f"GMVMax item report failed for {advertiser_id} store={sid}: {e}")

        if not all_rows:
            logger.debug(f"No GMVMax item data for {advertiser_id}")
            return

        # 4. 写入 MetricsSnapshot，data_level = "GMVMAX_ITEM"
        snapshots = []
        for row, store_id in all_rows:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})
            item_group_id = dims.get("item_group_id", "")

            snapshot = MetricsSnapshot(
                advertiser_id=advertiser_id,
                data_level="GMVMAX_ITEM",
                object_id=item_group_id,
                object_name="",
                stat_date=datetime.strptime(
                    dims.get("stat_time_day", str(today)).split(" ")[0],
                    "%Y-%m-%d",
                ).date(),
                snapshot_time=snapshot_time,
                store_id=store_id,

                # GMVMax item metrics
                spend=float(metrics.get("cost", 0) or 0),
                conversion=int(metrics.get("orders", 0) or 0),
                cost_per_conversion=float(metrics.get("cost_per_order", 0) or 0),
                gross_revenue=float(metrics.get("gross_revenue", 0) or 0),
                roi=float(metrics.get("roi", 0) or 0),
            )
            snapshots.append(snapshot)

        db.add_all(snapshots)
        logger.info(f"Synced {len(snapshots)} GMVMax item snapshots for {advertiser_id} (stores: {store_ids})")

    except TikTokAPIError as e:
        if e.code == 40105:
            result = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == advertiser_id))
            adv = result.scalar_one_or_none()
            if adv:
                adv.is_token_valid = False
        logger.error(f"GMVMax item sync API error for {advertiser_id}: {e}")
    except Exception as e:
        logger.exception(f"GMVMax item sync failed for {advertiser_id}: {e}")
    finally:
        await client.close()


async def sync_gmvmax_creatives(
    advertiser_id: str,
    access_token: str,
    db: AsyncSession,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """同步单个广告账户的 GMVMax 素材级别(item_id)数据"""
    client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
    today = date.today()
    if start_date is None:
        start_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = today.strftime("%Y-%m-%d")
    snapshot_time = datetime.now(timezone.utc)

    try:
        # 1. 获取关联店铺（合并 API + DB）
        store_ids = await _get_active_store_ids(advertiser_id, client, db)
        if not store_ids:
            logger.debug(f"No stores linked to {advertiser_id}, skip GMVMax creative sync")
            return

        # 2. 从数据库获取该广告主已有的 GMVMAX_CAMPAIGN campaign_ids
        result = await db.execute(
            select(MetricsSnapshot.object_id)
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
            )
            .distinct()
        )
        campaign_ids = [row[0] for row in result.fetchall() if row[0]]

        if not campaign_ids:
            logger.debug(f"No GMVMAX_CAMPAIGN records for {advertiser_id}, skip creative sync")
            return

        # 3. 从数据库获取该广告主已有的 GMVMAX_ITEM item_group_ids
        result = await db.execute(
            select(MetricsSnapshot.object_id)
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level == "GMVMAX_ITEM",
            )
            .distinct()
        )
        item_group_ids = [row[0] for row in result.fetchall() if row[0]]

        if not item_group_ids:
            logger.debug(f"No GMVMAX_ITEM records for {advertiser_id}, skip creative sync")
            return

        # 3.5. 查 item_group_id → store_id 映射（从刚同步的 GMVMAX_ITEM 记录）
        ig_store_result = await db.execute(
            select(MetricsSnapshot.object_id, MetricsSnapshot.store_id)
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level == "GMVMAX_ITEM",
                MetricsSnapshot.store_id.isnot(None),
            )
            .distinct()
        )
        ig_to_store = {row[0]: row[1] for row in ig_store_result.fetchall() if row[0] and row[1]}

        # 4. 逐个 item_group_id：用其对应的 store_id 调用 API
        snapshots = []
        for ig_id in item_group_ids:
            # 每个 item_group 只属于一个 store，API 限制 store_ids 最多 1 个
            ig_store_id = ig_to_store.get(ig_id) or (store_ids[0] if store_ids else None)
            if not ig_store_id:
                continue
            try:
                # 4a. 汇总报表（不带 stat_time_day）：真实数据
                summary_rows = []
                s_page = 1
                while True:
                    summary = await client.get_gmvmax_report(
                        [ig_store_id], start_date, end_date,
                        dimensions=["campaign_id", "item_id"],
                        metrics=["cost", "gross_revenue", "orders", "roi", "cost_per_order",
                                 "product_impressions", "product_clicks", "product_click_rate"],
                        filtering={"campaign_ids": campaign_ids, "item_group_ids": [ig_id]},
                        page=s_page, page_size=200,
                    )
                    page_rows = summary.get("list", [])
                    if not page_rows:
                        break
                    summary_rows.extend(page_rows)
                    if s_page >= summary.get("page_info", {}).get("total_page", 1):
                        break
                    s_page += 1

                if not summary_rows:
                    continue

                # 写入汇总记录（stat_date 用 end_date 作为标记）
                for row in summary_rows:
                    d, m = row.get("dimensions", {}), row.get("metrics", {})
                    item_id = str(d.get("item_id", ""))
                    snapshots.append(MetricsSnapshot(
                        advertiser_id=advertiser_id,
                        data_level="GMVMAX_CREATIVE",
                        object_id=item_id,
                        object_name="自动选品" if item_id == "-1" else "",
                        stat_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
                        snapshot_time=snapshot_time,
                        campaign_id=d.get("campaign_id", ""),
                        product_id=ig_id,
                        store_id=ig_store_id,
                        spend=float(m.get("cost", 0) or 0),
                        gross_revenue=float(m.get("gross_revenue", 0) or 0),
                        conversion=int(m.get("orders", 0) or 0),
                        roi=float(m.get("roi", 0) or 0),
                        cost_per_conversion=float(m.get("cost_per_order", 0) or 0),
                        impressions=int(m.get("product_impressions", 0) or 0),
                        clicks=int(m.get("product_clicks", 0) or 0),
                        ctr=float(m.get("product_click_rate", 0) or 0),
                    ))

                # 4b. 每日 cost（带 stat_time_day）：供生命周期计算
                d_page = 1
                while True:
                    daily = await client.get_gmvmax_report(
                        [ig_store_id], start_date, end_date,
                        dimensions=["item_id", "stat_time_day"],
                        metrics=["cost"],
                        filtering={"campaign_ids": campaign_ids, "item_group_ids": [ig_id]},
                        page=d_page, page_size=200,
                    )
                    page_rows = daily.get("list", [])
                    if not page_rows:
                        break
                    for row in page_rows:
                        dims = row.get("dimensions", {})
                        metrics = row.get("metrics", {})
                        item_id = str(dims.get("item_id", ""))
                        day = dims.get("stat_time_day", "")[:10]
                        if not day:
                            continue
                        snapshots.append(MetricsSnapshot(
                            advertiser_id=advertiser_id,
                            data_level="GMVMAX_CREATIVE_DAILY",
                            object_id=item_id,
                            stat_date=datetime.strptime(day, "%Y-%m-%d").date(),
                            snapshot_time=snapshot_time,
                            product_id=ig_id,
                            store_id=ig_store_id,
                            spend=float(metrics.get("cost", 0) or 0),
                        ))
                    if d_page >= daily.get("page_info", {}).get("total_page", 1):
                        break
                    d_page += 1

            except Exception as e:
                logger.warning(f"GMVMax creative report failed for item_group_id={ig_id}: {e}")
                continue

        if not snapshots:
            logger.debug(f"No GMVMax creative data for {advertiser_id}")
            return

        db.add_all(snapshots)
        logger.info(f"Synced {len(snapshots)} GMVMax creative snapshots for {advertiser_id} (stores: {store_ids})")

    except TikTokAPIError as e:
        if e.code == 40105:
            result = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == advertiser_id))
            adv = result.scalar_one_or_none()
            if adv:
                adv.is_token_valid = False
        logger.error(f"GMVMax creative sync API error for {advertiser_id}: {e}")
    except Exception as e:
        logger.exception(f"GMVMax creative sync failed for {advertiser_id}: {e}")
    finally:
        await client.close()


async def run_detection_and_decision():
    """检测 + LLM 决策任务（同步完成后触发）"""
    from app.services.detector import DetectionEngine
    from app.services.llm_decision import LLMDecisionService

    llm_svc = LLMDecisionService()

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Advertiser).where(
                Advertiser.is_active == True,
                Advertiser.is_token_valid == True,
            )
        )
        advertisers = result.scalars().all()

        for adv in advertisers:
            try:
                # Ad 级检测
                engine = DetectionEngine(db)
                ad_alerts = await engine.detect_advertiser(adv.advertiser_id)

                # 素材级检测
                from app.services.creative_detector import CreativeDetector
                creative_engine = CreativeDetector(db)
                creative_alerts = await creative_engine.detect_advertiser(adv.advertiser_id)

                all_alerts = ad_alerts + creative_alerts
                logger.info(f"{adv.advertiser_id}: {len(ad_alerts)} ad alert(s), {len(creative_alerts)} creative alert(s)")

                for alert in all_alerts:
                    await llm_svc.process_alert(alert, db)

                # 加热扫描（与疲劳检测同步运行）
                from app.services.creative_booster import CreativeBooster
                booster = CreativeBooster(db)
                boost_decisions = await booster.scan_and_boost(adv.advertiser_id)
                if boost_decisions:
                    logger.info(f"{adv.advertiser_id}: {len(boost_decisions)} boost decision(s)")

            except Exception as e:
                logger.exception(f"Detection/decision failed for {adv.advertiser_id}: {e}")


async def _sync_stores(advertisers, db):
    """同步所有广告主关联的店铺信息到 stores 表。

    策略：
    - TikTok 的 /gmv_max/store/list/ 接口有时会漏返回已授权的 store，
      但 /gmv_max/report/ 仍能拉到数据。因此不以 store 列表为准判定失效。
    - 只 upsert API 返回的 store，已存在但 API 不返回的 store 保持不变。
    """
    from app.models.store import Store
    for adv in advertisers:
        client = TikTokClient(access_token=adv.access_token, advertiser_id=adv.advertiser_id)
        try:
            stores = await client.get_gmvmax_store_list()
            for s in (stores or []):
                store_id = str(s.get("store_id") or s.get("shop_id") or "")
                if not store_id:
                    continue
                existing = await db.execute(select(Store).where(Store.store_id == store_id))
                store = existing.scalar_one_or_none()
                region_codes = s.get("targeting_region_codes", [])
                if not store:
                    store = Store(store_id=store_id)
                    db.add(store)
                store.store_name = s.get("store_name", "")
                store.store_type = s.get("store_type", "")
                store.store_code = s.get("store_code", "")
                store.advertiser_id = adv.advertiser_id
                store.store_authorized_bc_id = str(s.get("store_authorized_bc_id") or s.get("bc_id") or "")
                store.region = ",".join(region_codes) if isinstance(region_codes, list) else str(region_codes or "")
                store.targeting_region_codes = region_codes
                store.is_active = True
                store.last_synced_at = datetime.now(timezone.utc)
            await db.flush()
            if stores:
                logger.info(f"[Store Sync] {adv.advertiser_id}: synced {len(stores)} store(s)")
        except Exception as e:
            logger.warning(f"[Store Sync] {adv.advertiser_id} failed: {e}")
        finally:
            await client.close()


async def _get_active_store_ids(advertiser_id: str, client: TikTokClient, db: AsyncSession) -> List[str]:
    """获取该广告主所有可用的 store_id。

    合并两个数据源：
    1. /gmv_max/store/list/ API 返回的 store
    2. 数据库中已存的该广告主的 active store（API 有时漏返回）
    """
    from app.models.store import Store
    ids = set()
    try:
        stores = await client.get_gmvmax_store_list()
        for s in (stores or []):
            sid = str(s.get("store_id") or s.get("shop_id") or "")
            if sid:
                ids.add(sid)
    except Exception:
        pass

    # 补充：数据库已记录的该广告主 active store
    db_result = await db.execute(
        select(Store.store_id).where(
            Store.advertiser_id == advertiser_id,
            Store.is_active == True,
        )
    )
    for (sid,) in db_result.all():
        if sid:
            ids.add(sid)
    return list(ids)


async def _run_sync_core(start_date: str, end_date: str, label: str):
    """内部同步核心逻辑，按指定日期范围采集所有广告账户的 GMVMax 数据"""
    logger.info(f"=== {label} started ({start_date} ~ {end_date}) ===")
    start = datetime.now()

    # 1. 先刷新过期 token
    await refresh_expired_tokens()

    # 2. 获取所有有效广告账户
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Advertiser).where(
                Advertiser.is_active == True,
                Advertiser.is_token_valid == True,
            )
        )
        advertisers = result.scalars().all()

        if not advertisers:
            logger.warning("No active advertisers to sync")
            return

        logger.info(f"Syncing {len(advertisers)} advertisers ({label})...")

        # 清除该日期范围内的旧数据，避免重复
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
        adv_ids = [adv.advertiser_id for adv in advertisers]
        await db.execute(
            MetricsSnapshot.__table__.delete().where(
                MetricsSnapshot.advertiser_id.in_(adv_ids),
                MetricsSnapshot.stat_date >= sd,
                MetricsSnapshot.stat_date <= ed,
            )
        )
        await db.flush()

        # 同步店铺信息到 DB（避免后续页面依赖实时 API）
        await _sync_stores(advertisers, db)

        # 同步 GMVMax 数据（Campaign → Item → Creative 按顺序执行，creative 依赖前两者的数据库记录）
        gmvmax_tasks = [
            sync_gmvmax(adv.advertiser_id, adv.access_token, db, start_date, end_date)
            for adv in advertisers
        ]
        await asyncio.gather(*gmvmax_tasks, return_exceptions=True)
        await db.flush()

        gmvmax_item_tasks = [
            sync_gmvmax_items(adv.advertiser_id, adv.access_token, db, start_date, end_date)
            for adv in advertisers
        ]
        await asyncio.gather(*gmvmax_item_tasks, return_exceptions=True)
        await db.flush()

        gmvmax_creative_tasks = [
            sync_gmvmax_creatives(adv.advertiser_id, adv.access_token, db, start_date, end_date)
            for adv in advertisers
        ]
        await asyncio.gather(*gmvmax_creative_tasks, return_exceptions=True)

        # 同步视频素材数据（Ad 级 → video_id 聚合，含视频封面/预览URL）
        creative_tasks = [
            sync_creatives(adv.advertiser_id, adv.access_token, db)
            for adv in advertisers
        ]
        await asyncio.gather(*creative_tasks, return_exceptions=True)

        # 更新 last_sync_at
        for adv in advertisers:
            adv.last_sync_at = datetime.now(timezone.utc)

        await db.commit()

        # === 同步完成，构建业务视图表 ===
        try:
            from app.services.view_builder import build_all_views
            await build_all_views(db)
            await db.commit()
        except Exception as e:
            logger.exception(f"[ViewBuilder] Failed to build views: {e}")

    elapsed = (datetime.now() - start).total_seconds()
    logger.info(f"=== {label} completed in {elapsed:.1f}s ===")


async def run_daily_sync():
    """每日同步任务（凌晨 2 点）：拉过去 7 天历史数据"""
    today = date.today()
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    await _run_sync_core(start_date, end_date, "Daily sync")


async def run_hourly_sync():
    """每小时同步任务：只拉今天的数据（实时更新）"""
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    await _run_sync_core(today_str, today_str, "Hourly sync (today)")

    # 同步完成后触发检测和决策
    await run_detection_and_decision()


async def run_full_sync(days: int = 60):
    """
    全量历史同步 — 拉取最近 N 天的全部数据。

    TikTok 报表 API 单次最多查 30 天，所以按 30 天一段分批拉取。
    例如 days=60 → 分 2 批：[60天前~31天前] + [30天前~今天]

    用途：首次部署、数据修复、新账户授权后的历史回填。
    完成后增量同步（hourly/daily）自动接管。
    """
    today = date.today()
    batch_size = 30  # TikTok API 单次最大天数

    # 从最远日期开始，按 30 天分段
    batches = []
    remaining = days
    cursor = today
    while remaining > 0:
        chunk = min(remaining, batch_size)
        batch_start = cursor - timedelta(days=chunk)
        batch_end = cursor - timedelta(days=1) if cursor != today else cursor
        batches.append((batch_start, batch_end))
        cursor = batch_start
        remaining -= chunk

    # 反转，从最早的批次开始同步
    batches.reverse()

    logger.info(f"=== Full sync: {days} days, {len(batches)} batches ===")
    for i, (start, end) in enumerate(batches, 1):
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")
        logger.info(f"  Batch {i}/{len(batches)}: {start_str} ~ {end_str}")
        try:
            await _run_sync_core(start_str, end_str, f"Full sync batch {i}/{len(batches)}")
        except Exception as e:
            logger.error(f"  Batch {i} failed: {e}")
            continue

    logger.info(f"=== Full sync completed ({days} days) ===")


# 向后兼容保留旧名称
async def run_sync():
    """已弃用，保留向后兼容。触发今日数据同步。"""
    await run_hourly_sync()
