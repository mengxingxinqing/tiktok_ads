"""
重试配置模型
"""
from sqlalchemy import Column, String, BigInteger, Integer, Numeric
from app.models.base import Base, TimestampMixin


class RetryConfig(Base, TimestampMixin):
    """投放任务重试配置（管理员可调）"""
    __tablename__ = "retry_configs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    action_type = Column(String(32), unique=True, nullable=False)  # AD_CREATION / FOLLOWER_SYNC / TOKEN_REFRESH
    max_retries = Column(BigInteger, default=3)
    base_delay_seconds = Column(Integer, default=10)   # 初始延迟
    multiplier = Column(Numeric(4, 2), default=2.0)   # 延迟倍数
