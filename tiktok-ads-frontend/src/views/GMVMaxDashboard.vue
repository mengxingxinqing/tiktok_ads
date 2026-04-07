<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">🚀 GMVMax 大盘</div>
        <div class="page-subtitle">GMVMax 投放核心指标 · ROI 趋势 · Campaign 对比</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <select v-model="days" @change="load" style="width:100px">
          <option value="7">近7天</option>
          <option value="14">近14天</option>
          <option value="30">近30天</option>
        </select>
        <button class="btn btn-primary" @click="syncNow" :disabled="syncing">
          {{ syncing ? '⏳ 同步中...' : '🔄 同步' }}
        </button>
      </div>
    </div>

    <!-- 核心指标卡片 -->
    <div class="kpi-grid">
      <div class="kpi-card" v-for="kpi in kpis" :key="kpi.label">
        <div class="kpi-label">{{ kpi.icon }} {{ kpi.label }}</div>
        <div class="kpi-value" :class="kpi.cls">{{ kpi.value }}</div>
        <div class="kpi-delta" v-if="kpi.delta !== null" :class="kpi.delta >= 0 ? 'up' : 'down'">
          {{ kpi.delta >= 0 ? '▲' : '▼' }} {{ Math.abs(kpi.delta).toFixed(1) }}% vs 昨日
        </div>
      </div>
    </div>

    <!-- ROI 告警 banner -->
    <div v-if="roiAlert" class="alert-banner" :class="roiAlert.cls">
      {{ roiAlert.icon }} {{ roiAlert.message }}
    </div>

    <!-- 趋势图 + Campaign 表 并排 -->
    <div class="two-col-layout">

      <!-- 左：趋势折线（简易条形模拟） -->
      <div class="card">
        <div class="card-header">
          <span>📈 趋势</span>
          <div style="display:flex;gap:6px">
            <button
              v-for="m in trendMetrics" :key="m.key"
              :class="['metric-btn', { active: activeTrend === m.key }]"
              @click="activeTrend = m.key"
            >{{ m.label }}</button>
          </div>
        </div>

        <div v-if="!overview.trend?.length" class="empty-state" style="padding:40px 0">
          <div class="empty-icon">📊</div>
          <div>暂无数据，先同步</div>
        </div>
        <div v-else>
          <!-- 数值趋势表格 -->
          <table style="font-size:12px">
            <thead>
              <tr>
                <th>日期</th>
                <th>花费</th>
                <th>GMV</th>
                <th>订单</th>
                <th>ROI</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in overview.trend" :key="row.date"
                :class="{ 'row-critical': row.roi < 1 && row.spend > 0 }">
                <td>{{ row.date.slice(5) }}</td>
                <td>${{ fmt(row.spend) }}</td>
                <td :class="row.gmv > row.spend * 4 ? 'good' : ''">
                  ${{ fmt(row.gmv) }}
                </td>
                <td>{{ row.orders }}</td>
                <td :class="roiClass(row.roi)">
                  {{ row.roi ? row.roi.toFixed(2) + 'x' : '-' }}
                </td>
              </tr>
            </tbody>
          </table>

          <!-- 简易 bar chart -->
          <div class="mini-chart">
            <div
              v-for="row in overview.trend" :key="'b'+row.date"
              class="bar-group"
            >
              <div class="bar spend-bar" :style="{ height: barH(row, 'spend') + 'px' }" :title="`花费: $${fmt(row.spend)}`"></div>
              <div class="bar gmv-bar" :style="{ height: barH(row, 'gmv') + 'px' }" :title="`GMV: $${fmt(row.gmv)}`"></div>
              <div class="bar-label">{{ row.date.slice(8) }}</div>
            </div>
          </div>
          <div class="chart-legend">
            <span class="legend-item spend">■ 花费</span>
            <span class="legend-item gmv">■ GMV</span>
          </div>
        </div>
      </div>

      <!-- 右：Campaign 排行 -->
      <div class="card">
        <div class="card-header">🎯 Campaign 排行（ROI 降序）</div>

        <div v-if="!overview.top_campaigns?.length" class="empty-state" style="padding:40px 0">
          <div class="empty-icon">📋</div>
          <div>暂无 Campaign 数据</div>
        </div>
        <div v-else>
          <div v-for="c in overview.top_campaigns" :key="c.campaign_id" class="campaign-row">
            <div class="campaign-head">
              <span class="campaign-id">{{ c.campaign_id }}</span>
              <span class="roi-badge" :class="roiClass(c.roi)">
                ROI {{ c.roi ? c.roi.toFixed(2) + 'x' : '-' }}
              </span>
            </div>
            <div class="campaign-metrics">
              <span>💰 ${{ fmt(c.spend) }}</span>
              <span>📈 ${{ fmt(c.gmv) }}</span>
              <span>🛒 {{ c.orders }} 单</span>
            </div>
            <!-- ROI 进度条 -->
            <div class="roi-bar-bg">
              <div
                class="roi-bar-fill"
                :style="{ width: Math.min((c.roi || 0) / 10 * 100, 100) + '%' }"
                :class="roiClass(c.roi)"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 今日 vs 昨日 vs 7日均值 对比 -->
    <div class="card">
      <div class="card-header">📊 周期对比</div>
      <div class="comparison-table">
        <table>
          <thead>
            <tr>
              <th>指标</th>
              <th>今日</th>
              <th>昨日</th>
              <th>7日均值</th>
              <th>今日 vs 昨日</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in comparisonRows" :key="row.label">
              <td>{{ row.label }}</td>
              <td style="font-weight:600">{{ row.today }}</td>
              <td style="color:var(--text-muted)">{{ row.yesterday }}</td>
              <td style="color:var(--text-muted)">{{ row.avg7d }}</td>
              <td :class="row.delta >= 0 ? 'up' : 'down'">
                {{ row.delta >= 0 ? '▲' : '▼' }} {{ Math.abs(row.delta).toFixed(1) }}%
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'

const days = ref('7')
const syncing = ref(false)
const overview = ref({})

const trendMetrics = [
  { key: 'roi', label: 'ROI' },
  { key: 'gmv', label: 'GMV' },
  { key: 'spend', label: '花费' },
]
const activeTrend = ref('roi')

// ── helpers ────────────────────────────────────────────
const fmt = v => v ? Number(v).toFixed(2) : '0.00'

const roiClass = roi => {
  if (!roi || roi === 0) return ''
  if (roi >= 5) return 'excellent'
  if (roi >= 3) return 'good'
  if (roi >= 1) return 'warning'
  return 'danger'
}

const delta = (a, b) => b > 0 ? ((a - b) / b * 100) : 0

// 趋势图 bar 高度归一化
const barH = (row, field) => {
  const max = Math.max(...(overview.value.trend || []).map(r => r[field] || 0))
  if (!max) return 0
  return Math.round((row[field] || 0) / max * 80)
}

// ── computed ───────────────────────────────────────────
const kpis = computed(() => {
  const t = overview.value.today || {}
  const y = overview.value.yesterday || {}
  const roiVal = t.spend > 0 ? (t.gmv / t.spend) : 0
  const roiYest = y.spend > 0 ? (y.gmv / y.spend) : 0

  return [
    {
      label: '花费', icon: '💰', cls: '',
      value: `$${fmt(t.spend)}`,
      delta: delta(t.spend, y.spend),
    },
    {
      label: 'GMV', icon: '📈', cls: t.gmv > t.spend * 4 ? 'good' : '',
      value: `$${fmt(t.gmv)}`,
      delta: delta(t.gmv, y.gmv),
    },
    {
      label: '订单', icon: '🛒', cls: '',
      value: t.orders || 0,
      delta: delta(t.orders, y.orders),
    },
    {
      label: 'ROI', icon: '📊', cls: roiClass(roiVal),
      value: roiVal ? roiVal.toFixed(2) + 'x' : '-',
      delta: delta(roiVal, roiYest),
    },
    {
      label: '客单价', icon: '🎯', cls: '',
      value: t.orders > 0 ? `$${fmt(t.gmv / t.orders)}` : '-',
      delta: null,
    },
    {
      label: '单笔成本', icon: '💸', cls: '',
      value: t.orders > 0 ? `$${fmt(t.spend / t.orders)}` : '-',
      delta: delta(
        t.orders > 0 ? t.spend / t.orders : 0,
        y.orders > 0 ? y.spend / y.orders : 0
      ),
    },
  ]
})

const roiAlert = computed(() => {
  const t = overview.value.today || {}
  const roi = t.spend > 0 ? t.gmv / t.spend : null
  if (roi === null) return null
  if (roi < 1 && t.spend > 5) return { cls: 'critical', icon: '🚨', message: `ROI ${roi.toFixed(2)}x — 当前投放亏损，请立即检查！` }
  if (roi < 2 && t.spend > 20) return { cls: 'warning', icon: '⚠️', message: `ROI ${roi.toFixed(2)}x — 低于保本线，建议暂停优化` }
  return null
})

const comparisonRows = computed(() => {
  const t = overview.value.today || {}
  const y = overview.value.yesterday || {}
  const avg = overview.value.last_7d || {}
  const tRoi = t.spend > 0 ? t.gmv / t.spend : 0
  const yRoi = y.spend > 0 ? y.gmv / y.spend : 0
  const aRoi = avg.spend > 0 ? avg.gmv / avg.spend : 0

  return [
    { label: '💰 花费', today: `$${fmt(t.spend)}`, yesterday: `$${fmt(y.spend)}`, avg7d: `$${fmt(avg.spend)}`, delta: delta(t.spend, y.spend) },
    { label: '📈 GMV', today: `$${fmt(t.gmv)}`, yesterday: `$${fmt(y.gmv)}`, avg7d: `$${fmt(avg.gmv)}`, delta: delta(t.gmv, y.gmv) },
    { label: '🛒 订单', today: t.orders || 0, yesterday: y.orders || 0, avg7d: fmt(avg.orders), delta: delta(t.orders, y.orders) },
    { label: '📊 ROI', today: tRoi ? tRoi.toFixed(2)+'x' : '-', yesterday: yRoi ? yRoi.toFixed(2)+'x' : '-', avg7d: aRoi ? aRoi.toFixed(2)+'x' : '-', delta: delta(tRoi, yRoi) },
  ]
})

// ── loaders ────────────────────────────────────────────
async function load() {
  try {
    const data = await api.get('/dashboard/gmvmax-overview', { params: { days: days.value } })
    overview.value = data
  } catch (e) {
    console.error('GMVMax overview failed:', e)
    overview.value = {}
  }
}

async function syncNow() {
  syncing.value = true
  try {
    await api.post('/admin/sync/trigger')
    setTimeout(async () => {
      await load()
      syncing.value = false
    }, 5000)
  } catch {
    syncing.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}
@media (max-width: 1200px) { .kpi-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }

.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
}
.kpi-label { font-size: 12px; color: var(--text-muted); margin-bottom: 8px; }
.kpi-value { font-size: 22px; font-weight: 700; color: var(--text); }
.kpi-delta { font-size: 11px; margin-top: 6px; }
.kpi-delta.up { color: var(--success); }
.kpi-delta.down { color: var(--danger); }

.kpi-value.excellent { color: #10b981; }
.kpi-value.good { color: #34d399; }
.kpi-value.warning { color: #f59e0b; }
.kpi-value.danger { color: var(--danger); }

.alert-banner {
  padding: 12px 16px;
  border-radius: var(--radius);
  margin-bottom: 16px;
  font-size: 14px;
  font-weight: 500;
}
.alert-banner.critical { background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.4); color: #ef4444; }
.alert-banner.warning { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); color: #f59e0b; }

.two-col-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
@media (max-width: 900px) { .two-col-layout { grid-template-columns: 1fr; } }

.metric-btn {
  padding: 3px 10px; border-radius: 4px; border: 1px solid var(--border);
  background: transparent; color: var(--text-muted); font-size: 11px; cursor: pointer;
}
.metric-btn.active { background: var(--primary); color: white; border-color: var(--primary); }

table { width: 100%; border-collapse: collapse; }
th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); font-size: 13px; }
th { color: var(--text-muted); font-size: 11px; font-weight: 600; }
.row-critical td { background: rgba(239,68,68,0.08); }
td.good { color: var(--success); font-weight: 600; }
td.up { color: var(--success); }
td.down { color: var(--danger); }

.mini-chart {
  display: flex; align-items: flex-end; gap: 4px;
  height: 100px; padding: 8px 0 0; border-top: 1px solid var(--border); margin-top: 12px;
}
.bar-group { display: flex; align-items: flex-end; gap: 2px; flex: 1; flex-direction: column; }
.bar { width: 100%; min-height: 2px; border-radius: 2px 2px 0 0; transition: height 0.3s; }
.bar-group { align-items: flex-end; flex-direction: row; position: relative; padding-bottom: 18px; }
.bar-label { position: absolute; bottom: 0; width: 100%; text-align: center; font-size: 10px; color: var(--text-muted); }
.spend-bar { background: var(--primary); }
.gmv-bar { background: var(--success); }
.chart-legend { display: flex; gap: 16px; font-size: 11px; padding: 8px 0; }
.legend-item { color: var(--text-muted); }
.legend-item.spend { color: var(--primary); }
.legend-item.gmv { color: var(--success); }

.campaign-row { padding: 12px 0; border-bottom: 1px solid var(--border); }
.campaign-row:last-child { border-bottom: none; }
.campaign-head { display: flex; justify-content: space-between; margin-bottom: 6px; }
.campaign-id { font-size: 12px; color: var(--text-muted); font-family: monospace; }
.roi-badge { font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 4px; }
.roi-badge.excellent { background: rgba(16,185,129,0.15); color: #10b981; }
.roi-badge.good { background: rgba(52,211,153,0.15); color: #34d399; }
.roi-badge.warning { background: rgba(245,158,11,0.15); color: #f59e0b; }
.roi-badge.danger { background: rgba(239,68,68,0.15); color: #ef4444; }
.campaign-metrics { display: flex; gap: 16px; font-size: 12px; color: var(--text-muted); margin-bottom: 8px; }
.roi-bar-bg { height: 4px; background: var(--border); border-radius: 2px; }
.roi-bar-fill { height: 4px; border-radius: 2px; transition: width 0.5s; }
.roi-bar-fill.excellent { background: #10b981; }
.roi-bar-fill.good { background: #34d399; }
.roi-bar-fill.warning { background: #f59e0b; }
.roi-bar-fill.danger { background: #ef4444; }

.comparison-table table { font-size: 13px; }
.comparison-table td.up { color: var(--success); }
.comparison-table td.down { color: var(--danger); }
</style>
