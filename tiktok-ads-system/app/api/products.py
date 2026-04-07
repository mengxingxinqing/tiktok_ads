"""
商品成本管理接口

GET    /products/costs                  成本配置列表
POST   /products/costs                  新增/更新成本配置
DELETE /products/costs/{id}             删除
GET    /products/costs/{product_id}/profit  计算某商品的真实利润
GET    /products/profit-report          账户级利润报表（按日期）
GET    /products/profit-by-product      按品维度聚合利润
GET    /products/profit-by-shop         按店铺维度聚合利润
"""
from typing import Optional, List
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.product import ProductCost
from app.models.metrics import MetricsSnapshot
from app.services.product_discovery import ProductDiscoveryService

router = APIRouter(prefix="/products", tags=["Product Costs"])


# ===== Schemas =====

class ProductCostIn(BaseModel):
    product_id:       str
    sku_id:           Optional[str] = None
    product_name:     Optional[str] = None
    currency:         str = "USD"

    product_cost:     float = Field(0.0, ge=0, description="货品成本（含包装）")
    freight_inbound:  float = Field(0.0, ge=0, description="头程运费/件")
    freight_outbound: float = Field(0.0, ge=0, description="尾程运费/件")
    affiliate_rate:   float = Field(0.0, ge=0, le=100, description="达人佣金率 %")
    platform_fee_rate:float = Field(5.0, ge=0, le=50,  description="平台佣金率 %")
    return_rate:      float = Field(0.0, ge=0, le=100, description="退货率 %")
    damage_rate:      float = Field(0.0, ge=0, le=100, description="货损率 %")
    selling_price:    Optional[float] = None
    notes:            Optional[str] = None


# ===== 接口 =====

@router.get("/discover")
async def discover_products(
    advertiser_id: Optional[str] = None,
    bc_id: Optional[str] = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    """
    发现未配置的商品
    从近 N 天的 GMVMAX_ITEM 数据中提取 item_group_id，列出未配置的商品。
    如果提供 bc_id，会从 TikTok Shop API 获取商品名称、图片、价格等详情。
    """
    service = ProductDiscoveryService()

    if advertiser_id:
        # 单个账户
        discovery = await service.discover_products_for_advertiser(
            advertiser_id, db, limit_days=days, bc_id=bc_id,
        )
        return discovery
    else:
        # 所有账户
        discoveries = await service.discover_all_advertisers(
            db, limit_days=days, bc_id=bc_id,
        )
        return {
            "total_advertisers": len(discoveries),
            "total_pending": sum(d.get("pending_count", 0) for d in discoveries),
            "results": discoveries,
        }


@router.get("/costs")
async def list_costs(
    product_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(ProductCost).where(ProductCost.is_active == True)
    if product_id:
        query = query.where(ProductCost.product_id == product_id)
    query = query.order_by(ProductCost.updated_at.desc())

    result = await db.execute(query)
    items = result.scalars().all()
    return {"total": len(items), "items": [_fmt(c) for c in items]}


@router.post("/costs")
async def upsert_cost(body: ProductCostIn, db: AsyncSession = Depends(get_db)):
    """新增或更新（按 product_id + sku_id 匹配，同一商品只需配置一次）"""
    query = select(ProductCost).where(
        ProductCost.product_id == body.product_id,
        ProductCost.sku_id == body.sku_id,
    )
    result = await db.execute(query)
    cost = result.scalar_one_or_none()

    if cost:
        for k, v in body.model_dump(exclude={"product_id", "sku_id"}).items():
            if v is not None:
                setattr(cost, k, v)
        action = "updated"
    else:
        cost = ProductCost(**body.model_dump())
        db.add(cost)
        action = "created"

    await db.commit()
    await db.refresh(cost)
    return {"action": action, "id": cost.id, "item": _fmt(cost)}


@router.delete("/costs/{cost_id}")
async def delete_cost(cost_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductCost).where(ProductCost.id == cost_id))
    cost = result.scalar_one_or_none()
    if not cost:
        raise HTTPException(status_code=404, detail="Not found")
    cost.is_active = False
    await db.commit()
    return {"success": True}


@router.get("/costs/{product_id}/profit")
async def calc_profit(
    product_id: str,
    gmv: float,
    units_sold: int,
    ad_spend: float,
    sku_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """即时计算某商品的真实利润（传入 GMV/件数/广告花费）"""
    query = select(ProductCost).where(
        ProductCost.product_id == product_id,
        ProductCost.is_active  == True,
    )
    if sku_id:
        query = query.where(ProductCost.sku_id == sku_id)

    result = await db.execute(query.limit(1))
    cost = result.scalar_one_or_none()

    if not cost:
        raise HTTPException(status_code=404, detail="Product cost config not found")

    return cost.calc_profit(gmv=gmv, units_sold=units_sold, ad_spend=ad_spend)


@router.get("/profit-report")
async def profit_report(
    advertiser_id: Optional[str] = None,
    days: int = 7,
    db: AsyncSession = Depends(get_db),
):
    """
    账户级利润报表
    把广告花费和 GMV 数据与成本配置关联，计算真实利润
    """
    since = date.today() - timedelta(days=days)

    # 拉取广告指标（AD + GMVMAX_CAMPAIGN 层汇总）
    metrics_q = (
        select(
            MetricsSnapshot.advertiser_id,
            MetricsSnapshot.stat_date,
            func.sum(MetricsSnapshot.spend).label("ad_spend"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmvmax_revenue"),
        )
        .where(
            MetricsSnapshot.stat_date >= since,
            MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
        )
        .group_by(MetricsSnapshot.advertiser_id, MetricsSnapshot.stat_date)
    )
    if advertiser_id:
        metrics_q = metrics_q.where(MetricsSnapshot.advertiser_id == advertiser_id)

    metrics_result = await db.execute(metrics_q)
    metrics_rows = metrics_result.all()

    # 拉取成本配置（全局均值，商品不再绑定账户）
    cost_q = select(
        func.avg(ProductCost.product_cost).label("avg_product_cost"),
        func.avg(ProductCost.freight_inbound).label("avg_inbound"),
        func.avg(ProductCost.freight_outbound).label("avg_outbound"),
        func.avg(ProductCost.affiliate_rate).label("avg_affiliate"),
        func.avg(ProductCost.platform_fee_rate).label("avg_platform"),
        func.avg(ProductCost.return_rate).label("avg_return"),
        func.avg(ProductCost.damage_rate).label("avg_damage"),
        func.avg(ProductCost.selling_price).label("avg_price"),
    ).where(ProductCost.is_active == True)

    cost_result = await db.execute(cost_q)
    global_cost = cost_result.first()

    # 合并计算
    report = []
    for row in metrics_rows:
        adv_id = row.advertiser_id
        cost_row = global_cost
        gmvmax_revenue = float(row.gmvmax_revenue or 0)

        entry = {
            "advertiser_id": adv_id,
            "stat_date":     str(row.stat_date),
            "ad_spend":      round(float(row.ad_spend or 0), 2),
            "orders":        int(row.orders or 0),
            "gmvmax_revenue": round(gmvmax_revenue, 2),
            "has_cost_config": cost_row is not None and cost_row.avg_product_cost is not None,
        }

        if cost_row and cost_row.avg_product_cost is not None and row.orders and row.orders > 0:
            avg_price = float(cost_row.avg_price or 0)
            # 优先使用 GMVMax 真实收入，没有则估算
            gmv_est = gmvmax_revenue if gmvmax_revenue > 0 else avg_price * int(row.orders)

            # 用临时 ProductCost 对象计算
            pc = ProductCost(
                product_cost      = float(cost_row.avg_product_cost or 0),
                freight_inbound   = float(cost_row.avg_inbound or 0),
                freight_outbound  = float(cost_row.avg_outbound or 0),
                affiliate_rate    = float(cost_row.avg_affiliate or 0),
                platform_fee_rate = float(cost_row.avg_platform or 5),
                return_rate       = float(cost_row.avg_return or 0),
                damage_rate       = float(cost_row.avg_damage or 0),
            )
            profit_data = pc.calc_profit(
                gmv        = gmv_est,
                units_sold = int(row.orders),
                ad_spend   = float(row.ad_spend or 0),
            )
            entry.update({
                "gmv_estimated":  profit_data["gmv"],
                "net_gmv":        profit_data["net_gmv"],
                "real_profit":    profit_data["real_profit"],
                "real_margin":    profit_data["real_margin"],
                "real_roas":      profit_data["real_roas"],
                "break_even_roas": profit_data["break_even_roas"],
                "is_profitable":  profit_data["is_profitable"],
                "cost_breakdown": {
                    "goods_cost":     profit_data["goods_cost"],
                    "inbound_cost":   profit_data["inbound_cost"],
                    "outbound_cost":  profit_data["outbound_cost"],
                    "affiliate_cost": profit_data["affiliate_cost"],
                    "platform_cost":  profit_data["platform_cost"],
                },
            })

        report.append(entry)

    report.sort(key=lambda x: x["stat_date"], reverse=True)
    return {"days": days, "total": len(report), "data": report}


@router.get("/profit-by-product")
async def profit_by_product(
    advertiser_id: Optional[str] = None,
    days: int = 7,
    db: AsyncSession = Depends(get_db),
):
    """
    按品维度聚合利润报表

    逻辑：
    1. 从 metrics_snapshots 按 product_id 聚合（GMVMAX_ITEM 有 product_id）
    2. 关联 product_costs 表的成本配置
    3. 计算每个商品的真实利润、ROI、保本 ROAS

    用途：
    - 找出哪些品是亏钱的（is_profitable=False）
    - 找出哪些品 ROAS 高（值得加大投入）
    - 品维度的成本结构分析
    """
    since = date.today() - timedelta(days=days)

    # 按 product_id 聚合 metrics
    metrics_q = (
        select(
            MetricsSnapshot.advertiser_id,
            MetricsSnapshot.product_id,
            func.sum(MetricsSnapshot.spend).label("ad_spend"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
            func.sum(MetricsSnapshot.impressions).label("impressions"),
            func.sum(MetricsSnapshot.clicks).label("clicks"),
        )
        .where(
            MetricsSnapshot.stat_date >= since,
            MetricsSnapshot.product_id.isnot(None),
            MetricsSnapshot.data_level.in_(["AD", "GMVMAX_ITEM", "GMVMAX_CAMPAIGN"]),
        )
        .group_by(MetricsSnapshot.advertiser_id, MetricsSnapshot.product_id)
        .having(func.sum(MetricsSnapshot.spend) > 0)
    )
    if advertiser_id:
        metrics_q = metrics_q.where(MetricsSnapshot.advertiser_id == advertiser_id)

    metrics_result = await db.execute(metrics_q)
    metrics_rows = metrics_result.all()

    # 拉取成本配置（按 product_id 匹配，不绑定账户）
    cost_q = select(ProductCost).where(ProductCost.is_active == True)
    cost_result = await db.execute(cost_q)
    cost_map = {c.product_id: c for c in cost_result.scalars().all()}

    report = []
    for row in metrics_rows:
        pc = cost_map.get(row.product_id)
        ad_spend = float(row.ad_spend or 0)
        orders = int(row.orders or 0)
        gmv = float(row.gmv or 0)

        entry = {
            "advertiser_id": row.advertiser_id,
            "product_id": row.product_id,
            "product_name": pc.product_name if pc else None,
            "ad_spend": round(ad_spend, 2),
            "orders": orders,
            "gmv": round(gmv, 2),
            "impressions": int(row.impressions or 0),
            "clicks": int(row.clicks or 0),
            "has_cost_config": pc is not None,
        }

        if pc and orders > 0 and gmv > 0:
            profit_data = pc.calc_profit(gmv=gmv, units_sold=orders, ad_spend=ad_spend)
            entry.update({
                "real_profit": profit_data["real_profit"],
                "real_margin": profit_data["real_margin"],
                "real_roas": profit_data["real_roas"],
                "break_even_roas": profit_data["break_even_roas"],
                "is_profitable": profit_data["is_profitable"],
            })
        else:
            # 没有成本配置，只给简单 ROAS
            entry.update({
                "real_profit": None,
                "real_margin": None,
                "real_roas": round(gmv / ad_spend, 2) if ad_spend > 0 else None,
                "break_even_roas": None,
                "is_profitable": None,
            })

        report.append(entry)

    # 按花费降序排列
    report.sort(key=lambda x: x["ad_spend"], reverse=True)
    return {"days": days, "total": len(report), "products": report}


@router.get("/profit-by-shop")
async def profit_by_shop(
    advertiser_id: Optional[str] = None,
    days: int = 7,
    db: AsyncSession = Depends(get_db),
):
    """
    按店铺维度聚合利润报表

    逻辑：
    1. 从 metrics_snapshots 按 shop_id（GMVMax 数据中有此字段）聚合
    2. 关联成本配置（按账户均值估算）
    3. 计算每个店铺的整体利润情况

    用途：
    - 多店铺账户管理时，看哪个店铺盈利最好
    - 店铺级别的 ROI 和利润趋势
    """
    since = date.today() - timedelta(days=days)

    # 先查 metrics_snapshots 看有没有 shop_id 字段
    # GMVMax 数据中 shop_id 通过 join 或字段存储
    # 当前方案：按 advertiser_id 汇总（一个 advertiser 对应一个店铺的 token）
    # 再根据 shop_summary 的逻辑按店铺划分

    metrics_q = (
        select(
            MetricsSnapshot.advertiser_id,
            func.sum(MetricsSnapshot.spend).label("ad_spend"),
            func.sum(MetricsSnapshot.conversion).label("orders"),
            func.sum(MetricsSnapshot.gross_revenue).label("gmv"),
            func.sum(MetricsSnapshot.impressions).label("impressions"),
            func.count(MetricsSnapshot.object_id.distinct()).label("active_ads"),
        )
        .where(
            MetricsSnapshot.stat_date >= since,
            MetricsSnapshot.data_level.in_(["AD", "GMVMAX_CAMPAIGN"]),
        )
        .group_by(MetricsSnapshot.advertiser_id)
        .having(func.sum(MetricsSnapshot.spend) > 0)
    )
    if advertiser_id:
        metrics_q = metrics_q.where(MetricsSnapshot.advertiser_id == advertiser_id)

    metrics_result = await db.execute(metrics_q)
    metrics_rows = metrics_result.all()

    # 拉取全局成本均值（商品不再绑定账户）
    cost_q = select(
        func.avg(ProductCost.product_cost).label("avg_cost"),
        func.avg(ProductCost.freight_inbound).label("avg_inbound"),
        func.avg(ProductCost.freight_outbound).label("avg_outbound"),
        func.avg(ProductCost.affiliate_rate).label("avg_affiliate"),
        func.avg(ProductCost.platform_fee_rate).label("avg_platform"),
        func.avg(ProductCost.return_rate).label("avg_return"),
        func.avg(ProductCost.damage_rate).label("avg_damage"),
        func.avg(ProductCost.selling_price).label("avg_price"),
        func.count().label("product_count"),
    ).where(ProductCost.is_active == True)
    cost_result = await db.execute(cost_q)
    global_cost_row = cost_result.first()

    # 拉取账户名（作为店铺名使用）
    from app.models.advertiser import Advertiser
    adv_q = select(Advertiser.advertiser_id, Advertiser.advertiser_name)
    adv_result = await db.execute(adv_q)
    adv_map = {r.advertiser_id: r.advertiser_name for r in adv_result.all()}

    report = []
    for row in metrics_rows:
        adv_id = row.advertiser_id
        cost_row = global_cost_row
        ad_spend = float(row.ad_spend or 0)
        orders = int(row.orders or 0)
        gmv = float(row.gmv or 0)

        entry = {
            "advertiser_id": adv_id,
            "shop_name": adv_map.get(adv_id, adv_id),
            "ad_spend": round(ad_spend, 2),
            "orders": orders,
            "gmv": round(gmv, 2),
            "impressions": int(row.impressions or 0),
            "active_ads": int(row.active_ads or 0),
            "has_cost_config": cost_row is not None and cost_row.avg_cost is not None,
            "product_count": int(cost_row.product_count) if cost_row and cost_row.product_count else 0,
        }

        if cost_row and cost_row.avg_cost is not None and orders > 0 and gmv > 0:
            pc = ProductCost(
                product_cost=float(cost_row.avg_cost or 0),
                freight_inbound=float(cost_row.avg_inbound or 0),
                freight_outbound=float(cost_row.avg_outbound or 0),
                affiliate_rate=float(cost_row.avg_affiliate or 0),
                platform_fee_rate=float(cost_row.avg_platform or 5),
                return_rate=float(cost_row.avg_return or 0),
                damage_rate=float(cost_row.avg_damage or 0),
            )
            profit_data = pc.calc_profit(gmv=gmv, units_sold=orders, ad_spend=ad_spend)
            entry.update({
                "real_profit": profit_data["real_profit"],
                "real_margin": profit_data["real_margin"],
                "real_roas": profit_data["real_roas"],
                "break_even_roas": profit_data["break_even_roas"],
                "is_profitable": profit_data["is_profitable"],
            })
        else:
            entry.update({
                "real_profit": None,
                "real_margin": None,
                "real_roas": round(gmv / ad_spend, 2) if ad_spend > 0 else None,
                "break_even_roas": None,
                "is_profitable": None,
            })

        report.append(entry)

    report.sort(key=lambda x: x["ad_spend"], reverse=True)
    return {"days": days, "total": len(report), "shops": report}


def _fmt(c: ProductCost) -> dict:
    return {
        "id":               c.id,
        "advertiser_id":    c.advertiser_id,
        "product_id":       c.product_id,
        "sku_id":           c.sku_id,
        "product_name":     c.product_name,
        "currency":         c.currency,
        "product_cost":     c.product_cost,
        "freight_inbound":  c.freight_inbound,
        "freight_outbound": c.freight_outbound,
        "affiliate_rate":   c.affiliate_rate,
        "platform_fee_rate":c.platform_fee_rate,
        "return_rate":      c.return_rate,
        "damage_rate":      c.damage_rate,
        "selling_price":    c.selling_price,
        "total_fixed_cost": c.total_cost_per_unit(),
        "notes":            c.notes,
        "updated_at":       c.updated_at,
    }
