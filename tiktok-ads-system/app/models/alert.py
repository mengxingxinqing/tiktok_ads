"""
告警记录
"""
from sqlalchemy import Column, String, Float, DateTime, BigInteger, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"), nullable=False, index=True)
    data_level = Column(String(32))
    object_id = Column(String(64), index=True)
    object_name = Column(String(512))

    # 告警类型
    # SPEND_ANOMALY / CTR_DROP / CVR_DROP / BUDGET_DEPLETED / TOKEN_EXPIRY
    # AD_REJECTED / ACCOUNT_SUSPENDED / CPM_SPIKE / TREND_DECLINE
    alert_type = Column(String(64), nullable=False, index=True)
    severity = Column(String(16), default="WARNING", comment="INFO / WARNING / CRITICAL")

    title = Column(String(256), nullable=False)
    message = Column(Text)
    metrics_snapshot = Column(JSON, comment="触发告警时的指标值")

    # 状态
    is_resolved = Column(Boolean, default=False, index=True)
    resolved_at = Column(DateTime(timezone=True))
    notified_at = Column(DateTime(timezone=True), comment="飞书通知发送时间")
