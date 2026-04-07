"""
素材分组模型
- CreativeGroup: 素材分组
- CreativeGroupItem: 分组内素材条目
"""
from sqlalchemy import Column, String, BigInteger, Boolean, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class CreativeGroup(Base, TimestampMixin):
    """素材分组"""
    __tablename__ = "creative_groups"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=True, index=True)
    name = Column(String(128), nullable=False, comment="分组名称")
    description = Column(Text, nullable=True)
    color = Column(String(16), default="#6366f1")
    is_active = Column(Boolean, default=True)

    items = relationship("CreativeGroupItem", back_populates="group",
                         cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self):
        return f"<CreativeGroup {self.id} name={self.name}>"


class CreativeGroupItem(Base, TimestampMixin):
    """分组内素材条目"""
    __tablename__ = "creative_group_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, ForeignKey("creative_groups.id", ondelete="CASCADE"),
                      nullable=False, index=True)
    advertiser_id = Column(String(64), nullable=False, index=True)
    video_id = Column(String(128), nullable=False, index=True)
    creative_name = Column(String(512), nullable=True, comment="冗余存储素材名称")

    group = relationship("CreativeGroup", back_populates="items")

    __table_args__ = (
        UniqueConstraint("group_id", "video_id", name="uq_group_video"),
    )

    def __repr__(self):
        return f"<CreativeGroupItem group={self.group_id} video={self.video_id}>"
