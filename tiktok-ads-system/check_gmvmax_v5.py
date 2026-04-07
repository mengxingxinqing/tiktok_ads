"""
GMVMax v5: 已知 cost/orders 有效，继续探测更多 metrics
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
    sd, ed = start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    # 基于已知的 cost/orders，大量探测
    candidates = [
        # 花费/成本相关
        "cost", "billed_cost", "cash_spend", "total_cost",
        # GMV/收入
        "gmv", "revenue", "total_revenue", "gross_revenue",
        "total_sales", "total_sales_value", "sales_value",
        "gross_merchandise_value",
        # 订单
        "orders", "total_orders", "complete_payment",
        "total_complete_payment", "purchase",
        # ROAS
        "roas", "complete_payment_roas", "purchase_roas", "roi",
        # 展示/点击
        "impressions", "impression", "show_cnt",
        "clicks", "click_cnt", "click",
        "ctr", "cpc", "cpm", "cpa",
        # 转化
        "conversion", "conversions", "conversion_rate",
        "cost_per_conversion", "cost_per_order",
        "cost_per_result",
        # 视频
        "video_views", "video_play", "video_play_actions",
        "video_watched_2s", "video_watched_6s",
        "average_video_play",
        # 互动
        "likes", "comments", "shares", "follows",
        "reach", "frequency",
        # 商品
        "product_clicks", "product_views",
        "product_detail_page_views", "add_to_cart",
        "initiate_checkout", "checkout",
        # 直播
        "live_views", "live_viewers",
        # 网站事件
        "page_views", "page_view",
        # 通用
        "result", "results", "result_rate",
        "cost_per_1000_reached",
        # 可能的 GMVMax 专有
        "attributed_revenue", "attributed_orders",
        "store_revenue", "store_orders",
        "shop_purchases", "shop_revenue",
        "ad_revenue", "ad_orders",
        "paid_orders", "paid_revenue",
        "settled_revenue", "settled_orders",
        "confirmed_revenue", "confirmed_orders",
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
                    "page_size": 3,
                },
            )
            rows = data.get("list", [])
            total = data.get("page_info", {}).get("total_number", 0)
            valid_metrics.append(metric)
            sample = ""
            if rows:
                m = rows[0].get("metrics", {})
                sample = f" => {m.get(metric, '?')}"
            print(f"✅ {metric}{sample}")
        except TikTokAPIError as e:
            if "Invalid metric" in str(e.message):
                pass
            else:
                print(f"⚠️  {metric}: [{e.code}] {e.message}")

    print(f"\n{'=' * 60}")
    print(f"有效 GMVMax metrics ({len(valid_metrics)} 个):")
    print(f"{'=' * 60}")
    for m in valid_metrics:
        print(f"  - {m}")

    # 用所有有效 metrics 拉一次完整数据
    if valid_metrics:
        print(f"\n{'=' * 60}")
        print("完整数据（所有有效 metrics，30 天）")
        print(f"{'=' * 60}")
        start30 = end - timedelta(days=30)
        try:
            data = await client._request(
                "GET",
                "/open_api/v1.3/gmv_max/report/get/",
                params={
                    "advertiser_id": ADVERTISER_ID,
                    "store_ids": json.dumps([STORE_ID]),
                    "dimensions": json.dumps(["campaign_id", "stat_time_day"]),
                    "metrics": json.dumps(valid_metrics),
                    "start_date": start30.strftime("%Y-%m-%d"),
                    "end_date": ed,
                    "page": 1,
                    "page_size": 50,
                },
            )
            rows = data.get("list", [])
            total = data.get("page_info", {}).get("total_number", 0)
            print(f"总记录数: {total}")
            for row in rows[:10]:
                dims = row.get("dimensions", {})
                metrics = row.get("metrics", {})
                print(f"\n日期: {dims.get('stat_time_day')} | campaign: {dims.get('campaign_id')}")
                for k, v in metrics.items():
                    print(f"   {k}: {v}")
        except TikTokAPIError as e:
            print(f"❌ [{e.code}]: {e.message}")

    # 测试 ad_id 维度
    if valid_metrics:
        print(f"\n{'=' * 60}")
        print("ad_id 维度数据")
        print(f"{'=' * 60}")
        try:
            data = await client._request(
                "GET",
                "/open_api/v1.3/gmv_max/report/get/",
                params={
                    "advertiser_id": ADVERTISER_ID,
                    "store_ids": json.dumps([STORE_ID]),
                    "dimensions": json.dumps(["ad_id", "stat_time_day"]),
                    "metrics": json.dumps(valid_metrics),
                    "start_date": start30.strftime("%Y-%m-%d"),
                    "end_date": ed,
                    "page": 1,
                    "page_size": 20,
                },
            )
            rows = data.get("list", [])
            total = data.get("page_info", {}).get("total_number", 0)
            print(f"总记录数: {total}")
            for row in rows[:5]:
                print(f"   {json.dumps(row, ensure_ascii=False)}")
        except TikTokAPIError as e:
            print(f"❌ [{e.code}]: {e.message}")

    await client.close()
    print("\n✅ 完成")


asyncio.run(main())
