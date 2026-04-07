"""
商品发现服务

从 GMVMAX_ITEM 指标快照中提取 item_group_id（商品组 ID），
再通过 TikTok Shop API 获取商品详情（名称、图片、价格等），
返回未配置成本的商品列表供前端配置。

逻辑：
1. 查询 GMVMAX_ITEM 层的 metrics_snapshots，按 object_id (= item_group_id) 聚合
2. 排除已有 ProductCost 配置的商品
3. 调用 store/product/get 获取商品名称、图片、价格
4. 返回 pending 列表
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sqlfunc

from app.models.advertiser import Advertiser
from app.models.product import ProductCost
from app.models.metrics import MetricsSnapshot
from app.services.tiktok_client import TikTokClient, TikTokAPIError

logger = logging.getLogger(__name__)


class ProductDiscoveryService:
    """发现和采集商品（基于 GMVMAX_ITEM 数据）"""

    async def _fetch_store_product_map(
        self,
        advertiser_id: str,
        access_token: str,
        bc_id: Optional[str] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        从 TikTok Shop API 获取商品详情，建立 item_group_id -> product_info 的映射

        Returns:
            {"item_group_id": {"title": "...", "image_url": "...", "min_price": "...", ...}}
        """
        client = TikTokClient(access_token=access_token, advertiser_id=advertiser_id)
        product_map: Dict[str, Dict[str, Any]] = {}

        try:
            # 获取关联店铺
            stores = await client.get_gmvmax_store_list()
            if not stores:
                logger.debug(f"[ProductDiscovery] No stores for {advertiser_id}")
                return product_map

            for store in stores:
                store_id = str(
                    store.get("store_id") or store.get("shop_id") or store.get("id") or ""
                )
                if not store_id:
                    continue

                # bc_id 可能来自 store 信息，也可能需要外部传入
                effective_bc_id = bc_id or store.get("bc_id") or store.get("store_authorized_bc_id", "")
                if not effective_bc_id:
                    logger.warning(
                        f"[ProductDiscovery] No bc_id for store {store_id}, "
                        "cannot fetch product details"
                    )
                    continue

                try:
                    products = await client.get_all_store_products(
                        store_id=store_id,
                        bc_id=effective_bc_id,
                    )
                    for p in products:
                        igid = p.get("item_group_id", "")
                        if igid:
                            product_map[igid] = {
                                "title": p.get("title", ""),
                                "image_url": p.get("product_image_url", ""),
                                "min_price": p.get("min_price"),
                                "max_price": p.get("max_price"),
                                "currency": p.get("currency", ""),
                                "category": p.get("category", ""),
                                "status": p.get("status", ""),
                                "store_id": store_id,
                            }
                    logger.info(
                        f"[ProductDiscovery] Fetched {len(products)} products "
                        f"from store {store_id}"
                    )
                except TikTokAPIError as e:
                    logger.warning(
                        f"[ProductDiscovery] Failed to fetch products from store "
                        f"{store_id}: [{e.code}] {e.message}"
                    )
                except Exception as e:
                    logger.warning(
                        f"[ProductDiscovery] Error fetching products from store "
                        f"{store_id}: {e}"
                    )

        except Exception as e:
            logger.error(f"[ProductDiscovery] Store product fetch error: {e}", exc_info=True)
        finally:
            await client.close()

        return product_map

    async def discover_products_for_advertiser(
        self,
        advertiser_id: str,
        db: AsyncSession,
        limit_days: int = 30,
        bc_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        为某账户发现商品
        从最近 N 天的 GMVMAX_ITEM 数据中提取 item_group_id，去重后获取花费统计

        Returns:
            {
                "advertiser_id": "...",
                "discovered_count": 5,
                "configured_count": 2,
                "pending_count": 3,
                "pending": [
                    {
                        "product_id": "item_group_id",
                        "product_name": "商品名",
                        "image_url": "...",
                        "selling_price": "10.50",
                        "currency": "SGD",
                        "category": "...",
                        "total_spend": 100.5,
                        "total_orders": 5,
                        "total_revenue": 200.0,
                        "days_active": 10,
                        "first_seen_date": "2026-03-25",
                        "status": "PENDING_CONFIG"
                    }
                ]
            }
        """

        logger.info(f"[ProductDiscovery] Starting for advertiser {advertiser_id}")

        try:
            # 1. 查询 GMVMAX_ITEM 层数据，按 object_id (= item_group_id) 聚合
            since = datetime.utcnow().date() - timedelta(days=limit_days)

            metrics_q = (
                select(
                    MetricsSnapshot.object_id,
                    sqlfunc.sum(MetricsSnapshot.spend).label("total_spend"),
                    sqlfunc.sum(MetricsSnapshot.conversion).label("total_orders"),
                    sqlfunc.sum(MetricsSnapshot.gross_revenue).label("total_revenue"),
                    sqlfunc.min(MetricsSnapshot.stat_date).label("first_seen_date"),
                    sqlfunc.max(MetricsSnapshot.stat_date).label("last_seen_date"),
                )
                .where(
                    MetricsSnapshot.advertiser_id == advertiser_id,
                    MetricsSnapshot.stat_date >= since,
                    MetricsSnapshot.data_level == "GMVMAX_ITEM",
                    MetricsSnapshot.object_id.isnot(None),
                    MetricsSnapshot.object_id != "",
                )
                .group_by(MetricsSnapshot.object_id)
                .order_by(sqlfunc.sum(MetricsSnapshot.spend).desc())
            )

            result = await db.execute(metrics_q)
            rows = result.all()

            logger.info(
                f"[ProductDiscovery] Found {len(rows)} item_group_ids "
                f"for {advertiser_id}"
            )

            # 2. 查询已配置过的商品（product_id = item_group_id）
            configured_q = select(ProductCost.product_id).where(
                ProductCost.advertiser_id == advertiser_id,
                ProductCost.is_active == True,
            )
            configured_result = await db.execute(configured_q)
            configured_ids = {row[0] for row in configured_result.all()}

            logger.info(f"[ProductDiscovery] {len(configured_ids)} already configured")

            # 3. 尝试从 TikTok Shop API 获取商品详情
            product_map: Dict[str, Dict[str, Any]] = {}
            adv_result = await db.execute(
                select(Advertiser).where(
                    Advertiser.advertiser_id == advertiser_id
                )
            )
            adv = adv_result.scalar_one_or_none()
            if adv and adv.access_token:
                product_map = await self._fetch_store_product_map(
                    advertiser_id=advertiser_id,
                    access_token=adv.access_token,
                    bc_id=bc_id,
                )
                logger.info(
                    f"[ProductDiscovery] Product map has {len(product_map)} entries"
                )

            # 4. 构建 pending 列表（未配置的商品）
            pending_products = []
            for row in rows:
                item_group_id = row.object_id
                if item_group_id in configured_ids:
                    continue

                first_date = row.first_seen_date
                last_date = row.last_seen_date
                days_active = (
                    (last_date - first_date).days + 1
                    if first_date and last_date
                    else 1
                )

                # 从商品信息映射补充详情
                product_info = product_map.get(item_group_id, {})

                pending_products.append(
                    {
                        "product_id": item_group_id,
                        "product_name": (
                            product_info.get("title")
                            or f"Product {item_group_id[:8]}..."
                        ),
                        "image_url": product_info.get("image_url"),
                        "selling_price": product_info.get("min_price"),
                        "max_price": product_info.get("max_price"),
                        "currency": product_info.get("currency"),
                        "category": product_info.get("category"),
                        "store_id": product_info.get("store_id"),
                        "shop_status": product_info.get("status"),
                        "total_spend": round(float(row.total_spend or 0), 2),
                        "total_orders": int(row.total_orders or 0),
                        "total_revenue": round(float(row.total_revenue or 0), 2),
                        "days_active": days_active,
                        "first_seen_date": (
                            first_date.isoformat() if first_date else None
                        ),
                        "status": "PENDING_CONFIG",
                    }
                )

            return {
                "advertiser_id": advertiser_id,
                "discovered_count": len(rows),
                "configured_count": len(configured_ids),
                "pending_count": len(pending_products),
                "pending": pending_products,
            }

        except Exception as e:
            logger.error(
                f"[ProductDiscovery] Error for {advertiser_id}: {e}", exc_info=True
            )
            return {
                "advertiser_id": advertiser_id,
                "error": str(e),
                "discovered_count": 0,
                "configured_count": 0,
                "pending_count": 0,
                "pending": [],
            }

    async def discover_all_advertisers(
        self,
        db: AsyncSession,
        limit_days: int = 30,
        bc_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """为所有账户发现商品"""

        advertiser_q = select(Advertiser.advertiser_id).where(
            Advertiser.is_active == True
        )
        result = await db.execute(advertiser_q)
        advertiser_ids = [row[0] for row in result.all()]

        results = []
        for adv_id in advertiser_ids:
            discovery = await self.discover_products_for_advertiser(
                adv_id, db, limit_days, bc_id=bc_id,
            )
            results.append(discovery)

        return results
