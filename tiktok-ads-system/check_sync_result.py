import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as db:
        # 各账户 metrics 数量
        r = await db.execute(text(
            "SELECT advertiser_id, COUNT(*) as cnt, MAX(stat_date) as latest_date "
            "FROM metrics_snapshots GROUP BY advertiser_id"
        ))
        metrics = {row[0]: (row[1], row[2]) for row in r.fetchall()}

        # 账户列表
        r2 = await db.execute(text(
            "SELECT advertiser_id, advertiser_name FROM advertisers WHERE is_active=1"
        ))
        accounts = r2.fetchall()

    print("账户数据同步情况:")
    for adv_id, name in accounts:
        cnt, latest = metrics.get(adv_id, (0, None))
        status = "✅ 有数据" if cnt > 0 else "❌ 无数据"
        print(f"  {status} {name} ({adv_id}) — {cnt} 条, 最新: {latest}")

asyncio.run(main())
