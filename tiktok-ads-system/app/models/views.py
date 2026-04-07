"""
业务视图表 — 由同步任务构建，前端只查这些表
"""
from sqlalchemy import Column, String, Float, BigInteger, Integer, Date, DateTime, Text, Index
from .base import Base, TimestampMixin


class ProductView(Base, TimestampMixin):
    """商品视图：合并 TikTok Shop 商品信息 + GMVMAX_ITEM 投放指标"""
    __tablename__ = "product_view"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    item_group_id = Column(String(128), unique=True, nullable=False, index=True)

    # 商品信息（从 TikTok Shop API）
    title = Column(String(512))
    image_url = Column(Text)
    min_price = Column(Float)
    max_price = Column(Float)
    currency = Column(String(8))
    status = Column(String(32))

    # 关联
    store_id = Column(String(64), index=True)
    advertiser_id = Column(String(64), index=True)

    # 投放指标（从 GMVMAX_ITEM 聚合）
    total_spend = Column(Float, default=0)
    total_orders = Column(Integer, default=0)
    total_revenue = Column(Float, default=0)
    roi = Column(Float, default=0)
    active_days = Column(Integer, default=0)
    first_seen = Column(Date)
    last_seen = Column(Date)

    # 关联创意数
    creative_count = Column(Integer, default=0)


class CreativeView(Base, TimestampMixin):
    """创意视图：合并 GMVMAX_CREATIVE 指标 + 商品信息 + 视频信息"""
    __tablename__ = "creative_view"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    item_id = Column(String(128), unique=True, nullable=False, index=True)
    is_auto_selected = Column(Integer, default=0, comment="1=自动选品")

    # 商品关联
    item_group_id = Column(String(128), index=True)
    product_name = Column(String(512))
    product_image_url = Column(Text)

    # 视频关联（从 creatives 表）
    video_id = Column(String(128))
    video_url = Column(Text)
    cover_url = Column(Text)
    creative_name = Column(String(512))
    duration = Column(Float)

    # 投放指标
    advertiser_id = Column(String(64), index=True)
    campaign_id = Column(String(64))
    total_spend = Column(Float, default=0)
    total_orders = Column(Integer, default=0)
    total_revenue = Column(Float, default=0)
    total_impressions = Column(BigInteger, default=0)
    total_clicks = Column(BigInteger, default=0)
    roi = Column(Float, default=0)
    avg_cost_per_order = Column(Float, default=0)

    # 生命周期
    stage = Column(String(16), comment="WARM_UP/GROWTH/PEAK/DECAY/FATIGUE/DEAD/AUTO")
    trend = Column(String(8), comment="up/stable/down")
    recommendation = Column(String(16))
    reason = Column(String(256))
    daily_avg_spend = Column(Float, default=0)
    active_days = Column(Integer, default=0)
    first_seen = Column(Date)
    last_seen = Column(Date)


class DailySummary(Base, TimestampMixin):
    """每日汇总：按 advertiser_id + stat_date 聚合，含周期对比"""
    __tablename__ = "daily_summary"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    stat_date = Column(Date, nullable=False, index=True)
    advertiser_id = Column(String(64), nullable=False, index=True)

    # Campaign 级汇总
    campaign_count = Column(Integer, default=0)
    total_spend = Column(Float, default=0)
    total_revenue = Column(Float, default=0)
    total_orders = Column(Integer, default=0)
    roi = Column(Float, default=0)

    # Creative 级汇总
    active_creatives = Column(Integer, default=0)
    total_impressions = Column(BigInteger, default=0)
    total_clicks = Column(BigInteger, default=0)

    # 周期对比（构建时计算好，前端直接读）
    spend_vs_yesterday = Column(Float, comment="环比 %")
    revenue_vs_yesterday = Column(Float)
    roi_vs_yesterday = Column(Float)
    spend_vs_last_week = Column(Float, comment="周同比 %")
    revenue_vs_last_week = Column(Float)

    __table_args__ = (
        Index("ix_daily_summary_date_adv", "stat_date", "advertiser_id", unique=True),
    )
