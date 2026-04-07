"""
分析服务 — 账户大盘、风险评分、预测等
"""
import asyncio
from datetime import datetime, timedelta, timezone, date
from typing import Optional, Dict, Any, List

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.advertiser import Advertiser
from app.models.metrics import MetricsSnapshot
from app.models.product import ProductCost
from app.models.analytics import (
    AccountSnapshot, DailyReport, RiskAlert, HourlyMetrics, GrowthRecommendation
)


class AnalyticsService:
    """账户数据分析"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_account_snapshot(self, advertiser_id: str) -> Optional[AccountSnapshot]:
        """
        生成账户快照 — 聚合最近一小时的数据
        """
        now = datetime.now(timezone.utc)
        hour_ago = now - timedelta(hours=1)

        # 1. 聚合最近 1 小时的指标
        metrics_q = (
            select(
                func.sum(MetricsSnapshot.spend).label("total_spend"),
                func.sum(MetricsSnapshot.conversion).label("total_orders"),
                func.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
                func.avg(MetricsSnapshot.cpc).label("avg_cpc"),
                func.avg(MetricsSnapshot.ctr).label("avg_ctr"),
                func.count(MetricsSnapshot.campaign_id.distinct()).label("active_campaigns"),
                func.count(MetricsSnapshot.adgroup_id.distinct()).label("active_adgroups"),
            )
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
                MetricsSnapshot.snapshot_time >= hour_ago,
                MetricsSnapshot.snapshot_time <= now,
            )
        )
        metrics_result = await self.db.execute(metrics_q)
        metrics_row = metrics_result.one()

        total_spend = float(metrics_row.total_spend or 0)
        total_orders = int(metrics_row.total_orders or 0)
        total_revenue = float(metrics_row.total_revenue or 0)

        # 2. 拉取成本配置，计算真实利润
        real_profit = 0.0
        real_margin = 0.0
        roas = 0.0

        # 优先使用 GMVMax 真实收入
        if total_revenue > 0:
            gmv = total_revenue
            roas = gmv / total_spend if total_spend > 0 else 0
        elif total_orders > 0:
            avg_price_q = select(func.avg(ProductCost.selling_price)).where(
                ProductCost.advertiser_id == advertiser_id,
                ProductCost.is_active == True,
            )
            avg_price_result = await self.db.execute(avg_price_q)
            avg_price = avg_price_result.scalar() or 0
            gmv = avg_price * total_orders
            roas = gmv / total_spend if total_spend > 0 else 0
        else:
            gmv = 0

        if total_orders > 0:

            # 计算利润（简化版，实际应该按商品匹配）
            cost_q = select(
                func.avg(ProductCost.product_cost).label("avg_product_cost"),
                func.avg(ProductCost.freight_inbound).label("avg_inbound"),
                func.avg(ProductCost.freight_outbound).label("avg_outbound"),
                func.avg(ProductCost.affiliate_rate).label("avg_affiliate"),
                func.avg(ProductCost.platform_fee_rate).label("avg_platform"),
            ).where(ProductCost.advertiser_id == advertiser_id, ProductCost.is_active == True)
            cost_result = await self.db.execute(cost_q)
            cost_row = cost_result.one()

            fixed_cost = (
                float(cost_row.avg_product_cost or 0)
                + float(cost_row.avg_inbound or 0)
                + float(cost_row.avg_outbound or 0)
            ) * total_orders
            var_rate = (
                float(cost_row.avg_affiliate or 0) + float(cost_row.avg_platform or 5)
            ) / 100
            var_cost = gmv * var_rate
            real_profit = gmv - fixed_cost - var_cost - total_spend
            real_margin = (real_profit / gmv * 100) if gmv > 0 else 0
        else:
            gmv = 0.0

        # 3. 生命周期分布
        lifecycle_q = (
            select(
                func.count(MetricsSnapshot.video_id).filter(
                    MetricsSnapshot.snapshot_time >= hour_ago
                ).label("peak_count"),
            )
            .where(MetricsSnapshot.advertiser_id == advertiser_id)
        )

        # 4. 计算健康分数和风险等级
        health_score = self._calculate_health_score(
            roas=roas,
            real_profit=real_profit,
            orders=total_orders,
        )
        risk_level = self._assess_risk_level(health_score)

        # 5. 创建快照
        snapshot = AccountSnapshot(
            advertiser_id=advertiser_id,
            snapshot_time=now,
            stat_date=now.date(),
            spend=round(total_spend, 2),
            gmv=round(gmv, 2),
            orders=total_orders,
            roas=round(roas, 2),
            real_profit=round(real_profit, 2),
            real_margin=round(real_margin, 2),
            active_videos=0,
            active_campaigns=int(metrics_row.active_campaigns or 0),
            active_adgroups=int(metrics_row.active_adgroups or 0),
            avg_ctr=float(metrics_row.avg_ctr or 0),
            avg_cpc=float(metrics_row.avg_cpc or 0),
            health_score=health_score,
            risk_level=risk_level,
        )

        self.db.add(snapshot)
        logger.info(f"Generated snapshot for {advertiser_id}: spend=${total_spend}, ROI={roas:.2f}x")
        return snapshot

    def _calculate_health_score(self, roas: float, real_profit: float, orders: int) -> int:
        """
        计算账户健康度 (0-100)
        
        规则：
        - ROAS vs 保本线（假设 4.5x）
        - 利润是否为正
        - 订单量趋势
        """
        score = 50  # 基础分

        # ROAS 分数
        break_even = 4.5
        if roas >= break_even * 1.2:
            score += 25  # 很好
        elif roas >= break_even:
            score += 15  # 还好
        elif roas >= break_even * 0.9:
            score -= 10  # 接近亏损
        else:
            score -= 25  # 亏损

        # 利润分数
        if real_profit > 0:
            score += 10
        else:
            score -= 15

        # 订单量
        if orders > 100:
            score += 5
        elif orders < 10:
            score -= 10

        return max(0, min(100, score))

    def _assess_risk_level(self, health_score: int) -> str:
        """根据健康分数判断风险等级"""
        if health_score >= 70:
            return "low"
        elif health_score >= 50:
            return "medium"
        elif health_score >= 30:
            return "high"
        else:
            return "critical"

    async def get_account_overview(self, advertiser_id: str) -> Dict[str, Any]:
        """
        获取账户大盘信息
        
        返回：
        - 今日数据（目前）
        - 与昨日对比
        - 与上周同期对比
        - 目标进度
        - 预测今日
        """
        today = date.today()
        now = datetime.now(timezone.utc)

        # 1. 拉最新快照
        latest_q = (
            select(AccountSnapshot)
            .where(
                AccountSnapshot.advertiser_id == advertiser_id,
                AccountSnapshot.stat_date == today,
            )
            .order_by(AccountSnapshot.snapshot_time.desc())
            .limit(1)
        )
        latest_result = await self.db.execute(latest_q)
        latest_snapshot = latest_result.scalar_one_or_none()

        if not latest_snapshot:
            # 如果今天还没有快照，即时计算
            latest_snapshot = await self.generate_account_snapshot(advertiser_id)
            await self.db.commit()

        # 2. 拉昨日快照
        yesterday = today - timedelta(days=1)
        yesterday_q = (
            select(AccountSnapshot)
            .where(
                AccountSnapshot.advertiser_id == advertiser_id,
                AccountSnapshot.stat_date == yesterday,
            )
            .order_by(AccountSnapshot.snapshot_time.desc())
            .limit(1)
        )
        yesterday_result = await self.db.execute(yesterday_q)
        yesterday_snapshot = yesterday_result.scalar_one_or_none()

        # 3. 拉上周同期
        last_week = today - timedelta(days=7)
        last_week_q = (
            select(AccountSnapshot)
            .where(
                AccountSnapshot.advertiser_id == advertiser_id,
                AccountSnapshot.stat_date == last_week,
            )
            .order_by(AccountSnapshot.snapshot_time.desc())
            .limit(1)
        )
        last_week_result = await self.db.execute(last_week_q)
        last_week_snapshot = last_week_result.scalar_one_or_none()

        # 4. 计算对比
        vs_yesterday_gmv = self._calculate_change_pct(
            yesterday_snapshot.gmv if yesterday_snapshot else 0,
            latest_snapshot.gmv,
        )
        vs_last_week_gmv = self._calculate_change_pct(
            last_week_snapshot.gmv if last_week_snapshot else 0,
            latest_snapshot.gmv,
        )

        return {
            "current": {
                "time": latest_snapshot.snapshot_time.isoformat(),
                "spend": latest_snapshot.spend,
                "gmv": latest_snapshot.gmv,
                "orders": latest_snapshot.orders,
                "roas": latest_snapshot.roas,
                "real_profit": latest_snapshot.real_profit,
                "real_margin": latest_snapshot.real_margin,
                "active_videos": latest_snapshot.active_videos,
                "health_score": latest_snapshot.health_score,
                "risk_level": latest_snapshot.risk_level,
            },
            "comparison": {
                "vs_yesterday": {
                    "gmv_pct": vs_yesterday_gmv,
                    "roas_pct": self._calculate_change_pct(
                        yesterday_snapshot.roas if yesterday_snapshot else 0,
                        latest_snapshot.roas,
                    ),
                },
                "vs_last_week": {
                    "gmv_pct": vs_last_week_gmv,
                    "roas_pct": self._calculate_change_pct(
                        last_week_snapshot.roas if last_week_snapshot else 0,
                        latest_snapshot.roas,
                    ),
                },
            },
            "forecast": {
                "note": "Based on current pace",
                "estimated_daily_spend": latest_snapshot.spend * 24,
                "estimated_daily_gmv": latest_snapshot.gmv * 24,
                "estimated_daily_profit": latest_snapshot.real_profit * 24,
            },
        }

    @staticmethod
    def _calculate_change_pct(old_value: float, new_value: float) -> float:
        """计算百分比变化"""
        if old_value == 0:
            return 0.0 if new_value == 0 else 100.0
        return round((new_value - old_value) / old_value * 100, 2)

    async def detect_risk_alerts(self, advertiser_id: str) -> List[RiskAlert]:
        """
        实时风险检测 — 5 种告警类型
        1. CMO 快速下跌（Level 1）
        2. ROI 跌破保本线（Level 2）
        3. Hook Rate 崩盘（Level 2）
        4. 预算快速烧完（Level 1）
        5. 多个素材同时疲劳（Level 2）
        """
        alerts = []
        now = datetime.now(timezone.utc)

        # ===== 1. CMO 下跌检测 =====
        two_hours_ago = now - timedelta(hours=2)
        hourly_q = (
            select(HourlyMetrics)
            .where(
                HourlyMetrics.advertiser_id == advertiser_id,
                HourlyMetrics.hour_start >= two_hours_ago,
            )
            .order_by(HourlyMetrics.hour_start)
        )
        hourly_result = await self.db.execute(hourly_q)
        hourly_data = hourly_result.scalars().all()

        if len(hourly_data) >= 2:
            latest_hourly = hourly_data[-1]
            prev_hourly = hourly_data[-2]

            # CMO 环比下跌 > 10%
            if prev_hourly.cmo and latest_hourly.cmo:
                cmo_change = (latest_hourly.cmo - prev_hourly.cmo) / prev_hourly.cmo * 100
                if cmo_change < -10:
                    alerts.append(
                        RiskAlert(
                            advertiser_id=advertiser_id,
                            alert_type="CMO_DROP",
                            severity="WARNING",
                            title=f"CMO 下跌 {abs(cmo_change):.1f}%",
                            message=(
                                f"订单成本从 ${prev_hourly.cmo:.2f} → ${latest_hourly.cmo:.2f}，"
                                f"环比下跌 {abs(cmo_change):.1f}%。素材可能开始疲劳，建议监测。"
                            ),
                            metric_name="CMO",
                            current_value=latest_hourly.cmo,
                            threshold=prev_hourly.cmo,
                            change_pct=cmo_change,
                            recommended_action="monitor",
                            status="active",
                        )
                    )

        # ===== 2. ROI 跌破保本线 =====
        latest_snapshot_q = (
            select(AccountSnapshot)
            .where(AccountSnapshot.advertiser_id == advertiser_id)
            .order_by(AccountSnapshot.snapshot_time.desc())
            .limit(1)
        )
        latest_snapshot_result = await self.db.execute(latest_snapshot_q)
        latest_snapshot = latest_snapshot_result.scalar_one_or_none()

        if latest_snapshot and latest_snapshot.roas:
            break_even_roas = 4.5  # 可从 ProductCost 配置获取
            if latest_snapshot.roas < break_even_roas * 0.9:  # 接近亏损线
                alerts.append(
                    RiskAlert(
                        advertiser_id=advertiser_id,
                        alert_type="ROI_BELOW_BREAKEVEN",
                        severity="CRITICAL" if latest_snapshot.roas < break_even_roas else "WARNING",
                        title=f"ROI 接近或跌破保本线 ({latest_snapshot.roas:.2f}x)",
                        message=(
                            f"当前 ROAS {latest_snapshot.roas:.2f}x，保本线 {break_even_roas}x。"
                            f"按照这个速度，您正在亏损。建议立即暂停或降低出价。"
                        ),
                        metric_name="ROAS",
                        current_value=latest_snapshot.roas,
                        threshold=break_even_roas,
                        change_pct=(latest_snapshot.roas - break_even_roas) / break_even_roas * 100,
                        recommended_action="pause" if latest_snapshot.roas < break_even_roas else "reduce_budget",
                        status="active",
                    )
                )

        # ===== 3. 利润快速下降 =====
        if latest_snapshot and len(hourly_data) >= 3:
            latest_hourly = hourly_data[-1]
            three_hours_ago_hourly = hourly_data[0]

            if latest_hourly.roas and three_hours_ago_hourly.roas:
                roas_change = (latest_hourly.roas - three_hours_ago_hourly.roas) / three_hours_ago_hourly.roas * 100
                if roas_change < -15:  # 3 小时内 ROAS 下跌 > 15%
                    alerts.append(
                        RiskAlert(
                            advertiser_id=advertiser_id,
                            alert_type="ROI_DROP",
                            severity="HIGH",
                            title=f"ROAS 快速下跌 {abs(roas_change):.1f}%",
                            message=(
                                f"过去 3 小时内，ROAS 从 {three_hours_ago_hourly.roas:.2f}x → {latest_hourly.roas:.2f}x，"
                                f"下跌 {abs(roas_change):.1f}%。可能素材疲劳加速，建议替换素材或暂停。"
                            ),
                            metric_name="ROAS",
                            current_value=latest_hourly.roas,
                            threshold=three_hours_ago_hourly.roas,
                            change_pct=roas_change,
                            recommended_action="reduce_budget",
                            status="active",
                        )
                    )

        # ===== 4. 预算快速烧完（日维度）=====
        today = now.date()
        today_spend_q = (
            select(func.sum(MetricsSnapshot.spend))
            .where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.stat_date == today,
            )
        )
        today_spend_result = await self.db.execute(today_spend_q)
        today_spend = float(today_spend_result.scalar() or 0)

        daily_budget = 2000  # 可从 Advertiser 配置获取
        hours_elapsed = now.hour + now.minute / 60
        expected_spend = daily_budget * (hours_elapsed / 24)
        actual_pct = today_spend / daily_budget * 100 if daily_budget > 0 else 0
        expected_pct = hours_elapsed / 24 * 100

        if actual_pct > expected_pct + 20:  # 比预期快 20%
            alerts.append(
                RiskAlert(
                    advertiser_id=advertiser_id,
                    alert_type="BUDGET_EXCEED",
                    severity="WARNING",
                    title=f"预算快速烧完 ({actual_pct:.0f}%，预期 {expected_pct:.0f}%)",
                    message=(
                        f"已花费 ${today_spend:.0f} / ${daily_budget}，进度 {actual_pct:.1f}%。"
                        f"按当前速度，预计 {now.hour + (daily_budget - today_spend) / (today_spend / (hours_elapsed + 0.01)) // 60:.0f}:00 用完。"
                        f"建议降低出价或暂停部分活动。"
                    ),
                    metric_name="SPEND",
                    current_value=today_spend,
                    threshold=daily_budget,
                    change_pct=actual_pct - expected_pct,
                    recommended_action="reduce_budget",
                    status="active",
                )
            )

        # ===== 5. 多个素材同时疲劳 =====
        from app.models.creative import Creative, LifecycleStage

        fatigue_creatives_q = (
            select(Creative)
            .where(
                Creative.advertiser_id == advertiser_id,
                Creative.lifecycle_stage == LifecycleStage.FATIGUE,
            )
        )
        fatigue_result = await self.db.execute(fatigue_creatives_q)
        fatigue_count = len(fatigue_result.scalars().all())

        if fatigue_count >= 3:
            alerts.append(
                RiskAlert(
                    advertiser_id=advertiser_id,
                    alert_type="MATERIAL_FATIGUE_BULK",
                    severity="HIGH",
                    title=f"{fatigue_count} 个素材同时疲劳",
                    message=(
                        f"发现 {fatigue_count} 条素材处于 FATIGUE 阶段。"
                        f"这通常意味着人群覆盖饱和或素材库存不足。"
                        f"建议：1. 立即停用 FATIGUE 素材；2. 大量投入新素材；3. 考虑扩大定向范围。"
                    ),
                    metric_name="FATIGUE_COUNT",
                    current_value=fatigue_count,
                    threshold=2,  # 超过 2 个就告警
                    change_pct=0,
                    recommended_action="replace_materials",
                    status="active",
                )
            )

        # 保存所有告警
        for alert in alerts:
            self.db.add(alert)

        return alerts

    async def generate_stop_loss_plan(self, advertiser_id: str) -> Dict[str, Any]:
        """
        生成止损方案（当风险等级 >= HIGH 时）
        返回 3 个方案：激进 / 保守 / 监测
        """
        latest_snapshot_q = (
            select(AccountSnapshot)
            .where(AccountSnapshot.advertiser_id == advertiser_id)
            .order_by(AccountSnapshot.snapshot_time.desc())
            .limit(1)
        )
        latest_result = await self.db.execute(latest_snapshot_q)
        latest = latest_result.scalar_one_or_none()

        if not latest:
            return {"error": "No data"}

        break_even_roas = 4.5
        loss_per_hour = max(0, (latest.spend / (latest.roas + 0.1) - latest.gmv / (latest.roas + 0.1)))

        return {
            "current_state": {
                "roas": latest.roas,
                "real_profit": latest.real_profit,
                "spend_rate": latest.spend,  # 每小时
                "loss_rate_if_continues": loss_per_hour,
            },
            "plans": {
                "aggressive": {
                    "name": "激进止损",
                    "actions": [
                        "暂停所有 DECAY 和 FATIGUE 素材",
                        "停用 CTR < 1% 的广告",
                        "降低所有出价 20%",
                    ],
                    "expected_impact": {
                        "gmv_change": -20,
                        "roas_change": +15,
                        "profit_improvement": "可能从亏损扭正",
                    },
                    "risk": "高（GMV 大幅下跌，需要 3-7 天恢复）",
                    "timeline": "立即执行",
                },
                "conservative": {
                    "name": "保守调整",
                    "actions": [
                        "降低 DECAY 素材预算 50%",
                        "停用最差 2-3 个素材",
                        "降低出价 5-10%",
                    ],
                    "expected_impact": {
                        "gmv_change": -5,
                        "roas_change": +3,
                        "profit_improvement": "短期小幅改善",
                    },
                    "risk": "低（波动不大）",
                    "timeline": "立即执行，2 小时后评估",
                },
                "monitor": {
                    "name": "保持监测（推荐）",
                    "actions": [
                        "不主动调整，每 30 分钟检查一次",
                        "如果 ROAS 继续下跌 5%，自动触发激进止损",
                        "准备新素材库存，随时可以替换",
                    ],
                    "expected_impact": {
                        "gmv_change": 0,
                        "roas_change": 0,
                        "profit_improvement": "等待自然恢复或进一步恶化",
                    },
                    "risk": "中等（可能继续亏损）",
                    "timeline": "持续监测，48 小时内评估",
                    "trigger_conditions": [
                        f"如果 ROAS < {break_even_roas * 0.8:.2f}x，立即激进止损",
                        f"如果累计亏损 > $500，立即激进止损",
                        f"如果 FATIGUE 素材 > 5 个，立即替换",
                    ],
                },
            },
            "recommendation": "monitor",  # 根据实际情况推荐
            "note": "建议选择 '保持监测'，给平台 1-2 小时恢复时间。如果 ROAS 继续下跌，自动触发激进止损。",
        }
