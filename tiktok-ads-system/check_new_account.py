"""
检查新账户 7615246831711862800 的数据
"""
import asyncio
from datetime import date, timedelta
import httpx
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from app.core.config import settings
from sqlalchemy import text

ADVERTISER_ID = "7615246831711862800"

async def main():
    # 1. 查数据库
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT advertiser_id, advertiser_name, is_active, is_token_valid, access_token "
            f"FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        row = r.fetchone()

    if not row:
        print(f"❌ 账户 {ADVERTISER_ID} 不在数据库中，需要授权")
        
        # 检查现有 token 能否访问这个账户
        async with AsyncSessionLocal() as db:
            r2 = await db.execute(text("SELECT DISTINCT access_token FROM advertisers WHERE is_active=1"))
            tokens = [r[0] for r in r2.fetchall()]

        print(f"\n尝试用现有 {len(tokens)} 个 token 访问...")
        for token in tokens:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{settings.TIKTOK_API_BASE}/open_api/v1.3/oauth2/advertiser/get/",
                    headers={"Access-Token": token},
                    params={"app_id": settings.TIKTOK_APP_ID, "secret": settings.TIKTOK_APP_SECRET},
                )
                adv_list = resp.json().get("data", {}).get("list", [])
                ids = [a["advertiser_id"] for a in adv_list]
                if ADVERTISER_ID in ids:
                    print(f"✅ Token {token[:20]}... 可以访问这个账户！")
                    print("→ 只需要将这个账户加入数据库即可，不需要重新授权")
                    # 直接用这个 token 查数据
                    await check_data(token)
                    return
                else:
                    print(f"❌ Token {token[:20]}... 无法访问")
        
        print("\n结论：这个账户不在任何已授权的 BC 下，需要让该账户所属 BC 重新授权")
        return

    print(f"✅ 账户已在数据库: {row[1]} | is_active={row[2]} | is_token_valid={row[3]}")
    await check_data(row[4])


async def check_data(token):
    client = TikTokClient(access_token=token, advertiser_id=ADVERTISER_ID)
    end = date.today()
    start = end - timedelta(days=30)

    print(f"\n查询近 30 天报表 ({start} ~ {end})...")
    
    # Campaign 数
    try:
        data = await client._request("GET", "/open_api/v1.3/campaign/get/",
            params={"advertiser_id": ADVERTISER_ID, "page_size": 10})
        total = data.get("page_info", {}).get("total_number", 0)
        campaigns = data.get("list", [])
        print(f"推广计划: {total} 个")
        for c in campaigns[:5]:
            print(f"  - {c.get('campaign_id')} | {c.get('campaign_name')} | {c.get('objective_type')} | {c.get('operation_status')}")
    except TikTokAPIError as e:
        print(f"Campaign 查询失败: {e}")

    # 报表数据
    try:
        report = await client._request("GET", "/open_api/v1.3/report/integrated/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "report_type": "BASIC",
                "data_level": "AUCTION_CAMPAIGN",
                "dimensions": '["campaign_id","stat_time_day"]',
                "metrics": '["spend","impressions","clicks","conversion"]',
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": end.strftime("%Y-%m-%d"),
                "page_size": 5,
            }
        )
        total = report.get("page_info", {}).get("total_number", 0)
        rows = report.get("list", [])
        print(f"\n近 30 天报表: {total} 条数据")
        for row in rows[:3]:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})
            print(f"  {dims.get('stat_time_day')} | campaign:{dims.get('campaign_id')} | spend:{metrics.get('spend')} | conv:{metrics.get('conversion')}")
    except TikTokAPIError as e:
        print(f"报表查询失败: {e}")

    await client.close()


asyncio.run(main())
