# 操作类型快速参考表

## 所有操作类型速查

| 操作 ID | 操作名称 | 目标级别 | 期望效果 | 观测窗口 | 关键指标 |
|---|---|---|---|---|---|
| **AD_PAUSE** | 暂停广告 | AD | ↓ 花费, ↑ ROAS | 1h | spend, roas, ctr |
| **AD_ENABLE** | 启用广告 | AD | ↑ 花费, ↑ 转化 | 2h | spend, conversion, roas |
| **AD_RAISE_BID** | 提价 | AD | ↑ 展现, ↑ CPC | 2-4h | impression, cpc, click |
| **AD_LOWER_BID** | 降价 | AD | ↓ CPC, ↓ 展现 | 2-4h | cpc, impression, conversion |
| **AD_INCREASE_BUDGET** | 增预算 | AD | ↑ 花费, ↑ 转化 | 3-6h | spend, conversion, roas |
| **AD_DECREASE_BUDGET** | 降预算 | AD | ↓ 花费, ↓ 转化 | 3-6h | spend, roas |
| **ADGROUP_PAUSE** | 暂停广告组 | ADGROUP | ↓ 组花费, 释放预算 | 1-2h | adgroup_spend |
| **ADGROUP_INCREASE_BUDGET** | 增组预算 | ADGROUP | ↑ 总花费, ↑ 总转化 | 3-6h | adgroup_spend, adgroup_conversion |
| **CAMPAIGN_PAUSE** | 暂停 Campaign | CAMPAIGN | ↓ 账户花费, ↑ 账户 ROAS | 2-4h | campaign_spend, account_roas |
| **CAMPAIGN_ADJUST_BUDGET** | 调 Campaign 预算 | CAMPAIGN | 成本控制 | 6h | campaign_spend, campaign_roas |
| **CREATIVE_HEATUP** | 加热素材 | CREATIVE | ↑ 素材花费, ↑ 转化 | 6-12h | creative_spend, creative_conversion, hook_rate |
| **CREATIVE_PAUSE** | 暂停素材 | CREATIVE | 移除疲劳素材 | 4-8h | creative_spend, hook_rate |
| **ACCOUNT_ADJUST_BUDGET** | 调账户预算 | ACCOUNT | 总体成本控制 | 6-12h | account_spend, account_roas |
| **EMERGENCY_STOP** | 紧急止损 | AD/CAMPAIGN | 停止异常 | 1h | anomaly_metric |

---

## 操作成功评价快速判断

### PAUSE / 暂停类

```
✓ 成功：花费减少 + (ROAS 提升 或 保持)
△ 一般：花费减少但 ROAS 下跌
✗ 失败：花费没有减少
```

### ENABLE / 启用和增加类

```
✓ 成功：花费增加 + 转化增加 + ROAS 维持或提升
△ 一般：花费增加 + 转化增加但 ROAS 下跌较多
✗ 失败：花费增加但转化没增加
```

### RAISE_BID / 提价类

```
✓ 成功：展现增加 + 转化增加 + ROAS 维持 (≥ -0.5x)
△ 一般：展现增加但 ROAS 下跌显著
✗ 失败：展现没有增加或大幅下跌
```

### LOWER_BID / 降价类

```
✓ 成功：CPC 下降 + 转化维持 + ROAS 提升
△ 一般：CPC 下降但转化也下降
✗ 失败：CPC 没有下降
```

### HEATUP_CREATIVE / 加热类

```
✓ 成功：转化增加 + ROAS 维持 (≥ -0.2x)
△ 一般：转化增加但 ROAS 下跌
✗ 失败：转化没有增加或下降
```

---

## 关键观测指标及其计算

| 指标 | 计算公式 | 单位 | 说明 |
|---|---|---|---|
| **spend** | 直接采集 | $ | 广告花费 |
| **impression** | 直接采集 | 次 | 展现数 |
| **click** | 直接采集 | 次 | 点击数 |
| **CTR** | click / impression × 100 | % | 点击率 |
| **conversion** | 直接采集 | 次 | 转化数 |
| **conversion_rate** | conversion / click × 100 | % | 转化率 |
| **CPC** | spend / click | $ | 每次点击成本 |
| **CPM** | spend / impression × 1000 | $ | 每千次展现成本 |
| **ROAS** | gmv / spend | 倍 | 投资回报率 |
| **hook_rate** | watched_2s / play_actions × 100 | % | 前 2 秒留存率 |
| **hold_rate** | watched_6s / play_actions × 100 | % | 前 6 秒留存率 |
| **delta_X** | after_X - before_X | 同单位 | 任何指标的变化量 |
| **delta_X_pct** | delta_X / before_X × 100 | % | 百分比变化 |

---

## 评分等级

```
1.0  │ 完美 - 完全符合预期，各项指标向预期方向优化
     │
0.8  │ 优秀 - 大部分指标符合预期
     │
0.6  │ 良好 - 主要目标达成，但有次要指标未如预期
     │
0.4  │ 一般 - 目标部分达成，有明显的权衡
     │
0.2  │ 差 - 目标基本未达成，效果有限
     │
0.0  │ 无效 - 完全无效，无明显改变
     │
-0.5 │ 反向 - 效果与预期完全相反
     │
-1.0 │ 最差 - 严重负面，需要回滚
```

---

## 常见操作组合

### 保守策略（降成本）
```
1. PAUSE_AD              (暂停差的广告)
2. LOWER_BID             (降价测试)
3. DECREASE_BUDGET       (减预算)
4. CAMPAIGN_PAUSE        (暂停整个不赚钱的 Campaign)

期望：总花费 ↓ 20-30%, 整体 ROAS ↑ 5-10%
```

### 增长策略（扩量）
```
1. CREATIVE_HEATUP       (加热好素材)
2. INCREASE_BUDGET       (加预算)
3. RAISE_BID             (提价获得更多展现)
4. ENABLE_AD             (启用好的暂停广告)

期望：总转化 ↑ 30-50%, 花费 ↑ 20-40%, ROAS 维持或略降
```

### 优化策略（提效率）
```
1. PAUSE_CREATIVE        (移除疲劳素材)
2. LOWER_BID             (降价)
3. CREATIVE_HEATUP       (加热新素材)

期望：保持转化不变，花费 ↓ 10-15%, ROAS ↑ 10-15%
```

### 止损策略（紧急）
```
1. EMERGENCY_STOP        (暂停高风险广告)
2. CAMPAIGN_PAUSE        (暂停异常 Campaign)
3. ACCOUNT_ADJUST_BUDGET (降账户总预算)

期望：立即停止异常，最小化损失
```

---

## 常见问题排查

### Q: 暂停广告后花费没有减少？
**A:** 可能是：
- TikTok API 尚未生效（等待 5 分钟）
- 广告有多个副本在运行（需要逐个暂停）
- 触发了某个自动规则导致重启
→ 建议：检查广告状态是否真的改为 PAUSED

### Q: 增加预算后转化没有增加？
**A:** 可能是：
- 已经达到了该素材的流量上限（受众已饱和）
- 素材质量差（Hook Rate 低）
- 竞争激烈，需要同时提价
→ 建议：检查 Hook Rate；考虑轮换素材或提价

### Q: 降价后 CPC 没有下降？
**A:** 可能是：
- 竞争环境改变（其他人也在降价）
- 你的出价仍然高于平台平均
- TikTok 动态定价，实际 CPC 由竞争决定
→ 建议：持续监控；如果 CPC 不动，考虑更激进地降价

### Q: 加热素材后 ROAS 大幅下跌？
**A:** 可能是：
- 预算增加导致获得了质量差的流量
- 竞争激烈，出价被迫上升
- 素材开始疲劳（曝光过多）
→ 建议：检查 Hook Rate 是否下跌；考虑同时降价或轮换新素材

---

## 何时触发各操作

### 何时 PAUSE_AD
- Hook Rate < 1.5%（完全没吸引力）
- ROAS < 保本线 70%（严重亏损）
- CTR < 0.5%（点击率极低）

### 何时 ENABLE_AD
- 修复了导致暂停的问题
- 素材质量重新评估后是好的
- 要测试价格下跌后的效果

### 何时 RAISE_BID
- ROAS > 保本线 150%（非常健康）
- 还有预算，想要更多转化
- 竞争激烈，需要保持排名

### 何时 LOWER_BID
- ROAS < 保本线但 > 70%（略亏）
- 想要降成本同时测试
- 预算压力大

### 何时 INCREASE_BUDGET
- Hook Rate > 60%（高吸引）
- ROAS > 保本线（盈利）
- 投放 2-5 天，数据稳定

### 何时 DECREASE_BUDGET
- ROAS 开始下跌趋势
- 预算分配调整
- 要测试最小可行预算

### 何时 CREATIVE_HEATUP
- Hook Rate > 65%
- 投放 3-7 天
- ROAS > 保本线
- 还有预算余量

### 何时 CREATIVE_PAUSE
- Hook Rate < 1%（疲劳）
- 曝光已经超过 100k（创意疲劳）
- 需要轮换新素材

---

## 数据采集检查清单

执行任何操作前，确保已采集：

- [ ] 花费 (spend)
- [ ] 展现 (impression)
- [ ] 点击 (click)
- [ ] 转化 (conversion)
- [ ] ROAS（或 GMV 用于计算）
- [ ] CPC / CPM（自动计算）
- [ ] 若涉及素材：Hook Rate, Hold Rate
- [ ] 若涉及成本：使用产品 cost config
- [ ] 时间戳（采集时间）

