import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as db:
        # 先看看有哪些
        r = await db.execute(text("SELECT advertiser_id, advertiser_name FROM advertisers"))
        rows = r.fetchall()
        print("删除前：")
        for row in rows:
            marker = "✅ 保留" if row[0] == "7615246831711862800" else "🗑️  删除"
            print(f"  {marker}  {row[0]} | {row[1]}")

        # 删除其他的
        await db.execute(text(
            "DELETE FROM advertisers WHERE advertiser_id != '7615246831711862800'"
        ))
        await db.commit()

        r2 = await db.execute(text("SELECT advertiser_id, advertiser_name FROM advertisers"))
        remaining = r2.fetchall()
        print(f"\n删除后，剩余 {len(remaining)} 个账户：")
        for row in remaining:
            print(f"  ✅ {row[0]} | {row[1]}")

asyncio.run(main())
