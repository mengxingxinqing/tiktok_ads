"""
素材模型 — 素材库（万粉成本维度）

一条 CreativeMaterial = 一次 Spark Ads 授权：
auth_code → /tt_video/authorize/ → /tt_video/list/ → (identity_id, item_id)

⚠️ auth_code 是 advertiser-scoped 的，不能跨户复用。
所以同一个视频想投在两个广告户，需要两条 CreativeMaterial 记录。
"""
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, Numeric, Text
from app.models.base import Base, TimestampMixin


class CreativeMaterial(Base, TimestampMixin):
    """涨粉素材库（独立于 creatives 表）"""
    __tablename__ = "creative_materials"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # 内部唯一 key：(advertiser_id, item_id) 的组合；video_id 保留为外显字段
    video_id = Column(String(128), nullable=False, index=True)
    advertiser_id = Column(String(64), nullable=True, index=True)   # 绑定到哪个广告户

    # Spark Ads 授权信息
    auth_code = Column(String(256), nullable=True)                  # TikTok 创作者生成的授权码
    item_id = Column(String(128), nullable=True, index=True)         # TikTok 原帖 ID
    identity_id = Column(String(128), nullable=True)
    identity_type = Column(String(32), nullable=True, default="AUTH_CODE")
    ad_auth_status = Column(String(32), nullable=True)              # AUTHORIZED / PENDING / EXPIRED
    auth_end_time = Column(DateTime(timezone=True), nullable=True)
    bound_tk_account_id = Column(String(64), nullable=True)         # 这条授权属于哪个 TK 账号

    # 素材信息
    video_url = Column(Text, nullable=True)
    cover_url = Column(Text, nullable=True)
    duration = Column(Numeric(8, 2), nullable=True)   # 秒

    # 万粉成本追踪
    total_spend = Column(Numeric(14, 4), default=0)              # 累计花费 USD
    total_followers_gained = Column(Integer, default=0)           # 累计粉丝增量
    cost_per_10k = Column(Numeric(10, 4), nullable=True)         # = total_spend/total_followers*10000
    sample_count = Column(Integer, default=0)                     # 使用次数

    # Rolling 平均（最近5次）
    avg_cost_per_10k = Column(Numeric(10, 4), nullable=True)
    latest_cost_per_10k = Column(Numeric(10, 4), nullable=True)
