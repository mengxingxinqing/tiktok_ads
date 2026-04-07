"""一次性全量同步 GMVMax 30天数据"""
import asyncio
import json
from datetime import date, timedelta, datetime, timezone
from sqlalchemy import text
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient
from app.models.metrics import MetricsSnapshot

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
    start = end - timedelta(days=30)
    snapshot_time = datetime.now(timezone.utc)

    data = await client.get_gmvmax_report(
        store_ids=[STORE_ID],
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        page_size=500,
    )

    rows = data.get("list", [])
    print(f"拉取到 {len(rows)} 条 GMVMax 记录")

    # 先清理旧的 GMVMAX_CAMPAIGN 数据避免重复
    async with AsyncSessionLocal() as db:
        await db.execute(text(
            "DELETE FROM metrics_snapshots WHERE data_level = 'GMVMAX_CAMPAIGN' AND advertiser_id = :adv_id"
        ), {"adv_id": ADVERTISER_ID})

        snapshots = []
        for row in rows:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})
            campaign_id = dims.get("campaign_id", "")
            stat_time = dims.get("stat_time_day", str(end))
            if " " in stat_time:
                stat_time = stat_time.split(" ")[0]

            snapshot = MetricsSnapshot(
                advertiser_id=ADVERTISER_ID,
                data_level="GMVMAX_CAMPAIGN",
                object_id=campaign_id,
                object_name="",
                stat_date=datetime.strptime(stat_time, "%Y-%m-%d").date(),
                snapshot_time=snapshot_time,
                campaign_id=campaign_id,
                spend=float(metrics.get("cost", 0) or 0),
                conversion=int(metrics.get("orders", 0) or 0),
                cost_per_conversion=float(metrics.get("cost_per_order", 0) or 0),
                gross_revenue=float(metrics.get("gross_revenue", 0) or 0),
                roi=float(metrics.get("roi", 0) or 0),
                live_views=int(metrics.get("live_views", 0) or 0),
            )
            snapshots.append(snapshot)

        db.add_all(snapshots)
        await db.commit()
        print(f"写入 {len(snapshots)} 条记录")

        # 验证
        r = await db.execute(text("""
            SELECT stat_date, object_id, spend, conversion, gross_revenue, roi
            FROM metrics_snapshots
            WHERE data_level = 'GMVMAX_CAMPAIGN' AND advertiser_id = :adv_id AND spend > 0
            ORDER BY stat_date DESC
        """), {"adv_id": ADVERTISER_ID})
        for row in r.fetchall():
            print(f"  {row.stat_date} | {row.object_id} | spend=${row.spend:.2f} | orders={row.conversion} | rev=${row.gross_revenue:.2f} | roi={row.roi:.2f}")

    await client.close()
    print("✅ 完成")

asyncio.run(main())
