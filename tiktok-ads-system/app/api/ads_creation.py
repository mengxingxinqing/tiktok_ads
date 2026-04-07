"""
Ads广告创建接口

POST /ads/campaign/create              创建推广计划（CONVERSION目标）
POST /ads/campaign/create-full         一键创建完整Ads广告
POST /ads/gmvmax/campaign/create-full  一键创建完整GMVMAX广告
POST /ads/video/upload                 上传视频创意
POST /ads/image/upload                 上传图片创意
"""
from typing import Optional, List, Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.services.tiktok_client import TikTokClient
from app.services.ads_campaign_creator import AdsCampaignCreator, GmvmaxCampaignCreator
from sqlalchemy import select

router = APIRouter(prefix="/ads", tags=["Ads Creation"])


@router.post("/campaign/create")
async def create_conversion_campaign(
    advertiser_id: str,
    campaign_name: str,
    daily_budget: float = 100.0,
    db: AsyncSession = Depends(get_db),
):
    """
    创建CONVERSION目标的推广计划
    
    参数：
    - advertiser_id: 广告账户ID
    - campaign_name: 计划名称，建议格式 "SKU_20260401_v1"
    - daily_budget: 每日预算（USD），默认 $100
    
    返回：
    {
        "status": "success",
        "campaign_id": "...",
        "campaign_name": "...",
        "daily_budget": 100.0
    }
    """
    # 验证广告主
    result = await db.execute(
        select(Advertiser).where(
            Advertiser.advertiser_id == advertiser_id,
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found or inactive")

    try:
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )
        creator = AdsCampaignCreator(client, db)
        
        campaign = await creator.create_conversion_campaign(
            advertiser_id=advertiser_id,
            campaign_name=campaign_name,
            daily_budget=daily_budget,
        )
        
        await client.close()
        
        return {
            "status": "success",
            "data": campaign,
        }
    
    except Exception as e:
        logger.error(f"Failed to create campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/campaign/create-full")
async def create_full_ads_campaign(
    advertiser_id: str,
    campaign_name: str,
    daily_budget: float,
    video_id: str,
    landing_page_url: str,
    targeting: Dict[str, Any],  # JSON格式的受众定向
    ad_text: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    一键创建完整的转化型Ads广告
    
    参数：
    - advertiser_id: 广告账户ID
    - campaign_name: 计划名称
    - daily_budget: 日预算（USD）
    - video_id: 已上传的视频ID
    - landing_page_url: 落地页URL（转化链接）
    - targeting: 受众定向JSON，示例：
        {
            "age": ["21", "35"],
            "gender": ["FEMALE"],
            "location": ["US", "CA"],
            "interest": ["shopping", "fashion"],
            "placements": ["TIKTOK"]
        }
    - ad_text: 广告文案（可选）
    
    返回：完整的campaign/adgroup/ad信息
    """
    # 验证广告主
    result = await db.execute(
        select(Advertiser).where(
            Advertiser.advertiser_id == advertiser_id,
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found or inactive")

    try:
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )
        creator = AdsCampaignCreator(client, db)
        
        result = await creator.create_full_campaign(
            advertiser_id=advertiser_id,
            campaign_name=campaign_name,
            daily_budget=daily_budget,
            video_id=video_id,
            landing_page_url=landing_page_url,
            targeting=targeting,
            ad_text=ad_text,
        )
        
        await client.close()
        
        if result["status"] == "success":
            return {
                "status": "success",
                "data": result,
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error"))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create full campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/video/upload")
async def upload_video_creative(
    advertiser_id: str = Form(...),
    file: UploadFile = File(...),
    video_name: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    """
    上传视频创意
    
    参数：
    - advertiser_id: 广告账户ID
    - file: 视频文件
    - video_name: 视频名称
    
    返回：
    {
        "video_id": "...",
        "video_name": "...",
        "status": "success"
    }
    """
    # 验证广告主
    result = await db.execute(
        select(Advertiser).where(
            Advertiser.advertiser_id == advertiser_id,
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found or inactive")

    import tempfile
    import os
    
    try:
        # 保存临时文件
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Video saved to temp: {temp_path}")
        
        # 上传到TikTok
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )
        
        upload_result = await client.upload_video(
            file_path=temp_path,
            video_name=video_name,
        )
        
        await client.close()
        
        # 清理临时文件
        os.remove(temp_path)
        
        video_id = upload_result.get("video_id")
        
        return {
            "status": "success",
            "data": {
                "video_id": video_id,
                "video_name": video_name,
            },
        }
    
    except Exception as e:
        logger.error(f"Failed to upload video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image/upload")
async def upload_image_creative(
    advertiser_id: str,
    file: UploadFile = File(...),
    image_name: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    上传图片创意
    
    参数：
    - advertiser_id: 广告账户ID
    - file: 图片文件
    - image_name: 图片名称
    
    返回：
    {
        "image_id": "...",
        "image_name": "...",
        "status": "success"
    }
    """
    # 验证广告主
    result = await db.execute(
        select(Advertiser).where(
            Advertiser.advertiser_id == advertiser_id,
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found or inactive")

    import tempfile
    import os
    
    try:
        # 保存临时文件
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Image saved to temp: {temp_path}")
        
        # 上传到TikTok
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )
        
        upload_result = await client.upload_image(
            file_path=temp_path,
            image_name=image_name,
        )
        
        await client.close()
        
        # 清理临时文件
        os.remove(temp_path)
        
        image_id = upload_result.get("image_id")
        
        return {
            "status": "success",
            "data": {
                "image_id": image_id,
                "image_name": image_name,
            },
        }
    
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gmvmax/campaign/create-full")
async def create_full_gmvmax_campaign(
    advertiser_id: str,
    campaign_name: str,
    daily_budget: float,
    shop_id: str,
    video_id: Optional[str] = None,
    ad_text: Optional[str] = None,
    targeting: Optional[Dict[str, Any]] = None,
    catalog_id: Optional[str] = None,
    roas_goal: Optional[float] = None,
    item_group_ids: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    一键创建完整的GMVMAX广告

    GMVMAX 是 TikTok 的全自动优化模式，特点：
    - 自动选择商品（从TikTok Shop）
    - 自动优化受众
    - 自动调整出价
    - 追求 GMV 最大化

    参数：
    - advertiser_id: 广告账户ID
    - campaign_name: 计划名称
    - daily_budget: 每日预算（USD）
    - shop_id: TikTok Shop ID（GMVMAX必需）
    - video_id: 已上传的视频ID（可选，不传则由系统自动生成）
    - ad_text: 广告文案（可选）
    - targeting: 受众定向（可选，系统会自动扩展）
    - catalog_id: 商品目录ID（可选，不指定则投放全部商品）
    - roas_goal: ROI 目标（可选，如 2.0 表示期望 1:2 回报）
    - item_group_ids: 指定投放的商品ID列表（可选，不传则全部商品）

    返回：Campaign/AdGroup/Ad IDs
    """
    # 验证广告主
    result = await db.execute(
        select(Advertiser).where(
            Advertiser.advertiser_id == advertiser_id,
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found or inactive")

    try:
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )
        creator = GmvmaxCampaignCreator(client, db)
        
        result = await creator.create_full_gmvmax_campaign(
            advertiser_id=advertiser_id,
            campaign_name=campaign_name,
            daily_budget=daily_budget,
            shop_id=shop_id,
            video_id=video_id,
            ad_text=ad_text,
            targeting=targeting,
            catalog_id=catalog_id,
            roas_goal=roas_goal,
            item_group_ids=item_group_ids,
        )
        
        await client.close()
        
        if result["status"] == "success":
            return {
                "status": "success",
                "data": result,
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error"))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create GMVMAX campaign: {e}")
        raise HTTPException(status_code=500, detail=str(e))
