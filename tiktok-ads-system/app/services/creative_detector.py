"""
素材检测引擎
专注于：素材疲劳 / Hook Rate 衰退 / 与账户均值对比
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import date, timedelta

import numpy as np
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.creative import Creative, CreativeSnapshot, LifecycleStage
from app.models.alert import Alert


@dataclass
class CreativeDetectionResult:
    triggered: bool
    alert_type: str
    severity: str
    title: str
    message: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


class CreativeDetector:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_advertiser(self, advertiser_id: str) -> List[Alert]:
        """对账户下所有活跃素材做检测"""

        # 账户内素材均值基准（近3天，用于对比）
        benchmark = await self._get_benchmark(advertiser_id, days=3)

        # 拉取近 2 天有数据的活跃素材
        result = await self.db.execute(
            select(Creative).where(
                Creative.advertiser_id == advertiser_id,
                Creative.last_active_date >= date.today() - timedelta(days=2),
                Creative.is_fatigue == "N",  # 只看未疲劳的
            )
        )
        creatives = result.scalars().all()

        if not creatives:
            return []

        new_alerts = []
        for creative in creatives:
            # 获取近 14 天快照
            snapshots = await self._get_snapshots(creative.advertiser_id, creative.video_id, days=14)
            if not snapshots:
                continue

            detections = self._detect(creative, snapshots, benchmark)
            for d in detections:
                alert = Alert(
                    advertiser_id=advertiser_id,
                    data_level="CREATIVE",
                    object_id=creative.video_id,
                    object_name=creative.creative_name or creative.video_id,
                    alert_type=d.alert_type,
                    severity=d.severity,
                    title=d.title,
                    message=d.message,
                    metrics_snapshot=d.metrics,
                )
                self.db.add(alert)
                new_alerts.append(alert)
                logger.info(f"[Creative Alert] {d.severity} {d.alert_type}: {creative.video_id}")

        if new_alerts:
            await self.db.commit()

        return new_alerts

    # 冷启动保护期（天数内不触发疲劳/暂停类告警）
    COLD_START_PROTECT_DAYS = 7

    def _detect(
        self,
        creative: Creative,
        snapshots: List[CreativeSnapshot],
        benchmark: Dict[str, float],
    ) -> List[CreativeDetectionResult]:

        results = []
        latest = snapshots[-1]
        hook_vals  = [float(s.hook_rate  or 0) for s in snapshots]
        hold_vals  = [float(s.hold_rate  or 0) for s in snapshots]
        spend_vals = [float(s.spend      or 0) for s in snapshots]
        ctr_vals   = [float(s.ctr        or 0) for s in snapshots]

        days   = creative.days_running or len(snapshots)
        stage  = creative.lifecycle_stage

        # ======================================
        # 冷启动保护期：前 7 天数据波动属正常
        # 系统在摸人群，不触发任何疲劳/暂停告警
        # ======================================
        in_cold_start = days < self.COLD_START_PROTECT_DAYS
        if in_cold_start:
            # 冷启动期只监控严重异常：高花费但完全没有播放（素材可能加载失败）
            if latest.spend > 30 and (latest.video_play_actions or 0) == 0:
                results.append(CreativeDetectionResult(
                    triggered=True,
                    alert_type="COLD_START_NO_PLAY",
                    severity="CRITICAL",
                    title=f"冷启动异常-无播放: {creative.creative_name or creative.video_id[:12]}",
                    message=(
                        f"冷启动第 {days} 天，花费 ${latest.spend:.0f} 但播放量为 0。"
                        f"素材可能存在问题（格式/审核/加载），请立即检查。"
                    ),
                    metrics={
                        "spend": latest.spend,
                        "video_play_actions": 0,
                        "days_running": days,
                        "lifecycle_stage": "COLD_START_PROTECTED",
                    },
                    confidence=0.95,
                ))
            return results  # 冷启动期直接返回，跳过后续所有检测

        # ---- 1. 进入疲劳阶段 ----
        if stage == LifecycleStage.FATIGUE:
            results.append(CreativeDetectionResult(
                triggered=True,
                alert_type="CREATIVE_FATIGUE",
                severity="WARNING",
                title=f"素材疲劳: {creative.creative_name or creative.video_id[:12]}",
                message=(
                    f"已投放 {days} 天，Hook Rate {latest.hook_rate:.1f}% 持续下滑，"
                    f"低于健康阈值 2%。建议更换素材或暂停。"
                ),
                metrics={
                    "hook_rate": latest.hook_rate,
                    "hold_rate": latest.hold_rate,
                    "days_running": days,
                    "lifecycle_stage": stage,
                    "spend_total": sum(spend_vals),
                },
                confidence=0.9,
            ))

        # ---- 2. Hook Rate 与账户均值差距过大（冷启动保护已过）----
        bench_hook = benchmark.get("avg_hook_rate", 0)
        if bench_hook > 0 and latest.hook_rate < bench_hook * 0.5 and latest.spend > 10:
            results.append(CreativeDetectionResult(
                triggered=True,
                alert_type="HOOK_RATE_BELOW_BENCHMARK",
                severity="WARNING",
                title=f"Hook Rate 低于账户均值: {creative.video_id[:12]}",
                message=(
                    f"当前 Hook Rate {latest.hook_rate:.1f}%，"
                    f"账户均值 {bench_hook:.1f}%，"
                    f"仅为均值的 {latest.hook_rate/bench_hook*100:.0f}%。"
                ),
                metrics={
                    "hook_rate": latest.hook_rate,
                    "benchmark_hook_rate": bench_hook,
                    "ratio": latest.hook_rate / bench_hook if bench_hook > 0 else 0,
                },
                confidence=0.75,
            ))

        # ---- 3. Hook Rate 急速下滑（近5天斜率）----
        if len(hook_vals) >= 5:
            slope = self._slope(hook_vals[-5:])
            if slope < -0.3 and latest.spend > 5:  # 每天下降 0.3% 以上
                results.append(CreativeDetectionResult(
                    triggered=True,
                    alert_type="HOOK_RATE_DECLINING",
                    severity="WARNING",
                    title=f"Hook Rate 快速下滑: {creative.creative_name or creative.video_id[:12]}",
                    message=(
                        f"近5日 Hook Rate 持续下滑，斜率 {slope:.2f}/day，"
                        f"当前 {latest.hook_rate:.1f}%（初始 {hook_vals[0]:.1f}%）。"
                    ),
                    metrics={
                        "hook_rate_trend": hook_vals[-5:],
                        "slope": slope,
                        "hook_rate_latest": latest.hook_rate,
                    },
                    confidence=0.8,
                ))

        # ---- 4. 高花费低 Hook Rate（浪费预算）----
        if latest.spend > 50 and latest.hook_rate < 1.5:
            results.append(CreativeDetectionResult(
                triggered=True,
                alert_type="HIGH_SPEND_LOW_HOOK",
                severity="CRITICAL",
                title=f"高花费低 Hook Rate: {creative.video_id[:12]}",
                message=(
                    f"今日花费 ${latest.spend:.0f}，但 Hook Rate 仅 {latest.hook_rate:.1f}%，"
                    f"严重浪费预算。建议立即暂停。"
                ),
                metrics={
                    "spend": latest.spend,
                    "hook_rate": latest.hook_rate,
                    "hold_rate": latest.hold_rate,
                },
                confidence=0.92,
            ))

        return [r for r in results if r.triggered]

    @staticmethod
    def _slope(values: List[float]) -> float:
        x = np.arange(len(values), dtype=float)
        y = np.array(values, dtype=float)
        x_mean, y_mean = x.mean(), y.mean()
        denom = ((x - x_mean) ** 2).sum()
        if denom < 1e-10:
            return 0.0
        return float(((x - x_mean) * (y - y_mean)).sum() / denom)

    async def _get_snapshots(
        self,
        advertiser_id: str,
        video_id: str,
        days: int = 14,
    ) -> List[CreativeSnapshot]:
        since = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(CreativeSnapshot)
            .where(
                CreativeSnapshot.advertiser_id == advertiser_id,
                CreativeSnapshot.video_id == video_id,
                CreativeSnapshot.stat_date >= since,
            )
            .order_by(CreativeSnapshot.stat_date.asc())
        )
        all_snaps = result.scalars().all()

        # 每天取最新快照
        by_date = {}
        for s in all_snaps:
            if s.stat_date not in by_date or s.snapshot_time > by_date[s.stat_date].snapshot_time:
                by_date[s.stat_date] = s
        return sorted(by_date.values(), key=lambda x: x.stat_date)

    async def _get_benchmark(self, advertiser_id: str, days: int = 3) -> Dict[str, float]:
        """计算账户内所有素材的平均指标，作为基准线"""
        since = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(
                func.avg(CreativeSnapshot.hook_rate).label("avg_hook_rate"),
                func.avg(CreativeSnapshot.hold_rate).label("avg_hold_rate"),
                func.avg(CreativeSnapshot.ctr).label("avg_ctr"),
                func.avg(CreativeSnapshot.cost_per_conversion).label("avg_cpa"),
            ).where(
                CreativeSnapshot.advertiser_id == advertiser_id,
                CreativeSnapshot.stat_date >= since,
                CreativeSnapshot.spend > 1,  # 过滤无效数据
            )
        )
        row = result.one()
        return {
            "avg_hook_rate": float(row.avg_hook_rate or 0),
            "avg_hold_rate": float(row.avg_hold_rate or 0),
            "avg_ctr":       float(row.avg_ctr or 0),
            "avg_cpa":       float(row.avg_cpa or 0),
        }
