"""
评论数据同步服务

定时从 TikTok 拉取广告评论，存入数据库
后续可接入情感分析和飞书告警
"""
from datetime import datetime, timezone
from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.comment import AdComment
from app.services.tiktok_client import TikTokClient


class CommentSyncService:
    def __init__(self, client: TikTokClient, db: AsyncSession):
        self.client = client
        self.db = db

    async def sync(self, advertiser_id: str, ad_ids: list[str]) -> dict:
        """
        同步指定广告的评论数据

        Args:
            advertiser_id: 广告账户 ID
            ad_ids: 要同步评论的广告 ID 列表

        Returns:
            { "synced": int, "new": int, "updated": int }
        """
        if not ad_ids:
            return {"synced": 0, "new": 0, "updated": 0}

        total_new = 0
        total_updated = 0
        total_synced = 0

        # 分批处理（每次最多 20 个 ad_id）
        batch_size = 20
        for i in range(0, len(ad_ids), batch_size):
            batch = ad_ids[i:i + batch_size]
            try:
                comments = await self.client.get_all_comments(batch)
                logger.info(f"[CommentSync] 获取 {len(comments)} 条评论 (ads: {len(batch)})")

                for raw in comments:
                    new, updated = await self._upsert_comment(advertiser_id, raw)
                    total_new += new
                    total_updated += updated
                    total_synced += 1

            except Exception as e:
                logger.error(f"[CommentSync] 批次同步失败: {e}")
                continue

        await self.db.flush()
        logger.info(
            f"[CommentSync] 完成: 共 {total_synced} 条, "
            f"新增 {total_new}, 更新 {total_updated}"
        )

        return {"synced": total_synced, "new": total_new, "updated": total_updated}

    async def _upsert_comment(self, advertiser_id: str, raw: dict) -> tuple[int, int]:
        """插入或更新单条评论，返回 (new_count, updated_count)"""
        comment_id = str(raw.get("comment_id", ""))
        if not comment_id:
            return 0, 0

        result = await self.db.execute(
            select(AdComment).where(AdComment.comment_id == comment_id)
        )
        existing = result.scalar_one_or_none()

        # 解析评论时间
        comment_time = None
        raw_time = raw.get("create_time") or raw.get("comment_time")
        if raw_time:
            try:
                if isinstance(raw_time, (int, float)):
                    comment_time = datetime.fromtimestamp(raw_time, tz=timezone.utc)
                else:
                    comment_time = datetime.fromisoformat(str(raw_time))
            except (ValueError, OSError):
                pass

        # 公共字段
        fields = {
            "advertiser_id": advertiser_id,
            "ad_id": str(raw.get("ad_id", "")),
            "campaign_id": str(raw.get("campaign_id", "")) or None,
            "comment_id": comment_id,
            "parent_comment_id": str(raw.get("parent_comment_id", "")) or None,
            "content": raw.get("content") or raw.get("text", ""),
            "user_id": str(raw.get("user_id", "")) or None,
            "user_name": raw.get("user_name") or raw.get("display_name", ""),
            "user_avatar": raw.get("user_avatar") or raw.get("avatar_url", ""),
            "likes": raw.get("likes", 0) or 0,
            "replies": raw.get("replies", 0) or raw.get("reply_count", 0) or 0,
            "status": raw.get("status", "PUBLIC"),
            "comment_time": comment_time,
        }

        if existing:
            # 更新互动数据
            for key in ("likes", "replies", "status"):
                setattr(existing, key, fields[key])
            return 0, 1
        else:
            self.db.add(AdComment(**fields))
            return 1, 0


async def run_comment_sync():
    """
    定时任务入口：遍历所有活跃广告账户，同步评论

    当前仅入库，暂不触发告警
    """
    from app.core.database import AsyncSessionLocal
    from app.models.advertiser import Advertiser
    from app.models.metrics import MetricsSnapshot

    logger.info("[CommentSync] 开始评论同步任务")

    async with AsyncSessionLocal() as db:
        # 获取所有活跃账户
        result = await db.execute(
            select(Advertiser).where(
                Advertiser.is_active == True,
                Advertiser.is_token_valid == True,
            )
        )
        advertisers = result.scalars().all()

        if not advertisers:
            logger.info("[CommentSync] 没有活跃账户，跳过")
            return

        for adv in advertisers:
            try:
                # 获取该账户下近期有投放的 ad_id
                ad_result = await db.execute(
                    select(MetricsSnapshot.object_id)
                    .where(
                        MetricsSnapshot.advertiser_id == adv.advertiser_id,
                        MetricsSnapshot.data_level == "AD",
                    )
                    .distinct()
                    .limit(200)
                )
                ad_ids = [r[0] for r in ad_result.all()]

                if not ad_ids:
                    logger.debug(f"[CommentSync] {adv.advertiser_id} 无活跃广告，跳过")
                    continue

                client = TikTokClient(
                    access_token=adv.access_token,
                    advertiser_id=adv.advertiser_id,
                )
                service = CommentSyncService(client, db)
                stats = await service.sync(adv.advertiser_id, ad_ids)
                await client.close()

                logger.info(
                    f"[CommentSync] {adv.advertiser_id}: "
                    f"新增 {stats['new']}, 更新 {stats['updated']}"
                )

            except Exception as e:
                logger.error(f"[CommentSync] {adv.advertiser_id} 同步失败: {e}")
                continue

        await db.commit()

    logger.info("[CommentSync] 评论同步任务完成")
