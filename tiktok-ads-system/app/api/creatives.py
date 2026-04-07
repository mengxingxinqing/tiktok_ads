"""
素材监控接口
GET /creatives                  素材列表（支持过滤）
GET /creatives/{video_id}       素材详情 + 历史趋势
GET /creatives/fatigue          疲劳素材列表
GET /dashboard/creative-stats   素材维度统计
"""
import logging
import time
from datetime import date, timedelta
from typing import Optional, Dict, Any, List
from collections import defaultdict

import asyncio
import httpx

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, func

from app.core.database import get_db
from app.models.creative import Creative, CreativeSnapshot, LifecycleStage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/creatives", tags=["Creatives"])


@router.get("")
async def list_creatives(
    advertiser_id: Optional[str] = None,
    lifecycle_stage: Optional[str] = None,
    is_fatigue: Optional[bool] = None,
    min_spend: float = Query(0, description="最低花费筛选"),
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """素材列表，默认按最近活跃时间倒序"""
    query = select(Creative).order_by(Creative.last_active_date.desc())

    if advertiser_id:
        query = query.where(Creative.advertiser_id == advertiser_id)
    if lifecycle_stage:
        query = query.where(Creative.lifecycle_stage == lifecycle_stage)
    if is_fatigue is not None:
        query = query.where(Creative.is_fatigue == ("Y" if is_fatigue else "N"))

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    creatives = result.scalars().all()

    return {
        "total": len(creatives),
        "items": [_format_creative(c) for c in creatives],
    }


@router.get("/fatigue")
async def fatigue_creatives(
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """疲劳素材列表 — 需要优先处理"""
    query = (
        select(Creative)
        .where(Creative.is_fatigue == "Y")
        .order_by(Creative.last_active_date.desc())
        .limit(100)
    )
    if advertiser_id:
        query = query.where(Creative.advertiser_id == advertiser_id)

    result = await db.execute(query)
    creatives = result.scalars().all()
    return {"total": len(creatives), "items": [_format_creative(c) for c in creatives]}


@router.get("/gmvmax-items")
async def list_gmvmax_items(
    advertiser_id: Optional[str] = None,
    item_group_id: Optional[str] = Query(None, description="按 item_group_id 过滤"),
    sort_by: str = Query("total_spend", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    db: AsyncSession = Depends(get_db),
):
    """GMVMax 商品组数据 — 直接从 product_view 表读取"""
    from app.models.views import ProductView

    query = select(ProductView)
    if advertiser_id:
        query = query.where(ProductView.advertiser_id == advertiser_id)
    if item_group_id:
        query = query.where(ProductView.item_group_id.like(f"%{item_group_id}%"))

    sort_map = {
        "total_spend": ProductView.total_spend, "total_orders": ProductView.total_orders,
        "total_revenue": ProductView.total_revenue, "avg_roi": ProductView.roi,
    }
    col = sort_map.get(sort_by, ProductView.total_spend)
    query = query.order_by(col.desc() if sort_order == "desc" else col.asc())

    result = await db.execute(query)
    rows = result.scalars().all()

    return {
        "total": len(rows),
        "sort_by": sort_by,
        "sort_order": sort_order,
        "enriched": True,
        "items": [
            {
                "item_group_id": r.item_group_id,
                "advertiser_id": r.advertiser_id or "",
                "product_name": r.title or "",
                "image_url": r.image_url or "",
                "price": r.min_price,
                "total_spend": r.total_spend or 0,
                "total_orders": r.total_orders or 0,
                "total_revenue": r.total_revenue or 0,
                "avg_roi": r.roi or 0,
                "active_days": r.active_days or 0,
                "creative_count": r.creative_count or 0,
                "first_seen": str(r.first_seen) if r.first_seen else None,
                "last_seen": str(r.last_seen) if r.last_seen else None,
            }
            for r in rows
        ],
    }


# oEmbed 缓存：item_id -> {title, thumbnail_url}
_oembed_cache: Dict[str, Dict[str, str]] = {}


async def _fetch_oembed_batch(item_ids: List[str]) -> Dict[str, Dict[str, str]]:
    """
    批量获取 TikTok oEmbed 信息（公开 API，不需要 token）。
    item_id = TikTok 帖子 ID，可获取缩略图和标题。
    结果缓存在内存中避免重复请求。
    """
    result = {}
    to_fetch = []
    for iid in item_ids:
        if iid in _oembed_cache:
            result[iid] = _oembed_cache[iid]
        elif iid and iid != "-1":
            to_fetch.append(iid)

    if not to_fetch:
        return result

    async def _get_one(client: httpx.AsyncClient, iid: str):
        try:
            resp = await client.get(
                "https://www.tiktok.com/oembed",
                params={"url": f"https://www.tiktok.com/video/{iid}"},
            )
            if resp.status_code == 200:
                data = resp.json()
                # 从 html 的 cite 属性提取正确 URL（含 @username）
                import re
                html = data.get("html", "")
                cite_match = re.search(r'cite="(https://www\.tiktok\.com/@[^"]+)"', html)
                video_url = cite_match.group(1) if cite_match else f"https://www.tiktok.com/@{data.get('author_unique_id', data.get('author_name', ''))}/video/{iid}"
                entry = {
                    "title": data.get("title", ""),
                    "thumbnail_url": data.get("thumbnail_url", ""),
                    "author_name": data.get("author_name", ""),
                    "video_url": video_url,
                }
                _oembed_cache[iid] = entry
                return iid, entry
        except Exception:
            pass
        return iid, {}

    async with httpx.AsyncClient(timeout=8.0) as client:
        tasks = [_get_one(client, iid) for iid in to_fetch[:50]]  # 最多 50 个并发
        results = await asyncio.gather(*tasks)
        for iid, entry in results:
            result[iid] = entry

    return result


@router.get("/gmvmax-creatives")
async def list_gmvmax_creatives(
    advertiser_id: Optional[str] = None,
    item_id: Optional[str] = Query(None, description="按 item_id 过滤"),
    start_date: Optional[str] = Query(None, description="创建日期起始 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="创建日期截止 YYYY-MM-DD"),
    sort_by: str = Query("total_spend", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    include_auto: bool = Query(True, description="是否包含自动选品"),
    db: AsyncSession = Depends(get_db),
):
    """GMVMax 创意列表 — 直接从 creative_view 表读取"""
    from app.models.views import CreativeView

    query = select(CreativeView)
    if advertiser_id:
        query = query.where(CreativeView.advertiser_id == advertiser_id)
    if not include_auto:
        query = query.where(CreativeView.is_auto_selected == 0)
    if item_id:
        query = query.where(CreativeView.item_id.like(f"%{item_id}%"))
    if start_date:
        query = query.where(CreativeView.first_seen >= start_date)
    if end_date:
        query = query.where(CreativeView.first_seen <= end_date)

    sort_map = {
        "total_spend": CreativeView.total_spend, "total_orders": CreativeView.total_orders,
        "total_revenue": CreativeView.total_revenue, "avg_roi": CreativeView.roi,
    }
    col = sort_map.get(sort_by, CreativeView.total_spend)
    query = query.order_by(col.desc() if sort_order == "desc" else col.asc())

    result = await db.execute(query)
    rows = result.scalars().all()

    # 批量获取 oEmbed 缩略图（item_id = TikTok 帖子 ID）
    oembed_cache = await _fetch_oembed_batch([r.item_id for r in rows if r.item_id and not r.is_auto_selected and r.item_id != "-1"])

    items = []
    for r in rows:
        iid = r.item_id or ""
        oe = oembed_cache.get(iid, {})
        # 视频 URL：直接用 TikTok 帖子链接（可嵌入播放）
        tiktok_video_url = oe.get("video_url", "") or (f"https://www.tiktok.com/video/{iid}" if iid and iid != "-1" and not r.is_auto_selected else "")
        items.append({
            "item_id": iid,
            "is_auto_selected": bool(r.is_auto_selected),
            "label": "自动选品" if r.is_auto_selected else (r.product_name or r.creative_name or f"创意...{iid[-6:]}" if iid and len(iid) > 6 else iid),
            "advertiser_id": r.advertiser_id or "",
            "product_name": oe.get("title") or r.product_name or "",
            "image_url": oe.get("thumbnail_url") or r.product_image_url or "",
            "cover_url": oe.get("thumbnail_url") or r.cover_url or "",
            "video_url": r.video_url or tiktok_video_url,
            "video_id": r.video_id or "",
            "tiktok_url": tiktok_video_url,
            "creative_name": r.creative_name or "",
            "campaign_id": r.campaign_id or "",
            "parent_item_group_id": r.item_group_id or "",
            "total_spend": r.total_spend or 0,
            "total_orders": r.total_orders or 0,
            "total_revenue": r.total_revenue or 0,
            "total_impressions": r.total_impressions or 0,
            "total_clicks": r.total_clicks or 0,
            "avg_roi": r.roi or 0,
            "avg_cost_per_order": r.avg_cost_per_order or 0,
            "stage": r.stage or "UNKNOWN",
            "trend": r.trend or "",
            "recommendation": r.recommendation or "",
            "reason": r.reason or "",
            "daily_avg_spend": r.daily_avg_spend or 0,
            "active_days": r.active_days or 0,
            "first_seen": str(r.first_seen) if r.first_seen else None,
            "last_seen": str(r.last_seen) if r.last_seen else None,
        })

    return {
        "total": len(rows),
        "sort_by": sort_by,
        "sort_order": sort_order,
        "enriched": True,
        "items": items,
    }


# 以下旧代码（_analyze_creative_lifecycle 等）已移至 view_builder.py，保留空标记
# 旧的 _fetch_product_map / _fetch_video_map 缓存逻辑也已移至 view_builder

_LEGACY_REMOVED = True  # 标记旧代码已清理

@router.get("/{video_id}/trend")
async def creative_trend(
    video_id: str,
    advertiser_id: str,
    days: int = Query(14, le=30),
    db: AsyncSession = Depends(get_db),
):
    """素材历史趋势数据"""
    since = date.today() - timedelta(days=days)

    result = await db.execute(
        select(CreativeSnapshot)
        .where(
            CreativeSnapshot.advertiser_id == advertiser_id,
            CreativeSnapshot.video_id == video_id,
            CreativeSnapshot.stat_date >= since,
        )
        .order_by(CreativeSnapshot.stat_date.asc())
    )
    snaps = result.scalars().all()

    # 每天取最新
    by_date = {}
    for s in snaps:
        if s.stat_date not in by_date or s.snapshot_time > by_date[s.stat_date].snapshot_time:
            by_date[s.stat_date] = s
    daily = sorted(by_date.values(), key=lambda x: x.stat_date)

    return {
        "video_id": video_id,
        "days": days,
        "data": [
            {
                "date": str(s.stat_date),
                "spend": s.spend,
                "impressions": s.impressions,
                "ctr": s.ctr,
                "hook_rate": s.hook_rate,
                "hold_rate": s.hold_rate,
                "avg_play_sec": s.average_video_play,
                "conversion": s.conversion,
                "lifecycle_stage": s.lifecycle_stage,
                "days_running": s.days_running,
                "ad_count": s.ad_count,
            }
            for s in daily
        ],
    }


@router.get("/stats/overview")
async def creative_stats(
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """素材维度统计概览"""
    q = select(Creative)
    if advertiser_id:
        q = q.where(Creative.advertiser_id == advertiser_id)
    result = await db.execute(q)
    all_creatives = result.scalars().all()

    by_stage = {}
    for c in all_creatives:
        stage = c.lifecycle_stage or "UNKNOWN"
        by_stage[stage] = by_stage.get(stage, 0) + 1

    # 今日 hook_rate 均值
    today = date.today()
    hook_result = await db.execute(
        select(func.avg(CreativeSnapshot.hook_rate))
        .where(
            CreativeSnapshot.stat_date == today,
            CreativeSnapshot.spend > 1,
            *([CreativeSnapshot.advertiser_id == advertiser_id] if advertiser_id else []),
        )
    )
    avg_hook = float(hook_result.scalar() or 0)

    return {
        "total_creatives": len(all_creatives),
        "fatigue_count": sum(1 for c in all_creatives if c.is_fatigue == "Y"),
        "by_lifecycle": by_stage,
        "avg_hook_rate_today": round(avg_hook, 2),
    }


@router.get("/preview/{video_id}")
async def creative_preview(
    video_id: str,
    advertiser_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取素材的视频预览 URL 和封面图"""
    from app.models.advertiser import Advertiser
    from app.services.tiktok_client import TikTokClient, TikTokAPIError

    result = await db.execute(
        select(Advertiser).where(Advertiser.advertiser_id == advertiser_id)
    )
    advertiser = result.scalar_one_or_none()
    if not advertiser:
        return {"error": "Advertiser not found"}

    client = TikTokClient(
        access_token=advertiser.access_token,
        advertiser_id=advertiser_id,
    )
    try:
        videos = await client.get_video_info([video_id])
        if videos:
            v = videos[0]
            return {
                "video_id": v.get("video_id"),
                "preview_url": v.get("preview_url"),
                "cover_url": v.get("video_cover_url"),
                "file_name": v.get("file_name"),
                "duration": v.get("duration"),
                "width": v.get("width"),
                "height": v.get("height"),
            }
        return {"error": "Video not found", "video_id": video_id}
    except TikTokAPIError as e:
        return {"error": str(e.message), "video_id": video_id}
    finally:
        await client.close()


def _format_creative(c: Creative) -> dict:
    return {
        "id": c.id,
        "advertiser_id": c.advertiser_id,
        "video_id": c.video_id,
        "creative_name": c.creative_name,
        "video_url": c.video_url,
        "cover_url": c.cover_url,
        "duration": c.duration,
        "status": c.status,
        "shop_id": c.shop_id,
        "shop_name": c.shop_name,
        "product_id": c.product_id,
        "product_name": c.product_name,
        "lifecycle_stage": c.lifecycle_stage,
        "is_fatigue": c.is_fatigue == "Y",
        "days_running": c.days_running,
        "total_spend": c.total_spend,
        "total_conversion": c.total_conversion,
        "total_impression": c.total_impression,
        "latest_ctr": c.latest_ctr,
        "latest_roas": c.latest_roas,
        "latest_hook_rate": c.latest_hook_rate,
        "latest_hold_rate": c.latest_hold_rate,
        "first_seen_date": str(c.first_seen_date) if c.first_seen_date else None,
        "last_active_date": str(c.last_active_date) if c.last_active_date else None,
    }
