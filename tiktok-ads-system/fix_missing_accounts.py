"""
将 token 下所有账户同步到数据库，并查报表验证
"""
import asyncio
from datetime import date, timedelta, datetime, timezone
import httpx
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from app.models.advertiser import Advertiser
from app.core.config import settings
from sqlalchemy import text, select

# 用已知有效的 token
TOKEN = "07f57abb41f446b356da76ff3e3d6a4221be41e4"

async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{settings.TIKTOK_API_BASE}/open_api/v1.3/oauth2/advertiser/get/",
            headers={"Access-Token": TOKEN},
            params={"app_id": settings.TIKTOK_APP_ID, "secret": settings.TIKTOK_APP_SECRET},
        )
        adv_list = resp.json().get("data", {}).get("list", [])

    print(f"该 token 下共 {len(adv_list)} 个账户:")
    for a in adv_list:
        print(f"  {a['advertiser_id']} | {a['advertiser_name']}")

    # 将所有账户写入数据库
    async with AsyncSessionLocal() as db:
        for adv in adv_list:
            adv_id = str(adv["advertiser_id"])
            adv_name = adv.get("advertiser_name", "")

            r = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == adv_id))
            existing = r.scalar_one_or_none()

            if existing:
                existing.access_token = TOKEN
                existing.is_active = True
                existing.is_token_valid = True
                existing.advertiser_name = adv_name
                print(f"  ✅ 更新: {adv_id} ({adv_name})")
            else:
                new_adv = Advertiser(
                    advertiser_id=adv_id,
                    advertiser_name=adv_name,
                    access_token=TOKEN,
                    refresh_token=None,
                    is_active=True,
                    is_token_valid=True,
                )
                db.add(new_adv)
                print(f"  ➕ 新增: {adv_id} ({adv_name})")

        await db.commit()
        print("\n✅ 数据库已更新")

    # 对每个账户查报表
    end = date.today()
    start = (end - timedelta(days=30)).strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")

    print(f"\n=== 查询近 30 天数据 ({start} ~ {end_str}) ===")
    for adv in adv_list:
        adv_id = str(adv["advertiser_id"])
        adv_name = adv.get("advertiser_name", "")
        client_tiktok = TikTokClient(access_token=TOKEN, advertiser_id=adv_id)
        try:
            data = await client_tiktok._request("GET", "/open_api/v1.3/report/integrated/get/",
                params={
                    "advertiser_id": adv_id,
                    "report_type": "BASIC",
                    "data_level": "AUCTION_CAMPAIGN",
                    "dimensions": '["campaign_id","stat_time_day"]',
                    "metrics": '["spend","impressions","clicks","conversion"]',
                    "start_date": start,
                    "end_date": end_str,
                    "page_size": 3,
                }
            )
            total = data.get("page_info", {}).get("total_number", 0)
            rows = data.get("list", [])
            status = "✅ 有数据!" if total > 0 else "❌ 无数据"
            print(f"\n  {status} {adv_name} ({adv_id}) — {total} 条报表")
            for row in rows[:2]:
                dims = row.get("dimensions", {})
                m = row.get("metrics", {})
                print(f"    {dims.get('stat_time_day')} | spend:{m.get('spend')} | conv:{m.get('conversion')}")
        except TikTokAPIError as e:
            print(f"\n  ⚠️  {adv_name} ({adv_id}): {e.message[:60]}")
        finally:
            await client_tiktok.close()

asyncio.run(main())
