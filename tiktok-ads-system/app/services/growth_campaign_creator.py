"""
智能涨粉广告创建服务（Spark Ads / AUTH_CODE 方式）

流程（对应 docs/tiktok-api/create_spark_ads.md §"Pull organic posts from authorization codes"）：
  1. TK 账号所有者在 TikTok App 里为某条视频生成 auth_code
  2. 前端上送 auth_code 给后端
  3. 后端调 /tt_video/authorize/ 把帖子绑定到目标广告户
  4. 调 /tt_video/list/ 拿到 identity_id + item_id（video_id）
  5. 创建 Campaign / AdGroup / Ad（identity_type=AUTH_CODE）
"""
from decimal import Decimal
from typing import Dict, Any, Optional
import json
import uuid

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.tiktok_client import TikTokClient, TikTokAPIError
from app.models.ad_account import AdAccount
from app.models.tk_account import TkAccount
from app.models.creative_material import CreativeMaterial


# 涨粉投放默认参数（通用稳妥值，各地区可能需要微调）
DEFAULT_PLACEMENT = ["PLACEMENT_TIKTOK"]
DEFAULT_BILLING_EVENT = "CPC"
DEFAULT_OPTIMIZATION_GOAL = "CLICK"   # TikTok "涨粉"类广告多用 CLICK/VIDEO_VIEW
DEFAULT_PACING = "PACING_MODE_SMOOTH"
DEFAULT_SCHEDULE_TYPE = "SCHEDULE_FROM_NOW"
DEFAULT_OBJECTIVE = "TRAFFIC"          # ENGAGEMENT 在新版 API 已下线，用 TRAFFIC 把用户引到 TK 主页
DEFAULT_LOCATION_IDS = ["6252001"]     # 默认美国；调用方可覆盖
DEFAULT_AGE_GROUPS = ["AGE_18_24", "AGE_25_34", "AGE_35_44"]


class GrowthCampaignCreator:
    """涨粉广告创建器（Spark Ads）"""

    def __init__(self, client: TikTokClient, db: AsyncSession):
        self.client = client
        self.db = db

    async def bind_auth_code(
        self,
        auth_code: str,
    ) -> Dict[str, Any]:
        """
        绑定一条 auth_code 到当前广告户。
        返回该授权的 identity_id / item_id / display_name / preview_url 等。
        """
        await self.client.tt_video_authorize(auth_code=auth_code)

        # 查列表找回这条授权的详情
        info = await self.client.tt_video_info(auth_code=auth_code)
        if not info:
            raise TikTokAPIError(-1, f"auth_code {auth_code} 绑定后未查到详情")

        # /tt_video/info/ 的返回结构参见 docs/tiktok-api/create_spark_ads.md
        item_info = info.get("item_info", {})
        user_info = info.get("user_info", {})
        auth_info = info.get("auth_info", {})
        video_info = info.get("video_info", {})

        return {
            "auth_code": auth_code,
            "item_id": item_info.get("item_id"),
            "identity_id": user_info.get("identity_id"),
            "identity_type": user_info.get("identity_type") or "AUTH_CODE",
            "display_name": user_info.get("display_name"),
            "ad_auth_status": auth_info.get("ad_auth_status"),
            "auth_end_time": auth_info.get("auth_end_time"),
            "preview_url": video_info.get("preview_url"),
            "poster_url": video_info.get("poster_url"),
            "duration": video_info.get("duration"),
        }

    async def create_growth_campaign(
        self,
        tk_account: TkAccount,
        ad_account: AdAccount,
        video_id: str,                # CreativeMaterial.video_id（即 item_id）
        budget_local: Decimal,
        target_cost_per_10k: Decimal = Decimal("35.0"),
        campaign_name: Optional[str] = None,
        ad_text: Optional[str] = None,
        identity_id: Optional[str] = None,
        identity_type: str = "AUTH_CODE",
    ) -> Dict[str, Any]:
        """创建完整 Spark Ad（Campaign + AdGroup + Ad）。"""
        # 1. 定位素材（拿 identity_id / item_id）
        if not identity_id:
            # 从 CreativeMaterial 里找
            from sqlalchemy import select
            result = await self.db.execute(
                select(CreativeMaterial).where(
                    CreativeMaterial.advertiser_id == ad_account.advertiser_id,
                    CreativeMaterial.video_id == video_id,
                )
            )
            material = result.scalar_one_or_none()
            if not material or not material.identity_id:
                raise TikTokAPIError(-1, f"素材 {video_id} 在广告户 {ad_account.advertiser_id} 没有 identity 绑定")
            identity_id = material.identity_id
            identity_type = material.identity_type or "AUTH_CODE"
            item_id = material.item_id or video_id
        else:
            item_id = video_id

        campaign_name = campaign_name or f"growth_{tk_account.account_id}_{uuid.uuid4().hex[:6]}"

        # 2. Campaign
        # budget 单位为本币，与广告户 currency 一致
        campaign_result = await self.client.create_campaign(
            campaign_name=campaign_name,
            objective_type=DEFAULT_OBJECTIVE,
            budget=float(budget_local),
            budget_mode="BUDGET_MODE_TOTAL",   # 涨粉用总预算，达标即可停
        )
        tiktok_campaign_id = campaign_result.get("campaign_id")
        logger.info(f"[SparkAds] Campaign created: {tiktok_campaign_id}")

        # 3. AdGroup（必填字段按 TRAFFIC + TikTok 位置）
        adgroup_name = f"{campaign_name}_AG"
        adgroup_body = {
            "campaign_id": tiktok_campaign_id,
            "adgroup_name": adgroup_name,
            "placement_type": "PLACEMENT_TYPE_NORMAL",
            "placements": DEFAULT_PLACEMENT,
            "budget_mode": "BUDGET_MODE_TOTAL",
            "budget": float(budget_local),
            "schedule_type": DEFAULT_SCHEDULE_TYPE,
            "pacing": DEFAULT_PACING,
            "billing_event": DEFAULT_BILLING_EVENT,
            "optimization_goal": DEFAULT_OPTIMIZATION_GOAL,
            "bid_type": "BID_TYPE_NO_BID",     # 自动出价
            "location_ids": DEFAULT_LOCATION_IDS,
            "age_groups": DEFAULT_AGE_GROUPS,
            "gender": "GENDER_UNLIMITED",
            "operating_systems": ["ANDROID", "IOS"],
            "promotion_type": "WEBSITE",
            "landing_page_url": tk_account.profile_url or f"https://www.tiktok.com/@{tk_account.account_id}",
        }
        adgroup_result = await self.client.create_adgroup(**adgroup_body)
        tiktok_adgroup_id = adgroup_result.get("adgroup_id")
        logger.info(f"[SparkAds] AdGroup created: {tiktok_adgroup_id}")

        # 4. Ad（Spark Ads：identity_type=AUTH_CODE，走新格式的 creatives 数组）
        creatives = [{
            "ad_name": f"{campaign_name}_AD",
            "identity_type": identity_type,
            "identity_id": identity_id,
            "ad_format": "SINGLE_VIDEO",
            "video_id": item_id,
            "ad_text": ad_text or f"Follow @{tk_account.account_id} for more!",
            "call_to_action": "LEARN_MORE",
        }]
        ad_result = await self.client.create_ad_spark(
            adgroup_id=tiktok_adgroup_id,
            creatives=creatives,
        )
        ad_ids = ad_result.get("ad_ids", [])
        tiktok_ad_id = ad_ids[0] if ad_ids else None
        logger.info(f"[SparkAds] Ad created: {tiktok_ad_id}")

        return {
            "tiktok_campaign_id": tiktok_campaign_id,
            "tiktok_adgroup_id": tiktok_adgroup_id,
            "tiktok_ad_id": tiktok_ad_id,
            "identity_id": identity_id,
            "identity_type": identity_type,
            "post_id": item_id,
            "budget_local": float(budget_local),
            "currency": ad_account.currency,
            "status": "success",
        }

    async def stop_ad(self, tiktok_campaign_id: str) -> Dict[str, Any]:
        """暂停 Spark Ads Campaign。"""
        try:
            await self.client.update_campaign_status(
                campaign_ids=[tiktok_campaign_id],
                operation_status="DISABLE",
            )
            logger.info(f"[SparkAds] Campaign stopped: {tiktok_campaign_id}")
            return {"status": "stopped", "campaign_id": tiktok_campaign_id}
        except TikTokAPIError as e:
            logger.error(f"[SparkAds] Stop failed: {e}")
            raise
