import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def check():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            "SELECT advertiser_id, advertiser_name, is_active, is_token_valid, last_sync_at, access_token "
            "FROM advertisers WHERE advertiser_id = '7620344099409018898'"
        ))
        row = r.fetchone()
        if row:
            print(f'ID: {row[0]}')
            print(f'Name: {row[1]}')
            print(f'is_active: {row[2]}')
            print(f'is_token_valid: {row[3]}')
            print(f'last_sync_at: {row[4]}')
            print(f'token: {str(row[5])[:20] if row[5] else None}...')
        else:
            print('账户不存在！')

        # 也看一下 metrics_snapshots 里有没有数据
        r2 = await db.execute(text(
            "SELECT COUNT(*), MAX(stat_date) FROM metrics_snapshots WHERE advertiser_id = '7620344099409018898'"
        ))
        row2 = r2.fetchone()
        print(f'metrics_snapshots: {row2[0]} 条, 最新日期: {row2[1]}')

asyncio.run(check())
