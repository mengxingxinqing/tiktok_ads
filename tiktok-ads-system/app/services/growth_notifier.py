"""
飞书通知服务 — 涨粉模块专用
"""
import httpx
from typing import Optional
from loguru import logger


class GrowthFeishuNotifier:
    """涨粉模块飞书通知（复用现有 FeishuNotifier 的逻辑）"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self._client = httpx.AsyncClient(timeout=10.0)

    async def _send(self, payload: dict) -> bool:
        if not self.webhook_url:
            logger.debug("Feishu webhook not configured")
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

    async def notify_campaign_completed(
        self,
        campaign_id: str,
        tk_account: str,
        followers_gained: int,
        total_spend: float,
        auto_stop_reason: str,
    ):
        """Campaign 达标/停止通知"""
        emoji_map = {
            "REACHED_TARGET": "✅",
            "OVER_BUDGET": "⚠️",
            "OVER_COST_LIMIT": "🚨",
            "MANUAL": "🛑",
        }
        emoji = emoji_map.get(auto_stop_reason, "📢")
        cost_per_10k = (total_spend / followers_gained * 10000) if followers_gained > 0 else 0

        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": f"{emoji} 涨粉 Campaign {campaign_id[:8]}... 已结束",
                    "template": "purple" if auto_stop_reason == "REACHED_TARGET" else "red",
                },
                "elements": [
                    {"tag": "div", "text": {"content": f"**TK账号：** @{tk_account}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**粉丝增量：** +{followers_gained:,}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**总花费：** ${total_spend:.2f}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**万粉成本：** ${cost_per_10k:.2f}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**停止原因：** {auto_stop_reason}", "type": "markdown"}},
                ],
            },
        }
        await self._send(payload)

    async def notify_budget_exhausted_undershoot(
        self,
        campaign_id: str,
        tk_account: str,
        followers_gained: int,
        target_followers: int,
        total_spend: float,
        budget: float,
        currency: str = "USD",
    ):
        """
        Case 3：预算烧完但未达粉丝目标 —— 等待人工决策（不自动做决定）
        """
        ratio = followers_gained / target_followers if target_followers else 0
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {"title": "⚠️ 预算烧完未达标 - 需要人工决策", "template": "orange"},
                "elements": [
                    {"tag": "div", "text": {"content": f"**Campaign：** `{campaign_id}`", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**TK账号：** @{tk_account}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**已涨粉：** +{followers_gained:,} / {target_followers:,} ({ratio:.1%})", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**花费：** {currency} {total_spend:.2f} / {budget:.2f}（已烧完）", "type": "markdown"}},
                    {"tag": "hr"},
                    {"tag": "div", "text": {"content": "可选动作：\n- **继续**：在该 TK 下重建 Campaign（会新起预算）\n- **换素材**：素材可能不适合，先去素材库替换后再建\n- **放弃**：接受当前达成度，不再投", "type": "markdown"}},
                ],
            },
        }
        await self._send(payload)

    async def notify_cost_alert(
        self,
        campaign_id: str,
        tk_account: str,
        current_cost: float,
        target_cost: float,
    ):
        """万粉成本超限告警"""
        ratio = current_cost / target_cost if target_cost > 0 else 0
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {"title": "🚨 万粉成本告警", "template": "red"},
                "elements": [
                    {"tag": "div", "text": {"content": f"**Campaign：** `{campaign_id[:8]}`...", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**TK账号：** @{tk_account}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**当前万粉成本：** ${current_cost:.2f}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**目标万粉成本：** ${target_cost:.2f}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": f"**超标比例：** {ratio:.1%}", "type": "markdown"}},
                    {"tag": "div", "text": {"content": "请选择：**继续投放 / 暂停 / 换素材**", "type": "markdown"}},
                ],
            },
        }
        await self._send(payload)
