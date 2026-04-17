"""
Ad Account 授权 + 同步服务

复用现有 Business Center OAuth 授权流程，
授权后将 BC 下的所有广告账户同步到 ad_accounts 表
"""
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from decimal import Decimal
from loguru import logger

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.tiktok_client import TikTokClient
from app.models.ad_account import AdAccount
from app.services import currency as fx
# NOTE: 有意不 import app.models.advertiser —— 涨粉模块与 gmvmax 的 advertisers 表完全隔离


class AdAccountSyncService:
    """
    将 Business Center 授权的账户同步到 ad_accounts 表

    流程：
    1. 从涨粉模块自己的 ad_accounts BC 代表行获取 access_token
    2. 对每个 advertiser，同步余额和基本信息
    3. 如 ad_accounts 表中不存在，则新建；存在则更新
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def sync_all_from_bc(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        token_expire_at=None,
        owner_advertiser_id: Optional[str] = None,
    ) -> Dict[str, int]:
        """
        从 Business Center 同步所有广告账户

        Args:
            access_token: Business Center 的 access_token
            refresh_token: 同一授权下的 refresh_token（用于后续自动续期）
            token_expire_at: token 过期时间
            owner_advertiser_id: 授权发起方（BC 代表户），若非空则新建/更新的 AdAccount
                                 会在 token_owner_advertiser_id 记录，表示共享同一 token

        Returns:
            {"created": N, "updated": M, "failed": K}
        """
        client = TikTokClient(access_token=access_token, advertiser_id="0")
        try:
            advertiser_list = await client.get_advertiser_list(access_token)
        finally:
            await client.close()

        created = 0
        updated = 0
        failed = 0

        for adv in advertiser_list:
            advertiser_id = adv.get("advertiser_id")
            if not advertiser_id:
                continue

            try:
                # 获取该广告账户的详细信息（余额）
                result = await self._sync_single(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_expire_at=token_expire_at,
                    owner_advertiser_id=owner_advertiser_id,
                    advertiser_id=advertiser_id,
                    adv_data=adv,
                )
                if result == "created":
                    created += 1
                elif result == "updated":
                    updated += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"[AdAccountSync] Failed to sync {advertiser_id}: {e}")
                failed += 1

        logger.info(f"[AdAccountSync] Done: created={created}, updated={updated}, failed={failed}")
        return {"created": created, "updated": updated, "failed": failed}

    async def _sync_single(
        self,
        access_token: str,
        advertiser_id: str,
        adv_data: Dict,
        refresh_token: Optional[str] = None,
        token_expire_at=None,
        owner_advertiser_id: Optional[str] = None,
    ) -> str:
        """同步单个广告账户"""
        # 查 ad_accounts 表
        result = await self.db.execute(
            select(AdAccount).where(AdAccount.advertiser_id == advertiser_id)
        )
        existing = result.scalar_one_or_none()

        # 获取最新余额
        client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
        try:
            balance_data = await client.get_balance()
        except Exception as e:
            logger.warning(f"[AdAccountSync] get_balance failed for {advertiser_id}: {e}")
            balance_data = {}
        finally:
            await client.close()

        balance = balance_data.get("balance", 0)
        currency = adv_data.get("currency", "USD")
        balance_decimal = Decimal(str(balance)) if balance else Decimal("0")
        balance_usd = await fx.to_usd(self.db, balance_decimal, currency)

        if existing:
            # 更新：token 只有是自己授权或属于同一 owner 时才覆盖
            existing.advertiser_name = adv_data.get("advertiser_name", existing.advertiser_name)
            existing.balance = balance_decimal if balance else existing.balance
            existing.balance_usd = balance_usd if balance else existing.balance_usd
            existing.currency = currency
            existing.balance_updated_at = datetime.now(timezone.utc)
            # 同一来源的 token 覆盖；不同来源（已有独立授权）不要覆盖
            if existing.token_owner_advertiser_id == owner_advertiser_id or existing.token_owner_advertiser_id is None and owner_advertiser_id is None:
                existing.access_token = access_token
                if refresh_token:
                    existing.refresh_token = refresh_token
                if token_expire_at:
                    existing.token_expire_at = token_expire_at
            return "updated"
        else:
            # 新建
            new_acct = AdAccount(
                advertiser_id=advertiser_id,
                advertiser_name=adv_data.get("advertiser_name", ""),
                access_token=access_token,
                refresh_token=refresh_token,
                token_expire_at=token_expire_at,
                token_owner_advertiser_id=owner_advertiser_id,
                currency=currency,
                balance=balance_decimal,
                balance_usd=balance_usd,
                balance_updated_at=datetime.now(timezone.utc),
                is_active=True,
                priority=5,
                allow_use=True,
            )
            self.db.add(new_acct)
            return "created"

    async def sync_balance(self, advertiser_id: str, access_token: str) -> Decimal:
        """
        单独同步某个账户的余额

        Returns:
            最新余额
        """
        client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
        try:
            balance_data = await client.get_balance()
        finally:
            await client.close()

        balance = Decimal(str(balance_data.get("balance", 0)))

        result = await self.db.execute(
            select(AdAccount).where(AdAccount.advertiser_id == advertiser_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            balance_usd = await fx.to_usd(self.db, balance, existing.currency)
            existing.balance = balance
            existing.balance_usd = balance_usd
            existing.balance_updated_at = datetime.now(timezone.utc)
            # 余额不足自动降级：按 USD 口径 < $10
            if balance_usd < Decimal("10"):
                existing.is_active = False
                logger.info(
                    f"[AdAccountSync] {advertiser_id} balance low "
                    f"({balance} {existing.currency} ≈ ${balance_usd}), deactivated"
                )
            else:
                existing.is_active = True

        await self.db.commit()
        return balance

    async def refresh_all_balances(self):
        """
        定时任务：刷新所有 ad_accounts 的余额
        顺带刷新即将过期的 access_token
        """
        result = await self.db.execute(
            select(AdAccount).where(AdAccount.allow_use == True)
        )
        accounts = result.scalars().all()

        for acct in accounts:
            # 自动刷新即将过期的 token（<24h）
            try:
                await self._ensure_token_fresh(acct)
            except Exception as e:
                logger.error(f"[AdAccountSync] refresh token failed for {acct.advertiser_id}: {e}")
                continue

            try:
                await self.sync_balance(acct.advertiser_id, acct.access_token)
                logger.debug(f"[BalanceSync] {acct.advertiser_id}: {acct.balance} {acct.currency}")
            except Exception as e:
                logger.error(f"[BalanceSync] {acct.advertiser_id} failed: {e}")

        await self.db.commit()

    async def _ensure_token_fresh(self, acct: AdAccount) -> None:
        """
        如果 access_token 24h 内将过期，用 refresh_token 刷新；
        token_owner_advertiser_id 非空表示 token 来自 BC，此时该 BC 代表户同步即可，
        其他依赖同 token 的广告户走 _propagate_refreshed_token 统一更新。
        """
        from datetime import datetime, timezone, timedelta
        if not acct.refresh_token:
            return
        if acct.token_expire_at and acct.token_expire_at > datetime.now(timezone.utc) + timedelta(hours=24):
            return

        data = await TikTokClient.refresh_token(acct.refresh_token)
        new_token = data.get("access_token")
        new_refresh = data.get("refresh_token")
        expires_in = data.get("expires_in") or 0
        if not new_token:
            return

        expire_at = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
        acct.access_token = new_token
        if new_refresh:
            acct.refresh_token = new_refresh
        acct.token_expire_at = expire_at
        logger.info(f"[AdAccountSync] Token refreshed for {acct.advertiser_id}, expire_at={expire_at}")

        # 如果这个账户是 BC 代表（被其他户共享了同一 token），同步刷新其他户
        if acct.token_owner_advertiser_id is None:
            await self._propagate_refreshed_token(
                owner_advertiser_id=acct.advertiser_id,
                access_token=new_token,
                refresh_token=new_refresh or acct.refresh_token,
                expire_at=expire_at,
            )

    async def _propagate_refreshed_token(
        self,
        owner_advertiser_id: str,
        access_token: str,
        refresh_token: str,
        expire_at,
    ) -> None:
        result = await self.db.execute(
            select(AdAccount).where(AdAccount.token_owner_advertiser_id == owner_advertiser_id)
        )
        peers = result.scalars().all()
        for peer in peers:
            peer.access_token = access_token
            peer.refresh_token = refresh_token
            peer.token_expire_at = expire_at
        if peers:
            logger.info(f"[AdAccountSync] Propagated refreshed token to {len(peers)} peers of {owner_advertiser_id}")
