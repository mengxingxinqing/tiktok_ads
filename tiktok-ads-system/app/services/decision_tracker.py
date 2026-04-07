"""
决策效果追踪服务

每次执行决策时：
1. 记录决策前的数据（baseline）
2. 执行决策
3. 24小时后（或指定时间），记录决策后的数据
4. 自动计算效果对比和评分
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.models import Decision, DecisionImpact, MetricsSnapshot
from app.services.tiktok_client import TikTokClient, TikTokAPIError


class DecisionTracker:
    """追踪决策效果"""

    @staticmethod
    async def create_impact_record(
        db: AsyncSession,
        decision: Decision,
        before_data: Dict[str, Any],
    ) -> DecisionImpact:
        """
        创建决策效果记录（记录前置数据）

        Args:
            db: 数据库会话
            decision: 决策对象
            before_data: 决策前的数据 dict
                必须包含: spend, conversion, roas, impression, click, bid, status 等

        Returns:
            DecisionImpact 对象
        """
        impact = DecisionImpact(
            decision_id=decision.id,
            advertiser_id=decision.advertiser_id,
            data_level=decision.data_level,
            object_id=decision.object_id,
            object_name=decision.object_name,
            # 决策前数据
            before_spend=before_data.get("spend"),
            before_conversion=before_data.get("conversion"),
            before_impression=before_data.get("impression"),
            before_click=before_data.get("click"),
            before_ctr=before_data.get("ctr"),
            before_conversion_rate=before_data.get("conversion_rate"),
            before_roas=before_data.get("roas"),
            before_cpc=before_data.get("cpc"),
            before_cpm=before_data.get("cpm"),
            before_bid=before_data.get("bid"),
            before_budget=before_data.get("budget"),
            before_status=before_data.get("status"),
            snapshot_time_before=datetime.now(timezone.utc),
        )

        db.add(impact)
        await db.commit()
        logger.info(
            f"Created impact record for decision {decision.id}: {decision.data_level}:{decision.object_id}"
        )
        return impact

    @staticmethod
    async def update_impact_record(
        db: AsyncSession,
        impact_id: int,
        after_data: Dict[str, Any],
        decision_action: str,
    ) -> DecisionImpact:
        """
        更新决策效果记录（记录后置数据）

        Args:
            db: 数据库会话
            impact_id: DecisionImpact ID
            after_data: 决策后的数据 dict
            decision_action: 决策类型（pause, enable, increase_budget, etc）

        Returns:
            更新后的 DecisionImpact
        """
        # 查询记录
        result = await db.execute(
            select(DecisionImpact).where(DecisionImpact.id == impact_id)
        )
        impact = result.scalar_one_or_none()
        if not impact:
            raise ValueError(f"DecisionImpact {impact_id} not found")

        # 填入后置数据
        impact.after_spend = after_data.get("spend")
        impact.after_conversion = after_data.get("conversion")
        impact.after_impression = after_data.get("impression")
        impact.after_click = after_data.get("click")
        impact.after_ctr = after_data.get("ctr")
        impact.after_conversion_rate = after_data.get("conversion_rate")
        impact.after_roas = after_data.get("roas")
        impact.after_cpc = after_data.get("cpc")
        impact.after_cpm = after_data.get("cpm")
        impact.after_bid = after_data.get("bid")
        impact.after_budget = after_data.get("budget")
        impact.after_status = after_data.get("status")
        impact.snapshot_time_after = datetime.now(timezone.utc)

        # 自动计算变化量
        impact.calculate_deltas()

        # 评估效果
        impact.evaluate_effectiveness(decision_action)

        await db.commit()
        logger.info(
            f"Updated impact record {impact_id}: "
            f"delta_roas={impact.delta_roas_pct}%, "
            f"effectiveness={'✓' if impact.is_effective else '✗'}"
        )

        return impact

    @staticmethod
    async def get_impact_report(
        db: AsyncSession,
        advertiser_id: str,
        days: int = 30,
    ) -> Dict[str, Any]:
        """
        获取决策效果报告

        Args:
            db: 数据库会话
            advertiser_id: 广告主 ID
            days: 查看最近多少天的决策

        Returns:
            报告 dict
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        # 查询所有有效果数据的决策影响记录
        result = await db.execute(
            select(DecisionImpact)
            .where(
                (DecisionImpact.advertiser_id == advertiser_id)
                & (DecisionImpact.after_spend.isnot(None))  # 已采集后置数据
            )
            .order_by(DecisionImpact.created_at.desc())
        )
        impacts = result.scalars().all()

        # 统计
        total = len(impacts)
        effective = len([i for i in impacts if i.is_effective])
        ineffective = len([i for i in impacts if not i.is_effective and i.is_effective is not None])

        avg_effectiveness = (
            sum(i.effectiveness_score for i in impacts if i.effectiveness_score) / len(impacts)
            if impacts
            else 0
        )

        # 按决策类型分组统计
        by_action = {}
        for impact in impacts:
            # 从关联的决策获取 action
            decision_result = await db.execute(
                select(Decision).where(Decision.id == impact.decision_id)
            )
            decision = decision_result.scalar_one_or_none()
            if not decision:
                continue

            action = decision.action
            if action not in by_action:
                by_action[action] = {
                    "count": 0,
                    "effective": 0,
                    "avg_delta_roas_pct": 0,
                    "avg_effectiveness": 0,
                    "items": [],
                }

            by_action[action]["count"] += 1
            if impact.is_effective:
                by_action[action]["effective"] += 1

            if impact.delta_roas_pct:
                by_action[action]["avg_delta_roas_pct"] += impact.delta_roas_pct
            if impact.effectiveness_score:
                by_action[action]["avg_effectiveness"] += impact.effectiveness_score

            by_action[action]["items"].append(
                {
                    "object_id": impact.object_id,
                    "object_name": impact.object_name,
                    "before_roas": impact.before_roas,
                    "after_roas": impact.after_roas,
                    "delta_roas_pct": impact.delta_roas_pct,
                    "effectiveness_score": impact.effectiveness_score,
                    "is_effective": impact.is_effective,
                }
            )

        # 计算平均值
        for action, data in by_action.items():
            if data["count"] > 0:
                data["avg_delta_roas_pct"] /= data["count"]
                data["avg_effectiveness"] /= data["count"]
                data["effective_rate"] = f"{(data['effective'] / data['count'] * 100):.1f}%"

        return {
            "advertiser_id": advertiser_id,
            "period_days": days,
            "summary": {
                "total_impacts": total,
                "effective": effective,
                "ineffective": ineffective,
                "effective_rate": f"{(effective / total * 100):.1f}%" if total > 0 else "0%",
                "avg_effectiveness_score": round(avg_effectiveness, 2),
            },
            "by_action": by_action,
        }

    @staticmethod
    async def get_top_effective_decisions(
        db: AsyncSession,
        advertiser_id: str,
        limit: int = 10,
    ) -> list:
        """获取效果最好的决策"""
        result = await db.execute(
            select(DecisionImpact)
            .where(
                (DecisionImpact.advertiser_id == advertiser_id)
                & (DecisionImpact.effectiveness_score.isnot(None))
            )
            .order_by(DecisionImpact.effectiveness_score.desc())
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_bottom_decisions(
        db: AsyncSession,
        advertiser_id: str,
        limit: int = 10,
    ) -> list:
        """获取效果最差的决策（需要反思）"""
        result = await db.execute(
            select(DecisionImpact)
            .where(
                (DecisionImpact.advertiser_id == advertiser_id)
                & (DecisionImpact.effectiveness_score.isnot(None))
            )
            .order_by(DecisionImpact.effectiveness_score.asc())
            .limit(limit)
        )
        return result.scalars().all()
