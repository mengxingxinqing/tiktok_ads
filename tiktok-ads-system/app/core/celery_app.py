"""
Celery 应用配置

启动 Worker:
    celery -A app.core.celery_app worker --loglevel=info --pool=solo

启动 Beat（定时调度）:
    celery -A app.core.celery_app beat --loglevel=info

Windows 下建议用 --pool=solo（不支持 prefork）
"""
import os
from celery import Celery
from celery.schedules import crontab

# 从 .env 读取 Redis URL，默认本地
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "tiktok_ads",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

app.conf.update(
    # 序列化
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # 时区
    timezone="UTC",
    enable_utc=True,

    # 任务发现
    imports=[
        "app.tasks.celery_tasks",
        "app.tasks.growth_monitor",
        "app.tasks.growth_daily_reconcile",
    ],

    # 任务执行
    task_acks_late=True,                  # 任务执行完才 ack，失败可重试
    worker_prefetch_multiplier=1,         # 每次只取 1 个任务
    task_soft_time_limit=600,             # 软超时 10 分钟
    task_time_limit=900,                  # 硬超时 15 分钟
    task_reject_on_worker_lost=True,      # Worker 异常退出时任务重新入队

    # 结果
    result_expires=3600,                  # 结果保留 1 小时

    # Beat 定时调度
    beat_schedule={
        # 每日同步（凌晨 2 点）：拉过去 7 天历史数据
        "daily-sync": {
            "task": "app.tasks.celery_tasks.daily_sync",
            "schedule": crontab(hour=2, minute=0),
        },
        # 每小时同步今日数据
        "hourly-sync": {
            "task": "app.tasks.celery_tasks.hourly_sync",
            "schedule": crontab(minute=0),  # 每小时整点
        },
        # 每小时告警检测
        "hourly-detection": {
            "task": "app.tasks.celery_tasks.detection_and_decision",
            "schedule": crontab(minute=5),  # 每小时第 5 分钟（等同步完）
        },
        # 每日日报（上午 9 点）
        "daily-report": {
            "task": "app.tasks.celery_tasks.daily_report",
            "schedule": crontab(hour=9, minute=0),
        },
        # 评论同步（每 4 小时）
        "comment-sync": {
            "task": "app.tasks.celery_tasks.comment_sync",
            "schedule": crontab(minute=30, hour="*/4"),  # 每 4 小时的第 30 分钟
        },
        # 涨粉监控（每 15 分钟）
        "growth-monitor": {
            "task": "app.tasks.growth_monitor.celery_check_campaigns",
            "schedule": crontab(minute="*/15"),  # 每 15 分钟
        },
        # 涨粉每日对账（UTC 13:00，避开 TikTok UTC 12:00 数据修正窗口）
        "growth-reconcile-daily": {
            "task": "app.tasks.growth_daily_reconcile.celery_reconcile",
            "schedule": crontab(hour=13, minute=0),
        },
    },
)
