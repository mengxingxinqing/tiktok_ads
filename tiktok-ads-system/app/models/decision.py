"""
LLM 决策记录 — 每次 LLM 给出建议/执行动作都记录在这里，支持回溯和审计
"""
from sqlalchemy import Column, String, Float, DateTime, BigInteger, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Decision(Base, TimestampMixin):
    __tablename__ = "decisions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 归属
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"), nullable=False, index=True)
    data_level = Column(String(32), comment="CAMPAIGN / ADGROUP / AD")
    object_id = Column(String(64), index=True, comment="操作对象 ID")
    object_name = Column(String(512))

    # 触发原因
    trigger_type = Column(String(64), comment="ANOMALY / TREND / SCHEDULED / MANUAL")
    trigger_reason = Column(Text, comment="触发原因描述")
    metrics_context = Column(JSON, comment="决策时的指标快照（JSON）")

    # LLM 决策
    llm_prompt = Column(Text, comment="发给 LLM 的 prompt")
    llm_response = Column(Text, comment="LLM 原始响应")
    action = Column(String(64), comment="决策动作: pause/enable/increase_budget/decrease_bid/etc")
    action_params = Column(JSON, comment="动作参数，如 {budget: 1000}")
    confidence = Column(Float, comment="LLM 置信度 0~1")
    reason = Column(Text, comment="LLM 决策理由")

    # 执行状态
    # PENDING = 等待执行, AUTO_EXECUTED = 自动执行, MANUAL_APPROVED = 人工批准后执行
    # MANUAL_REJECTED = 人工拒绝, FAILED = 执行失败, SKIPPED = 跳过
    status = Column(String(32), default="PENDING", index=True)
    is_auto_executed = Column(Boolean, default=False, comment="是否自动执行（置信度高）")
    executed_at = Column(DateTime(timezone=True), comment="执行时间")
    execution_result = Column(JSON, comment="执行结果（TikTok API 响应）")
    error_message = Column(Text, comment="执行失败原因")

    # 回滚支持
    is_rollback = Column(Boolean, default=False, comment="是否为回滚操作")
    rollback_of_id = Column(BigInteger, ForeignKey("decisions.id"), comment="回滚的原决策 ID")
    pre_action_state = Column(JSON, comment="执行前的状态快照，用于回滚")

    advertiser = relationship("Advertiser", back_populates="decisions")

    def __repr__(self):
        return f"<Decision {self.action} on {self.data_level}:{self.object_id} [{self.status}]>"


class DecisionImpact(Base, TimestampMixin):
    """
    决策效果追踪表
    
    记录每次决策执行前后的数据对比
    帮助评估决策的实际效果
    """
    __tablename__ = "decision_impacts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 关联的决策
    decision_id = Column(BigInteger, ForeignKey("decisions.id"), nullable=False, index=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"), nullable=False, index=True)

    # 广告/对象信息
    data_level = Column(String(32), comment="CAMPAIGN / ADGROUP / AD")
    object_id = Column(String(128), nullable=False, comment="Ad/AdGroup/Campaign ID")
    object_name = Column(String(512))

    # ===== 决策前数据（baseline）=====
    # 花费、转化、ROAS 等核心指标
    before_spend = Column(Float, comment="决策前花费 $")
    before_conversion = Column(Float, comment="决策前转化数")
    before_impression = Column(Float, comment="决策前展现数")
    before_click = Column(Float, comment="决策前点击数")
    before_ctr = Column(Float, comment="决策前 CTR %")
    before_conversion_rate = Column(Float, comment="决策前转化率 %")
    before_roas = Column(Float, comment="决策前 ROAS")
    before_cpc = Column(Float, comment="决策前 CPC $")
    before_cpm = Column(Float, comment="决策前 CPM $")
    before_bid = Column(Float, comment="决策前出价")
    before_budget = Column(Float, comment="决策前日预算 $")
    before_status = Column(String(32), comment="决策前状态 (ENABLED/PAUSED)")

    # 快照时间
    snapshot_time_before = Column(DateTime(timezone=True), comment="决策前数据采集时间")

    # ===== 决策后数据（current）=====
    after_spend = Column(Float, comment="决策后花费 $")
    after_conversion = Column(Float, comment="决策后转化数")
    after_impression = Column(Float, comment="决策后展现数")
    after_click = Column(Float, comment="决策后点击数")
    after_ctr = Column(Float, comment="决策后 CTR %")
    after_conversion_rate = Column(Float, comment="决策后转化率 %")
    after_roas = Column(Float, comment="决策后 ROAS")
    after_cpc = Column(Float, comment="决策后 CPC $")
    after_cpm = Column(Float, comment="决策后 CPM $")
    after_bid = Column(Float, comment="决策后出价")
    after_budget = Column(Float, comment="决策后日预算 $")
    after_status = Column(String(32), comment="决策后状态")

    # 快照时间
    snapshot_time_after = Column(DateTime(timezone=True), comment="决策后数据采集时间")

    # ===== 变化量（自动计算）=====
    delta_spend = Column(Float, comment="花费变化 $ (正=增加，负=减少)")
    delta_spend_pct = Column(Float, comment="花费变化 % (正=增加，负=减少)")
    delta_conversion = Column(Float, comment="转化变化数")
    delta_conversion_pct = Column(Float, comment="转化变化 %")
    delta_roas = Column(Float, comment="ROAS 变化量 (正=提升，负=下降)")
    delta_roas_pct = Column(Float, comment="ROAS 变化 %")
    delta_cpc = Column(Float, comment="CPC 变化 $ (正=增加，负=减少)")
    delta_ctr = Column(Float, comment="CTR 变化 % 点")

    # ===== 效果评估 =====
    # 根据决策类型来评估效果
    # 如果是"暂停"：期望 ROAS 提升
    # 如果是"加热"：期望花费增加但 ROAS 维持
    # 如果是"降价"：期望转化增加
    is_effective = Column(Boolean, comment="决策是否有效（是否向预期方向改变）")
    effectiveness_score = Column(Float, comment="效果评分 -1.0 ~ 1.0 (-1=最坏，0=无效果，1=最好)")
    
    # 人工评价
    review_notes = Column(Text, comment="人工审查备注")
    reviewed_at = Column(DateTime(timezone=True), comment="审查时间")

    # 是否被回滚
    is_rolled_back = Column(Boolean, default=False, comment="该决策是否被回滚")
    rolled_back_at = Column(DateTime(timezone=True), comment="回滚时间")
    rollback_reason = Column(Text, comment="回滚原因")

    def calculate_deltas(self):
        """自动计算各项变化"""
        if self.before_spend and self.after_spend:
            self.delta_spend = self.after_spend - self.before_spend
            self.delta_spend_pct = (self.delta_spend / self.before_spend * 100) if self.before_spend > 0 else 0

        if self.before_conversion is not None and self.after_conversion is not None:
            self.delta_conversion = self.after_conversion - self.before_conversion
            self.delta_conversion_pct = (
                (self.delta_conversion / self.before_conversion * 100)
                if self.before_conversion > 0 else 0
            )

        if self.before_roas and self.after_roas:
            self.delta_roas = self.after_roas - self.before_roas
            self.delta_roas_pct = (self.delta_roas / self.before_roas * 100) if self.before_roas > 0 else 0

        if self.before_cpc and self.after_cpc:
            self.delta_cpc = self.after_cpc - self.before_cpc

        if self.before_ctr and self.after_ctr:
            self.delta_ctr = self.after_ctr - self.before_ctr

    def evaluate_effectiveness(self, decision_action: str):
        """
        根据决策类型评估效果
        
        decision_action: "pause", "enable", "increase_budget", "decrease_bid", "heat_up" 等
        """
        if decision_action == "pause":
            # 暂停后，期望 ROAS 提升或花费减少
            if self.delta_spend and self.delta_spend < 0:
                if self.delta_roas and self.delta_roas > 0:
                    self.is_effective = True
                    self.effectiveness_score = 1.0
                elif self.delta_roas and self.delta_roas < 0:
                    self.is_effective = False
                    self.effectiveness_score = -0.5
                else:
                    self.is_effective = True
                    self.effectiveness_score = 0.8
            else:
                self.is_effective = False
                self.effectiveness_score = -1.0

        elif decision_action in ["increase_budget", "heat_up"]:
            # 加热，期望转化增加、ROAS 维持
            if self.delta_conversion and self.delta_conversion > 0:
                if self.delta_roas and self.delta_roas > -0.2:  # ROAS 没有大幅下跌
                    self.is_effective = True
                    self.effectiveness_score = 0.8
                else:
                    self.is_effective = True
                    self.effectiveness_score = 0.5  # 转化增加但 ROAS 下跌
            else:
                self.is_effective = False
                self.effectiveness_score = -0.8

        elif decision_action in ["decrease_bid", "lower_bid"]:
            # 降价，期望 CPC 下降，转化不要大幅下跌
            if self.delta_cpc and self.delta_cpc < 0:
                if self.delta_conversion and self.delta_conversion < -0.1:
                    self.is_effective = True
                    self.effectiveness_score = 0.6
                else:
                    self.is_effective = True
                    self.effectiveness_score = 0.9
            else:
                self.is_effective = False
                self.effectiveness_score = -0.5

        else:
            # 其他决策，简单判断
            if self.delta_roas and self.delta_roas > 0:
                self.is_effective = True
                self.effectiveness_score = 0.5
            else:
                self.is_effective = False
                self.effectiveness_score = 0.0
