"""
店铺模型 — 持久化 TikTok Shop 店铺信息，避免每次都调 API
"""
from sqlalchemy import Column, String, BigInteger, Boolean, DateTime, Text, JSON
from .base import Base, TimestampMixin


class Store(Base, TimestampMixin):
    __tablename__ = "stores"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    store_id = Column(String(64), unique=True, nullable=False, index=True, comment="TikTok Shop 店铺 ID")
    store_name = Column(String(256), comment="店铺名称")
    store_type = Column(String(32), comment="店铺类型: TIKTOK_SHOP")
    store_code = Column(String(64), comment="店铺编码")

    # 关联
    advertiser_id = Column(String(64), index=True, comment="关联的广告账户 ID")
    store_authorized_bc_id = Column(String(64), comment="授权的 Business Center ID")

    # 地区
    region = Column(String(128), comment="投放地区（逗号分隔）")
    targeting_region_codes = Column(JSON, comment="地区代码列表")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否激活")
    last_synced_at = Column(DateTime(timezone=True), comment="最后同步时间")

    def __repr__(self):
        return f"<Store {self.store_id} ({self.store_name})>"
