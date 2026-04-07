"""
广告评论模型 — 存储 TikTok 广告下的用户评论数据
"""
from sqlalchemy import Column, String, BigInteger, Text, Boolean, DateTime, Index, Integer
from .base import Base, TimestampMixin


class AdComment(Base, TimestampMixin):
    """
    广告评论表

    每条评论的唯一标识是 comment_id
    通过 ad_id 关联到具体广告
    """
    __tablename__ = "ad_comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 归属
    advertiser_id = Column(String(64), nullable=False, index=True, comment="广告账户 ID")
    ad_id = Column(String(64), nullable=False, index=True, comment="广告 ID")
    campaign_id = Column(String(64), index=True, comment="Campaign ID")

    # 评论基础信息
    comment_id = Column(String(128), unique=True, nullable=False, index=True, comment="TikTok 评论唯一 ID")
    parent_comment_id = Column(String(128), index=True, comment="父评论 ID（回复时有值）")
    content = Column(Text, comment="评论内容")
    user_id = Column(String(128), comment="评论者用户 ID")
    user_name = Column(String(256), comment="评论者用户名")
    user_avatar = Column(Text, comment="评论者头像 URL")

    # 互动数据
    likes = Column(Integer, default=0, comment="点赞数")
    replies = Column(Integer, default=0, comment="回复数")

    # 状态
    status = Column(String(32), default="PUBLIC", comment="PUBLIC / HIDDEN / DELETED")
    is_owner_replied = Column(Boolean, default=False, comment="广告主是否已回复")

    # 情感分析（由我们系统计算）
    sentiment = Column(String(16), comment="POSITIVE / NEUTRAL / NEGATIVE")
    sentiment_score = Column(Integer, comment="情感得分 -100 ~ 100")

    # TikTok 原始时间
    comment_time = Column(DateTime(timezone=True), comment="评论发布时间")

    __table_args__ = (
        Index("ix_comment_ad_time", "ad_id", "comment_time"),
        Index("ix_comment_adv_time", "advertiser_id", "comment_time"),
        Index("ix_comment_sentiment", "advertiser_id", "sentiment"),
    )

    def __repr__(self):
        return f"<AdComment {self.comment_id} ad={self.ad_id} sentiment={self.sentiment}>"


class BlockedWord(Base, TimestampMixin):
    """
    评论屏蔽词表

    通过 TikTok API 管理，自动过滤包含屏蔽词的评论
    """
    __tablename__ = "blocked_words"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    advertiser_id = Column(String(64), nullable=False, index=True, comment="广告账户 ID")
    word = Column(String(256), nullable=False, comment="屏蔽词")
    blocked_word_id = Column(String(128), comment="TikTok 返回的屏蔽词 ID")
    is_active = Column(Boolean, default=True, comment="是否启用")

    __table_args__ = (
        Index("ix_blocked_word_adv", "advertiser_id", "word"),
    )

    def __repr__(self):
        return f"<BlockedWord {self.word} adv={self.advertiser_id}>"
