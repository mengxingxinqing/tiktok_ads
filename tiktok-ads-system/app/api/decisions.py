"""
决策管理接口
- GET  /decisions          查看决策列表（支持过滤）
- POST /decisions/{id}/approve   人工批准并执行
- POST /decisions/{id}/reject    人工拒绝
- POST /decisions/{id}/rollback  回滚已执行的决策
- GET  /alerts             查看告警列表
- POST /alerts/{id}/resolve      标记告警为已解决
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.advertiser import Advertiser
from app.models.decision import Decision
from app.models.alert import Alert
from app.services.llm_decision import LLMDecisionService

router = APIRouter(tags=["Decisions & Alerts"])
llm_svc = LLMDecisionService()


# ===== 决策接口 =====

@router.get("/decisions")
async def list_decisions(
    advertiser_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    query = select(Decision).order_by(Decision.created_at.desc())
    if advertiser_id:
        query = query.where(Decision.advertiser_id == advertiser_id)
    if status:
        query = query.where(Decision.status == status)
    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    decisions = result.scalars().all()

    return {
        "total": len(decisions),
        "items": [
            {
                "id": d.id,
                "advertiser_id": d.advertiser_id,
                "data_level": d.data_level,
                "object_id": d.object_id,
                "object_name": d.object_name,
                "action": d.action,
                "action_params": d.action_params,
                "confidence": d.confidence,
                "reason": d.reason,
                "status": d.status,
                "is_auto_executed": d.is_auto_executed,
                "executed_at": d.executed_at,
                "trigger_type": d.trigger_type,
                "created_at": d.created_at,
            }
            for d in decisions
        ],
    }


@router.post("/decisions/{decision_id}/approve")
async def approve_decision(
    decision_id: int,
    db: AsyncSession = Depends(get_db),
):
    """人工批准并立即执行决策"""
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    decision = result.scalar_one_or_none()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    if decision.status not in ("PENDING",):
        raise HTTPException(status_code=400, detail=f"Decision status is {decision.status}, cannot approve")

    # 获取广告主
    adv_result = await db.execute(
        select(Advertiser).where(Advertiser.advertiser_id == decision.advertiser_id)
    )
    advertiser = adv_result.scalar_one_or_none()
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")

    decision.status = "MANUAL_APPROVED"
    ok = await llm_svc.execute_decision(decision, advertiser, db)
    return {"success": ok, "decision_id": decision_id, "action": decision.action}


@router.post("/decisions/{decision_id}/reject")
async def reject_decision(
    decision_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    decision = result.scalar_one_or_none()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    if decision.status != "PENDING":
        raise HTTPException(status_code=400, detail=f"Cannot reject: status={decision.status}")

    decision.status = "MANUAL_REJECTED"
    await db.commit()
    return {"success": True, "decision_id": decision_id}


@router.post("/decisions/{decision_id}/rollback")
async def rollback_decision(
    decision_id: int,
    db: AsyncSession = Depends(get_db),
):
    """回滚已执行的决策（执行反向操作）"""
    result = await db.execute(select(Decision).where(Decision.id == decision_id))
    decision = result.scalar_one_or_none()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    if decision.status not in ("AUTO_EXECUTED", "MANUAL_APPROVED"):
        raise HTTPException(status_code=400, detail="Only executed decisions can be rolled back")

    # 构造反向动作
    reverse_map = {
        "pause": "enable",
        "enable": "pause",
        "increase_budget": "decrease_budget",
        "decrease_budget": "increase_budget",
        "increase_bid": "decrease_bid",
        "decrease_bid": "increase_bid",
    }
    reverse_action = reverse_map.get(decision.action)
    if not reverse_action:
        raise HTTPException(status_code=400, detail=f"Action '{decision.action}' cannot be rolled back automatically")

    # 获取广告主
    adv_result = await db.execute(
        select(Advertiser).where(Advertiser.advertiser_id == decision.advertiser_id)
    )
    advertiser = adv_result.scalar_one_or_none()

    # 创建回滚决策
    rollback = Decision(
        advertiser_id=decision.advertiser_id,
        data_level=decision.data_level,
        object_id=decision.object_id,
        object_name=decision.object_name,
        trigger_type="MANUAL",
        trigger_reason=f"手动回滚决策 #{decision_id}",
        action=reverse_action,
        action_params=decision.pre_action_state or {},
        confidence=1.0,
        reason=f"回滚操作：撤销决策 #{decision_id} ({decision.action})",
        status="MANUAL_APPROVED",
        is_rollback=True,
        rollback_of_id=decision_id,
    )
    db.add(rollback)
    await db.flush()

    ok = await llm_svc.execute_decision(rollback, advertiser, db)
    return {"success": ok, "rollback_decision_id": rollback.id, "original_decision_id": decision_id}


# ===== 告警接口 =====

@router.get("/alerts")
async def list_alerts(
    advertiser_id: Optional[str] = None,
    shop_id: Optional[str] = None,
    severity: Optional[str] = None,
    is_resolved: Optional[bool] = Query(False),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
):
    query = select(Alert).order_by(Alert.created_at.desc())
    if advertiser_id:
        query = query.where(Alert.advertiser_id == advertiser_id)
    if severity:
        query = query.where(Alert.severity == severity)
    if is_resolved is not None:
        query = query.where(Alert.is_resolved == is_resolved)
    query = query.limit(limit)

    result = await db.execute(query)
    alerts = result.scalars().all()

    return {
        "total": len(alerts),
        "items": [
            {
                "id": a.id,
                "advertiser_id": a.advertiser_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "title": a.title,
                "message": a.message,
                "object_id": a.object_id,
                "object_name": a.object_name,
                "is_resolved": a.is_resolved,
                "metrics_snapshot": a.metrics_snapshot,
                "created_at": a.created_at,
                "shop_id": shop_id,  # 透传 shop_id 过滤参数
            }
            for a in alerts
        ],
        "shop_id": shop_id,
    }


@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_resolved = True
    alert.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    return {"success": True, "alert_id": alert_id}
