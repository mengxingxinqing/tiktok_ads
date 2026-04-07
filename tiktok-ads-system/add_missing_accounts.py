"""
手动添加同一 token 下的缺失账户到数据库
基于之前 check_token_scope.py 查到的结果
"""
import asyncio
from app.core.database import AsyncSessionLocal
from app.models.advertiser import Advertiser
from sqlalchemy import select

TOKEN = "07f57abb41f446b356da76ff3e3d6a4221be41e4"

# 之前查到的 4 个账户
ACCOUNTS = [
    ("7585080394601791505", "广州一群科技-20251215-1"),
    ("7615246831711862800", "591$"),
    ("7616286272197574663", "Jingshun Hall Store"),  # ← 绑了店铺的，有投放数据
    ("7616312887514169352", "广告户01"),
]

async def main():
    async with AsyncSessionLocal() as db:
        for adv_id, adv_name in ACCOUNTS:
            r = await db.execute(select(Advertiser).where(Advertiser.advertiser_id == adv_id))
            existing = r.scalar_one_or_none()

            if existing:
                existing.access_token = TOKEN
                existing.is_active = True
                existing.is_token_valid = True
                existing.advertiser_name = adv_name
                print(f"✅ 更新: {adv_id} ({adv_name})")
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
                print(f"➕ 新增: {adv_id} ({adv_name})")

        await db.commit()
        print("\n✅ 全部写入成功！")
        print("现在触发同步: POST http://localhost:8000/admin/sync/trigger")

asyncio.run(main())
