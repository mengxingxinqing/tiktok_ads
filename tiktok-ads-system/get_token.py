import asyncio
from sqlalchemy import text
from app.core.database import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            "SELECT advertiser_id, advertiser_name, access_token FROM advertisers "
            "WHERE advertiser_id = '7615246831711862800'"
        ))
        row = r.fetchone()
        if row:
            print(f"ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Token: {row[2]}")

asyncio.run(main())
