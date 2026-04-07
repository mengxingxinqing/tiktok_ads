"""
Ads广告自动创建服务

目的：简化转化型Ads广告的创建流程
功能：
1. 创建推广计划（Campaign）→ 目标为CONVERSION
2. 创建广告组（AdGroup）→ 配置受众和出价
3. 创建广告（Ad）→ 绑定创意和落地页
4. 上传创意（视频/图片）

典型流程：
upload_video → create_campaign → create_adgroup → create_ad
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.tiktok_client import TikTokClient, TikTokAPIError
from app.models.advertiser import Advertiser
from app.models.decision import Decision


class AdsCampaignCreator:
    """
    高级Ads广告创建助手
    """

    def __init__(self, client: TikTokClient, db: AsyncSession):
        self.client = client
        self.db = db

    async def create_conversion_campaign(
        self,
        advertiser_id: str,
        campaign_name: str,
        daily_budget: float = 100.0,  # 默认日预算 $100
    ) -> Dict[str, Any]:
        """
        创建转化型推广计划（CONVERSION）
        
        Args:
            advertiser_id: 广告账户ID
            campaign_name: 计划名称，建议格式 "SKU_20260401_v1"
            daily_budget: 每日预算（USD）
        
        Returns:
            {
                "campaign_id": "...",
                "campaign_name": "...",
                "status": "ENABLE"
            }
        """
        try:
            result = await self.client.create_campaign(
                campaign_name=campaign_name,
                objective_type="CONVERSION",  # 转化目标
                budget=daily_budget,
                budget_mode="DAILY",
            )
            
            campaign_id = result.get("campaign_id")
            logger.info(f"Campaign created: {campaign_name} (ID: {campaign_id})")
            
            return {
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "status": "ENABLE",
                "daily_budget": daily_budget,
            }
        
        except TikTokAPIError as e:
            logger.error(f"Failed to create campaign: {e}")
            raise

    async def create_targeting_adgroup(
        self,
        campaign_id: str,
        adgroup_name: str,
        targeting: Dict[str, Any],
        bid_amount: float = 0.5,  # 默认出价 $0.5 CPC
        bid_type: str = "CPC",    # CPC, CPM, oCPC
    ) -> Dict[str, Any]:
        """
        创建定向广告组
        
        Args:
            campaign_id: 推广计划ID
            adgroup_name: 广告组名称，格式 "US_Female_21-35"
            targeting: 受众定向，示例：
                {
                    "age": ["21", "35"],
                    "gender": ["FEMALE"],
                    "location": ["US", "CA"],
                    "interest": ["fashion", "shopping"],
                    "placements": ["TIKTOK"],
                }
            bid_amount: 出价（$）
            bid_type: 出价类型
        
        Returns:
            {
                "adgroup_id": "...",
                "adgroup_name": "...",
                "bid": 0.5,
                "bid_type": "CPC"
            }
        """
        try:
            result = await self.client.create_adgroup(
                campaign_id=campaign_id,
                adgroup_name=adgroup_name,
                target_audience=targeting,
                bid_type=bid_type,
                bid=bid_amount,
            )
            
            adgroup_id = result.get("adgroup_id")
            logger.info(f"AdGroup created: {adgroup_name} (ID: {adgroup_id})")
            
            return {
                "adgroup_id": adgroup_id,
                "adgroup_name": adgroup_name,
                "bid": bid_amount,
                "bid_type": bid_type,
                "targeting": targeting,
            }
        
        except TikTokAPIError as e:
            logger.error(f"Failed to create adgroup: {e}")
            raise

    async def create_conversion_ad(
        self,
        adgroup_id: str,
        ad_name: str,
        video_id: Optional[str] = None,
        image_ids: Optional[List[str]] = None,
        ad_text: Optional[str] = None,
        landing_page_url: Optional[str] = None,
        call_to_action: str = "SHOP_NOW",
    ) -> Dict[str, Any]:
        """
        创建转化型广告
        
        Args:
            adgroup_id: 广告组ID
            ad_name: 广告名称
            video_id: 视频ID（优先使用，更高转化）
            image_ids: 图片ID列表（可选，若无视频）
            ad_text: 广告文案
            landing_page_url: 跳转链接（转化关键）
            call_to_action: 按钮文案，常见值：
                - SHOP_NOW: 立即购物
                - LEARN_MORE: 了解更多
                - SIGN_UP: 立即注册
                - GET_OFFER: 获取优惠
                - CONTACT_US: 联系我们
        
        Returns:
            {
                "ad_id": "...",
                "ad_name": "...",
                "status": "ENABLE"
            }
        """
        if not video_id and not image_ids:
            raise ValueError("video_id 和 image_ids 必须至少提供一个")
        
        try:
            result = await self.client.create_ad(
                adgroup_id=adgroup_id,
                ad_name=ad_name,
                video_id=video_id,
                image_ids=image_ids,
                ad_text=ad_text,
                landing_page_url=landing_page_url,
                call_to_action=call_to_action,
            )
            
            ad_id = result.get("ad_id")
            logger.info(f"Ad created: {ad_name} (ID: {ad_id})")
            
            return {
                "ad_id": ad_id,
                "ad_name": ad_name,
                "status": "ENABLE",
                "cta": call_to_action,
            }
        
        except TikTokAPIError as e:
            logger.error(f"Failed to create ad: {e}")
            raise

    async def create_full_campaign(
        self,
        advertiser_id: str,
        campaign_name: str,
        daily_budget: float,
        video_id: str,  # 已上传的视频ID
        landing_page_url: str,  # 转化落地页
        targeting: Dict[str, Any],
        ad_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        一键创建完整的转化型Ads广告

        流程：
        1. 创建推广计划（CONVERSION目标）
        2. 创建广告组（定向+出价）
        3. 创建广告（绑定视频+落地页）
        
        Args:
            advertiser_id: 广告账户
            campaign_name: 计划名称
            daily_budget: 日预算
            video_id: 上传的视频ID
            landing_page_url: 落地页URL
            targeting: 受众定向
            ad_text: 广告文案（可选）
        
        Returns:
            {
                "campaign_id": "...",
                "adgroup_id": "...",
                "ad_id": "...",
                "status": "success",
                "summary": {...}
            }
        """
        try:
            # 1. 创建推广计划
            campaign = await self.create_conversion_campaign(
                advertiser_id=advertiser_id,
                campaign_name=campaign_name,
                daily_budget=daily_budget,
            )
            campaign_id = campaign["campaign_id"]
            logger.info(f"✓ Campaign created: {campaign_id}")

            # 2. 创建广告组
            adgroup = await self.create_targeting_adgroup(
                campaign_id=campaign_id,
                adgroup_name=f"{campaign_name}_AdGroup_01",
                targeting=targeting,
                bid_amount=0.5,  # $0.5 CPC
            )
            adgroup_id = adgroup["adgroup_id"]
            logger.info(f"✓ AdGroup created: {adgroup_id}")

            # 3. 创建广告
            ad = await self.create_conversion_ad(
                adgroup_id=adgroup_id,
                ad_name=f"{campaign_name}_Ad_01",
                video_id=video_id,
                landing_page_url=landing_page_url,
                ad_text=ad_text,
                call_to_action="SHOP_NOW",
            )
            ad_id = ad["ad_id"]
            logger.info(f"✓ Ad created: {ad_id}")

            return {
                "status": "success",
                "campaign_id": campaign_id,
                "adgroup_id": adgroup_id,
                "ad_id": ad_id,
                "summary": {
                    "campaign_name": campaign_name,
                    "daily_budget": daily_budget,
                    "video_id": video_id,
                    "landing_page_url": landing_page_url,
                    "targeting": targeting,
                },
            }
        
        except Exception as e:
            logger.error(f"Failed to create full campaign: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }

    async def upload_and_create_campaign(
        self,
        advertiser_id: str,
        campaign_name: str,
        daily_budget: float,
        video_file_path: str,
        landing_page_url: str,
        targeting: Dict[str, Any],
        ad_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        上传视频 + 创建完整广告（全自动）
        
        这是最高级的方法：从视频文件直接生成投放广告
        """
        try:
            # 1. 上传视频
            logger.info(f"Uploading video: {video_file_path}")
            upload_result = await self.client.upload_video(
                file_path=video_file_path,
                video_name=f"{campaign_name}_video",
            )
            video_id = upload_result.get("video_id")
            logger.info(f"✓ Video uploaded: {video_id}")

            # 2. 创建完整广告流程
            return await self.create_full_campaign(
                advertiser_id=advertiser_id,
                campaign_name=campaign_name,
                daily_budget=daily_budget,
                video_id=video_id,
                landing_page_url=landing_page_url,
                targeting=targeting,
                ad_text=ad_text,
            )
        
        except Exception as e:
            logger.error(f"Failed to upload and create campaign: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }


class GmvmaxCampaignCreator:
    """
    GMVMAX 专用广告创建助手
    
    特点：
    - 自动优化（系统自动调整出价、人群、商品）
    - 简化配置（无需手动指定落地页和商品）
    - 全自动投放（基于 Shop 的商品库）
    """

    def __init__(self, client: TikTokClient, db: AsyncSession):
        self.client = client
        self.db = db

    async def create_gmvmax_campaign(
        self,
        advertiser_id: str,
        campaign_name: str,
        daily_budget: float = 100.0,
        shop_id: Optional[str] = None,
        roas_goal: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        创建 GMVMAX 推广计划

        Args:
            advertiser_id: 广告账户
            campaign_name: 计划名称
            daily_budget: 日预算
            shop_id: TikTok Shop ID（GMVMAX必需）
            roas_goal: ROI 目标（可选）

        Returns:
            campaign_id 等信息
        """
        if not shop_id:
            raise ValueError("GMVMAX 必须提供 shop_id")

        try:
            result = await self.client.create_gmvmax_campaign(
                campaign_name=campaign_name,
                budget=daily_budget,
                budget_mode="DAILY",
                shop_id=shop_id,
                roas_goal=roas_goal,
            )
            
            campaign_id = result.get("campaign_id")
            logger.info(f"GMVMAX Campaign created: {campaign_name} (ID: {campaign_id})")
            
            return {
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "daily_budget": daily_budget,
                "shop_id": shop_id,
                "mode": "GMVMAX",
            }
        
        except Exception as e:
            logger.error(f"Failed to create GMVMAX campaign: {e}")
            raise

    async def create_gmvmax_adgroup(
        self,
        campaign_id: str,
        adgroup_name: str,
        daily_budget: Optional[float] = None,
        targeting: Optional[Dict] = None,
        catalog_id: Optional[str] = None,
        item_group_ids: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        创建 GMVMAX 广告组
        
        GMVMAX 会自动优化以下参数，无需手动指定：
        - 出价（自动调整为最优价格）
        - 受众（自动扩展和优化）
        - 商品选择（自动选择最优商品）
        
        Args:
            campaign_id: 推广计划ID
            adgroup_name: 广告组名称
            daily_budget: 日预算（可选，会覆盖计划预算）
            targeting: 初始受众定向（可选，系统会自动扩展）
            catalog_id: 商品目录ID（可选，不指定则投放全部商品）
        
        Returns:
            adgroup_id 等信息
        """
        try:
            result = await self.client.create_gmvmax_adgroup(
                campaign_id=campaign_id,
                adgroup_name=adgroup_name,
                daily_budget=daily_budget,
                targeting=targeting,
                catalog_id=catalog_id,
                item_group_ids=item_group_ids,
            )
            
            adgroup_id = result.get("adgroup_id")
            logger.info(f"GMVMAX AdGroup created: {adgroup_name} (ID: {adgroup_id})")
            
            return {
                "adgroup_id": adgroup_id,
                "adgroup_name": adgroup_name,
                "auto_optimization": True,
            }
        
        except Exception as e:
            logger.error(f"Failed to create GMVMAX adgroup: {e}")
            raise

    async def create_gmvmax_ad(
        self,
        adgroup_id: str,
        ad_name: str,
        video_id: Optional[str] = None,
        image_ids: Optional[List[str]] = None,
        ad_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        创建 GMVMAX 广告
        
        GMVMAX 广告的特点：
        - 自动跳转到 Shop 中表现最好的商品
        - 无需手动指定落地页
        - 系统自动选择最优商品展示
        
        Args:
            adgroup_id: 广告组ID
            ad_name: 广告名称
            video_id: 视频ID（优先使用）
            image_ids: 图片ID列表
            ad_text: 广告文案（可选）
        
        Returns:
            ad_id 等信息
        """
        if not video_id and not image_ids:
            raise ValueError("video_id 和 image_ids 必须至少提供一个")
        
        try:
            result = await self.client.create_gmvmax_ad(
                adgroup_id=adgroup_id,
                ad_name=ad_name,
                video_id=video_id,
                image_ids=image_ids,
                ad_text=ad_text,
            )
            
            ad_id = result.get("ad_id")
            logger.info(f"GMVMAX Ad created: {ad_name} (ID: {ad_id})")
            
            return {
                "ad_id": ad_id,
                "ad_name": ad_name,
                "status": "ENABLE",
                "mode": "GMVMAX",
            }
        
        except Exception as e:
            logger.error(f"Failed to create GMVMAX ad: {e}")
            raise

    async def create_full_gmvmax_campaign(
        self,
        advertiser_id: str,
        campaign_name: str,
        daily_budget: float,
        shop_id: str,  # TikTok Shop ID
        video_id: Optional[str] = None,
        ad_text: Optional[str] = None,
        targeting: Optional[Dict] = None,
        catalog_id: Optional[str] = None,
        roas_goal: Optional[float] = None,
        item_group_ids: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        一键创建完整的 GMVMAX 广告

        流程：
        1. 创建推广计划（GMVMAX目标）
        2. 创建广告组（可配置初始定向，但系统会自动优化）
        3. 创建广告（绑定创意，可选）
        4. 系统自动：选择最优商品、优化人群、调整出价

        Args:
            advertiser_id: 广告账户
            campaign_name: 计划名称
            daily_budget: 日预算
            shop_id: TikTok Shop ID
            video_id: 上传的视频ID（可选）
            ad_text: 广告文案（可选）
            targeting: 初始受众定向（可选）
            catalog_id: 商品目录ID（可选）
            roas_goal: ROI 目标（可选）
            item_group_ids: 指定投放的商品ID列表（可选）

        Returns:
            campaign_id, adgroup_id, ad_id(可选)
        """
        try:
            # 1. 创建推广计划
            campaign = await self.create_gmvmax_campaign(
                advertiser_id=advertiser_id,
                campaign_name=campaign_name,
                daily_budget=daily_budget,
                shop_id=shop_id,
                roas_goal=roas_goal,
            )
            campaign_id = campaign["campaign_id"]
            logger.info(f"✓ GMVMAX Campaign created: {campaign_id}")

            # 2. 创建广告组
            adgroup = await self.create_gmvmax_adgroup(
                campaign_id=campaign_id,
                adgroup_name=f"{campaign_name}_AdGroup_01",
                targeting=targeting,
                catalog_id=catalog_id,
                item_group_ids=item_group_ids,
            )
            adgroup_id = adgroup["adgroup_id"]
            logger.info(f"✓ GMVMAX AdGroup created: {adgroup_id}")

            # 3. 创建广告（有视频时才创建）
            ad_id = None
            if video_id:
                ad = await self.create_gmvmax_ad(
                    adgroup_id=adgroup_id,
                    ad_name=f"{campaign_name}_Ad_01",
                    video_id=video_id,
                    ad_text=ad_text,
                )
                ad_id = ad["ad_id"]
                logger.info(f"✓ GMVMAX Ad created: {ad_id}")

            return {
                "status": "success",
                "mode": "GMVMAX",
                "campaign_id": campaign_id,
                "adgroup_id": adgroup_id,
                "ad_id": ad_id,
                "shop_id": shop_id,
                "summary": {
                    "campaign_name": campaign_name,
                    "daily_budget": daily_budget,
                    "roas_goal": roas_goal,
                    "video_id": video_id,
                    "item_group_ids": item_group_ids,
                    "targeting": targeting,
                    "auto_optimization": True,
                },
            }

        except Exception as e:
            logger.error(f"Failed to create full GMVMAX campaign: {e}")
            return {
                "status": "failed",
                "mode": "GMVMAX",
                "error": str(e),
            }
