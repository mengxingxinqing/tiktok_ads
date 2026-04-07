<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">创意大盘</div>
        <div class="page-subtitle">追踪创意生产流水线：新增 → 学习 → 跑量 → 衰退 → 停止</div>
      </div>
      <select v-model="filter.days" @change="loadAll" style="width:100px">
        <option value="7">近 7 天</option>
        <option value="14">近 14 天</option>
        <option value="30">近 30 天</option>
        <option value="60">近 60 天</option>
      </select>
    </div>

    <!-- 流水线卡片 -->
    <div class="pipeline">
      <div class="pipe-card">
        <div class="pipe-num">{{ overview.total }}</div>
        <div class="pipe-label">创意总量</div>
      </div>
      <div class="pipe-arrow">→</div>
      <div class="pipe-card learning">
        <div class="pipe-num">{{ overview.learning }}</div>
        <div class="pipe-label">🌱 学习中</div>
      </div>
      <div class="pipe-arrow">→</div>
      <div class="pipe-card running">
        <div class="pipe-num">{{ overview.running }}</div>
        <div class="pipe-label">🚀 跑量中</div>
      </div>
      <div class="pipe-arrow">→</div>
      <div class="pipe-card declining">
        <div class="pipe-num">{{ overview.declining }}</div>
        <div class="pipe-label">📉 衰退中</div>
      </div>
      <div class="pipe-arrow">→</div>
      <div class="pipe-card stopped">
        <div class="pipe-num">{{ overview.stopped }}</div>
        <div class="pipe-label">💀 已停止</div>
      </div>
    </div>

    <!-- 汇总条 -->
    <div v-if="summary" class="summary-bar card">
      <div class="summary-item">
        <span class="summary-label">期间新增</span>
        <span class="summary-value">{{ summary.total_new }} 个</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">总花费</span>
        <span class="summary-value">${{ fmt(summary.total_spend) }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">总 GMV</span>
        <span class="summary-value" style="color:var(--success)">${{ fmt(summary.total_revenue) }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">总订单</span>
        <span class="summary-value">{{ summary.total_orders }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">整体 ROI</span>
        <span class="summary-value" :style="{color: summary.roi >= 1 ? 'var(--success)' : 'var(--danger)'}">
          {{ summary.roi > 0 ? summary.roi.toFixed(2) + 'x' : '-' }}
        </span>
      </div>
    </div>

    <!-- 每日流水线表格 -->
    <div class="card">
      <div style="font-weight:600;margin-bottom:12px">按创建日期统计</div>
      <table>
        <thead>
          <tr>
            <th>创建日期</th>
            <th>新增</th>
            <th>🌱 学习中</th>
            <th>🚀 跑量中</th>
            <th>📉 衰退</th>
            <th>💀 停止</th>
            <th>花费</th>
            <th>GMV</th>
            <th>订单</th>
            <th>ROI</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in daily" :key="d.date">
            <td style="font-weight:600;white-space:nowrap">{{ d.date }}</td>
            <td style="font-weight:700">{{ d.new_count }}</td>
            <td class="stage-learning">{{ d.learning }}</td>
            <td class="stage-running">{{ d.running }}</td>
            <td class="stage-declining">{{ d.declining }}</td>
            <td class="stage-stopped">{{ d.stopped }}</td>
            <td>${{ fmt(d.total_spend) }}</td>
            <td style="color:var(--success)">${{ fmt(d.total_revenue) }}</td>
            <td>{{ d.total_orders }}</td>
            <td :style="{color: d.roi >= 1 ? 'var(--success)' : d.roi > 0 ? 'var(--danger)' : 'var(--text-muted)', fontWeight: 600}">
              {{ d.roi > 0 ? d.roi.toFixed(2) + 'x' : '-' }}
            </td>
          </tr>
          <tr v-if="!daily.length">
            <td colspan="10">
              <div class="empty-state">
                <div class="empty-icon">📊</div>
                <div>暂无数据</div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'

const filter = ref({ days: '30' })
const overview = ref({ total: 0, learning: 0, running: 0, declining: 0, stopped: 0 })
const daily = ref([])
const summary = ref(null)

const fmt = v => Number(v || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

async function loadOverview() {
  try {
    overview.value = await api.get('/creative-dashboard/overview')
  } catch { /* ignore */ }
}

async function loadDaily() {
  try {
    const data = await api.get('/creative-dashboard/daily', { params: { days: filter.value.days } })
    daily.value = data.daily || []
    summary.value = data.summary || null
  } catch { daily.value = []; summary.value = null }
}

async function loadAll() {
  await Promise.all([loadOverview(), loadDaily()])
}

onMounted(loadAll)
</script>

<style scoped>
.pipeline {
  display: flex; align-items: center; gap: 0; margin-bottom: 16px;
  overflow-x: auto; padding: 4px 0;
}
.pipe-card {
  flex: 1; min-width: 100px;
  background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px 12px; text-align: center;
}
.pipe-card.learning { border-color: var(--info); background: rgba(59,130,246,0.06); }
.pipe-card.running { border-color: var(--success); background: rgba(16,185,129,0.06); }
.pipe-card.declining { border-color: var(--warning); background: rgba(245,158,11,0.06); }
.pipe-card.stopped { border-color: var(--text-muted); background: rgba(107,114,128,0.06); }
.pipe-num { font-size: 28px; font-weight: 700; }
.pipe-label { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.pipe-arrow { font-size: 20px; color: var(--text-muted); padding: 0 6px; flex-shrink: 0; }

.summary-bar {
  display: flex; gap: 24px; flex-wrap: wrap; padding: 14px 20px; margin-bottom: 16px;
}
.summary-item { display: flex; flex-direction: column; gap: 2px; }
.summary-label { font-size: 11px; color: var(--text-muted); }
.summary-value { font-size: 16px; font-weight: 700; }

table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); }
th { font-size: 11px; color: var(--text-muted); white-space: nowrap; }

.stage-learning { color: var(--info); font-weight: 600; }
.stage-running { color: var(--success); font-weight: 600; }
.stage-declining { color: var(--warning); font-weight: 600; }
.stage-stopped { color: var(--text-muted); }

.empty-state { text-align: center; padding: 40px; color: var(--text-muted); }
.empty-icon { font-size: 36px; margin-bottom: 8px; }
</style>
