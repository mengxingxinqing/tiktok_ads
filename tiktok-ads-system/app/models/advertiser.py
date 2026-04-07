"""
广告账户模型 — 存储每个广告主的授权信息和 token
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, BigInteger
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Advertiser(Base, TimestampMixin):
    __tablename__ = "advertisers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), unique=True, nullable=False, index=True, comment="TikTok 广告账户 ID")
    advertiser_name = Column(String(256), comment="广告账户名称")

    # OAuth Token
    access_token = Column(Text, nullable=False, comment="访问 token，24h 有效")
    refresh_token = Column(Text, nullable=True, comment="刷新 token（可能不返回），1年有效")
    access_token_expire_at = Column(DateTime(timezone=True), comment="access_token 过期时间")
    refresh_token_expire_at = Column(DateTime(timezone=True), nullable=True, comment="refresh_token 过期时间")

    # 账户状态
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_token_valid = Column(Boolean, default=True, comment="token 是否有效")
    last_sync_at = Column(DateTime(timezone=True), comment="最后一次数据同步时间")
    last_token_refresh_at = Column(DateTime(timezone=True), comment="最后一次 token 刷新时间")

    # 账户信息（从 TikTok 拉取）
    currency = Column(String(8), comment="账户货币")
    timezone = Column(String(64), comment="账户时区")
    account_status = Column(String(32), comment="账户状态")
    balance = Column(String(32), comment="账户余额")

    # 关联
    metrics_snapshots = relationship("MetricsSnapshot", back_populates="advertiser", lazy="dynamic")
    decisions = relationship("Decision", back_populates="advertiser", lazy="dynamic")

    def is_token_expired(self) -> bool:
        """检查 access_token 是否已过期（或即将在30分钟内过期）"""
        if not self.access_token_expire_at:
            return False  # Business Center token 无过期时间，永久有效
        
        from datetime import datetime, timezone, timedelta
        now = datetime.now(timezone.utc)
        expire_at = self.access_token_expire_at
        # 统一转为 aware datetime
        if expire_at.tzinfo is None:
            expire_at = expire_at.replace(tzinfo=timezone.utc)
        threshold = expire_at - timedelta(minutes=30)
        
        return now >= threshold

    def hours_until_expiry(self) -> float:
        """计算还有多少小时直到 token 过期，没有过期时间则返回 inf"""
        if not self.access_token_expire_at:
            return -1  # Business Center token 永不过期，用 -1 表示
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        expire_at = self.access_token_expire_at
        if expire_at.tzinfo is None:
            expire_at = expire_at.replace(tzinfo=timezone.utc)
        delta = expire_at - now
        
        return delta.total_seconds() / 3600

    def __repr__(self):
        return f"<Advertiser {self.advertiser_id} ({self.advertiser_name})>"
