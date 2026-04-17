"""
Ads 账户模型 — 智能涨粉模块专用表（独立于 advertisers 表）
"""
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Numeric
from app.models.base import Base, TimestampMixin


class AdAccount(Base, TimestampMixin):
    """Ads 托管账户"""
    __tablename__ = "ad_accounts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), unique=True, nullable=False, index=True)
    advertiser_name = Column(String(256))

    # OAuth Token
    # access_token 来源可以是 BC 级 token（多户共用同一 BC 授权）或账户独立授权
    # 当 token_owner_advertiser_id 非空时表示 token 是从某 BC 拿到的（该 advertiser 是 BC 代表）
    access_token = Column(String(2048), nullable=False)
    refresh_token = Column(String(2048), nullable=True)
    token_expire_at = Column(DateTime(timezone=True), nullable=True)
    token_owner_advertiser_id = Column(String(64), nullable=True)  # 授权给 token 的账户（BC 代表）

    # 账户信息
    currency = Column(String(8), nullable=False, default="USD")
    balance = Column(Numeric(14, 4), default=0)     # 本币余额
    balance_usd = Column(Numeric(14, 4), nullable=True)  # 换算成 USD 的余额快照
    balance_updated_at = Column(DateTime(timezone=True), nullable=True)

    # 状态
    is_active = Column(Boolean, default=True)     # 余额不足时自动=False
    priority = Column(BigInteger, default=5)    # 1=最高优先
    allow_use = Column(Boolean, default=True)   # 管理员可手动禁用

    # 预算预留：待启动/运行中 Campaign 占用的 USD 预算，避免超卖
    reserved_budget_usd = Column(Numeric(14, 4), default=0)
