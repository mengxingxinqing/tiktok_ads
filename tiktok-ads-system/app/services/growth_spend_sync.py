"""
涨粉 Campaign 花费同步
- 读取所有 RUNNING 状态的 Campaign
- 按 ad_account 分组，拉取 TikTok /report/integrated/get/（AUCTION_CAMPAIGN）
- 更新 total_spend_local（本币）与 total_spend（USD 换算）
"""
from datetime import datetime, timezone, date, timedelta
from decimal import Decimal
from typing import Dict, List
import json

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ad_account import AdAccount
from app.models.growth_campaign import GrowthCampaign
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from app.services import currency as fx


async def sync_spend_for_running(db: AsyncSession) -> Dict[str, int]:
    """
    同步所有 RUNNING 状态 Campaign 的花费。
    返回：{"checked": N, "updated": M, "failed": K}
    """
    result = await db.execute(
        select(GrowthCampaign).where(GrowthCampaign.status == "RUNNING")
    )
    campaigns = result.scalars().all()

    # 按 ad_account_id 分组
    by_acct: Dict[str, List[GrowthCampaign]] = {}
    for c in campaigns:
        if c.tiktok_campaign_id:
            by_acct.setdefault(c.ad_account_id, []).append(c)

    checked = 0
    updated = 0
    failed = 0

    for ad_account_id, cs in by_acct.items():
        acct_result = await db.execute(
            select(AdAccount).where(AdAccount.advertiser_id == ad_account_id)
        )
        ad_account = acct_result.scalar_one_or_none()
        if not ad_account:
            failed += len(cs)
            continue

        client = TikTokClient(
            access_token=ad_account.access_token,
            advertiser_id=ad_account_id,
        )
        try:
            # 拉最近 14 天，一次 API 覆盖多个 campaign
            start_date = (date.today() - timedelta(days=14)).strftime("%Y-%m-%d")
            end_date = date.today().strftime("%Y-%m-%d")
            campaign_ids = [c.tiktok_campaign_id for c in cs]

            report = await client.get_report(
                data_level="AUCTION_CAMPAIGN",
                start_date=start_date,
                end_date=end_date,
                dimensions=["campaign_id"],
                metrics=["spend"],
                filtering=json.dumps({"campaign_ids": campaign_ids}),
                page_size=1000,
            )
            rows = report.get("list", []) if isinstance(report, dict) else []

            spend_by_id: Dict[str, Decimal] = {}
            for row in rows:
                dims = row.get("dimensions", {})
                mets = row.get("metrics", {})
                cid = dims.get("campaign_id") or row.get("campaign_id")
                val = mets.get("spend") if mets else row.get("spend")
                if cid and val is not None:
                    spend_by_id[str(cid)] = Decimal(str(val))

            for c in cs:
                checked += 1
                spend_local = spend_by_id.get(c.tiktok_campaign_id)
                if spend_local is None:
                    continue
                spend_usd = await fx.to_usd(db, spend_local, ad_account.currency)
                c.total_spend_local = spend_local
                c.total_spend = spend_usd
                c.last_spend_synced_at = datetime.now(timezone.utc)
                updated += 1
        except TikTokAPIError as e:
            logger.error(f"[GrowthSpend] Report API error for acct {ad_account_id}: {e}")
            failed += len(cs)
        except Exception as e:
            logger.exception(f"[GrowthSpend] Unexpected error for acct {ad_account_id}: {e}")
            failed += len(cs)
        finally:
            await client.close()

    await db.commit()
    logger.info(f"[GrowthSpend] checked={checked} updated={updated} failed={failed}")
    return {"checked": checked, "updated": updated, "failed": failed}
