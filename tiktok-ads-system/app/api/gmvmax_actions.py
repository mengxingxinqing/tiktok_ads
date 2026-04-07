"""
GMVMax Action 接口

POST /gmvmax/campaign/status              暂停/启用 Campaign
POST /gmvmax/adgroup/status               暂停/启用广告组（下掉/恢复素材）
POST /gmvmax/adgroup/budget               调整广告组预算（加热 = 提高预算）
POST /gmvmax/upload-and-create            上传视频 + 创建 GMVMax 广告（一键加热新素材）
GET  /gmvmax/campaigns                    获取账户的 GMVMax Campaign 列表
GET  /gmvmax/campaigns/{campaign_id}/adgroups  获取 Campaign 下广告组列表
"""

import os
import tempfile
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.services.tiktok_client import TikTokClient

router = APIRouter(prefix="/gmvmax", tags=["GMVMax Actions"])


# =========== Request Schemas ===========

class CampaignStatusRequest(BaseModel):
    advertiser_id: str
    campaign_id: str
    operation: str  # "ENABLE" | "DISABLE"


class AdgroupStatusRequest(BaseModel):
    advertiser_id: str
    adgroup_id: str
    operation: str  # "ENABLE" | "DISABLE"


class AdgroupBudgetRequest(BaseModel):
    advertiser_id: str
    adgroup_id: str
    daily_budget: float


class CampaignBudgetRequest(BaseModel):
    advertiser_id: str
    campaign_id: str
    budget: float


class CreativeBoostRequest(BaseModel):
    advertiser_id: str
    campaign_id: str
    video_id: str = ""
    item_id: str = ""
    budget: float = 50.0
    duration_days: int = 1


class CreativeManageRequest(BaseModel):
    advertiser_id: str
    campaign_id: str
    action: str  # "REMOVE" | "RESTORE"
    item_ids: Optional[List[str]] = None
    video_ids: Optional[List[str]] = None


# =========== 工具函数 ===========

async def _get_advertiser(advertiser_id: str, db: AsyncSession) -> Advertiser:
    """从 DB 查 advertiser，验证 active + token_valid"""
    result = await db.execute(
        select(Advertiser).where(
            Advertiser.advertiser_id == advertiser_id,
            Advertiser.is_active == True,
            Advertiser.is_token_valid == True,
        )
    )
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail=f"Advertiser {advertiser_id} not found or inactive")
    return advertiser


# =========== 端点 ===========

@router.post("/campaign/status")
async def update_campaign_status(
    body: CampaignStatusRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    暂停/启用 GMVMax Campaign

    body:
    - advertiser_id: 广告账户 ID
    - campaign_id: Campaign ID
    - operation: "ENABLE" | "DISABLE"
    """
    operation = body.operation.upper()
    if operation not in ("ENABLE", "DISABLE"):
        raise HTTPException(status_code=400, detail="operation must be ENABLE or DISABLE")

    advertiser = await _get_advertiser(body.advertiser_id, db)
    try:
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=body.advertiser_id,
        )
        result = await client.update_campaign_status(
            campaign_ids=[body.campaign_id],
            operation_status=operation,
        )
        await client.close()

        return {
            "status": "success",
            "campaign_id": body.campaign_id,
            "operation": operation,
            "data": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"update_campaign_status failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/campaign/budget")
async def update_campaign_budget(
    body: CampaignBudgetRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    调整 GMVMax Campaign 日预算（加热 = 提高预算）
    """
    advertiser = await _get_advertiser(body.advertiser_id, db)
    client = TikTokClient(access_token=advertiser.access_token, advertiser_id=body.advertiser_id)
    try:
        result = await client._request("POST", "/open_api/v1.3/campaign/update/", json={
            "advertiser_id": body.advertiser_id,
            "campaign_id": body.campaign_id,
            "budget": body.budget,
            "budget_mode": "BUDGET_MODE_DAY",
        })
        await client.close()
        return {
            "success": True,
            "campaign_id": body.campaign_id,
            "new_budget": body.budget,
            "result": result,
        }
    except TikTokAPIError as e:
        await client.close()
        raise HTTPException(status_code=400, detail=f"TikTok API Error [{e.code}]: {e.message}")
    except Exception as e:
        await client.close()
        logger.error(f"update_campaign_budget failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/creative-boost/create")
async def create_creative_boost(
    body: CreativeBoostRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    给单个素材/视频创建加热会话（Creative Boost Session）。

    GMVMax 专属功能：为指定视频分配额外预算，增加曝光。
    - 最低预算 $50
    - 单个 Campaign 内最多 200 个视频的加热会话
    - 同一视频同一时间段不能有重叠的加热会话
    """
    from datetime import datetime, timedelta

    advertiser = await _get_advertiser(body.advertiser_id, db)
    client = TikTokClient(access_token=advertiser.access_token, advertiser_id=body.advertiser_id)
    try:
        # 计算加热时间范围
        now = datetime.utcnow()
        start_time = now.strftime("%Y-%m-%d %H:%M:%S")
        end_time = (now + timedelta(days=body.duration_days)).strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "advertiser_id": body.advertiser_id,
            "campaign_id": body.campaign_id,
            "promote_type": "creative_boost",
            "budget": max(body.budget, 50.0),  # 最低 $50
            "start_time": start_time,
            "end_time": end_time,
        }
        # video_id 或 item_id 至少传一个
        if body.video_id:
            payload["video_id"] = body.video_id
        if body.item_id:
            payload["item_id"] = body.item_id

        result = await client._request(
            "POST",
            "/open_api/v1.3/gmv_max/campaign/max_session/create/",
            json=payload,
        )
        return {
            "success": True,
            "campaign_id": body.campaign_id,
            "budget": body.budget,
            "duration_days": body.duration_days,
            "start_time": start_time,
            "end_time": end_time,
            "session": result,
        }
    except TikTokAPIError as e:
        raise HTTPException(status_code=400, detail=f"TikTok API Error [{e.code}]: {e.message}")
    except Exception as e:
        logger.error(f"create_creative_boost failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/creative-boost/list")
async def list_creative_boosts(
    advertiser_id: str,
    campaign_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取 Campaign 下所有活跃的加热会话"""
    advertiser = await _get_advertiser(advertiser_id, db)
    client = TikTokClient(access_token=advertiser.access_token, advertiser_id=advertiser_id)
    try:
        result = await client._request(
            "GET",
            "/open_api/v1.3/gmv_max/campaign/max_session/get/",
            params={"advertiser_id": advertiser_id, "campaign_id": campaign_id},
        )
        return result
    except TikTokAPIError as e:
        raise HTTPException(status_code=400, detail=f"TikTok API Error [{e.code}]: {e.message}")
    finally:
        await client.close()


@router.post("/adgroup/status")
async def update_adgroup_status(
    body: AdgroupStatusRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    暂停/启用 GMVMax 广告组（等同于下掉/恢复素材）

    body:
    - advertiser_id: 广告账户 ID
    - adgroup_id: 广告组 ID
    - operation: "ENABLE" | "DISABLE"
    """
    operation = body.operation.upper()
    if operation not in ("ENABLE", "DISABLE"):
        raise HTTPException(status_code=400, detail="operation must be ENABLE or DISABLE")

    advertiser = await _get_advertiser(body.advertiser_id, db)
    try:
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=body.advertiser_id,
        )
        result = await client.update_adgroup_status(
            adgroup_ids=[body.adgroup_id],
            operation_status=operation,
        )
        await client.close()

        return {
            "status": "success",
            "adgroup_id": body.adgroup_id,
            "operation": operation,
            "data": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"update_adgroup_status failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adgroup/budget")
async def update_adgroup_budget(
    body: AdgroupBudgetRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    调整 GMVMax 广告组日预算（加热 = 提高预算，降温 = 降低预算）

    body:
    - advertiser_id: 广告账户 ID
    - adgroup_id: 广告组 ID
    - daily_budget: 新的日预算（USD，浮点数）
    """
    if body.daily_budget <= 0:
        raise HTTPException(status_code=400, detail="daily_budget must be positive")

    advertiser = await _get_advertiser(body.advertiser_id, db)
    try:
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=body.advertiser_id,
        )
        result = await client.update_gmvmax_adgroup_budget(
            adgroup_id=body.adgroup_id,
            budget=body.daily_budget,
        )
        await client.close()

        return {
            "status": "success",
            "adgroup_id": body.adgroup_id,
            "daily_budget": body.daily_budget,
            "data": result,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"update_adgroup_budget failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-and-create")
async def upload_and_create_gmvmax_ad(
    video_file: UploadFile = File(...),
    advertiser_id: str = Form(...),
    campaign_id: str = Form(...),
    ad_name: str = Form(...),
    ad_text: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """
    上传视频 + 在已有 GMVMax Campaign 下创建广告（一键加热新素材）

    body (multipart/form-data):
    - video_file: 视频文件
    - advertiser_id: 广告账户 ID
    - campaign_id: 已有 GMVMax Campaign ID（直接往里加广告组+广告）
    - ad_name: 广告名称
    - ad_text: 广告文案（可选）

    流程：
    1. 上传视频 → 获取 video_id
    2. 在 campaign_id 下创建广告组（GMVMax 模式）
    3. 在广告组下创建广告，使用上传的 video_id
    """
    advertiser = await _get_advertiser(advertiser_id, db)

    temp_path = None
    try:
        # 1. 保存临时文件
        temp_dir = tempfile.gettempdir()
        safe_filename = video_file.filename or "upload.mp4"
        temp_path = os.path.join(temp_dir, f"gmvmax_{advertiser_id}_{safe_filename}")
        content = await video_file.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        logger.info(f"Video saved to temp: {temp_path}")

        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )

        # 2. 上传视频到 TikTok
        video_name = os.path.splitext(safe_filename)[0]
        upload_result = await client.upload_video(
            file_path=temp_path,
            video_name=video_name,
        )
        video_id = upload_result.get("video_id")
        if not video_id:
            raise ValueError(f"Video upload failed, no video_id returned: {upload_result}")
        logger.info(f"Video uploaded, video_id={video_id}")

        # 3. 获取 Campaign 信息（用于确认 shop_id 等参数）
        from app.services.ads_campaign_creator import GmvmaxCampaignCreator
        creator = GmvmaxCampaignCreator(client, db)

        # 直接在指定 campaign 下创建广告组 + 广告
        # 先获取该 campaign 信息
        import json
        campaign_result = await client._request(
            "GET",
            "/open_api/v1.3/campaign/get/",
            params={
                "advertiser_id": advertiser_id,
                "filtering": json.dumps({"campaign_ids": [campaign_id]}),
                "fields": json.dumps(["campaign_id", "campaign_name", "objective_type", "budget", "budget_mode"]),
            },
        )
        campaign_list = campaign_result.get("data", {}).get("list", [])
        if not campaign_list:
            raise HTTPException(status_code=404, detail=f"Campaign {campaign_id} not found")
        campaign_info = campaign_list[0]

        # 创建广告组（GMVMax）
        adgroup_result = await client.create_gmvmax_adgroup(
            campaign_id=campaign_id,
            adgroup_name=f"{ad_name}_adgroup",
            budget=campaign_info.get("budget", 50.0),
        )
        adgroup_id = adgroup_result.get("adgroup_id")
        if not adgroup_id:
            raise ValueError(f"AdGroup creation failed: {adgroup_result}")
        logger.info(f"AdGroup created, adgroup_id={adgroup_id}")

        # 创建广告（GMVMax）
        ad_result = await client.create_gmvmax_ad(
            adgroup_id=adgroup_id,
            ad_name=ad_name,
            video_id=video_id,
            ad_text=ad_text,
        )
        ad_id = ad_result.get("ad_id")
        logger.info(f"Ad created, ad_id={ad_id}")

        await client.close()

        return {
            "status": "success",
            "data": {
                "video_id": video_id,
                "campaign_id": campaign_id,
                "adgroup_id": adgroup_id,
                "ad_id": ad_id,
                "ad_name": ad_name,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"upload_and_create_gmvmax_ad failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


class ExcludeCreativeRequest(BaseModel):
    advertiser_id: str
    campaign_id: str
    item_id: str  # 要排除的创意 item_id


@router.post("/creative/exclude")
async def exclude_creative(
    body: ExcludeCreativeRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    从 GMVMax Campaign 中排除（下掉）指定创意

    流程：
    1. 获取该 campaign 当前所有创意
    2. 从列表中移除目标 item_id
    3. 用 campaign/gmv_max/update 提交更新后的 item_list

    body:
    - advertiser_id: 广告账户 ID
    - campaign_id: Campaign ID
    - item_id: 要排除的创意 item_id
    """
    advertiser = await _get_advertiser(body.advertiser_id, db)

    # 获取 store 信息
    from app.models.store import Store
    store_result = await db.execute(
        select(Store).where(Store.advertiser_id == body.advertiser_id, Store.is_active == True)
    )
    store = store_result.scalar_one_or_none()
    if not store or not store.store_authorized_bc_id:
        raise HTTPException(status_code=400, detail="未找到关联店铺或缺少 BC 授权信息")

    client = TikTokClient(
        access_token=advertiser.access_token,
        advertiser_id=body.advertiser_id,
    )
    try:
        result = await client.exclude_gmvmax_creative(
            campaign_id=body.campaign_id,
            exclude_item_id=body.item_id,
            store_id=store.store_id,
            store_authorized_bc_id=store.store_authorized_bc_id,
        )
        return {
            "status": "success",
            "message": f"创意 {body.item_id} 已从 Campaign {body.campaign_id} 中排除",
            **result,
        }
    except Exception as e:
        logger.error(f"exclude_creative failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/campaigns")
async def list_gmvmax_campaigns(
    advertiser_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    获取账户下的 GMVMax Campaign 列表（含状态）

    query params:
    - advertiser_id: 广告账户 ID
    """
    advertiser = await _get_advertiser(advertiser_id, db)
    try:
        import json
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )

        # 拉取所有 campaign，过滤 objective_type=SHOP_PURCHASES（GMVMax）
        result = await client._request(
            "GET",
            "/open_api/v1.3/campaign/get/",
            params={
                "advertiser_id": advertiser_id,
                "filtering": json.dumps({"objective_type": "SHOP_PURCHASES"}),
                "fields": json.dumps([
                    "campaign_id", "campaign_name", "operation_status",
                    "secondary_status", "budget", "budget_mode",
                    "objective_type", "create_time",
                ]),
                "page_size": 100,
            },
        )
        await client.close()

        campaigns = result.get("data", {}).get("list", [])
        return {
            "status": "success",
            "advertiser_id": advertiser_id,
            "total": len(campaigns),
            "campaigns": campaigns,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"list_gmvmax_campaigns failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campaigns/{campaign_id}/adgroups")
async def list_campaign_adgroups(
    campaign_id: str,
    advertiser_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    获取 GMVMax Campaign 下的广告组列表

    path params:
    - campaign_id: Campaign ID

    query params:
    - advertiser_id: 广告账户 ID
    """
    advertiser = await _get_advertiser(advertiser_id, db)
    try:
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser_id,
        )
        adgroups = await client.get_gmvmax_adgroup_list(campaign_id=campaign_id)
        await client.close()

        return {
            "status": "success",
            "advertiser_id": advertiser_id,
            "campaign_id": campaign_id,
            "total": len(adgroups),
            "adgroups": adgroups,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"list_campaign_adgroups failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 视频创意管理流程 ====================


@router.get("/identities")
async def list_identities(
    advertiser_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    获取可用的达人身份列表（Identity）
    包含 GMVMax 专用身份 + 标准身份
    """
    advertiser = await _get_advertiser(advertiser_id, db)
    client = TikTokClient(access_token=advertiser.access_token, advertiser_id=advertiser_id)
    try:
        # 1. 从 Store 获取 GMVMax identities
        from app.models.store import Store
        store_result = await db.execute(
            select(Store).where(Store.advertiser_id == advertiser_id, Store.is_active == True)
        )
        store = store_result.scalar_one_or_none()

        gmvmax_ids = []
        if store:
            try:
                gmvmax_ids = await client.get_gmvmax_identities(
                    store_id=store.store_id,
                    store_authorized_bc_id=store.store_authorized_bc_id,
                )
            except Exception:
                pass

        # 2. 标准 identity 列表
        standard_ids = []
        try:
            data = await client._request("GET", "/open_api/v1.3/identity/get/", params={
                "advertiser_id": advertiser_id, "page": 1, "page_size": 100,
            })
            standard_ids = data.get("list", [])
        except Exception:
            pass

        return {
            "advertiser_id": advertiser_id,
            "store_id": store.store_id if store else None,
            "gmvmax_identities": gmvmax_ids,
            "standard_identities": standard_ids,
            "total": len(gmvmax_ids) + len(standard_ids),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"list_identities failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.post("/video/upload")
async def upload_video(
    advertiser_id: str = "",
    video_file: bytes = None,
    db: AsyncSession = Depends(get_db),
):
    """
    上传视频到广告账户素材库
    GMVMax 会自动将素材库中的视频纳入投放
    """
    from fastapi import UploadFile, File, Form

    # 这个接口通过 /ads/video/upload 已有，这里提供 GMVMax 专用的包装
    # 直接转发到已有的上传接口
    raise HTTPException(status_code=307, headers={"Location": "/ads/video/upload"})


@router.get("/video/status")
async def check_video_status(
    advertiser_id: str,
    video_ids: str,  # 逗号分隔的 video_id 列表
    db: AsyncSession = Depends(get_db),
):
    """
    查询视频审核状态
    返回每个视频的审核进度、封面图、预览URL等信息
    """
    advertiser = await _get_advertiser(advertiser_id, db)
    client = TikTokClient(access_token=advertiser.access_token, advertiser_id=advertiser_id)
    try:
        ids = [v.strip() for v in video_ids.split(",") if v.strip()]
        if not ids:
            return {"videos": []}

        videos = await client.get_video_info(ids)
        return {
            "advertiser_id": advertiser_id,
            "total": len(videos),
            "videos": [
                {
                    "video_id": v.get("video_id", ""),
                    "file_name": v.get("file_name", ""),
                    "duration": v.get("duration"),
                    "width": v.get("width"),
                    "height": v.get("height"),
                    "preview_url": v.get("preview_url", ""),
                    "cover_url": v.get("video_cover_url", ""),
                    "material_id": v.get("material_id", ""),
                    "create_time": v.get("create_time", ""),
                    "modify_time": v.get("modify_time", ""),
                }
                for v in videos
            ],
        }
    except TikTokAPIError as e:
        raise HTTPException(status_code=400, detail=f"TikTok API Error [{e.code}]: {e.message}")
    finally:
        await client.close()


@router.get("/creative/posts")
async def list_campaign_posts(
    advertiser_id: str,
    campaign_id: str = "",
    db: AsyncSession = Depends(get_db),
):
    """
    获取 GMVMax Campaign 可用的帖子/创意列表
    从 TikTok oEmbed 补充缩略图和标题
    """
    from app.models.store import Store

    advertiser = await _get_advertiser(advertiser_id, db)
    client = TikTokClient(access_token=advertiser.access_token, advertiser_id=advertiser_id)

    store_result = await db.execute(
        select(Store).where(Store.advertiser_id == advertiser_id, Store.is_active == True)
    )
    store = store_result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="No store found for this advertiser")

    try:
        # 尝试 GMVMax creative post API
        posts = []
        try:
            data = await client._request("GET", "/open_api/v1.3/gmv_max/creative/post/get/", params={
                "advertiser_id": advertiser_id,
                "shop_id": store.store_id,
                "store_authorized_bc_id": store.store_authorized_bc_id,
                "page_size": 50,
            })
            posts = data.get("post_list", data.get("list", []))
        except Exception:
            pass

        # 如果 API 不返回，从数据库 creative_view 获取 item_ids
        if not posts:
            from app.models.views import CreativeView
            query = select(CreativeView).where(CreativeView.advertiser_id == advertiser_id)
            if campaign_id:
                query = query.where(CreativeView.campaign_id == campaign_id)
            result = await db.execute(query.order_by(CreativeView.total_spend.desc()))
            rows = result.scalars().all()

            # 用 oEmbed 补充信息
            import httpx as _httpx
            async with _httpx.AsyncClient(timeout=8.0) as hc:
                for r in rows[:50]:
                    if r.item_id and r.item_id != "-1" and not r.is_auto_selected:
                        post = {
                            "item_id": r.item_id,
                            "product_name": r.product_name or "",
                            "image_url": r.product_image_url or "",
                            "campaign_id": r.campaign_id or "",
                            "total_spend": r.total_spend or 0,
                            "total_orders": r.total_orders or 0,
                            "stage": r.stage or "",
                        }
                        # oEmbed
                        try:
                            resp = await hc.get("https://www.tiktok.com/oembed", params={
                                "url": f"https://www.tiktok.com/video/{r.item_id}"
                            })
                            if resp.status_code == 200:
                                oe = resp.json()
                                import re
                                html = oe.get("html", "")
                                cite = re.search(r'cite="(https://www\.tiktok\.com/@[^"]+)"', html)
                                post["tiktok_url"] = cite.group(1) if cite else ""
                                post["thumbnail_url"] = oe.get("thumbnail_url", "")
                                post["title"] = oe.get("title", "")
                                post["author"] = oe.get("author_name", "")
                        except Exception:
                            pass
                        posts.append(post)

        return {
            "advertiser_id": advertiser_id,
            "campaign_id": campaign_id,
            "store_id": store.store_id,
            "total": len(posts),
            "posts": posts,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"list_campaign_posts failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.post("/creative/manage")
async def manage_creatives(
    body: CreativeManageRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    管理 GMVMax Campaign 中的创意（排除/恢复视频）

    action: REMOVE（排除，不再投放） | RESTORE（恢复投放）
    item_ids: TikTok 帖子 ID 列表
    video_ids: 视频 ID 列表
    每次最多 400 个
    """
    if body.action not in ("REMOVE", "RESTORE"):
        raise HTTPException(status_code=400, detail="action must be REMOVE or RESTORE")
    if not body.item_ids and not body.video_ids:
        raise HTTPException(status_code=400, detail="item_ids or video_ids required")

    advertiser = await _get_advertiser(body.advertiser_id, db)
    client = TikTokClient(access_token=advertiser.access_token, advertiser_id=body.advertiser_id)
    try:
        payload = {
            "advertiser_id": body.advertiser_id,
            "campaign_id": body.campaign_id,
            "shopping_ads_type": "PRODUCT",
            "action": body.action,
        }
        if body.item_ids:
            payload["item_ids"] = body.item_ids[:400]
        if body.video_ids:
            payload["video_ids"] = body.video_ids[:400]

        result = await client._request(
            "POST",
            "/open_api/v1.3/gmv_max/creative/manage/",
            json=payload,
        )
        return {
            "success": True,
            "action": body.action,
            "campaign_id": body.campaign_id,
            "count": len(body.item_ids or []) + len(body.video_ids or []),
            "result": result,
        }
    except TikTokAPIError as e:
        raise HTTPException(status_code=400, detail=f"TikTok API Error [{e.code}]: {e.message}")
    except Exception as e:
        logger.error(f"manage_creatives failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()
