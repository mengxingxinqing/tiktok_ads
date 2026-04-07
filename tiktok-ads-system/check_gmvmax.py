"""
检查 GMVMAX 账户的数据
"""
import asyncio, json
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from sqlalchemy import text

ADVERTISER_ID = "7620344099409018898"

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        token = r.fetchone()[0]

    client = TikTokClient(access_token=token, advertiser_id=ADVERTISER_ID)

    # 1. 查所有推广计划（不加 fields 过滤，看原始数据）
    print("=== 查推广计划（全量字段）===")
    try:
        import httpx
        resp = await client._request(
            "GET",
            "/open_api/v1.3/campaign/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "page_size": 20,
            },
        )
        campaigns = resp.get("list", [])
        total = resp.get("page_info", {}).get("total_number", 0)
        print(f"总数: {total}")
        for c in campaigns:
            print(f"  ID: {c.get('campaign_id')} | 名称: {c.get('campaign_name')} | 目标: {c.get('objective_type')} | 状态: {c.get('operation_status')}/{c.get('secondary_status')}")
    except Exception as e:
        print(f"错误: {e}")

    # 2. 查 SHOPPING_SALES 报表（GMVMAX 用的是这个 data_level）
    print("\n=== 查 SHOPPING_SALES 报表 ===")
    end = date.today()
    start = end - timedelta(days=30)
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/report/integrated/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "report_type": "BASIC",
                "data_level": "AUCTION_CAMPAIGN",
                "dimensions": '["campaign_id","stat_time_day"]',
                "metrics": '["spend","impressions","clicks","conversion"]',
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": end.strftime("%Y-%m-%d"),
                "page_size": 10,
            },
        )
        rows = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"CAMPAIGN 报表: {total} 条")
        for row in rows[:5]:
            print(f"  {row}")
    except Exception as e:
        print(f"错误: {e}")

    # 3. 尝试 LIVE_COMMERCE data_level（直播电商）
    print("\n=== 查广告组（全量）===")
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/adgroup/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "page_size": 10,
            },
        )
        adgroups = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"广告组总数: {total}")
        for ag in adgroups[:5]:
            print(f"  ID: {ag.get('adgroup_id')} | 名称: {ag.get('adgroup_name')} | campaign: {ag.get('campaign_id')} | 状态: {ag.get('operation_status')}")
    except Exception as e:
        print(f"错误: {e}")

    await client.close()

asyncio.run(main())
