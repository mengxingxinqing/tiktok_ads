"""
智能涨粉定时任务
每 15 分钟检查一次 RUNNING 状态的 Campaign：
1. 刷新 TK 账号粉丝数
2. 检查是否达标 → 自动停止
3. 检查万粉成本是否超限 → 告警
"""
import asyncio
from datetime import datetime, timezone, timedelta
from decimal import Decimal

from loguru import logger
from sqlalchemy import select, or_


# ======================= 自适应采集调度 =======================
# 核心思想：越接近目标，采集越密；越远越稀
# - 用上次采集到本次采集之间的粉丝增速估算 ETA
# - 下次采集时间 = now + ETA × 0.4，保证在达标前还能看到一次
# - 边界：[最小 5 分钟, 最大 2 小时]
#
# 举例：
#   目标 +10000，当前 +100，速率 50/小时 → ETA 198h → 下次 2h 后（封顶）
#   目标 +10000，当前 +9500，速率 50/小时 → ETA 10h → 下次 4h 后（封顶 2h）
#   目标 +10000，当前 +9950，速率 200/小时 → ETA 0.25h → 下次 5min 后

_MIN_INTERVAL = timedelta(minutes=5)
_MAX_INTERVAL = timedelta(hours=2)
_SPRINT_MAX_INTERVAL = timedelta(minutes=20)     # 冲刺区上限：~20 min
_SPRINT_MIN_INTERVAL = timedelta(minutes=15)     # 冲刺区下限：避免 ETA 突变引起 5 min 猛采
_SPRINT_THRESHOLD_RATIO = 0.05                    # 余量 / 目标 <= 5% 视为冲刺区
_SPRINT_THRESHOLD_ABS = 200                        # 余量 <= 200 视为冲刺区
_DEFAULT_INTERVAL = timedelta(minutes=30)        # 速率未知 / 没涨时的兜底
_ETA_FACTOR = 0.4                                # 在达标前提前多少触发下次


def _compute_next_check_at(
    now: datetime,
    baseline: int,
    current_followers: int,
    target_followers: int,
    last_check_at,
    last_check_followers,
) -> datetime:
    """
    根据当前差值与观测速率算下次采集时刻。
    """
    remaining = max(0, target_followers - (current_followers - baseline))
    if remaining <= 0:
        # 本轮就会触发达标停投，随便给个近未来值
        return now

    # 观测速率（followers / hour）
    velocity = None
    if last_check_at and last_check_followers is not None:
        elapsed_h = (now - last_check_at).total_seconds() / 3600.0
        if elapsed_h > 0:
            delta = max(0, current_followers - last_check_followers)
            if delta > 0:
                velocity = delta / elapsed_h

    # 冲刺区：余量 <= 5% of target 或 <= 200，强制用更短的上限，避免错过达标
    sprint_zone = remaining <= max(
        _SPRINT_THRESHOLD_ABS,
        int(target_followers * _SPRINT_THRESHOLD_RATIO),
    )

    if not velocity or velocity <= 0:
        # 没涨或第一次：冲刺区上限，非冲刺区默认 30min
        default = _SPRINT_MAX_INTERVAL if sprint_zone else _DEFAULT_INTERVAL
        return now + default

    eta_hours = remaining / velocity
    next_in = timedelta(seconds=eta_hours * 3600 * _ETA_FACTOR)

    if sprint_zone:
        # 冲刺区夹在 [15min, 20min]
        if next_in < _SPRINT_MIN_INTERVAL:
            next_in = _SPRINT_MIN_INTERVAL
        elif next_in > _SPRINT_MAX_INTERVAL:
            next_in = _SPRINT_MAX_INTERVAL
    else:
        if next_in < _MIN_INTERVAL:
            next_in = _MIN_INTERVAL
        elif next_in > _MAX_INTERVAL:
            next_in = _MAX_INTERVAL
    return now + next_in

from app.core.database import AsyncSessionLocal
from app.models.tk_account import TkAccount
from app.models.growth_campaign import GrowthCampaign
from app.models.creative_material import CreativeMaterial
from app.models.ad_account import AdAccount
from app.services.follower_scraper import TikTokFollowerScraper
from app.services.growth_notifier import GrowthFeishuNotifier
from app.services.budget_calculator import BudgetCalculator
from app.services.growth_spend_sync import sync_spend_for_running
from app.core.config import settings


async def check_growth_campaigns():
    """
    定时检查所有 RUNNING 状态的 Campaign
    """
    logger.info("[GrowthMonitor] Starting growth campaign check...")

    scraper = TikTokFollowerScraper()
    notifier = GrowthFeishuNotifier(webhook_url=settings.FEISHU_WEBHOOK_URL)

    async with AsyncSessionLocal() as db:
        # Step 1: 先刷新花费，让后续万粉成本 / 预算判定用上最新值
        try:
            await sync_spend_for_running(db)
        except Exception as e:
            logger.exception(f"[GrowthMonitor] spend sync failed: {e}")

        # Step 2: 只处理到达 next_check_at 的 RUNNING Campaign（自适应调度）
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(GrowthCampaign).where(
                GrowthCampaign.status == "RUNNING",
                or_(
                    GrowthCampaign.next_check_at.is_(None),
                    GrowthCampaign.next_check_at <= now,
                ),
            )
        )
        campaigns = result.scalars().all()

        if not campaigns:
            logger.debug("[GrowthMonitor] No campaigns due for check")
            return

        logger.info(
            f"[GrowthMonitor] Due for check: {len(campaigns)} "
            f"(pool is throttled by next_check_at)"
        )

        for campaign in campaigns:
            await _check_single_campaign(db, campaign, scraper, notifier)

    await notifier._client.aclose()
    logger.info("[GrowthMonitor] Campaign check completed")


async def _check_single_campaign(db, campaign, scraper, notifier):
    """
    检查单个 Campaign

    达标判定基于 baseline_followers（Campaign 启动瞬间的粉丝快照），
    不再依赖上一轮 scrape 的差值，避免 15 分钟区间漂移。
    """
    try:
        # 1. 获取最新的 TK 账号粉丝数
        tk_result = await db.execute(
            select(TkAccount).where(TkAccount.account_id == campaign.tk_account_id)
        )
        tk = tk_result.scalar_one_or_none()
        if not tk:
            logger.warning(f"[GrowthMonitor] TK account {campaign.tk_account_id} not found")
            return

        previous_followers = tk.follower_count or 0

        # 刷新粉丝数（用 asyncio.to_thread 包装同步 Playwright 调用）
        new_count = await asyncio.to_thread(scraper.get_follower_count, tk.account_id)

        now = datetime.now(timezone.utc)

        if new_count is None:
            # 爬粉失败：累计失败次数，下次采集推迟一个指数退避档
            campaign.scrape_failure_count = (campaign.scrape_failure_count or 0) + 1
            # 5, 10, 20, 40, 60 分钟 回退
            backoff = min(60, 5 * (2 ** min(3, campaign.scrape_failure_count - 1)))
            campaign.next_check_at = now + timedelta(minutes=backoff)
            logger.warning(
                f"[GrowthMonitor] Campaign {campaign.campaign_id[:8]} scrape failed "
                f"({campaign.scrape_failure_count} consecutive, next in {backoff}m)"
            )
            if campaign.scrape_failure_count >= 5:
                # 连续 5 次失败：账号很可能被封/改名，直接暂停
                await _stop_campaign(db, campaign, tk, 0, notifier, "SCRAPE_FAILED")
                return
            await db.commit()
            return

        # 爬粉成功：重置失败计数
        campaign.scrape_failure_count = 0
        tk.follower_count = new_count
        tk.follower_updated_at = now

        # 2. 基于 baseline 计算累计涨粉
        # 对历史 Campaign（无 baseline）做一次补写：把上一轮粉丝数当作 baseline
        if campaign.baseline_followers is None:
            campaign.baseline_followers = previous_followers
            logger.info(
                f"[GrowthMonitor] Backfilled baseline for {campaign.campaign_id[:8]} "
                f"= {previous_followers}"
            )

        followers_gained = max(0, new_count - (campaign.baseline_followers or 0))
        campaign.followers_gained = followers_gained

        logger.info(
            f"[GrowthMonitor] Campaign {campaign.campaign_id[:8]}: "
            f"followers {new_count} (baseline {campaign.baseline_followers}, "
            f"gained +{followers_gained} / target +{campaign.target_followers})"
        )

        # 3. 达标判定
        if followers_gained >= campaign.target_followers:
            await _stop_campaign(db, campaign, tk, followers_gained, notifier, "REACHED_TARGET")
            return

        # 4. 预算耗尽判定（USD 口径）——Case 3：烧完但未达标 → 飞书告警，不自动决策
        if campaign.total_spend and campaign.budget and float(campaign.total_spend) >= float(campaign.budget):
            try:
                await notifier.notify_budget_exhausted_undershoot(
                    campaign_id=campaign.campaign_id,
                    tk_account=tk.account_id,
                    followers_gained=followers_gained,
                    target_followers=campaign.target_followers,
                    total_spend=float(campaign.total_spend),
                    budget=float(campaign.budget),
                    currency="USD",
                )
            except Exception as e:
                logger.warning(f"[GrowthMonitor] Failed to send undershoot alert: {e}")
            await _stop_campaign(db, campaign, tk, followers_gained, notifier, "OVER_BUDGET")
            return

        # 5. 万粉成本超限告警（超 1.2× 目标）
        if campaign.total_spend and float(campaign.total_spend) > 0 and followers_gained > 0:
            real_cost = float(campaign.total_spend) / followers_gained * 10000
            target_cost = float(campaign.target_cost_per_10k or 35)

            if real_cost > target_cost * 1.2:
                logger.warning(
                    f"[GrowthMonitor] Campaign {campaign.campaign_id[:8]} cost alert: "
                    f"${real_cost:.2f}/10k > ${target_cost:.2f}/10k × 1.2"
                )
                await notifier.notify_cost_alert(
                    campaign_id=campaign.campaign_id,
                    tk_account=tk.account_id,
                    current_cost=real_cost,
                    target_cost=target_cost,
                )

        # 6. 计算下次采集时间（自适应）
        next_at = _compute_next_check_at(
            now=now,
            baseline=campaign.baseline_followers or 0,
            current_followers=new_count,
            target_followers=campaign.target_followers,
            last_check_at=campaign.last_check_at,
            last_check_followers=campaign.last_check_followers,
        )
        campaign.last_check_at = now
        campaign.last_check_followers = new_count
        campaign.next_check_at = next_at
        logger.info(
            f"[GrowthMonitor] Campaign {campaign.campaign_id[:8]} "
            f"next check @ {next_at.isoformat()} "
            f"(remaining {max(0, campaign.target_followers - followers_gained)} followers)"
        )

        await db.commit()

    except Exception as e:
        logger.exception(f"[GrowthMonitor] Error checking campaign {campaign.campaign_id}: {e}")
        await db.rollback()


async def _stop_campaign(db, campaign, tk, followers_gained, notifier, reason):
    """停止 Campaign 并更新成本"""
    try:
        # 调用 TikTok API 真实停投
        from app.models.ad_account import AdAccount
        from app.services.tiktok_client import TikTokClient, TikTokAPIError
        from app.services.growth_campaign_creator import GrowthCampaignCreator

        acct_result = await db.execute(
            select(AdAccount).where(AdAccount.advertiser_id == campaign.ad_account_id)
        )
        ad_account = acct_result.scalar_one_or_none()

        if campaign.tiktok_campaign_id and ad_account is not None:
            try:
                client = TikTokClient(
                    access_token=ad_account.access_token,
                    advertiser_id=campaign.ad_account_id,
                )
                creator = GrowthCampaignCreator(client=client, db=db)
                await creator.stop_ad(campaign.tiktok_campaign_id)
                await client.close()
            except TikTokAPIError as e:
                logger.warning(f"[GrowthMonitor] TikTok stop failed: {e}, continue with local state")

        # 释放预算预留
        if ad_account is not None and campaign.budget:
            reserved = float(ad_account.reserved_budget_usd or 0)
            ad_account.reserved_budget_usd = max(0, reserved - float(campaign.budget))

        # 更新 Campaign
        campaign.status = "COMPLETED" if reason == "REACHED_TARGET" else "PAUSED"
        campaign.end_time = datetime.now(timezone.utc)
        campaign.auto_stop_reason = reason
        campaign.followers_gained = followers_gained

        # 更新 TK 账号
        tk.status = "COMPLETED" if reason == "REACHED_TARGET" else "PAUSED"
        tk.completed_at = datetime.now(timezone.utc)
        # 不再给 follower_count 累加：follower_count 已是 scrape 到的实时值

        # 素材成本回写由 growth_daily_reconcile 每日 T+1 用官方 follows+spend 统一处理
        # 这里不再用轮询数据刷 CreativeMaterial，避免脏数据进入"官方真值"表

        await db.commit()

        # 发飞书通知
        spend = float(campaign.total_spend or 0)
        await notifier.notify_campaign_completed(
            campaign_id=campaign.campaign_id,
            tk_account=tk.account_id,
            followers_gained=followers_gained,
            total_spend=spend,
            auto_stop_reason=reason,
        )

        logger.info(
            f"[GrowthMonitor] Campaign {campaign.campaign_id[:8]} stopped: "
            f"{reason}, followers_gained={followers_gained}, spend=${spend:.2f}"
        )

    except Exception as e:
        logger.exception(f"[GrowthMonitor] Error stopping campaign {campaign.campaign_id}: {e}")


# ==================== Celery Beat 任务注册 ====================
from celery import shared_task

@shared_task(name="growth.check_campaigns")
def celery_check_campaigns():
    """Celery 包装（同步入口）"""
    asyncio.run(check_growth_campaigns())
