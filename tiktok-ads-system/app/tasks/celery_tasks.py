"""
Celery 任务定义

所有定时任务和可手动触发的后台任务统一在此注册。
原有的 async 函数通过 asyncio.run() 桥接到 Celery 的同步 Worker 中。
"""
import asyncio
from loguru import logger

from app.core.celery_app import app


def _run_async(coro):
    """在 Celery 同步 Worker 中运行 async 函数"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# ===================== 数据同步 =====================

@app.task(name="app.tasks.celery_tasks.daily_sync", bind=True, max_retries=2)
def daily_sync(self):
    """每日同步：拉过去 7 天历史数据（凌晨 2 点）"""
    logger.info("[Celery] 开始每日数据同步")
    try:
        from app.tasks.sync_task import run_daily_sync
        _run_async(run_daily_sync())
        logger.info("[Celery] 每日数据同步完成")
    except Exception as exc:
        logger.error(f"[Celery] 每日同步失败: {exc}")
        raise self.retry(exc=exc, countdown=300)


@app.task(name="app.tasks.celery_tasks.hourly_sync", bind=True, max_retries=2)
def hourly_sync(self):
    """每小时同步：拉今日实时数据"""
    logger.info("[Celery] 开始每小时数据同步")
    try:
        from app.tasks.sync_task import run_hourly_sync
        _run_async(run_hourly_sync())
        logger.info("[Celery] 每小时数据同步完成")
    except Exception as exc:
        logger.error(f"[Celery] 每小时同步失败: {exc}")
        raise self.retry(exc=exc, countdown=120)


# ===================== 告警检测 =====================

@app.task(name="app.tasks.celery_tasks.detection_and_decision", bind=True, max_retries=1)
def detection_and_decision(self):
    """每小时告警检测 + LLM 决策"""
    logger.info("[Celery] 开始告警检测")
    try:
        from app.tasks.sync_task import run_detection_and_decision
        _run_async(run_detection_and_decision())
        logger.info("[Celery] 告警检测完成")
    except Exception as exc:
        logger.error(f"[Celery] 告警检测失败: {exc}")
        raise self.retry(exc=exc, countdown=120)


# ===================== 日报 =====================

@app.task(name="app.tasks.celery_tasks.daily_report", bind=True, max_retries=2)
def daily_report(self):
    """每日日报：发送飞书通知"""
    logger.info("[Celery] 开始发送日报")
    try:
        from app.tasks.report_task import send_daily_report
        _run_async(send_daily_report())
        logger.info("[Celery] 日报发送完成")
    except Exception as exc:
        logger.error(f"[Celery] 日报发送失败: {exc}")
        raise self.retry(exc=exc, countdown=60)


# ===================== 评论同步 =====================

@app.task(name="app.tasks.celery_tasks.comment_sync", bind=True, max_retries=1)
def comment_sync(self):
    """评论数据同步：拉取广告评论入库"""
    logger.info("[Celery] 开始评论同步")
    try:
        from app.services.comment_sync import run_comment_sync
        _run_async(run_comment_sync())
        logger.info("[Celery] 评论同步完成")
    except Exception as exc:
        logger.error(f"[Celery] 评论同步失败: {exc}")
        raise self.retry(exc=exc, countdown=300)
