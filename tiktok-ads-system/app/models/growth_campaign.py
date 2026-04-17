"""
涨粉投放 Campaign 模型
"""
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, Numeric
from app.models.base import Base, TimestampMixin


class GrowthCampaign(Base, TimestampMixin):
    """涨粉投放任务"""
    __tablename__ = "growth_campaigns"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    campaign_id = Column(String(64), unique=True, nullable=False, index=True)

    # 关联
    tk_account_id = Column(String(64), nullable=False, index=True)
    ad_account_id = Column(String(64), nullable=False, index=True)
    video_id = Column(String(128), nullable=False)
    ad_id = Column(String(64), nullable=True)   # TikTok 广告ID，创建后填充

    # TikTok 内部层级
    tiktok_campaign_id = Column(String(64), nullable=True)
    tiktok_adgroup_id = Column(String(64), nullable=True)
    tiktok_ad_id = Column(String(64), nullable=True)

    # Spark Ads 绑定信息（创建时快照，便于调试和重放）
    identity_id = Column(String(128), nullable=True)
    identity_type = Column(String(32), nullable=True)  # AUTH_CODE / CUSTOMIZED_USER
    post_id = Column(String(128), nullable=True)        # Spark Ads 要 promote 的原帖 id

    # 目标
    target_followers = Column(BigInteger, nullable=False)   # 目标粉丝增量
    budget = Column(Numeric(12, 2), nullable=False)          # USD 预算上限（规划口径）
    budget_local = Column(Numeric(14, 4), nullable=True)    # 实际下发给 TikTok 的本币预算
    budget_currency = Column(String(8), nullable=True)       # 本币币种，与 AdAccount.currency 一致
    target_cost_per_10k = Column(Numeric(10, 4), default=35.0)

    # 基线粉丝数：Campaign 启动瞬间的粉丝数快照
    # followers_gained = 实时粉丝数 - baseline_followers
    baseline_followers = Column(BigInteger, nullable=True)

    # 状态：PENDING / RUNNING / COMPLETED / FAILED / PAUSED
    status = Column(String(32), default="PENDING", index=True)

    # 执行记录
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_spend = Column(Numeric(12, 2), default=0)           # USD（换算后口径，便于跨户汇总）
    total_spend_local = Column(Numeric(14, 4), default=0)     # 本币原始值（来自 TikTok 报表）
    last_spend_synced_at = Column(DateTime(timezone=True), nullable=True)
    followers_gained = Column(Integer, default=0)
    scrape_failure_count = Column(Integer, default=0)         # 连续爬粉失败次数
    auto_stop_reason = Column(String(64), nullable=True)
    retry_count = Column(Integer, default=0)

    # 自适应采集调度
    # 上一次采集时的时点和粉丝值，用于计算观测速率
    last_check_at = Column(DateTime(timezone=True), nullable=True)
    last_check_followers = Column(Integer, nullable=True)
    # 下一次采集时刻；monitor 任务按该时刻过滤待处理 Campaign
    next_check_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # 每日对账（T+1 官方数据真值，与上面的轮询/爬虫数据并存不覆盖）
    # total_spend*/followers_gained = 运行时轮询+爬虫近实时估计
    # official_* = 官方 /report/integrated/get/ 的定稿值，用于素材成本回填
    official_spend_local = Column(Numeric(14, 4), nullable=True)
    official_spend_usd = Column(Numeric(14, 4), nullable=True)
    official_followers_gained = Column(Integer, nullable=True)
    last_reconciled_at = Column(DateTime(timezone=True), nullable=True)
