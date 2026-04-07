"""
验证当前所有 token 能访问的账户
"""
import asyncio
import httpx
from app.core.database import AsyncSessionLocal
from app.core.config import settings
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            "SELECT DISTINCT access_token FROM advertisers WHERE is_active=1"
        ))
        tokens = [row[0] for row in r.fetchall()]

    print(f"共 {len(tokens)} 个不同的 token\n")

    for i, token in enumerate(tokens, 1):
        print(f"=== Token {i}: {token[:20]}... ===")
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.TIKTOK_API_BASE}/open_api/v1.3/oauth2/advertiser/get/",
                headers={"Access-Token": token},
                params={
                    "app_id": settings.TIKTOK_APP_ID,
                    "secret": settings.TIKTOK_APP_SECRET,
                },
            )
            data = resp.json()
            if data.get("code") != 0:
                print(f"  ❌ 错误: {data.get('message')}")
                continue

            adv_list = data.get("data", {}).get("list", [])
            print(f"  可访问 {len(adv_list)} 个广告账户:")
            for a in adv_list:
                adv_id = a.get("advertiser_id")
                adv_name = a.get("advertiser_name")
                print(f"    → {adv_id} | {adv_name}")

asyncio.run(main())
