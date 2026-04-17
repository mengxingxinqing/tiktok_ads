"""
汇率换算工具
- 从 exchange_rates 表读取 1 <currency> = rate USD
- 内置内存缓存（60 秒），避免每次预算计算都查库
- 未配置汇率的货币回退为 1:1（并记录告警），防止流程硬中断
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional
from datetime import datetime, timezone, timedelta

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exchange_rate import ExchangeRate


_CACHE: Dict[str, Decimal] = {}
_CACHE_AT: Optional[datetime] = None
_CACHE_TTL = timedelta(seconds=60)


async def _load(db: AsyncSession) -> Dict[str, Decimal]:
    global _CACHE, _CACHE_AT
    now = datetime.now(timezone.utc)
    if _CACHE_AT and now - _CACHE_AT < _CACHE_TTL and _CACHE:
        return _CACHE

    result = await db.execute(select(ExchangeRate))
    rows = result.scalars().all()
    cache = {row.currency_from.upper(): Decimal(str(row.rate)) for row in rows}
    cache["USD"] = Decimal("1")   # 恒等
    _CACHE = cache
    _CACHE_AT = now
    return cache


def invalidate_cache():
    """汇率被 upsert 后调用，强制下一次重载。"""
    global _CACHE_AT
    _CACHE_AT = None


async def rate_to_usd(db: AsyncSession, currency: str) -> Decimal:
    """1 <currency> = ? USD。未配置则回退 1:1 并告警。"""
    code = (currency or "USD").upper()
    rates = await _load(db)
    if code in rates:
        return rates[code]
    logger.warning(f"[currency] No exchange rate configured for {code}, using 1:1 fallback")
    return Decimal("1")


async def to_usd(db: AsyncSession, amount, currency: str) -> Decimal:
    """本币金额 → USD。"""
    if amount is None:
        return Decimal("0")
    r = await rate_to_usd(db, currency)
    return (Decimal(str(amount)) * r).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


async def from_usd(db: AsyncSession, amount_usd, currency: str) -> Decimal:
    """USD → 本币金额（用于把系统层预算换算成 TikTok API 期望的本币）。"""
    if amount_usd is None:
        return Decimal("0")
    r = await rate_to_usd(db, currency)
    if r == 0:
        logger.error(f"[currency] Zero rate for {currency}, cannot convert from USD")
        return Decimal("0")
    return (Decimal(str(amount_usd)) / r).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
