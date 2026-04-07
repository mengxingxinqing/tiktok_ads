"""
检查 token 的权限范围，以及账户的真实关系
"""
import asyncio
import httpx
from app.core.database import AsyncSessionLocal
from app.core.config import settings
from sqlalchemy import text

ADVERTISER_ID = "7615246831711862800"

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        token = r.fetchone()[0]

    print(f"Token: {token[:30]}...")

    async with httpx.AsyncClient(timeout=15.0) as client:
        # 1. 这个 token 能访问哪些账户
        resp = await client.get(
            f"{settings.TIKTOK_API_BASE}/open_api/v1.3/oauth2/advertiser/get/",
            headers={"Access-Token": token},
            params={"app_id": settings.TIKTOK_APP_ID, "secret": settings.TIKTOK_APP_SECRET},
        )
        data = resp.json()
        print(f"\n=== 该 token 关联的广告账户 ===")
        print(f"code: {data.get('code')}, message: {data.get('message')}")
        for a in data.get("data", {}).get("list", []):
            marker = "⭐" if a["advertiser_id"] == ADVERTISER_ID else "  "
            print(f"  {marker} {a['advertiser_id']} | {a['advertiser_name']}")

        # 2. 尝试获取这个账户下的 shop 绑定信息
        resp2 = await client.get(
            f"{settings.TIKTOK_API_BASE}/open_api/v1.3/store/list/",
            headers={"Access-Token": token},
            params={"advertiser_id": ADVERTISER_ID},
        )
        d2 = resp2.json()
        print(f"\n=== 绑定的 Shop ===")
        print(f"code: {d2.get('code')}, message: {d2.get('message')}")
        stores = d2.get("data", {}).get("stores", []) or d2.get("data", {}).get("list", [])
        for s in stores:
            print(f"  shop_id: {s.get('store_id') or s.get('shop_id')} | {s.get('store_name') or s.get('name')}")

        # 3. 查 BC 信息 — 看这个账户归属于哪个 BC
        resp3 = await client.get(
            f"{settings.TIKTOK_API_BASE}/open_api/v1.3/bc/advertiser/get/",
            headers={"Access-Token": token},
            params={"bc_id": "", "page_size": 20},
        )
        d3 = resp3.json()
        print(f"\n=== BC 下的广告账户 ===")
        print(f"code: {d3.get('code')}, message: {d3.get('message')}")
        for a in d3.get("data", {}).get("list", []):
            marker = "⭐" if a.get("advertiser_id") == ADVERTISER_ID else "  "
            print(f"  {marker} {a.get('advertiser_id')} | {a.get('name') or a.get('advertiser_name')}")

asyncio.run(main())
