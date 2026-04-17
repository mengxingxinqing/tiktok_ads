"""
汇率配置模型
"""
from sqlalchemy import Column, String, BigInteger, Numeric, DateTime
from app.models.base import Base, TimestampMixin


class ExchangeRate(Base, TimestampMixin):
    """币种汇率表（管理员配置）"""
    __tablename__ = "exchange_rates"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    currency_from = Column(String(8), nullable=False)   # 如 JPY
    currency_to = Column(String(8), nullable=False, default="USD")
    rate = Column(Numeric(14, 6), nullable=False)     # 1 currency_from = rate USD
