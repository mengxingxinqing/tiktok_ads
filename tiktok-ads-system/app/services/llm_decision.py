"""
LLM 智能决策服务
- 把检测结果 + 历史指标 → 打包成 prompt → 调用 LLM → 解析结构化决策
- 支持动作：pause / enable / increase_budget / decrease_budget / decrease_bid / increase_bid / replace_creative / no_action
"""
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from openai import AsyncOpenAI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.services.notifier import FeishuNotifier
from app.models.advertiser import Advertiser
from app.models.product import ProductCost
from app.models.metrics import MetricsSnapshot
from app.models.decision import Decision
from app.models.alert import Alert
from app.services.tiktok_client import TikTokClient, TikTokAPIError


# 支持的动作及置信度阈值（高于此值自动执行）
ACTION_AUTO_THRESHOLD = {
    "pause":            0.85,   # 暂停广告
    "enable":           0.80,   # 启用广告
    "decrease_budget":  0.80,   # 降低预算
    "increase_budget":  0.75,   # 提高预算
    "decrease_bid":     0.78,   # 降低出价
    "increase_bid":     0.75,   # 提高出价
    "replace_creative": 0.70,   # 建议换素材（通知为主，不自动执行）
    "no_action":        0.0,    # 观察，不操作
}

# 需要人工确认的高风险动作（不管置信度多高都不自动执行）
MANUAL_ONLY_ACTIONS = {"replace_creative"}


SYSTEM_PROMPT = """你是一位专业的 TikTok 广告投放优化专家，拥有丰富的数字营销经验。
你的任务是分析广告投放数据，发现问题，并给出具体的优化建议。

## 分析维度
1. 投放效率：CTR、CPM、CPC 是否健康
2. 转化质量：CVR、CPA 是否达标
3. 预算利用率：花费趋势是否正常
4. 素材表现：视频完播率、互动指标

## 输出要求
必须以 JSON 格式输出，字段：
{
  "action": "pause|enable|increase_budget|decrease_budget|increase_bid|decrease_bid|replace_creative|no_action",
  "action_params": {},  // 动作参数，如 {"budget": 500, "reason": "提高20%"}
  "confidence": 0.0~1.0,  // 置信度
  "reason": "决策理由（中文，简洁明了）",
  "risk_level": "low|medium|high",
  "suggestions": ["建议1", "建议2"]  // 附加建议
}

## 置信度标准
- 0.9+：数据明确，强烈建议操作
- 0.8~0.9：数据倾向明显，建议操作
- 0.7~0.8：有一定依据，可以考虑
- <0.7：数据不足，建议观察

不要输出任何 JSON 以外的内容。"""


def build_prompt(
    alert: Alert,
    snapshots: List,   # MetricsSnapshot 或 CreativeSnapshot
    advertiser_context: Dict[str, Any],
) -> str:
    """构建 LLM 分析 prompt，兼容 Ad 级和素材级告警"""

    is_creative = alert.data_level == "CREATIVE"

    # 整理近期指标趋势
    recent_data = []
    for s in snapshots[-7:]:
        if is_creative:
            recent_data.append({
                "date": str(s.stat_date),
                "spend": s.spend,
                "impressions": s.impressions,
                "ctr": s.ctr,
                "video_play_actions": s.video_play_actions,
                "hook_rate":   f"{s.hook_rate:.2f}%",
                "hold_rate":   f"{s.hold_rate:.2f}%",
                "avg_play_sec": s.average_video_play,
                "conversion": s.conversion,
                "lifecycle_stage": s.lifecycle_stage,
                "days_running": s.days_running,
            })
        else:
            recent_data.append({
                "date": str(s.stat_date),
                "spend": s.spend,
                "impressions": s.impressions,
                "clicks": s.clicks,
                "ctr": s.ctr,
                "cpm": s.cpm,
                "conversion": s.conversion,
                "cost_per_conversion": s.cost_per_conversion,
                "video_play_actions": s.video_play_actions,
                "video_watched_2s": s.video_watched_2s,
                "video_watched_6s": s.video_watched_6s,
            })

    # 账户基准线（素材告警时提供）
    benchmark_section = ""
    if is_creative and advertiser_context.get("benchmark"):
        b = advertiser_context["benchmark"]
        benchmark_section = f"""
## 账户内素材基准值（近3天均值）
- 平均 Hook Rate: {b.get('avg_hook_rate', 0):.1f}%
- 平均 Hold Rate: {b.get('avg_hold_rate', 0):.1f}%
- 平均 CTR: {b.get('avg_ctr', 0):.2f}%
- 平均 CPA: ${b.get('avg_cpa', 0):.2f}
"""

    level_label = "素材" if is_creative else "广告"

    # 利润/成本信息
    profit_section = ""
    pc = advertiser_context.get("profit_context")
    if pc:
        be_roas = f"{pc['break_even_roas']}" if pc.get("break_even_roas") else "未计算（缺少售价）"
        profit_section = f"""
## 商品成本参考（账户均值，{pc['product_count']} 个 SKU）
- 货品成本: ${pc['avg_product_cost']}/件
- 头程运费: ${pc['avg_freight_in']}/件
- 尾程运费: ${pc['avg_freight_out']}/件
- 每件固定成本合计: ${pc['avg_fixed_cost']}
- 达人佣金率: {pc['avg_affiliate_rate']}%
- 平台抽佣率: {pc['avg_platform_rate']}%
- 退货率: {pc['avg_return_rate']}%
- 货损率: {pc['avg_damage_rate']}%
- 平均售价: ${pc['avg_selling_price']}
- ⚠️ 保本 ROAS: {be_roas}（低于此值即亏损）
"""

    # 冷启动期提示
    cold_start_warning = ""
    if is_creative and snapshots:
        days_running = getattr(snapshots[-1], "days_running", 0) or 0
        if days_running < 7:
            cold_start_warning = f"""
⚠️ 注意：该素材当前处于冷启动保护期（已投放 {days_running} 天，< 7天）。
GMV Max 前7天数据波动属正常，学习期内系统仍在摸索人群。
请在决策时保持谨慎，优先选择"观察"而非激进操作。
若确实需要操作，confidence 不应超过 0.7。
"""

    prompt = f"""## 告警信息
- 告警类型: {alert.alert_type}
- 严重程度: {alert.severity}
- 告警标题: {alert.title}
- 告警详情: {alert.message}

## {level_label}信息
- 广告账户: {alert.advertiser_id}
- 数据层级: {alert.data_level}
- 对象ID: {alert.object_id}
- 对象名称: {alert.object_name or '未知'}
- 账户货币: {advertiser_context.get('currency', 'USD')}
{benchmark_section}{profit_section}
{cold_start_warning}
## 近期数据趋势（最近{len(recent_data)}天）
{json.dumps(recent_data, ensure_ascii=False, indent=2)}

## 触发告警时的指标
{json.dumps(alert.metrics_snapshot or {}, ensure_ascii=False, indent=2)}

请结合以上数据，判断该{level_label}的问题根因，给出明确的操作建议。"""

    return prompt


class LLMDecisionService:

    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.LLM_API_BASE,
            api_key=settings.LLM_API_KEY,
        )

    async def analyze(
        self,
        alert: Alert,
        snapshots: List[MetricsSnapshot],
        advertiser_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """调用 LLM 分析，返回结构化决策"""
        prompt = build_prompt(alert, snapshots, advertiser_context)

        try:
            response = await self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,  # 决策类任务用低温度
                max_tokens=800,
                response_format={"type": "json_object"},
            )

            raw = response.choices[0].message.content
            result = json.loads(raw)

            # 校验必要字段
            if "action" not in result:
                result["action"] = "no_action"
            if "confidence" not in result:
                result["confidence"] = 0.5

            result["_raw_response"] = raw
            result["_prompt"] = prompt
            return result

        except json.JSONDecodeError as e:
            logger.error(f"LLM returned invalid JSON: {e}")
            return {"action": "no_action", "confidence": 0.0, "reason": f"LLM 响应解析失败: {e}"}
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            return {"action": "no_action", "confidence": 0.0, "reason": f"LLM 调用失败: {e}"}

    async def execute_decision(
        self,
        decision: Decision,
        advertiser: Advertiser,
        db: AsyncSession,
    ) -> bool:
        """执行 LLM 决策（写操作）"""
        client = TikTokClient(
            access_token=advertiser.access_token,
            advertiser_id=advertiser.advertiser_id,
        )
        action = decision.action
        params = decision.action_params or {}
        object_id = decision.object_id

        try:
            result = None

            if action == "pause":
                if decision.data_level == "AD":
                    result = await client.update_ad_status([object_id], "DISABLE")
                elif decision.data_level == "ADGROUP":
                    result = await client.update_adgroup_status([object_id], "DISABLE")

            elif action == "enable":
                if decision.data_level == "AD":
                    result = await client.update_ad_status([object_id], "ENABLE")
                elif decision.data_level == "ADGROUP":
                    result = await client.update_adgroup_status([object_id], "ENABLE")

            elif action == "decrease_budget":
                budget = params.get("budget")
                if budget and decision.data_level == "ADGROUP":
                    result = await client.update_adgroup_budget(object_id, float(budget))
                elif budget and decision.data_level == "CAMPAIGN":
                    result = await client.update_campaign_budget(object_id, float(budget))

            elif action == "increase_budget":
                budget = params.get("budget")
                if budget and decision.data_level == "ADGROUP":
                    result = await client.update_adgroup_budget(object_id, float(budget))
                elif budget and decision.data_level == "CAMPAIGN":
                    result = await client.update_campaign_budget(object_id, float(budget))

            elif action in ("no_action", "replace_creative"):
                # 不执行操作，只记录
                decision.status = "SKIPPED"
                decision.executed_at = datetime.now(timezone.utc)
                await db.commit()
                return True

            # 记录执行结果
            decision.status = "AUTO_EXECUTED"
            decision.is_auto_executed = True
            decision.executed_at = datetime.now(timezone.utc)
            decision.execution_result = result
            await db.commit()

            logger.info(f"Decision executed: {action} on {object_id} -> {result}")
            return True

        except TikTokAPIError as e:
            logger.error(f"TikTok API error executing decision {decision.id}: {e}")
            decision.status = "FAILED"
            decision.error_message = str(e)
            await db.commit()
            return False
        except Exception as e:
            logger.exception(f"Unexpected error executing decision {decision.id}: {e}")
            decision.status = "FAILED"
            decision.error_message = str(e)
            await db.commit()
            return False
        finally:
            await client.close()

    async def process_alert(
        self,
        alert: Alert,
        db: AsyncSession,
    ) -> Optional[Decision]:
        """
        完整流程：告警 → LLM 分析 → 存决策 → 按置信度决定是否自动执行
        """
        # 1. 获取广告主信息
        result = await db.execute(
            select(Advertiser).where(Advertiser.advertiser_id == alert.advertiser_id)
        )
        advertiser = result.scalar_one_or_none()
        if not advertiser:
            logger.warning(f"Advertiser not found: {alert.advertiser_id}")
            return None

        # 2. 获取历史指标（素材级 or Ad 级）
        from datetime import date, timedelta
        since = date.today() - timedelta(days=14)

        # 2.5 尝试获取成本配置（用于利润计算）
        profit_context = await self._get_profit_context(
            advertiser_id=alert.advertiser_id,
            db=db,
        )

        if alert.data_level == "CREATIVE":
            from app.models.creative import CreativeSnapshot
            from app.services.creative_detector import CreativeDetector
            metrics_result = await db.execute(
                select(CreativeSnapshot)
                .where(
                    CreativeSnapshot.advertiser_id == alert.advertiser_id,
                    CreativeSnapshot.video_id == alert.object_id,
                    CreativeSnapshot.stat_date >= since,
                )
                .order_by(CreativeSnapshot.stat_date.asc())
            )
            snapshots = metrics_result.scalars().all()
            # 获取账户基准
            detector = CreativeDetector(db)
            benchmark = await detector._get_benchmark(alert.advertiser_id)
            advertiser_context = {
                "currency": advertiser.currency or "USD",
                "benchmark": benchmark,
                "profit_context": profit_context,
            }
        else:
            metrics_result = await db.execute(
                select(MetricsSnapshot)
                .where(
                    MetricsSnapshot.advertiser_id == alert.advertiser_id,
                    MetricsSnapshot.object_id == alert.object_id,
                    MetricsSnapshot.stat_date >= since,
                )
                .order_by(MetricsSnapshot.stat_date.asc())
            )
            snapshots = metrics_result.scalars().all()
            advertiser_context = {
                "currency": advertiser.currency or "USD",
                "profit_context": profit_context,
            }

        # 3. 调用 LLM 分析
        llm_result = await self.analyze(
            alert=alert,
            snapshots=snapshots,
            advertiser_context=advertiser_context,
        )

        action = llm_result.get("action", "no_action")
        confidence = float(llm_result.get("confidence", 0.0))
        auto_threshold = ACTION_AUTO_THRESHOLD.get(action, 1.0)
        should_auto = (
            confidence >= auto_threshold
            and action not in MANUAL_ONLY_ACTIONS
        )

        # 4. 保存决策记录
        decision = Decision(
            advertiser_id=alert.advertiser_id,
            data_level=alert.data_level,
            object_id=alert.object_id,
            object_name=alert.object_name,
            trigger_type="ANOMALY",
            trigger_reason=alert.message,
            metrics_context=alert.metrics_snapshot,
            llm_prompt=llm_result.get("_prompt", ""),
            llm_response=llm_result.get("_raw_response", ""),
            action=action,
            action_params=llm_result.get("action_params", {}),
            confidence=confidence,
            reason=llm_result.get("reason", ""),
            status="PENDING",
        )
        db.add(decision)
        await db.flush()  # 获取 decision.id

        # 5. 自动执行或等待人工审批
        if should_auto:
            logger.info(f"Auto-executing decision {decision.id}: {action} (confidence={confidence:.2f})")
            await self.execute_decision(decision, advertiser, db)
        else:
            logger.info(
                f"Decision {decision.id} queued for manual review: "
                f"{action} (confidence={confidence:.2f} < threshold={auto_threshold})"
            )
            decision.status = "PENDING"

        await db.commit()

        # 推飞书通知
        notifier = FeishuNotifier(webhook_url=settings.FEISHU_WEBHOOK_URL)
        try:
            # 告警通知（CRITICAL 必推，WARNING 有决策时推）
            if alert.severity == "CRITICAL":
                await notifier.send_alert(alert)
            # 待审批决策通知
            if decision.status == "PENDING":
                await notifier.send_decision_pending(decision)
        finally:
            await notifier.close()

        return decision

    @staticmethod
    async def _get_profit_context(
        advertiser_id: str,
        db,
    ) -> Optional[Dict[str, Any]]:
        """从 product_costs 表拉取账户成本均值，供 LLM 决策参考"""
        try:
            from sqlalchemy import func as sqlfunc
            result = await db.execute(
                select(
                    sqlfunc.avg(ProductCost.product_cost).label("avg_product_cost"),
                    sqlfunc.avg(ProductCost.freight_inbound).label("avg_inbound"),
                    sqlfunc.avg(ProductCost.freight_outbound).label("avg_outbound"),
                    sqlfunc.avg(ProductCost.affiliate_rate).label("avg_affiliate"),
                    sqlfunc.avg(ProductCost.platform_fee_rate).label("avg_platform"),
                    sqlfunc.avg(ProductCost.return_rate).label("avg_return"),
                    sqlfunc.avg(ProductCost.damage_rate).label("avg_damage"),
                    sqlfunc.avg(ProductCost.selling_price).label("avg_price"),
                    sqlfunc.count(ProductCost.id).label("product_count"),
                ).where(
                    ProductCost.advertiser_id == advertiser_id,
                    ProductCost.is_active == True,
                )
            )
            row = result.one()
            if not row.product_count:
                return None

            avg_price = float(row.avg_price or 0)
            avg_fixed = (
                float(row.avg_product_cost or 0)
                + float(row.avg_inbound or 0)
                + float(row.avg_outbound or 0)
            )
            variable_rate = (
                float(row.avg_affiliate or 0) + float(row.avg_platform or 5)
            ) / 100

            # 估算保本 ROAS
            break_even_roas = None
            if avg_price > 0 and avg_fixed > 0:
                net_price = avg_price * (
                    1 - float(row.avg_return or 0) / 100
                      - float(row.avg_damage or 0) / 100
                )
                margin = net_price * (1 - variable_rate) - avg_fixed
                if margin > 0:
                    break_even_roas = round(net_price / margin, 2)

            return {
                "product_count":      int(row.product_count),
                "avg_product_cost":   round(float(row.avg_product_cost or 0), 2),
                "avg_freight_in":     round(float(row.avg_inbound or 0), 2),
                "avg_freight_out":    round(float(row.avg_outbound or 0), 2),
                "avg_fixed_cost":     round(avg_fixed, 2),
                "avg_affiliate_rate": round(float(row.avg_affiliate or 0), 2),
                "avg_platform_rate":  round(float(row.avg_platform or 5), 2),
                "avg_return_rate":    round(float(row.avg_return or 0), 2),
                "avg_damage_rate":    round(float(row.avg_damage or 0), 2),
                "avg_selling_price":  round(avg_price, 2),
                "break_even_roas":    break_even_roas,
            }
        except Exception as e:
            logger.warning(f"Failed to get profit context for {advertiser_id}: {e}")
            return None
