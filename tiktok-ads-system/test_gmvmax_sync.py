"""
端到端测试：执行 GMVMax 同步，验证数据入库
"""
import asyncio
from datetime import date, timedelta
from sqlalchemy import text
from app.core.database import AsyncSessionLocal
from app.tasks.sync_task import sync_gmvmax

ADVERTISER_ID = "7615246831711862800"


async def main():
    # 1. 获取 token
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            f"SELECT access_token FROM advertisers WHERE advertiser_id = '{ADVERTISER_ID}'"
        ))
        token = r.fetchone()[0]

    # 2. 执行 GMVMax 同步
    print("=== 执行 GMVMax 同步 ===")
    async with AsyncSessionLocal() as db:
        await sync_gmvmax(ADVERTISER_ID, token, db)
        await db.commit()

    # 3. 验证数据入库
    print("\n=== 验证数据库 ===")
    async with AsyncSessionLocal() as db:
        r = await db.execute(text("""
            SELECT stat_date, object_id as campaign_id, spend, conversion as orders,
                   gross_revenue, roi, live_views
            FROM metrics_snapshots
            WHERE data_level = 'GMVMAX_CAMPAIGN'
              AND advertiser_id = :adv_id
            ORDER BY stat_date DESC
            LIMIT 20
        """), {"adv_id": ADVERTISER_ID})
        rows = r.fetchall()
        print(f"GMVMax 记录数: {len(rows)}")
        for row in rows:
            print(f"  {row.stat_date} | campaign: {row.campaign_id} | spend: ${row.spend:.2f} | orders: {row.orders} | revenue: ${row.gross_revenue:.2f} | roi: {row.roi:.2f}")

        # 总计
        r2 = await db.execute(text("""
            SELECT COUNT(*) as cnt, SUM(spend) as total_spend, SUM(gross_revenue) as total_rev, SUM(conversion) as total_orders
            FROM metrics_snapshots
            WHERE data_level = 'GMVMAX_CAMPAIGN'
              AND advertiser_id = :adv_id
        """), {"adv_id": ADVERTISER_ID})
        summary = r2.fetchone()
        print(f"\n总计: {summary.cnt} 条 | 总花费: ${summary.total_spend:.2f} | 总收入: ${summary.total_rev:.2f} | 总订单: {summary.total_orders}")

    print("\n✅ 测试完成")


asyncio.run(main())
