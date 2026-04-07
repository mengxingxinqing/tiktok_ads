"""
评论管理接口

GET    /comments                      评论列表（支持筛选）
GET    /comments/stats                评论统计概览
POST   /comments/sync/trigger         手动触发评论同步
POST   /comments/{comment_id}/hide    隐藏评论
POST   /comments/{comment_id}/show    显示评论
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.core.database import get_db
from app.models.comment import AdComment

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("")
async def list_comments(
    advertiser_id: Optional[str] = None,
    ad_id: Optional[str] = None,
    sentiment: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """评论列表，支持按账户、广告、情感、状态筛选"""
    query = select(AdComment).order_by(desc(AdComment.comment_time))

    if advertiser_id:
        query = query.where(AdComment.advertiser_id == advertiser_id)
    if ad_id:
        query = query.where(AdComment.ad_id == ad_id)
    if sentiment:
        query = query.where(AdComment.sentiment == sentiment)
    if status:
        query = query.where(AdComment.status == status)

    # 总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # 分页
    result = await db.execute(query.offset((page - 1) * page_size).limit(page_size))
    comments = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [_fmt_comment(c) for c in comments],
    }


@router.get("/stats")
async def comment_stats(
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """评论统计概览"""
    base = select(AdComment)
    if advertiser_id:
        base = base.where(AdComment.advertiser_id == advertiser_id)

    # 总数
    total = (await db.execute(
        select(func.count()).select_from(base.subquery())
    )).scalar() or 0

    # 按情感分布
    sentiment_query = (
        select(AdComment.sentiment, func.count().label("cnt"))
        .group_by(AdComment.sentiment)
    )
    if advertiser_id:
        sentiment_query = sentiment_query.where(AdComment.advertiser_id == advertiser_id)
    sentiment_result = await db.execute(sentiment_query)
    sentiment_dist = {r.sentiment or "UNKNOWN": r.cnt for r in sentiment_result.all()}

    # 未回复数
    unreplied = (await db.execute(
        select(func.count()).select_from(
            base.where(AdComment.is_owner_replied == False).subquery()
        )
    )).scalar() or 0

    return {
        "total": total,
        "unreplied": unreplied,
        "sentiment": sentiment_dist,
    }


@router.post("/sync/trigger")
async def trigger_comment_sync():
    """手动触发一次评论同步（通过 Celery）"""
    from app.tasks.celery_tasks import comment_sync
    result = comment_sync.delay()
    return {"message": "评论同步任务已派发", "task_id": result.id}


def _fmt_comment(c: AdComment) -> dict:
    return {
        "id": c.id,
        "comment_id": c.comment_id,
        "advertiser_id": c.advertiser_id,
        "ad_id": c.ad_id,
        "campaign_id": c.campaign_id,
        "parent_comment_id": c.parent_comment_id,
        "content": c.content,
        "user_name": c.user_name,
        "user_avatar": c.user_avatar,
        "likes": c.likes,
        "replies": c.replies,
        "status": c.status,
        "is_owner_replied": c.is_owner_replied,
        "sentiment": c.sentiment,
        "sentiment_score": c.sentiment_score,
        "comment_time": str(c.comment_time) if c.comment_time else None,
        "created_at": str(c.created_at) if c.created_at else None,
    }
