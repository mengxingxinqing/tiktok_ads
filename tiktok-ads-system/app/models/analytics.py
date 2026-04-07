"""
分析和报表数据模型

用于支持：账户大盘、预测、风险评分等高阶分析
"""
from sqlalchemy import Column, String, Float, DateTime, BigInteger, ForeignKey, Index, Date, Integer
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class AccountSnapshot(Base, TimestampMixin):
    """
    账户级快照 — 每小时计算一次
    用于大盘展示、风险评分、预测
    """
    __tablename__ = "account_snapshots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)

    # 快照时间（通常是整点）
    snapshot_time = Column(DateTime(timezone=True), nullable=False, index=True)
    stat_date = Column(Date, nullable=False, index=True)

    # ===== 核心投放指标（汇总） =====
    spend = Column(Float, default=0.0, comment="总花费")
    gmv = Column(Float, default=0.0, comment="总 GMV")
    orders = Column(Integer, default=0, comment="总订单数")
    roas = Column(Float, default=0.0, comment="ROAS")
    real_profit = Column(Float, default=0.0, comment="真实利润")
    real_margin = Column(Float, default=0.0, comment="真实利润率 %")

    # ===== 素材多样性 =====
    active_videos = Column(Integer, comment="活跃视频数")
    active_campaigns = Column(Integer, comment="活跃 campaign 数")
    active_adgroups = Column(Integer, comment="活跃 adgroup 数")

    # ===== 生命周期分布 =====
    videos_peak = Column(Integer, default=0, comment="PEAK 阶段视频数")
    videos_growth = Column(Integer, default=0, comment="GROWTH 阶段视频数")
    videos_warmup = Column(Integer, default=0, comment="WARM_UP 阶段视频数")
    videos_decay = Column(Integer, default=0, comment="DECAY 阶段视频数")
    videos_fatigue = Column(Integer, default=0, comment="FATIGUE 阶段视频数")

    # ===== 视频指标（平均值）=====
    avg_hook_rate = Column(Float, comment="平均 Hook Rate %")
    avg_ctr = Column(Float, comment="平均 CTR %")
    avg_cpc = Column(Float, comment="平均 CPC $")

    # ===== 健康度评分 =====
    health_score = Column(Integer, comment="账户健康度 0-100")
    risk_level = Column(String(20), comment="low / medium / high / critical")

    # ===== 每日目标进度 =====
    daily_spend_target = Column(Float, comment="日花费目标 $")
    daily_gmv_target = Column(Float, comment="日 GMV 目标 $")
    spend_progress = Column(Float, comment="花费达成率 %")
    gmv_progress = Column(Float, comment="GMV 达成率 %")

    # ===== 趋势指标 =====
    spend_change_24h = Column(Float, comment="过去 24h 花费环比 %")
    gmv_change_24h = Column(Float, comment="过去 24h GMV 环比 %")
    roas_change_24h = Column(Float, comment="过去 24h ROAS 环比 %")
    profit_change_24h = Column(Float, comment="过去 24h 利润环比 %")

    # ===== 周期对比 =====
    vs_yesterday_gmv_pct = Column(Float, comment="VS 昨日 GMV %")
    vs_last_week_gmv_pct = Column(Float, comment="VS 上周同期 GMV %")
    vs_yesterday_roas_pct = Column(Float, comment="VS 昨日 ROAS %")
    vs_last_week_roas_pct = Column(Float, comment="VS 上周同期 ROAS %")

    __table_args__ = (
        Index("ix_account_snapshot_time", "advertiser_id", "snapshot_time"),
        Index("ix_account_snapshot_date", "advertiser_id", "stat_date"),
    )

    def __repr__(self):
        return f"<AccountSnapshot {self.advertiser_id} @ {self.snapshot_time}>"


class DailyReport(Base, TimestampMixin):
    """
    每日报表 — 日结时生成（23:59）
    用于长期趋势分析
    """
    __tablename__ = "daily_reports"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)
    report_date = Column(Date, nullable=False, index=True)

    # 核心指标
    spend = Column(Float, default=0.0)
    gmv = Column(Float, default=0.0)
    orders = Column(Integer, default=0)
    roas = Column(Float, default=0.0)
    real_profit = Column(Float, default=0.0)
    real_margin = Column(Float, default=0.0)

    # 对标数据
    gmv_target = Column(Float, comment="当日 GMV 目标")
    gmv_progress = Column(Float, comment="目标达成率 %")
    roas_target = Column(Float, comment="当日 ROAS 目标")

    # 周期对比
    vs_yesterday_gmv_pct = Column(Float)
    vs_last_week_gmv_pct = Column(Float)
    vs_yesterday_roas_pct = Column(Float)
    vs_last_week_roas_pct = Column(Float)

    # 摘要
    notes = Column(String(512), comment="当日备注，如大促/测试")

    __table_args__ = (
        Index("ix_daily_report_date", "advertiser_id", "report_date"),
    )


class RiskAlert(Base, TimestampMixin):
    """
    风险告警 — 实时生成
    超过 ROI 保本线、CMO 快速下跌等
    """
    __tablename__ = "risk_alerts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)

    # 告警类型
    alert_type = Column(String(50), comment="CMO_DROP / ROI_BELOW_BREAKEVEN / BUDGET_EXCEED")
    severity = Column(String(20), comment="INFO / WARNING / CRITICAL")

    # 告警内容
    title = Column(String(256))
    message = Column(String(1024))

    # 指标数据
    metric_name = Column(String(50), comment="CMO / ROI / Hook Rate")
    current_value = Column(Float, comment="当前值")
    threshold = Column(Float, comment="阈值/目标值")
    change_pct = Column(Float, comment="环比 %")

    # 止损建议
    recommended_action = Column(String(50), comment="pause / reduce_budget / monitor")
    action_params = Column(String(512), comment="JSON 格式的建议参数")

    # 状态
    status = Column(String(20), comment="active / acknowledged / resolved")
    resolved_at = Column(DateTime, comment="解决时间")
    resolved_by = Column(String(64), comment="处理人 ID")

    __table_args__ = (
        Index("ix_risk_alert_time", "advertiser_id", "created_at"),
        Index("ix_risk_alert_status", "advertiser_id", "status"),
    )


class HourlyMetrics(Base, TimestampMixin):
    """
    小时级时间序列 — 用于趋势分析和预测
    """
    __tablename__ = "hourly_metrics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)

    # 时间（精确到小时）
    hour_start = Column(DateTime(timezone=True), nullable=False, index=True)
    hour_end = Column(DateTime(timezone=True))

    # 指标
    spend = Column(Float, default=0.0)
    gmv = Column(Float, default=0.0)
    orders = Column(Integer, default=0)
    impressions = Column(BigInteger, default=0)
    clicks = Column(BigInteger, default=0)
    cpc = Column(Float, default=0.0)
    cpm = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)

    # 计算列
    cpa = Column(Float, comment="转化成本")
    cmo = Column(Float, comment="订单成本")
    roas = Column(Float, default=0.0)

    __table_args__ = (
        Index("ix_hourly_metrics_time", "advertiser_id", "hour_start"),
    )


class GrowthRecommendation(Base, TimestampMixin):
    """
    梯度增长建议 — 为新投放/素材生成的预算建议
    """
    __tablename__ = "growth_recommendations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    advertiser_id = Column(String(64), ForeignKey("advertisers.advertiser_id"),
                           nullable=False, index=True)

    # 投放对象
    object_type = Column(String(30), comment="CAMPAIGN / ADGROUP / VIDEO")
    object_id = Column(String(128))
    object_name = Column(String(512))

    # 生命周期阶段
    current_stage = Column(String(30), comment="WARM_UP / GROWTH / PEAK")
    days_running = Column(Integer, comment="已投放天数")

    # 当前指标
    current_daily_spend = Column(Float)
    current_hook_rate = Column(Float)
    current_roas = Column(Float)

    # 三个方案
    conservative_plan = Column(String(2048), comment="JSON: Day 1-10 的预算建议")
    standard_plan = Column(String(2048), comment="JSON: 标准方案")
    aggressive_plan = Column(String(2048), comment="JSON: 激进方案")

    # 推荐
    recommended_plan = Column(String(30), comment="conservative / standard / aggressive")
    confidence = Column(Integer, comment="置信度 0-100")

    # 风险提示
    risk_notes = Column(String(1024))

    # 状态
    status = Column(String(20), comment="active / completed / cancelled")
    applied_plan = Column(String(30), comment="用户选择了哪个方案")
    applied_at = Column(DateTime, comment="应用时间")

    __table_args__ = (
        Index("ix_growth_rec_object", "advertiser_id", "object_type", "object_id"),
    )
