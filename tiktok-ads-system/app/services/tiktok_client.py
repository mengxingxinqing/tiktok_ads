"""
TikTok Business API 客户端
基于官方 SDK (tiktok-business-api-sdk) 封装的异步客户端
- 底层使用官方 SDK 的 API 类
- 通过 asyncio.to_thread 将同步调用转为异步
- 保留 rate limit 控制（asyncio Semaphore + 滑动窗口）
- 自动重试（指数退避）
"""
import asyncio
import json
import time
from typing import Optional, Dict, Any, List

from loguru import logger

from business_api_client import ApiClient, Configuration
from business_api_client.api import (
    AuthenticationApi,
    CampaignCreationApi,
    AdApi,
    AdgroupApi,
    ReportingApi,
    FileApi,
    VideoApi,
    StoreApi,
    IdentityApi,
)
from business_api_client.rest import ApiException

from app.core.config import settings


# ===================== Rate Limiter =====================

class RateLimiter:
    """滑动窗口限速器"""

    def __init__(self, max_calls: int, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self._calls: List[float] = []
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            self._calls = [t for t in self._calls if now - t < self.period]
            if len(self._calls) >= self.max_calls:
                sleep_time = self.period - (now - self._calls[0])
                if sleep_time > 0:
                    logger.debug(f"Rate limit: sleeping {sleep_time:.2f}s")
                    await asyncio.sleep(sleep_time)
                self._calls = self._calls[1:]
            self._calls.append(time.monotonic())


# 全局限速器 & 并发控制
_rate_limiter = RateLimiter(max_calls=settings.TIKTOK_RATE_LIMIT_PER_MIN, period=60.0)
_semaphore = asyncio.Semaphore(settings.TIKTOK_MAX_CONCURRENT)

# 全局 SDK ApiClient（复用连接池，配置超时）
_sdk_config = Configuration()
_sdk_config.host = settings.TIKTOK_API_BASE
_sdk_api_client = ApiClient(configuration=_sdk_config)
# SDK 内部 urllib3 默认无超时且重试 3 次，配置合理值
_sdk_api_client.rest_client.pool_manager.connection_pool_kw["timeout"] = 15
_sdk_api_client.rest_client.pool_manager.connection_pool_kw["retries"] = 1


# ===================== Exceptions =====================

class TikTokAPIError(Exception):
    def __init__(self, code: int, message: str, request_id: str = ""):
        self.code = code
        self.message = message
        self.request_id = request_id
        super().__init__(f"[{code}] {message} (request_id={request_id})")


# ===================== Client =====================

class TikTokClient:
    """
    TikTok Marketing API 异步客户端
    底层使用官方 SDK，通过 asyncio.to_thread 实现异步
    每个 advertiser 用自己的 access_token 实例化
    """

    def __init__(self, access_token: str, advertiser_id: str):
        self.access_token = access_token
        self.advertiser_id = advertiser_id

        # SDK API 实例（共享全局 ApiClient）
        self._campaign_api = CampaignCreationApi(api_client=_sdk_api_client)
        self._ad_api = AdApi(api_client=_sdk_api_client)
        self._adgroup_api = AdgroupApi(api_client=_sdk_api_client)
        self._reporting_api = ReportingApi(api_client=_sdk_api_client)
        self._file_api = FileApi(api_client=_sdk_api_client)
        self._video_api = VideoApi(api_client=_sdk_api_client)
        self._store_api = StoreApi(api_client=_sdk_api_client)
        self._identity_api = IdentityApi(api_client=_sdk_api_client)

    async def _call_sdk(self, sdk_method, *args, retry: int = 3, **kwargs) -> Dict[str, Any]:
        """
        通用 SDK 调用包装：
        1. 注入 access_token
        2. rate limit + semaphore
        3. 重试（指数退避）
        4. 解析 JSON 返回 data dict
        """
        kwargs["access_token"] = self.access_token

        method_name = getattr(sdk_method, "__name__", str(sdk_method))

        for attempt in range(retry):
            async with _semaphore:
                await _rate_limiter.acquire()
                try:
                    # SDK 默认 _preload_content=True 返回 InlineResponse200 对象
                    resp = await asyncio.to_thread(sdk_method, *args, **kwargs)

                    # SDK 成功时（code=0）直接返回 data 层的 dict
                    # SDK 失败时抛 ApiException
                    # 所以 resp 通常已经是 data 内容
                    if isinstance(resp, dict):
                        # SDK 有两种返回格式：
                        # 1. 直接返回 data 层内容（大多数端点）
                        # 2. 返回完整 {code, data, message} 结构
                        if "code" in resp and "data" in resp:
                            code = resp.get("code", 0)
                            if code != 0:
                                raise TikTokAPIError(code, resp.get("message", ""), resp.get("request_id", ""))
                            return resp.get("data", {})
                        return resp
                    elif hasattr(resp, "to_dict"):
                        d = resp.to_dict()
                        if "code" in d and "data" in d:
                            code = d.get("code", 0)
                            if code != 0:
                                raise TikTokAPIError(code, d.get("message", ""), d.get("request_id", ""))
                            return d.get("data", {})
                        return d
                    elif hasattr(resp, "data") and isinstance(resp.data, bytes):
                        data = json.loads(resp.data.decode("utf-8"))
                        code = data.get("code", 0)
                        if code != 0:
                            raise TikTokAPIError(code, data.get("message", ""), data.get("request_id", ""))
                        return data.get("data", {})
                    else:
                        return {}

                except ApiException as e:
                    if e.status == 429:
                        wait = 2 ** attempt
                        logger.warning(f"Rate limited on {method_name}, retry in {wait}s")
                        await asyncio.sleep(wait)
                        continue
                    raise TikTokAPIError(e.status, str(e.body)[:200], "")

                except TikTokAPIError:
                    raise

                except Exception as e:
                    wait = 2 ** attempt
                    logger.warning(f"Error on {method_name} (attempt {attempt+1}): {e}, retry in {wait}s")
                    if attempt == retry - 1:
                        raise TikTokAPIError(-1, f"{method_name} failed: {e}")
                    await asyncio.sleep(wait)

        raise TikTokAPIError(-1, f"Max retries exceeded for {method_name}")

    async def _request(
        self, method: str, path: str,
        params: Optional[Dict] = None, json_body: Optional[Dict] = None,
        retry: int = 3,
    ) -> Dict[str, Any]:
        """直接 HTTP 请求（用于 SDK 未覆盖的端点，如 store/product/get）"""
        import httpx
        url = f"{settings.TIKTOK_API_BASE}{path}"
        headers = {"Access-Token": self.access_token, "Content-Type": "application/json"}

        for attempt in range(retry):
            async with _semaphore:
                await _rate_limiter.acquire()
                try:
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        resp = await client.request(method, url, headers=headers, params=params, json=json_body)
                        data = resp.json()
                        if resp.status_code == 429:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        if resp.status_code != 200:
                            raise TikTokAPIError(resp.status_code, resp.text)
                        code = data.get("code", 0)
                        if code != 0:
                            raise TikTokAPIError(code, data.get("message", ""), data.get("request_id", ""))
                        return data.get("data", {})
                except (httpx.TimeoutException, httpx.ConnectError) as e:
                    if attempt == retry - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)
        raise TikTokAPIError(-1, f"Max retries exceeded for {path}")

    # ===================== OAuth =====================

    @staticmethod
    async def exchange_token(auth_code: str) -> Dict[str, Any]:
        """auth_code 换取 access_token"""
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{settings.TIKTOK_API_BASE}/open_api/v1.3/oauth2/access_token/",
                json={"app_id": settings.TIKTOK_APP_ID, "auth_code": auth_code, "secret": settings.TIKTOK_APP_SECRET},
            )
            data = resp.json()
            if data.get("code") != 0:
                raise TikTokAPIError(data["code"], data.get("message", ""), data.get("request_id", ""))
            return data.get("data", {})

    @staticmethod
    async def refresh_token(refresh_token_value: str) -> Dict[str, Any]:
        """用 refresh_token 刷新 access_token"""
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{settings.TIKTOK_API_BASE}/open_api/v1.3/oauth2/refresh_token/",
                json={"app_id": settings.TIKTOK_APP_ID, "secret": settings.TIKTOK_APP_SECRET, "refresh_token": refresh_token_value},
            )
            data = resp.json()
            if data.get("code") != 0:
                raise TikTokAPIError(data["code"], data.get("message", ""), data.get("request_id", ""))
            return data.get("data", {})

    @staticmethod
    async def get_advertiser_list(access_token: str) -> List[Dict]:
        """获取授权的广告账户列表"""
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.TIKTOK_API_BASE}/open_api/v1.3/oauth2/advertiser/get/",
                headers={"Access-Token": access_token},
                params={"app_id": settings.TIKTOK_APP_ID, "secret": settings.TIKTOK_APP_SECRET},
            )
            data = resp.json()
            if data.get("code") != 0:
                raise TikTokAPIError(data.get("code", -1), data.get("message", ""), data.get("request_id", ""))
            return data.get("data", {}).get("list", [])

    # ===================== 账户信息 =====================

    async def get_balance(self) -> Dict:
        """获取广告账户余额 — /advertiser/balance/get/"""
        return await self._request(
            "GET",
            "/open_api/v1.3/advertiser/balance/get/",
            params={"advertiser_id": self.advertiser_id},
        )

    # ===================== Campaign =====================

    async def get_campaigns(self, page: int = 1, page_size: int = 100) -> Dict:
        return await self._call_sdk(
            self._campaign_api.campaign_get,
            advertiser_id=self.advertiser_id, page=page, page_size=page_size,
            fields=json.dumps(["campaign_id", "campaign_name", "operation_status", "secondary_status", "budget", "budget_mode", "objective_type", "create_time"]),
        )

    async def create_campaign(self, campaign_name: str, objective_type: str, budget: float, budget_mode: str = "DAILY") -> Dict:
        return await self._call_sdk(self._campaign_api.campaign_create, body={
            "advertiser_id": self.advertiser_id, "campaign_name": campaign_name,
            "objective_type": objective_type, "budget": budget, "budget_mode": budget_mode,
        })

    async def update_campaign_budget(self, campaign_id: str, budget: float) -> Dict:
        return await self._call_sdk(self._campaign_api.campaign_update, body={
            "advertiser_id": self.advertiser_id, "campaign_id": campaign_id, "budget": budget,
        })

    async def update_campaign_status(self, campaign_ids: List[str], operation_status: str) -> Dict:
        return await self._call_sdk(self._campaign_api.campaign_status_update, body={
            "advertiser_id": self.advertiser_id, "campaign_ids": campaign_ids, "operation_status": operation_status,
        })

    # ===================== AdGroup =====================

    async def get_adgroups(self, campaign_ids: Optional[List[str]] = None, page: int = 1, page_size: int = 100) -> Dict:
        kw = {"advertiser_id": self.advertiser_id, "page": page, "page_size": page_size}
        if campaign_ids:
            kw["filtering"] = json.dumps({"campaign_ids": campaign_ids})
        return await self._call_sdk(self._adgroup_api.adgroup_get, **kw)

    async def create_adgroup(self, campaign_id: str, adgroup_name: str, **extra) -> Dict:
        body = {"advertiser_id": self.advertiser_id, "campaign_id": campaign_id, "adgroup_name": adgroup_name, **extra}
        return await self._call_sdk(self._adgroup_api.adgroup_create, body=body)

    async def update_adgroup_status(self, adgroup_ids: List[str], operation_status: str) -> Dict:
        return await self._call_sdk(self._adgroup_api.adgroup_status_update, body={
            "advertiser_id": self.advertiser_id, "adgroup_ids": adgroup_ids, "operation_status": operation_status,
        })

    async def update_adgroup_budget(self, adgroup_id: str, budget: float) -> Dict:
        return await self._call_sdk(self._adgroup_api.adgroup_update, body={
            "advertiser_id": self.advertiser_id, "adgroup_id": adgroup_id, "budget": budget,
        })

    # ===================== Ad =====================

    async def get_ads(self, adgroup_ids: Optional[List[str]] = None, page: int = 1, page_size: int = 100) -> Dict:
        kw = {"advertiser_id": self.advertiser_id, "page": page, "page_size": page_size}
        if adgroup_ids:
            kw["filtering"] = json.dumps({"adgroup_ids": adgroup_ids})
        return await self._call_sdk(self._ad_api.ad_get, **kw)

    async def get_ad_detail(self, ad_ids: List[str]) -> Dict:
        return await self._call_sdk(
            self._ad_api.ad_get, advertiser_id=self.advertiser_id,
            filtering=json.dumps({"ad_ids": ad_ids}),
            fields=json.dumps(["ad_id", "ad_name", "adgroup_id", "campaign_id", "video_id", "image_ids", "ad_format", "item_group_ids", "sku_ids", "product_info", "operation_status", "create_time"]),
            page_size=len(ad_ids),
        )

    async def get_ads_batch(self, ad_ids: List[str]) -> Dict:
        return await self.get_ad_detail(ad_ids)

    async def create_ad(self, adgroup_id: str, ad_name: str, **extra) -> Dict:
        body = {"advertiser_id": self.advertiser_id, "adgroup_id": adgroup_id, "ad_name": ad_name, **extra}
        return await self._call_sdk(self._ad_api.ad_create, body=body)

    async def create_ad_spark(self, adgroup_id: str, creatives: List[Dict]) -> Dict:
        """Spark Ads 风格的 /ad/create/：只接 creatives 数组。"""
        return await self._request(
            "POST",
            "/open_api/v1.3/ad/create/",
            json_body={
                "advertiser_id": self.advertiser_id,
                "adgroup_id": adgroup_id,
                "creatives": creatives,
            },
        )

    async def update_ad_status(self, ad_ids: List[str], operation_status: str) -> Dict:
        return await self._call_sdk(self._ad_api.ad_status_update, body={
            "advertiser_id": self.advertiser_id, "ad_ids": ad_ids, "operation_status": operation_status,
        })

    # ===================== Reporting =====================
    # 注意: 报表接口需要 JSON 数组作为 query param（如 dimensions=["a","b"]），
    # 但 SDK 用 multi 格式序列化（dimensions=a&dimensions=b），导致 API 报错。
    # 因此报表类接口全部用 _request() 直接调用。

    async def get_report(
        self, data_level: str, start_date: str, end_date: str,
        dimensions: Optional[List[str]] = None, metrics: Optional[List[str]] = None,
        page: int = 1, page_size: int = 1000, **extra,
    ) -> Dict:
        if dimensions is None:
            dimensions = {"AUCTION_CAMPAIGN": ["campaign_id", "stat_time_day"], "AUCTION_ADGROUP": ["adgroup_id", "stat_time_day"],
                          "AUCTION_AD": ["ad_id", "stat_time_day"], "ORDER": ["order_id", "product_id", "stat_time_day"]}.get(data_level, ["ad_id", "stat_time_day"])
        if metrics is None:
            metrics = ["spend", "impressions", "clicks", "ctr", "cpm", "cpc", "conversion", "cost_per_conversion", "conversion_rate",
                       "video_play_actions", "video_watched_2s", "video_watched_6s", "average_video_play"]

        return await self._request("GET", "/open_api/v1.3/report/integrated/get/", params={
            "advertiser_id": self.advertiser_id, "report_type": "BASIC", "data_level": data_level,
            "dimensions": json.dumps(dimensions), "metrics": json.dumps(metrics),
            "start_date": start_date, "end_date": end_date, "page": page, "page_size": page_size,
        })

    async def get_order_report(self, start_date: str, end_date: str, include_affiliate: bool = True, **kw) -> Dict:
        dims = ["order_id", "product_id", "campaign_id", "shop_id", "stat_time_day"]
        if include_affiliate:
            dims.append("order_source")
        mets = ["order_id", "order_amount", "order_status", "payment_status", "product_id", "product_name", "quantity", "unit_price",
                "shop_id", "shop_name", "order_source", "affiliate_id", "affiliate_name", "commission_rate", "commission_amount"]
        return await self.get_report("ORDER", start_date, end_date, dimensions=dims, metrics=mets, **kw)

    # ===================== Spark Ads / TT Video Authorize =====================

    async def tt_video_authorize(self, auth_code: str) -> Dict:
        """
        绑定创作者授权的 TikTok 帖子到本广告户。
        POST /open_api/v1.3/tt_video/authorize/
        """
        return await self._request(
            "POST",
            "/open_api/v1.3/tt_video/authorize/",
            json_body={"advertiser_id": self.advertiser_id, "auth_code": auth_code},
        )

    async def tt_video_list(self, page: int = 1, page_size: int = 20) -> Dict:
        """
        查询已授权到本广告户的帖子，返回 identity_id + item_id。
        GET /open_api/v1.3/tt_video/list/
        """
        return await self._request(
            "GET",
            "/open_api/v1.3/tt_video/list/",
            params={"advertiser_id": self.advertiser_id, "page": page, "page_size": page_size},
        )

    async def tt_video_info(self, auth_code: str) -> Dict:
        """按 auth_code 查单条已授权帖子。"""
        return await self._request(
            "GET",
            "/open_api/v1.3/tt_video/info/",
            params={"advertiser_id": self.advertiser_id, "auth_code": auth_code},
        )

    # ===================== File / Video =====================

    async def get_video_info(self, video_ids: List[str]) -> List[Dict]:
        """搜索视频素材库（SDK 的 filtering 参数用 multi 格式会拆散，用 _request）"""
        data = await self._request("GET", "/open_api/v1.3/file/video/ad/search/", params={
            "advertiser_id": self.advertiser_id,
            "filtering": json.dumps({"video_ids": video_ids}),
            "page_size": len(video_ids),
        })
        return data.get("list", [])

    async def upload_video(self, file_path: str, video_name: str) -> Dict:
        import httpx
        with open(file_path, 'rb') as f:
            async with httpx.AsyncClient(timeout=300.0) as client:
                resp = await client.post(
                    f"{settings.TIKTOK_API_BASE}/open_api/v1.3/file/video/ad/upload/",
                    headers={"Access-Token": self.access_token},
                    data={"advertiser_id": self.advertiser_id, "upload_type": "UPLOAD_BY_FILE"},
                    files={"video_file": (video_name, f, "video/mp4")},
                )
                data = resp.json()
                if data.get("code") != 0:
                    raise TikTokAPIError(data["code"], data.get("message", ""), data.get("request_id", ""))
                return data.get("data", {})

    async def upload_image(self, file_path: str, image_name: str) -> Dict:
        import httpx
        with open(file_path, 'rb') as f:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{settings.TIKTOK_API_BASE}/open_api/v1.3/file/image/ad/upload/",
                    headers={"Access-Token": self.access_token},
                    data={"advertiser_id": self.advertiser_id, "upload_type": "UPLOAD_BY_FILE"},
                    files={"image_file": (image_name, f, "image/jpeg")},
                )
                data = resp.json()
                if data.get("code") != 0:
                    raise TikTokAPIError(data["code"], data.get("message", ""), data.get("request_id", ""))
                return data.get("data", {})

    # ===================== GMVMax Store =====================

    async def get_gmvmax_store_list(self) -> List[Dict]:
        """获取 GMVMax 关联的店铺列表"""
        data = await self._request("GET", "/open_api/v1.3/store/list/", params={
            "advertiser_id": self.advertiser_id,
            "page": 1,
            "page_size": 50,
        })
        return data.get("stores", []) or data.get("list", [])

    async def get_store_products(self, store_id: str, bc_id: str, page: int = 1, page_size: int = 50) -> Dict:
        return await self._request("GET", "/open_api/v1.3/store/product/get/", params={
            "bc_id": bc_id, "advertiser_id": self.advertiser_id, "store_id": store_id, "page": page, "page_size": page_size,
        })

    async def get_all_store_products(self, store_id: str, bc_id: str) -> List[Dict]:
        all_products, page = [], 1
        while True:
            data = await self.get_store_products(store_id, bc_id, page, 50)
            products = data.get("store_products", [])
            if not products:
                break
            all_products.extend(products)
            if page >= data.get("page_info", {}).get("total_page", 1):
                break
            page += 1
        return all_products

    # ===================== GMVMax Campaign =====================

    async def get_gmvmax_campaign_info(self, campaign_ids: Optional[List[str]] = None) -> Dict:
        if campaign_ids and len(campaign_ids) == 1:
            return await self._call_sdk(self._campaign_api.campaign_gmv_max_info, advertiser_id=self.advertiser_id, campaign_id=campaign_ids[0])
        results = []
        for cid in (campaign_ids or []):
            try:
                r = await self._call_sdk(self._campaign_api.campaign_gmv_max_info, advertiser_id=self.advertiser_id, campaign_id=cid)
                results.append(r)
            except TikTokAPIError:
                continue
        return {"list": results}

    async def create_gmvmax_campaign(self, **body) -> Dict:
        body.setdefault("advertiser_id", self.advertiser_id)
        return await self._call_sdk(self._campaign_api.campaign_gmv_max_create, body=body)

    async def update_gmvmax_campaign(self, **body) -> Dict:
        body.setdefault("advertiser_id", self.advertiser_id)
        return await self._call_sdk(self._campaign_api.campaign_gmv_max_update, body=body)

    async def exclude_gmvmax_creative(
        self,
        campaign_id: str,
        exclude_item_id: str,
        store_id: str,
        store_authorized_bc_id: str,
    ) -> Dict:
        """
        从 GMVMax Campaign 中排除指定创意

        流程：
        1. 获取当前 campaign 的所有创意列表（通过 /gmv_max/video/get/）
        2. 从列表中移除目标 item_id
        3. 调 campaign/gmv_max/update 提交新的 item_list
        """
        # 1. 获取达人身份
        identities = await self.get_gmvmax_identities(store_id, store_authorized_bc_id)

        # 2. 获取所有创意
        all_items = []
        for identity in (identities or [None]):
            kwargs = {}
            if identity:
                kwargs["identity_list"] = [{
                    "identity_id": str(identity.get("identity_id", "")),
                    "identity_type": str(identity.get("identity_type", "")),
                    "store_id": store_id,
                }]
            items = await self.get_all_gmvmax_videos(store_id, store_authorized_bc_id, **kwargs)
            all_items.extend(items)

        # 3. 构建新的 item_list，排除目标创意
        excluded = None
        new_item_list = []
        for item in all_items:
            iid = str(item.get("item_id", ""))
            if iid == exclude_item_id:
                excluded = item
                continue  # 跳过要排除的
            vi = item.get("video_info", {})
            ii = item.get("identity_info", {})
            new_item_list.append({
                "item_id": iid,
                "video_info": {"video_id": vi.get("video_id", "")},
                "identity_info": {
                    "identity_id": str(ii.get("identity_id", "")),
                    "identity_type": str(ii.get("identity_type", "")),
                },
                "spu_id_list": item.get("spu_id_list", []),
            })

        if not excluded:
            raise TikTokAPIError(-1, f"Creative item_id={exclude_item_id} not found in campaign {campaign_id}")

        # 4. 更新 campaign
        result = await self.update_gmvmax_campaign(
            advertiser_id=self.advertiser_id,
            campaign_id=campaign_id,
            item_list=new_item_list,
        )

        return {
            "excluded_item_id": exclude_item_id,
            "excluded_text": excluded.get("text", ""),
            "remaining_count": len(new_item_list),
            "result": result,
        }

    # ===================== GMVMax Report =====================

    async def get_gmvmax_report(
        self, store_ids: List[str], start_date: str, end_date: str,
        dimensions: Optional[List[str]] = None, metrics: Optional[List[str]] = None,
        filtering: Optional[Dict] = None, page: int = 1, page_size: int = 100,
    ) -> Dict:
        """GMVMax 报表（用 _request，SDK 的 multi 格式不兼容 JSON 数组参数）"""
        if dimensions is None:
            dimensions = ["campaign_id", "stat_time_day"]
        if metrics is None:
            metrics = ["cost", "gross_revenue", "orders", "roi", "cost_per_order", "live_views"]
        params = {
            "advertiser_id": self.advertiser_id, "store_ids": json.dumps(store_ids),
            "dimensions": json.dumps(dimensions), "metrics": json.dumps(metrics),
            "start_date": start_date, "end_date": end_date, "page": page, "page_size": page_size,
        }
        if filtering:
            params["filtering"] = json.dumps(filtering)
        return await self._request("GET", "/open_api/v1.3/gmv_max/report/get/", params=params)

    async def get_gmvmax_item_report(self, store_ids: List[str], campaign_ids: List[str], start_date: str, end_date: str, **kw) -> Dict:
        return await self.get_gmvmax_report(store_ids, start_date, end_date,
            dimensions=["item_group_id", "stat_time_day"], metrics=["cost", "gross_revenue", "orders", "roi", "cost_per_order"],
            filtering={"campaign_ids": campaign_ids}, **kw)

    async def get_gmvmax_creative_report(self, store_ids: List[str], campaign_ids: List[str], item_group_ids: List[str], start_date: str, end_date: str, **kw) -> Dict:
        return await self.get_gmvmax_report(store_ids, start_date, end_date,
            dimensions=["campaign_id", "item_id", "stat_time_day"],
            metrics=["cost", "gross_revenue", "orders", "roi", "cost_per_order", "product_impressions", "product_clicks", "product_click_rate"],
            filtering={"campaign_ids": campaign_ids, "item_group_ids": item_group_ids}, **kw)

    # ===================== GMVMax 创意/视频 =====================

    async def get_gmvmax_videos(
        self, store_id: str, store_authorized_bc_id: str,
        spu_id_list: Optional[List[str]] = None, identity_list: Optional[List[Dict]] = None,
        page: int = 1, page_size: int = 50,
        sort_field: Optional[str] = None, sort_type: str = "DESC", keyword: Optional[str] = None,
    ) -> Dict:
        """获取 GMVMax 创意视频列表（商品关联的视频）"""
        kw = {"advertiser_id": self.advertiser_id, "store_id": store_id, "store_authorized_bc_id": store_authorized_bc_id, "page": page, "page_size": page_size}
        if spu_id_list:
            kw["spu_id_list"] = spu_id_list
        if identity_list:
            kw["identity_list"] = identity_list
        if sort_field:
            kw["sort_field"] = sort_field
        if sort_type:
            kw["sort_type"] = sort_type
        if keyword:
            kw["keyword"] = keyword
        return await self._call_sdk(self._video_api.gmv_max_video_get, **kw)

    async def get_all_gmvmax_videos(self, store_id: str, store_authorized_bc_id: str, **kwargs) -> List[Dict]:
        """获取全部 GMVMax 创意视频（自动翻页）"""
        all_items, page = [], 1
        while True:
            data = await self.get_gmvmax_videos(store_id, store_authorized_bc_id, page=page, page_size=50, **kwargs)
            items = data.get("item_list", [])
            if not items:
                break
            all_items.extend(items)
            if page >= data.get("page_info", {}).get("total_page", 1):
                break
            page += 1
        return all_items

    async def get_gmvmax_identities(self, store_id: str, store_authorized_bc_id: str) -> List[Dict]:
        """获取 GMVMax 可用的达人身份列表"""
        data = await self._call_sdk(
            self._identity_api.gmv_max_identity_get,
            advertiser_id=self.advertiser_id, store_id=store_id, store_authorized_bc_id=store_authorized_bc_id,
        )
        return data.get("identity_list", [])

    # ===================== GMVMax 便捷方法 =====================

    async def get_gmvmax_adgroup_list(self, campaign_id: str) -> List[Dict]:
        data = await self.get_adgroups(campaign_ids=[campaign_id])
        return data.get("list", [])

    async def update_gmvmax_adgroup_budget(self, adgroup_id: str, budget: float) -> Dict:
        return await self.update_adgroup_budget(adgroup_id, budget)

    async def create_gmvmax_adgroup(self, campaign_id: str, adgroup_name: str, **extra) -> Dict:
        return await self.create_adgroup(campaign_id, adgroup_name, **extra)

    async def create_gmvmax_ad(self, adgroup_id: str, ad_name: str, **extra) -> Dict:
        return await self.create_ad(adgroup_id, ad_name, **extra)

    # ===================== Comments =====================

    async def get_comments(
        self,
        ad_ids: List[str],
        page: int = 1,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        """
        获取广告评论列表
        GET /open_api/v1.3/comment/list/
        """
        return await self._request("GET", "/open_api/v1.3/comment/list/", params={
            "advertiser_id": self.advertiser_id,
            "ad_ids": json.dumps(ad_ids),
            "page": page,
            "page_size": page_size,
        })

    async def get_all_comments(self, ad_ids: List[str], max_pages: int = 20) -> List[Dict]:
        """获取广告下全部评论（自动翻页）"""
        all_comments = []
        for page in range(1, max_pages + 1):
            data = await self.get_comments(ad_ids, page=page, page_size=100)
            items = data.get("comments", data.get("list", []))
            all_comments.extend(items)
            total = data.get("page_info", {}).get("total_page", 1)
            if page >= total:
                break
        return all_comments

    async def post_comment(self, ad_id: str, comment_id: str, content: str) -> Dict:
        """
        回复评论
        POST /open_api/v1.3/comment/post/
        """
        return await self._request("POST", "/open_api/v1.3/comment/post/", json_body={
            "advertiser_id": self.advertiser_id,
            "ad_id": ad_id,
            "comment_id": comment_id,
            "content": content,
        })

    async def update_comment_status(self, ad_id: str, comment_ids: List[str], status: str) -> Dict:
        """
        隐藏/显示评论
        POST /open_api/v1.3/comment/status/update/
        status: PUBLIC / HIDDEN
        """
        return await self._request("POST", "/open_api/v1.3/comment/status/update/", json_body={
            "advertiser_id": self.advertiser_id,
            "ad_id": ad_id,
            "comment_ids": comment_ids,
            "status": status,
        })

    async def delete_comment(self, ad_id: str, comment_ids: List[str]) -> Dict:
        """
        删除评论
        POST /open_api/v1.3/comment/delete/
        """
        return await self._request("POST", "/open_api/v1.3/comment/delete/", json_body={
            "advertiser_id": self.advertiser_id,
            "ad_id": ad_id,
            "comment_ids": comment_ids,
        })

    async def create_blocked_word(self, words: List[str]) -> Dict:
        """
        创建屏蔽词
        POST /open_api/v1.3/blockedword/create/
        """
        return await self._request("POST", "/open_api/v1.3/blockedword/create/", json_body={
            "advertiser_id": self.advertiser_id,
            "blocked_words": words,
        })

    async def get_blocked_words(self) -> Dict:
        """
        获取屏蔽词列表
        GET /open_api/v1.3/blockedword/list/
        """
        return await self._request("GET", "/open_api/v1.3/blockedword/list/", params={
            "advertiser_id": self.advertiser_id,
        })

    async def delete_blocked_word(self, blocked_word_ids: List[str]) -> Dict:
        """
        删除屏蔽词
        POST /open_api/v1.3/blockedword/delete/
        """
        return await self._request("POST", "/open_api/v1.3/blockedword/delete/", json_body={
            "advertiser_id": self.advertiser_id,
            "blocked_word_ids": blocked_word_ids,
        })

    # ===================== Lifecycle =====================

    async def close(self):
        """SDK 使用 urllib3 连接池，由全局 ApiClient 管理，无需手动关闭"""
        pass
