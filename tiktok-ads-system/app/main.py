"""
TikTok 广告投放检测和智能决策系统 — 后端入口
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from loguru import logger
from sqlalchemy import func, select

from app.core.config import settings
from app.core.database import engine, AsyncSessionLocal
from app.models.base import Base
from app.api import auth
from app.api import decisions
from app.api import dashboard
from app.api import creatives
from app.api import boost
from app.api import products
from app.api import analytics
from app.api import orders
from app.api import ads_creation
from app.api import campaigns
from app.api import shops
from app.api import rules
from app.api import shop_summary
from app.api import gmvmax_actions
from app.api import channel_analysis
from app.api import creative_groups
from app.api import comments
from app.api import creative_dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured")

    # 数据库迁移：添加渠道来源拆分字段（已存在则跳过）
    from sqlalchemy import text as _text
    _source_columns = [
        "ALTER TABLE metrics_snapshots ADD COLUMN source_type VARCHAR(32)",
        "ALTER TABLE metrics_snapshots ADD COLUMN affiliate_id VARCHAR(64)",
        "ALTER TABLE metrics_snapshots ADD COLUMN affiliate_name VARCHAR(256)",
        "ALTER TABLE metrics_snapshots ADD COLUMN commission_amount FLOAT DEFAULT 0.0",
        "ALTER TABLE metrics_snapshots ADD COLUMN commission_rate FLOAT DEFAULT 0.0",
        "ALTER TABLE metrics_snapshots ADD COLUMN store_id VARCHAR(64)",
        "CREATE INDEX idx_metrics_store ON metrics_snapshots(store_id)",
    ]
    async with engine.begin() as conn:
        for _sql in _source_columns:
            try:
                await conn.execute(_text(_sql))
                logger.info(f"Migration: {_sql[:60]}...")
            except Exception as _e:
                # MySQL error 1060: Duplicate column name → 列已存在，跳过
                logger.debug(f"Migration skip (column exists): {_e}")
    logger.info("Source field migration done")

    # 数据库迁移：creative_groups.advertiser_id 改为可空（分组与广告户无关）
    _nullable_migrations = [
        "ALTER TABLE creative_groups MODIFY COLUMN advertiser_id VARCHAR(64) NULL",
    ]
    async with engine.begin() as conn:
        for _sql in _nullable_migrations:
            try:
                await conn.execute(_text(_sql))
                logger.info(f"Migration: {_sql[:60]}...")
            except Exception as _e:
                logger.debug(f"Migration skip: {_e}")
    logger.info("Creative groups nullable migration done")

    # 数据库迁移：product_costs.advertiser_id 改为可空（成本配置按 product_id 唯一）
    _product_migrations = [
        "ALTER TABLE product_costs MODIFY COLUMN advertiser_id VARCHAR(64) NULL",
    ]
    async with engine.begin() as conn:
        for _sql in _product_migrations:
            try:
                await conn.execute(_text(_sql))
                logger.info(f"Migration: {_sql[:60]}...")
            except Exception as _e:
                logger.debug(f"Migration skip: {_e}")
    logger.info("Product costs nullable migration done")

    # 初始化默认规则（表为空时自动写入）
    from app.models.rule import AlertRule, DEFAULT_RULES
    async with AsyncSessionLocal() as db:
        count_result = await db.execute(select(func.count()).select_from(AlertRule))
        rule_count = count_result.scalar()
        if rule_count == 0:
            for rule_data in DEFAULT_RULES:
                db.add(AlertRule(**rule_data))
            await db.commit()
            logger.info(f"Seeded {len(DEFAULT_RULES)} default alert rules")
        else:
            logger.info(f"Alert rules already exist ({rule_count} rules), skip seeding")

    # 定时任务已迁移到 Celery Beat，无需在 FastAPI 进程中调度
    # 启动方式：
    #   celery -A app.core.celery_app worker --loglevel=info --pool=solo
    #   celery -A app.core.celery_app beat --loglevel=info
    logger.info("定时任务由 Celery Beat 调度，请确保 Worker 和 Beat 进程已启动")

    yield

    await engine.dispose()
    logger.info("Server shutdown complete")


app = FastAPI(
    title="TikTok Ads Intelligence System",
    description="TikTok 广告投放检测和智能决策系统",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(auth.router)
app.include_router(decisions.router)
app.include_router(dashboard.router)
app.include_router(creatives.router)
app.include_router(boost.router)
app.include_router(products.router)
app.include_router(analytics.router)
app.include_router(orders.router)
app.include_router(ads_creation.router)  # 新增：Ads广告创建
app.include_router(campaigns.router)    # 新增：广告层级查询
app.include_router(shops.router)        # 新增：店铺管理与分析
app.include_router(rules.router)        # 新增：可配置规则引擎
app.include_router(shop_summary.router) # 新增：店铺汇总大盘
app.include_router(gmvmax_actions.router) # 新增：GMVMax Actions
app.include_router(channel_analysis.router) # 新增：渠道来源分析
app.include_router(creative_groups.router) # 新增：素材分组管理
app.include_router(comments.router)           # 新增：评论监控（数据入库）
app.include_router(creative_dashboard.router) # 新增：创意大盘


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/admin/sync/trigger")
async def trigger_sync():
    """手动触发一次数据同步（通过 Celery）"""
    from app.tasks.celery_tasks import hourly_sync
    result = hourly_sync.delay()
    return {"message": "数据同步任务已派发", "task_id": result.id}


@app.post("/admin/sync/full")
async def trigger_full_sync(days: int = 60):
    """
    全量历史同步 — 拉取最近 N 天的全部数据（按 30 天分批）。
    首次使用、数据修复时调用。完成后增量同步自动接管。
    """
    import asyncio
    from app.tasks.sync_task import run_full_sync
    asyncio.create_task(run_full_sync(days))
    return {
        "message": f"全量同步已启动（{days} 天），后台运行中",
        "days": days,
        "batches": (days + 29) // 30,
        "note": "可通过服务日志查看进度，完成后增量同步自动接管",
    }


@app.post("/admin/report/trigger")
async def trigger_report():
    """手动触发日报发送（通过 Celery）"""
    from app.tasks.celery_tasks import daily_report
    result = daily_report.delay()
    return {"message": "日报任务已派发", "task_id": result.id}


@app.post("/admin/feishu/test")
async def test_feishu(webhook_url: str):
    """测试飞书 Webhook 连通性"""
    from app.services.notifier import FeishuNotifier
    from app.models.alert import Alert
    from datetime import datetime
    notifier = FeishuNotifier(webhook_url=webhook_url)
    test_alert = Alert(
        id=0,
        advertiser_id="test_advertiser",
        alert_type="TEST",
        severity="INFO",
        title="飞书通知测试",
        message="这是一条测试消息，说明飞书 Webhook 配置正确 ✅",
        created_at=datetime.now(),
    )
    ok = await notifier.send_alert(test_alert)
    await notifier.close()
    return {"success": ok, "webhook_url": webhook_url[:30] + "..."}


# ==================== 前端静态文件托管 ====================
# 从 tiktok-ads-frontend/dist 目录提供 Vue SPA
# ============ 前端托管 ============
# 开发模式：反代到 Vite Dev Server（热更新，改代码不需要打包）
# 生产模式：托管 dist 静态文件
_frontend_dist = Path(__file__).resolve().parent.parent.parent / "tiktok-ads-frontend-dist"
if not _frontend_dist.exists():
    _frontend_dist = Path(__file__).resolve().parent.parent.parent / "tiktok-ads-frontend" / "dist"

VITE_DEV_URL = os.environ.get("VITE_DEV_URL", "http://localhost:5175")

import mimetypes
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("image/svg+xml", ".svg")

if os.environ.get("DEV_PROXY", ""):
    # 开发模式：所有非 API 请求反代到 Vite
    import httpx

    @app.api_route("/{path:path}", methods=["GET", "HEAD"])
    async def dev_proxy(request: Request, path: str):
        url = f"{VITE_DEV_URL}/{path}"
        req_headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host",)}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers=req_headers, params=dict(request.query_params), follow_redirects=True)
                excluded = {"content-encoding", "transfer-encoding", "content-length"}
                resp_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
                from starlette.responses import Response
                return Response(content=resp.content, status_code=resp.status_code, headers=resp_headers)
        except httpx.ConnectError:
            from starlette.responses import Response
            return Response(content="Vite dev server not running on " + VITE_DEV_URL, status_code=502, media_type="text/plain")

    # Vite HMR websocket
    @app.websocket("/{path:path}")
    async def dev_ws_proxy(websocket):
        import asyncio
        import websockets
        ws_url = VITE_DEV_URL.replace("http://", "ws://") + "/" + websocket.path_params.get("path", "")
        await websocket.accept()
        try:
            async with websockets.connect(ws_url) as ws:
                async def forward_to_client():
                    async for msg in ws:
                        await websocket.send_text(msg if isinstance(msg, str) else msg.decode())
                async def forward_to_server():
                    while True:
                        data = await websocket.receive_text()
                        await ws.send(data)
                await asyncio.gather(forward_to_client(), forward_to_server())
        except Exception:
            pass

    logger.info(f"DEV MODE: proxying frontend to {VITE_DEV_URL}")

elif _frontend_dist.exists():
    # 生产模式：托管 dist 静态文件
    app.mount("/assets", StaticFiles(directory=str(_frontend_dist / "assets")), name="frontend-assets")

    @app.get("/{path:path}")
    async def spa_fallback(request: Request, path: str):
        file_path = _frontend_dist / path
        if path and file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(_frontend_dist / "index.html"))

    logger.info(f"PROD MODE: frontend served from {_frontend_dist}")
else:
    logger.warning(f"Frontend not available (no dist, no dev proxy)")
