"""
OAuth 授权相关接口
GET  /auth/login/{state}     → 生成授权 URL，引导广告主跳转
GET  /auth/callback          → TikTok 回调，接收 auth_code，完成 token 换取和存储
GET  /auth/advertisers       → 查看已授权的广告账户列表
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.models.metrics import MetricsSnapshot
from app.models.decision import Decision, DecisionImpact
from app.models.alert import Alert
from app.models.creative import Creative, CreativeSnapshot, CreativeHeatUp
from app.models.creative_group import CreativeGroup, CreativeGroupItem
from app.models.analytics import AccountSnapshot, DailyReport, RiskAlert, HourlyMetrics, GrowthRecommendation
from app.models.product import ProductCost
from app.services.tiktok_client import TikTokClient, TikTokAPIError

router = APIRouter(prefix="/auth", tags=["OAuth"])


@router.get("/login")
async def generate_auth_url(remark: Optional[str] = Query(None, description="备注，会作为 state 传递")):
    """
    生成 TikTok OAuth 授权 URL
    
    授权权限：Business Center（最高权限）
    包含：
    - 广告账户管理
    - 数据访问（报表、指标）
    - 财务权限
    - 店铺管理（关联 TikTok Shop 时）
    
    让广告主访问这个 URL 完成授权
    """
    state = remark or f"auth_{int(datetime.now().timestamp())}"
    
    # 使用 URL 编码标准格式（与 TikTok 官方格式保持一致）
    # redirect_uri 需要 URL 编码
    encoded_redirect_uri = quote(settings.TIKTOK_REDIRECT_URI, safe='')
    
    auth_url = (
        f"https://business-api.tiktok.com/portal/auth"
        f"?app_id={settings.TIKTOK_APP_ID}"
        f"&state={state}"
        f"&redirect_uri={encoded_redirect_uri}"
    )
    
    return {
        "auth_url": auth_url,
        "state": state,
        "permission_level": "Business Center (Full Access)",
        "includes": [
            "Advertiser account management",
            "Campaign/AdGroup/Ad management",
            "Reporting & metrics",
            "Finance permissions",
            "Shop integration (if applicable)",
        ],
        "note": "redirect_uri is URL-encoded according to TikTok official standard",
    }


@router.get("/callback")
async def oauth_callback(
    auth_code: Optional[str] = Query(None, description="TikTok 返回的授权码（新参数名）"),
    code: Optional[str] = Query(None, description="TikTok 返回的授权码（旧参数名，兼容性）"),
    state: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    TikTok OAuth 回调接口
    完成 auth_code/code → access_token 换取，并存储到数据库
    
    TikTok 可能返回：
    - auth_code（新标准）
    - code（旧标准，兼容性）
    两个参数都支持
    """
    # 兼容两种参数名
    token_code = auth_code or code
    if not token_code:
        logger.error("OAuth callback: missing both auth_code and code parameters")
        raise HTTPException(status_code=400, detail="Missing auth_code or code parameter")

    logger.info(f"OAuth callback: state={state}, auth_code={token_code[:8]}...")

    # === State 前缀分流：涨粉模块专属授权，不写 advertisers 表 ===
    if state and state.startswith("growth_"):
        try:
            from app.api.growth import handle_growth_oauth_callback
            result = await handle_growth_oauth_callback(db=db, token_code=token_code, state=state)
            base = settings.TIKTOK_REDIRECT_URI.rsplit("/auth/callback", 1)[0]
            return RedirectResponse(
                url=f"{base}/growth?authorized={result.get('owner_advertiser_id', '')}"
                    f"&created={result.get('created', 0)}&updated={result.get('updated', 0)}",
                status_code=302,
            )
        except TikTokAPIError as e:
            base = settings.TIKTOK_REDIRECT_URI.rsplit("/auth/callback", 1)[0]
            return RedirectResponse(
                url=f"{base}/auth/error?message={quote(f'TikTok {e.code}: {e.message}')}",
                status_code=302,
            )
        except HTTPException as e:
            base = settings.TIKTOK_REDIRECT_URI.rsplit("/auth/callback", 1)[0]
            return RedirectResponse(
                url=f"{base}/auth/error?message={quote(str(e.detail))}",
                status_code=302,
            )
        except Exception as e:
            logger.exception(f"[GrowthOAuth] callback failed: {e}")
            base = settings.TIKTOK_REDIRECT_URI.rsplit("/auth/callback", 1)[0]
            return RedirectResponse(
                url=f"{base}/auth/error?message={quote(f'{type(e).__name__}: {e}')}",
                status_code=302,
            )

    try:
        # 1. 换取 token
        logger.info(f"[OAuth] Step 1: Exchanging auth_code for access_token")
        token_data = await TikTokClient.exchange_token(token_code)
        logger.info(f"[OAuth] Token exchange response keys: {list(token_data.keys())}")
        logger.info(f"[OAuth] Full token_data: {token_data}")
        
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")  # 秒数，如果有的话
        refresh_expires_in = token_data.get("refresh_expires_in")  # 秒数，如果有的话
        
        logger.info(f"[OAuth] access_token: {'✅ ' + access_token[:20] + '...' if access_token else '❌ None'}")
        logger.info(f"[OAuth] refresh_token: {'✅ ' + refresh_token[:20] + '...' if refresh_token else '⚠️  None (Business Center token - long-lived, no refresh needed)'}")
        logger.info(f"[OAuth] expires_in: {expires_in} seconds" + (f" (~{expires_in/3600:.1f}h)" if expires_in else " (not provided = long-lived token)"))
        
        if not access_token:
            logger.error(f"[OAuth] ERROR: No access_token in response. Keys: {list(token_data.keys())}")
            raise HTTPException(status_code=400, detail="No access_token in TikTok response")

        # 计算过期时间
        # Business Center 授权返回的 token 不带 expires_in，说明是长期有效的 token
        if expires_in:
            access_expire = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            logger.info(f"[OAuth] Token type: Short-lived (expires in {expires_in}s)")
        else:
            access_expire = None  # 长期有效，不过期
            logger.info(f"[OAuth] Token type: Long-lived Business Center token (no expiry)")
        
        refresh_expire = datetime.now(timezone.utc) + timedelta(seconds=refresh_expires_in) if refresh_expires_in else (datetime.now(timezone.utc) + timedelta(days=364) if refresh_token else None)
        logger.info(f"[OAuth] Expiry: access={access_expire}, refresh={refresh_expire}")

        # 2. 获取广告账户列表
        logger.info(f"[OAuth] Step 2: Getting advertiser list with access_token")
        advertiser_list = await TikTokClient.get_advertiser_list(access_token)
        logger.info(f"[OAuth] Got {len(advertiser_list)} advertiser(s): {[a.get('advertiser_id') for a in advertiser_list]}")
        
        if not advertiser_list:
            logger.error(f"[OAuth] ERROR: No advertiser accounts found")
            raise HTTPException(status_code=400, detail="No advertiser accounts found under this authorization")

        saved = []
        logger.info(f"[OAuth] Step 3: Saving advertisers to database")
        
        for idx, adv in enumerate(advertiser_list, 1):
            advertiser_id = str(adv["advertiser_id"])
            advertiser_name = adv.get("advertiser_name", "Unknown")
            currency = adv.get("currency", "")
            timezone_val = adv.get("timezone", "")
            
            logger.info(f"[OAuth]   [{idx}/{len(advertiser_list)}] Processing advertiser: {advertiser_id} ({advertiser_name})")

            # 3. 查数据库，存在则更新，不存在则创建
            result = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == advertiser_id))
            advertiser = result.scalar_one_or_none()

            if advertiser:
                logger.info(f"[OAuth]     Existing advertiser found, updating token...")
                advertiser.access_token = access_token
                if refresh_token:
                    advertiser.refresh_token = refresh_token
                    advertiser.refresh_token_expire_at = refresh_expire
                    logger.info(f"[OAuth]     Updated refresh_token")
                advertiser.access_token_expire_at = access_expire
                advertiser.is_token_valid = True
                advertiser.is_active = True
                advertiser.advertiser_name = advertiser_name
                logger.info(f"[OAuth]     ✅ Updated advertiser {advertiser_id}")
            else:
                logger.info(f"[OAuth]     New advertiser, creating record...")
                advertiser = Advertiser(
                    advertiser_id=advertiser_id,
                    advertiser_name=advertiser_name,
                    access_token=access_token,
                    refresh_token=refresh_token,  # 可能为 None
                    access_token_expire_at=access_expire,
                    refresh_token_expire_at=refresh_expire,
                    currency=currency,
                    timezone=timezone_val,
                )
                db.add(advertiser)
                logger.info(f"[OAuth]     ✅ Created advertiser {advertiser_id}")

            saved.append({"advertiser_id": advertiser_id, "name": advertiser_name})

        logger.info(f"[OAuth] Step 4: Committing {len(saved)} advertiser(s) to database")
        await db.commit()
        logger.info(f"[OAuth] ✅ All {len(saved)} advertiser(s) saved successfully")

        # Step 5: 自动触发全量数据同步（后台执行，不阻塞回调）
        import asyncio
        from app.tasks.sync_task import run_full_sync
        asyncio.create_task(run_full_sync(days=60))
        logger.info(f"[OAuth] Step 5: Full sync (60 days) triggered in background")

        # 重定向到前端成功页面（带参数）
        advertisers_json = ",".join([f"{a['advertiser_id']}:{a['name']}" for a in saved])
        logger.info(f"[OAuth] ✅ SUCCESS: Authorized {len(saved)} advertiser(s)")
        logger.info(f"[OAuth] Redirecting to success page: /auth/success?count={len(saved)}")
        
        return RedirectResponse(
            url=f"{settings.TIKTOK_REDIRECT_URI.rsplit('/auth/callback', 1)[0]}/auth/success?count={len(saved)}&advertisers={advertisers_json}",
            status_code=302
        )

    except TikTokAPIError as e:
        logger.error(f"[OAuth] ❌ TikTok API Error: code={e.code}, message={e.message}, request_id={e.request_id}")
        error_msg = f"TikTok Error [{e.code}]: {e.message}"
        logger.error(f"[OAuth] Redirecting to error page with message: {error_msg}")
        # 重定向到前端错误页面
        return RedirectResponse(
            url=f"{settings.TIKTOK_REDIRECT_URI.rsplit('/auth/callback', 1)[0]}/auth/error?message={quote(error_msg)}",
            status_code=302
        )
    except HTTPException as e:
        logger.error(f"[OAuth] ❌ HTTP Error: status={e.status_code}, detail={e.detail}")
        logger.error(f"[OAuth] Redirecting to error page with message: {e.detail}")
        return RedirectResponse(
            url=f"{settings.TIKTOK_REDIRECT_URI.rsplit('/auth/callback', 1)[0]}/auth/error?message={quote(str(e.detail))}",
            status_code=302
        )
    except Exception as e:
        logger.exception(f"[OAuth] ❌ Unexpected Error: {type(e).__name__}: {str(e)}")
        logger.error(f"[OAuth] Full traceback:", exc_info=True)
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"[OAuth] Redirecting to error page with message: {error_msg}")
        return RedirectResponse(
            url=f"{settings.TIKTOK_REDIRECT_URI.rsplit('/auth/callback', 1)[0]}/auth/error?message={quote(error_msg)}",
            status_code=302
        )


@router.get("/advertisers")
async def list_advertisers(
    db: AsyncSession = Depends(get_db),
    active_only: bool = Query(True),
):
    """列出所有已授权的广告账户，余额使用数据库缓存值，通过 /balance/refresh 更新"""
    query = select(Advertiser)
    if active_only:
        query = query.where(Advertiser.is_active == True)
    result = await db.execute(query.order_by(Advertiser.created_at.desc()))
    advertisers = result.scalars().all()

    return {
        "total": len(advertisers),
        "advertisers": [
            {
                "advertiser_id": a.advertiser_id,
                "name": a.advertiser_name,
                "is_active": a.is_active,
                "is_token_valid": a.is_token_valid,
                "is_token_expired": a.is_token_expired(),
                "hours_until_expiry": round(a.hours_until_expiry(), 2),
                "access_token_expire_at": a.access_token_expire_at,
                "refresh_token_expire_at": a.refresh_token_expire_at,
                "last_sync_at": a.last_sync_at,
                "currency": a.currency,
                "balance": a.balance,
            }
            for a in advertisers
        ],
    }


@router.post("/balance/refresh")
async def refresh_all_balances(db: AsyncSession = Depends(get_db)):
    """从 TikTok API 拉取所有账户的最新余额并写入数据库"""
    import asyncio

    result = await db.execute(
        select(Advertiser).where(Advertiser.is_active == True, Advertiser.is_token_valid == True)
    )
    advertisers = result.scalars().all()

    updated = {}

    async def _fetch(adv):
        client = TikTokClient(access_token=adv.access_token, advertiser_id=adv.advertiser_id)
        try:
            data = await client.get_balance()
            bal = data.get("balance")
            cash = data.get("cash")
            grant = data.get("grant")
            transfer_in = data.get("transfer_in")
            # 写入数据库
            adv.balance = str(bal) if bal is not None else adv.balance
            if not adv.currency and data.get("currency"):
                adv.currency = data["currency"]
            updated[adv.advertiser_id] = {
                "balance": bal, "cash": cash, "grant": grant, "transfer_in": transfer_in,
            }
        except Exception as e:
            logger.warning(f"Failed to refresh balance for {adv.advertiser_id}: {e}")
            updated[adv.advertiser_id] = {"error": str(e)}
        finally:
            await client.close()

    await asyncio.gather(*[_fetch(a) for a in advertisers])
    await db.commit()

    return {"updated": len([v for v in updated.values() if "error" not in v]), "details": updated}


@router.delete("/advertisers/{advertiser_id}")
async def delete_advertiser(
    advertiser_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    删除广告账户及其所有关联数据

    清理的数据包括：
    - 指标快照 (metrics_snapshots)
    - 决策记录 (decisions) 及决策效果 (decision_impacts)
    - 告警记录 (alerts)
    - 素材加热记录 (creative_heatups)
    - 素材快照 (creative_snapshots)
    - 素材 (creatives)
    - 素材分组条目 (creative_group_items) 及分组 (creative_groups)
    - 账户快照 (account_snapshots)
    - 日报 (daily_reports)
    - 风险告警 (risk_alerts)
    - 小时指标 (hourly_metrics)
    - 增长建议 (growth_recommendations)
    - 商品成本 (product_costs)
    - 广告账户本身 (advertisers)
    """
    # 检查账户是否存在
    result = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == advertiser_id))
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail=f"广告账户 {advertiser_id} 不存在")

    logger.info(f"[Delete] 开始删除广告账户 {advertiser_id} ({advertiser.advertiser_name}) 及所有关联数据")

    deleted_counts = {}

    # 按依赖顺序删除关联数据（子表先删）
    tables = [
        ("decision_impacts", DecisionImpact),
        ("decisions", Decision),
        ("alerts", Alert),
        ("creative_heatups", CreativeHeatUp),
        ("creative_snapshots", CreativeSnapshot),
        ("creatives", Creative),
        ("creative_group_items", CreativeGroupItem),
        ("creative_groups", CreativeGroup),
        ("metrics_snapshots", MetricsSnapshot),
        ("account_snapshots", AccountSnapshot),
        ("daily_reports", DailyReport),
        ("risk_alerts", RiskAlert),
        ("hourly_metrics", HourlyMetrics),
        ("growth_recommendations", GrowthRecommendation),
        ("product_costs", ProductCost),
    ]

    for name, model in tables:
        result = await db.execute(
            select(model).where(model.advertiser_id == advertiser_id)
        )
        rows = result.scalars().all()
        for row in rows:
            await db.delete(row)
        deleted_counts[name] = len(rows)
        if rows:
            logger.info(f"[Delete]   {name}: 删除 {len(rows)} 条记录")

    # 最后删除广告账户本身
    await db.delete(advertiser)
    await db.commit()

    logger.info(f"[Delete] ✅ 广告账户 {advertiser_id} 及所有关联数据已删除")

    return {
        "message": f"广告账户 {advertiser_id} 已删除",
        "advertiser_id": advertiser_id,
        "advertiser_name": advertiser.advertiser_name,
        "deleted_counts": deleted_counts,
    }
