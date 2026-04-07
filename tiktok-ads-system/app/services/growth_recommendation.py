"""
梯度增长建议引擎 — 为新投放/素材生成的预算计划

输入：当前日花费、Hook Rate、生命周期阶段、账户历史 ROI
输出：Day 1-10 的预算建议（保守/标准/激进）+ 风险提示
"""
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.config import settings
from app.models.advertiser import Advertiser
from app.models.creative import Creative, LifecycleStage
from app.models.metrics import MetricsSnapshot
from app.models.analytics import GrowthRecommendation
from app.services.llm_decision import LLMDecisionService


class GrowthRecommendationEngine:
    """梯度增长建议"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm_service = LLMDecisionService()

    async def generate_recommendation(
        self,
        advertiser_id: str,
        object_type: str,  # CAMPAIGN / ADGROUP / VIDEO
        object_id: str,
        object_name: str,
        current_daily_spend: float,
        current_hook_rate: float,
        days_running: int,
    ) -> Optional[GrowthRecommendation]:
        """
        为某个投放对象生成梯度增长建议

        Args:
            advertiser_id: 广告账户
            object_type: 投放对象类型
            object_id: 对象 ID
            object_name: 对象名称
            current_daily_spend: 当前日花费（$）
            current_hook_rate: 当前 Hook Rate（%）
            days_running: 已运行天数

        Returns:
            GrowthRecommendation 记录或 None
        """
        # 1. 确定生命周期阶段
        current_stage = self._determine_stage(days_running, current_hook_rate)

        # 2. 从历史数据获取账户基准
        benchmark = await self._get_account_benchmark(advertiser_id)

        # 3. 用 LLM 生成建议
        plans = await self._generate_plans_with_llm(
            object_name=object_name,
            current_stage=current_stage,
            current_daily_spend=current_daily_spend,
            current_hook_rate=current_hook_rate,
            days_running=days_running,
            account_avg_roi=benchmark.get("avg_roi", 2.5),
            account_avg_hook=benchmark.get("avg_hook_rate", 5.0),
        )

        if not plans:
            return None

        # 4. 创建推荐记录
        recommendation = GrowthRecommendation(
            advertiser_id=advertiser_id,
            object_type=object_type,
            object_id=object_id,
            object_name=object_name,
            current_stage=current_stage,
            days_running=days_running,
            current_daily_spend=current_daily_spend,
            current_hook_rate=current_hook_rate,
            current_roas=benchmark.get("avg_roi", 2.5),
            conservative_plan=json.dumps(plans["conservative"]),
            standard_plan=json.dumps(plans["standard"]),
            aggressive_plan=json.dumps(plans["aggressive"]),
            recommended_plan=plans["recommended"],
            confidence=plans["confidence"],
            risk_notes=plans["risk_notes"],
            status="active",
        )

        self.db.add(recommendation)
        logger.info(
            f"Generated growth recommendation for {object_name} "
            f"(stage={current_stage}, spend=${current_daily_spend})"
        )

        return recommendation

    def _determine_stage(self, days_running: int, hook_rate: float) -> str:
        """根据投放天数和 Hook Rate 判断阶段"""
        if days_running < 3:
            return "WARM_UP"
        elif days_running < 7:
            if hook_rate > 5.0:
                return "GROWTH"
            return "WARM_UP"
        elif hook_rate > 7.0:
            return "PEAK"
        elif hook_rate > 4.0:
            return "GROWTH"
        else:
            return "DECAY"

    async def _get_account_benchmark(self, advertiser_id: str) -> Dict[str, float]:
        """从历史数据获取账户基准"""
        # 拉最近 7 天的数据
        from datetime import timedelta, date

        since = date.today() - timedelta(days=7)

        metrics_q = select(
            func.avg(MetricsSnapshot.cost_per_conversion).label("avg_cpa"),
            func.avg(MetricsSnapshot.ctr).label("avg_ctr"),
        ).where(
            MetricsSnapshot.advertiser_id == advertiser_id,
            MetricsSnapshot.stat_date >= since,
        )

        result = await self.db.execute(metrics_q)
        row = result.one()

        # 用 Creative 获取平均 Hook Rate
        creative_q = select(
            func.avg(Creative.hook_rate_latest).label("avg_hook")
        ).where(Creative.advertiser_id == advertiser_id)

        creative_result = await self.db.execute(creative_q)
        creative_row = creative_result.one()

        return {
            "avg_cpa": float(row.avg_cpa or 0),
            "avg_ctr": float(row.avg_ctr or 0),
            "avg_hook_rate": float(creative_row.avg_hook or 5.0),
            "avg_roi": 2.5,  # 简化，实际应该计算
        }

    async def _generate_plans_with_llm(
        self,
        object_name: str,
        current_stage: str,
        current_daily_spend: float,
        current_hook_rate: float,
        days_running: int,
        account_avg_roi: float,
        account_avg_hook: float,
    ) -> Optional[Dict[str, Any]]:
        """用 LLM 生成三个梯度增长方案"""

        prompt = f"""
You are a TikTok advertising expert. Generate a budget growth plan for the following campaign:

Campaign: {object_name}
Current Stage: {current_stage}
Days Running: {days_running}
Current Daily Spend: ${current_daily_spend:.2f}
Current Hook Rate: {current_hook_rate:.1f}%
Account Avg Hook Rate: {account_avg_hook:.1f}%
Account Avg ROI: {account_avg_roi:.2f}x

Generate a budget growth plan for the next 10 days with 3 strategies:

Return ONLY a valid JSON object (no markdown, no explanations) with this exact structure:
{{
  "conservative": {{
    "name": "Conservative Growth",
    "description": "Slow, safe increase",
    "daily_budget": [Day1_amount, Day2_amount, ..., Day10_amount],
    "rationale": "explanation"
  }},
  "standard": {{
    "name": "Standard Growth",
    "description": "Balanced approach",
    "daily_budget": [Day1_amount, Day2_amount, ..., Day10_amount],
    "rationale": "explanation"
  }},
  "aggressive": {{
    "name": "Aggressive Growth",
    "description": "Fast scaling",
    "daily_budget": [Day1_amount, Day2_amount, ..., Day10_amount],
    "rationale": "explanation"
  }},
  "recommended": "conservative|standard|aggressive",
  "confidence": 0-100,
  "risk_notes": "key risks and mitigations"
}}
"""

        try:
            # 调用 LLM
            response = await self.llm_service.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            response_text = response.choices[0].message.content.strip()

            # 清理可能的 markdown 包装
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            plans = json.loads(response_text)

            # 验证返回的结构
            if not all(k in plans for k in ["conservative", "standard", "aggressive", "recommended", "confidence"]):
                logger.warning("LLM response missing required fields, using default")
                return self._generate_default_plans(
                    current_daily_spend, current_stage, current_hook_rate
                )

            return plans

        except Exception as e:
            logger.warning(f"LLM generation failed: {e}, using default plans")
            return self._generate_default_plans(
                current_daily_spend, current_stage, current_hook_rate
            )

    def _generate_default_plans(
        self,
        current_spend: float,
        stage: str,
        hook_rate: float,
    ) -> Dict[str, Any]:
        """
        默认计划（如果 LLM 失败）
        
        规则（GMV Max 标准）：
        - WARM_UP: 保持或小幅增长
        - GROWTH: 加速增长
        - PEAK: 继续增长但速度放缓
        - DECAY: 减少或维持
        """

        if stage == "WARM_UP":
            # 前 7 天，保守增长，每天 +10-15%
            base_increase = 0.12
        elif stage == "GROWTH":
            # 学习期通过，加速，每天 +20-30%
            base_increase = 0.25
        elif stage == "PEAK":
            # 峰值期，持续但缓增，每天 +10-15%
            base_increase = 0.12
        else:  # DECAY
            # 衰退期，减少
            base_increase = -0.05

        # 生成 3 个方案
        conservative = [round(current_spend * ((1 + base_increase * 0.5) ** i), 2) for i in range(10)]
        standard = [round(current_spend * ((1 + base_increase) ** i), 2) for i in range(10)]
        aggressive = [round(current_spend * ((1 + base_increase * 1.5) ** i), 2) for i in range(10)]

        return {
            "conservative": {
                "name": "Conservative",
                "description": "Slow, low-risk growth",
                "daily_budget": conservative,
                "rationale": f"Increase 50% slower than standard (base +{base_increase*0.5*100:.0f}%/day)",
            },
            "standard": {
                "name": "Standard",
                "description": "Balanced growth following GMV Max best practices",
                "daily_budget": standard,
                "rationale": f"Steady growth at +{base_increase*100:.0f}%/day, suitable for {stage} stage",
            },
            "aggressive": {
                "name": "Aggressive",
                "description": "Fast scaling for high performers",
                "daily_budget": aggressive,
                "rationale": f"Accelerated growth at +{base_increase*1.5*100:.0f}%/day, high risk but high reward",
            },
            "recommended": "standard",
            "confidence": 75,
            "risk_notes": (
                f"Current Hook Rate {hook_rate:.1f}% is {'above' if hook_rate > 5 else 'below'} "
                f"industry average. Adjust aggressiveness accordingly."
            ),
        }

    async def get_recommendation(
        self, advertiser_id: str, object_id: str
    ) -> Optional[GrowthRecommendation]:
        """获取某个对象的推荐"""
        rec_q = select(GrowthRecommendation).where(
            GrowthRecommendation.advertiser_id == advertiser_id,
            GrowthRecommendation.object_id == object_id,
            GrowthRecommendation.status == "active",
        )
        result = await self.db.execute(rec_q)
        return result.scalar_one_or_none()

    async def apply_recommendation(
        self, recommendation_id: int, chosen_plan: str
    ) -> bool:
        """
        用户选择某个方案后，标记为已应用
        
        Args:
            recommendation_id: 推荐 ID
            chosen_plan: 选择的方案（conservative / standard / aggressive）
        """
        rec_q = select(GrowthRecommendation).where(GrowthRecommendation.id == recommendation_id)
        result = await self.db.execute(rec_q)
        rec = result.scalar_one_or_none()

        if rec:
            rec.applied_plan = chosen_plan
            rec.applied_at = datetime.now(timezone.utc)
            rec.status = "completed"
            await self.db.commit()
            logger.info(f"Applied {chosen_plan} plan to recommendation {recommendation_id}")
            return True

        return False
