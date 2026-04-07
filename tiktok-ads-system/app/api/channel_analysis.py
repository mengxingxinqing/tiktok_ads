"""
渠道来源分析接口（Channel Analysis）

区分 SELF_OWNED（渠道号/自有直播）和 AFFILIATE（达人联盟）两种订单来源，
提供大盘概览、达人排行、对比分析等端点。

GET /channel/overview     大盘概览（渠道 vs 达人贡献）
GET /channel/affiliates   达人维度排行
GET /channel/compare      渠道号 vs 达人号 详细对比
"""
from collections import defaultdict
from datetime import date, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.metrics import MetricsSnapshot

router = APIRouter(prefix="/channel", tags=["Channel Analysis"])

# 支持的 data_level（按优先级排）
_SOURCE_LEVELS = ("ORDER_SOURCE", "GMVMAX_SOURCE")


async def _get_source_rows(
    db: AsyncSession,
    advertiser_id: str,
    since: date,
    today: date,
    shop_id: Optional[str] = None,
) -> List[MetricsSnapshot]:
    """
    从 MetricsSnapshot 中查询 ORDER_SOURCE / GMVMAX_SOURCE 数据。
    若无数据，返回空列表（由调用方决定 fallback 策略）。
    """
    conditions = [
        MetricsSnapshot.advertiser_id == advertiser_id,
        MetricsSnapshot.data_level.in_(_SOURCE_LEVELS),
        MetricsSnapshot.stat_date >= since,
        MetricsSnapshot.stat_date <= today,
    ]
    if shop_id:
        # shop_id 可能存在于 object_id 或 affiliate_id，这里暂时通过 advertiser_id 过滤
        pass  # 已通过 advertiser_id 限制

    result = await db.execute(select(MetricsSnapshot).where(*conditions))
    return result.scalars().all()


async def _fallback_from_api(
    advertiser_id: str,
    access_token: str,
    start_date: str,
    end_date: str,
) -> List[dict]:
    """
    实时从 get_order_report() 拉取并返回原始行列表（fallback 用）。
    返回格式：list of {date, order_source, gmv, orders, commission_amount, commission_rate,
                       affiliate_id, affiliate_name, spend}
    """
    from app.services.tiktok_client import TikTokClient
    client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
    try:
        order_data = await client.get_order_report(
            start_date=start_date,
            end_date=end_date,
            include_affiliate=True,
        )
        rows = order_data.get("list", [])
        aggregated: dict = defaultdict(lambda: {
            "gmv": 0.0, "orders": 0,
            "commission_amount": 0.0, "commission_rate_sum": 0.0,
            "commission_rate_count": 0,
            "affiliate_ids": set(), "affiliate_names": set(),
        })
        for row in rows:
            dims = row.get("dimensions", {})
            metrics = row.get("metrics", {})
            day_raw = dims.get("stat_time_day", "")
            day = day_raw.split(" ")[0] if day_raw else ""
            source = dims.get("order_source") or metrics.get("order_source") or "SELF_OWNED"
            key = (day, source)
            aggregated[key]["gmv"] += float(metrics.get("order_amount", 0) or 0)
            aggregated[key]["orders"] += 1
            if source == "AFFILIATE":
                aggregated[key]["commission_amount"] += float(metrics.get("commission_amount", 0) or 0)
                cr = float(metrics.get("commission_rate", 0) or 0)
                if cr > 0:
                    aggregated[key]["commission_rate_sum"] += cr
                    aggregated[key]["commission_rate_count"] += 1
                aff_id = metrics.get("affiliate_id") or dims.get("affiliate_id")
                aff_name = metrics.get("affiliate_name") or dims.get("affiliate_name")
                if aff_id:
                    aggregated[key]["affiliate_ids"].add(str(aff_id))
                if aff_name:
                    aggregated[key]["affiliate_names"].add(str(aff_name))

        result = []
        for (day, source), data in aggregated.items():
            avg_cr = (
                data["commission_rate_sum"] / data["commission_rate_count"]
                if data["commission_rate_count"] > 0 else 0.0
            )
            result.append({
                "date": day,
                "order_source": source,
                "gmv": data["gmv"],
                "orders": data["orders"],
                "commission_amount": data["commission_amount"],
                "commission_rate": avg_cr,
                "affiliate_ids": ",".join(sorted(data["affiliate_ids"])),
                "affiliate_names": ",".join(sorted(data["affiliate_names"])),
                "spend": 0.0,  # fallback 时无 spend 数据
            })
        return result
    except Exception:
        return []
    finally:
        await client.close()


def _rows_to_dicts(rows: List[MetricsSnapshot]) -> List[dict]:
    """MetricsSnapshot 行 → 统一字典格式"""
    return [
        {
            "date": str(r.stat_date),
            "order_source": r.source_type or "SELF_OWNED",
            "gmv": float(r.gross_revenue or 0),
            "orders": int(r.conversion or 0),
            "commission_amount": float(r.commission_amount or 0),
            "commission_rate": float(r.commission_rate or 0),
            "affiliate_ids": r.affiliate_id or "",
            "affiliate_names": r.affiliate_name or "",
            "spend": float(r.spend or 0),
        }
        for r in rows
    ]


@router.get("/overview")
async def channel_overview(
    advertiser_id: str = Query(..., description="广告账户 ID"),
    days: int = Query(7, ge=1, le=90, description="统计天数"),
    shop_id: Optional[str] = Query(None, description="店铺 ID（可选过滤）"),
    db: AsyncSession = Depends(get_db),
):
    """
    渠道来源大盘概览：自有渠道 vs 达人联盟贡献

    返回：
    - total: 总花费/GMV/订单/ROI
    - self_owned: 渠道号贡献（GMV、订单数、占比）
    - affiliate: 达人号贡献（GMV、订单数、占比、佣金）
    - trend: 每日趋势（self_owned_gmv / affiliate_gmv / total_gmv）
    """
    today = date.today()
    since = today - timedelta(days=days)

    # 1. 先查数据库
    db_rows = await _get_source_rows(db, advertiser_id, since, today, shop_id)
    if db_rows:
        data = _rows_to_dicts(db_rows)
    else:
        # fallback: 实时拉取
        adv_result = await db.execute(
            select(__import__("app.models.advertiser", fromlist=["Advertiser"]).Advertiser)
            .where(__import__("app.models.advertiser", fromlist=["Advertiser"]).Advertiser.advertiser_id == advertiser_id)
        )
        adv = adv_result.scalar_one_or_none()
        if not adv or not adv.access_token:
            data = []
        else:
            data = await _fallback_from_api(
                advertiser_id=advertiser_id,
                access_token=adv.access_token,
                start_date=since.strftime("%Y-%m-%d"),
                end_date=today.strftime("%Y-%m-%d"),
            )

    # 2. 汇总 GMVMax Campaign 级别的 spend（总花费来源）
    spend_result = await db.execute(
        select(func.sum(MetricsSnapshot.spend))
        .where(
            MetricsSnapshot.advertiser_id == advertiser_id,
            MetricsSnapshot.data_level == "GMVMAX_CAMPAIGN",
            MetricsSnapshot.stat_date >= since,
            MetricsSnapshot.stat_date <= today,
        )
    )
    total_spend = float(spend_result.scalar() or 0)

    # 3. 按 order_source 聚合
    so_gmv = so_orders = 0.0
    aff_gmv = aff_orders = aff_commission = 0.0
    trend_daily: dict = defaultdict(lambda: {"self_owned_gmv": 0.0, "affiliate_gmv": 0.0})

    for row in data:
        source = row["order_source"]
        gmv = row["gmv"]
        orders = row["orders"]
        day = row["date"]

        if source == "SELF_OWNED":
            so_gmv += gmv
            so_orders += orders
            trend_daily[day]["self_owned_gmv"] += gmv
        elif source == "AFFILIATE":
            aff_gmv += gmv
            aff_orders += orders
            aff_commission += row["commission_amount"]
            trend_daily[day]["affiliate_gmv"] += gmv

    total_gmv = so_gmv + aff_gmv
    total_orders = int(so_orders + aff_orders)
    total_roi = round(total_gmv / total_spend, 4) if total_spend > 0 else 0.0

    def pct(part, whole):
        return round(part / whole * 100, 2) if whole > 0 else 0.0

    # trend 列表（按日期排序）
    all_days = sorted(set(
        str(since + timedelta(days=i)) for i in range(days + 1)
    ))
    trend = []
    for d in all_days:
        daily = trend_daily.get(d, {})
        so = daily.get("self_owned_gmv", 0.0)
        af = daily.get("affiliate_gmv", 0.0)
        trend.append({
            "date": d,
            "self_owned_gmv": round(so, 2),
            "affiliate_gmv": round(af, 2),
            "total_gmv": round(so + af, 2),
        })

    return {
        "advertiser_id": advertiser_id,
        "days": days,
        "total": {
            "spend": round(total_spend, 2),
            "gmv": round(total_gmv, 2),
            "orders": total_orders,
            "roi": total_roi,
        },
        "self_owned": {
            "gmv": round(so_gmv, 2),
            "orders": int(so_orders),
            "pct": pct(so_gmv, total_gmv),
        },
        "affiliate": {
            "gmv": round(aff_gmv, 2),
            "orders": int(aff_orders),
            "pct": pct(aff_gmv, total_gmv),
            "commission_amount": round(aff_commission, 2),
        },
        "trend": trend,
    }


@router.get("/affiliates")
async def channel_affiliates(
    advertiser_id: str = Query(..., description="广告账户 ID"),
    days: int = Query(7, ge=1, le=90, description="统计天数"),
    db: AsyncSession = Depends(get_db),
):
    """
    达人维度排行榜（按 GMV 倒序）

    返回：
    [ { affiliate_id, affiliate_name, gmv, orders, commission_amount, commission_rate, roi } ]
    """
    today = date.today()
    since = today - timedelta(days=days)

    # 查数据库中 AFFILIATE 来源的记录
    result = await db.execute(
        select(MetricsSnapshot).where(
            MetricsSnapshot.advertiser_id == advertiser_id,
            MetricsSnapshot.data_level.in_(_SOURCE_LEVELS),
            MetricsSnapshot.source_type == "AFFILIATE",
            MetricsSnapshot.stat_date >= since,
            MetricsSnapshot.stat_date <= today,
        )
    )
    rows = result.scalars().all()

    if not rows:
        # fallback: 实时拉取
        adv_result = await db.execute(
            select(__import__("app.models.advertiser", fromlist=["Advertiser"]).Advertiser)
            .where(__import__("app.models.advertiser", fromlist=["Advertiser"]).Advertiser.advertiser_id == advertiser_id)
        )
        adv = adv_result.scalar_one_or_none()
        if not adv or not adv.access_token:
            return []
        data = await _fallback_from_api(
            advertiser_id=advertiser_id,
            access_token=adv.access_token,
            start_date=since.strftime("%Y-%m-%d"),
            end_date=today.strftime("%Y-%m-%d"),
        )
        aff_data = [d for d in data if d["order_source"] == "AFFILIATE"]
    else:
        aff_data = _rows_to_dicts(rows)

    # 按 affiliate_id 聚合（一条记录可能包含多个达人 ID，这里做简化聚合）
    aff_agg: dict = defaultdict(lambda: {
        "gmv": 0.0, "orders": 0,
        "commission_amount": 0.0,
        "commission_rate_sum": 0.0, "commission_rate_count": 0,
        "spend": 0.0, "name": "",
    })

    for row in aff_data:
        # affiliate_ids 可能是逗号分隔的多个 ID
        ids = [x.strip() for x in row["affiliate_ids"].split(",") if x.strip()]
        names = [x.strip() for x in row["affiliate_names"].split(",") if x.strip()]
        if not ids:
            ids = ["unknown"]

        # 简化：均分 GMV 到各达人（若多个）
        n = len(ids)
        for i, aff_id in enumerate(ids):
            aff_name = names[i] if i < len(names) else ""
            aff_agg[aff_id]["gmv"] += row["gmv"] / n
            aff_agg[aff_id]["orders"] += max(1, row["orders"] // n)
            aff_agg[aff_id]["commission_amount"] += row["commission_amount"] / n
            aff_agg[aff_id]["spend"] += row["spend"] / n
            if row["commission_rate"] > 0:
                aff_agg[aff_id]["commission_rate_sum"] += row["commission_rate"]
                aff_agg[aff_id]["commission_rate_count"] += 1
            if aff_name:
                aff_agg[aff_id]["name"] = aff_name

    # 构建返回列表
    affiliate_list = []
    for aff_id, data in aff_agg.items():
        gmv = data["gmv"]
        spend = data["spend"]
        avg_cr = (
            data["commission_rate_sum"] / data["commission_rate_count"]
            if data["commission_rate_count"] > 0 else 0.0
        )
        affiliate_list.append({
            "affiliate_id": aff_id,
            "affiliate_name": data["name"],
            "gmv": round(gmv, 2),
            "orders": data["orders"],
            "commission_amount": round(data["commission_amount"], 2),
            "commission_rate": round(avg_cr, 4),
            "roi": round(gmv / spend, 4) if spend > 0 else 0.0,
        })

    # 按 GMV 倒序
    affiliate_list.sort(key=lambda x: x["gmv"], reverse=True)
    return affiliate_list


@router.get("/compare")
async def channel_compare(
    advertiser_id: str = Query(..., description="广告账户 ID"),
    days: int = Query(7, ge=1, le=90, description="统计天数"),
    db: AsyncSession = Depends(get_db),
):
    """
    渠道号 vs 达人号 对比分析

    返回：
    {
      "self_owned": { gmv, orders, avg_order_value, spend, roi },
      "affiliate":  { gmv, orders, avg_order_value, spend, roi, commission_total },
      "best_affiliate": { affiliate_id, name, gmv },
    }
    """
    today = date.today()
    since = today - timedelta(days=days)

    db_rows = await _get_source_rows(db, advertiser_id, since, today)
    if db_rows:
        data = _rows_to_dicts(db_rows)
    else:
        adv_result = await db.execute(
            select(__import__("app.models.advertiser", fromlist=["Advertiser"]).Advertiser)
            .where(__import__("app.models.advertiser", fromlist=["Advertiser"]).Advertiser.advertiser_id == advertiser_id)
        )
        adv = adv_result.scalar_one_or_none()
        if not adv or not adv.access_token:
            data = []
        else:
            data = await _fallback_from_api(
                advertiser_id=advertiser_id,
                access_token=adv.access_token,
                start_date=since.strftime("%Y-%m-%d"),
                end_date=today.strftime("%Y-%m-%d"),
            )

    # 聚合
    so = {"gmv": 0.0, "orders": 0, "spend": 0.0}
    af = {"gmv": 0.0, "orders": 0, "spend": 0.0, "commission": 0.0}
    aff_contributions: dict = defaultdict(lambda: {"gmv": 0.0, "name": ""})

    for row in data:
        source = row["order_source"]
        gmv = row["gmv"]
        orders = row["orders"]
        spend = row["spend"]

        if source == "SELF_OWNED":
            so["gmv"] += gmv
            so["orders"] += orders
            so["spend"] += spend
        elif source == "AFFILIATE":
            af["gmv"] += gmv
            af["orders"] += orders
            af["spend"] += spend
            af["commission"] += row["commission_amount"]
            # 追踪 best affiliate
            ids = [x.strip() for x in row["affiliate_ids"].split(",") if x.strip()]
            names = [x.strip() for x in row["affiliate_names"].split(",") if x.strip()]
            n = max(len(ids), 1)
            for i, aid in enumerate(ids):
                aff_contributions[aid]["gmv"] += gmv / n
                if i < len(names):
                    aff_contributions[aid]["name"] = names[i]

    def avg_ov(gmv, orders):
        return round(gmv / orders, 4) if orders > 0 else 0.0

    def roi(gmv, spend):
        return round(gmv / spend, 4) if spend > 0 else 0.0

    # best affiliate
    best_affiliate = None
    if aff_contributions:
        best_id = max(aff_contributions, key=lambda x: aff_contributions[x]["gmv"])
        best_data = aff_contributions[best_id]
        best_affiliate = {
            "affiliate_id": best_id,
            "name": best_data["name"],
            "gmv": round(best_data["gmv"], 2),
        }

    return {
        "advertiser_id": advertiser_id,
        "days": days,
        "self_owned": {
            "gmv": round(so["gmv"], 2),
            "orders": so["orders"],
            "avg_order_value": avg_ov(so["gmv"], so["orders"]),
            "spend": round(so["spend"], 2),
            "roi": roi(so["gmv"], so["spend"]),
        },
        "affiliate": {
            "gmv": round(af["gmv"], 2),
            "orders": af["orders"],
            "avg_order_value": avg_ov(af["gmv"], af["orders"]),
            "spend": round(af["spend"], 2),
            "roi": roi(af["gmv"], af["spend"]),
            "commission_total": round(af["commission"], 2),
        },
        "best_affiliate": best_affiliate,
    }
