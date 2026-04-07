"""
素材自动加热服务

核心逻辑：
  发现高潜力素材（GROWTH阶段 + hook_rate 高于均值）
  → LLM 计算建议加热幅度
  → 自动提高对应 AdGroup 预算/出价
  → 写入 Decision 记录 + 设置冷却期

与疲劳暂停对称：
  疲劳 → 自动暂停/降预算
  起量 → 自动加热/提预算
"""
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import List, Optional, Dict, Any

import numpy as np
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.creative import Creative, CreativeSnapshot, LifecycleStage
from app.models.metrics import MetricsSnapshot
from app.models.decision import Decision
from app.models.alert import Alert
from app.models.advertiser import Advertiser


# 加热冷却期（执行加热后多少小时内不重复）
BOOST_COOLDOWN_HOURS = 4

# 加热幅度计算（hook_rate 超均值倍数 → 预算增幅）
BOOST_RATIO_MAP = [
    (2.0, 0.50),   # hook_rate > 均值 2x → 加预算 50%
    (1.5, 0.30),   # hook_rate > 均值 1.5x → 加预算 30%
    (1.2, 0.20),   # hook_rate > 均值 1.2x → 加预算 20%
]

# 单次加热上限
MAX_BOOST_RATIO = 0.50   # 最多加 50%
MIN_BOOST_BUDGET = 10.0  # 加热预算最小增量（低于这个不操作）


@dataclass
class BoostCandidate:
    """加热候选素材"""
    creative: Creative
    latest_snapshot: CreativeSnapshot
    hook_rate: float
    hook_slope: float          # 近3天上升斜率
    benchmark_hook: float      # 账户均值
    hook_ratio: float          # hook_rate / benchmark（超均值倍数）
    related_adgroups: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0         # 综合评分，越高越值得加热


class CreativeBooster:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def scan_and_boost(self, advertiser_id: str) -> List[Decision]:
        """
        扫描账户下的高潜力素材，生成加热决策
        """
        # 1. 获取账户基准
        benchmark = await self._get_benchmark(advertiser_id)
        avg_hook = benchmark.get("avg_hook_rate", 0)

        if avg_hook < 0.1:
            logger.debug(f"[Booster] {advertiser_id}: no benchmark data yet, skip")
            return []

        # 2. 扫描 GROWTH 阶段素材
        result = await self.db.execute(
            select(Creative).where(
                Creative.advertiser_id == advertiser_id,
                Creative.lifecycle_stage.in_([LifecycleStage.GROWTH, LifecycleStage.WARM_UP]),
                Creative.is_fatigue == "N",
                Creative.last_active_date >= date.today() - timedelta(days=1),
            )
        )
        creatives = result.scalars().all()

        candidates = []
        for creative in creatives:
            candidate = await self._evaluate(creative, avg_hook)
            if candidate:
                candidates.append(candidate)

        if not candidates:
            return []

        # 3. 按评分排序，只处理 Top N（避免一次操作太多）
        candidates.sort(key=lambda x: x.score, reverse=True)
        top_candidates = candidates[:5]  # 每次最多处理 5 个

        logger.info(f"[Booster] {advertiser_id}: {len(candidates)} candidates, boosting top {len(top_candidates)}")

        # 4. 获取广告主信息
        adv_result = await self.db.execute(
            select(Advertiser).where(Advertiser.advertiser_id == advertiser_id)
        )
        advertiser = adv_result.scalar_one_or_none()
        if not advertiser:
            return []

        decisions = []
        for candidate in top_candidates:
            decision = await self._create_boost_decision(
                candidate, advertiser, benchmark,
                cold_start_mode=(candidate.creative.days_running or 0) < 7,
            )
            if decision:
                decisions.append(decision)

        if decisions:
            await self.db.commit()

        return decisions

    async def _evaluate(self, creative: Creative, avg_hook: float) -> Optional[BoostCandidate]:
        """
        评估素材是否值得加热，返回 BoostCandidate 或 None
        """
        # 获取近7天快照
        snaps = await self._get_daily_snapshots(creative.advertiser_id, creative.video_id, days=7)
        if not snaps or len(snaps) < 2:
            return None

        latest = snaps[-1]
        hook_rate = float(latest.hook_rate or 0)

        # 基础筛选：hook_rate 必须高于均值 20%
        if hook_rate < avg_hook * 1.2:
            return None

        # 必须有花费（排除未投放的）
        if latest.spend < 5:
            return None

        # 计算 hook_rate 近3天斜率
        recent_hooks = [float(s.hook_rate or 0) for s in snaps[-3:]]
        hook_slope = self._slope(recent_hooks) if len(recent_hooks) >= 2 else 0.0

        # 斜率不能是负的（下降中不加热）
        if hook_slope < -0.1:
            return None

        # 冷启动期（前7天）特殊处理：
        # 前3天完全不加热（数据量太少，不可信）
        # 4-7天：只有 hook_rate 极显著高于均值（>2x）才加热，且置信度上限 0.7
        days_running = creative.days_running or 0
        if days_running < 3:
            return None
        cold_start_mode = days_running < 7

        # 冷启动期（4-7天）阈值更严格：需要 hook_rate > 均值 2x 才触发
        if cold_start_mode and hook_ratio < 2.0:
            return None

        # 检查冷却期（最近 BOOST_COOLDOWN_HOURS 内是否已经加热过）
        if await self._in_cooldown(creative.advertiser_id, creative.video_id):
            logger.debug(f"[Booster] {creative.video_id} in cooldown, skip")
            return None

        hook_ratio = hook_rate / avg_hook if avg_hook > 0 else 1.0

        # 综合评分：hook_ratio × (1 + slope) × log(spend+1)
        score = hook_ratio * max(1.0, 1 + hook_slope) * np.log1p(latest.spend)

        # 找关联的 AdGroup（通过 metrics_snapshots 找到 adgroup_id）
        adgroups = await self._get_related_adgroups(creative.advertiser_id, creative.ad_id)

        return BoostCandidate(
            creative=creative,
            latest_snapshot=latest,
            hook_rate=hook_rate,
            hook_slope=hook_slope,
            benchmark_hook=avg_hook,
            hook_ratio=hook_ratio,
            related_adgroups=adgroups,
            score=float(score),
        )

    async def _create_boost_decision(
        self,
        candidate: BoostCandidate,
        advertiser: Advertiser,
        benchmark: Dict[str, float],
        cold_start_mode: bool = False,
    ) -> Optional[Decision]:
        """
        创建加热决策：计算建议预算增幅，存入 Decision 表
        """
        # 计算加热幅度
        boost_ratio = 0.20  # 默认 20%
        for threshold, ratio in BOOST_RATIO_MAP:
            if candidate.hook_ratio >= threshold:
                boost_ratio = ratio
                break

        boost_ratio = min(boost_ratio, MAX_BOOST_RATIO)

        # 取关联 AdGroup 中花费最高的操作
        target_adgroup = None
        if candidate.related_adgroups:
            target_adgroup = max(candidate.related_adgroups, key=lambda x: x.get("spend", 0))

        # 构建 LLM prompt 让其决策最终幅度
        prompt = self._build_boost_prompt(candidate, benchmark, boost_ratio, target_adgroup)

        # 调用 LLM
        from app.services.llm_decision import LLMDecisionService
        from app.models.alert import Alert as AlertModel
        from datetime import datetime

        # 构造一个虚拟 Alert 传给 LLM（加热场景）
        boost_alert = AlertModel(
            id=0,
            advertiser_id=advertiser.advertiser_id,
            data_level="CREATIVE",
            object_id=candidate.creative.video_id,
            object_name=candidate.creative.creative_name or candidate.creative.video_id,
            alert_type="CREATIVE_BOOST_OPPORTUNITY",
            severity="INFO",
            title=f"素材起量机会: {candidate.creative.video_id[:16]}",
            message=f"Hook Rate {candidate.hook_rate:.1f}% 高于账户均值 {candidate.benchmark_hook:.1f}% 的 {candidate.hook_ratio:.1f}x，建议加热",
            metrics_snapshot={
                "hook_rate": candidate.hook_rate,
                "hook_slope": candidate.hook_slope,
                "benchmark_hook": candidate.benchmark_hook,
                "hook_ratio": candidate.hook_ratio,
                "spend": candidate.latest_snapshot.spend,
                "lifecycle_stage": candidate.creative.lifecycle_stage,
                "days_running": candidate.creative.days_running,
                "suggested_boost_ratio": boost_ratio,
                "target_adgroup_id": target_adgroup.get("adgroup_id") if target_adgroup else None,
            },
            created_at=datetime.now(),
        )

        # 使用加热专用 system prompt
        llm_svc = LLMDecisionService()
        llm_result = await llm_svc.analyze(
            alert=boost_alert,
            snapshots=[candidate.latest_snapshot],
            advertiser_context={
                "currency": advertiser.currency or "USD",
                "benchmark": benchmark,
                "boost_context": True,
                "suggested_boost_ratio": boost_ratio,
            },
        )

        action = llm_result.get("action", "no_action")
        confidence = float(llm_result.get("confidence", 0.0))
        action_params = llm_result.get("action_params", {})

        # 加热场景强制 action 为 increase_budget 或 increase_bid
        if action not in ("increase_budget", "increase_bid", "no_action"):
            action = "increase_budget"
            action_params = action_params or {}

        # 如果 LLM 没给具体预算值，用系统计算的
        if action == "increase_budget" and "budget" not in action_params and target_adgroup:
            current_budget = target_adgroup.get("budget", 0)
            if current_budget > 0:
                action_params["budget"] = round(current_budget * (1 + boost_ratio), 2)
                action_params["original_budget"] = current_budget
                action_params["boost_ratio"] = boost_ratio

        # 冷启动期（4-7天）：置信度上限 0.7，强制人工审批
        if cold_start_mode:
            confidence = min(confidence, 0.70)

        # 加热决策置信度阈值
        auto_threshold = 0.78
        should_auto = confidence >= auto_threshold and not cold_start_mode

        decision = Decision(
            advertiser_id=advertiser.advertiser_id,
            data_level="CREATIVE",
            object_id=candidate.creative.video_id,
            object_name=candidate.creative.creative_name or candidate.creative.video_id,
            trigger_type="BOOST_OPPORTUNITY",
            trigger_reason=boost_alert.message,
            metrics_context=boost_alert.metrics_snapshot,
            llm_prompt=llm_result.get("_prompt", prompt),
            llm_response=llm_result.get("_raw_response", ""),
            action=action,
            action_params=action_params,
            confidence=confidence,
            reason=llm_result.get("reason", ""),
            status="PENDING",
        )
        self.db.add(decision)
        await self.db.flush()

        if should_auto and action != "no_action" and target_adgroup:
            logger.info(
                f"[Booster] Auto-boost {candidate.creative.video_id}: "
                f"{action} adgroup={target_adgroup.get('adgroup_id')} "
                f"(confidence={confidence:.2f})"
            )
            # 执行加热
            from app.services.tiktok_client import TikTokClient
            client = TikTokClient(
                access_token=advertiser.access_token,
                advertiser_id=advertiser.advertiser_id,
            )
            try:
                if action == "increase_budget" and action_params.get("budget"):
                    await client.update_adgroup_budget(
                        target_adgroup["adgroup_id"],
                        action_params["budget"],
                    )
                elif action == "increase_bid" and action_params.get("bid"):
                    # 出价调整（后续实现）
                    pass
                decision.status = "AUTO_EXECUTED"
                decision.is_auto_executed = True
                decision.executed_at = datetime.now(timezone.utc)
            except Exception as e:
                logger.error(f"[Booster] Execute failed: {e}")
                decision.status = "FAILED"
                decision.error_message = str(e)
            finally:
                await client.close()
        else:
            # 推飞书待审批
            from app.core.config import settings
            from app.services.notifier import FeishuNotifier
            notifier = FeishuNotifier(webhook_url=settings.FEISHU_WEBHOOK_URL)
            await notifier.send_decision_pending(decision)
            await notifier.close()

        return decision

    def _build_boost_prompt(
        self,
        candidate: BoostCandidate,
        benchmark: Dict,
        suggested_ratio: float,
        target_adgroup: Optional[Dict],
    ) -> str:
        return f"""## 素材加热决策

该素材当前处于上升期，Hook Rate 显著高于账户均值，有加大投放的机会。

## 素材数据
- video_id: {candidate.creative.video_id}
- 已投放天数: {candidate.creative.days_running}天
- 生命周期阶段: {candidate.creative.lifecycle_stage}
- 当前 Hook Rate: {candidate.hook_rate:.1f}%
- 账户平均 Hook Rate: {benchmark.get('avg_hook_rate', 0):.1f}%
- Hook Rate 是均值的: {candidate.hook_ratio:.1f}x
- 近3天 Hook Rate 趋势: {"上升" if candidate.hook_slope > 0 else "平稳"}（斜率 {candidate.hook_slope:.2f}）
- 今日花费: ${candidate.latest_snapshot.spend:.2f}
- 今日转化: {candidate.latest_snapshot.conversion}

## 关联 AdGroup 信息
{f"- adgroup_id: {target_adgroup['adgroup_id']}" if target_adgroup else "- 暂未找到关联 AdGroup"}
{f"- 当前预算: ${target_adgroup.get('budget', 0):.2f}" if target_adgroup else ""}

## 系统建议
建议提高预算 {suggested_ratio*100:.0f}%（基于 Hook Rate 超均值幅度计算）

请判断是否应该加热该素材，如果是，给出具体的预算或出价调整建议。
action 应为 increase_budget / increase_bid / no_action 之一。"""

    @staticmethod
    def _slope(values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        x = np.arange(len(values), dtype=float)
        y = np.array(values, dtype=float)
        x_mean, y_mean = x.mean(), y.mean()
        denom = ((x - x_mean) ** 2).sum()
        if denom < 1e-10:
            return 0.0
        return float(((x - x_mean) * (y - y_mean)).sum() / denom)

    async def _in_cooldown(self, advertiser_id: str, video_id: str) -> bool:
        """检查是否在冷却期内"""
        cooldown_since = datetime.now(timezone.utc) - timedelta(hours=BOOST_COOLDOWN_HOURS)
        result = await self.db.execute(
            select(Decision).where(
                Decision.advertiser_id == advertiser_id,
                Decision.object_id == video_id,
                Decision.trigger_type == "BOOST_OPPORTUNITY",
                Decision.created_at >= cooldown_since,
                Decision.status.in_(["AUTO_EXECUTED", "MANUAL_APPROVED", "PENDING"]),
            ).limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def _get_benchmark(self, advertiser_id: str) -> Dict[str, float]:
        since = date.today() - timedelta(days=3)
        result = await self.db.execute(
            select(
                func.avg(CreativeSnapshot.hook_rate).label("avg_hook_rate"),
                func.avg(CreativeSnapshot.hold_rate).label("avg_hold_rate"),
                func.avg(CreativeSnapshot.ctr).label("avg_ctr"),
                func.avg(CreativeSnapshot.cost_per_conversion).label("avg_cpa"),
            ).where(
                CreativeSnapshot.advertiser_id == advertiser_id,
                CreativeSnapshot.stat_date >= since,
                CreativeSnapshot.spend > 1,
            )
        )
        row = result.one()
        return {
            "avg_hook_rate": float(row.avg_hook_rate or 0),
            "avg_hold_rate": float(row.avg_hold_rate or 0),
            "avg_ctr":       float(row.avg_ctr or 0),
            "avg_cpa":       float(row.avg_cpa or 0),
        }

    async def _get_daily_snapshots(
        self,
        advertiser_id: str,
        video_id: str,
        days: int = 7,
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
        by_date = {}
        for s in all_snaps:
            if s.stat_date not in by_date or s.snapshot_time > by_date[s.stat_date].snapshot_time:
                by_date[s.stat_date] = s
        return sorted(by_date.values(), key=lambda x: x.stat_date)

    async def _get_related_adgroups(
        self,
        advertiser_id: str,
        ad_id: Optional[str],
    ) -> List[Dict]:
        """找到素材对应的 AdGroup 及其最新预算/花费"""
        if not ad_id:
            return []
        result = await self.db.execute(
            select(
                MetricsSnapshot.adgroup_id,
                func.sum(MetricsSnapshot.spend).label("spend"),
                func.max(MetricsSnapshot.budget).label("budget"),
            ).where(
                MetricsSnapshot.advertiser_id == advertiser_id,
                MetricsSnapshot.data_level == "ADGROUP",
                MetricsSnapshot.stat_date >= date.today() - timedelta(days=3),
            )
            .group_by(MetricsSnapshot.adgroup_id)
            .order_by(func.sum(MetricsSnapshot.spend).desc())
            .limit(3)
        )
        rows = result.all()
        return [
            {"adgroup_id": str(r.adgroup_id), "spend": float(r.spend or 0), "budget": float(r.budget or 0)}
            for r in rows if r.adgroup_id
        ]
