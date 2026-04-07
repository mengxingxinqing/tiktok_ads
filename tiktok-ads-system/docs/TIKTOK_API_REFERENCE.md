# TikTok Business API 接口参考文档

> 基于官方 SDK `tiktok-business-api-sdk` v1.2.1，API 版本 v1.3
> Base URL: `https://business-api.tiktok.com`
> 认证方式: 请求头 `Access-Token: {access_token}`

---

## 目录

1. [认证授权 (Authentication)](#1-认证授权)
2. [广告账户 (Account)](#2-广告账户)
3. [Campaign 管理](#3-campaign-管理)
4. [AdGroup 管理](#4-adgroup-管理)
5. [Ad 管理](#5-ad-管理)
6. [GMVMax 专属接口](#6-gmvmax-专属接口)
7. [Smart+ 接口](#7-smart-接口)
8. [报表查询 (Reporting)](#8-报表查询)
9. [素材文件 (File/Video/Image)](#9-素材文件)
10. [创意管理 (Creative)](#10-创意管理)
11. [店铺与商品 (Store/Catalog)](#11-店铺与商品)
12. [受众管理 (Audience/DMP)](#12-受众管理)
13. [身份管理 (Identity)](#13-身份管理)
14. [像素与事件 (Pixel/Event)](#14-像素与事件)
15. [Business Center (BC)](#15-business-center)
16. [工具类 (Tool)](#16-工具类)
17. [评论管理 (Comments)](#17-评论管理)
18. [自动规则 (Automated Rules)](#18-自动规则)
19. [应用管理 (App)](#19-应用管理)

---

## 1. 认证授权

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/oauth2/access_token/` | 获取 Access Token（OAuth2 授权码换 Token） |
| `GET` | `/open_api/v1.3/oauth2/advertiser/get/` | 获取授权的广告账户列表 |

## 2. 广告账户

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/advertiser/info/` | 获取广告账户信息 |
| `POST` | `/open_api/v1.3/advertiser/update/` | 更新广告账户信息 |
| `GET` | `/open_api/v1.3/advertiser/balance/get/` | 获取账户余额 |
| `GET` | `/open_api/v1.3/advertiser/transaction/get/` | 获取账户交易记录 |
| `GET` | `/open_api/v1.3/term/check/` | 检查服务条款状态 |
| `POST` | `/open_api/v1.3/term/confirm/` | 确认服务条款 |
| `GET` | `/open_api/v1.3/term/get/` | 获取服务条款 |

## 3. Campaign 管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/campaign/create/` | 创建 Campaign |
| `GET` | `/open_api/v1.3/campaign/get/` | 获取 Campaign 列表 |
| `POST` | `/open_api/v1.3/campaign/update/` | 更新 Campaign |
| `POST` | `/open_api/v1.3/campaign/status/update/` | 更新 Campaign 状态 |

## 4. AdGroup 管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/adgroup/create/` | 创建 AdGroup |
| `GET` | `/open_api/v1.3/adgroup/get/` | 获取 AdGroup 列表 |
| `POST` | `/open_api/v1.3/adgroup/update/` | 更新 AdGroup |
| `POST` | `/open_api/v1.3/adgroup/status/update/` | 更新 AdGroup 状态 |
| `GET` | `/open_api/v1.3/adgroup/quota/` | 获取 AdGroup 配额 |

## 5. Ad 管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/ad/create/` | 创建 Ad |
| `GET` | `/open_api/v1.3/ad/get/` | 获取 Ad 列表/详情 |
| `POST` | `/open_api/v1.3/ad/update/` | 更新 Ad |
| `POST` | `/open_api/v1.3/ad/status/update/` | 更新 Ad 状态 |
| `POST` | `/open_api/v1.3/ad/aco/create/` | 创建 ACO Ad |
| `GET` | `/open_api/v1.3/ad/aco/get/` | 获取 ACO Ad |
| `POST` | `/open_api/v1.3/ad/aco/update/` | 更新 ACO Ad |
| `POST` | `/open_api/v1.3/ad/aco/material_status/update/` | 更新 ACO 素材状态 |

### Ad Get 可用字段 (fields 参数)

> 注意: GMVMax Ad 不通过此接口返回，需使用 GMVMax 专属接口

```
ad_id, ad_name, adgroup_id, campaign_id, video_id, image_ids, ad_format,
item_group_ids, sku_ids, product_info, operation_status, create_time,
secondary_status, ad_text, ad_texts, call_to_action, landing_page_url,
identity_id, identity_type, ...
```

**⚠️ 不支持的字段**: `product_id`（需用 `item_group_ids` 代替）

## 6. GMVMax 专属接口

> GMVMax (GMV Maximization) 广告不通过标准 Campaign/Ad 接口暴露，有独立的 API 体系

### Campaign 管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/campaign/gmv_max/create/` | 创建 GMVMax Campaign |
| `GET` | `/open_api/v1.3/campaign/gmv_max/info/` | 获取 GMVMax Campaign 详情 ⚠️ `campaign_id` 必传 |
| `POST` | `/open_api/v1.3/campaign/gmv_max/update/` | 更新 GMVMax Campaign |

### GMVMax Campaign Info 返回字段
```json
{
  "campaign_id": "1860170148768769",
  "campaign_name": "商品 GMV Max_总收入_...",
  "budget": 20,
  "roas_bid": 1.5,
  "operation_status": "ENABLE",
  "item_group_ids": ["1734279365287380445"],
  "identity_list": [
    {"identity_id": "xxx", "identity_type": "TTS_TT", "store_id": "xxx"}
  ],
  "store_id": "7494275728565437917",
  "store_authorized_bc_id": "7615007176230338577",
  "product_video_specific_type": "AUTO_SELECTION",
  "shopping_ads_type": "PRODUCT",
  ...
}
```

### Session 管理（分时段投放）

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/campaign/gmv_max/session/create/` | 创建投放时段 |
| `GET` | `/open_api/v1.3/campaign/gmv_max/session/get/` | 获取投放时段详情 |
| `GET` | `/open_api/v1.3/campaign/gmv_max/session/list/` | 列出投放时段 |
| `POST` | `/open_api/v1.3/campaign/gmv_max/session/update/` | 更新投放时段 |
| `POST` | `/open_api/v1.3/campaign/gmv_max/session/delete/` | 删除投放时段 |

### 店铺与授权

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/gmv_max/store/list/` | 获取关联店铺列表 |
| `GET` | `/open_api/v1.3/gmv_max/store/shop_ad_usage_check/` | 检查店铺广告使用状态 |
| `POST` | `/open_api/v1.3/gmv_max/exclusive_authorization/create/` | 创建独占授权 |
| `GET` | `/open_api/v1.3/gmv_max/exclusive_authorization/get/` | 获取独占授权状态 |

### 🔑 创意视频（核心接口）

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/gmv_max/video/get/` | **获取 GMVMax 创意视频列表** |
| `GET` | `/open_api/v1.3/gmv_max/identity/get/` | 获取可用达人身份列表 |
| `GET` | `/open_api/v1.3/gmv_max/custom_anchor_video_list/get/` | 获取自定义锚点视频列表 |
| `GET` | `/open_api/v1.3/gmv_max/bid/recommend/` | 获取出价建议 |
| `GET` | `/open_api/v1.3/gmv_max/occupied_custom_shop_ads/list/` | 获取已占用的自定义店铺广告 |

#### `/gmv_max/video/get/` 详细说明

> **这是获取商品关联创意视频的关键接口**，对应 TikTok 后台「商品分析 → 关联创意」

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `advertiser_id` | string | ✅ | 广告账户 ID |
| `store_id` | string | ✅ | 店铺 ID |
| `store_authorized_bc_id` | string | ✅ | 店铺授权的 BC ID |
| `spu_id_list` | string[] | | 按 SPU ID 过滤 |
| `identity_list` | object[] | ⚠️ 建议传 | 达人身份列表（不传可能返回空） |
| `page` | int | | 页码，默认 1 |
| `page_size` | int | | 每页数量，默认 10，最大 50 |
| `sort_field` | string | | 排序：`GMV` / `VIDEO_VIEWS` / `VIDEO_LIKES` / `CLICK_THROUGH_RATE` / `ORDER_RATE` / `POST_TIME` / `PRODUCT_CLICKS` |
| `sort_type` | string | | `ASC` / `DESC`（默认） |
| `keyword` | string | | 关键词搜索 |
| `custom_posts_eligible` | bool | | 是否只返回可自定义的帖子 |

**identity_list 元素格式**:
```json
{
  "identity_id": "7592163398194234375",
  "identity_type": "TTS_TT",
  "store_id": "7494275728565437917"
}
```

**响应格式**:
```json
{
  "item_list": [
    {
      "item_id": "7592448323710209287",
      "text": "Look at me growing more hair...",
      "spu_id_list": ["1733590471946241501"],
      "can_change_anchor": true,
      "video_info": {
        "video_id": "v14025g50000d5esm8fog65rklm3mnd0",
        "preview_url": "https://...",
        "video_cover_url": "https://...",
        "duration": 15.5,
        "width": 720,
        "height": 1280,
        "bit_rate": 1200,
        "format": "mp4",
        "size": 2048000,
        "signature": "abc123..."
      },
      "identity_info": {
        "identity_id": "7592163398194234375",
        "identity_type": "TTS_TT",
        "display_name": "Jingshun Hall Store",
        "profile_image": "https://..."
      }
    }
  ],
  "page_info": {
    "page": 1,
    "page_size": 10,
    "total_number": 3,
    "total_page": 1
  }
}
```

**⚠️ 重要注意事项**:
1. 必须先调 `/gmv_max/identity/get/` 获取达人身份，再传入 `identity_list` 参数
2. 不传 `identity_list` 时大概率返回空列表
3. `spu_id_list` 可选，不传则返回该达人下所有创意视频
4. `item_id` 是创意的唯一标识，可通过 `spu_id_list` 关联到商品

#### `/gmv_max/identity/get/` 详细说明

**请求参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `advertiser_id` | string | ✅ | 广告账户 ID |
| `store_id` | string | ✅ | 店铺 ID |
| `store_authorized_bc_id` | string | ✅ | 店铺授权的 BC ID |

**响应格式**:
```json
{
  "identity_list": [
    {
      "identity_id": "7592163398194234375",
      "identity_type": "TTS_TT",
      "display_name": "Jingshun Hall Store",
      "profile_image": "https://...",
      "product_gmv_max_available": true,
      "live_gmv_max_available": false,
      "user_name": "jingshunhall"
    }
  ]
}
```

### GMVMax 报表

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/gmv_max/report/get/` | GMVMax 报表查询 |

**可用维度 (dimensions)**:
- `campaign_id` — Campaign 级
- `stat_time_day` — 按天
- `item_group_id` — 商品组级（需传 `filtering.campaign_ids`）
- `item_id` — 创意级/单品级（需传 `filtering.campaign_ids` + `filtering.item_group_ids`）

**可用过滤 (filtering)**:
```json
{
  "campaign_ids": ["xxx"],
  "campaign_name": "关键词",
  "campaign_statuses": ["STATUS_DELIVERY_OK", "STATUS_DISABLE"],
  "item_group_ids": ["xxx"],
  "item_ids": ["xxx"],
  "room_ids": ["xxx"],
  "creative_types": [1, 2, 3],
  "creative_delivery_statuses": [1, 2, 3],
  "gmv_max_promotion_types": [0, 1],
  "search_word": "关键词"
}
```

**creative_types 枚举**: `1`=ADS_AND_ORGANIC, `2`=ORGANIC, `3`=REMOVED

**creative_delivery_statuses 枚举**: `1`=IN_QUEUE, `2`=LEARNING, `3`=DELIVERING, `4`=NOT_DELIVERING, `5`=AUTHORIZATION_NEEDED, `6`=EXCLUDED, `7`=UNAVAILABLE, `9`=REJECTED, `10`=NOT_ACTIVE

**gmv_max_promotion_types 枚举**: `0`=PRODUCT, `1`=LIVE

**可用指标 (metrics)**:
```
cost, gross_revenue, orders, roi, cost_per_order,
product_impressions, product_clicks, product_click_rate,
live_views, ...
```

## 7. Smart+ 接口

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/smart_plus/campaign/create/` | 创建 Smart+ Campaign |
| `GET` | `/open_api/v1.3/smart_plus/campaign/get/` | 获取 Smart+ Campaign |
| `POST` | `/open_api/v1.3/smart_plus/campaign/update/` | 更新 Smart+ Campaign |
| `POST` | `/open_api/v1.3/smart_plus/campaign/status/update/` | 更新状态 |
| `POST` | `/open_api/v1.3/smart_plus/adgroup/create/` | 创建 Smart+ AdGroup |
| `GET` | `/open_api/v1.3/smart_plus/adgroup/get/` | 获取 Smart+ AdGroup |
| `POST` | `/open_api/v1.3/smart_plus/adgroup/update/` | 更新 Smart+ AdGroup |
| `POST` | `/open_api/v1.3/smart_plus/adgroup/status/update/` | 更新状态 |
| `POST` | `/open_api/v1.3/smart_plus/ad/create/` | 创建 Smart+ Ad |
| `GET` | `/open_api/v1.3/smart_plus/ad/get/` | 获取 Smart+ Ad |
| `POST` | `/open_api/v1.3/smart_plus/ad/update/` | 更新 Smart+ Ad |
| `POST` | `/open_api/v1.3/smart_plus/ad/status/update/` | 更新状态 |
| `POST` | `/open_api/v1.3/smart_plus/ad/appeal/` | Smart+ Ad 申诉 |
| `GET` | `/open_api/v1.3/smart_plus/ad/review_info/` | 获取审核信息 |
| `POST` | `/open_api/v1.3/smart_plus/ad/material_status/update/` | 更新素材状态 |
| `GET` | `/open_api/v1.3/smart_plus/material/review_info/` | 获取素材审核信息 |
| `GET` | `/open_api/v1.3/smart_plus/material_report/overview/` | 素材报表概览 |
| `GET` | `/open_api/v1.3/smart_plus/material_report/breakdown/` | 素材报表明细 |

## 8. 报表查询

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/report/integrated/get/` | 综合报表查询（同步） |
| `POST` | `/open_api/v1.3/report/task/create/` | 创建异步报表任务 |
| `GET` | `/open_api/v1.3/report/task/check/` | 检查报表任务状态 |
| `POST` | `/open_api/v1.3/report/task/cancel/` | 取消报表任务 |
| `GET` | `/open_api/v1.3/gmv_max/report/get/` | GMVMax 专用报表（见第 6 节） |

### 综合报表 data_level 支持值
```
AUCTION_CAMPAIGN, AUCTION_ADGROUP, AUCTION_AD,
RESERVATION_CAMPAIGN, RESERVATION_ADGROUP, RESERVATION_AD,
AUCTION_ADVERTISER, RESERVATION_ADVERTISER
```

**⚠️ 注意**: GMVMax 广告数据不在 `AUCTION_*` 报表中，需用 `/gmv_max/report/get/`

## 9. 素材文件

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/file/video/ad/upload/` | 上传广告视频 |
| `GET` | `/open_api/v1.3/file/video/ad/info/` | 获取视频信息 |
| `GET` | `/open_api/v1.3/file/video/ad/search/` | 搜索视频素材库 |
| `POST` | `/open_api/v1.3/file/image/ad/upload/` | 上传广告图片 |
| `GET` | `/open_api/v1.3/file/image/ad/info/` | 获取图片信息 |

### `/file/video/ad/search/` 返回字段
```json
{
  "video_id": "xxx",
  "preview_url": "https://...",
  "video_cover_url": "https://...",
  "file_name": "product_demo.mp4",
  "duration": 30.5,
  "width": 1080,
  "height": 1920
}
```

**⚠️ 注意**: GMVMax 自动选取的视频不在广告素材库中，需用 `/gmv_max/video/get/`

## 10. 创意管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/creative/asset/delete/` | 删除创意素材 |
| `POST` | `/open_api/v1.3/creative/asset/share/` | 分享创意素材 |
| `POST` | `/open_api/v1.3/creative/image/edit/` | 编辑创意图片 |
| `POST` | `/open_api/v1.3/creative/portfolio/create/` | 创建创意集 |
| `GET` | `/open_api/v1.3/creative/portfolio/get/` | 获取创意集 |
| `GET` | `/open_api/v1.3/creative/portfolio/list/` | 列出创意集 |
| `POST` | `/open_api/v1.3/creative/shareable_link/create/` | 创建可分享链接 |
| `POST` | `/open_api/v1.3/creative/smart_text/generate/` | AI 生成文案 |
| `GET` | `/open_api/v1.3/discovery/detail/` | 发现详情 |
| `GET` | `/open_api/v1.3/discovery/trending_list/` | 趋势列表 |
| `POST` | `/open_api/v1.3/playable/upload/` | 上传互动素材 |
| `POST` | `/open_api/v1.3/playable/save/` | 保存互动素材 |
| `GET` | `/open_api/v1.3/playable/get/` | 获取互动素材 |
| `GET` | `/open_api/v1.3/playable/validate/` | 验证互动素材 |
| `POST` | `/open_api/v1.3/playable/delete/` | 删除互动素材 |

## 11. 店铺与商品

### 店铺
| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/store/list/` | 获取关联店铺列表 |
| `GET` | `/open_api/v1.3/store/product/list/` | 获取店铺商品列表 |

### 商品目录 (Catalog)
| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/catalog/create/` | 创建商品目录 |
| `GET` | `/open_api/v1.3/catalog/get/` | 获取商品目录 |
| `POST` | `/open_api/v1.3/catalog/update/` | 更新商品目录 |
| `POST` | `/open_api/v1.3/catalog/delete/` | 删除商品目录 |
| `GET` | `/open_api/v1.3/catalog/overview/` | 商品目录概览 |
| `POST` | `/open_api/v1.3/catalog/capitalize/` | 商品目录资本化 |
| `GET` | `/open_api/v1.3/catalog/available_country/get/` | 获取可用国家 |
| `GET` | `/open_api/v1.3/catalog/location_currency/get/` | 获取地区货币 |
| `GET` | `/open_api/v1.3/catalog/lexicon/get/` | 获取商品词典 |
| `POST` | `/open_api/v1.3/catalog/feed/create/` | 创建商品 Feed |
| `GET` | `/open_api/v1.3/catalog/feed/get/` | 获取 Feed |
| `POST` | `/open_api/v1.3/catalog/feed/update/` | 更新 Feed |
| `POST` | `/open_api/v1.3/catalog/feed/delete/` | 删除 Feed |
| `GET` | `/open_api/v1.3/catalog/feed/log/` | Feed 日志 |
| `POST` | `/open_api/v1.3/catalog/product/file/` | 上传商品文件 |
| `POST` | `/open_api/v1.3/catalog/product/delete/` | 删除商品 |
| `GET` | `/open_api/v1.3/catalog/product/log/` | 商品日志 |
| `GET` | `/open_api/v1.3/catalog/set/get/` | 获取商品集 |
| `POST` | `/open_api/v1.3/catalog/set/update/` | 更新商品集 |
| `POST` | `/open_api/v1.3/catalog/set/delete/` | 删除商品集 |
| `GET` | `/open_api/v1.3/catalog/set/product/get/` | 获取商品集内商品 |
| `GET` | `/open_api/v1.3/catalog/video/get/` | 获取目录视频 |
| `POST` | `/open_api/v1.3/catalog/video/delete/` | 删除目录视频 |
| `POST` | `/open_api/v1.3/catalog/eventsource/bind/` | 绑定事件源 |
| `GET` | `/open_api/v1.3/catalog/eventsource_bind/get/` | 获取绑定状态 |
| `POST` | `/open_api/v1.3/catalog/eventsource/unbind/` | 解绑事件源 |

## 12. 受众管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/audience/insight/overlap/` | 受众重叠分析 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/create/` | 创建自定义受众 |
| `GET` | `/open_api/v1.3/dmp/custom_audience/get/` | 获取自定义受众详情 |
| `GET` | `/open_api/v1.3/dmp/custom_audience/list/` | 列出自定义受众 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/update/` | 更新自定义受众 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/delete/` | 删除自定义受众 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/file/upload/` | 上传受众文件 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/rule/create/` | 创建基于规则的受众 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/lookalike/create/` | 创建 Lookalike 受众 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/lookalike/update/` | 更新 Lookalike 受众 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/apply/` | 申请使用受众 |
| `GET` | `/open_api/v1.3/dmp/custom_audience/apply/log/` | 申请日志 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/share/` | 分享受众 |
| `POST` | `/open_api/v1.3/dmp/custom_audience/share/cancel/` | 取消分享 |
| `GET` | `/open_api/v1.3/dmp/custom_audience/share/log/` | 分享日志 |
| `POST` | `/open_api/v1.3/dmp/saved_audience/create/` | 创建保存的受众 |
| `GET` | `/open_api/v1.3/dmp/saved_audience/list/` | 列出保存的受众 |
| `POST` | `/open_api/v1.3/dmp/saved_audience/delete/` | 删除保存的受众 |

## 13. 身份管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/identity/create/` | 创建身份 |
| `GET` | `/open_api/v1.3/identity/get/` | 获取身份列表 |
| `GET` | `/open_api/v1.3/identity/video/info/` | 获取身份下视频信息 |
| `GET` | `/open_api/v1.3/gmv_max/identity/get/` | 获取 GMVMax 可用达人身份 |

## 14. 像素与事件

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/pixel/create/` | 创建 Pixel |
| `GET` | `/open_api/v1.3/pixel/list/` | 列出 Pixel |
| `POST` | `/open_api/v1.3/pixel/update/` | 更新 Pixel |
| `POST` | `/open_api/v1.3/pixel/event/create/` | 创建 Pixel 事件 |
| `GET` | `/open_api/v1.3/pixel/event/stats/` | Pixel 事件统计 |
| `POST` | `/open_api/v1.3/pixel/event/update/` | 更新 Pixel 事件 |
| `POST` | `/open_api/v1.3/pixel/event/delete/` | 删除 Pixel 事件 |
| `POST` | `/open_api/v1.3/pixel/batch/` | 批量上报 Pixel 事件 |
| `POST` | `/open_api/v1.3/pixel/track/` | 上报单次 Pixel 事件 |

## 15. Business Center

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/bc/get/` | 获取 BC 信息 |
| `POST` | `/open_api/v1.3/bc/advertiser/create/` | 在 BC 下创建广告账户 |
| `GET` | `/open_api/v1.3/bc/balance/get/` | 获取 BC 余额 |
| `GET` | `/open_api/v1.3/bc/transaction/get/` | BC 交易记录 |
| `GET` | `/open_api/v1.3/bc/account/transaction/get/` | BC 账户交易记录 |
| `POST` | `/open_api/v1.3/bc/transfer/` | BC 转账 |
| `GET` | `/open_api/v1.3/bc/invoice/unpaid/get/` | 获取未付发票 |
| `GET` | `/open_api/v1.3/bc/billing_group/get/` | 获取账单组 |
| `POST` | `/open_api/v1.3/bc/billing_group/create/` | 创建账单组 |
| `POST` | `/open_api/v1.3/bc/billing_group/update/` | 更新账单组 |
| `GET` | `/open_api/v1.3/bc/member/get/` | 获取 BC 成员 |
| `POST` | `/open_api/v1.3/bc/member/invite/` | 邀请成员 |
| `POST` | `/open_api/v1.3/bc/member/update/` | 更新成员 |
| `POST` | `/open_api/v1.3/bc/member/delete/` | 删除成员 |
| `GET` | `/open_api/v1.3/bc/partner/get/` | 获取合作伙伴 |
| `POST` | `/open_api/v1.3/bc/partner/add/` | 添加合作伙伴 |
| `POST` | `/open_api/v1.3/bc/partner/delete/` | 删除合作伙伴 |
| `GET` | `/open_api/v1.3/bc/partner/asset/get/` | 获取合作伙伴资产 |
| `POST` | `/open_api/v1.3/bc/partner/asset/delete/` | 删除合作伙伴资产 |
| `GET` | `/open_api/v1.3/bc/asset/get/` | 获取资产列表 |
| `POST` | `/open_api/v1.3/bc/asset/assign/` | 分配资产 |
| `POST` | `/open_api/v1.3/bc/asset/unassign/` | 取消分配资产 |
| `GET` | `/open_api/v1.3/bc/asset/admin/get/` | 获取管理员资产 |
| `POST` | `/open_api/v1.3/bc/asset/admin/delete/` | 删除管理员资产 |
| `GET` | `/open_api/v1.3/bc/asset/member/get/` | 获取成员资产 |
| `GET` | `/open_api/v1.3/bc/asset/partner/get/` | 获取合作伙伴资产 |
| `GET` | `/open_api/v1.3/bc/asset_group/list/` | 列出资产组 |
| `POST` | `/open_api/v1.3/bc/asset_group/create/` | 创建资产组 |
| `GET` | `/open_api/v1.3/bc/asset_group/get/` | 获取资产组 |
| `POST` | `/open_api/v1.3/bc/asset_group/update/` | 更新资产组 |
| `POST` | `/open_api/v1.3/bc/asset_group/delete/` | 删除资产组 |
| `POST` | `/open_api/v1.3/bc/image/upload/` | 通过 BC 上传图片 |
| `GET` | `/open_api/v1.3/bc/pixel/link/get/` | 获取 Pixel 关联 |
| `POST` | `/open_api/v1.3/bc/pixel/link/update/` | 更新 Pixel 关联 |
| `POST` | `/open_api/v1.3/bc/pixel/transfer/` | 转移 Pixel |

## 16. 工具类

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/tool/targeting/list/` | 获取定向选项列表 |
| `POST` | `/open_api/v1.3/tool/targeting/info/` | 获取定向详情 |
| `POST` | `/open_api/v1.3/tool/targeting/search/` | 搜索定向 |
| `POST` | `/open_api/v1.3/tool/targeting_category/recommend/` | 推荐定向类目 |
| `POST` | `/open_api/v1.3/tool/bid/recommend/` | 出价建议 |
| `GET` | `/open_api/v1.3/tool/action_category/` | 行为类目 |
| `GET` | `/open_api/v1.3/tool/carrier/` | 运营商列表 |
| `GET` | `/open_api/v1.3/tool/contextual_tag/get/` | 上下文标签 |
| `GET` | `/open_api/v1.3/tool/contextual_tag/info/` | 上下文标签详情 |
| `GET` | `/open_api/v1.3/tool/hashtag/get/` | 获取 Hashtag |
| `GET` | `/open_api/v1.3/tool/hashtag/recommend/` | 推荐 Hashtag |
| `GET` | `/open_api/v1.3/tool/interest_keyword/get/` | 兴趣关键词 |
| `GET` | `/open_api/v1.3/tool/open_url/` | 获取 Open URL |
| `GET` | `/open_api/v1.3/tool/os_version/` | OS 版本列表 |
| `GET` | `/open_api/v1.3/tool/phone_region_code/` | 手机区号 |
| `GET` | `/open_api/v1.3/tool/timezone/` | 时区列表 |
| `GET` | `/open_api/v1.3/tool/url_validate/` | URL 验证 |
| `GET` | `/open_api/v1.3/tool/vbo_status/` | VBO 状态 |
| `GET` | `/open_api/v1.3/tool/brand_safety/partner/authorize/status/` | 品牌安全授权状态 |
| `GET` | `/open_api/v1.3/search/region/` | 搜索地区 |

## 17. 评论管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/comment/list/` | 获取评论列表 |
| `POST` | `/open_api/v1.3/comment/post/` | 发布评论 |
| `POST` | `/open_api/v1.3/comment/delete/` | 删除评论 |
| `POST` | `/open_api/v1.3/comment/status/update/` | 更新评论状态 |
| `GET` | `/open_api/v1.3/comment/reference/` | 获取评论引用 |
| `POST` | `/open_api/v1.3/comment/task/create/` | 创建评论任务 |
| `GET` | `/open_api/v1.3/comment/task/check/` | 检查评论任务 |
| `POST` | `/open_api/v1.3/blockedword/create/` | 创建屏蔽词 |
| `GET` | `/open_api/v1.3/blockedword/list/` | 获取屏蔽词列表 |
| `POST` | `/open_api/v1.3/blockedword/update/` | 更新屏蔽词 |
| `POST` | `/open_api/v1.3/blockedword/delete/` | 删除屏蔽词 |
| `GET` | `/open_api/v1.3/blockedword/check/` | 检查屏蔽词 |
| `POST` | `/open_api/v1.3/blockedword/task/create/` | 创建屏蔽词任务 |
| `GET` | `/open_api/v1.3/blockedword/task/check/` | 检查屏蔽词任务 |

## 18. 自动规则

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/optimizer/rule/create/` | 创建自动规则 |
| `GET` | `/open_api/v1.3/optimizer/rule/get/` | 获取规则详情 |
| `GET` | `/open_api/v1.3/optimizer/rule/list/` | 列出规则 |
| `POST` | `/open_api/v1.3/optimizer/rule/update/` | 更新规则 |
| `POST` | `/open_api/v1.3/optimizer/rule/batch_bind/` | 批量绑定规则 |
| `GET` | `/open_api/v1.3/optimizer/rule/result/get/` | 获取规则执行结果 |
| `GET` | `/open_api/v1.3/optimizer/rule/result/list/` | 列出规则执行结果 |

## 19. 应用管理

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/app/create/` | 创建应用 |
| `GET` | `/open_api/v1.3/app/info/` | 获取应用信息 |
| `GET` | `/open_api/v1.3/app/list/` | 列出应用 |
| `POST` | `/open_api/v1.3/app/update/` | 更新应用 |
| `GET` | `/open_api/v1.3/app/optimization_event/` | 获取优化事件 |
| `GET` | `/open_api/v1.3/app/optimization_event/retargeting/` | 获取再营销优化事件 |

---

## 附录

### Pangle 相关

| 方法 | 端点 | 说明 |
|------|------|------|
| `GET` | `/open_api/v1.3/pangle_audience_package/get/` | Pangle 受众包 |
| `GET` | `/open_api/v1.3/pangle_block_list/get/` | Pangle 屏蔽列表 |
| `POST` | `/open_api/v1.3/pangle_block_list/update/` | 更新 Pangle 屏蔽列表 |

### 离线事件

| 方法 | 端点 | 说明 |
|------|------|------|
| `POST` | `/open_api/v1.3/offline/create/` | 创建离线事件集 |
| `GET` | `/open_api/v1.3/offline/get/` | 获取离线事件集 |
| `POST` | `/open_api/v1.3/offline/update/` | 更新离线事件集 |
| `POST` | `/open_api/v1.3/offline/delete/` | 删除离线事件集 |

---

### 本项目已实现的接口

以下是 `TikTokClient` (`app/services/tiktok_client.py`) 中已封装的方法：

| 方法 | 对应端点 | 用途 |
|------|----------|------|
| `get_campaigns()` | `campaign/get/` | 获取 Campaign 列表 |
| `get_adgroups()` | `adgroup/get/` | 获取 AdGroup 列表 |
| `get_ads()` | `ad/get/` | 获取 Ad 列表 |
| `get_ad_detail()` | `ad/get/` | 获取 Ad 详情（含 item_group_ids） |
| `get_report()` | `report/integrated/get/` | 综合报表查询 |
| `get_video_info()` | `file/video/ad/search/` | 搜索视频素材库 |
| `update_ad_status()` | `ad/status/update/` | 更新 Ad 状态 |
| `update_adgroup_status()` | `adgroup/status/update/` | 更新 AdGroup 状态 |
| `update_adgroup_budget()` | `adgroup/update/` | 更新 AdGroup 预算 |
| `update_campaign_budget()` | `campaign/update/` | 更新 Campaign 预算 |
| `create_campaign()` | `campaign/create/` | 创建 Campaign |
| `create_adgroup()` | `adgroup/create/` | 创建 AdGroup |
| `create_ad()` | `ad/create/` | 创建 Ad |
| `upload_video()` | `file/video/ad/upload/` | 上传视频 |
| `upload_image()` | `file/image/ad/upload/` | 上传图片 |
| `get_gmvmax_store_list()` | `gmv_max/store/list/` | 获取 GMVMax 关联店铺 |
| `get_gmvmax_campaign_info()` | `campaign/gmv_max/info/` | GMVMax Campaign 详情 |
| `get_gmvmax_report()` | `gmv_max/report/get/` | GMVMax Campaign 报表 |
| `get_gmvmax_item_report()` | `gmv_max/report/get/` | GMVMax 商品组报表 |
| `get_gmvmax_creative_report()` | `gmv_max/report/get/` | GMVMax 创意级报表 |
| `get_gmvmax_videos()` | `gmv_max/video/get/` | **GMVMax 创意视频列表** |
| `get_all_gmvmax_videos()` | `gmv_max/video/get/` | GMVMax 创意视频（自动翻页） |
| `get_gmvmax_identities()` | `gmv_max/identity/get/` | GMVMax 达人身份列表 |
| `get_store_products()` | `store/product/list/` | 获取店铺商品 |
| `get_all_store_products()` | `store/product/list/` | 获取全部商品（翻页） |
| `get_order_report()` | `report/integrated/get/` | 订单报表 |
| `refresh_token()` | `oauth2/access_token/` | 刷新 Token |

---

> 官方 SDK 仓库: `tiktok/tiktok-business-api-sdk`
> 官方文档: https://business-api.tiktok.com/portal/docs
> 更新时间: 2026-04-02
