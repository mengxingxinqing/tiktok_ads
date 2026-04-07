<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">📊 账户大盘</div>
        <div class="page-subtitle">实时监控账户投放状态，关键指标一览无余</div>
      </div>
      <button class="btn btn-ghost" @click="refresh">🔄 刷新</button>
    </div>

    <!-- 核心指标卡片 -->
    <div class="metrics-grid">
      <!-- 花费 -->
      <div class="metric-card">
        <div class="metric-label">💰 花费（今日）</div>
        <div class="metric-value">${{ fmt(overview.current?.spend) }}</div>
        <div class="metric-progress">
          <div class="progress-bar" style="width: 72.5%"></div>
          <span class="progress-text">目标 72.5%</span>
        </div>
      </div>

      <!-- GMV -->
      <div class="metric-card">
        <div class="metric-label">📈 GMV（今日）</div>
        <div class="metric-value">${{ fmt(overview.current?.gmv) }}</div>
        <div class="metric-status" :class="{ 'stat-up': comparisonGmv > 0, 'stat-down': comparisonGmv < 0 }">
          VS 昨日: {{ comparisonGmv > 0 ? '+' : '' }}{{ comparisonGmv }}%
        </div>
      </div>

      <!-- 订单 -->
      <div class="metric-card">
        <div class="metric-label">🛒 订单</div>
        <div class="metric-value">{{ overview.current?.orders || 0 }}</div>
        <div class="metric-sub">{{ fmt(overview.current?.gmv / (overview.current?.orders || 1)) }}/单</div>
      </div>

      <!-- ROI -->
      <div class="metric-card">
        <div class="metric-label">📊 ROAS</div>
        <div class="metric-value" :class="overview.current?.roas > 4.5 ? 'success' : 'warning'">
          {{ (overview.current?.roas || 0).toFixed(2) }}x
        </div>
        <div class="metric-sub">保本线 4.5x</div>
      </div>

      <!-- 真实利润 -->
      <div class="metric-card">
        <div class="metric-label">💹 真实利润</div>
        <div class="metric-value" :class="overview.current?.real_profit > 0 ? 'success' : 'danger'">
          {{ overview.current?.real_profit > 0 ? '+' : '' }}${{ fmt(overview.current?.real_profit) }}
        </div>
        <div class="metric-sub">{{ (overview.current?.real_margin || 0).toFixed(1) }}% 利润率</div>
      </div>

      <!-- 健康度 -->
      <div class="metric-card">
        <div class="metric-label">❤️ 账户健康度</div>
        <div class="health-score" :class="healthScoreClass">{{ overview.current?.health_score || 0 }}</div>
        <div class="metric-sub">{{ overview.current?.risk_level?.toUpperCase() }}</div>
      </div>
    </div>

    <!-- 周期对比 -->
    <div class="card" style="margin-top: 20px">
      <div style="font-weight: 600; margin-bottom: 16px">📊 周期对比</div>
      <div class="comparison-grid">
        <div class="comparison-item">
          <span class="comparison-label">VS 昨日</span>
          <div class="comparison-values">
            <div class="comp-value">
              <span>GMV</span>
              <span :class="{ 'stat-up': comparisonGmv > 0, 'stat-down': comparisonGmv < 0 }">
                {{ comparisonGmv > 0 ? '+' : '' }}{{ comparisonGmv }}%
              </span>
            </div>
            <div class="comp-value">
              <span>ROAS</span>
              <span :class="{ 'stat-up': comparisonRoas > 0, 'stat-down': comparisonRoas < 0 }">
                {{ comparisonRoas > 0 ? '+' : '' }}{{ comparisonRoas }}%
              </span>
            </div>
          </div>
        </div>
        <div class="comparison-item">
          <span class="comparison-label">VS 上周同期</span>
          <div class="comparison-values">
            <div class="comp-value">
              <span>GMV</span>
              <span :class="{ 'stat-up': comparisonLastWeekGmv > 0, 'stat-down': comparisonLastWeekGmv < 0 }">
                {{ comparisonLastWeekGmv > 0 ? '+' : '' }}{{ comparisonLastWeekGmv }}%
              </span>
            </div>
            <div class="comp-value">
              <span>ROAS</span>
              <span :class="{ 'stat-up': comparisonLastWeekRoas > 0, 'stat-down': comparisonLastWeekRoas < 0 }">
                {{ comparisonLastWeekRoas > 0 ? '+' : '' }}{{ comparisonLastWeekRoas }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 预测 -->
    <div class="card" style="margin-top: 20px">
      <div style="font-weight: 600; margin-bottom: 16px">🔮 今日预测（按现有速度外推）</div>
      <div class="forecast-grid">
        <div class="forecast-item">
          <span>预计花费</span>
          <span style="font-weight: 600">${{ fmt(forecast.spend) }}</span>
        </div>
        <div class="forecast-item">
          <span>预计 GMV</span>
          <span style="font-weight: 600">${{ fmt(forecast.gmv) }}</span>
        </div>
        <div class="forecast-item">
          <span>预计利润</span>
          <span style="font-weight: 600; color: var(--success)">${{ fmt(forecast.profit) }}</span>
        </div>
      </div>
    </div>

    <!-- 风险告警 + 止损建议 -->
    <div v-if="risks.length > 0" class="card" style="margin-top: 20px; border-left: 4px solid var(--danger)">
      <div style="font-weight: 600; margin-bottom: 12px; color: var(--danger)">⚠️ 风险告警</div>
      <div style="display: flex; flex-direction: column; gap: 12px">
        <div v-for="risk in risks" :key="risk.type" class="risk-item">
          <div style="display: flex; justify-content: space-between">
            <span style="font-weight: 600">{{ risk.title }}</span>
            <span :class="['badge', `badge-${risk.severity.toLowerCase()}`]">{{ severityLabel(risk.severity) }}</span>
          </div>
          <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px">{{ risk.message }}</div>
          <div v-if="risk.recommended_action" style="font-size: 12px; color: var(--warning); margin-top: 6px">
            💡 建议: {{ actionLabel(risk.recommended_action) }}
          </div>
        </div>
      </div>

      <!-- 止损方案 -->
      <div v-if="showStopLoss && stopLossPlan" style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border)">
        <div style="font-weight: 600; margin-bottom: 12px">🛡️ 止损方案</div>
        <div style="background: var(--bg); padding: 12px; border-radius: 8px; margin-bottom: 12px">
          <div style="font-size: 13px; color: var(--text-muted)">当前状态</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px">
            <div>ROAS: {{ stopLossPlan.current_state.roas.toFixed(2) }}x</div>
            <div :class="stopLossPlan.current_state.real_profit > 0 ? 'stat-up' : 'stat-down'">
              利润: ${{ stopLossPlan.current_state.real_profit.toFixed(2) }}
            </div>
          </div>
        </div>

        <!-- 三个方案卡片 -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px">
          <div v-for="(plan, key) in stopLossPlan.plans" :key="key" class="plan-card">
            <div style="font-weight: 600; font-size: 14px">{{ plan.name }}</div>
            <div style="font-size: 12px; color: var(--text-muted); margin: 6px 0">{{ plan.description }}</div>

            <div style="background: var(--bg); padding: 8px; border-radius: 6px; margin: 8px 0">
              <div style="font-size: 11px; color: var(--text-muted)">预期影响</div>
              <div style="font-size: 12px; margin-top: 4px">
                <div>GMV {{ plan.expected_impact.gmv_change > 0 ? '+' : '' }}{{ plan.expected_impact.gmv_change }}%</div>
                <div>ROAS {{ plan.expected_impact.roas_change > 0 ? '+' : '' }}{{ plan.expected_impact.roas_change }}%</div>
              </div>
            </div>

            <div :class="['badge', riskBadgeClass(plan.risk)]" style="font-size: 10px">
              {{ plan.risk }}
            </div>
          </div>
        </div>

        <div style="margin-top: 12px; padding: 10px; background: var(--info-bg); border-radius: 6px; border-left: 3px solid var(--info)">
          <div style="font-size: 12px">{{ stopLossPlan.note }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, watch } from 'vue'
import { api } from '../api'
import { useGlobalFilterStore } from '../stores/globalFilter'

const globalFilterStore = useGlobalFilterStore()
const globalShopId = inject('globalShopId', ref(''))

const overview = ref({
  current: {},
  comparison: { vs_yesterday: {}, vs_last_week: {} },
  forecast: {},
})
const risks = ref([])
const stopLossPlan = ref(null)
const showStopLoss = ref(false)

const fmt = (v) => Number(v || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const severityLabel = s => ({ CRITICAL: '紧急', WARNING: '警告', INFO: '信息' }[s] || s)
const actionLabel = a => ({ pause: '暂停投放', reduce_budget: '缩减预算', monitor: '持续观察', increase_budget: '增加预算', lower_bid: '降低出价' }[a] || a)

const comparisonGmv = computed(() => overview.value.comparison?.vs_yesterday?.gmv_pct || 0)
const comparisonRoas = computed(() => overview.value.comparison?.vs_yesterday?.roas_pct || 0)
const comparisonLastWeekGmv = computed(() => overview.value.comparison?.vs_last_week?.gmv_pct || 0)
const comparisonLastWeekRoas = computed(() => overview.value.comparison?.vs_last_week?.roas_pct || 0)

const forecast = computed(() => ({
  spend: overview.value.forecast?.estimated_daily_spend || 0,
  gmv: overview.value.forecast?.estimated_daily_gmv || 0,
  profit: overview.value.forecast?.estimated_daily_profit || 0,
}))

const healthScoreClass = computed(() => {
  const score = overview.value.current?.health_score || 0
  if (score >= 70) return 'health-high'
  if (score >= 50) return 'health-medium'
  return 'health-low'
})

// 获取当前广告账户 ID（优先全局筛选器 → localStorage → 第一个活跃账户）
function getAdvertiserId() {
  const shop = globalFilterStore.shops.find(s => s.id === globalShopId.value)
  if (shop?.advertiser_id) return shop.advertiser_id
  if (globalFilterStore.shopId) return globalFilterStore.shopId
  return localStorage.getItem('current_advertiser_id') || 'test'
}

async function load() {
  const advertiserId = getAdvertiserId()

  try {
    overview.value = await api.get(`/analytics/account/${advertiserId}`)
  } catch (e) {
    console.error('Failed to load overview:', e)
  }

  try {
    const data = await api.get(`/analytics/risks/${advertiserId}`)
    risks.value = data.alerts || []
    if (risks.value.length > 0) {
      showStopLoss.value = true
      loadStopLossPlan()
    }
  } catch (e) {
    console.error('Failed to load risks:', e)
  }
}

async function loadStopLossPlan() {
  try {
    const advertiserId = getAdvertiserId()
    stopLossPlan.value = await api.get(`/analytics/stop-loss/${advertiserId}`)
  } catch (e) {
    console.error('Failed to load stop loss plan:', e)
  }
}

function riskBadgeClass(risk) {
  if (risk.includes('低')) return 'badge-info'
  if (risk.includes('中')) return 'badge-warning'
  return 'badge-danger'
}

async function refresh() {
  await load()
}

// 全局店铺切换时重新加载
watch(globalShopId, () => load())
onMounted(load)
</script>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.metric-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
}

.metric-value.success {
  color: var(--success);
}

.metric-value.warning {
  color: var(--warning);
}

.metric-value.danger {
  color: var(--danger);
}

.metric-status,
.metric-sub {
  font-size: 13px;
  color: var(--text-muted);
}

.progress-bar {
  height: 4px;
  background: var(--primary);
  border-radius: 2px;
  margin-bottom: 4px;
}

.progress-text {
  font-size: 12px;
  color: var(--text-muted);
}

.health-score {
  font-size: 48px;
  font-weight: 700;
  text-align: center;
}

.health-high {
  color: var(--success);
}

.health-medium {
  color: var(--warning);
}

.health-low {
  color: var(--danger);
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.comparison-item {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comparison-label {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 600;
}

.comparison-values {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.comp-value {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comp-value span:first-child {
  font-size: 14px;
}

.comp-value span:last-child {
  font-weight: 600;
  font-size: 14px;
}

.stat-up {
  color: var(--success);
}

.stat-down {
  color: var(--danger);
}

.forecast-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.forecast-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px;
  background: var(--bg);
  border-radius: 8px;
  border: 1px solid var(--border);
}

.forecast-item span:first-child {
  font-size: 12px;
  color: var(--text-muted);
}

.risk-item {
  padding: 12px;
  background: var(--bg);
  border-radius: 8px;
  border-left: 3px solid var(--danger);
}

.plan-card {
  padding: 12px;
  background: var(--bg);
  border-radius: 8px;
  border: 1px solid var(--border);
}

.badge-critical {
  background: #fee;
  color: var(--danger);
}

.badge-warning {
  background: #fef3cd;
  color: #856404;
}

.badge-info {
  background: #d1ecf1;
  color: #0c5460;
}
</style>
