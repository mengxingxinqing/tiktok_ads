"""
尝试所有可能的 data_level 查询账户 7615246831711862800 的数据
"""
import asyncio
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from sqlalchemy import text

ADVERTISER_ID = "7615246831711862800"

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"))
        token = r.fetchone()[0]

    client = TikTokClient(access_token=token, advertiser_id=ADVERTISER_ID)
    end = date.today()
    start = (end - timedelta(days=30)).strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    # 先查账户基本信息
    print("=== 账户基本信息 ===")
    try:
        resp = await client._request("GET", "/open_api/v1.3/advertiser/info/",
            params={"advertiser_ids": f'["{ADVERTISER_ID}"]'})
        info = resp.get("list", [{}])[0] if resp.get("list") else {}
        print(f"  名称: {info.get('name')}")
        print(f"  状态: {info.get('status')}")
        print(f"  余额: {info.get('balance')}")
        print(f"  货币: {info.get('currency')}")
    except Exception as e:
        print(f"  查询失败: {e}")

    # 尝试不同 data_level
    data_levels = [
        ("AUCTION_CAMPAIGN", '["campaign_id","stat_time_day"]'),
        ("AUCTION_ADGROUP", '["adgroup_id","stat_time_day"]'),
        ("AUCTION_AD", '["ad_id","stat_time_day"]'),
    ]

    print(f"\n=== 报表查询（{start} ~ {end_str}）===")
    for level, dims in data_levels:
        try:
            data = await client._request("GET", "/open_api/v1.3/report/integrated/get/",
                params={
                    "advertiser_id": ADVERTISER_ID,
                    "report_type": "BASIC",
                    "data_level": level,
                    "dimensions": dims,
                    "metrics": '["spend","impressions","clicks"]',
                    "start_date": start,
                    "end_date": end_str,
                    "page_size": 3,
                }
            )
            total = data.get("page_info", {}).get("total_number", 0)
            rows = data.get("list", [])
            print(f"  {level}: {total} 条")
            for row in rows[:2]:
                print(f"    {row}")
        except TikTokAPIError as e:
            print(f"  {level}: API错误 - {e.message[:80]}")

    # 直接查 ad 列表（不通过报表）
    print("\n=== 直接查 Ad 列表 ===")
    try:
        data = await client._request("GET", "/open_api/v1.3/ad/get/",
            params={"advertiser_id": ADVERTISER_ID, "page_size": 5})
        total = data.get("page_info", {}).get("total_number", 0)
        ads = data.get("list", [])
        print(f"  广告总数: {total}")
        for ad in ads[:3]:
            print(f"    {ad.get('ad_id')} | {ad.get('ad_name')} | status:{ad.get('operation_status')}")
    except TikTokAPIError as e:
        print(f"  查询失败: {e.message[:80]}")

    await client.close()

asyncio.run(main())
