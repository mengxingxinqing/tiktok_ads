"""
手动测试 TikTok 报表 API，找到有数据的时间范围
"""
import asyncio
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient
from sqlalchemy import text

ADVERTISER_ID = "7620344099409018898"

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        row = r.fetchone()
        access_token = row[0]

    client = TikTokClient(access_token=access_token, advertiser_id=ADVERTISER_ID)

    # 拉最近 30 天看看有没有数据
    end = date.today()
    start = end - timedelta(days=30)
    print(f"查询 {start} ~ {end}")

    data = await client.get_report(
        data_level="AUCTION_AD",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        page_size=10,
    )
    rows = data.get("list", [])
    total = data.get("page_info", {}).get("total_number", 0)
    print(f"AD 级报表: {total} 条总数, 返回 {len(rows)} 条")
    if rows:
        print("示例:", rows[0])

    # 也试 Campaign 级
    data2 = await client.get_report(
        data_level="AUCTION_CAMPAIGN",
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        page_size=5,
    )
    rows2 = data2.get("list", [])
    total2 = data2.get("page_info", {}).get("total_number", 0)
    print(f"Campaign 级报表: {total2} 条总数, 返回 {len(rows2)} 条")
    if rows2:
        print("示例:", rows2[0])

    await client.close()

asyncio.run(main())
