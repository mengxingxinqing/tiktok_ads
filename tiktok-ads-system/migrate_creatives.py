import asyncio
from sqlalchemy import text
from app.core.database import engine

NEEDED_COLUMNS = {
    "status": "ALTER TABLE creatives ADD COLUMN status VARCHAR(32) NULL",
    "review_status": "ALTER TABLE creatives ADD COLUMN review_status VARCHAR(32) NULL",
    "review_reject_reason": "ALTER TABLE creatives ADD COLUMN review_reject_reason TEXT NULL",
    "review_time": "ALTER TABLE creatives ADD COLUMN review_time DATETIME(6) NULL",
    "shop_id": "ALTER TABLE creatives ADD COLUMN shop_id VARCHAR(64) NULL",
    "shop_name": "ALTER TABLE creatives ADD COLUMN shop_name VARCHAR(256) NULL",
    "product_id": "ALTER TABLE creatives ADD COLUMN product_id VARCHAR(64) NULL",
    "product_name": "ALTER TABLE creatives ADD COLUMN product_name VARCHAR(256) NULL",
}

async def migrate():
    async with engine.begin() as conn:
        r = await conn.execute(text("DESCRIBE creatives"))
        existing = {row[0] for row in r.fetchall()}
        print(f"现有列数: {len(existing)}")

        added = 0
        for col, sql in NEEDED_COLUMNS.items():
            if col not in existing:
                print(f"  添加列: {col}")
                await conn.execute(text(sql))
                added += 1
            else:
                print(f"  已存在: {col}")

        if added:
            print(f"\n✅ 补充了 {added} 个列，迁移完成！")
        else:
            print("\n✅ 无需迁移，所有列都已存在")

asyncio.run(migrate())
