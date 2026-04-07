"""
规则引擎 API — 可配置告警规则的增删改查
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.rule import AlertRule, DEFAULT_RULES

router = APIRouter(prefix="/rules", tags=["rules"])


# ---- Pydantic schemas ----

class RuleOut(BaseModel):
    id: int
    rule_key: str
    rule_name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    params: Optional[Dict[str, Any]]
    severity: str
    is_enabled: bool
    advertiser_id: Optional[str]

    class Config:
        from_attributes = True


class RuleUpdate(BaseModel):
    rule_name: Optional[str] = None
    description: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    severity: Optional[str] = None
    is_enabled: Optional[bool] = None


# ---- Endpoints ----

@router.get("")
async def list_rules(
    category: Optional[str] = None,
    is_enabled: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
):
    """获取所有规则列表（支持按 category / is_enabled 过滤）"""
    query = select(AlertRule)
    if category:
        query = query.where(AlertRule.category == category)
    if is_enabled is not None:
        query = query.where(AlertRule.is_enabled == is_enabled)
    result = await db.execute(query.order_by(AlertRule.id))
    rules = result.scalars().all()
    return {"total": len(rules), "rules": rules}


@router.put("/{rule_key}", response_model=RuleOut)
async def update_rule(
    rule_key: str,
    body: RuleUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新规则参数或开关"""
    result = await db.execute(select(AlertRule).where(AlertRule.rule_key == rule_key))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule '{rule_key}' not found")

    if body.rule_name is not None:
        rule.rule_name = body.rule_name
    if body.description is not None:
        rule.description = body.description
    if body.params is not None:
        rule.params = body.params
    if body.severity is not None:
        rule.severity = body.severity
    if body.is_enabled is not None:
        rule.is_enabled = body.is_enabled

    await db.commit()
    await db.refresh(rule)
    return rule


@router.post("/reset", response_model=List[RuleOut])
async def reset_rules(db: AsyncSession = Depends(get_db)):
    """重置所有规则为默认值（只更新 params/severity，不删除自定义规则）"""
    default_map = {r["rule_key"]: r for r in DEFAULT_RULES}

    result = await db.execute(select(AlertRule))
    existing = {r.rule_key: r for r in result.scalars().all()}

    for rule_key, defaults in default_map.items():
        if rule_key in existing:
            rule = existing[rule_key]
            rule.params = defaults.get("params")
            rule.severity = defaults.get("severity", "WARNING")
            rule.is_enabled = True
        else:
            db.add(AlertRule(**defaults))

    await db.commit()

    result = await db.execute(select(AlertRule).order_by(AlertRule.id))
    return result.scalars().all()
