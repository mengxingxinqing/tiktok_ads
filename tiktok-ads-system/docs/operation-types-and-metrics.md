# 操作类型与观测指标定义

## 概述

系统支持的所有操作类型、每种操作的预期效果、以及执行前后应该观测的关键指标。

---

## 1️⃣ 广告级操作 (AD Level)

### 1.1 暂停广告 (PAUSE_AD)

**操作描述**：
- 将广告从 ENABLED 改为 PAUSED
- 停止该广告的投放

**触发场景**：
- Hook Rate < 1.5%（极低）
- ROAS < 保本线的 70%（严重亏损）
- CTR < 0.5%（点击率极低）
- 出现异常花费或数据错误

**期望效果**：
- 花费立即下降
- 节省预算成本
- 整体账户 ROAS 提升

**观测指标**：

| 指标 | Before | After | 计算公式 |
|---|---|---|---|
| **花费** | spend_before | spend_after | delta_spend = after - before |
| **展现** | impression_before | impression_after | delta_impression = after - before |
| **点击** | click_before | click_after | delta_click = after - before |
| **转化** | conversion_before | conversion_after | delta_conversion = after - before |
| **CTR** | ctr_before | ctr_after | delta_ctr = after - before (百分比点) |
| **ROAS** | roas_before | roas_after | delta_roas = after - before |
| **CPC** | cpc_before | cpc_after | delta_cpc = after - before |
| **CPM** | cpm_before | cpm_after | delta_cpm = after - before |
| **转化率** | conversion_rate_before | conversion_rate_after | delta_cr = after - before |
| **状态** | status_before (ENABLED) | status_after (PAUSED) | - |

**成功评价**：
```python
if delta_spend < 0:  # 花费确实减少了
    if delta_roas > 0:
        score = 1.0  # 完美：费用减，效率升
    elif delta_roas >= -0.5:
        score = 0.8  # 很好：费用减，效率维持
    else:
        score = 0.5  # 还好：费用减，但效率下跌
else:
    score = -1.0  # 最差：费用没减（操作未生效）
```

**观测窗口**：1小时（应该立即生效）

---

### 1.2 启用广告 (ENABLE_AD)

**操作描述**：
- 将广告从 PAUSED 改为 ENABLED
- 恢复该广告的投放

**触发场景**：
- 素材质量提升（Hook Rate 提高）
- 修复某个配置问题
- 人工审核通过，需要恢复投放

**期望效果**：
- 花费增加
- 获得更多转化
- 扩大盈利规模

**观测指标**：同 PAUSE_AD，但期望方向相反

**成功评价**：
```python
if delta_spend > 0:  # 花费确实增加了
    if delta_conversion > 0:  # 转化也增加了
        if delta_roas >= -0.1:  # ROAS 没大幅下跌
            score = 1.0  # 完美
        else:
            score = 0.6  # 还好（转化增加但效率下跌）
    else:
        score = -0.5  # 差（花费增加但转化没增）
else:
    score = -1.0  # 最差
```

**观测窗口**：2-3小时（需要积累足够流量）

---

### 1.3 调整出价 (ADJUST_BID)

**操作描述**：
- 修改广告的竞价金额
- 可以提价（RAISE_BID）或降价（LOWER_BID）

#### 1.3a 提价 (RAISE_BID)

**操作参数**：
- `new_bid`: 新的出价
- `raise_pct`: 提价百分比（如 10 表示提 10%）

**触发场景**：
- ROAS 健康，想要更多展现
- 竞争激烈，需要提高排名
- 投放阶段是 GROWTH，需要扩量

**期望效果**：
- CPC 上升（竞价更高，被选中的概率上升）
- CPM 上升（更高的竞价报价）
- 展现/点击增加（更多被展示）
- 转化可能增加，但效率下降

**观测指标**：

| 指标 | Before | After | 说明 |
|---|---|---|---|
| **出价** | bid_before | bid_after | 新出价值 |
| **花费** | spend_before | spend_after | 应该增加 |
| **展现** | impression_before | impression_after | 应该增加 |
| **点击** | click_before | click_after | 应该增加 |
| **CPC** | cpc_before | cpc_after | 应该增加（更高出价 = 更高 CPC） |
| **CPM** | cpm_before | cpm_after | 应该增加 |
| **转化** | conversion_before | conversion_after | 可能增加 |
| **ROAS** | roas_before | roas_after | 可能下跌（成本上升） |
| **CTR** | ctr_before | ctr_after | 可能略升 |

**成功评价**：
```python
if delta_bid > 0:  # 出价确实提了
    if delta_click > 0 or delta_impression > 0:  # 流量增加
        if delta_conversion >= -0.1:  # 转化没有负向变化
            if delta_roas >= -0.5:
                score = 0.9  # 优秀
            else:
                score = 0.7  # 良好（流量增但效率下跌）
        else:
            score = 0.3  # 一般（流量增但转化反降）
    else:
        score = -0.5  # 差（出价提了但没带来流量增）
else:
    score = -1.0  # 最差（出价未生效）
```

**观测窗口**：2-4小时

---

#### 1.3b 降价 (LOWER_BID)

**操作参数**：
- `new_bid`: 新的出价
- `lower_pct`: 降价百分比（如 -10 表示降 10%）

**触发场景**：
- ROAS 开始下跌，需要降成本
- 想测试低价格能否维持转化
- 预算紧张，需要降 CPC

**期望效果**：
- CPC 下降（更低出价）
- CPM 下降
- 展现/点击可能减少
- 如果转化维持，则 ROAS 提升

**观测指标**：同提价，但期望方向相反

**成功评价**：
```python
if delta_bid < 0:  # 出价确实降了
    if delta_cpc < 0:  # CPC 也降了
        if delta_conversion >= 0:  # 转化没下跌
            if delta_roas > 0:
                score = 1.0  # 完美
            else:
                score = 0.8  # 很好（成本降，转化维持）
        else:
            score = 0.4  # 一般（成本降但转化减少）
    else:
        score = -0.5  # 差（出价降了但 CPC 没降）
else:
    score = -1.0  # 最差
```

**观测窗口**：2-4小时

---

### 1.4 调整预算 (ADJUST_BUDGET)

**操作描述**：
- 修改广告或广告组的日预算

#### 1.4a 增加预算 (INCREASE_BUDGET)

**操作参数**：
- `new_budget`: 新的日预算
- `increase_pct`: 增加百分比（如 50 表示增 50%）

**触发场景**：
- 素材质量好（Hook Rate > 60%）
- ROAS 健康，想要扩量
- 预算充足，想要最大化转化

**期望效果**：
- 花费增加（预算提高了可用额度）
- 展现/点击/转化可能增加
- ROAS 可能维持或略降（成本增加）

**观测指标**：

| 指标 | Before | After | 说明 |
|---|---|---|---|
| **日预算** | budget_before | budget_after | 新预算 |
| **花费** | spend_before | spend_after | 应该增加（或接近新预算） |
| **展现** | impression_before | impression_after | 应该增加 |
| **点击** | click_before | click_after | 应该增加 |
| **转化** | conversion_before | conversion_after | 应该增加 |
| **ROAS** | roas_before | roas_after | 可能维持或略降 |
| **CPC** | cpc_before | cpc_after | 通常不变（不影响竞价） |
| **CPM** | cpm_before | cpm_after | 通常不变 |

**成功评价**：
```python
if delta_budget > 0:  # 预算确实增加了
    if delta_spend > 0:  # 花费增加
        if delta_conversion > 0:  # 转化也增加
            if delta_roas >= -0.3:  # ROAS 没大幅下跌
                score = 1.0  # 完美
            else:
                score = 0.7  # 良好（转化增但效率下跌明显）
        else:
            score = 0.2  # 差（花费增但转化没增）
    else:
        score = -0.5  # 差（预算增但没花出去）
else:
    score = -1.0
```

**观测窗口**：3-6小时（需要时间消耗预算）

---

#### 1.4b 降低预算 (DECREASE_BUDGET)

**操作参数**：
- `new_budget`: 新的日预算
- `decrease_pct`: 降低百分比（如 -30 表示降 30%）

**触发场景**：
- ROAS 开始下跌，需要降成本
- 预算分配调整，转向高效广告
- 测试最小可行预算

**期望效果**：
- 花费下降（预算减少了上限）
- 展现/点击/转化下降
- 如果单位效率不变，ROAS 应该保持

**观测指标**：同增预算，但期望方向相反

**成功评价**：
```python
if delta_budget < 0:  # 预算确实降了
    if delta_spend < 0:  # 花费减少
        if delta_roas >= -0.1:  # ROAS 维持
            score = 0.9  # 优秀（成本降，效率维持）
        else:
            score = 0.6  # 良好（成本降，效率略降）
    else:
        score = 0  # 预算降但花费没减（可能有其他因素）
else:
    score = -1.0
```

**观测窗口**：3-6小时

---

## 2️⃣ 广告组级操作 (ADGROUP Level)

### 2.1 暂停广告组 (PAUSE_ADGROUP)

**操作描述**：
- 暂停整个广告组下的所有广告
- 同时停止预算消耗

**触发场景**：
- 广告组整体效果差（ROAS < 保本线）
- 某个 Campaign 需要全面调整
- 释放预算给更好的广告组

**观测指标**：

| 指标 | Before | After |
|---|---|---|
| 日总花费 | adgroup_spend_before | adgroup_spend_after |
| 日总转化 | adgroup_conversion_before | adgroup_conversion_after |
| 广告组 ROAS | adgroup_roas_before | adgroup_roas_after |
| 包含广告数 | ad_count_before | ad_count_after (都为 0 或 paused) |
| 预算利用率 | utilization_before | utilization_after (应为 0%) |

**成功评价**：同 PAUSE_AD

---

### 2.2 增加广告组预算 (INCREASE_ADGROUP_BUDGET)

**操作描述**：
- 提高广告组的日预算
- 该组下所有广告共享这个预算

**观测指标**：

| 指标 | Before | After |
|---|---|---|
| 组日预算 | adgroup_budget_before | adgroup_budget_after |
| 实际花费 | adgroup_spend_before | adgroup_spend_after |
| 总展现 | adgroup_impression_before | adgroup_impression_after |
| 总转化 | adgroup_conversion_before | adgroup_conversion_after |
| 组 ROAS | adgroup_roas_before | adgroup_roas_after |

---

## 3️⃣ Campaign 级操作 (CAMPAIGN Level)

### 3.1 暂停 Campaign (PAUSE_CAMPAIGN)

**操作描述**：
- 暂停整个 Campaign 及其下所有广告组和广告

**触发场景**：
- Campaign 整体不盈利
- 产品下架或营销活动结束
- 准备重新规划

**观测指标**：

| 指标 | Before | After |
|---|---|---|
| Campaign 日花费 | campaign_spend_before | campaign_spend_after |
| Campaign 日转化 | campaign_conversion_before | campaign_conversion_after |
| Campaign ROAS | campaign_roas_before | campaign_roas_after |
| 账户总花费 | account_spend_before | account_spend_after |
| 账户总 ROAS | account_roas_before | account_roas_after |

**成功评价**：
```python
if delta_campaign_spend < 0:  # Campaign 花费减少
    if account_roas_after > account_roas_before:  # 账户整体 ROAS 提升
        score = 1.0  # 完美（移除了拖累，账户效率提升）
    else:
        score = 0.7  # 很好（虽然账户整体未升，但节省了成本）
else:
    score = -1.0
```

---

### 3.2 调整 Campaign 预算 (ADJUST_CAMPAIGN_BUDGET)

**操作描述**：
- 修改 Campaign 的日预算上限

**观测指标**：同 ADGROUP 级别的预算调整

---

## 4️⃣ 素材级操作 (CREATIVE Level)

### 4.1 加热素材 (HEATUP_CREATIVE)

**操作描述**：
- 增加含有该素材的广告的预算或出价
- 或创建新 Ad 复用该素材

**触发场景**：
- Hook Rate > 60%（高吸引）
- 投放 2-5 天，数据稳定
- ROAS > 保本线，想要扩量

**期望效果**：
- 该素材的花费增加
- 转化增加
- ROAS 可能维持或略降（成本上升）

**观测指标**：

| 指标 | Before | After | 说明 |
|---|---|---|---|
| **素材日花费** | creative_spend_before | creative_spend_after | 应该增加 |
| **素材日转化** | creative_conversion_before | creative_conversion_after | 应该增加 |
| **素材 ROAS** | creative_roas_before | creative_roas_after | 可能维持或略降 |
| **Hook Rate** | hook_rate_before | hook_rate_after | 应该维持（素材本身没变） |
| **Hold Rate** | hold_rate_before | hold_rate_after | 应该维持 |
| **生命周期** | lifecycle_before | lifecycle_after | 可能从 GROWTH → PEAK |

**成功评价**：
```python
if delta_spend > 0:  # 花费增加
    if delta_conversion > 0:  # 转化也增加
        if delta_roas >= -0.2:  # ROAS 没大幅下跌
            score = 0.9  # 优秀
        else:
            score = 0.6  # 良好（转化增但效率下跌）
    else:
        score = 0.2  # 差（花费增但转化没增）
else:
    score = 0  # 加热未生效
```

**观测窗口**：6-12小时

---

### 4.2 暂停素材 (PAUSE_CREATIVE)

**操作描述**：
- 暂停所有使用该素材的广告

**触发场景**：
- Hook Rate 跌至 < 1%（完全疲劳）
- 曝光过多，审美疲劳
- 需要轮换新素材

**观测指标**：

| 指标 | Before | After |
|---|---|---|
| 素材花费 | creative_spend_before | creative_spend_after |
| 素材转化 | creative_conversion_before | creative_conversion_after |
| 素材使用中的 Ad 数 | ad_count_before | ad_count_after (应为 0) |
| 素材 Hook Rate | hook_rate_before | hook_rate_after |

---

## 5️⃣ 账户级操作 (ACCOUNT Level)

### 5.1 调整账户花费上限 (ADJUST_ACCOUNT_BUDGET)

**操作描述**：
- 改变整个账户的日花费上限

**观测指标**：

| 指标 | Before | After | 说明 |
|---|---|---|---|
| 账户日预算 | account_budget_before | account_budget_after | - |
| 账户日花费 | account_spend_before | account_spend_after | 应接近新预算 |
| 账户日转化 | account_conversion_before | account_conversion_after | 对应花费变化 |
| 账户 ROAS | account_roas_before | account_roas_after | 应维持在相似水平 |

---

## 6️⃣ 特殊操作

### 6.1 紧急止损 (EMERGENCY_STOP)

**操作描述**：
- 快速暂停高风险广告或整个账户
- 用于应对异常（如诈骗流量、故障等）

**触发场景**：
- ROAS 突然暴跌 (< 0.5x)
- 花费异常增长（1小时内翻倍）
- 检测到可疑的点击/转化模式

**观测指标**：

| 指标 | Before | After |
|---|---|---|
| 花费 | spend_before | spend_after |
| 异常指标 | anomaly_metric_before | anomaly_metric_after |
| 恢复时间 | - | time_to_recovery |

**成功评价**：
- 任何成功止住异常增长都算成功
- score = 1.0（优先级最高）

---

## 📊 完整观测指标清单

### 基础指标（所有操作都需要）
```
花费 (spend)
展现 (impression)
点击 (click)
CTR (ctr) = click / impression * 100%
转化 (conversion)
转化率 (conversion_rate) = conversion / click * 100%
ROAS (roas) = gmv / spend
CPC (cpc) = spend / click
CPM (cpm) = spend / impression * 1000
```

### 素材相关指标（只需在素材操作时观测）
```
Hook Rate (hook_rate) = watched_2s / play_actions * 100%
Hold Rate (hold_rate) = watched_6s / play_actions * 100%
平均播放时长 (avg_play_duration)
完播率 (completion_rate)
生命周期 (lifecycle_stage)
```

### 财务相关指标（成本关联操作）
```
实收 GMV (net_gmv)
真实利润 (real_profit)
真实 ROI (real_roi)
保本 ROAS (break_even_roas)
```

---

## 🎯 观测窗口指南

| 操作类型 | 观测窗口 | 说明 |
|---|---|---|
| PAUSE_AD / ENABLE_AD | 1-2h | 流量变化快速 |
| ADJUST_BID (提/降价) | 2-4h | 需要竞价系统反应 |
| ADJUST_BUDGET | 3-6h | 需要时间消耗预算 |
| HEATUP_CREATIVE | 6-12h | 需要数据积累 |
| PAUSE_CREATIVE | 4-8h | 需要足够数据 |
| Campaign / Account 级 | 12-24h | 大规模变化需更长观测 |

---

## 📝 实现规范

### 数据库记录

每次操作都应记录在 `DecisionImpact` 或 `CreativeHeatUp` 表中：

```python
{
    decision_type: str,          # PAUSE_AD, INCREASE_BUDGET 等
    target_level: str,           # AD, ADGROUP, CAMPAIGN, CREATIVE, ACCOUNT
    target_id: str,              # 具体的 ID
    
    before_metrics: {            # 操作前的所有指标
        'spend': float,
        'impression': int,
        'click': int,
        'conversion': int,
        'roas': float,
        'cpc': float,
        'ctr': float,
        ... 其他指标
    },
    
    after_metrics: {             # 操作后的指标
        ... 同 before_metrics
    },
    
    deltas: {                    # 自动计算的变化量
        'spend_delta': float,
        'conversion_delta': int,
        'roas_delta': float,
        'roas_delta_pct': float,
        ... 其他变化
    },
    
    evaluation: {                # 自动评估结果
        'is_successful': bool,
        'success_score': float,  # 0.0 ~ 1.0
        'reason': str,
    },
}
```

### 前端展示

所有操作效果应在统一的"决策评估"页面展示：

```
┌─ 决策类型别 (PAUSE_AD, INCREASE_BUDGET 等)
│  ├─ 执行次数
│  ├─ 成功率
│  ├─ 平均评分
│  └─ 代表案例（最好 / 最差）
└─ 可逐个查看每次操作的对比数据
```

---

## ✅ 总结

**操作分类**：
- **广告级** (5 种)：暂停、启用、提价、降价、调预算
- **广告组级** (3 种)：暂停、调预算、......
- **Campaign 级** (2 种)：暂停、调预算
- **素材级** (2 种)：加热、暂停
- **账户级** (1 种)：调花费上限
- **特殊** (1 种)：紧急止损

**总共 14+ 种操作**，每种都有明确的：
- ✓ 触发条件
- ✓ 期望效果
- ✓ 观测指标 (15~20 项)
- ✓ 成功评价标准
- ✓ 观测窗口

