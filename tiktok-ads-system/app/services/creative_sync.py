"""
素材级数据同步服务

流程：
1. 拉取广告账户下所有 Ad 的详情（获取 video_id）
2. 按 video_id 聚合同一素材在多个 Ad 下的指标
3. 计算 hook_rate / hold_rate 等素材特有指标
4. 判断生命周期阶段（WARM_UP / GROWTH / PEAK / DECAY / FATIGUE）
5. 存入 creative_snapshots 表
"""
from datetime import date, timedelta, datetime, timezone
from typing import Dict, List, Optional
from collections import defaultdict

import numpy as np
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.creative import Creative, CreativeSnapshot, LifecycleStage
from app.services.tiktok_client import TikTokClient, TikTokAPIError


# 生命周期判断阈值
LIFECYCLE_RULES = {
    # (天数下限, 天数上限, hook_rate变化斜率) -> 阶段
    "WARM_UP":  lambda days, slope, hook: days < 3,
    "GROWTH":   lambda days, slope, hook: days >= 3 and slope > 0.01 and hook >= 5.0,
    "PEAK":     lambda days, slope, hook: days >= 3 and abs(slope) <= 0.01 and hook >= 5.0,
    "DECAY":    lambda days, slope, hook: slope < -0.01 and hook >= 2.0,
    "FATIGUE":  lambda days, slope, hook: hook < 2.0 or (slope < -0.05 and days > 7),
}


def calc_hook_rate(play: int, watched_2s: int) -> float:
    """Hook Rate = 2秒留存率"""
    if not play or play <= 0:
        return 0.0
    return round(watched_2s / play * 100, 2)


def calc_hold_rate(play: int, watched_6s: int) -> float:
    """Hold Rate = 6秒留存率"""
    if not play or play <= 0:
        return 0.0
    return round(watched_6s / play * 100, 2)


def calc_lifecycle(days: int, hook_rates: List[float]) -> str:
    """
    根据投放天数和 hook_rate 趋势判断生命周期阶段

    冷启动保护：
    - 前3天：强制 WARM_UP，数据量不足，不做任何判断
    - 4-7天：可以判断 GROWTH/WARM_UP，但不判断 FATIGUE
    - 7天以上：全量判断
    """
    if not hook_rates or days < 1:
        return LifecycleStage.UNKNOWN

    # 前3天强制 WARM_UP（冷启动保护）
    if days < 3:
        return LifecycleStage.WARM_UP

    latest_hook = hook_rates[-1] if hook_rates else 0.0

    # 计算斜率（近5天）
    recent = hook_rates[-5:]
    if len(recent) >= 3:
        x = np.arange(len(recent), dtype=float)
        y = np.array(recent, dtype=float)
        x_mean, y_mean = x.mean(), y.mean()
        denom = ((x - x_mean) ** 2).sum()
        slope = float(((x - x_mean) * (y - y_mean)).sum() / denom) if denom > 1e-10 else 0.0
    else:
        slope = 0.0

    # 4-7天冷启动期：只允许判断 WARM_UP 和 GROWTH，不判断 FATIGUE/DECAY
    if days < 7:
        if slope > 0.01 and latest_hook >= 3.0:
            return LifecycleStage.GROWTH
        return LifecycleStage.WARM_UP  # 默认保持 WARM_UP

    # 7天以上：完整判断
    for stage, fn in LIFECYCLE_RULES.items():
        if fn(days, slope, latest_hook):
            return stage

    return LifecycleStage.UNKNOWN


class CreativeSyncService:

    def __init__(self, client: TikTokClient, db: AsyncSession):
        self.client = client
        self.db = db

    async def sync(self, advertiser_id: str):
        """
        同步一个广告账户下所有素材的数据
        """
        self._ad_info_cache: Dict[str, dict] = {}  # ad_id -> {video_id, ad_name, product_id, ...}

        today = date.today()
        start_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        snapshot_time = datetime.now(timezone.utc)

        # Step 1: 拉取 Ad 级别报表（含 video_id 维度）
        logger.info(f"[Creative Sync] {advertiser_id}: fetching ad-level report...")
        try:
            report = await self.client.get_report(
                data_level="AUCTION_AD",
                start_date=start_date,
                end_date=end_date,
                dimensions=["ad_id", "stat_time_day"],
                metrics=[
                    "spend", "impressions", "clicks", "ctr", "cpm", "cpc",
                    "conversion", "cost_per_conversion", "conversion_rate",
                    "video_play_actions", "video_watched_2s", "video_watched_6s",
                    "average_video_play", "likes", "comments", "shares",
                ],
                page_size=1000,
            )
        except TikTokAPIError as e:
            logger.error(f"[Creative Sync] report fetch failed: {e}")
            return

        rows = report.get("list", [])
        if not rows:
            logger.debug(f"[Creative Sync] {advertiser_id}: no AUCTION_AD report data, trying GMVMax ads...")
            # Fallback: 从 GMVMax campaign 下查找 Ad，仅同步视频信息（不写 snapshot）
            await self._sync_gmvmax_video_info(advertiser_id)
            return

        # Step 2: 获取 Ad 详情拿到 video_id 映射
        ad_ids = list({r["dimensions"]["ad_id"] for r in rows if r.get("dimensions", {}).get("ad_id")})
        video_map = await self._fetch_video_map(ad_ids)  # ad_id -> video_id

        # Step 2.5: 获取视频详情（封面图、预览 URL、文件名）
        unique_video_ids = list(set(video_map.values()))
        video_info_map = await self._fetch_video_info(unique_video_ids)
        if video_info_map:
            logger.info(f"[Creative Sync] {advertiser_id}: fetched video info for {len(video_info_map)}/{len(unique_video_ids)} videos")

        # 构建 video_id -> product_id 映射（从 ad detail 中提取）
        video_product_map: Dict[str, str] = {}
        video_name_map: Dict[str, str] = {}
        for ad_id, info in self._ad_info_cache.items():
            vid = info.get("video_id", "")
            pid = info.get("product_id", "")
            ad_name = info.get("ad_name", "")
            if vid and pid:
                video_product_map[vid] = pid
            if vid and ad_name:
                video_name_map[vid] = ad_name

        # Step 3: 按 (video_id, stat_date) 聚合
        # 结构: {(video_id, stat_date): {指标...}}
        aggregated: Dict[tuple, dict] = defaultdict(lambda: {
            "spend": 0.0, "impressions": 0, "clicks": 0,
            "ctr_sum": 0.0, "ctr_cnt": 0,
            "cpm_sum": 0.0, "cpc_sum": 0.0,
            "conversion": 0, "cost_per_conversion_sum": 0.0, "cpc_cnt": 0,
            "conversion_rate_sum": 0.0,
            "video_play_actions": 0, "video_watched_2s": 0, "video_watched_6s": 0,
            "average_video_play_sum": 0.0, "average_video_play_cnt": 0,
            "likes": 0, "comments": 0, "shares": 0,
            "ad_ids": set(),
        })

        for row in rows:
            dims = row.get("dimensions", {})
            m = row.get("metrics", {})
            ad_id = dims.get("ad_id", "")
            stat_date = dims.get("stat_time_day", str(today))
            video_id = video_map.get(ad_id)

            if not video_id:
                continue  # 没有 video_id 的跳过（图片广告等）

            key = (video_id, stat_date)
            agg = aggregated[key]

            agg["spend"]          += float(m.get("spend", 0) or 0)
            agg["impressions"]    += int(m.get("impressions", 0) or 0)
            agg["clicks"]         += int(m.get("clicks", 0) or 0)
            agg["conversion"]     += int(m.get("conversion", 0) or 0)
            agg["video_play_actions"] += int(m.get("video_play_actions", 0) or 0)
            agg["video_watched_2s"]   += int(m.get("video_watched_2s", 0) or 0)
            agg["video_watched_6s"]   += int(m.get("video_watched_6s", 0) or 0)
            agg["likes"]    += int(m.get("likes", 0) or 0)
            agg["comments"] += int(m.get("comments", 0) or 0)
            agg["shares"]   += int(m.get("shares", 0) or 0)

            # 均值类指标
            ctr = float(m.get("ctr", 0) or 0)
            if ctr > 0:
                agg["ctr_sum"] += ctr; agg["ctr_cnt"] += 1

            avg_play = float(m.get("average_video_play", 0) or 0)
            if avg_play > 0:
                agg["average_video_play_sum"] += avg_play
                agg["average_video_play_cnt"] += 1

            agg["ad_ids"].add(ad_id)

        # Step 4: 写入数据库
        saved = 0
        for (video_id, stat_date_str), agg in aggregated.items():
            stat_date_obj = date.fromisoformat(stat_date_str.split(" ")[0]) if isinstance(stat_date_str, str) else stat_date_str

            # 确保 Creative 记录存在，附带视频详情
            vinfo = video_info_map.get(video_id, {})
            creative = await self._upsert_creative(
                advertiser_id=advertiser_id,
                video_id=video_id,
                ad_id=next(iter(agg["ad_ids"]), ""),
                first_seen=stat_date_obj,
                video_url=vinfo.get("preview_url", ""),
                cover_url=vinfo.get("cover_url", ""),
                creative_name=video_name_map.get(video_id, "") or vinfo.get("file_name", ""),
                product_id=video_product_map.get(video_id, ""),
                duration=vinfo.get("duration"),
                width=vinfo.get("width"),
                height=vinfo.get("height"),
            )

            # 计算衍生指标
            plays = agg["video_play_actions"]
            hook_rate = calc_hook_rate(plays, agg["video_watched_2s"])
            hold_rate = calc_hold_rate(plays, agg["video_watched_6s"])
            ctr_avg = agg["ctr_sum"] / agg["ctr_cnt"] if agg["ctr_cnt"] > 0 else (
                agg["clicks"] / agg["impressions"] * 100 if agg["impressions"] > 0 else 0.0
            )
            avg_play = (agg["average_video_play_sum"] / agg["average_video_play_cnt"]
                        if agg["average_video_play_cnt"] > 0 else 0.0)

            # 计算生命周期（需要历史 hook_rate 序列）
            days_running = (stat_date_obj - creative.first_seen_date).days + 1 if creative.first_seen_date else 1
            hook_history = await self._get_hook_history(advertiser_id, video_id, days=14)
            hook_history.append(hook_rate)
            stage = calc_lifecycle(days_running, hook_history)

            snapshot = CreativeSnapshot(
                advertiser_id=advertiser_id,
                video_id=video_id,
                creative_id=creative.id,
                stat_date=stat_date_obj,
                snapshot_time=snapshot_time,
                ad_count=len(agg["ad_ids"]),
                spend=agg["spend"],
                impressions=agg["impressions"],
                clicks=agg["clicks"],
                ctr=ctr_avg,
                conversion=agg["conversion"],
                video_play_actions=plays,
                video_watched_2s=agg["video_watched_2s"],
                video_watched_6s=agg["video_watched_6s"],
                average_video_play=avg_play,
                hook_rate=hook_rate,
                hold_rate=hold_rate,
                days_running=days_running,
                lifecycle_stage=stage,
            )
            self.db.add(snapshot)

            # 更新 Creative 的生命周期状态
            creative.last_active_date = stat_date_obj
            creative.days_running = days_running
            creative.lifecycle_stage = stage
            creative.is_fatigue = "Y" if stage == LifecycleStage.FATIGUE else "N"

            saved += 1

        await self.db.flush()
        logger.info(f"[Creative Sync] {advertiser_id}: saved {saved} creative snapshots")

    async def _fetch_video_map(self, ad_ids: List[str]) -> Dict[str, str]:
        """
        批量获取 ad_id -> video_id 映射
        同时收集 ad_id -> {video_id, ad_name, product_id, adgroup_id} 的完整映射
        分批请求（每批最多 100 个）
        """
        video_map = {}
        batch_size = 100

        for i in range(0, len(ad_ids), batch_size):
            batch = ad_ids[i:i + batch_size]
            try:
                result = await self.client.get_ad_detail(batch)
                for ad in result.get("list", []):
                    ad_id = str(ad.get("ad_id", ""))
                    video_id = str(ad.get("video_id", ""))
                    if ad_id and video_id and video_id != "0":
                        video_map[ad_id] = video_id
                        # 同时存储额外信息到实例级缓存
                        item_group_ids = ad.get("item_group_ids") or []
                        self._ad_info_cache[ad_id] = {
                            "video_id": video_id,
                            "ad_name": ad.get("ad_name", ""),
                            "product_id": str(item_group_ids[0]) if item_group_ids else "",
                            "adgroup_id": str(ad.get("adgroup_id", "")),
                        }
            except TikTokAPIError as e:
                logger.warning(f"get_ad_detail batch failed: {e}")

        return video_map

    async def _fetch_video_info(self, video_ids: List[str]) -> Dict[str, dict]:
        """
        批量获取 video_id -> {preview_url, cover_url, file_name, duration, ...} 映射
        """
        info_map = {}
        batch_size = 50

        for i in range(0, len(video_ids), batch_size):
            batch = video_ids[i:i + batch_size]
            try:
                videos = await self.client.get_video_info(batch)
                for v in videos:
                    vid = str(v.get("video_id", ""))
                    if vid:
                        info_map[vid] = {
                            "preview_url": v.get("preview_url", ""),
                            "cover_url": v.get("video_cover_url", ""),
                            "file_name": v.get("file_name", ""),
                            "duration": v.get("duration"),
                            "width": v.get("width"),
                            "height": v.get("height"),
                        }
            except TikTokAPIError as e:
                logger.warning(f"get_video_info batch failed: {e}")

        return info_map

    async def _upsert_creative(
        self,
        advertiser_id: str,
        video_id: str,
        ad_id: str,
        first_seen: date,
        video_url: str = "",
        cover_url: str = "",
        creative_name: str = "",
        product_id: str = "",
        duration: Optional[float] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> Creative:
        """Creative 不存在则创建，存在则更新视频信息"""
        result = await self.db.execute(
            select(Creative).where(
                Creative.advertiser_id == advertiser_id,
                Creative.video_id == video_id,
            )
        )
        creative = result.scalar_one_or_none()

        if not creative:
            creative = Creative(
                advertiser_id=advertiser_id,
                video_id=video_id,
                ad_id=ad_id,
                first_seen_date=first_seen,
                video_url=video_url or None,
                cover_url=cover_url or None,
                creative_name=creative_name or None,
                product_id=product_id or None,
                duration=duration,
                width=width,
                height=height,
            )
            self.db.add(creative)
            await self.db.flush()
        else:
            # 更新已有记录的视频信息（之前可能为空）
            if video_url and not creative.video_url:
                creative.video_url = video_url
            if cover_url and not creative.cover_url:
                creative.cover_url = cover_url
            if creative_name and not creative.creative_name:
                creative.creative_name = creative_name
            if product_id and not creative.product_id:
                creative.product_id = product_id
            if duration and not creative.duration:
                creative.duration = duration
            if width and not creative.width:
                creative.width = width
            if height and not creative.height:
                creative.height = height

        return creative

    async def _sync_gmvmax_video_info(self, advertiser_id: str):
        """
        GMVMax 专用路径：通过 /gmv_max/video/get/ 获取商品关联的创意视频
        接口返回：item_id, text(标题), video_info(封面/预览URL), identity_info(达人), spu_id_list(商品)
        写入 Creative 表
        """
        # 1. 获取店铺信息（需要 store_id 和 bc_id）
        try:
            stores = await self.client.get_gmvmax_store_list()
        except TikTokAPIError as e:
            logger.warning(f"[Creative Sync] get store list failed for {advertiser_id}: {e}")
            stores = []

        # Fallback: 从 Store 表读取（API 返回空时兜底）
        if not stores:
            from app.models.store import Store
            store_result = await self.db.execute(select(Store).where(Store.is_active == True))
            db_stores = store_result.scalars().all()
            if db_stores:
                stores = [{"store_id": s.store_id, "store_authorized_bc_id": s.store_authorized_bc_id} for s in db_stores]
                logger.info(f"[Creative Sync] {advertiser_id}: using {len(stores)} stores from DB fallback")
            else:
                logger.debug(f"[Creative Sync] {advertiser_id}: no stores from API or DB, skip GMVMax video sync")
                return

        total_saved = 0
        for store in stores:
            store_id = str(store.get("store_id") or store.get("shop_id") or "")
            bc_id = str(store.get("store_authorized_bc_id") or store.get("bc_id") or "")
            if not store_id or not bc_id:
                continue

            # 2. 先获取达人身份列表（video/get 需要传 identity_list 才能返回数据）
            try:
                identities = await self.client.get_gmvmax_identities(
                    store_id=store_id,
                    store_authorized_bc_id=bc_id,
                )
            except TikTokAPIError as e:
                logger.warning(f"[Creative Sync] get identities failed for store {store_id}: {e}")
                identities = []

            # 3. 逐个 identity 调用 /gmv_max/video/get/ 获取创意视频列表
            all_items = []
            identity_targets = identities if identities else [None]
            for identity in identity_targets:
                try:
                    kwargs = {}
                    if identity:
                        kwargs["identity_list"] = [{
                            "identity_id": str(identity.get("identity_id", "")),
                            "identity_type": str(identity.get("identity_type", "")),
                            "store_id": store_id,
                        }]
                    items = await self.client.get_all_gmvmax_videos(
                        store_id=store_id,
                        store_authorized_bc_id=bc_id,
                        **kwargs,
                    )
                    all_items.extend(items)
                    if items:
                        iname = identity.get("display_name", "") if identity else "no-identity"
                        logger.info(f"[Creative Sync] identity '{iname}': {len(items)} videos")
                except TikTokAPIError as e:
                    logger.warning(f"[Creative Sync] gmvmax video get failed for store {store_id}: {e}")
                    continue

            if not all_items:
                logger.debug(f"[Creative Sync] {advertiser_id} store {store_id}: no GMVMax videos")
                continue

            logger.info(f"[Creative Sync] {advertiser_id} store {store_id}: found {len(all_items)} GMVMax creative videos")

            # 3. 解析并 upsert Creative 记录
            for item in all_items:
                item_id = str(item.get("item_id", ""))
                if not item_id:
                    continue

                vi = item.get("video_info", {})
                ii = item.get("identity_info", {})
                spu_ids = item.get("spu_id_list", [])
                video_id = str(vi.get("video_id", ""))

                # video_id 是必须的，没有就跳过
                if not video_id or video_id == "0":
                    continue

                creative_name = item.get("text", "")  # 创意标题
                product_id = str(spu_ids[0]) if spu_ids else ""
                preview_url = vi.get("preview_url", "")
                cover_url = vi.get("video_cover_url", "")
                duration = vi.get("duration")
                width = vi.get("width")
                height = vi.get("height")

                await self._upsert_creative(
                    advertiser_id=advertiser_id,
                    video_id=video_id,
                    ad_id=item_id,  # 用 item_id 作为 ad_id 标识
                    first_seen=date.today(),
                    video_url=preview_url,
                    cover_url=cover_url,
                    creative_name=creative_name,
                    product_id=product_id,
                    duration=float(duration) if duration else None,
                    width=int(width) if width else None,
                    height=int(height) if height else None,
                )
                total_saved += 1

            await self.db.flush()

        if total_saved:
            logger.info(f"[Creative Sync] {advertiser_id}: saved {total_saved} GMVMax creative records")
        else:
            logger.debug(f"[Creative Sync] {advertiser_id}: no GMVMax creative videos found")

    async def _get_hook_history(
        self,
        advertiser_id: str,
        video_id: str,
        days: int = 14,
    ) -> List[float]:
        """获取近 N 天的 hook_rate 历史（升序）"""
        since = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(CreativeSnapshot.hook_rate)
            .where(
                CreativeSnapshot.advertiser_id == advertiser_id,
                CreativeSnapshot.video_id == video_id,
                CreativeSnapshot.stat_date >= since,
            )
            .order_by(CreativeSnapshot.stat_date.asc())
        )
        return [float(r[0] or 0) for r in result.all()]
