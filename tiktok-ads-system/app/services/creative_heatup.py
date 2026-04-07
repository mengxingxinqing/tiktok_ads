"""
素材加热管理服务

支持：
1. 记录加热前数据
2. 执行加热操作
3. 采集加热后数据
4. 自动评估加热效果
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.models import CreativeHeatUp, Creative, CreativeSnapshot


class CreativeHeatupManager:
    """素材加热管理"""

    @staticmethod
    async def start_heatup(
        db: AsyncSession,
        advertiser_id: str,
        video_id: str,
        heatup_type: str,  # INCREASE_BUDGET / NEW_AD / RAISE_BID / CLONE_AD
        reason: str,
        params: str,
        before_data: Dict[str, Any],
    ) -> CreativeHeatUp:
        """
        开始素材加热操作

        Args:
            db: 数据库会话
            advertiser_id: 广告账户 ID
            video_id: 素材 ID
            heatup_type: 加热类型
            reason: 加热原因
            params: 加热参数
            before_data: 加热前的数据快照

        Returns:
            CreativeHeatUp 对象
        """
        # 查询或创建 Creative 记录
        result = await db.execute(
            select(Creative).where(
                (Creative.advertiser_id == advertiser_id)
                & (Creative.video_id == video_id)
            )
        )
        creative = result.scalar_one_or_none()

        heatup = CreativeHeatUp(
            advertiser_id=advertiser_id,
            video_id=video_id,
            creative_id=creative.id if creative else None,
            heatup_type=heatup_type,
            heatup_reason=reason,
            heatup_params=params,
            # 加热前数据
            before_daily_spend=before_data.get("daily_spend"),
            before_ctr=before_data.get("ctr"),
            before_conversion=before_data.get("conversion"),
            before_roas=before_data.get("roas"),
            before_hook_rate=before_data.get("hook_rate"),
            before_hold_rate=before_data.get("hold_rate"),
            before_bid=before_data.get("bid"),
            before_budget=before_data.get("budget"),
            before_lifecycle=before_data.get("lifecycle"),
            snapshot_before=datetime.now(timezone.utc),
        )

        db.add(heatup)
        await db.commit()

        logger.info(
            f"Started heatup for {video_id} ({heatup_type}): {reason}"
        )

        return heatup

    @staticmethod
    async def complete_heatup(
        db: AsyncSession,
        heatup_id: int,
        after_data: Dict[str, Any],
    ) -> CreativeHeatUp:
        """
        完成素材加热效果采集

        Args:
            db: 数据库会话
            heatup_id: CreativeHeatUp ID
            after_data: 加热后的数据快照

        Returns:
            更新后的 CreativeHeatUp
        """
        result = await db.execute(
            select(CreativeHeatUp).where(CreativeHeatUp.id == heatup_id)
        )
        heatup = result.scalar_one_or_none()
        if not heatup:
            raise ValueError(f"CreativeHeatUp {heatup_id} not found")

        # 填入加热后数据
        heatup.after_daily_spend = after_data.get("daily_spend")
        heatup.after_ctr = after_data.get("ctr")
        heatup.after_conversion = after_data.get("conversion")
        heatup.after_roas = after_data.get("roas")
        heatup.after_hook_rate = after_data.get("hook_rate")
        heatup.after_hold_rate = after_data.get("hold_rate")
        heatup.after_bid = after_data.get("bid")
        heatup.after_budget = after_data.get("budget")
        heatup.after_lifecycle = after_data.get("lifecycle")
        heatup.snapshot_after = datetime.now(timezone.utc)

        # 自动计算效果指标
        heatup.calculate_deltas()

        # 评估加热是否成功
        heatup.evaluate_success()

        await db.commit()

        logger.info(
            f"Completed heatup {heatup_id}: "
            f"success={'✓' if heatup.is_successful == 'Y' else '✗'}, "
            f"score={heatup.success_score:.2f}"
        )

        return heatup

    @staticmethod
    async def get_heatup_report(
        db: AsyncSession,
        advertiser_id: str,
        days: int = 30,
    ) -> Dict[str, Any]:
        """
        获取加热操作报告

        Args:
            db: 数据库会话
            advertiser_id: 广告账户 ID
            days: 查看最近多少天的加热记录

        Returns:
            报告 dict
        """
        from datetime import timedelta

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        # 查询加热记录
        result = await db.execute(
            select(CreativeHeatUp)
            .where(
                (CreativeHeatUp.advertiser_id == advertiser_id)
                & (CreativeHeatUp.after_daily_spend.isnot(None))  # 已采集后置数据
            )
            .order_by(CreativeHeatUp.created_at.desc())
        )
        heatups = result.scalars().all()

        # 统计
        total = len(heatups)
        successful = len([h for h in heatups if h.is_successful == "Y"])
        failed = len([h for h in heatups if h.is_successful == "N"])

        avg_score = sum(h.success_score for h in heatups if h.success_score) / len(heatups) if heatups else 0

        # 按加热类型分组
        by_type = {}
        for heatup in heatups:
            htype = heatup.heatup_type
            if htype not in by_type:
                by_type[htype] = {
                    "count": 0,
                    "successful": 0,
                    "avg_score": 0,
                    "avg_delta_conversion": 0,
                    "items": [],
                }

            by_type[htype]["count"] += 1
            if heatup.is_successful == "Y":
                by_type[htype]["successful"] += 1

            if heatup.success_score:
                by_type[htype]["avg_score"] += heatup.success_score
            if heatup.delta_conversion:
                by_type[htype]["avg_delta_conversion"] += heatup.delta_conversion

            by_type[htype]["items"].append(
                {
                    "video_id": heatup.video_id,
                    "heatup_type": heatup.heatup_type,
                    "before_roas": heatup.before_roas,
                    "after_roas": heatup.after_roas,
                    "delta_conversion": heatup.delta_conversion,
                    "success_score": heatup.success_score,
                    "is_successful": heatup.is_successful == "Y",
                }
            )

        # 计算平均值
        for htype, data in by_type.items():
            if data["count"] > 0:
                data["avg_score"] /= data["count"]
                data["avg_delta_conversion"] /= data["count"]
                data["success_rate"] = f"{(data['successful'] / data['count'] * 100):.1f}%"

        return {
            "advertiser_id": advertiser_id,
            "period_days": days,
            "summary": {
                "total_heatups": total,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful / total * 100):.1f}%" if total > 0 else "0%",
                "avg_score": round(avg_score, 2),
            },
            "by_type": by_type,
        }

    @staticmethod
    async def get_top_heatups(
        db: AsyncSession,
        advertiser_id: str,
        limit: int = 10,
    ) -> list:
        """获取最成功的加热操作"""
        result = await db.execute(
            select(CreativeHeatUp)
            .where(
                (CreativeHeatUp.advertiser_id == advertiser_id)
                & (CreativeHeatUp.success_score.isnot(None))
            )
            .order_by(CreativeHeatUp.success_score.desc())
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_failed_heatups(
        db: AsyncSession,
        advertiser_id: str,
        limit: int = 10,
    ) -> list:
        """获取失败的加热操作（需要反思）"""
        result = await db.execute(
            select(CreativeHeatUp)
            .where(
                (CreativeHeatUp.advertiser_id == advertiser_id)
                & (CreativeHeatUp.is_successful == "N")
            )
            .order_by(CreativeHeatUp.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
