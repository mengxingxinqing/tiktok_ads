"""
TK 账号模型
"""
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Integer, Numeric
from app.models.base import Base, TimestampMixin


class TkAccount(Base, TimestampMixin):
    """TK 账号（涨粉目标账号）"""
    __tablename__ = "tk_accounts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    account_id = Column(String(64), unique=True, nullable=False, index=True)   # TK username 或数字 ID
    account_name = Column(String(256))
    profile_url = Column(String(512))   # https://www.tiktok.com/@{username}

    # 粉丝数
    follower_count = Column(Integer, default=0)
    follower_updated_at = Column(DateTime(timezone=True), nullable=True)

    # 目标
    target_follower_count = Column(BigInteger, nullable=False)
    target_cost_per_10k = Column(Numeric(10, 4), default=35.0)   # USD

    # 状态：IDLE / RUNNING / COMPLETED / PAUSED / FAILED
    status = Column(String(32), default="IDLE", index=True)

    # 运行时绑定
    bound_ad_account_id = Column(String(64), nullable=True)
    bound_video_id = Column(String(128), nullable=True)

    # Spark Ads / TAP（TikTok Account Spark Code）授权
    # TK 账号用户需在客户端用 "Ad Authorization" 生成 code，系统调 /tt_user/authorize/
    # 把 code 换成 identity_id，挂在某个广告户下
    identity_id = Column(String(128), nullable=True)          # TikTok 返回的 identity_id
    identity_advertiser_id = Column(String(64), nullable=True)  # identity 属于哪个广告户
    tap_authorized_at = Column(DateTime(timezone=True), nullable=True)
    tap_expires_at = Column(DateTime(timezone=True), nullable=True)

    # 达标时间
    completed_at = Column(DateTime(timezone=True), nullable=True)
