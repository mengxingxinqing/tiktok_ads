"""
创意大盘接口

GET /creative-dashboard/overview      创意流水线概览（新增/学习/跑量/停止）
GET /creative-dashboard/daily         按创建日期聚合的每日创意流水线
"""
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_

from app.core.database import get_db
from app.models.views import CreativeView

router = APIRouter(prefix="/creative-dashboard", tags=["Creative Dashboard"])


@router.get("/overview")
async def creative_overview(
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    创意流水线概览
    - total: 创意总量（不含自动选品）
    - learning: 学习中（WARM_UP，冷启动 < 3 天）
    - running: 跑量中（GROWTH + PEAK）
    - declining: 衰退中（DECAY）
    - stopped: 已停止（DEAD + FATIGUE）
    """
    conditions = [CreativeView.is_auto_selected == 0]
    if advertiser_id:
        conditions.append(CreativeView.advertiser_id == advertiser_id)

    result = await db.execute(
        select(
            func.count().label("total"),
            func.sum(case((CreativeView.stage == "WARM_UP", 1), else_=0)).label("learning"),
            func.sum(case((CreativeView.stage.in_(["GROWTH", "PEAK"]), 1), else_=0)).label("running"),
            func.sum(case((CreativeView.stage == "DECAY", 1), else_=0)).label("declining"),
            func.sum(case((CreativeView.stage.in_(["DEAD", "FATIGUE"]), 1), else_=0)).label("stopped"),
        ).where(and_(*conditions))
    )
    r = result.one()

    total = r.total or 0
    learning = r.learning or 0
    running = r.running or 0
    declining = r.declining or 0
    stopped = r.stopped or 0
    # 过审率 = (学习+跑量+衰退+停止) / 总量（GMVMax 不存在审核拒绝，所有上架的都"过审"了）
    active_ever = learning + running + declining + stopped
    pass_rate = round(active_ever / total * 100, 1) if total > 0 else 0

    return {
        "total": total,
        "learning": learning,
        "running": running,
        "declining": declining,
        "stopped": stopped,
        "pass_rate": pass_rate,
    }


@router.get("/daily")
async def creative_daily(
    advertiser_id: Optional[str] = None,
    days: int = Query(30, ge=1, le=180),
    db: AsyncSession = Depends(get_db),
):
    """
    按创意创建日期聚合的流水线数据
    每个日期：新增几个创意，当前各处于什么阶段，累计花费/订单
    """
    since = date.today() - timedelta(days=days)

    conditions = [
        CreativeView.first_seen.isnot(None),
        CreativeView.first_seen >= since,
        CreativeView.is_auto_selected == 0,
    ]
    if advertiser_id:
        conditions.append(CreativeView.advertiser_id == advertiser_id)

    result = await db.execute(
        select(
            CreativeView.first_seen.label("create_date"),
            func.count().label("new_count"),
            func.sum(case((CreativeView.stage == "WARM_UP", 1), else_=0)).label("learning"),
            func.sum(case((CreativeView.stage.in_(["GROWTH", "PEAK"]), 1), else_=0)).label("running"),
            func.sum(case((CreativeView.stage == "DECAY", 1), else_=0)).label("declining"),
            func.sum(case((CreativeView.stage.in_(["DEAD", "FATIGUE"]), 1), else_=0)).label("stopped"),
            func.sum(CreativeView.total_spend).label("total_spend"),
            func.sum(CreativeView.total_orders).label("total_orders"),
            func.sum(CreativeView.total_revenue).label("total_revenue"),
        )
        .where(and_(*conditions))
        .group_by(CreativeView.first_seen)
        .order_by(CreativeView.first_seen.desc())
    )
    rows = result.all()

    data = []
    for r in rows:
        spend = float(r.total_spend or 0)
        revenue = float(r.total_revenue or 0)
        data.append({
            "date": str(r.create_date),
            "new_count": r.new_count or 0,
            "learning": r.learning or 0,
            "running": r.running or 0,
            "declining": r.declining or 0,
            "stopped": r.stopped or 0,
            "total_spend": round(spend, 2),
            "total_orders": int(r.total_orders or 0),
            "total_revenue": round(revenue, 2),
            "roi": round(revenue / spend, 2) if spend > 0 else 0,
        })

    total_new = sum(d["new_count"] for d in data)
    total_spend = sum(d["total_spend"] for d in data)
    total_revenue = sum(d["total_revenue"] for d in data)

    return {
        "days": days,
        "summary": {
            "total_new": total_new,
            "total_spend": round(total_spend, 2),
            "total_orders": sum(d["total_orders"] for d in data),
            "total_revenue": round(total_revenue, 2),
            "roi": round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
        },
        "daily": data,
    }
