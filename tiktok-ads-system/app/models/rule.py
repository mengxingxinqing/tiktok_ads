"""
告警规则模型 — 可配置规则引擎的数据库模型
"""
from sqlalchemy import BigInteger, Boolean, Column, JSON, String, Text

from app.models.base import Base, TimestampMixin


class AlertRule(Base, TimestampMixin):
    __tablename__ = "alert_rules"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    rule_key = Column(String(64), unique=True, nullable=False)  # 规则唯一标识
    rule_name = Column(String(128))                              # 规则名称（中文）
    description = Column(Text)                                  # 规则说明
    category = Column(String(32))                               # gmvmax / ad / creative

    # 规则参数（JSON存储，用户可配置）
    params = Column(JSON)  # 例如 {"threshold": 1.0, "min_spend": 5.0}

    severity = Column(String(16), default="WARNING")  # INFO / WARNING / CRITICAL
    is_enabled = Column(Boolean, default=True)

    # 作用范围
    advertiser_id = Column(String(64), nullable=True)  # null = 全局规则


# 默认规则定义（写在代码里，首次启动时写入数据库）
DEFAULT_RULES = [
    # -------- GMVMax 规则 --------
    {
        "rule_key": "GMVMAX_ROI_CRITICAL",
        "rule_name": "GMVMax ROI 亏损",
        "description": "今日 ROI < min_roi（花费高于 GMV 收入），且花费超过 min_spend",
        "category": "gmvmax",
        "params": {"min_roi": 1.0, "min_spend": 5.0},
        "severity": "CRITICAL",
    },
    {
        "rule_key": "GMVMAX_ROI_DROP",
        "rule_name": "GMVMax ROI 大幅下降",
        "description": "今日 ROI 较 lookback_days 日均值下降超过 drop_pct%",
        "category": "gmvmax",
        "params": {"drop_pct": 30, "lookback_days": 7, "min_spend": 10.0},
        "severity": "WARNING",
    },
    {
        "rule_key": "GMVMAX_ZERO_GMV",
        "rule_name": "GMVMax 无转化",
        "description": "花费超过 min_spend 但 GMV 收入为 0",
        "category": "gmvmax",
        "params": {"min_spend": 20.0},
        "severity": "CRITICAL",
    },
    {
        "rule_key": "GMVMAX_BUDGET_BURN",
        "rule_name": "GMVMax 花费激增",
        "description": "今日花费超过昨日 surge_pct%（例如 200 = 今日是昨日的 3x）",
        "category": "gmvmax",
        "params": {"surge_pct": 200},
        "severity": "WARNING",
    },
    {
        "rule_key": "GMVMAX_GMV_SURGE",
        "rule_name": "GMVMax GMV 大幅增长",
        "description": "今日 GMV 超过 lookback_days 日均值 surge_pct%（利好提示）",
        "category": "gmvmax",
        "params": {"surge_pct": 150, "lookback_days": 7},
        "severity": "INFO",
    },
    # -------- 通用 Ad 规则 --------
    {
        "rule_key": "AD_CTR_LOW",
        "rule_name": "CTR 过低",
        "description": "有花费时 CTR 低于 threshold%",
        "category": "ad",
        "params": {"threshold": 0.5},
        "severity": "WARNING",
    },
    {
        "rule_key": "AD_ZERO_SPEND",
        "rule_name": "广告无花费",
        "description": "近3日有历史花费，但今日花费为 0",
        "category": "ad",
        "params": {"min_avg_spend": 10.0},
        "severity": "WARNING",
    },
    {
        "rule_key": "AD_CPM_HIGH",
        "rule_name": "CPM 异常偏高",
        "description": "今日 CPM 超过 7 日历史均值 multiplier 倍",
        "category": "ad",
        "params": {"multiplier": 2.0},
        "severity": "WARNING",
    },
]
