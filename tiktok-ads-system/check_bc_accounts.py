"""
查询 Business Center 下所有可访问的广告账户
可能 GMVMAX 投放是在子账户（店铺的 advertiser_id）下，不是在当前账户下
"""
import asyncio
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient
from app.core.config import settings
from sqlalchemy import text
import httpx

# 先看数据库里存了哪些账户
async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            "SELECT advertiser_id, advertiser_name, access_token FROM advertisers WHERE is_active=1"
        ))
        accounts = r.fetchall()

    print(f"=== 数据库中的账户 ({len(accounts)} 个) ===")
    for adv_id, name, token in accounts:
        print(f"  {adv_id} | {name}")

    # 用每个 token 查询它能访问的所有 advertiser_ids
    print("\n=== 各 token 能访问的账户列表 ===")
    seen_tokens = set()
    for adv_id, name, token in accounts:
        if token in seen_tokens:
            continue
        seen_tokens.add(token)

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
            adv_list = data.get("data", {}).get("list", [])
            print(f"\n  Token ({token[:16]}...) 可访问 {len(adv_list)} 个账户:")
            for a in adv_list:
                print(f"    → {a.get('advertiser_id')} | {a.get('advertiser_name')}")

asyncio.run(main())
