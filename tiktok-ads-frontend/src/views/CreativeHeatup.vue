<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">🔥 创意加热追踪</div>
        <div class="page-subtitle">记录和评估每次创意加热操作的效果</div>
      </div>
      <div style="display:flex;gap:8px">
        <select v-model.number="daysFilter" style="padding:8px 12px;border-radius:8px" @change="load">
          <option :value="7">最近 7 天</option>
          <option :value="14">最近 14 天</option>
          <option :value="30">最近 30 天</option>
          <option :value="90">最近 90 天</option>
        </select>
        <button class="btn btn-ghost" @click="load">🔄 刷新</button>
      </div>
    </div>

    <!-- 概览卡片 -->
    <div class="metrics-grid" style="margin-bottom:20px">
      <div class="metric-card">
        <div class="metric-label">🔥 总加热次数</div>
        <div class="metric-value">{{ summary.total_heatups || 0 }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">✅ 成功加热</div>
        <div class="metric-value" style="color:var(--success)">{{ summary.successful || 0 }}</div>
        <div class="metric-sub">{{ summary.success_rate || '0%' }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">❌ 失败加热</div>
        <div class="metric-value" style="color:var(--danger)">{{ summary.failed || 0 }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">⭐ 平均评分</div>
        <div class="metric-value">{{ (summary.avg_score || 0).toFixed(2) }}</div>
        <div class="metric-sub">0 ~ 1.0 的评分</div>
      </div>
    </div>

    <!-- 按加热类型统计 -->
    <div class="card" style="margin-bottom:20px">
      <div style="font-weight:600;margin-bottom:16px">📊 按加热类型统计</div>

      <table v-if="Object.keys(byType).length > 0">
        <thead>
          <tr>
            <th>加热类型</th>
            <th style="text-align:center">执行次数</th>
            <th style="text-align:center">成功次数</th>
            <th style="text-align:center">成功率</th>
            <th style="text-align:right">平均转化增加</th>
            <th style="text-align:right">平均评分</th>
            <th>评价</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, htype) in byType" :key="htype">
            <td style="font-weight:600">{{ translateHeatupType(htype) }}</td>
            <td style="text-align:center">{{ data.count }}</td>
            <td style="text-align:center;color:var(--success)">{{ data.successful }}</td>
            <td style="text-align:center">{{ data.success_rate }}</td>
            <td style="text-align:right" :class="data.avg_delta_conversion >= 0 ? 'stat-up' : 'stat-down'">
              {{ data.avg_delta_conversion > 0 ? '+' : '' }}{{ data.avg_delta_conversion.toFixed(1) }}
            </td>
            <td style="text-align:right" :class="data.avg_score >= 0.5 ? 'stat-up' : 'stat-down'">
              {{ data.avg_score.toFixed(2) }}
            </td>
            <td>
              <span v-if="data.success_rate.includes('100')" class="badge badge-success">优秀</span>
              <span v-else-if="data.success_rate.includes('50')" class="badge badge-warning">一般</span>
              <span v-else class="badge badge-danger">需改进</span>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else style="padding:20px;text-align:center;color:var(--text-muted)">
        暂无加热数据
      </div>
    </div>

    <!-- 最成功的加热操作 -->
    <div class="card" style="margin-bottom:20px">
      <div style="font-weight:600;margin-bottom:16px">🏆 最成功的加热操作</div>

      <table v-if="topHeatups.length > 0">
        <thead>
          <tr>
            <th>创意 ID</th>
            <th>加热类型</th>
            <th style="text-align:right">前转化</th>
            <th style="text-align:right">后转化</th>
            <th style="text-align:right">转化增加</th>
            <th style="text-align:right">前 ROAS</th>
            <th style="text-align:right">后 ROAS</th>
            <th style="text-align:right">评分</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="heatup in topHeatups" :key="heatup.id">
            <td style="font-family:monospace;font-size:12px">{{ heatup.video_id }}</td>
            <td>{{ translateHeatupType(heatup.heatup_type) }}</td>
            <td style="text-align:right">{{ heatup.before_conversion?.toFixed(0) || '-' }}</td>
            <td style="text-align:right">{{ heatup.after_conversion?.toFixed(0) || '-' }}</td>
            <td style="text-align:right;color:var(--success);font-weight:600">
              {{ heatup.delta_conversion > 0 ? '+' : '' }}{{ heatup.delta_conversion?.toFixed(1) || '-' }}
            </td>
            <td style="text-align:right">{{ heatup.before_roas?.toFixed(2) || '-' }}x</td>
            <td style="text-align:right">{{ heatup.after_roas?.toFixed(2) || '-' }}x</td>
            <td style="text-align:right;color:var(--success);font-weight:600">
              {{ heatup.success_score?.toFixed(2) || '-' }}
            </td>
            <td>
              <span class="badge badge-success">✓ 成功</span>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else style="padding:20px;text-align:center;color:var(--text-muted)">
        暂无数据
      </div>
    </div>

    <!-- 失败的加热操作 -->
    <div class="card">
      <div style="font-weight:600;margin-bottom:16px">⚠️ 失败的加热操作（需要反思）</div>

      <table v-if="failedHeatups.length > 0">
        <thead>
          <tr>
            <th>创意 ID</th>
            <th>加热原因</th>
            <th>加热类型</th>
            <th style="text-align:right">前转化</th>
            <th style="text-align:right">后转化</th>
            <th style="text-align:right">转化变化</th>
            <th style="text-align:right">前 ROAS</th>
            <th style="text-align:right">后 ROAS</th>
            <th style="text-align:right">评分</th>
            <th style="width:150px">反思备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="heatup in failedHeatups" :key="heatup.id">
            <td style="font-family:monospace;font-size:12px">{{ heatup.video_id }}</td>
            <td style="font-size:12px">{{ heatup.heatup_reason }}</td>
            <td>{{ translateHeatupType(heatup.heatup_type) }}</td>
            <td style="text-align:right">{{ heatup.before_conversion?.toFixed(0) || '-' }}</td>
            <td style="text-align:right">{{ heatup.after_conversion?.toFixed(0) || '-' }}</td>
            <td style="text-align:right;color:var(--danger)">
              {{ heatup.delta_conversion < 0 ? '' : '+' }}{{ heatup.delta_conversion?.toFixed(1) || '-' }}
            </td>
            <td style="text-align:right">{{ heatup.before_roas?.toFixed(2) || '-' }}x</td>
            <td style="text-align:right">{{ heatup.after_roas?.toFixed(2) || '-' }}x</td>
            <td style="text-align:right;color:var(--danger);font-weight:600">
              {{ heatup.success_score?.toFixed(2) || '-' }}
            </td>
            <td>
              <input
                v-model="heatup.notes"
                type="text"
                placeholder="输入反思"
                style="width:100%;padding:4px 8px;font-size:12px;border:1px solid var(--border);border-radius:4px"
                @blur="saveReview(heatup)"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else style="padding:20px;text-align:center;color:var(--text-muted)">
        暂无失败数据（恭喜！）
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'


const daysFilter = ref(30)
const summary = ref({})
const byType = ref({})
const topHeatups = ref([])
const failedHeatups = ref([])

const translateHeatupType = (htype) => {
  const map = {
    INCREASE_BUDGET: '加预算',
    NEW_AD: '新建 Ad',
    RAISE_BID: '加价',
    CLONE_AD: '克隆 Ad',
  }
  return map[htype] || htype
}

async function load() {
  try {
    const advertiserId = localStorage.getItem('current_advertiser_id') || 'test'

    const res = await api.get(`/creatives/heatup-report/${advertiserId}`, {
      params: { days: daysFilter.value },
    })

    summary.value = res.summary || res.data?.summary || {}
    byType.value = res.by_type || res.data?.by_type || {}

    // 获取最成功和失败的加热
    const topRes = await api.get(`/creatives/top-heatups/${advertiserId}`, {
      params: { limit: 5 },
    })
    topHeatups.value = topRes.data.items || []

    const failRes = await api.get(`/creatives/failed-heatups/${advertiserId}`, {
      params: { limit: 5 },
    })
    failedHeatups.value = failRes.data.items || []
  } catch (e) {
    console.error('Failed to load heatup report:', e)
  }
}

async function saveReview(heatup) {
  try {
    await api.patch(`/creatives/heatups/${heatup.id}`, {
      notes: heatup.notes,
    })
  } catch (e) {
    console.error('Failed to save review:', e)
  }
}

onMounted(load)
</script>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
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
  font-size: 24px;
  font-weight: 700;
}

.metric-sub {
  font-size: 12px;
  color: var(--text-muted);
}

.stat-up {
  color: var(--success);
}

.stat-down {
  color: var(--danger);
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-danger {
  background: #f8d7da;
  color: #721c24;
}

.badge-warning {
  background: #fff3cd;
  color: #856404;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

thead tr {
  background: var(--bg);
  border-bottom: 2px solid var(--border);
}

th {
  padding: 10px 8px;
  text-align: left;
  font-weight: 600;
  color: var(--text-secondary);
}

td {
  padding: 8px;
  border-bottom: 1px solid var(--border);
}

tbody tr:hover {
  background: var(--hover-bg);
}
</style>
