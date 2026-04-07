"""
检查所有账户，找有投放数据的
"""
import asyncio
from datetime import date, timedelta
from app.core.database import AsyncSessionLocal
from app.services.tiktok_client import TikTokClient, TikTokAPIError
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            "SELECT advertiser_id, advertiser_name, access_token FROM advertisers "
            "WHERE is_active = 1 AND is_token_valid = 1"
        ))
        accounts = r.fetchall()

    print(f"共 {len(accounts)} 个账户，检查是否有Campaign数据...\n")

    end = date.today()
    start = end - timedelta(days=30)

    for adv_id, name, token in accounts:
        client = TikTokClient(access_token=token, advertiser_id=adv_id)
        try:
            data = await client.get_campaigns(page_size=1)
            total = data.get("page_info", {}).get("total_number", 0)
            print(f"  {'✅' if total > 0 else '❌'}  {name} ({adv_id})  →  {total} 个推广计划")
        except TikTokAPIError as e:
            print(f"  ⚠️  {name} ({adv_id})  →  API错误: {e.message[:50]}")
        except Exception as e:
            print(f"  ⚠️  {name} ({adv_id})  →  异常: {str(e)[:50]}")
        finally:
            await client.close()

asyncio.run(main())
