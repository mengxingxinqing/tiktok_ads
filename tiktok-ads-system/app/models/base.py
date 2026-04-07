from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.mysql import DATETIME


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """
    MySQL 兼容的时间戳 Mixin
    用 DATETIME(6) 保留微秒精度
    """
    created_at = Column(
        DATETIME(fsp=6),
        server_default=func.now(6),
        nullable=False,
    )
    updated_at = Column(
        DATETIME(fsp=6),
        server_default=func.now(6),
        onupdate=func.now(6),
        nullable=False,
    )
