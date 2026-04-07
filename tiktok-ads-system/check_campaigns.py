import asyncio
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient
from sqlalchemy import text

ADVERTISER_ID = "7620344099409018898"

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        token = r.fetchone()[0]

    client = TikTokClient(access_token=token, advertiser_id=ADVERTISER_ID)
    
    # 查推广计划
    data = await client.get_campaigns()
    campaigns = data.get("list", [])
    total = data.get("page_info", {}).get("total_number", 0)
    print(f"推广计划总数: {total}")
    for c in campaigns[:10]:
        print(f"  Campaign: {c.get('campaign_id')} | {c.get('campaign_name')} | 状态: {c.get('status')}")
    
    # 如果有计划，查广告
    if campaigns:
        cid = campaigns[0]["campaign_id"]
        data2 = await client.get_ads()
        ads = data2.get("list", [])
        total2 = data2.get("page_info", {}).get("total_number", 0)
        print(f"\n广告总数: {total2}")
        for a in ads[:5]:
            print(f"  Ad: {a.get('ad_id')} | {a.get('ad_name')} | 状态: {a.get('status')}")
    
    await client.close()

asyncio.run(main())
