# TikTok Ads 广告创建指南

## 概述

本系统现已支持**自动创建转化型Ads广告**，从上传创意到建立完整广告结构，一行代码即可完成。

---

## 核心概念

### TikTok Ads 广告结构

```
Campaign (推广计划)
  ├─ objective_type: CONVERSION（转化目标）
  └─ budget: 总预算
      └─ AdGroup (广告组)
           ├─ targeting: 受众定向（年龄、性别、地区等）
           ├─ bid_type: CPC / CPM / oCPC / oCPM
           └─ bid: 出价
               └─ Ad (广告)
                    ├─ video_id 或 image_ids: 创意
                    ├─ landing_page_url: 落地页（转化关键）
                    └─ call_to_action: 行动号召
```

### Ads vs GMVMAX

| 特性 | Ads | GMVMAX |
|------|-----|--------|
| 目标 | 灵活（转化/流量/覆盖等） | **商品销售** |
| 需求 | 任何商业网站 | 必须TikTok Shop |
| 优化 | 手动 + 自动出价 | 全自动ROI优化 |
| 适用 | 独立站、SaaS、服务等 | TikTok Shop 卖家 |

---

## 快速开始

### 方式1：完整自动化（推荐）

```python
# 上传视频 + 创建完整广告（最高级）
POST /ads/campaign/create-full

{
    "advertiser_id": "xxxx",
    "campaign_name": "Product_A_20260401",
    "daily_budget": 100.0,
    "video_id": "7123456789",        # 已上传的视频ID
    "landing_page_url": "https://yourshop.com/product-a",
    "ad_text": "Limited time offer! 30% off",
    "targeting": {
        "age": ["21", "35"],
        "gender": ["FEMALE"],
        "location": ["US", "CA", "UK"],
        "interest": ["shopping", "fashion", "beauty"],
        "placements": ["TIKTOK"],
        "languages": ["en"]
    }
}
```

**返回：**
```json
{
    "status": "success",
    "data": {
        "campaign_id": "campaign_123",
        "adgroup_id": "adgroup_456",
        "ad_id": "ad_789",
        "summary": {...}
    }
}
```

### 方式2：分步创建（细粒度控制）

#### 步骤1：上传视频

```bash
curl -X POST http://localhost:8000/ads/video/upload \
  -F "advertiser_id=xxxx" \
  -F "video_name=ProductA_v1" \
  -F "file=@path/to/video.mp4"
```

**返回：** `video_id`

#### 步骤2：创建推广计划

```bash
curl -X POST http://localhost:8000/ads/campaign/create \
  -H "Content-Type: application/json" \
  -d '{
    "advertiser_id": "xxxx",
    "campaign_name": "Product_A_20260401",
    "daily_budget": 100.0
  }'
```

**返回：** `campaign_id`

#### 步骤3：创建广告组（在ads_campaign_creator服务中调用）

#### 步骤4：创建广告（在ads_campaign_creator服务中调用）

---

## API 详细文档

### 1. 创建CONVERSION推广计划

**端点：** `POST /ads/campaign/create`

**参数：**
- `advertiser_id` (string, 必需): 广告账户ID
- `campaign_name` (string, 必需): 推广计划名称，建议格式 `SKU_20260401_v1`
- `daily_budget` (float, 可选): 每日预算（USD），默认 $100

**示例：**
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/ads/campaign/create",
        json={
            "advertiser_id": "1234567890",
            "campaign_name": "Summer_Collection_v1",
            "daily_budget": 150.0
        }
    )
    print(response.json())
```

**返回：**
```json
{
    "status": "success",
    "data": {
        "campaign_id": "campaign_123",
        "campaign_name": "Summer_Collection_v1",
        "daily_budget": 150.0
    }
}
```

---

### 2. 一键创建完整Ads广告

**端点：** `POST /ads/campaign/create-full`

**参数：**
- `advertiser_id` (string): 广告账户ID
- `campaign_name` (string): 推广计划名称
- `daily_budget` (float): 日预算（USD）
- `video_id` (string): 已上传的视频ID
- `landing_page_url` (string): 落地页URL（转化关键）
- `targeting` (object): 受众定向
- `ad_text` (string, 可选): 广告文案

**targeting 示例：**
```json
{
    "age": ["21", "35"],
    "gender": ["FEMALE"],
    "location": ["US", "CA", "UK"],
    "interest": ["shopping", "fashion"],
    "placements": ["TIKTOK"],
    "languages": ["en"]
}
```

**返回：**
```json
{
    "status": "success",
    "data": {
        "campaign_id": "...",
        "adgroup_id": "...",
        "ad_id": "...",
        "summary": {
            "campaign_name": "...",
            "daily_budget": 100.0,
            "video_id": "...",
            "landing_page_url": "https://...",
            "targeting": {...}
        }
    }
}
```

---

### 3. 上传视频创意

**端点：** `POST /ads/video/upload`

**参数：**
- `advertiser_id` (string): 广告账户ID
- `file` (file): 视频文件（MP4, MOV, AVI等）
- `video_name` (string): 视频名称

**视频要求：**
- 格式：MP4, MOV, AVI, WMV
- 最大尺寸：2GB
- 时长：3秒 - 60分钟（建议 < 60秒）
- 分辨率：推荐 1080x1920（竖屏） 或 1920x1080（横屏）

**Python 示例：**
```python
import httpx

async with httpx.AsyncClient() as client:
    with open("product_video.mp4", "rb") as f:
        response = await client.post(
            "http://localhost:8000/ads/video/upload",
            params={
                "advertiser_id": "1234567890",
                "video_name": "ProductDemo_v1"
            },
            files={"file": f}
        )
        video_data = response.json()
        print(video_data["data"]["video_id"])  # 用于创建广告
```

---

### 4. 上传图片创意

**端点：** `POST /ads/image/upload`

**参数：**
- `advertiser_id` (string): 广告账户ID
- `file` (file): 图片文件（PNG, JPG, GIF等）
- `image_name` (string): 图片名称

**图片要求：**
- 格式：PNG, JPG, JPEG, GIF, WEBP
- 最大尺寸：30MB
- 分辨率：推荐 1080x1920（竖屏） 或 1920x1080（横屏）
- 最小：600x600

---

## 实际应用例子

### 场景1：新产品上市

```python
from app.services.tiktok_client import TikTokClient
from app.services.ads_campaign_creator import AdsCampaignCreator

# 初始化
client = TikTokClient(access_token="...", advertiser_id="...")
creator = AdsCampaignCreator(client, db)

# 上传视频 + 创建广告
result = await creator.upload_and_create_campaign(
    advertiser_id="1234567890",
    campaign_name="iPhone_15_Launch",
    daily_budget=500.0,
    video_file_path="/path/to/iphone_demo.mp4",
    landing_page_url="https://apple.com/iphone15",
    targeting={
        "age": ["18", "65"],
        "location": ["US", "CA", "UK", "AU"],
        "interest": ["technology", "gadgets"],
        "placements": ["TIKTOK"],
    },
    ad_text="iPhone 15: Powered by A17 Pro. Available now!"
)

print(result)
# 返回 campaign_id, adgroup_id, ad_id
```

### 场景2：按地区分层投放

```python
# 为不同地区创建不同的广告组和出价

# US 女性用户
us_campaign = await creator.create_full_campaign(
    advertiser_id="...",
    campaign_name="Summer_US_Female",
    daily_budget=200.0,
    video_id="xxx",
    landing_page_url="https://...",
    targeting={
        "age": ["18", "45"],
        "gender": ["FEMALE"],
        "location": ["US"],
        "interest": ["fashion", "shopping"],
        "placements": ["TIKTOK"],
    }
)

# UK 男性用户
uk_campaign = await creator.create_full_campaign(
    advertiser_id="...",
    campaign_name="Summer_UK_Male",
    daily_budget=100.0,
    video_id="xxx",
    landing_page_url="https://...",
    targeting={
        "age": ["25", "55"],
        "gender": ["MALE"],
        "location": ["UK"],
        "interest": ["sports", "outdoors"],
        "placements": ["TIKTOK"],
    }
)
```

### 场景3：A/B测试不同创意

```python
# 视频A
video_a = await client.upload_video(
    file_path="/path/to/creative_a.mp4",
    video_name="TestA_v1"
)

# 视频B
video_b = await client.upload_video(
    file_path="/path/to/creative_b.mp4",
    video_name="TestB_v1"
)

# 同一受众，不同创意
campaign_a = await creator.create_full_campaign(
    advertiser_id="...",
    campaign_name="ABTest_CreativeA",
    daily_budget=50.0,
    video_id=video_a["video_id"],
    landing_page_url="https://...",
    targeting={...}
)

campaign_b = await creator.create_full_campaign(
    advertiser_id="...",
    campaign_name="ABTest_CreativeB",
    daily_budget=50.0,
    video_id=video_b["video_id"],
    landing_page_url="https://...",
    targeting={...}
)

# 对比两个广告的转化效果
```

---

## 转化优化建议

### 1. 受众定向

**高转化受众特征：**
- 年龄：通常 25-44 岁转化率最高
- 地理：发达国家（US, UK, CA, AU） vs 新兴市场
- 兴趣：购物、时尚、美妆、技术等高消费力人群
- 语言：与落地页语言匹配

### 2. 落地页优化

```python
# ❌ 不好的落地页
"landing_page_url": "https://example.com"  # 泛用首页

# ✅ 好的落地页
"landing_page_url": "https://example.com/product/summer-collection?utm_source=tiktok&utm_medium=ads&utm_campaign=summer_2026"
```

### 3. 创意优化

- **前3秒很关键**：Hook率决定观看完成度
- **竖屏优先**：TikTok 用户90%+ 竖屏浏览
- **品质**：1080x1920 高清视频效果更好
- **长度**：15-30秒最佳（太长跳出率高）

### 4. 出价策略

```python
# 初始出价建议
bid_amount = {
    "TRAFFIC": 0.30,           # 流量 $0.30 CPC
    "CONVERSION": 0.50,        # 转化 $0.50 CPC（可根据LTV调整）
    "VIDEO_VIEWS": 0.01,       # 播放 $0.01 CPV
}
```

---

## 监控和优化

创建广告后，系统会**自动监控**以下指标：

- **CTR（点击率）**：通常 1-3%
- **CPC（单次点击成本）**：根据行业和地区
- **CVR（转化率）**：2-5% 较好
- **ROAS（广告回报率）**：目标 3:1 或以上

### 自动优化触发

当系统检测到以下情况时，会自动决策：
- Hook rate < 2% → 建议换素材
- CPM > 历史均值 20% → 降低出价
- CVR 下降 → 扩大受众范围或调整落地页

查看优化建议：
```
GET /decisions?advertiser_id=...&status=PENDING
```

---

## 常见问题

### Q1: 创建广告后多久能看到数据？
A: 广告上线后 24-48 小时才能积累足够的数据。建议先运行 3-7 天观察趋势。

### Q2: 如何选择 CPC vs CPM 出价？
A: 
- **CPC**：适合关注点击转化，风险低
- **CPM**：适合品牌曝光，成本可控

### Q3: 素材上传后如何重复使用？
A: 保存 `video_id` 和 `image_id`，创建不同广告时直接引用，无需重复上传。

### Q4: 如何暂停或编辑已创建的广告？
A: 暂停功能已在 `/decisions/{id}/approve` 中集成，LLM 会自动建议最优操作。

---

## 下一步

1. ✅ 创建转化型Ads广告
2. 📊 监控数据（系统自动同步）
3. 🤖 LLM 自动优化建议
4. 📈 根据ROAS调整预算

**如有问题，查看日志：**
```
tail -f /var/log/tiktok-ads-system.log
```
