"""
素材加热管理接口
POST /boost/scan/{advertiser_id}   手动触发扫描
GET  /boost/candidates             查看当前加热候选素材
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.models.decision import Decision

router = APIRouter(prefix="/boost", tags=["Creative Boost"])


@router.post("/scan/{advertiser_id}")
async def trigger_boost_scan(
    advertiser_id: str,
    db: AsyncSession = Depends(get_db),
):
    """手动触发单个账户的加热扫描"""
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

    from app.services.creative_booster import CreativeBooster
    booster = CreativeBooster(db)
    decisions = await booster.scan_and_boost(advertiser_id)

    return {
        "advertiser_id": advertiser_id,
        "boost_decisions": len(decisions),
        "decisions": [
            {
                "id": d.id,
                "video_id": d.object_id,
                "action": d.action,
                "action_params": d.action_params,
                "confidence": d.confidence,
                "status": d.status,
                "reason": d.reason,
            }
            for d in decisions
        ],
    }


@router.get("/candidates")
async def list_boost_candidates(
    advertiser_id: str = None,
    db: AsyncSession = Depends(get_db),
):
    """查看待处理的加热决策"""
    query = (
        select(Decision)
        .where(
            Decision.trigger_type == "BOOST_OPPORTUNITY",
            Decision.status == "PENDING",
        )
        .order_by(Decision.created_at.desc())
        .limit(50)
    )
    if advertiser_id:
        query = query.where(Decision.advertiser_id == advertiser_id)

    result = await db.execute(query)
    decisions = result.scalars().all()

    return {
        "total": len(decisions),
        "items": [
            {
                "id": d.id,
                "advertiser_id": d.advertiser_id,
                "video_id": d.object_id,
                "action": d.action,
                "action_params": d.action_params,
                "confidence": d.confidence,
                "reason": d.reason,
                "metrics": d.metrics_context,
                "created_at": d.created_at,
            }
            for d in decisions
        ],
    }
