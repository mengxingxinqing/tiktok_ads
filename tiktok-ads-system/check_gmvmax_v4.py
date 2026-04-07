"""
GMVMax 诊断脚本 v4
探测正确的 metric 名称 + 尝试 service_type=TT_SHOP 方式
"""
import asyncio
import json
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from sqlalchemy import text

ADVERTISER_ID = "7615246831711862800"
STORE_ID = "7494275728565437917"


async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        token = r.fetchone()[0]

    client = TikTokClient(access_token=token, advertiser_id=ADVERTISER_ID)
    end = date.today()
    start = end - timedelta(days=7)
    sd = start.strftime("%Y-%m-%d")
    ed = end.strftime("%Y-%m-%d")

    # ============================================
    # 方式 1: report/integrated/get + service_type=TT_SHOP
    # 这是 Supermetrics/Airbyte 等工具实际用的方式
    # ============================================
    print("=" * 60)
    print("方式 1: report/integrated/get + service_type=TT_SHOP")
    print("=" * 60)

    for data_level in ["AUCTION_CAMPAIGN", "AUCTION_ADGROUP", "AUCTION_AD"]:
        print(f"\n--- data_level={data_level} ---")
        dim_map = {
            "AUCTION_CAMPAIGN": ["campaign_id", "stat_time_day"],
            "AUCTION_ADGROUP": ["adgroup_id", "stat_time_day"],
            "AUCTION_AD": ["ad_id", "stat_time_day"],
        }
        try:
            data = await client._request(
                "GET",
                "/open_api/v1.3/report/integrated/get/",
                params={
                    "advertiser_id": ADVERTISER_ID,
                    "service_type": "TT_SHOP",
                    "report_type": "BASIC",
                    "data_level": data_level,
                    "dimensions": json.dumps(dim_map[data_level]),
                    "metrics": json.dumps([
                        "spend", "impressions", "clicks", "ctr", "cpm", "cpc",
                        "conversion", "cost_per_conversion",
                    ]),
                    "start_date": sd,
                    "end_date": ed,
                    "page": 1,
                    "page_size": 20,
                },
            )
            rows = data.get("list", [])
            total = data.get("page_info", {}).get("total_number", 0)
            print(f"   ✅ {total} 条记录")
            for row in rows[:3]:
                print(f"   {json.dumps(row, ensure_ascii=False)}")
        except TikTokAPIError as e:
            print(f"   ❌ [{e.code}]: {e.message}")

    # ============================================
    # 方式 2: gmv_max/report/get 逐个试 metric
    # ============================================
    print("\n" + "=" * 60)
    print("方式 2: gmv_max/report/get 逐个探测 metric")
    print("=" * 60)

    # 可能的 metric 名称（各种命名风格）
    candidates = [
        # TT_SHOP 前缀风格 (Supermetrics 发现的)
        "TT_SHOP_spend", "TT_SHOP_billed_cost",
        # 驼峰风格
        "totalCost", "totalSpend", "totalGmv",
        # 下划线风格
        "total_cost", "total_spend", "total_gmv",
        "gross_merchandise_value", "ad_cost",
        "total_purchase_value", "purchase_roas",
        # 简单名
        "cost", "gmv", "roas", "orders", "revenue",
        "billed_cost", "cash_spend",
        # 商店相关
        "shop_purchases", "shop_revenue",
        "product_orders", "product_revenue",
        # video 相关
        "video_views", "reach",
        # CPA 相关
        "cpa", "cpc", "cpm",
        # 完整支付相关
        "complete_payment", "complete_payment_roas",
        "onsite_complete_payment", "onsite_complete_payment_value",
        "total_complete_payment", "total_complete_payment_rate",
        # 结算相关
        "stat_cost", "show_cnt", "click_cnt",
    ]

    valid_metrics = []
    for metric in candidates:
        try:
            data = await client._request(
                "GET",
                "/open_api/v1.3/gmv_max/report/get/",
                params={
                    "advertiser_id": ADVERTISER_ID,
                    "store_ids": json.dumps([STORE_ID]),
                    "dimensions": json.dumps(["campaign_id", "stat_time_day"]),
                    "metrics": json.dumps([metric]),
                    "start_date": sd,
                    "end_date": ed,
                    "page": 1,
                    "page_size": 5,
                },
            )
            rows = data.get("list", [])
            total = data.get("page_info", {}).get("total_number", 0)
            print(f"   ✅ {metric}: 有效! ({total} 条)")
            valid_metrics.append(metric)
            if rows:
                print(f"      示例: {json.dumps(rows[0], ensure_ascii=False)}")
        except TikTokAPIError as e:
            if "Invalid metric" in str(e.message):
                pass  # 静默跳过无效的
            else:
                print(f"   ⚠️  {metric}: [{e.code}] {e.message}")

    print(f"\n✅ 有效 metrics: {valid_metrics}")

    # ============================================
    # 方式 3: 如果方式1成功了，看看有没有 campaign 数据
    # ============================================
    print("\n" + "=" * 60)
    print("方式 3: 不带 service_type, 30天范围")
    print("=" * 60)
    start30 = end - timedelta(days=30)
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/report/integrated/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "report_type": "BASIC",
                "data_level": "AUCTION_CAMPAIGN",
                "dimensions": json.dumps(["campaign_id", "stat_time_day"]),
                "metrics": json.dumps(["spend", "impressions", "clicks"]),
                "start_date": start30.strftime("%Y-%m-%d"),
                "end_date": ed,
                "page": 1,
                "page_size": 20,
            },
        )
        rows = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"   普通报表 30天: {total} 条记录")
        for row in rows[:5]:
            print(f"   {json.dumps(row, ensure_ascii=False)}")
    except TikTokAPIError as e:
        print(f"   ❌ [{e.code}]: {e.message}")

    await client.close()
    print("\n✅ 诊断完成")


asyncio.run(main())
