"""
每日日报任务 — 每天早上 9 点发送
"""
from datetime import date, timedelta

from loguru import logger
from sqlalchemy import select, func

from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.metrics import MetricsSnapshot
from app.models.alert import Alert
from app.models.decision import Decision
from app.models.advertiser import Advertiser
from app.services.notifier import FeishuNotifier


async def send_daily_report():
    """汇总今日数据，发送飞书日报"""
    today = date.today()
    yesterday = today - timedelta(days=1)

    async with AsyncSessionLocal() as db:
        # 昨日汇总数据
        result = await db.execute(
            select(
                func.sum(MetricsSnapshot.spend).label("total_spend"),
                func.sum(MetricsSnapshot.impressions).label("total_impressions"),
                func.sum(MetricsSnapshot.clicks).label("total_clicks"),
                func.sum(MetricsSnapshot.conversion).label("total_conversion"),
                func.avg(MetricsSnapshot.ctr).label("avg_ctr"),
                func.avg(MetricsSnapshot.cost_per_conversion).label("avg_cpa"),
            ).where(
                MetricsSnapshot.stat_date == yesterday,
                MetricsSnapshot.data_level == "AD",
            )
        )
        metrics = result.one()

        # 活跃账户数
        adv_count = await db.execute(
            select(func.count(Advertiser.id)).where(Advertiser.is_active == True)
        )

        # 今日告警数
        alerts_count = await db.execute(
            select(func.count(Alert.id)).where(
                func.date(Alert.created_at) == today
            )
        )

        # 今日自动执行决策数
        auto_count = await db.execute(
            select(func.count(Decision.id)).where(
                func.date(Decision.created_at) == today,
                Decision.is_auto_executed == True,
            )
        )

        # 待处理决策数
        pending_count = await db.execute(
            select(func.count(Decision.id)).where(Decision.status == "PENDING")
        )

        stats = {
            "total_spend": float(metrics.total_spend or 0),
            "total_impressions": int(metrics.total_impressions or 0),
            "total_clicks": int(metrics.total_clicks or 0),
            "total_conversion": int(metrics.total_conversion or 0),
            "avg_ctr": float(metrics.avg_ctr or 0),
            "avg_cpa": float(metrics.avg_cpa or 0),
            "active_advertisers": adv_count.scalar() or 0,
            "alerts_today": alerts_count.scalar() or 0,
            "auto_decisions": auto_count.scalar() or 0,
            "pending_decisions": pending_count.scalar() or 0,
        }

    notifier = FeishuNotifier(webhook_url=settings.FEISHU_WEBHOOK_URL)
    ok = await notifier.send_daily_report(stats)
    await notifier.close()

    logger.info(f"Daily report sent: {ok}, stats={stats}")
