# 数据架构：取数 → 构建 → 展示

> 核心原则：**前端永远只查 DB，不依赖实时 API**

---

## 当前问题

```
❌ 当前混乱的数据流：

前端页面
  ├── 有的查 DB（campaigns、creatives）
  ├── 有的实时调 TikTok API（shops/list、product enrichment）
  └── 有的混合（creative_dashboard 查 creatives 表但数据不全）

导致：
  - 网络不通 → 页面空白
  - 数据不一致（DB 有 41 个创意，creatives 表只有 3 个）
  - 响应慢（实时 API 超时 30s+）
```

## 目标架构

```
✅ 三层分离：

Layer 1: 同步层（Celery/定时任务）
  TikTok API → 原始数据 → metrics_snapshots / creatives / stores

Layer 2: 构建层（同步完成后触发）
  原始数据 → 聚合/关联/计算 → 业务视图表（新增）

Layer 3: 展示层（API 接口）
  业务视图表 → 前端展示（纯 DB 查询，毫秒级）
```

---

## Layer 1: 同步层（已有）

### 同步任务清单

| 任务 | 数据源 | 写入表 | 频率 |
|------|--------|--------|------|
| sync_gmvmax | `/gmv_max/report/get/` | `metrics_snapshots` (GMVMAX_CAMPAIGN) | 每小时 |
| sync_gmvmax_items | `/gmv_max/report/get/` | `metrics_snapshots` (GMVMAX_ITEM) | 每小时 |
| sync_gmvmax_creatives | `/gmv_max/report/get/` | `metrics_snapshots` (GMVMAX_CREATIVE) | 每小时 |
| sync_creatives | `/gmv_max/video/get/` | `creatives` (视频信息) | 每小时 |
| sync_stores | `/gmv_max/store/list/` | `stores` | 每小时 |
| **sync_products** (待新增) | `/store/product/get/` | **`products`** (待新增) | 每小时 |
| **sync_campaign_names** (待新增) | `/campaign/gmv_max/info/` | `metrics_snapshots.object_name` | 每小时 |

### 同步后触发构建

```python
async def _run_sync_core(...):
    # 1. 同步原始数据
    await sync_stores(...)
    await sync_gmvmax(...)
    await sync_gmvmax_items(...)
    await sync_gmvmax_creatives(...)
    await sync_creatives(...)
    await sync_products(...)        # 新增
    
    # 2. 同步完成后，构建业务视图
    await build_product_view(...)   # 新增
    await build_creative_view(...)  # 新增
    await build_daily_summary(...)  # 新增
```

---

## Layer 2: 构建层（待新增）

### 2.1 商品视图表 `product_view`

> 替代当前实时调 TikTok Shop API 的 `_fetch_product_map()`

```sql
CREATE TABLE product_view (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    item_group_id VARCHAR(128) UNIQUE NOT NULL,
    
    -- 商品信息（从 TikTok Shop API 同步）
    title VARCHAR(512),
    image_url TEXT,
    min_price FLOAT,
    max_price FLOAT,
    currency VARCHAR(8),
    status VARCHAR(32),
    
    -- 关联
    store_id VARCHAR(64),
    advertiser_id VARCHAR(64),
    
    -- 投放指标（从 GMVMAX_ITEM 聚合）
    total_spend FLOAT DEFAULT 0,
    total_orders INT DEFAULT 0,
    total_revenue FLOAT DEFAULT 0,
    roi FLOAT DEFAULT 0,
    active_days INT DEFAULT 0,
    first_seen DATE,
    last_seen DATE,
    
    -- 关联创意数
    creative_count INT DEFAULT 0,
    
    updated_at DATETIME DEFAULT NOW()
);
```

**构建逻辑**：
```python
async def build_product_view(db):
    """同步完成后，合并 TikTok Shop 商品信息 + GMVMAX_ITEM 指标"""
    # 1. 从 stores 表拿 store_id + bc_id
    # 2. 调 get_all_store_products() 拿商品名/图片
    # 3. 从 metrics_snapshots(GMVMAX_ITEM) 聚合花费/订单/GMV
    # 4. UPSERT 到 product_view 表
```

### 2.2 创意视图表 `creative_view`

> 替代当前 `/creatives/gmvmax-creatives` 的实时聚合 + enrichment

```sql
CREATE TABLE creative_view (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    item_id VARCHAR(128) UNIQUE NOT NULL,
    
    -- 商品关联
    item_group_id VARCHAR(128),
    product_name VARCHAR(512),
    product_image_url TEXT,
    
    -- 视频关联（从 creatives 表）
    video_id VARCHAR(128),
    video_url TEXT,
    cover_url TEXT,
    creative_name VARCHAR(512),
    
    -- 投放指标（从 GMVMAX_CREATIVE 聚合）
    advertiser_id VARCHAR(64),
    total_spend FLOAT DEFAULT 0,
    total_orders INT DEFAULT 0,
    total_revenue FLOAT DEFAULT 0,
    total_impressions BIGINT DEFAULT 0,
    total_clicks BIGINT DEFAULT 0,
    roi FLOAT DEFAULT 0,
    
    -- 生命周期
    stage VARCHAR(16),          -- WARM_UP/GROWTH/PEAK/DECAY/FATIGUE/DEAD
    trend VARCHAR(8),           -- up/stable/down
    active_days INT DEFAULT 0,
    first_seen DATE,
    last_seen DATE,
    
    updated_at DATETIME DEFAULT NOW()
);
```

**构建逻辑**：
```python
async def build_creative_view(db):
    """同步完成后，合并 GMVMAX_CREATIVE 指标 + 商品信息 + 视频信息"""
    # 1. 从 metrics_snapshots(GMVMAX_CREATIVE) 聚合
    # 2. 通过 product_id(item_group_id) 关联 product_view 拿商品名/图片
    # 3. 通过 product_id 关联 creatives 表拿视频信息
    # 4. 计算生命周期阶段
    # 5. UPSERT 到 creative_view 表
```

### 2.3 每日汇总表 `daily_summary`

> 替代当前 dashboard/gmvmax-overview 的实时聚合

```sql
CREATE TABLE daily_summary (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    stat_date DATE NOT NULL,
    advertiser_id VARCHAR(64) NOT NULL,
    
    -- Campaign 级汇总
    campaign_count INT DEFAULT 0,
    total_spend FLOAT DEFAULT 0,
    total_revenue FLOAT DEFAULT 0,
    total_orders INT DEFAULT 0,
    roi FLOAT DEFAULT 0,
    
    -- Creative 级汇总
    active_creatives INT DEFAULT 0,
    total_impressions BIGINT DEFAULT 0,
    total_clicks BIGINT DEFAULT 0,
    
    -- 周期对比（构建时计算好）
    spend_vs_yesterday FLOAT,      -- 环比 %
    revenue_vs_yesterday FLOAT,
    roi_vs_yesterday FLOAT,
    spend_vs_last_week FLOAT,      -- 周同比 %
    revenue_vs_last_week FLOAT,
    
    updated_at DATETIME DEFAULT NOW(),
    UNIQUE KEY (stat_date, advertiser_id)
);
```

---

## Layer 3: 展示层

### API 改造对照

| 页面 | 当前数据源 | 改造后数据源 |
|------|-----------|------------|
| 广告看板 | `metrics_snapshots` 实时聚合 | `metrics_snapshots`（已正确） |
| 创意列表 | `metrics_snapshots` + 实时 API enrichment | `creative_view` |
| 创意大盘 | `metrics_snapshots`（已修复） | `metrics_snapshots`（已正确） |
| 店铺管理 | 实时 API + `metrics_snapshots` | `stores` + `metrics_snapshots`（已修复） |
| 商品成本 | `product_costs` + 实时 API | `product_view` + `product_costs` |
| 总览大盘 | `analytics_service` 实时计算 | `daily_summary` |
| GMVMax 大盘 | `metrics_snapshots` 实时聚合 | `daily_summary` |

### 关键原则

1. **前端只查 DB** — 所有 API 接口只读本地表，不调外部 API
2. **同步后构建** — 每次同步完成自动触发视图表更新
3. **兜底机制** — 构建失败不影响展示（用上次构建的数据）
4. **缓存分级** — 内存缓存(5min) → DB视图表 → 磁盘缓存(fallback)

---

## 实施优先级

### Phase 1（立即）
- [x] `stores` 表 — 已完成
- [x] `shop_summary/list` 从 DB 读 — 已完成
- [x] `creative_dashboard` 切到 `metrics_snapshots` — 已完成
- [x] Campaign 名称同步 — 已完成
- [ ] `sync_products` — 同步商品信息到 `product_view` 表

### Phase 2（近期）
- [ ] `product_view` 表 + 构建逻辑
- [ ] `creative_view` 表 + 构建逻辑
- [ ] 创意列表 API 改为查 `creative_view`

### Phase 3（中期）
- [ ] `daily_summary` 表 + 构建逻辑
- [ ] Dashboard / GMVMax 大盘改为查 `daily_summary`
- [ ] 移除所有 API 接口中的实时 TikTok API 调用
