<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">📡 渠道分析</div>
        <div class="page-subtitle">渠道号 vs 达人号 · 来源拆分 · 佣金分析</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <select v-model="filter.days" @change="load" style="width:100px">
          <option value="7">近7天</option>
          <option value="14">近14天</option>
          <option value="30">近30天</option>
        </select>
        <button class="btn btn-ghost" @click="load">🔄 刷新</button>
      </div>
    </div>

    <!-- 总体对比卡片 -->
    <div class="compare-grid">
      <!-- 总体 -->
      <div class="channel-card total">
        <div class="channel-label">📊 总体 GMV</div>
        <div class="channel-value">${{ fmt(overview.total?.gmv) }}</div>
        <div class="channel-sub">{{ overview.total?.orders || 0 }} 单 · 客单价 ${{ fmtAvg(overview.total?.gmv, overview.total?.orders) }}</div>
      </div>

      <!-- 渠道号 SELF_OWNED -->
      <div class="channel-card self-owned">
        <div class="channel-label">🏬 渠道号（自有）</div>
        <div class="channel-value">${{ fmt(overview.self_owned?.gmv) }}</div>
        <div class="pct-bar-bg">
          <div class="pct-bar self" :style="{ width: selfPct + '%' }"></div>
        </div>
        <div class="channel-sub">
          {{ overview.self_owned?.orders || 0 }} 单 · 占比
          <span class="pct-badge self">{{ selfPct.toFixed(1) }}%</span>
        </div>
      </div>

      <!-- 达人号 AFFILIATE -->
      <div class="channel-card affiliate">
        <div class="channel-label">⭐ 达人号（联盟）</div>
        <div class="channel-value">${{ fmt(overview.affiliate?.gmv) }}</div>
        <div class="pct-bar-bg">
          <div class="pct-bar affiliate" :style="{ width: affiliatePct + '%' }"></div>
        </div>
        <div class="channel-sub">
          {{ overview.affiliate?.orders || 0 }} 单 · 占比
          <span class="pct-badge affiliate">{{ affiliatePct.toFixed(1) }}%</span>
        </div>
        <div v-if="overview.affiliate?.commission_amount > 0" class="commission-info">
          💸 佣金支出 ${{ fmt(overview.affiliate?.commission_amount) }}
        </div>
      </div>
    </div>

    <!-- 趋势对比 + 达人排行 -->
    <div class="two-col">

      <!-- 左：趋势 -->
      <div class="card">
        <div class="card-header">📈 每日来源趋势</div>
        <div v-if="!overview.trend?.length" class="empty-state" style="padding:40px 0">
          <div class="empty-icon">📊</div>
          <div>暂无趋势数据</div>
        </div>
        <div v-else>
          <table style="font-size:12px">
            <thead>
              <tr>
                <th>日期</th>
                <th>渠道号 GMV</th>
                <th>达人号 GMV</th>
                <th>总 GMV</th>
                <th>达人占比</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in overview.trend" :key="row.date">
                <td>{{ row.date.slice(5) }}</td>
                <td>${{ fmt(row.self_owned_gmv) }}</td>
                <td :class="row.affiliate_gmv > row.self_owned_gmv ? 'highlight' : ''">
                  ${{ fmt(row.affiliate_gmv) }}
                </td>
                <td style="font-weight:600">${{ fmt(row.total_gmv) }}</td>
                <td>
                  <div class="mini-bar-bg">
                    <div class="mini-bar" :style="{ width: pctOf(row.affiliate_gmv, row.total_gmv) + '%' }"></div>
                  </div>
                  <span style="font-size:10px;color:var(--text-muted)">{{ pctOf(row.affiliate_gmv, row.total_gmv).toFixed(0) }}%</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 右：达人排行 -->
      <div class="card">
        <div class="card-header">⭐ 达人贡献排行</div>
        <div v-if="!affiliates.length" class="empty-state" style="padding:40px 0">
          <div class="empty-icon">👤</div>
          <div>暂无达人数据</div>
        </div>
        <div v-else>
          <div v-for="(aff, i) in affiliates" :key="aff.affiliate_id" class="affiliate-row">
            <div class="aff-rank" :class="i < 3 ? 'top' : ''">{{ i + 1 }}</div>
            <div class="aff-info">
              <div class="aff-name">{{ aff.affiliate_name || aff.affiliate_id }}</div>
              <div class="aff-id">ID: {{ aff.affiliate_id }}</div>
            </div>
            <div class="aff-metrics">
              <div class="aff-gmv">${{ fmt(aff.gmv) }}</div>
              <div class="aff-sub">{{ aff.orders }} 单 · 佣金 ${{ fmt(aff.commission_amount) }}</div>
              <div class="aff-commission-rate" v-if="aff.commission_rate">
                佣金率 {{ (aff.commission_rate * 100).toFixed(1) }}%
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 渠道号 vs 达人号 详细对比 -->
    <div class="card">
      <div class="card-header">📊 渠道号 vs 达人号 详细对比</div>
      <div v-if="!compare.self_owned && !compare.affiliate" class="empty-state" style="padding:30px 0">
        <div>暂无对比数据</div>
      </div>
      <div v-else class="compare-table">
        <table>
          <thead>
            <tr>
              <th>指标</th>
              <th>🏬 渠道号</th>
              <th>⭐ 达人号</th>
              <th>对比</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in compareRows" :key="row.label">
              <td>{{ row.label }}</td>
              <td>{{ row.self }}</td>
              <td>{{ row.aff }}</td>
              <td :class="row.winner === 'self' ? 'self-win' : row.winner === 'aff' ? 'aff-win' : ''">
                {{ row.winner === 'self' ? '🏬 渠道号更优' : row.winner === 'aff' ? '⭐ 达人号更优' : '—' }}
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
import { useGlobalFilterStore } from '../stores/globalFilter'

const globalFilter = useGlobalFilterStore()
const filter = ref({ days: '7' })
const overview = ref({})
const affiliates = ref([])
const compare = ref({})

const fmt = v => v ? Number(v).toFixed(2) : '0.00'
const fmtAvg = (total, count) => count > 0 ? (total / count).toFixed(2) : '0.00'
const pctOf = (a, b) => b > 0 ? (a / b * 100) : 0

const selfPct = computed(() => {
  const total = overview.value.total?.gmv || 0
  const self = overview.value.self_owned?.gmv || 0
  return total > 0 ? (self / total * 100) : 0
})

const affiliatePct = computed(() => {
  const total = overview.value.total?.gmv || 0
  const aff = overview.value.affiliate?.gmv || 0
  return total > 0 ? (aff / total * 100) : 0
})

const compareRows = computed(() => {
  const s = compare.value.self_owned || {}
  const a = compare.value.affiliate || {}
  return [
    {
      label: '📈 GMV',
      self: `$${fmt(s.gmv)}`,
      aff: `$${fmt(a.gmv)}`,
      winner: (s.gmv || 0) > (a.gmv || 0) ? 'self' : (a.gmv || 0) > (s.gmv || 0) ? 'aff' : '',
    },
    {
      label: '🛒 订单数',
      self: s.orders || 0,
      aff: a.orders || 0,
      winner: (s.orders || 0) > (a.orders || 0) ? 'self' : (a.orders || 0) > (s.orders || 0) ? 'aff' : '',
    },
    {
      label: '💰 客单价',
      self: `$${fmtAvg(s.gmv, s.orders)}`,
      aff: `$${fmtAvg(a.gmv, a.orders)}`,
      winner: fmtAvg(s.gmv, s.orders) > fmtAvg(a.gmv, a.orders) ? 'self' : 'aff',
    },
    {
      label: '💸 佣金支出',
      self: '-',
      aff: `$${fmt(a.commission_total)}`,
      winner: '',
    },
    {
      label: '📊 净 GMV（扣佣金）',
      self: `$${fmt(s.gmv)}`,
      aff: `$${fmt((a.gmv || 0) - (a.commission_total || 0))}`,
      winner: (s.gmv || 0) > ((a.gmv || 0) - (a.commission_total || 0)) ? 'self' : 'aff',
    },
  ]
})

async function load() {
  const params = { days: filter.value.days }
  if (globalFilter.shopId) params.shop_id = globalFilter.shopId

  try {
    const [ov, affs, cmp] = await Promise.all([
      api.get('/channel/overview', { params }),
      api.get('/channel/affiliates', { params }),
      api.get('/channel/compare', { params }),
    ])
    overview.value = ov
    affiliates.value = affs.affiliates || affs || []
    compare.value = cmp
  } catch (e) {
    console.error('Channel analysis load failed:', e)
  }
}

onMounted(load)
</script>

<style scoped>
.compare-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
@media (max-width: 900px) { .compare-grid { grid-template-columns: 1fr; } }

.channel-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
}
.channel-card.total { border-color: var(--primary); }
.channel-card.self-owned { border-color: #3b82f6; }
.channel-card.affiliate { border-color: #f59e0b; }

.channel-label { font-size: 12px; color: var(--text-muted); margin-bottom: 8px; }
.channel-value { font-size: 28px; font-weight: 700; margin-bottom: 10px; }
.channel-sub { font-size: 12px; color: var(--text-muted); margin-top: 8px; }
.commission-info { font-size: 12px; color: #f59e0b; margin-top: 6px; }

.pct-bar-bg { height: 6px; background: var(--border); border-radius: 3px; margin: 8px 0; }
.pct-bar.self { height: 6px; background: #3b82f6; border-radius: 3px; transition: width 0.5s; }
.pct-bar.affiliate { height: 6px; background: #f59e0b; border-radius: 3px; transition: width 0.5s; }

.pct-badge { padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; }
.pct-badge.self { background: rgba(59,130,246,0.2); color: #3b82f6; }
.pct-badge.affiliate { background: rgba(245,158,11,0.2); color: #f59e0b; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
@media (max-width: 900px) { .two-col { grid-template-columns: 1fr; } }

table { width: 100%; border-collapse: collapse; }
th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); font-size: 13px; }
th { color: var(--text-muted); font-size: 11px; }
td.highlight { color: #f59e0b; font-weight: 600; }

.mini-bar-bg { display: inline-block; width: 60px; height: 4px; background: var(--border); border-radius: 2px; vertical-align: middle; margin-right: 4px; }
.mini-bar { height: 4px; background: #f59e0b; border-radius: 2px; }

.affiliate-row { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--border); }
.affiliate-row:last-child { border-bottom: none; }
.aff-rank { width: 28px; height: 28px; border-radius: 50%; background: var(--border); display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.aff-rank.top { background: #f59e0b; color: white; }
.aff-info { flex: 1; min-width: 0; }
.aff-name { font-size: 13px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.aff-id { font-size: 11px; color: var(--text-muted); }
.aff-metrics { text-align: right; }
.aff-gmv { font-size: 15px; font-weight: 700; color: #f59e0b; }
.aff-sub { font-size: 11px; color: var(--text-muted); }
.aff-commission-rate { font-size: 11px; color: var(--text-muted); }

.compare-table table td.self-win { color: #3b82f6; font-weight: 600; font-size: 12px; }
.compare-table table td.aff-win { color: #f59e0b; font-weight: 600; font-size: 12px; }
</style>
