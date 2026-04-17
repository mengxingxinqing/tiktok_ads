"""
万粉成本计算器
"""
from decimal import Decimal
from typing import Optional


class BudgetCalculator:
    """预算计算器"""

    DEFAULT_COST_PER_10K = Decimal("35.0")  # 默认万粉成本 USD
    # ⚠️ BUFFER_MULTIPLIER 直接作为 TikTok Campaign total_budget，是物理预算墙
    # 1.0 = 严格不留余量：预算烧光 = 按 target 成本跑完 = TikTok 自动停
    # Phase 1 的核心强约束："不跑超" 由 TikTok 平台硬保证，不依赖我们的监控
    BUFFER_MULTIPLIER = Decimal("1.0")

    @classmethod
    def calculate_budget(
        cls,
        target_follower_count: int,
        current_follower_count: int,
        avg_cost_per_10k: Optional[Decimal] = None,
    ) -> Decimal:
        """
        计算投放预算（USD，将作为 TikTok Campaign 的 total_budget）

        公式：预算 = 目标增量 × (万粉成本 / 10000) × 1.05
        TikTok 侧一旦烧满就自动停，即使本系统监控挂了也不会无限超投。

        Args:
            target_follower_count: 目标粉丝数
            current_follower_count: 当前粉丝数
            avg_cost_per_10k: 实测万粉成本（取系统均值；None 回退 $35）

        Returns:
            预算 USD（Decimal，保留2位小数）
        """
        target_increment = max(0, target_follower_count - current_follower_count)
        cost = avg_cost_per_10k or cls.DEFAULT_COST_PER_10K

        budget = Decimal(str(target_increment)) * (cost / Decimal("10000")) * cls.BUFFER_MULTIPLIER
        return round(budget, 2)

    @classmethod
    def update_material_cost(
        cls,
        material,
        campaign_spend: Decimal,
        campaign_followers_gained: int,
    ):
        """
        更新素材的万粉成本（Campaign 结束后调用）

        Args:
            material: CreativeMaterial 实例
            campaign_spend: 这次投放花费 USD
            campaign_followers_gained: 这次带来的粉丝增量
        """
        if campaign_followers_gained <= 0:
            return

        # 本次万粉成本
        cost_per_10k = (campaign_spend / campaign_followers_gained) * 10000

        # 更新累计值
        material.total_spend = (material.total_spend or Decimal("0")) + campaign_spend
        material.total_followers_gained = (material.total_followers_gained or 0) + campaign_followers_gained
        material.sample_count = (material.sample_count or 0) + 1

        # 计算最新万粉成本
        material.latest_cost_per_10k = cost_per_10k

        # 计算 Rolling 平均（最近5次）
        if material.sample_count >= 1:
            # 简单实现：所有样本的均值
            material.cost_per_10k = (material.total_spend / material.total_followers_gained) * 10000
            material.avg_cost_per_10k = cost_per_10k  # 简化：用本次覆盖
        else:
            material.avg_cost_per_10k = cost_per_10k
