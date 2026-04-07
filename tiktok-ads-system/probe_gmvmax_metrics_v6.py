"""
GMVMax Metric Probe v6 - Exhaustive metric discovery

Tests ALL plausible metric names against /gmv_max/report/get/ at multiple dimension levels.

Known valid metrics (confirmed working):
  campaign_id level: cost, orders, gross_revenue, roi, cost_per_order, live_views
  item_id level:     cost, orders, gross_revenue, roi, cost_per_order, product_clicks

This script probes ~200 candidate metric names derived from:
  1. Standard TikTok Ads API metrics (report/integrated/get)
  2. TikTok Shop / onsite event metrics
  3. Naming pattern variations (GMVMax uses "cost" not "spend", etc.)
  4. Supermetrics/Funnel/CData documented field names
  5. Community-discovered fields

Strategy: Test each metric individually with a minimal request.
          Group results by dimension level to find dimension-specific metrics.
"""
import asyncio
import json
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from sqlalchemy import text

ADVERTISER_ID = "7615246831711862800"
STORE_ID = "7494275728565437917"

# Comprehensive list of candidate metrics organized by category
CANDIDATE_METRICS = [
    # =============================================
    # CATEGORY 1: Known valid GMVMax metrics
    # =============================================
    "cost", "orders", "gross_revenue", "roi", "cost_per_order",
    "live_views", "product_clicks",

    # =============================================
    # CATEGORY 2: Standard TikTok Ads API metrics
    # (these use different names in GMVMax, but try anyway)
    # =============================================
    "spend", "impressions", "clicks", "ctr", "cpc", "cpm",
    "conversion", "conversions", "cost_per_conversion", "conversion_rate",
    "reach", "frequency", "cost_per_1000_reached",
    "result", "cost_per_result", "result_rate",
    "video_views", "video_play_actions",
    "video_watched_2s", "video_watched_6s",
    "video_views_p25", "video_views_p50", "video_views_p75", "video_views_p100",
    "average_video_play", "average_video_play_per_user",
    "avg_watch_time", "avg_watch_time_per_view",
    "likes", "comments", "shares", "follows",
    "profile_visits", "profile_visits_rate",
    "clicks_on_music_disc",

    # =============================================
    # CATEGORY 3: E-commerce / Shop metrics (standard API)
    # =============================================
    "complete_payment", "complete_payment_roas",
    "total_complete_payment", "total_complete_payment_rate",
    "onsite_shopping", "total_onsite_shopping_value",
    "onsite_complete_payment", "onsite_complete_payment_value",
    "onsite_initiate_checkout", "onsite_initiate_checkout_count",
    "onsite_add_to_cart", "onsite_add_to_cart_count",
    "onsite_product_detail_page_browse",
    "product_details_page_browse",
    "initiate_checkout", "initiate_checkout_count",
    "add_to_cart", "add_to_cart_count",
    "checkout", "checkouts",
    "purchase", "purchases",
    "total_purchase_value", "purchase_roas",
    "on_web_order", "web_event_add_to_cart",
    "value_per_complete_payment",

    # =============================================
    # CATEGORY 4: GMVMax-specific naming guesses
    # (based on pattern: "cost" instead of "spend")
    # =============================================
    # Revenue / GMV variations
    "revenue", "total_revenue", "net_revenue", "gmv",
    "total_gmv", "gross_merchandise_value",
    "attributed_revenue", "attributed_orders",
    "store_revenue", "store_orders",
    "shop_revenue", "shop_purchases", "shop_orders",
    "ad_revenue", "ad_orders",
    "paid_revenue", "paid_orders",
    "settled_revenue", "settled_orders",
    "confirmed_revenue", "confirmed_orders",
    "total_sales", "total_sales_value", "sales_value",

    # Cost variations
    "billed_cost", "cash_spend", "total_cost", "ad_cost",
    "stat_cost",

    # ROI / ROAS variations
    "roas", "total_roas", "gross_roas",

    # Order variations
    "total_orders", "sku_orders", "total_sku_orders",
    "order_count", "order_amount",

    # Product metrics (GMVMax style)
    "product_views", "product_impressions",
    "product_detail_page_views", "product_detail_views",
    "product_click_rate", "product_ad_clicks",
    "product_ad_impressions", "product_ad_click_rate",
    "total_product_clicks", "total_product_views",

    # Live metrics (GMVMax style)
    "live_viewers", "live_impressions",
    "live_clicks", "live_product_clicks",
    "live_orders", "live_revenue",
    "live_duration", "average_live_duration",
    "live_watch_duration",
    "cost_per_live_view", "cost_per_live_viewer",

    # Video metrics (GMVMax style)
    "video_views_2s", "video_views_6s",
    "video_play", "video_plays",
    "video_completion_rate",
    "video_view_rate",

    # Impression metrics (GMVMax style)
    "impression", "ad_impressions", "paid_impressions",
    "total_impressions", "show_cnt",

    # Click metrics (GMVMax style)
    "click", "ad_clicks", "paid_clicks",
    "total_clicks", "click_cnt",
    "click_rate",

    # Conversion funnel (GMVMax style)
    "add_to_cart_rate", "checkout_rate",
    "payment_rate", "order_rate",
    "conversion_value",

    # CPx metrics
    "cpa", "cost_per_click", "cost_per_impression",
    "cost_per_purchase", "cost_per_checkout",
    "cost_per_add_to_cart",

    # =============================================
    # CATEGORY 5: Supermetrics-discovered fields
    # (from report/integrated/get with service_type)
    # =============================================
    "gmv_max_ads_spend", "gmv_max_ads_billed_cost",
    "roi_protection_compensation_status",

    # =============================================
    # CATEGORY 6: Obscure / undocumented possibilities
    # =============================================
    "net_cost", "gross_cost",
    "refund_amount", "refund_orders", "refund_rate",
    "cancel_orders", "cancel_rate",
    "average_order_value", "aov",
    "new_customers", "returning_customers",
    "unique_visitors", "page_views",
    "bounce_rate", "session_duration",

    # Engagement (GMVMax style)
    "interactions", "engagement_rate",
    "anchor_clicks", "duet_clicks", "stitch_clicks",

    # Attribution
    "cta_conversion", "vta_conversion",
    "cta_purchase", "vta_purchase",
]

# Remove duplicates while preserving order
seen = set()
CANDIDATE_METRICS_UNIQUE = []
for m in CANDIDATE_METRICS:
    if m not in seen:
        seen.add(m)
        CANDIDATE_METRICS_UNIQUE.append(m)

CANDIDATE_METRICS = CANDIDATE_METRICS_UNIQUE


async def probe_dimension_level(client, dimension_config, sd, ed, label):
    """Probe all candidate metrics for a given dimension configuration."""
    print(f"\n{'=' * 70}")
    print(f"  PROBING: {label}")
    print(f"  Dimensions: {dimension_config['dimensions']}")
    if dimension_config.get("filtering"):
        print(f"  Filtering: {dimension_config['filtering']}")
    print(f"{'=' * 70}")

    valid = []
    errors = {}

    for i, metric in enumerate(CANDIDATE_METRICS):
        params = {
            "advertiser_id": ADVERTISER_ID,
            "store_ids": json.dumps([STORE_ID]),
            "dimensions": json.dumps(dimension_config["dimensions"]),
            "metrics": json.dumps([metric]),
            "start_date": sd,
            "end_date": ed,
            "page": 1,
            "page_size": 3,
        }
        if dimension_config.get("filtering"):
            params["filtering"] = json.dumps(dimension_config["filtering"])

        try:
            data = await client._request(
                "GET",
                "/open_api/v1.3/gmv_max/report/get/",
                params=params,
            )
            rows = data.get("list", [])
            sample_val = ""
            if rows:
                m = rows[0].get("metrics", {})
                sample_val = f" => {m.get(metric, '?')}"
            valid.append(metric)
            print(f"  [{i+1}/{len(CANDIDATE_METRICS)}] VALID   {metric}{sample_val}")
        except TikTokAPIError as e:
            msg = str(e.message)
            if "Invalid metric" in msg:
                pass  # Expected - silently skip
            elif "Invalid dimension" in msg:
                print(f"  [{i+1}/{len(CANDIDATE_METRICS)}] DIM_ERR {metric}: {msg}")
                errors[metric] = msg
            else:
                print(f"  [{i+1}/{len(CANDIDATE_METRICS)}] ERROR   {metric}: [{e.code}] {msg}")
                errors[metric] = msg
        except Exception as e:
            print(f"  [{i+1}/{len(CANDIDATE_METRICS)}] EXCEPT  {metric}: {e}")
            errors[metric] = str(e)

        # Rate limiting - small delay every 10 requests
        if (i + 1) % 10 == 0:
            await asyncio.sleep(0.5)

    return valid, errors


async def main():
    # Get access token
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        row = r.fetchone()
        if not row:
            print(f"ERROR: Advertiser {ADVERTISER_ID} not found in database")
            return
        token = row[0]

    client = TikTokClient(access_token=token, advertiser_id=ADVERTISER_ID)
    end = date.today()
    start = end - timedelta(days=7)
    sd, ed = start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    print(f"GMVMax Metric Probe v6")
    print(f"Date range: {sd} to {ed}")
    print(f"Total candidates: {len(CANDIDATE_METRICS)}")

    # First, get a campaign_id and item_group_id for filtering
    print("\n--- Fetching campaign_id for filtering ---")
    campaign_id = None
    item_group_id = None
    try:
        data = await client._request(
            "GET",
            "/open_api/v1.3/gmv_max/report/get/",
            params={
                "advertiser_id": ADVERTISER_ID,
                "store_ids": json.dumps([STORE_ID]),
                "dimensions": json.dumps(["campaign_id", "stat_time_day"]),
                "metrics": json.dumps(["cost"]),
                "start_date": sd,
                "end_date": ed,
                "page": 1,
                "page_size": 5,
            },
        )
        rows = data.get("list", [])
        if rows:
            campaign_id = rows[0].get("dimensions", {}).get("campaign_id")
            print(f"   Found campaign_id: {campaign_id}")
    except Exception as e:
        print(f"   Failed to get campaign_id: {e}")

    if campaign_id:
        try:
            data = await client._request(
                "GET",
                "/open_api/v1.3/gmv_max/report/get/",
                params={
                    "advertiser_id": ADVERTISER_ID,
                    "store_ids": json.dumps([STORE_ID]),
                    "dimensions": json.dumps(["item_group_id", "stat_time_day"]),
                    "metrics": json.dumps(["cost"]),
                    "filtering": json.dumps({"campaign_ids": [campaign_id]}),
                    "start_date": sd,
                    "end_date": ed,
                    "page": 1,
                    "page_size": 5,
                },
            )
            rows = data.get("list", [])
            if rows:
                item_group_id = rows[0].get("dimensions", {}).get("item_group_id")
                print(f"   Found item_group_id: {item_group_id}")
        except Exception as e:
            print(f"   Failed to get item_group_id: {e}")

    # ============================================
    # Level 1: campaign_id dimension
    # ============================================
    results = {}
    valid_campaign, errors_campaign = await probe_dimension_level(
        client,
        {"dimensions": ["campaign_id", "stat_time_day"]},
        sd, ed,
        "LEVEL 1: campaign_id + stat_time_day",
    )
    results["campaign_id"] = valid_campaign

    # ============================================
    # Level 2: item_group_id dimension (needs campaign_ids filter)
    # ============================================
    if campaign_id:
        valid_item_group, errors_item_group = await probe_dimension_level(
            client,
            {
                "dimensions": ["item_group_id", "stat_time_day"],
                "filtering": {"campaign_ids": [campaign_id]},
            },
            sd, ed,
            "LEVEL 2: item_group_id + stat_time_day",
        )
        results["item_group_id"] = valid_item_group

    # ============================================
    # Level 3: item_id dimension (needs campaign + item_group filter)
    # ============================================
    if campaign_id and item_group_id:
        valid_item, errors_item = await probe_dimension_level(
            client,
            {
                "dimensions": ["campaign_id", "item_id", "stat_time_day"],
                "filtering": {
                    "campaign_ids": [campaign_id],
                    "item_group_ids": [item_group_id],
                },
            },
            sd, ed,
            "LEVEL 3: item_id (creative/SKU level)",
        )
        results["item_id"] = valid_item

    # ============================================
    # Level 4: room_id dimension (LIVE)
    # ============================================
    if campaign_id:
        print("\n--- Testing room_id dimension ---")
        try:
            test_data = await client._request(
                "GET",
                "/open_api/v1.3/gmv_max/report/get/",
                params={
                    "advertiser_id": ADVERTISER_ID,
                    "store_ids": json.dumps([STORE_ID]),
                    "dimensions": json.dumps(["room_id", "stat_time_day"]),
                    "metrics": json.dumps(["cost"]),
                    "filtering": json.dumps({"campaign_ids": [campaign_id]}),
                    "start_date": sd,
                    "end_date": ed,
                    "page": 1,
                    "page_size": 3,
                },
            )
            print(f"   room_id dimension is valid! Rows: {len(test_data.get('list', []))}")
            valid_room, errors_room = await probe_dimension_level(
                client,
                {
                    "dimensions": ["room_id", "stat_time_day"],
                    "filtering": {"campaign_ids": [campaign_id]},
                },
                sd, ed,
                "LEVEL 4: room_id (LIVE room level)",
            )
            results["room_id"] = valid_room
        except TikTokAPIError as e:
            print(f"   room_id dimension not available: {e.message}")

    # ============================================
    # SUMMARY
    # ============================================
    print("\n" + "=" * 70)
    print("  FINAL RESULTS SUMMARY")
    print("=" * 70)

    all_valid = set()
    for level, metrics in results.items():
        all_valid.update(metrics)
        print(f"\n--- {level} ({len(metrics)} valid metrics) ---")
        for m in metrics:
            print(f"  - {m}")

    # Show metrics unique to each level
    print(f"\n--- METRICS AVAILABLE AT ALL LEVELS ---")
    if results:
        common = set(results[list(results.keys())[0]])
        for level_metrics in results.values():
            common = common.intersection(set(level_metrics))
        for m in sorted(common):
            print(f"  - {m}")

    print(f"\n--- METRICS UNIQUE TO SPECIFIC LEVELS ---")
    for level, metrics in results.items():
        unique = set(metrics) - set().union(*(
            set(v) for k, v in results.items() if k != level
        )) if len(results) > 1 else set(metrics)
        if unique:
            print(f"  {level} only:")
            for m in sorted(unique):
                print(f"    - {m}")

    print(f"\n{'=' * 70}")
    print(f"TOTAL UNIQUE VALID METRICS: {len(all_valid)}")
    print(f"{'=' * 70}")
    for m in sorted(all_valid):
        print(f"  {m}")

    await client.close()
    print("\nDone!")


asyncio.run(main())
