"""
指标快照模型 — 每 30 分钟存一次，是历史趋势分析的基础
"""
from sqlalchemy import Column, String, Float, DateTime, BigInteger, ForeignKey, Index, Date
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class MetricsSnapshot(Base, TimestampMixin):
    """
    Campaign / AdGroup / Ad 三层统一存储，用 data_level 区分
    """
    __tablename__ = "metrics_snapshots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 归属
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"), nullable=False, index=True)
    data_level = Column(String(32), nullable=False, comment="CAMPAIGN / ADGROUP / AD")
    object_id = Column(String(64), nullable=False, index=True, comment="对应层级的 ID")
    object_name = Column(String(512), comment="名称")
    stat_date = Column(Date, nullable=False, comment="统计日期（TikTok 数据日期）")
    snapshot_time = Column(DateTime(timezone=True), nullable=False, comment="本次采集时间")

    # 父级关联
    campaign_id = Column(String(64), index=True)
    adgroup_id = Column(String(64), index=True)

    # 商品关联（用于成本管理和商品发现）
    product_id = Column(String(128), index=True, comment="TikTok Shop 商品 ID（如有）")
    sku_id = Column(String(128), comment="SKU ID")

    # 状态
    object_status = Column(String(32), comment="ENABLE / DISABLE / DELETE / REVIEW")

    # === 核心投放指标 ===
    spend = Column(Float, default=0.0, comment="花费")
    impressions = Column(BigInteger, default=0, comment="曝光量")
    clicks = Column(BigInteger, default=0, comment="点击量")
    ctr = Column(Float, default=0.0, comment="点击率 %")
    cpm = Column(Float, default=0.0, comment="千次曝光成本")
    cpc = Column(Float, default=0.0, comment="单次点击成本")

    # === 转化指标 ===
    conversion = Column(BigInteger, default=0, comment="转化数")
    cost_per_conversion = Column(Float, default=0.0, comment="转化成本")
    conversion_rate = Column(Float, default=0.0, comment="转化率 %")
    real_time_conversion = Column(BigInteger, default=0, comment="实时转化数")
    real_time_cost_per_conversion = Column(Float, default=0.0, comment="实时转化成本")

    # === 视频指标（TikTok 特有）===
    video_play_actions = Column(BigInteger, default=0, comment="视频播放次数")
    video_watched_2s = Column(BigInteger, default=0, comment="2秒完播数")
    video_watched_6s = Column(BigInteger, default=0, comment="6秒完播数")
    average_video_play = Column(Float, default=0.0, comment="平均播放时长(秒)")
    video_view_rate = Column(Float, default=0.0, comment="完播率 %")

    # === GMVMax 专属指标 ===
    gross_revenue = Column(Float, default=0.0, comment="GMV 收入（GMVMax）")
    roi = Column(Float, default=0.0, comment="投资回报率 ROI（GMVMax）")
    live_views = Column(BigInteger, default=0, comment="直播观看数（GMVMax）")

    # === 渠道来源拆分（GMVMax 专属）===
    source_type = Column(String(32), nullable=True, comment="订单来源：SELF_OWNED/AFFILIATE/ALL")
    affiliate_id = Column(String(64), nullable=True, index=True, comment="达人 ID（AFFILIATE 来源时有值）")
    affiliate_name = Column(String(256), nullable=True, comment="达人名称")
    commission_amount = Column(Float, default=0.0, comment="达人佣金金额")
    commission_rate = Column(Float, default=0.0, comment="达人佣金率 %")

    # 预算信息（AdGroup/Campaign 层）
    budget = Column(Float, comment="设置预算")
    bid_price = Column(Float, comment="出价")

    advertiser = relationship("Advertiser", back_populates="metrics_snapshots")

    __table_args__ = (
        # 联合索引：快速查某个对象在某个时间段内的历史数据
        Index("ix_metrics_object_date", "object_id", "stat_date"),
        Index("ix_metrics_advertiser_level", "advertiser_id", "data_level", "stat_date"),
    )

    def __repr__(self):
        return f"<MetricsSnapshot {self.data_level}:{self.object_id} @ {self.stat_date}>"
