"""
GMVMax 诊断脚本 v2
使用 GMVMax 专属端点查询数据

关系链: BC(b1) → Advertiser(a1) → Shop(s1)
"""
import asyncio
import json
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from sqlalchemy import text

ADVERTISER_ID = "7615246831711862800"


async def main():
    # 1. 获取 token
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        row = r.fetchone()
        if not row:
            print(f"❌ 广告户 {ADVERTISER_ID} 不在数据库中")
            return
        token = row[0]

    client = TikTokClient(access_token=token, advertiser_id=ADVERTISER_ID)

    # ============================================
    # Step 1: 获取关联的店铺列表
    # ============================================
    print("=" * 60)
    print("Step 1: 获取关联店铺 (GET /store/list/)")
    print("=" * 60)
    store_ids = []
    try:
        stores = await client.get_gmvmax_store_list()
        if stores:
            print(f"✅ 找到 {len(stores)} 个店铺:")
            for s in stores:
                sid = s.get("store_id") or s.get("shop_id") or s.get("id")
                name = s.get("store_name") or s.get("name") or "未知"
                print(f"   店铺 ID: {sid} | 名称: {name}")
                print(f"   原始数据: {json.dumps(s, ensure_ascii=False)}")
                if sid:
                    store_ids.append(str(sid))
        else:
            print("⚠️  返回空列表")
    except TikTokAPIError as e:
        print(f"❌ API 错误: {e}")

    # ============================================
    # Step 2: 直接用 _request 裸调 GMVMax campaign 列表
    #         试不同的端点和参数组合
    # ============================================
    print("\n" + "=" * 60)
    print("Step 2: 探测 GMVMax Campaign（多种方式）")
    print("=" * 60)

    # 2a: /campaign/gmv_max/info/ 不带 campaign_id（看返回什么）
    print("\n--- 2a: /campaign/gmv_max/info/ (无 filtering) ---")
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/campaign/gmv_max/info/",
            params={"advertiser_id": ADVERTISER_ID},
        )
        print(f"   返回: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except TikTokAPIError as e:
        print(f"   错误 [{e.code}]: {e.message}")

    # 2b: /campaign/get/ 不加 fields 过滤，全量返回
    print("\n--- 2b: /campaign/get/ (全量字段) ---")
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/campaign/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "page_size": 50,
            },
        )
        campaigns = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"   总数: {total}")
        for c in campaigns[:5]:
            print(f"   {json.dumps(c, ensure_ascii=False)}")
    except TikTokAPIError as e:
        print(f"   错误 [{e.code}]: {e.message}")

    # 2c: /campaign/get/ 加 objective_type filtering
    print("\n--- 2c: /campaign/get/ filtering PRODUCT_SALES ---")
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/campaign/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "page_size": 50,
                "filtering": json.dumps({"objective_type": "PRODUCT_SALES"}),
            },
        )
        campaigns = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"   PRODUCT_SALES 总数: {total}")
        for c in campaigns[:5]:
            print(f"   {json.dumps(c, ensure_ascii=False)}")
    except TikTokAPIError as e:
        print(f"   错误 [{e.code}]: {e.message}")

    # 2d: /campaign/get/ filtering SHOP_PURCHASES
    print("\n--- 2d: /campaign/get/ filtering SHOP_PURCHASES ---")
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/campaign/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "page_size": 50,
                "filtering": json.dumps({"objective_type": "SHOP_PURCHASES"}),
            },
        )
        campaigns = data.get("list", [])
        total = data.get("page_info", {}).get("total_number", 0)
        print(f"   SHOP_PURCHASES 总数: {total}")
        for c in campaigns[:5]:
            print(f"   {json.dumps(c, ensure_ascii=False)}")
    except TikTokAPIError as e:
        print(f"   错误 [{e.code}]: {e.message}")

    # ============================================
    # Step 3: GMVMax 报表 — 用最少的 metrics 试
    # ============================================
    if store_ids:
        print("\n" + "=" * 60)
        print(f"Step 3: GMVMax 报表探测 store_ids={store_ids}")
        print("=" * 60)
        end = date.today()
        start = end - timedelta(days=7)

        # 3a: 最小 metrics 集合
        for metrics_set_name, metrics_list in [
            ("minimal_v1", ["spend", "complete_payment_roas"]),
            ("minimal_v2", ["total_complete_payment_rate", "complete_payment_roas"]),
            ("cost_only", ["cost"]),
            ("shop_metrics", ["total_sales_value", "total_orders"]),
        ]:
            print(f"\n--- 3a: metrics={metrics_set_name} ---")
            try:
                data = await client._request(
                    "GET",
                    "/open_api/v1.3/gmv_max/report/get/",
                    params={
                        "advertiser_id": ADVERTISER_ID,
                        "store_ids": json.dumps(store_ids),
                        "dimensions": json.dumps(["stat_time_day"]),
                        "metrics": json.dumps(metrics_list),
                        "start_date": start.strftime("%Y-%m-%d"),
                        "end_date": end.strftime("%Y-%m-%d"),
                        "page": 1,
                        "page_size": 10,
                    },
                )
                rows = data.get("list", [])
                total = data.get("page_info", {}).get("total_number", 0)
                print(f"   ✅ 成功! {total} 条记录")
                for row in rows[:3]:
                    print(f"   {json.dumps(row, ensure_ascii=False)}")
                break  # 找到有效的就停
            except TikTokAPIError as e:
                print(f"   ❌ [{e.code}]: {e.message}")

    # ============================================
    # Step 4: 查 BC 下所有广告户（确认账户关系）
    # ============================================
    print("\n" + "=" * 60)
    print("Step 4: 查当前 token 能访问的所有广告户")
    print("=" * 60)
    try:
        advertisers = await TikTokClient.get_advertiser_list(token)
        print(f"✅ 共 {len(advertisers)} 个广告户:")
        for adv in advertisers:
            print(f"   ID: {adv.get('advertiser_id')} | 名称: {adv.get('advertiser_name')}")
    except Exception as e:
        print(f"❌ 错误: {e}")

    await client.close()
    print("\n✅ 诊断完成")


asyncio.run(main())
