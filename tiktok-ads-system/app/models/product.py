"""
商品成本模型

绑定到 TikTok Shop 商品（product_id / sku_id 维度）
计算链路：
  GMV
  - 退货金额（退货率 × GMV）
  - 货损金额（货损率 × GMV）
  = 实收 GMV
  - 商品成本（product_cost × 销量）
  - 头程运费（freight_inbound × 销量）
  - 尾程运费（freight_outbound × 销量）
  - 达人佣金（affiliate_rate × GMV）
  - 广告花费（从 metrics 拿）
  - TikTok 平台佣金（platform_fee_rate × GMV）
  = 真实利润（Real Profit）
  / 实收 GMV
  = 真实利润率（Real Margin）
"""
from sqlalchemy import Column, String, Float, BigInteger, ForeignKey, Text, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class ProductCost(Base, TimestampMixin):
    """
    商品成本配置表
    粒度：advertiser_id + product_id（可精确到 sku_id）
    """
    __tablename__ = "product_costs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=True, index=True, comment="历史字段，已弃用；成本配置按 product_id 唯一")

    # 商品标识（TikTok Shop product_id / sku_id）
    product_id    = Column(String(128), nullable=False, index=True, comment="TikTok Shop 商品 ID")
    sku_id        = Column(String(128), index=True, comment="SKU ID，为空表示商品级")
    product_name  = Column(String(512), comment="商品名称")
    currency      = Column(String(8), default="USD")

    # ===== 成本项 =====

    # 1. 商品成本（含包装）
    product_cost  = Column(Float, default=0.0, comment="货品成本（含包装）单位：货币/件")

    # 2. 头程运费（国内仓→海外仓，按件均摊）
    freight_inbound = Column(Float, default=0.0, comment="头程运费（国内到海外仓）单位：货币/件")

    # 3. 尾程运费（海外仓→买家）
    freight_outbound = Column(Float, default=0.0, comment="尾程运费（海外仓到买家）单位：货币/件")

    # 4. 达人佣金率（占 GMV 的百分比）
    affiliate_rate = Column(Float, default=0.0, comment="达人佣金率 %，如 10 表示 10%")

    # 5. TikTok 平台佣金率
    platform_fee_rate = Column(Float, default=5.0, comment="TikTok 平台抽佣率 %，默认 5%")

    # 6. 退货率（历史均值，用于预估）
    return_rate    = Column(Float, default=0.0, comment="退货率 %，如 5 表示 5%")

    # 7. 货损率（运输/仓储损耗）
    damage_rate    = Column(Float, default=0.0, comment="货损率 %，如 1 表示 1%")

    # 8. 投放返点（TikTok Shop 的投放激励）
    ad_rebate_rate = Column(Float, default=0.0, comment="投放返点率 %，如 3 表示 3%（从花费中返回）")

    # 商品售价（用于校验 ROI 计算，可选）
    selling_price  = Column(Float, comment="商品售价（含税）")

    # 是否启用
    is_active      = Column(Boolean, default=True)

    # 备注
    notes          = Column(Text, comment="备注，如成本变更原因")

    __table_args__ = (
        Index("ix_product_cost_adv_product", "advertiser_id", "product_id", "sku_id"),
    )

    def __repr__(self):
        return f"<ProductCost {self.product_id} cost={self.product_cost}>"

    def total_cost_per_unit(self) -> float:
        """每件商品的固定成本（不含广告、佣金）"""
        return self.product_cost + self.freight_inbound + self.freight_outbound

    def calc_profit(
        self,
        gmv: float,
        units_sold: int,
        ad_spend: float,
    ) -> dict:
        """
        计算真实利润

        Args:
            gmv: 广告带来的 GMV（含税含佣金的销售额）
            units_sold: 销售件数
            ad_spend: 对应广告花费

        Returns:
            完整的利润拆解 dict
        """
        if gmv <= 0 or units_sold <= 0:
            return {
                "gmv": gmv,
                "net_gmv": 0,
                "real_profit": -ad_spend,
                "real_margin": -1.0,
                "real_roas": 0,
                "break_even_roas": None,
            }

        # 退货扣减
        return_deduction = gmv * (self.return_rate / 100)
        # 货损扣减
        damage_deduction = gmv * (self.damage_rate / 100)
        # 实收 GMV
        net_gmv = gmv - return_deduction - damage_deduction

        # 成本项
        goods_cost      = self.product_cost    * units_sold
        inbound_cost    = self.freight_inbound  * units_sold
        outbound_cost   = self.freight_outbound * units_sold
        affiliate_cost  = net_gmv * (self.affiliate_rate   / 100)
        platform_cost   = net_gmv * (self.platform_fee_rate / 100)

        # 投放返点（平台返回的激励，降低实际广告成本）
        ad_rebate = ad_spend * (self.ad_rebate_rate / 100)
        effective_ad_spend = ad_spend - ad_rebate

        total_cost = (
            goods_cost
            + inbound_cost
            + outbound_cost
            + affiliate_cost
            + platform_cost
            + effective_ad_spend
        )

        real_profit = net_gmv - total_cost
        real_margin = real_profit / net_gmv if net_gmv > 0 else -1.0
        real_roas   = net_gmv / effective_ad_spend if effective_ad_spend > 0 else 0

        # 保本 ROAS：至少要多少 ROAS 才不亏
        # net_gmv × (1 - affiliate_rate% - platform_fee%) - goods_cost - inbound - outbound = effective_ad_spend
        variable_rate = (self.affiliate_rate + self.platform_fee_rate) / 100
        fixed_cost_per_unit = self.product_cost + self.freight_inbound + self.freight_outbound
        avg_order_value = gmv / units_sold
        avg_net_order   = avg_order_value * (1 - self.return_rate/100) * (1 - self.damage_rate/100)
        margin_after_variable = avg_net_order * (1 - variable_rate) - fixed_cost_per_unit
        break_even_roas = (
            avg_net_order / margin_after_variable
            if margin_after_variable > 0 else None
        )

        return {
            "gmv":                 round(gmv, 2),
            "return_deduction":    round(return_deduction, 2),
            "damage_deduction":    round(damage_deduction, 2),
            "net_gmv":             round(net_gmv, 2),
            "goods_cost":          round(goods_cost, 2),
            "inbound_cost":        round(inbound_cost, 2),
            "outbound_cost":       round(outbound_cost, 2),
            "affiliate_cost":      round(affiliate_cost, 2),
            "platform_cost":       round(platform_cost, 2),
            "ad_spend":            round(ad_spend, 2),
            "ad_rebate":           round(ad_rebate, 2),           # 投放返点金额
            "effective_ad_spend":  round(effective_ad_spend, 2),  # 实际花费
            "total_cost":          round(total_cost, 2),
            "real_profit":         round(real_profit, 2),
            "real_margin":         round(real_margin * 100, 2),   # 转成 %
            "real_roas":           round(real_roas, 2),
            "break_even_roas":     round(break_even_roas, 2) if break_even_roas else None,
            "is_profitable":       real_profit > 0,
        }
