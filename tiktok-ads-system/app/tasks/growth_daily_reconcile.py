"""
每日对账任务
- 每天 UTC 13:00 运行（避开 TikTok UTC 12:00 数据修正窗口）
- 拉取"前一天"的 /report/integrated/get/（AUCTION_CAMPAIGN 维度），按 campaign_id 汇总
- 指标：spend（本币） + follows（官方涨粉数）
- 写入 GrowthCampaign.official_* 字段（与轮询 total_spend / followers_gained 并存不覆盖）
- 对 COMPLETED Campaign，额外用官方数据刷新 CreativeMaterial.avg_cost_per_10k / total_*

不做：
- 覆盖 total_spend / followers_gained（这两个是运行时监控用的，保留快照）
- 回写当日数据（TikTok 当日数据未定稿，等次日再算）
"""
from datetime import datetime, timezone, date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
import json
import asyncio

from celery import shared_task
from loguru import logger
from sqlalchemy import select, or_

from app.core.database import AsyncSessionLocal
from app.models.ad_account import AdAccount
from app.models.growth_campaign import GrowthCampaign
from app.models.creative_material import CreativeMaterial
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from app.services import currency as fx


# 拉过去 N 天的数据（覆盖之前对账失败的情况）
_LOOKBACK_DAYS = 3


async def reconcile_yesterday() -> Dict[str, int]:
    """
    对账流程：
      1. 列出所有需要对账的 Campaign（RUNNING 或最近 7 天内 COMPLETED）
      2. 按 ad_account 分组，批量调 /report/integrated/get/
      3. 写入 official_* 字段
      4. 对已 COMPLETED 的 Campaign，聚合素材级别的成本回写
    """
    checked = 0
    updated = 0
    failed = 0
    material_refreshed = 0

    async with AsyncSessionLocal() as db:
        today = date.today()
        earliest_completed = today - timedelta(days=_LOOKBACK_DAYS)
        start_date = (today - timedelta(days=_LOOKBACK_DAYS)).strftime("%Y-%m-%d")
        end_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")

        result = await db.execute(
            select(GrowthCampaign).where(
                or_(
                    GrowthCampaign.status == "RUNNING",
                    GrowthCampaign.end_time >= datetime.combine(earliest_completed, datetime.min.time(), tzinfo=timezone.utc),
                )
            )
        )
        campaigns = result.scalars().all()

        # 按 ad_account 分组批调
        by_acct: Dict[str, List[GrowthCampaign]] = {}
        for c in campaigns:
            if c.tiktok_campaign_id:
                by_acct.setdefault(c.ad_account_id, []).append(c)

        for ad_account_id, cs in by_acct.items():
            acct_q = await db.execute(select(AdAccount).where(AdAccount.advertiser_id == ad_account_id))
            ad_account = acct_q.scalar_one_or_none()
            if not ad_account:
                failed += len(cs)
                continue

            client = TikTokClient(access_token=ad_account.access_token, advertiser_id=ad_account_id)
            try:
                report = await client.get_report(
                    data_level="AUCTION_CAMPAIGN",
                    start_date=start_date,
                    end_date=end_date,
                    dimensions=["campaign_id"],
                    metrics=["spend", "follows"],
                    filtering=json.dumps({"campaign_ids": [c.tiktok_campaign_id for c in cs]}),
                    page_size=1000,
                )
                rows = report.get("list", []) if isinstance(report, dict) else []

                by_id: Dict[str, Dict[str, Decimal]] = {}
                for row in rows:
                    dims = row.get("dimensions", {}) or {}
                    mets = row.get("metrics", {}) or {}
                    cid = dims.get("campaign_id") or row.get("campaign_id")
                    if not cid:
                        continue
                    spend_val = mets.get("spend") if mets else row.get("spend")
                    follows_val = mets.get("follows") if mets else row.get("follows")
                    by_id[str(cid)] = {
                        "spend": Decimal(str(spend_val)) if spend_val is not None else Decimal("0"),
                        "follows": Decimal(str(follows_val)) if follows_val is not None else Decimal("0"),
                    }

                for c in cs:
                    checked += 1
                    d = by_id.get(c.tiktok_campaign_id)
                    if d is None:
                        continue
                    c.official_spend_local = d["spend"]
                    c.official_spend_usd = await fx.to_usd(db, d["spend"], ad_account.currency)
                    c.official_followers_gained = int(d["follows"])
                    c.last_reconciled_at = datetime.now(timezone.utc)
                    updated += 1

            except TikTokAPIError as e:
                logger.error(f"[Reconcile] Report API error for {ad_account_id}: {e}")
                failed += len(cs)
            except Exception as e:
                logger.exception(f"[Reconcile] Unexpected error for {ad_account_id}: {e}")
                failed += len(cs)
            finally:
                await client.close()

        await db.commit()

        # 对 COMPLETED Campaign 聚合刷新 CreativeMaterial 成本
        material_refreshed = await _refresh_materials_from_official(db)

    logger.info(
        f"[Reconcile] checked={checked} updated={updated} failed={failed} "
        f"materials_refreshed={material_refreshed}"
    )
    return {
        "checked": checked,
        "updated": updated,
        "failed": failed,
        "materials_refreshed": material_refreshed,
    }


async def _refresh_materials_from_official(db) -> int:
    """
    以官方数据为准重算每个素材的累计花费 / 涨粉 / 万粉成本。
    只统计 status == COMPLETED 且 official_* 非空的 Campaign。
    """
    from sqlalchemy import func as sa_func

    # 对每个 (advertiser_id, video_id) 聚合 sum(official_spend_usd) + sum(official_followers_gained)
    result = await db.execute(
        select(
            GrowthCampaign.ad_account_id,
            GrowthCampaign.video_id,
            sa_func.sum(GrowthCampaign.official_spend_usd).label("sum_spend_usd"),
            sa_func.sum(GrowthCampaign.official_followers_gained).label("sum_followers"),
            sa_func.count(GrowthCampaign.id).label("sample_n"),
        )
        .where(
            GrowthCampaign.status == "COMPLETED",
            GrowthCampaign.official_spend_usd.isnot(None),
            GrowthCampaign.official_followers_gained.isnot(None),
        )
        .group_by(GrowthCampaign.ad_account_id, GrowthCampaign.video_id)
    )
    rows = result.all()

    refreshed = 0
    for r in rows:
        spend_usd = Decimal(str(r.sum_spend_usd or 0))
        followers = int(r.sum_followers or 0)
        sample_n = int(r.sample_n or 0)

        if followers <= 0:
            continue

        cost_per_10k = (spend_usd / Decimal(followers)) * Decimal("10000")

        mat_q = await db.execute(
            select(CreativeMaterial).where(
                CreativeMaterial.advertiser_id == r.ad_account_id,
                CreativeMaterial.video_id == r.video_id,
            )
        )
        material = mat_q.scalar_one_or_none()
        if not material:
            continue

        material.total_spend = spend_usd
        material.total_followers_gained = followers
        material.sample_count = sample_n
        material.cost_per_10k = cost_per_10k.quantize(Decimal("0.0001"))
        material.avg_cost_per_10k = cost_per_10k.quantize(Decimal("0.0001"))
        material.latest_cost_per_10k = cost_per_10k.quantize(Decimal("0.0001"))
        refreshed += 1

    await db.commit()
    return refreshed


@shared_task(name="growth.reconcile_daily")
def celery_reconcile():
    """Celery 入口"""
    asyncio.run(reconcile_yesterday())
