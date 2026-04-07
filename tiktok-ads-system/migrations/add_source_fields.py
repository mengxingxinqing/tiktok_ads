"""
迁移脚本：为 metrics_snapshots 表添加渠道来源拆分字段

新增字段：
  source_type      VARCHAR(32)   订单来源：SELF_OWNED / AFFILIATE / ALL
  affiliate_id     VARCHAR(64)   达人 ID（AFFILIATE 来源时有值）
  affiliate_name   VARCHAR(256)  达人名称
  commission_amount FLOAT        达人佣金金额
  commission_rate   FLOAT        达人佣金率 %

运行方式：
  python -m migrations.add_source_fields
  或直接：
  python migrations/add_source_fields.py
"""
import asyncio
import sys
import os

# 将项目根目录加入 sys.path，以便 import app.*
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


_ALTER_STATEMENTS = [
    "ALTER TABLE metrics_snapshots ADD COLUMN source_type VARCHAR(32)",
    "ALTER TABLE metrics_snapshots ADD COLUMN affiliate_id VARCHAR(64)",
    "ALTER TABLE metrics_snapshots ADD COLUMN affiliate_name VARCHAR(256)",
    "ALTER TABLE metrics_snapshots ADD COLUMN commission_amount FLOAT DEFAULT 0.0",
    "ALTER TABLE metrics_snapshots ADD COLUMN commission_rate FLOAT DEFAULT 0.0",
]

# MySQL 1060 = Duplicate column name（列已存在）
_DUPLICATE_COLUMN_ERRNO = 1060


async def run_migration():
    print("Running migration: add source fields to metrics_snapshots ...")
    async with engine.begin() as conn:
        for sql in _ALTER_STATEMENTS:
            col = sql.split("ADD COLUMN")[1].strip().split()[0]
            try:
                await conn.execute(text(sql))
                print(f"  ✓ Added column: {col}")
            except Exception as e:
                err_str = str(e)
                # 判断是否是「列已存在」错误（MySQL 1060）
                if "1060" in err_str or "Duplicate column" in err_str.lower():
                    print(f"  - Skipped (already exists): {col}")
                else:
                    print(f"  ✗ Error on column {col}: {e}")
                    raise

    print("Migration complete.")


if __name__ == "__main__":
    asyncio.run(run_migration())
