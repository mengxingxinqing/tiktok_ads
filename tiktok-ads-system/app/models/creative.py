"""
素材模型
- Creative: 素材基础信息（video_id 维度）
- CreativeSnapshot: 每次采集的素材聚合指标（跨 Ad 聚合）
"""
from sqlalchemy import Column, String, Float, DateTime, BigInteger, ForeignKey, Index, Date, Integer, Text, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class LifecycleStage(str, enum.Enum):
    """素材投放生命周期"""
    WARM_UP  = "WARM_UP"   # 冷启动（<3天或曝光<1000）
    GROWTH   = "GROWTH"    # 上升期
    PEAK     = "PEAK"      # 峰值期
    DECAY    = "DECAY"     # 衰退期
    FATIGUE  = "FATIGUE"   # 疲劳（建议更换）
    UNKNOWN  = "UNKNOWN"


class CreativeStatus(str, enum.Enum):
    """素材审核和投放状态"""
    PENDING_REVIEW    = "PENDING_REVIEW"     # 待审核（刚上传，TikTok 还在审）
    APPROVED          = "APPROVED"           # 审核通过（可以投放）
    REJECTED          = "REJECTED"           # 审核不通过（被拒）
    UNDER_LEARNING    = "UNDER_LEARNING"     # 学习中（已投放但还在优化算法）
    ACTIVE            = "ACTIVE"             # 投放中（正常投放，数据稳定）
    PAUSED            = "PAUSED"             # 手动暂停（人为停止）
    FATIGUE           = "FATIGUE"            # 疲劳（系统检测到疲劳）
    DISABLED          = "DISABLED"           # 已禁用（永久下线）
    ARCHIVED          = "ARCHIVED"           # 已归档（历史素材）


class Creative(Base, TimestampMixin):
    """
    素材基础信息表
    主键是 (advertiser_id, video_id) —— 同一素材在不同账户下独立跟踪
    """
    __tablename__ = "creatives"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)
    video_id      = Column(String(128), nullable=False, index=True, comment="TikTok 视频素材 ID")
    ad_id         = Column(String(64), index=True, comment="首次发现该素材的 Ad ID")

    # ===== 素材基础信息 =====
    creative_name   = Column(String(512), comment="素材名称（从 Ad 名称推断）")
    video_url       = Column(Text, comment="视频播放地址")
    cover_url       = Column(Text, comment="封面图地址")
    duration        = Column(Float, comment="视频时长（秒）")
    width           = Column(Integer, comment="视频宽度")
    height          = Column(Integer, comment="视频高度")

    # ===== 素材状态 =====
    status = Column(String(32), default=CreativeStatus.PENDING_REVIEW, index=True,
                   comment="审核和投放状态")
    review_status = Column(String(32), comment="审核状态详情")
    review_reject_reason = Column(Text, comment="如果被拒，拒绝原因")
    review_time = Column(DateTime(timezone=True), comment="审核时间")

    # ===== 关联信息 =====
    shop_id     = Column(String(128), index=True, comment="TikTok Shop ID")
    shop_name   = Column(String(256), comment="店铺名称")
    product_id  = Column(String(128), index=True, comment="关联的商品 ID（若有）")
    product_name = Column(String(512), comment="商品名称")

    # ===== 生命周期 =====
    first_seen_date  = Column(Date, comment="首次采集到数据的日期")
    last_active_date = Column(Date, comment="最近有数据的日期")
    days_running     = Column(Integer, default=0, comment="已投放天数")
    lifecycle_stage  = Column(String(16), default=LifecycleStage.UNKNOWN, index=True,
                            comment="WARM_UP / GROWTH / PEAK / DECAY / FATIGUE")
    is_fatigue       = Column(String(1), default="N", index=True, comment="Y=已疲劳")

    # ===== 性能指标（最新）=====
    latest_hook_rate = Column(Float, comment="最新 Hook Rate %")
    latest_hold_rate = Column(Float, comment="最新 Hold Rate %")
    latest_roas = Column(Float, comment="最新 ROAS")
    latest_ctr = Column(Float, comment="最新 CTR %")
    total_spend = Column(Float, default=0.0, comment="累计花费")
    total_conversion = Column(BigInteger, default=0, comment="累计转化")
    total_impression = Column(BigInteger, default=0, comment="累计展现")

    # 关联
    snapshots = relationship("CreativeSnapshot", back_populates="creative", lazy="dynamic")

    __table_args__ = (
        Index("ix_creative_adv_video", "advertiser_id", "video_id", unique=True),
        Index("ix_creative_status", "status"),
        Index("ix_creative_lifecycle", "lifecycle_stage"),
        Index("ix_creative_shop", "shop_id"),
        Index("ix_creative_product", "product_id"),
        Index("ix_creative_created", "created_at"),
    )

    def __repr__(self):
        return f"<Creative {self.video_id} status={self.status} lifecycle={self.lifecycle_stage}>"


class CreativeSnapshot(Base, TimestampMixin):
    """
    素材每日快照 — 每 30 分钟采集，同一天多条（取最新）
    数据来源：把同一 video_id 下所有 Ad 的指标聚合
    """
    __tablename__ = "creative_snapshots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)
    video_id      = Column(String(128), nullable=False, index=True)
    stat_date     = Column(Date, nullable=False)
    snapshot_time = Column(DateTime(timezone=True), nullable=False)

    # 关联 Creative
    creative_id   = Column(BigInteger, ForeignKey("creatives.id"), index=True)

    # === 基础投放指标 ===
    ad_count      = Column(Integer, default=0, comment="使用该素材的 Ad 数量")
    spend         = Column(Float, default=0.0, comment="总花费")
    impressions   = Column(BigInteger, default=0)
    clicks        = Column(BigInteger, default=0)
    ctr           = Column(Float, default=0.0, comment="%")
    cpm           = Column(Float, default=0.0)
    cpc           = Column(Float, default=0.0)
    conversion    = Column(BigInteger, default=0)
    cost_per_conversion = Column(Float, default=0.0)
    conversion_rate     = Column(Float, default=0.0)

    # === 素材核心指标（TikTok 特有）===
    video_play_actions = Column(BigInteger, default=0, comment="播放次数")
    video_watched_2s   = Column(BigInteger, default=0, comment="2秒播放数")
    video_watched_6s   = Column(BigInteger, default=0, comment="6秒播放数")
    average_video_play = Column(Float, default=0.0, comment="平均播放时长(秒)")

    # === 计算指标（采集时算好，便于查询）===
    hook_rate        = Column(Float, default=0.0, comment="前2秒留存率 = watched_2s/plays %")
    hold_rate        = Column(Float, default=0.0, comment="前6秒留存率 = watched_6s/plays %")
    # 注：完播率需要 video_views_p100，TikTok API 字段名为 video_play_actions（完整播放）

    # 生命周期快照
    days_running     = Column(Integer, default=0)
    lifecycle_stage  = Column(String(16), default=LifecycleStage.UNKNOWN)

    creative = relationship("Creative", back_populates="snapshots")

    __table_args__ = (
        Index("ix_cs_video_date", "video_id", "stat_date"),
        Index("ix_cs_adv_date",   "advertiser_id", "stat_date"),
    )

    def __repr__(self):
        return f"<CreativeSnapshot {self.video_id} @ {self.stat_date} hook={self.hook_rate:.1f}%>"


class CreativeHeatUp(Base, TimestampMixin):
    """
    素材加热操作记录
    
    记录每次对素材的"加热"操作（增加预算、创建新 Ad、提高出价等）
    并追踪加热后的效果
    """
    __tablename__ = "creative_heatups"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)
    video_id = Column(String(128), nullable=False, index=True, comment="被加热的素材 ID")
    creative_id = Column(BigInteger, ForeignKey("creatives.id"))

    # 加热信息
    heatup_type = Column(String(32), comment="INCREASE_BUDGET / NEW_AD / RAISE_BID / CLONE_AD")
    heatup_reason = Column(Text, comment="为什么要加热该素材")
    heatup_params = Column(Text, comment="加热参数，如 budget +50%, cpc +0.2 等")

    # === 加热前数据 ===
    before_daily_spend = Column(Float, comment="加热前日花费")
    before_ctr = Column(Float, comment="加热前 CTR %")
    before_conversion = Column(Float, comment="加热前日转化数")
    before_roas = Column(Float, comment="加热前 ROAS")
    before_hook_rate = Column(Float, comment="加热前 Hook Rate %")
    before_hold_rate = Column(Float, comment="加热前 Hold Rate %")
    before_bid = Column(Float, comment="加热前出价")
    before_budget = Column(Float, comment="加热前预算")
    before_lifecycle = Column(String(16), comment="加热前生命周期阶段")

    snapshot_before = Column(DateTime(timezone=True), comment="加热前数据采集时间")

    # === 加热后数据（n 天后采集）===
    after_daily_spend = Column(Float, comment="加热后日花费")
    after_ctr = Column(Float, comment="加热后 CTR %")
    after_conversion = Column(Float, comment="加热后日转化数")
    after_roas = Column(Float, comment="加热后 ROAS")
    after_hook_rate = Column(Float, comment="加热后 Hook Rate %")
    after_hold_rate = Column(Float, comment="加热后 Hold Rate %")
    after_bid = Column(Float, comment="加热后出价")
    after_budget = Column(Float, comment="加热后预算")
    after_lifecycle = Column(String(16), comment="加热后生命周期阶段")

    snapshot_after = Column(DateTime(timezone=True), comment="加热后数据采集时间")

    # === 效果指标 ===
    delta_spend = Column(Float, comment="花费变化 $")
    delta_spend_pct = Column(Float, comment="花费变化 %")
    delta_conversion = Column(Float, comment="转化变化数")
    delta_conversion_pct = Column(Float, comment="转化变化 %")
    delta_roas = Column(Float, comment="ROAS 变化")
    delta_roas_pct = Column(Float, comment="ROAS 变化 %")
    delta_ctr = Column(Float, comment="CTR 变化 % 点")
    delta_hook_rate = Column(Float, comment="Hook Rate 变化 % 点")

    # === 效果评估 ===
    is_successful = Column(String(1), default="N", comment="Y = 加热成功（转化增加）")
    success_score = Column(Float, comment="成功评分 0 ~ 1.0")
    roi_on_heatup = Column(Float, comment="加热的投资回报率 = delta_conversion_value / delta_spend")

    # 人工评价
    notes = Column(Text, comment="人工备注")
    reviewed_at = Column(DateTime(timezone=True), comment="审查时间")

    # 是否已被回滚（取消加热）
    is_rolled_back = Column(String(1), default="N")
    rolled_back_at = Column(DateTime(timezone=True))
    rollback_reason = Column(Text)

    creative = relationship("Creative")

    __table_args__ = (
        Index("ix_heatup_adv_video", "advertiser_id", "video_id"),
        Index("ix_heatup_success", "is_successful"),
    )

    def calculate_deltas(self):
        """计算加热效果指标"""
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

        if self.before_ctr and self.after_ctr:
            self.delta_ctr = self.after_ctr - self.before_ctr

        if self.before_hook_rate and self.after_hook_rate:
            self.delta_hook_rate = self.after_hook_rate - self.before_hook_rate

    def evaluate_success(self):
        """评估加热是否成功"""
        # 加热成功的标志：转化增加且 ROAS 不低于加热前
        if self.delta_conversion and self.delta_conversion > 0:
            if self.delta_roas is None or self.delta_roas >= -0.2:  # ROAS 没有大幅下跌
                self.is_successful = "Y"
                
                # 计算加热投资回报率（简化，假设转化价值为 ROAS 乘以花费）
                if self.delta_spend and self.delta_spend > 0:
                    delta_value = self.delta_conversion * 50  # 假设每个转化价值 $50
                    self.roi_on_heatup = delta_value / self.delta_spend if self.delta_spend > 0 else 0

                # 评分逻辑
                if self.delta_roas and self.delta_roas > 0:
                    # 转化增加且 ROAS 提升
                    self.success_score = 1.0
                elif self.delta_roas and self.delta_roas < -0.2:
                    # 转化增加但 ROAS 明显下跌
                    self.success_score = 0.6
                else:
                    # 转化增加，ROAS 维持
                    self.success_score = 0.8
            else:
                self.is_successful = "N"
                self.success_score = 0.3
        else:
            self.is_successful = "N"
            self.success_score = 0.0
