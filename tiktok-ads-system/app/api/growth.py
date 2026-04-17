"""
智能涨粉模块 API

模块职责：
- TK 账号管理（录入、列表、目标设定）
- 素材库管理（上传、列表、万粉成本）
- 涨粉 Campaign 管理（创建、启动、停止）
- Ad Account 管理（列表、汇率）
"""
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Optional, List
from urllib.parse import quote
import uuid
import asyncio
import json
import logging

from loguru import logger
from app.services.tiktok_client import TikTokClient, TikTokAPIError

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.models.ad_account import AdAccount
from app.models.tk_account import TkAccount
from app.models.creative_material import CreativeMaterial
from app.models.growth_campaign import GrowthCampaign
from app.models.exchange_rate import ExchangeRate
from app.services.budget_calculator import BudgetCalculator
from app.services.follower_scraper import TikTokFollowerScraper
from app.services.ad_account_sync import AdAccountSyncService
from app.services.growth_notifier import GrowthFeishuNotifier
from app.services.growth_campaign_creator import GrowthCampaignCreator
from app.services import currency as fx
from app.core.config import settings

router = APIRouter(prefix="/api/growth", tags=["智能涨粉"])


# =========================== 独立 OAuth 授权（不写 advertisers 表） ===========================

@router.get("/auth/login")
async def growth_auth_url(remark: Optional[str] = Query(None, description="备注，作为 state 前缀后缀")):
    """
    生成涨粉模块专属的 TikTok OAuth 授权 URL。
    state 前缀 "growth_" 用于回调分流：/auth/callback 识别后只写 ad_accounts，不写 advertisers。
    """
    suffix = remark or str(int(datetime.now().timestamp()))
    state = f"growth_{suffix}"
    encoded_redirect_uri = quote(settings.TIKTOK_REDIRECT_URI, safe="")
    auth_url = (
        f"https://business-api.tiktok.com/portal/auth"
        f"?app_id={settings.TIKTOK_APP_ID}"
        f"&state={state}"
        f"&redirect_uri={encoded_redirect_uri}"
    )
    return {
        "auth_url": auth_url,
        "state": state,
        "note": "跳转后 TikTok 会回调到 /auth/callback，回调识别 state=growth_* 写入 ad_accounts，不影响 gmvmax 的 advertisers",
    }


async def handle_growth_oauth_callback(
    db: AsyncSession,
    token_code: str,
    state: Optional[str],
) -> dict:
    """
    涨粉模块专属回调处理：
    - 换 token
    - 拉 advertiser_list
    - 只写 ad_accounts 表，第一个账户标记为 BC 代表（token_owner_advertiser_id = 自己）
    - 其它账户 token_owner_advertiser_id 指向代表，共享同一 token + refresh
    """
    from loguru import logger as _log

    token_data = await TikTokClient.exchange_token(token_code)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in") or 0
    if not access_token:
        raise HTTPException(400, "No access_token in TikTok response")
    token_expire_at = (
        datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
        if expires_in else None
    )

    advertiser_list = await TikTokClient.get_advertiser_list(access_token)
    if not advertiser_list:
        raise HTTPException(400, "No advertiser accounts under this authorization")

    # 第一个 advertiser 作为 BC 代表户
    owner_id = str(advertiser_list[0]["advertiser_id"])

    svc = AdAccountSyncService(db=db)
    sync_result = await svc.sync_all_from_bc(
        access_token=access_token,
        refresh_token=refresh_token,
        token_expire_at=token_expire_at,
        owner_advertiser_id=owner_id,
    )
    # BC 代表户的 token_owner_advertiser_id = 自己（表示"这一行的 token 就是从自己授权拿到的"）
    owner_result = await db.execute(select(AdAccount).where(AdAccount.advertiser_id == owner_id))
    owner = owner_result.scalar_one_or_none()
    if owner:
        owner.token_owner_advertiser_id = owner_id
        await db.commit()

    _log.info(
        f"[GrowthOAuth] state={state} owner={owner_id} result={sync_result}"
    )
    return {"owner_advertiser_id": owner_id, **sync_result}


# =========================== TK 账号 ===========================

@router.post("/tk-accounts")
async def create_tk_account(
    account_id: str,
    account_name: Optional[str] = None,
    profile_url: Optional[str] = None,
    target_follower_count: int = 10000,
    target_cost_per_10k: float = 35.0,
    db: AsyncSession = Depends(get_db),
):
    """录入 TK 账号"""
    # 检查是否已存在
    exist = await db.execute(select(TkAccount).where(TkAccount.account_id == account_id))
    if exist.scalar_one_or_none():
        raise HTTPException(400, f"TK账号 {account_id} 已存在")

    # 补全 profile_url
    if not profile_url:
        profile_url = f"https://www.tiktok.com/@{account_id.lstrip('@')}"

    tk = TkAccount(
        account_id=account_id.lstrip("@"),
        account_name=account_name or account_id,
        profile_url=profile_url,
        target_follower_count=target_follower_count,
        target_cost_per_10k=Decimal(str(target_cost_per_10k)),
        status="IDLE",
    )
    db.add(tk)
    await db.commit()
    return {"id": tk.id, "account_id": tk.account_id, "status": "IDLE"}


@router.get("/tk-accounts")
async def list_tk_accounts(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """TK 账号列表"""
    query = select(TkAccount)
    if status:
        query = query.where(TkAccount.status == status)
    query = query.order_by(TkAccount.created_at.desc())
    result = await db.execute(query)
    accounts = result.scalars().all()
    return {
        "total": len(accounts),
        "accounts": [
            {
                "id": a.id,
                "account_id": a.account_id,
                "account_name": a.account_name,
                "profile_url": a.profile_url,
                "follower_count": a.follower_count,
                "target_follower_count": a.target_follower_count,
                "target_cost_per_10k": float(a.target_cost_per_10k or 35),
                "status": a.status,
                "bound_ad_account_id": a.bound_ad_account_id,
                "bound_video_id": a.bound_video_id,
                "follower_updated_at": a.follower_updated_at,
            }
            for a in accounts
        ],
    }


@router.post("/tk-accounts/{account_id}/refresh-followers")
async def refresh_tk_followers(
    account_id: str,
    db: AsyncSession = Depends(get_db),
):
    """手动刷新 TK 账号粉丝数"""
    result = await db.execute(select(TkAccount).where(TkAccount.account_id == account_id))
    tk = result.scalar_one_or_none()
    if not tk:
        raise HTTPException(404, f"TK账号 {account_id} 不存在")

    scraper = TikTokFollowerScraper()
    count = await asyncio.to_thread(scraper.get_follower_count, tk.account_id)
    if count is not None:
        tk.follower_count = count
        tk.follower_updated_at = datetime.now(timezone.utc)
        await db.commit()
        return {"account_id": account_id, "follower_count": count, "source": "scraper"}
    else:
        return {"account_id": account_id, "follower_count": None, "source": "failed"}


@router.patch("/tk-accounts/{account_id}")
async def update_tk_account(
    account_id: str,
    target_follower_count: Optional[int] = None,
    target_cost_per_10k: Optional[float] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """更新 TK 账号信息"""
    result = await db.execute(select(TkAccount).where(TkAccount.account_id == account_id))
    tk = result.scalar_one_or_none()
    if not tk:
        raise HTTPException(404, f"TK账号 {account_id} 不存在")

    if target_follower_count is not None:
        tk.target_follower_count = target_follower_count
    if target_cost_per_10k is not None:
        tk.target_cost_per_10k = Decimal(str(target_cost_per_10k))
    if status is not None:
        tk.status = status
    await db.commit()
    return {"account_id": account_id, "updated": True}


# =========================== 素材库 ===========================

@router.post("/creatives")
async def create_creative_material(
    video_id: str,
    advertiser_id: Optional[str] = None,
    video_url: Optional[str] = None,
    cover_url: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    添加素材到素材库（手动登记，不走 Spark Ads 授权）
    推荐使用 /creatives/bind-auth-code 走正规 Spark Ads 绑定流程
    """
    if advertiser_id:
        exist = await db.execute(
            select(CreativeMaterial).where(
                CreativeMaterial.video_id == video_id,
                CreativeMaterial.advertiser_id == advertiser_id,
            )
        )
    else:
        exist = await db.execute(
            select(CreativeMaterial).where(
                CreativeMaterial.video_id == video_id,
                CreativeMaterial.advertiser_id.is_(None),
            )
        )
    if exist.scalar_one_or_none():
        raise HTTPException(400, f"素材 {video_id} (advertiser={advertiser_id}) 已存在")

    cm = CreativeMaterial(
        video_id=video_id,
        advertiser_id=advertiser_id,
        video_url=video_url,
        cover_url=cover_url,
    )
    db.add(cm)
    await db.commit()
    return {"video_id": video_id, "id": cm.id}


@router.post("/creatives/bind-auth-code")
async def bind_auth_code(
    advertiser_id: str,
    auth_code: str,
    tk_account_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Spark Ads 核心入口：
    创作者在 TikTok App 里给一条视频生成 auth_code →
    本接口把它绑定到某广告户，并建立一条 CreativeMaterial（含 identity_id + item_id）
    """
    ad_result = await db.execute(select(AdAccount).where(AdAccount.advertiser_id == advertiser_id))
    ad_account = ad_result.scalar_one_or_none()
    if not ad_account:
        raise HTTPException(404, f"AdAccount {advertiser_id} 不存在")

    client = TikTokClient(access_token=ad_account.access_token, advertiser_id=advertiser_id)
    creator = GrowthCampaignCreator(client=client, db=db)
    try:
        info = await creator.bind_auth_code(auth_code=auth_code)
    except TikTokAPIError as e:
        raise HTTPException(400, f"TikTok 授权失败：{e.message}")
    finally:
        await client.close()

    # 查重：同一 (advertiser, item_id) 已绑定则更新
    existing_q = await db.execute(
        select(CreativeMaterial).where(
            CreativeMaterial.advertiser_id == advertiser_id,
            CreativeMaterial.item_id == info["item_id"],
        )
    )
    existing = existing_q.scalar_one_or_none()
    if existing:
        existing.auth_code = auth_code
        existing.identity_id = info["identity_id"]
        existing.identity_type = info["identity_type"]
        existing.ad_auth_status = info["ad_auth_status"]
        existing.video_url = info.get("preview_url")
        existing.cover_url = info.get("poster_url")
        existing.duration = Decimal(str(info["duration"])) if info.get("duration") else None
        if tk_account_id:
            existing.bound_tk_account_id = tk_account_id
        await db.commit()
        return {"id": existing.id, "item_id": existing.item_id, "updated": True}

    cm = CreativeMaterial(
        advertiser_id=advertiser_id,
        video_id=info["item_id"],     # 以 item_id 作为 video_id 对外暴露
        auth_code=auth_code,
        item_id=info["item_id"],
        identity_id=info["identity_id"],
        identity_type=info["identity_type"],
        ad_auth_status=info["ad_auth_status"],
        video_url=info.get("preview_url"),
        cover_url=info.get("poster_url"),
        duration=Decimal(str(info["duration"])) if info.get("duration") else None,
        bound_tk_account_id=tk_account_id,
    )
    db.add(cm)
    await db.commit()
    return {"id": cm.id, "item_id": cm.item_id, "identity_id": cm.identity_id, "created": True}


@router.get("/creatives")
async def list_creative_materials(
    advertiser_id: Optional[str] = None,
    authorized_only: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """素材库列表（按万粉成本排序）

    - advertiser_id：过滤绑定到该广告户的素材（创建 Campaign 时选素材用）
    - authorized_only：只返回 ad_auth_status == AUTHORIZED
    """
    query = select(CreativeMaterial)
    if advertiser_id:
        query = query.where(CreativeMaterial.advertiser_id == advertiser_id)
    if authorized_only:
        query = query.where(CreativeMaterial.ad_auth_status == "AUTHORIZED")
    # 排序：有样本的优先（按 avg_cost_per_10k 升序），无样本的按创建时间
    query = query.order_by(
        CreativeMaterial.avg_cost_per_10k.asc().nullslast(),
        CreativeMaterial.sample_count.desc(),
        CreativeMaterial.created_at.desc(),
    )
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    materials = result.scalars().all()

    # 总数（按同样过滤条件）
    count_q = select(func.count()).select_from(CreativeMaterial)
    if advertiser_id:
        count_q = count_q.where(CreativeMaterial.advertiser_id == advertiser_id)
    if authorized_only:
        count_q = count_q.where(CreativeMaterial.ad_auth_status == "AUTHORIZED")
    count_result = await db.execute(count_q)
    total = count_result.scalar()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "materials": [
            {
                "id": m.id,
                "video_id": m.video_id,
                "advertiser_id": m.advertiser_id,
                "item_id": m.item_id,
                "identity_id": m.identity_id,
                "identity_type": m.identity_type,
                "ad_auth_status": m.ad_auth_status,
                "bound_tk_account_id": m.bound_tk_account_id,
                "video_url": m.video_url,
                "cover_url": m.cover_url,
                "duration": float(m.duration) if m.duration else None,
                "sample_count": m.sample_count or 0,
                "avg_cost_per_10k": float(m.avg_cost_per_10k) if m.avg_cost_per_10k else None,
                "latest_cost_per_10k": float(m.latest_cost_per_10k) if m.latest_cost_per_10k else None,
                "total_spend": float(m.total_spend) if m.total_spend else 0,
                "total_followers_gained": m.total_followers_gained or 0,
            }
            for m in materials
        ],
    }


# =========================== Campaign ===========================

class CampaignAssignment(BaseModel):
    tk_account_id: str
    material_id: Optional[int] = None   # CreativeMaterial.id；缺省则按推荐规则挑


class CreateCampaignsBody(BaseModel):
    assignments: List[CampaignAssignment]
    ad_account_id: Optional[str] = None
    target_cost_per_10k: float = 35.0


@router.post("/campaigns")
async def create_growth_campaign(
    body: CreateCampaignsBody,
    db: AsyncSession = Depends(get_db),
):
    """
    创建涨粉 Campaign（Phase 1 手动选材模式）

    入参：
      assignments: [{ tk_account_id, material_id? }]
        - material_id 必须是已绑定到 ad_account 且 AUTHORIZED 的素材
        - 缺省则按"该广告户下 avg_cost 最低 + 样本 n>=3 的素材"推荐
      ad_account_id: 所有 Campaign 使用的广告户；缺省则按优先级+USD余额自动分配
      target_cost_per_10k: 目标单粉成本 USD
    """
    created = []
    errors = []

    for assignment in body.assignments:
        account_id = assignment.tk_account_id
        # 检查 TK 账号
        result = await db.execute(select(TkAccount).where(TkAccount.account_id == account_id))
        tk = result.scalar_one_or_none()
        if not tk:
            errors.append({"account_id": account_id, "error": "账号不存在"})
            continue
        if tk.status != "IDLE":
            errors.append({"account_id": account_id, "error": f"状态为 {tk.status}，非 IDLE"})
            continue

        # 分配 AdAccount
        if body.ad_account_id:
            ad_result = await db.execute(select(AdAccount).where(AdAccount.advertiser_id == body.ad_account_id))
            ad_account = ad_result.scalar_one_or_none()
        else:
            ad_result = await db.execute(
                select(AdAccount)
                .where(AdAccount.is_active == True, AdAccount.allow_use == True)
                .order_by(AdAccount.priority.asc(), AdAccount.balance_usd.desc().nullslast())
            )
            candidates = ad_result.scalars().all()
            ad_account = candidates[0] if candidates else None

        if not ad_account:
            errors.append({"account_id": account_id, "error": "无可用 AdAccount"})
            continue

        # 选择素材：手动指定 OR 推荐（avg_cost 最低 + n>=3）
        if assignment.material_id:
            mat_q = await db.execute(
                select(CreativeMaterial).where(
                    CreativeMaterial.id == assignment.material_id,
                    CreativeMaterial.advertiser_id == ad_account.advertiser_id,
                    CreativeMaterial.ad_auth_status == "AUTHORIZED",
                )
            )
            material = mat_q.scalar_one_or_none()
            if not material:
                errors.append({
                    "account_id": account_id,
                    "error": f"素材 id={assignment.material_id} 不存在或未授权到广告户 {ad_account.advertiser_id}",
                })
                continue
        else:
            # B 方案推荐：该广告户下 avg_cost 最低 + sample_count >= 3
            mat_q = await db.execute(
                select(CreativeMaterial)
                .where(
                    CreativeMaterial.advertiser_id == ad_account.advertiser_id,
                    CreativeMaterial.ad_auth_status == "AUTHORIZED",
                    CreativeMaterial.sample_count >= 3,
                )
                .order_by(CreativeMaterial.avg_cost_per_10k.asc().nullslast())
                .limit(1)
            )
            material = mat_q.scalar_one_or_none()
            if not material:
                # 兜底：没样本积累时取任意 AUTHORIZED 素材，但要求前端必须显式选择
                errors.append({
                    "account_id": account_id,
                    "error": f"广告户 {ad_account.advertiser_id} 下无 n>=3 的推荐素材，请在前端为该账号手动选择一条 AUTHORIZED 素材",
                })
                continue

        # 计算预算
        # 取该广告户下素材的加权均值，没有则回退到全局均值，再没有用 target
        all_mats = await db.execute(select(CreativeMaterial).where(CreativeMaterial.avg_cost_per_10k.isnot(None)))
        mats = all_mats.scalars().all()
        if mats:
            total_cost = sum(float(m.avg_cost_per_10k) for m in mats) / len(mats)
        else:
            total_cost = body.target_cost_per_10k

        budget_usd = BudgetCalculator.calculate_budget(
            target_follower_count=tk.target_follower_count,
            current_follower_count=tk.follower_count or 0,
            avg_cost_per_10k=Decimal(str(total_cost)),
        )

        # 余额校验（USD 口径，含已预留）
        available_usd = Decimal(str(ad_account.balance_usd or 0)) - Decimal(str(ad_account.reserved_budget_usd or 0))
        if available_usd < budget_usd:
            errors.append({
                "account_id": account_id,
                "error": f"AdAccount {ad_account.advertiser_id} 可用余额不足: "
                         f"${float(available_usd):.2f} < 预算 ${float(budget_usd):.2f}",
            })
            continue

        # 换算本币预算（TikTok API 只认本币）
        budget_local = await fx.from_usd(db, budget_usd, ad_account.currency)

        # 生成 campaign_id
        campaign_id = f"gc_{uuid.uuid4().hex[:12]}"

        # 目标粉丝增量
        target_followers = max(0, tk.target_follower_count - (tk.follower_count or 0))

        campaign = GrowthCampaign(
            campaign_id=campaign_id,
            tk_account_id=account_id,
            ad_account_id=ad_account.advertiser_id,
            video_id=material.video_id,
            target_followers=target_followers,
            budget=budget_usd,
            budget_local=budget_local,
            budget_currency=ad_account.currency,
            target_cost_per_10k=Decimal(str(body.target_cost_per_10k)),
            status="PENDING",
        )
        db.add(campaign)

        # 预留预算（防止后续并发创建超卖）
        ad_account.reserved_budget_usd = Decimal(str(ad_account.reserved_budget_usd or 0)) + budget_usd

        # 更新 TK 账号绑定
        tk.bound_ad_account_id = ad_account.advertiser_id
        tk.bound_video_id = material.video_id

        created.append({
            "account_id": account_id,
            "campaign_id": campaign_id,
            "budget_usd": float(budget_usd),
            "budget_local": float(budget_local),
            "currency": ad_account.currency,
        })

    await db.commit()
    return {"created": created, "errors": errors}


@router.get("/campaigns")
async def list_growth_campaigns(
    status: Optional[str] = None,
    tk_account_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """涨粉 Campaign 列表"""
    query = select(GrowthCampaign)
    if status:
        query = query.where(GrowthCampaign.status == status)
    if tk_account_id:
        query = query.where(GrowthCampaign.tk_account_id == tk_account_id)
    query = query.order_by(GrowthCampaign.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    campaigns = result.scalars().all()

    count_query = select(func.count()).select_from(GrowthCampaign)
    if status:
        count_query = count_query.where(GrowthCampaign.status == status)
    if tk_account_id:
        count_query = count_query.where(GrowthCampaign.tk_account_id == tk_account_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    return {
        "total": total,
        "campaigns": [
            {
                "campaign_id": c.campaign_id,
                "tk_account_id": c.tk_account_id,
                "ad_account_id": c.ad_account_id,
                "video_id": c.video_id,
                "ad_id": c.ad_id,
                "target_followers": c.target_followers,
                "target_cost_per_10k": float(c.target_cost_per_10k or 35),
                "budget": float(c.budget),
                "budget_local": float(c.budget_local) if c.budget_local else None,
                "budget_currency": c.budget_currency,
                "total_spend": float(c.total_spend or 0),
                "total_spend_local": float(c.total_spend_local or 0),
                "followers_gained": c.followers_gained or 0,
                # 对账后的官方真值（供 dashboard 鉴别）
                "official_followers_gained": c.official_followers_gained,
                "official_spend_usd": float(c.official_spend_usd) if c.official_spend_usd else None,
                "last_reconciled_at": c.last_reconciled_at,
                "status": c.status,
                "start_time": c.start_time,
                "end_time": c.end_time,
                "auto_stop_reason": c.auto_stop_reason,
            }
            for c in campaigns
        ],
    }


@router.post("/campaigns/{campaign_id}/start")
async def start_campaign(
    campaign_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    启动 Campaign（PENDING → RUNNING）
    - 记录 baseline_followers（当前粉丝数快照，用于后续达标判定）
    - 调 TikTok API 创建广告（Spark Ads）
    - 本币预算下发
    """
    result = await db.execute(select(GrowthCampaign).where(GrowthCampaign.campaign_id == campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(404, f"Campaign {campaign_id} 不存在")
    if campaign.status != "PENDING":
        raise HTTPException(400, f"Campaign 状态为 {campaign.status}，无法启动")

    ad_result = await db.execute(select(AdAccount).where(AdAccount.advertiser_id == campaign.ad_account_id))
    ad_account = ad_result.scalar_one_or_none()
    if not ad_account:
        raise HTTPException(500, f"AdAccount {campaign.ad_account_id} 不存在")

    # 取最新粉丝数作为 baseline
    tk_result = await db.execute(select(TkAccount).where(TkAccount.account_id == campaign.tk_account_id))
    tk = tk_result.scalar_one_or_none()
    if not tk:
        raise HTTPException(500, f"TK 账号 {campaign.tk_account_id} 不存在")

    scraper = TikTokFollowerScraper()
    fresh_count = await asyncio.to_thread(scraper.get_follower_count, tk.account_id)
    if fresh_count is None:
        # 爬粉失败也允许启动，使用上一次已知值；完全无数据时拒绝
        if tk.follower_count is None:
            raise HTTPException(400, "无法获取 TK 当前粉丝数，请先刷新 TK 账号")
        baseline = tk.follower_count
    else:
        tk.follower_count = fresh_count
        tk.follower_updated_at = datetime.now(timezone.utc)
        baseline = fresh_count

    campaign.baseline_followers = baseline

    # 本币预算（若创建时未回填）
    if campaign.budget_local is None:
        campaign.budget_local = await fx.from_usd(db, campaign.budget, ad_account.currency)
        campaign.budget_currency = ad_account.currency

    client = TikTokClient(access_token=ad_account.access_token, advertiser_id=campaign.ad_account_id)
    creator = GrowthCampaignCreator(client=client, db=db)

    try:
        tt_result = await creator.create_growth_campaign(
            tk_account=tk,
            ad_account=ad_account,
            video_id=campaign.video_id,
            budget_local=campaign.budget_local,
            target_cost_per_10k=campaign.target_cost_per_10k,
            campaign_name=f"gc_{campaign_id}",
        )

        campaign.tiktok_campaign_id = tt_result.get("tiktok_campaign_id")
        campaign.tiktok_adgroup_id = tt_result.get("tiktok_adgroup_id")
        campaign.tiktok_ad_id = tt_result.get("tiktok_ad_id")
        campaign.ad_id = tt_result.get("tiktok_ad_id")
        campaign.identity_id = tt_result.get("identity_id")
        campaign.identity_type = tt_result.get("identity_type")
        campaign.post_id = tt_result.get("post_id")
        campaign.status = "RUNNING"
        campaign.start_time = datetime.now(timezone.utc)
        # 首次采集调度：启动后 5 分钟就看一次，用于测速
        campaign.next_check_at = campaign.start_time + timedelta(minutes=5)
        campaign.last_check_at = campaign.start_time
        campaign.last_check_followers = baseline

        tk.status = "RUNNING"

        await db.commit()
        return {
            "campaign_id": campaign_id,
            "status": "RUNNING",
            "baseline_followers": baseline,
            "tiktok_ad_id": campaign.ad_id,
        }

    except TikTokAPIError as e:
        logger.error(f"[StartCampaign] TikTok API error: {e}")
        # 释放预算预留
        ad_account.reserved_budget_usd = max(
            Decimal("0"),
            Decimal(str(ad_account.reserved_budget_usd or 0)) - Decimal(str(campaign.budget or 0)),
        )
        campaign.status = "FAILED"
        campaign.auto_stop_reason = f"CREATE_FAILED:{e.code}"
        await db.commit()
        raise HTTPException(500, f"TikTok 广告创建失败：{e.message}")
    finally:
        await client.close()


@router.post("/campaigns/{campaign_id}/stop")
async def stop_campaign(
    campaign_id: str,
    reason: str = "MANUAL",
    db: AsyncSession = Depends(get_db),
):
    """
    停止 Campaign（RUNNING → COMPLETED/PAUSED）
    实际调用 TikTok API 停止广告
    """
    result = await db.execute(select(GrowthCampaign).where(GrowthCampaign.campaign_id == campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(404, f"Campaign {campaign_id} 不存在")
    if campaign.status != "RUNNING":
        raise HTTPException(400, f"Campaign 状态为 {campaign.status}，无法停止")

    # 调用 TikTok API 停止广告
    if campaign.tiktok_campaign_id:
        try:
            ad_result = await db.execute(
                select(AdAccount).where(AdAccount.advertiser_id == campaign.ad_account_id)
            )
            ad_account = ad_result.scalar_one_or_none()
            if ad_account:
                client = TikTokClient(
                    access_token=ad_account.access_token,
                    advertiser_id=campaign.ad_account_id,
                )
                creator = GrowthCampaignCreator(client=client, db=db)
                await creator.stop_ad(campaign.tiktok_campaign_id)
                await client.close()
        except TikTokAPIError as e:
            logger.warning(f"[StopCampaign] Failed to stop TikTok ad: {e}")
            # 不阻断，即使 API 失败也更新本地状态

    # 更新本地状态
    campaign.status = "COMPLETED" if reason == "REACHED_TARGET" else "PAUSED"
    campaign.end_time = datetime.now(timezone.utc)
    campaign.auto_stop_reason = reason

    # 更新 TK 账号状态
    tk_result = await db.execute(select(TkAccount).where(TkAccount.account_id == campaign.tk_account_id))
    tk = tk_result.scalar_one_or_none()
    if tk:
        tk.status = "COMPLETED" if reason == "REACHED_TARGET" else "PAUSED"
        tk.completed_at = datetime.now(timezone.utc)

    await db.commit()
    return {"campaign_id": campaign_id, "status": campaign.status, "reason": reason}


# =========================== Ad Account ===========================

@router.get("/ad-accounts")
async def list_ad_accounts(
    db: AsyncSession = Depends(get_db),
):
    """Ad Account 列表"""
    result = await db.execute(select(AdAccount).order_by(AdAccount.priority.asc()))
    accounts = result.scalars().all()
    return {
        "total": len(accounts),
        "accounts": [
            {
                "advertiser_id": a.advertiser_id,
                "advertiser_name": a.advertiser_name,
                "currency": a.currency,
                "balance": float(a.balance) if a.balance else 0,
                "balance_usd": float(a.balance_usd) if a.balance_usd else None,
                "reserved_budget_usd": float(a.reserved_budget_usd or 0),
                "available_budget_usd": float(
                    (Decimal(str(a.balance_usd or 0)) - Decimal(str(a.reserved_budget_usd or 0)))
                ),
                "is_active": a.is_active,
                "priority": a.priority,
                "allow_use": a.allow_use,
                "token_expire_at": a.token_expire_at,
                "balance_updated_at": a.balance_updated_at,
            }
            for a in accounts
        ],
    }


@router.post("/ad-accounts/sync")
async def sync_ad_accounts(
    bc_advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    从 Business Center 重新同步所有广告账户。
    token 来源是 **涨粉模块自己的 ad_accounts** 表中的 BC 代表行
    （token_owner_advertiser_id == advertiser_id 表示"这一行的 token 就是自己授权拿到的"）。

    与 gmvmax 的 advertisers 表完全隔离：
    - 如果 ad_accounts 为空，提示去 /api/growth/auth/login 走涨粉专属授权
    - 参数 bc_advertiser_id：只用指定 BC 代表户的 token 同步
    """
    query = select(AdAccount).where(
        AdAccount.token_owner_advertiser_id == AdAccount.advertiser_id
    )
    if bc_advertiser_id:
        query = query.where(AdAccount.advertiser_id == bc_advertiser_id)
    result = await db.execute(query)
    owners = result.scalars().all()
    if not owners:
        raise HTTPException(
            400,
            "涨粉模块未完成独立授权。请访问 GET /api/growth/auth/login 获取授权链接。",
        )

    svc = AdAccountSyncService(db=db)
    total = {"created": 0, "updated": 0, "failed": 0}
    for owner in owners:
        sync_result = await svc.sync_all_from_bc(
            access_token=owner.access_token,
            refresh_token=owner.refresh_token,
            token_expire_at=owner.token_expire_at,
            owner_advertiser_id=owner.advertiser_id,
        )
        for k in total:
            total[k] += sync_result.get(k, 0)
    return {"message": "同步完成", **total}


@router.patch("/ad-accounts/{advertiser_id}/priority")
async def update_ad_account_priority(
    advertiser_id: str,
    priority: int = Query(..., ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    """更新 Ad Account 优先级"""
    result = await db.execute(select(AdAccount).where(AdAccount.advertiser_id == advertiser_id))
    acct = result.scalar_one_or_none()
    if not acct:
        raise HTTPException(404, f"AdAccount {advertiser_id} 不存在")
    acct.priority = priority
    await db.commit()
    return {"advertiser_id": advertiser_id, "priority": priority}


@router.patch("/ad-accounts/{advertiser_id}/allow-use")
async def toggle_ad_account_allow_use(
    advertiser_id: str,
    allow_use: bool,
    db: AsyncSession = Depends(get_db),
):
    """启用/禁用 Ad Account"""
    result = await db.execute(select(AdAccount).where(AdAccount.advertiser_id == advertiser_id))
    acct = result.scalar_one_or_none()
    if not acct:
        raise HTTPException(404, f"AdAccount {advertiser_id} 不存在")
    acct.allow_use = allow_use
    await db.commit()
    return {"advertiser_id": advertiser_id, "allow_use": allow_use}


# =========================== 汇率 ===========================

@router.get("/exchange-rates")
async def list_exchange_rates(db: AsyncSession = Depends(get_db)):
    """汇率列表"""
    result = await db.execute(select(ExchangeRate))
    rates = result.scalars().all()
    return {"rates": [{"currency": r.currency_from, "rate": float(r.rate)} for r in rates]}


@router.post("/exchange-rates")
async def upsert_exchange_rate(
    currency: str,
    rate: float,
    db: AsyncSession = Depends(get_db),
):
    """添加/更新汇率（1 <currency> = rate USD）"""
    code = currency.upper()
    result = await db.execute(select(ExchangeRate).where(ExchangeRate.currency_from == code))
    existing = result.scalar_one_or_none()
    if existing:
        existing.rate = Decimal(str(rate))
    else:
        db.add(ExchangeRate(currency_from=code, rate=Decimal(str(rate))))
    await db.commit()
    fx.invalidate_cache()
    return {"currency": code, "rate": rate}
