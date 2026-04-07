"""
飞书通知服务
- 告警推送（CRITICAL/WARNING）
- 决策待审批通知
- 每日投放日报
"""
import httpx
from typing import Optional, List, Dict, Any
from datetime import date
from loguru import logger

from app.models.alert import Alert
from app.models.decision import Decision


# 飞书消息颜色
SEVERITY_COLOR = {
    "CRITICAL": "red",
    "WARNING":  "orange",
    "INFO":     "blue",
}

SEVERITY_EMOJI = {
    "CRITICAL": "🚨",
    "WARNING":  "⚠️",
    "INFO":     "ℹ️",
}


class FeishuNotifier:
    """
    飞书 Webhook 通知（群机器人）
    webhook_url 从配置读取，可选
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self._client = httpx.AsyncClient(timeout=10.0)

    async def _send(self, payload: Dict[str, Any]) -> bool:
        if not self.webhook_url:
            logger.debug("Feishu webhook not configured, skipping notification")
            return False
        try:
            resp = await self._client.post(self.webhook_url, json=payload)
            data = resp.json()
            if data.get("code") == 0 or data.get("StatusCode") == 0:
                return True
            logger.warning(f"Feishu notification failed: {data}")
            return False
        except Exception as e:
            logger.error(f"Feishu send error: {e}")
            return False

    async def send_alert(self, alert: Alert) -> bool:
        """发送告警通知"""
        emoji = SEVERITY_EMOJI.get(alert.severity, "⚠️")
        color = SEVERITY_COLOR.get(alert.severity, "orange")

        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"{emoji} {alert.title}",
                    },
                    "template": color,
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**广告账户**\n{alert.advertiser_id}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**告警类型**\n{alert.alert_type}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**严重程度**\n{alert.severity}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**对象**\n{alert.object_name or alert.object_id}"}},
                        ],
                    },
                    {
                        "tag": "div",
                        "text": {"tag": "lark_md", "content": f"**详情**\n{alert.message}"},
                    },
                    {"tag": "hr"},
                    {
                        "tag": "note",
                        "elements": [{"tag": "plain_text", "content": f"告警ID: {alert.id} · {alert.created_at}"}],
                    },
                ],
            },
        }
        return await self._send(payload)

    async def send_decision_pending(self, decision: Decision) -> bool:
        """发送待审批决策通知"""
        action_cn = {
            "pause": "暂停投放",
            "enable": "启用投放",
            "increase_budget": "提高预算",
            "decrease_budget": "降低预算",
            "increase_bid": "提高出价",
            "decrease_bid": "降低出价",
            "replace_creative": "建议换素材",
            "no_action": "观察不操作",
        }.get(decision.action, decision.action)

        confidence_bar = "█" * int(decision.confidence * 10) + "░" * (10 - int(decision.confidence * 10))

        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {"tag": "plain_text", "content": f"🤖 LLM 决策待审批：{action_cn}"},
                    "template": "yellow",
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**账户**\n{decision.advertiser_id}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**对象**\n{decision.object_name or decision.object_id}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**建议动作**\n{action_cn}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**置信度**\n{confidence_bar} {decision.confidence:.0%}"}},
                        ],
                    },
                    {
                        "tag": "div",
                        "text": {"tag": "lark_md", "content": f"**决策理由**\n{decision.reason}"},
                    },
                    {"tag": "hr"},
                    {
                        "tag": "note",
                        "elements": [{"tag": "plain_text", "content": f"决策ID: {decision.id} · 请在后台审批"}],
                    },
                ],
            },
        }
        return await self._send(payload)

    async def send_daily_report(self, stats: Dict[str, Any]) -> bool:
        """发送每日投放日报"""
        today = date.today().strftime("%Y-%m-%d")

        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {"tag": "plain_text", "content": f"📊 TikTok 广告日报 · {today}"},
                    "template": "blue",
                },
                "elements": [
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**今日总花费**\n${stats.get('total_spend', 0):.2f}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**总曝光**\n{stats.get('total_impressions', 0):,}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**总点击**\n{stats.get('total_clicks', 0):,}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**总转化**\n{stats.get('total_conversion', 0):,}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**平均CTR**\n{stats.get('avg_ctr', 0):.2f}%"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**平均CPA**\n${stats.get('avg_cpa', 0):.2f}"}},
                        ],
                    },
                    {"tag": "hr"},
                    {
                        "tag": "div",
                        "fields": [
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**活跃账户**\n{stats.get('active_advertisers', 0)}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**今日告警**\n{stats.get('alerts_today', 0)}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**自动执行决策**\n{stats.get('auto_decisions', 0)}"}},
                            {"is_short": True, "text": {"tag": "lark_md", "content": f"**待审批决策**\n{stats.get('pending_decisions', 0)}"}},
                        ],
                    },
                ],
            },
        }
        return await self._send(payload)

    async def close(self):
        await self._client.aclose()
