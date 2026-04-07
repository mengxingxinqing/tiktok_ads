"""
分析和报表 API

GET  /analytics/account/{advertiser_id}        账户大盘
GET  /analytics/risks/{advertiser_id}          风险告警
GET  /analytics/stop-loss/{advertiser_id}      止损方案
POST /analytics/growth-recommendation          生成梯度增长建议
GET  /analytics/growth-recommendation/{id}     获取建议
POST /analytics/growth-recommendation/{id}/apply  应用建议
"""
from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.analytics_service import AnalyticsService
from app.services.growth_recommendation import GrowthRecommendationEngine

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/account/{advertiser_id}")
async def get_account_overview(advertiser_id: str, db: AsyncSession = Depends(get_db)):
    """获取账户大盘"""
    try:
        service = AnalyticsService(db)
        overview = await service.get_account_overview(advertiser_id)
        return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/snapshot/{advertiser_id}")
async def generate_snapshot(advertiser_id: str, db: AsyncSession = Depends(get_db)):
    """手动生成账户快照（用于测试）"""
    try:
        service = AnalyticsService(db)
        snapshot = await service.generate_account_snapshot(advertiser_id)
        await db.commit()
        return {
            "success": True,
            "snapshot": {
                "spend": snapshot.spend,
                "gmv": snapshot.gmv,
                "roas": snapshot.roas,
                "profit": snapshot.real_profit,
                "health_score": snapshot.health_score,
                "risk_level": snapshot.risk_level,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risks/{advertiser_id}")
async def get_risk_alerts(advertiser_id: str, db: AsyncSession = Depends(get_db)):
    """获取风险告警"""
    try:
        service = AnalyticsService(db)
        alerts = await service.detect_risk_alerts(advertiser_id)
        await db.commit()
        return {
            "total": len(alerts),
            "alerts": [
                {
                    "type": a.alert_type,
                    "severity": a.severity,
                    "title": a.title,
                    "message": a.message,
                    "recommended_action": a.recommended_action,
                }
                for a in alerts
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stop-loss/{advertiser_id}")
async def get_stop_loss_plan(advertiser_id: str, db: AsyncSession = Depends(get_db)):
    """获取止损方案"""
    try:
        service = AnalyticsService(db)
        plan = await service.generate_stop_loss_plan(advertiser_id)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== 梯度增长建议 =====

class GrowthRecommendationRequest(BaseModel):
    advertiser_id: str
    object_type: str  # CAMPAIGN / ADGROUP / VIDEO
    object_id: str
    object_name: str
    current_daily_spend: float
    current_hook_rate: float
    days_running: int


class ApplyPlanRequest(BaseModel):
    chosen_plan: str  # conservative / standard / aggressive


@router.post("/growth-recommendation")
async def generate_growth_recommendation(
    req: GrowthRecommendationRequest, db: AsyncSession = Depends(get_db)
):
    """生成梯度增长建议"""
    try:
        engine = GrowthRecommendationEngine(db)
        recommendation = await engine.generate_recommendation(
            advertiser_id=req.advertiser_id,
            object_type=req.object_type,
            object_id=req.object_id,
            object_name=req.object_name,
            current_daily_spend=req.current_daily_spend,
            current_hook_rate=req.current_hook_rate,
            days_running=req.days_running,
        )
        await db.commit()

        if not recommendation:
            raise HTTPException(status_code=400, detail="Failed to generate recommendation")

        return {
            "id": recommendation.id,
            "object_name": recommendation.object_name,
            "current_stage": recommendation.current_stage,
            "current_spend": recommendation.current_daily_spend,
            "current_hook": recommendation.current_hook_rate,
            "conservative_plan": recommendation.conservative_plan,
            "standard_plan": recommendation.standard_plan,
            "aggressive_plan": recommendation.aggressive_plan,
            "recommended": recommendation.recommended_plan,
            "confidence": recommendation.confidence,
            "risk_notes": recommendation.risk_notes,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/growth-recommendation/{recommendation_id}")
async def get_growth_recommendation(recommendation_id: int, db: AsyncSession = Depends(get_db)):
    """获取梯度增长建议"""
    from sqlalchemy import select
    from app.models.analytics import GrowthRecommendation

    rec_q = select(GrowthRecommendation).where(GrowthRecommendation.id == recommendation_id)
    result = await db.execute(rec_q)
    rec = result.scalar_one_or_none()

    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return {
        "id": rec.id,
        "object_name": rec.object_name,
        "current_stage": rec.current_stage,
        "conservative_plan": rec.conservative_plan,
        "standard_plan": rec.standard_plan,
        "aggressive_plan": rec.aggressive_plan,
        "recommended": rec.recommended_plan,
        "status": rec.status,
    }


@router.post("/growth-recommendation/{recommendation_id}/apply")
async def apply_growth_recommendation(
    recommendation_id: int, req: ApplyPlanRequest, db: AsyncSession = Depends(get_db)
):
    """应用某个梯度增长方案"""
    try:
        engine = GrowthRecommendationEngine(db)
        success = await engine.apply_recommendation(recommendation_id, req.chosen_plan)

        if not success:
            raise HTTPException(status_code=404, detail="Recommendation not found")

        return {"success": True, "applied_plan": req.chosen_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
