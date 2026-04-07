"""
素材分组接口
GET    /creative-groups                        分组列表
POST   /creative-groups                        创建分组
PUT    /creative-groups/{group_id}              更新分组
DELETE /creative-groups/{group_id}              删除分组
POST   /creative-groups/{group_id}/items        批量添加素材
DELETE /creative-groups/{group_id}/items/{video_id}  移除素材
GET    /creative-groups/{group_id}/stats        分组聚合指标
GET    /creative-groups/compare                 多分组对比
"""
import logging
from datetime import date, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, delete

from app.core.database import get_db
from app.models.creative_group import CreativeGroup, CreativeGroupItem
from app.models.creative import Creative, CreativeSnapshot

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/creative-groups", tags=["CreativeGroups"])


# ── Schemas ──────────────────────────────────────────────

class GroupCreate(BaseModel):
    name: str
    advertiser_id: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = "#6366f1"


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None


class ItemsAdd(BaseModel):
    video_ids: List[str]
    advertiser_id: Optional[str] = None


# ── CRUD ─────────────────────────────────────────────────

@router.get("")
async def list_groups(
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """分组列表"""
    query = select(CreativeGroup).order_by(CreativeGroup.created_at.desc())
    if advertiser_id:
        query = query.where(CreativeGroup.advertiser_id == advertiser_id)
    result = await db.execute(query)
    groups = result.scalars().all()
    return {
        "total": len(groups),
        "items": [_fmt_group(g) for g in groups],
    }


@router.post("")
async def create_group(body: GroupCreate, db: AsyncSession = Depends(get_db)):
    """创建分组"""
    group = CreativeGroup(
        name=body.name,
        advertiser_id=body.advertiser_id,
        description=body.description,
        color=body.color,
    )
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return _fmt_group(group)


@router.put("/{group_id}")
async def update_group(group_id: int, body: GroupUpdate, db: AsyncSession = Depends(get_db)):
    """更新分组"""
    result = await db.execute(select(CreativeGroup).where(CreativeGroup.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        return {"error": "Group not found"}
    for field, val in body.model_dump(exclude_unset=True).items():
        setattr(group, field, val)
    await db.commit()
    await db.refresh(group)
    return _fmt_group(group)


@router.delete("/{group_id}")
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)):
    """删除分组（级联删除条目）"""
    result = await db.execute(select(CreativeGroup).where(CreativeGroup.id == group_id))
    group = result.scalar_one_or_none()
    if not group:
        return {"error": "Group not found"}
    await db.delete(group)
    await db.commit()
    return {"ok": True}


# ── Items ────────────────────────────────────────────────

@router.post("/{group_id}/items")
async def add_items(group_id: int, body: ItemsAdd, db: AsyncSession = Depends(get_db)):
    """批量添加素材到分组，重复 video_id 跳过"""
    # 校验分组存在
    grp = await db.execute(select(CreativeGroup).where(CreativeGroup.id == group_id))
    if not grp.scalar_one_or_none():
        return {"error": "Group not found"}

    # 已有 video_id
    existing = await db.execute(
        select(CreativeGroupItem.video_id).where(CreativeGroupItem.group_id == group_id)
    )
    existing_ids = {r[0] for r in existing.all()}

    # 从 creatives 表查 creative_name
    name_q = select(Creative.video_id, Creative.creative_name).where(
        Creative.video_id.in_(body.video_ids),
    )
    if body.advertiser_id:
        name_q = name_q.where(Creative.advertiser_id == body.advertiser_id)
    name_result = await db.execute(name_q)
    name_map = {r.video_id: r.creative_name for r in name_result.all()}

    added = 0
    for vid in body.video_ids:
        if vid in existing_ids:
            continue
        db.add(CreativeGroupItem(
            group_id=group_id,
            advertiser_id=body.advertiser_id,
            video_id=vid,
            creative_name=name_map.get(vid),
        ))
        added += 1

    await db.commit()
    return {"added": added, "skipped": len(body.video_ids) - added}


@router.delete("/{group_id}/items/{video_id}")
async def remove_item(group_id: int, video_id: str, db: AsyncSession = Depends(get_db)):
    """移除分组内素材"""
    await db.execute(
        delete(CreativeGroupItem).where(
            CreativeGroupItem.group_id == group_id,
            CreativeGroupItem.video_id == video_id,
        )
    )
    await db.commit()
    return {"ok": True}


# ── Stats ────────────────────────────────────────────────

@router.get("/compare")
async def compare_groups(
    group_ids: str = Query(..., description="逗号分隔的分组 ID，如 1,2,3"),
    days: int = Query(7, ge=1, le=30),
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """多分组对比"""
    ids = [int(x.strip()) for x in group_ids.split(",") if x.strip().isdigit()]
    results = []
    for gid in ids:
        stats = await _calc_group_stats(db, gid, days, advertiser_id)
        results.append(stats)
    return {"days": days, "groups": results}


@router.get("/{group_id}/stats")
async def group_stats(
    group_id: int,
    days: int = Query(7, ge=1, le=30),
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """分组聚合指标"""
    return await _calc_group_stats(db, group_id, days, advertiser_id)


# ── Helpers ──────────────────────────────────────────────

async def _calc_group_stats(
    db: AsyncSession, group_id: int, days: int, advertiser_id: Optional[str]
) -> dict:
    """计算分组聚合指标"""
    # 取分组信息
    grp_result = await db.execute(select(CreativeGroup).where(CreativeGroup.id == group_id))
    group = grp_result.scalar_one_or_none()
    if not group:
        return {"group_id": group_id, "error": "Group not found"}

    # 取 video_ids
    item_q = select(CreativeGroupItem.video_id).where(CreativeGroupItem.group_id == group_id)
    if advertiser_id:
        item_q = item_q.where(CreativeGroupItem.advertiser_id == advertiser_id)
    item_result = await db.execute(item_q)
    video_ids = [r[0] for r in item_result.all()]

    if not video_ids:
        return {
            "group_id": group_id, "group_name": group.name, "color": group.color,
            "creative_count": 0,
            "total_spend": 0, "impressions": 0, "clicks": 0, "conversion": 0,
            "avg_ctr": 0, "avg_hook_rate": 0, "avg_hold_rate": 0, "avg_cpc": 0,
            "best_creative": None,
        }

    since = date.today() - timedelta(days=days)

    # 每个 video_id 每天只取最新快照（按 snapshot_time desc 取第一条）
    # 用子查询取每 (video_id, stat_date) 最大 snapshot_time 的 id
    latest_sub = (
        select(
            func.max(CreativeSnapshot.id).label("max_id")
        )
        .where(
            CreativeSnapshot.video_id.in_(video_ids),
            CreativeSnapshot.stat_date >= since,
            *([CreativeSnapshot.advertiser_id == advertiser_id] if advertiser_id else []),
        )
        .group_by(CreativeSnapshot.video_id, CreativeSnapshot.stat_date)
        .subquery()
    )

    agg = await db.execute(
        select(
            func.sum(CreativeSnapshot.spend).label("total_spend"),
            func.sum(CreativeSnapshot.impressions).label("impressions"),
            func.sum(CreativeSnapshot.clicks).label("clicks"),
            func.sum(CreativeSnapshot.conversion).label("conversion"),
            func.avg(CreativeSnapshot.ctr).label("avg_ctr"),
            func.avg(CreativeSnapshot.hook_rate).label("avg_hook_rate"),
            func.avg(CreativeSnapshot.hold_rate).label("avg_hold_rate"),
            func.avg(CreativeSnapshot.cpc).label("avg_cpc"),
        )
        .where(CreativeSnapshot.id.in_(select(latest_sub.c.max_id)))
    )
    row = agg.one()

    # best creative by spend
    best_q = await db.execute(
        select(
            CreativeSnapshot.video_id,
            func.sum(CreativeSnapshot.spend).label("s"),
        )
        .where(
            CreativeSnapshot.id.in_(select(latest_sub.c.max_id))
        )
        .group_by(CreativeSnapshot.video_id)
        .order_by(func.sum(CreativeSnapshot.spend).desc())
        .limit(1)
    )
    best_row = best_q.first()

    return {
        "group_id": group_id,
        "group_name": group.name,
        "color": group.color,
        "creative_count": len(video_ids),
        "days": days,
        "total_spend": round(float(row.total_spend or 0), 2),
        "impressions": int(row.impressions or 0),
        "clicks": int(row.clicks or 0),
        "conversion": int(row.conversion or 0),
        "avg_ctr": round(float(row.avg_ctr or 0), 2),
        "avg_hook_rate": round(float(row.avg_hook_rate or 0), 2),
        "avg_hold_rate": round(float(row.avg_hold_rate or 0), 2),
        "avg_cpc": round(float(row.avg_cpc or 0), 2),
        "best_creative": {
            "video_id": best_row.video_id,
            "spend": round(float(best_row.s or 0), 2),
        } if best_row else None,
    }


def _fmt_group(g: CreativeGroup) -> dict:
    return {
        "id": g.id,
        "advertiser_id": g.advertiser_id,
        "name": g.name,
        "description": g.description,
        "color": g.color,
        "is_active": g.is_active,
        "item_count": len(g.items) if g.items else 0,
        "created_at": str(g.created_at) if g.created_at else None,
        "updated_at": str(g.updated_at) if g.updated_at else None,
    }
