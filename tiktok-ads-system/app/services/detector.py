"""
检测引擎 — 基于历史数据发现异常和趋势
支持：
1. 规则检测（阈值触发，参数可从数据库读取）
2. 统计异常检测（Z-score / 3σ）
3. 趋势检测（线性回归斜率）
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import date, timedelta

import numpy as np
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metrics import MetricsSnapshot
from app.models.alert import Alert
from app.models.rule import AlertRule, DEFAULT_RULES


# ===================== 数据结构 =====================

@dataclass
class DetectionResult:
    """单条检测结果"""
    triggered: bool
    alert_type: str
    severity: str           # INFO / WARNING / CRITICAL
    title: str
    message: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass
class ObjectContext:
    """某个广告对象的历史指标序列"""
    advertiser_id: str
    data_level: str
    object_id: str
    object_name: str
    snapshots: List[MetricsSnapshot]  # 按时间升序

    def values(self, field: str) -> List[float]:
        return [float(getattr(s, field) or 0) for s in self.snapshots]

    def latest(self, field: str) -> float:
        if not self.snapshots:
            return 0.0
        return float(getattr(self.snapshots[-1], field) or 0)

    def avg(self, field: str, days: int = 7) -> float:
        vals = self.values(field)[-days:]
        return float(np.mean(vals)) if vals else 0.0


# ===================== 规则检测 =====================

def _get_rule_params(rule_params_map: Dict[str, Dict], rule_key: str) -> Dict[str, Any]:
    """从规则参数映射中获取参数，fallback 到 DEFAULT_RULES 中的默认值"""
    if rule_key in rule_params_map:
        return rule_params_map[rule_key]
    for r in DEFAULT_RULES:
        if r["rule_key"] == rule_key:
            return r.get("params", {})
    return {}


class RuleEngine:
    """可配置规则引擎（参数从数据库读取，fallback 到默认值）"""

    @classmethod
    def check(cls, ctx: ObjectContext, rule_params_map: Optional[Dict[str, Dict]] = None) -> List[DetectionResult]:
        if rule_params_map is None:
            rule_params_map = {}

        results = []

        latest_spend = ctx.latest("spend")
        latest_ctr = ctx.latest("ctr")
        latest_cvr = ctx.latest("conversion_rate")
        latest_cpm = ctx.latest("cpm")
        avg_cpm = ctx.avg("cpm", days=7)

        # 从规则参数映射读取阈值
        ctr_params = _get_rule_params(rule_params_map, "AD_CTR_LOW")
        ctr_threshold = float(ctr_params.get("threshold", 0.5))

        zero_spend_params = _get_rule_params(rule_params_map, "AD_ZERO_SPEND")
        min_avg_spend = float(zero_spend_params.get("min_avg_spend", 10.0))

        cpm_params = _get_rule_params(rule_params_map, "AD_CPM_HIGH")
        cpm_multiplier = float(cpm_params.get("multiplier", 2.0))

        # 1. 有花费才做 CTR/CVR 检测（避免未开跑的广告误报）
        if latest_spend > 0:
            if latest_ctr < ctr_threshold:
                results.append(DetectionResult(
                    triggered=True,
                    alert_type="CTR_LOW",
                    severity="WARNING",
                    title=f"CTR 偏低: {ctx.object_name or ctx.object_id}",
                    message=f"CTR {latest_ctr:.2f}%，低于阈值 {ctr_threshold}%",
                    metrics={"ctr": latest_ctr, "spend": latest_spend},
                ))

            if latest_cvr < 0.3:
                results.append(DetectionResult(
                    triggered=True,
                    alert_type="CVR_LOW",
                    severity="WARNING",
                    title=f"转化率偏低: {ctx.object_name or ctx.object_id}",
                    message=f"转化率 {latest_cvr:.2f}%，低于阈值 0.3%",
                    metrics={"conversion_rate": latest_cvr, "spend": latest_spend},
                ))

            # CPM 飙升（有历史均值才比）
            if avg_cpm > 0 and latest_cpm > avg_cpm * cpm_multiplier:
                results.append(DetectionResult(
                    triggered=True,
                    alert_type="CPM_SPIKE",
                    severity="WARNING",
                    title=f"CPM 异常飙升: {ctx.object_name or ctx.object_id}",
                    message=f"CPM {latest_cpm:.2f}，是7日均值 {avg_cpm:.2f} 的 {latest_cpm/avg_cpm:.1f}x",
                    metrics={"cpm": latest_cpm, "avg_cpm_7d": avg_cpm},
                ))

        # 2. 有历史数据但今日花费为 0（可能被暂停/余额不足）
        if ctx.avg("spend", days=3) > min_avg_spend and latest_spend == 0:
            results.append(DetectionResult(
                triggered=True,
                alert_type="SPEND_STOPPED",
                severity="CRITICAL",
                title=f"投放停止: {ctx.object_name or ctx.object_id}",
                message=f"近3日平均花费 {ctx.avg('spend', 3):.2f}，但今日花费为 0",
                metrics={"spend_today": 0, "spend_avg_3d": ctx.avg("spend", 3)},
            ))

        return [r for r in results if r.triggered]


# ===================== GMVMax 专属告警检测 =====================

class GMVMaxDetector:
    """
    GMVMax 专属告警规则
    检测 data_level='GMVMAX_CAMPAIGN' 的数据
    参数可从数据库读取，fallback 到默认值
    """

    @classmethod
    def check(cls, ctx: ObjectContext, rule_params_map: Optional[Dict[str, Dict]] = None) -> List[DetectionResult]:
        if ctx.data_level != "GMVMAX_CAMPAIGN":
            return []

        if rule_params_map is None:
            rule_params_map = {}

        results = []
        latest_spend = ctx.latest("spend")
        latest_roi = ctx.latest("roi")
        latest_gmv = ctx.latest("gross_revenue")

        avg_roi_7d = ctx.avg("roi", days=7)
        avg_gmv_7d = ctx.avg("gross_revenue", days=7)

        # 取昨日花费（倒数第二条，若存在）
        spend_vals = ctx.values("spend")
        yesterday_spend = spend_vals[-2] if len(spend_vals) >= 2 else 0.0

        # 从数据库规则读取参数
        roi_critical_params = _get_rule_params(rule_params_map, "GMVMAX_ROI_CRITICAL")
        min_roi = float(roi_critical_params.get("min_roi", 1.0))
        roi_critical_min_spend = float(roi_critical_params.get("min_spend", 5.0))

        roi_drop_params = _get_rule_params(rule_params_map, "GMVMAX_ROI_DROP")
        drop_pct = float(roi_drop_params.get("drop_pct", 30)) / 100.0
        lookback_days_roi = int(roi_drop_params.get("lookback_days", 7))
        roi_drop_min_spend = float(roi_drop_params.get("min_spend", 10.0))

        zero_gmv_params = _get_rule_params(rule_params_map, "GMVMAX_ZERO_GMV")
        zero_gmv_min_spend = float(zero_gmv_params.get("min_spend", 20.0))

        budget_burn_params = _get_rule_params(rule_params_map, "GMVMAX_BUDGET_BURN")
        burn_surge_pct = float(budget_burn_params.get("surge_pct", 200)) / 100.0  # e.g. 200% → multiplier 3x

        gmv_surge_params = _get_rule_params(rule_params_map, "GMVMAX_GMV_SURGE")
        gmv_surge_pct = float(gmv_surge_params.get("surge_pct", 150)) / 100.0
        lookback_days_gmv = int(gmv_surge_params.get("lookback_days", 7))

        # 使用可配置的 lookback 天数重新计算均值
        avg_roi = ctx.avg("roi", days=lookback_days_roi)
        avg_gmv = ctx.avg("gross_revenue", days=lookback_days_gmv)

        # 1. ROI_DROP — 今日 ROI vs N日均值下降超过 drop_pct
        if avg_roi > 0 and latest_spend >= roi_drop_min_spend:
            roi_drop_rate = (avg_roi - latest_roi) / avg_roi
            if roi_drop_rate > drop_pct:
                results.append(DetectionResult(
                    triggered=True,
                    alert_type="ROI_DROP",
                    severity="WARNING",
                    title=f"GMVMax ROI 下滑: {ctx.object_name or ctx.object_id}",
                    message=(
                        f"今日 ROI {latest_roi:.2f}，较{lookback_days_roi}日均值 {avg_roi:.2f} "
                        f"下降 {roi_drop_rate*100:.1f}%（阈值 {drop_pct*100:.0f}%）"
                    ),
                    metrics={"roi_today": latest_roi, f"roi_avg_{lookback_days_roi}d": avg_roi, "drop_rate": roi_drop_rate},
                ))

        # 2. ROI_CRITICAL — GMVMax ROI < min_roi（亏本）
        if latest_spend >= roi_critical_min_spend and latest_roi < min_roi:
            results.append(DetectionResult(
                triggered=True,
                alert_type="ROI_CRITICAL",
                severity="CRITICAL",
                title=f"GMVMax ROI 亏本: {ctx.object_name or ctx.object_id}",
                message=f"今日 ROI {latest_roi:.2f} < {min_roi}，广告花费高于 GMV 收入，正在亏损",
                metrics={"roi_today": latest_roi, "spend": latest_spend, "gmv": latest_gmv},
            ))

        # 3. ZERO_GMV — 花费超过阈值但 gross_revenue = 0
        if latest_spend > zero_gmv_min_spend and latest_gmv == 0:
            results.append(DetectionResult(
                triggered=True,
                alert_type="ZERO_GMV",
                severity="CRITICAL",
                title=f"GMVMax 零收入: {ctx.object_name or ctx.object_id}",
                message=f"今日花费 ${latest_spend:.2f} 但 GMV 收入为 0，请检查 Shop 商品状态和转化链路",
                metrics={"spend": latest_spend, "gmv": 0},
            ))

        # 4. GMV_SURGE — 今日 GMV 超过 N 日均值 surge_pct%（好事，提示关注）
        if avg_gmv > 0 and latest_gmv > avg_gmv * (1 + gmv_surge_pct):
            surge_rate = (latest_gmv - avg_gmv) / avg_gmv
            results.append(DetectionResult(
                triggered=True,
                alert_type="GMV_SURGE",
                severity="INFO",
                title=f"GMVMax GMV 大幅增长: {ctx.object_name or ctx.object_id}",
                message=(
                    f"今日 GMV ${latest_gmv:.2f}，超过{lookback_days_gmv}日均值 ${avg_gmv:.2f} "
                    f"的 {surge_rate*100:.1f}%，表现优异！"
                ),
                metrics={"gmv_today": latest_gmv, f"gmv_avg_{lookback_days_gmv}d": avg_gmv, "surge_rate": surge_rate},
            ))

        # 5. BUDGET_BURN — 今日花费超过昨日 (1+burn_surge_pct)x
        burn_multiplier = 1 + burn_surge_pct
        if yesterday_spend > 0 and latest_spend > yesterday_spend * burn_multiplier:
            burn_rate = latest_spend / yesterday_spend
            results.append(DetectionResult(
                triggered=True,
                alert_type="BUDGET_BURN",
                severity="WARNING",
                title=f"GMVMax 花费暴增: {ctx.object_name or ctx.object_id}",
                message=(
                    f"今日花费 ${latest_spend:.2f}，是昨日 ${yesterday_spend:.2f} 的 {burn_rate:.1f}x"
                    f"（阈值 {burn_multiplier:.0f}x），请检查预算设置"
                ),
                metrics={"spend_today": latest_spend, "spend_yesterday": yesterday_spend, "burn_rate": burn_rate},
            ))

        return [r for r in results if r.triggered]


# ===================== 统计异常检测 =====================

class AnomalyDetector:
    """Z-score 异常检测（3σ 原则）"""

    @staticmethod
    def zscore_detect(ctx: ObjectContext, field: str, window: int = 14) -> Optional[DetectionResult]:
        vals = ctx.values(field)
        if len(vals) < 7:  # 数据太少不检测
            return None

        history = vals[-window-1:-1]  # 历史窗口（不含最新）
        latest = vals[-1]

        if len(history) < 4:
            return None

        mean = float(np.mean(history))
        std = float(np.std(history))

        if std < 1e-6:  # 数据无波动
            return None

        z = (latest - mean) / std

        if abs(z) > 3.0:
            direction = "暴增" if z > 0 else "骤降"
            severity = "CRITICAL" if abs(z) > 4 else "WARNING"
            return DetectionResult(
                triggered=True,
                alert_type=f"{field.upper()}_ANOMALY",
                severity=severity,
                title=f"{field} 异常{direction}: {ctx.object_name or ctx.object_id}",
                message=f"{field} 当前值 {latest:.2f}，历史均值 {mean:.2f}，偏差 {z:.1f}σ",
                metrics={field: latest, f"{field}_mean": mean, f"{field}_std": std, "zscore": z},
                confidence=min(1.0, abs(z) / 5.0),
            )
        return None

    @classmethod
    def check(cls, ctx: ObjectContext) -> List[DetectionResult]:
        results = []
        # 对核心指标做异常检测
        for field in ["spend", "ctr", "conversion", "cpm"]:
            result = cls.zscore_detect(ctx, field)
            if result:
                results.append(result)
        return results


# ===================== 趋势检测 =====================

class TrendDetector:
    """线性回归趋势检测"""

    @staticmethod
    def slope(values: List[float]) -> float:
        """计算序列斜率（正=上升，负=下降）"""
        if len(values) < 3:
            return 0.0
        x = np.arange(len(values), dtype=float)
        y = np.array(values, dtype=float)
        # 简单线性回归
        x_mean, y_mean = x.mean(), y.mean()
        denom = ((x - x_mean) ** 2).sum()
        if denom < 1e-10:
            return 0.0
        return float(((x - x_mean) * (y - y_mean)).sum() / denom)

    @classmethod
    def check(cls, ctx: ObjectContext) -> List[DetectionResult]:
        results = []

        # 检测 CTR 连续下降趋势（近 5 天）
        ctr_vals = ctx.values("ctr")[-5:]
        if len(ctr_vals) >= 4 and ctx.latest("spend") > 0:
            s = cls.slope(ctr_vals)
            if s < -0.05:  # 每天下降超过 0.05 个百分点
                results.append(DetectionResult(
                    triggered=True,
                    alert_type="CTR_DECLINING",
                    severity="WARNING",
                    title=f"CTR 持续下降趋势: {ctx.object_name or ctx.object_id}",
                    message=f"近5日 CTR 持续下降，斜率 {s:.3f}/day，当前 {ctx.latest('ctr'):.2f}%。素材可能疲劳。",
                    metrics={"ctr_trend_slope": s, "ctr_recent": ctr_vals, "ctr_latest": ctx.latest("ctr")},
                    confidence=0.7,
                ))

        # 检测花费下降趋势
        spend_vals = ctx.values("spend")[-5:]
        if len(spend_vals) >= 4 and ctx.avg("spend", 5) > 20:
            s = cls.slope(spend_vals)
            if s < -5:  # 每天花费减少超过 5
                results.append(DetectionResult(
                    triggered=True,
                    alert_type="SPEND_DECLINING",
                    severity="INFO",
                    title=f"花费持续减少: {ctx.object_name or ctx.object_id}",
                    message=f"近5日花费持续下降，斜率 {s:.1f}/day，当前 {ctx.latest('spend'):.2f}",
                    metrics={"spend_trend_slope": s, "spend_latest": ctx.latest("spend")},
                    confidence=0.6,
                ))

        return results


# ===================== 主检测器 =====================

class DetectionEngine:
    """
    综合检测器：整合规则 + 统计 + 趋势
    规则参数从数据库 alert_rules 表加载，fallback 到 DEFAULT_RULES
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self._rule_params_map: Optional[Dict[str, Dict]] = None

    async def _load_rule_params(self) -> Dict[str, Dict]:
        """从数据库加载启用的规则参数，缓存在实例上"""
        if self._rule_params_map is not None:
            return self._rule_params_map

        result = await self.db.execute(
            select(AlertRule).where(AlertRule.is_enabled == True)
        )
        rules = result.scalars().all()
        self._rule_params_map = {r.rule_key: (r.params or {}) for r in rules}
        return self._rule_params_map

    async def load_context(
        self,
        advertiser_id: str,
        data_level: str,
        object_id: str,
        days: int = 14,
    ) -> Optional[ObjectContext]:
        """从数据库加载历史指标"""
        since = date.today() - timedelta(days=days)
        result = await self.db.execute(
            select(MetricsSnapshot)
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level == data_level,
                MetricsSnapshot.object_id == object_id,
                MetricsSnapshot.stat_date >= since,
            )
            .order_by(MetricsSnapshot.stat_date.asc(), MetricsSnapshot.snapshot_time.asc())
        )
        snapshots = result.scalars().all()

        if not snapshots:
            return None

        # 每天取最新的一条快照（避免同一天多次采集导致重复）
        by_date: Dict[date, MetricsSnapshot] = {}
        for s in snapshots:
            if s.stat_date not in by_date or s.snapshot_time > by_date[s.stat_date].snapshot_time:
                by_date[s.stat_date] = s
        daily_snapshots = sorted(by_date.values(), key=lambda x: x.stat_date)

        return ObjectContext(
            advertiser_id=advertiser_id,
            data_level=data_level,
            object_id=object_id,
            object_name=daily_snapshots[-1].object_name or "",
            snapshots=daily_snapshots,
        )

    async def detect_object(
        self,
        advertiser_id: str,
        data_level: str,
        object_id: str,
    ) -> List[DetectionResult]:
        """对单个广告对象跑全套检测"""
        ctx = await self.load_context(advertiser_id, data_level, object_id)
        if not ctx or not ctx.snapshots:
            return []

        rule_params_map = await self._load_rule_params()

        results = []
        results.extend(RuleEngine.check(ctx, rule_params_map))
        results.extend(AnomalyDetector.check(ctx))
        results.extend(TrendDetector.check(ctx))
        results.extend(GMVMaxDetector.check(ctx, rule_params_map))
        return results

    async def detect_advertiser(self, advertiser_id: str) -> List[Alert]:
        """对整个广告账户的所有 Ad + GMVMax Campaign 跑检测，生成告警"""
        # 查出最近有数据的所有对象（AD + GMVMAX_CAMPAIGN）
        result = await self.db.execute(
            select(
                MetricsSnapshot.object_id,
                MetricsSnapshot.object_name,
                MetricsSnapshot.data_level,
            )
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
                MetricsSnapshot.stat_date >= date.today() - timedelta(days=1),
            )
            .distinct()
        )
        objects = result.all()

        if not objects:
            logger.debug(f"No recent ad/gmvmax data for {advertiser_id}")
            return []

        new_alerts = []
        for obj_id, obj_name, data_level in objects:
            detections = await self.detect_object(advertiser_id, data_level, obj_id)
            for d in detections:
                alert = Alert(
                    advertiser_id=advertiser_id,
                    data_level="AD",
                    object_id=obj_id,
                    object_name=obj_name,
                    alert_type=d.alert_type,
                    severity=d.severity,
                    title=d.title,
                    message=d.message,
                    metrics_snapshot=d.metrics,
                )
                self.db.add(alert)
                new_alerts.append(alert)
                logger.info(f"[ALERT] {d.severity} {d.alert_type}: {obj_id} - {d.title}")

        if new_alerts:
            await self.db.commit()

        return new_alerts
