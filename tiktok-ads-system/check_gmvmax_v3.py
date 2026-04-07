"""
GMVMax 诊断脚本 v3
修复: dimensions 必须有 1-3 个主维度(排除 stat_time_day/stat_time_hour)
同时测试两个广告户: 591$ 和 Jingshun Hall Store
"""
import asyncio
import json
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from sqlalchemy import text

# 两个可能的广告户
ADVERTISERS = {
    "7615246831711862800": "591$",
    "7616286272197574663": "Jingshun Hall Store",
}

STORE_ID = "7494275728565437917"


async def test_advertiser(adv_id: str, adv_name: str, token: str):
    print(f"\n{'#' * 60}")
    print(f"# 测试广告户: {adv_name} ({adv_id})")
    print(f"{'#' * 60}")

    client = TikTokClient(access_token=token, advertiser_id=adv_id)

    # 1. 查店铺
    print("\n--- 店铺列表 ---")
    try:
        stores = await client.get_gmvmax_store_list()
        if stores:
            for s in stores:
                print(f"   店铺: {s.get('store_id')} | {s.get('store_name')} | 区域: {s.get('targeting_region_codes')}")
        else:
            print("   无关联店铺")
    except TikTokAPIError as e:
        print(f"   错误: {e}")

    # 2. 普通 campaign/get
    print("\n--- 普通 Campaign 列表 ---")
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/campaign/get/",
            params={"advertiser_id": adv_id, "page_size": 50},
        )
        campaigns = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"   总数: {total}")
        for c in campaigns[:10]:
            print(f"   ID: {c.get('campaign_id')} | {c.get('campaign_name')} | objective: {c.get('objective_type')} | status: {c.get('operation_status')}")
    except TikTokAPIError as e:
        print(f"   错误: {e}")

    # 3. GMVMax 报表 — 用 campaign_id 作为主维度
    print("\n--- GMVMax 报表 (campaign_id 维度) ---")
    end = date.today()
    start = end - timedelta(days=30)
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/gmv_max/report/get/",
            params={
                "advertiser_id": adv_id,
                "store_ids": json.dumps([STORE_ID]),
                "dimensions": json.dumps(["campaign_id", "stat_time_day"]),
                "metrics": json.dumps(["spend", "complete_payment_roas"]),
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": end.strftime("%Y-%m-%d"),
                "page": 1,
                "page_size": 20,
            },
        )
        rows = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"   ✅ {total} 条记录")
        for row in rows[:5]:
            print(f"   {json.dumps(row, ensure_ascii=False)}")
    except TikTokAPIError as e:
        print(f"   ❌ [{e.code}]: {e.message}")

    # 4. GMVMax 报表 — 用 ad_id 作为主维度
    print("\n--- GMVMax 报表 (ad_id 维度) ---")
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/gmv_max/report/get/",
            params={
                "advertiser_id": adv_id,
                "store_ids": json.dumps([STORE_ID]),
                "dimensions": json.dumps(["ad_id", "stat_time_day"]),
                "metrics": json.dumps(["spend", "complete_payment_roas"]),
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": end.strftime("%Y-%m-%d"),
                "page": 1,
                "page_size": 20,
            },
        )
        rows = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"   ✅ {total} 条记录")
        for row in rows[:5]:
            print(f"   {json.dumps(row, ensure_ascii=False)}")
    except TikTokAPIError as e:
        print(f"   ❌ [{e.code}]: {e.message}")

    await client.close()


async def main():
    # 获取所有广告户的 token（BC 级别 token 通用）
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            "SELECT access_token FROM advertisers WHERE advertiser_id = '7615246831711862800'"
        ))
        row = r.fetchone()
        if not row:
            print("❌ 找不到 token")
            return
        token = row[0]

    for adv_id, adv_name in ADVERTISERS.items():
        await test_advertiser(adv_id, adv_name, token)

    print("\n\n✅ 全部诊断完成")


asyncio.run(main())
