from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # TikTok App
    TIKTOK_APP_ID: str
    TIKTOK_APP_SECRET: str
    TIKTOK_REDIRECT_URI: str  # 从 .env 读取，无默认值
    TIKTOK_API_BASE: str = "https://business-api.tiktok.com"

    # LLM
    LLM_API_BASE: str
    LLM_API_KEY: str
    LLM_MODEL: str = "gpt-5"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # App
    SECRET_KEY: str
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Scheduler
    SYNC_INTERVAL_MINUTES: int = 30

    # 飞书通知（可选）
    FEISHU_WEBHOOK_URL: Optional[str] = None
    DAILY_REPORT_HOUR: int = 9   # 每天几点发日报（24h制）

    # Rate limit: TikTok API 并发控制
    TIKTOK_MAX_CONCURRENT: int = 10   # 同时并发请求数
    TIKTOK_RATE_LIMIT_PER_MIN: int = 300  # 每分钟最大请求数（留安全余量）

    class Config:
        env_file = ".env"


settings = Settings()
