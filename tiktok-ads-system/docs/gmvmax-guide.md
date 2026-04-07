# GMVMAX 广告创建指南

## 什么是 GMVMAX？

GMVMAX 是 TikTok 针对 TikTok Shop 卖家推出的**全自动优化投放模式**。

### GMVMAX vs Ads（对比）

| 特性 | GMVMAX | Ads |
|------|--------|-----|
| **优化方式** | 全自动（系统优化） | 手动+自动出价 |
| **适用场景** | TikTok Shop | 任何业务 |
| **配置复杂度** | 低（系统自动） | 中等（需配置） |
| **灵活性** | 低（全自动） | 高（可手动调整） |
| **学习期** | 长（7-14天） | 短（3-7天） |
| **目标** | GMV最大化 | 自定义目标 |
| **商品选择** | 自动选择最优商品 | 指定商品 |

---

## GMVMAX 工作原理

```
推广计划创建（GMVMAX目标）
    ↓
绑定 TikTok Shop
    ↓
系统自动分析：
  - Shop 中哪些商品表现最好
  - 什么人群更可能购买
  - 最优的出价是多少
    ↓
自动调整投放：
  - 优先推广高转化商品
  - 拓展潜力受众
  - 实时调整出价
    ↓
最大化商品销售额（GMV）
```

---

## API 使用方式

### 方式1：HTTP API

```bash
curl -X POST http://localhost:8000/ads/gmvmax/campaign/create-full \
  -H "Content-Type: application/json" \
  -d '{
    "advertiser_id": "1234567890",
    "campaign_name": "Summer_GMVMAX_20260401",
    "daily_budget": 100.0,
    "video_id": "7123456789",
    "shop_id": "your_shop_id",
    "ad_text": "Exclusive summer collection - Limited time!",
    "targeting": {
      "age": ["18", "45"],
      "gender": ["FEMALE"],
      "location": ["US", "CA"]
    }
  }'
```

### 方式2：Python 代码

```python
from app.services.tiktok_client import TikTokClient
from app.services.ads_campaign_creator import GmvmaxCampaignCreator

# 初始化
client = TikTokClient(access_token="...", advertiser_id="...")
creator = GmvmaxCampaignCreator(client, db)

# 创建GMVMAX广告
result = await creator.create_full_gmvmax_campaign(
    advertiser_id="1234567890",
    campaign_name="Summer_GMVMAX",
    daily_budget=100.0,
    video_id="7123456789",
    shop_id="your_shop_id",
    ad_text="Limited time offer!",
    targeting={
        "age": ["18", "45"],
        "gender": ["FEMALE"],
        "location": ["US", "CA"],
    }
)

print(f"Campaign: {result['campaign_id']}")
print(f"AdGroup: {result['adgroup_id']}")
print(f"Ad: {result['ad_id']}")
```

---

## GMVMAX 关键参数

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `advertiser_id` | 广告账户ID | `1234567890` |
| `campaign_name` | 推广计划名称 | `Summer_GMVMAX_v1` |
| `daily_budget` | 每日预算（USD） | `100.0` |
| `video_id` | 上传的视频ID | `7123456789` |
| `shop_id` | TikTok Shop ID | `shop_123456` |

### 可选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `ad_text` | 广告文案 | `"Summer sale 30% off"` |
| `targeting` | 受众定向 | `{"age": ["21", "45"], ...}` |
| `catalog_id` | 商品目录ID（指定投放商品范围） | `catalog_123` |

---

## GMVMAX 的自动优化

### 系统自动调整的内容

#### 1. 商品选择 🎯
```
不指定商品
    ↓
系统分析 Shop 中所有商品
    ↓
优先推广这些商品：
  - 高转化率商品
  - 高利润商品
  - 季节性热销商品
  - 库存充足商品
    ↓
根据实时效果动态调整
```

#### 2. 受众优化 👥
```
你指定的初始受众
    ↓
系统自动扩展和优化：
  - 扩展到相似受众
  - 找到最有购买意愿的人群
  - 自动调整年龄、地区、兴趣
    ↓
动态调整以最大化转化
```

#### 3. 出价优化 💰
```
系统自动调整出价：
  - 高转化人群：提高出价
  - 低转化人群：降低出价
  - 库存紧张商品：提高出价
  - 滞销商品：降低出价
```

---

## GMVMAX vs 我们的 Ads + LLM 优化

### GMVMAX 的优势 ✅
- 系统官方优化，更了解 TikTok 平台
- 专为 Shop 设计，商品库同步无延迟
- 全自动，无需人工干预
- 快速学习（7-14天数据稳定）

### 我们的 Ads + LLM 优化的优势 ✅
- 更灵活的定向和配置
- 可支持任何业务类型（不限于 Shop）
- LLM 分析提供可解释的优化建议
- 可手动调整，有更多控制权
- 落地页转化追踪更灵活

### 如何选择？

**选 GMVMAX 如果你：**
- 是 TikTok Shop 卖家
- 想要最大化商品销售额（GMV）
- 愿意让系统全自动优化
- 有足够的数据积累（预算充足）

**选 Ads 如果你：**
- 需要更灵活的定向配置
- 有特定的转化追踪要求
- 想要更多的控制权
- 不是 Shop 卖家（或者只做引流）

---

## 实战例子

### 例子1：TikTok Shop 卖家

```python
# 一键启动 GMVMAX 投放
result = await creator.create_full_gmvmax_campaign(
    advertiser_id="YOUR_ADVERTISER_ID",
    campaign_name="Q2_2026_GMVMAX",
    daily_budget=500.0,  # $500/天
    video_id="video_id_from_upload",
    shop_id="YOUR_SHOP_ID",
    ad_text="New Collection 2026 - Up to 50% Off!",
    targeting={
        "age": ["18", "55"],        # 全年龄段
        "location": ["US", "CA", "UK", "AU"],  # 主要市场
    }
)

print(f"✅ Campaign {result['campaign_id']} launched!")
print(f"   System will auto-optimize for max GMV")
```

**期望效果：**
- Week 1-3：系统学习期，优化受众和商品
- Week 4+：GMV 稳定增长，ROI 优化

### 例子2：按商品分类投放

```python
# 只投放特定品类的商品
result = await creator.create_full_gmvmax_campaign(
    advertiser_id="YOUR_ADVERTISER_ID",
    campaign_name="Women_Fashion_GMVMAX",
    daily_budget=200.0,
    video_id="women_fashion_video",
    shop_id="YOUR_SHOP_ID",
    catalog_id="womens_clothing_catalog",  # 只推女装
    targeting={
        "age": ["18", "45"],
        "gender": ["FEMALE"],  # 只推给女性
    }
)
```

---

## GMVMAX 监控和优化

### 系统自动监控的指标

| 指标 | 说明 |
|------|------|
| **GMV** | 商品销售总额（关键指标） |
| **ROAS** | 广告回报率（花费 vs GMV） |
| **转化率** | 点击转化为购买的比例 |
| **CPA** | 每次转化成本 |
| **商品热度** | 哪些商品销售最好 |

### LLM 优化建议

虽然 GMVMAX 是全自动的，我们的系统也会：

1. **监控数据** — 每30分钟同步一次
2. **异常检测** — 发现 ROAS 下降、GMV 异常等
3. **生成建议** — 基于数据分析，给出优化方向
4. **可选执行** — 你可以选择执行或忽略建议

### 优化建议示例

```
⚠️ 检测到问题：
  - ROAS 从 5:1 下降到 3:1
  - 原因：预算过高，触及低质量人群

💡 建议：
  - 降低日预算 20% (从 $500 → $400)
  - 或扩展初始受众（系统会自动优化）
  - 等待 3-5 天数据稳定

✅ 操作：
  - 自动执行（如置信度 > 80%）
  - 或人工审核后执行
```

---

## GMVMAX 常见问题

### Q1: GMVMAX 需要多长时间学习？
A: 通常 7-14 天，需要足够的数据积累（建议日预算 $50+）。

### Q2: 可以同时运行 GMVMAX 和 Ads 广告吗？
A: 可以。建议不同的预算分配，避免互相竞争。

### Q3: GMVMAX 选不到我想要的商品怎么办？
A: 使用 `catalog_id` 参数，指定商品范围。系统会在范围内自动选择。

### Q4: 如果效果不好怎么办？
A: 
1. 先等待 7-14 天学习期
2. 检查 ad_text 和视频质量（Hook Rate）
3. 扩展受众范围或提高预算
4. 考虑切换回 Ads 模式，手动调整

### Q5: GMVMAX 的出价我能调吗？
A: 不建议。GMVMAX 的出价完全自动化，手动调整会干扰优化。

---

## 总结

**GMVMAX 适合场景：**
✅ TikTok Shop 卖家  
✅ 追求 GMV 最大化  
✅ 愿意让系统全自动优化  
✅ 有足够的预算和耐心等待学习期  

**我们系统的价值：**
✅ 提供 GMVMAX 创建接口  
✅ 自动监控 GMVMAX 效果  
✅ 生成数据驱动的优化建议  
✅ 支持混合策略（GMVMAX + Ads）  

现在你可以在同一个系统中同时使用 **Ads 和 GMVMAX** 两种模式！

---

*最后更新：2026-04-01*
