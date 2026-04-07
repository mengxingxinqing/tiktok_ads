<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">📊 决策效果评估</div>
        <div class="page-subtitle">查看每次系统决策的实际效果数据对比</div>
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
        <div class="metric-label">📈 总决策数</div>
        <div class="metric-value">{{ summary.total_impacts || 0 }}</div>
        <div class="metric-sub">{{ daysFilter }} 天内</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">✅ 有效决策</div>
        <div class="metric-value" style="color:var(--success)">{{ summary.effective || 0 }}</div>
        <div class="metric-sub">{{ summary.effective_rate || '0%' }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">❌ 无效决策</div>
        <div class="metric-value" style="color:var(--danger)">{{ summary.ineffective || 0 }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">⭐ 平均评分</div>
        <div class="metric-value">{{ (summary.avg_effectiveness_score || 0).toFixed(2) }}</div>
        <div class="metric-sub">-1.0 ~ 1.0 的评分</div>
      </div>
    </div>

    <!-- 按决策类型分组统计 -->
    <div class="card" style="margin-bottom:20px">
      <div style="font-weight:600;margin-bottom:16px">🎯 按决策类型统计</div>

      <table v-if="Object.keys(byAction).length > 0">
        <thead>
          <tr>
            <th>决策类型</th>
            <th style="text-align:center">执行次数</th>
            <th style="text-align:center">有效次数</th>
            <th style="text-align:center">有效率</th>
            <th style="text-align:right">平均 ROAS 变化</th>
            <th style="text-align:right">平均评分</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, action) in byAction" :key="action">
            <td style="font-weight:600">{{ translateAction(action) }}</td>
            <td style="text-align:center">{{ data.count }}</td>
            <td style="text-align:center;color:var(--success)">{{ data.effective }}</td>
            <td style="text-align:center">{{ data.effective_rate }}</td>
            <td style="text-align:right" :class="data.avg_delta_roas_pct >= 0 ? 'stat-up' : 'stat-down'">
              {{ data.avg_delta_roas_pct > 0 ? '+' : '' }}{{ data.avg_delta_roas_pct.toFixed(1) }}%
            </td>
            <td style="text-align:right" :class="data.avg_effectiveness >= 0 ? 'stat-up' : 'stat-down'">
              {{ data.avg_effectiveness.toFixed(2) }}
            </td>
            <td>
              <span v-if="data.effective_rate.includes('100')" class="badge badge-success">✓ 优秀</span>
              <span v-else-if="data.effective_rate.includes('50')" class="badge badge-warning">△ 一般</span>
              <span v-else class="badge badge-danger">✗ 需改进</span>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else style="padding:20px;text-align:center;color:var(--text-muted)">
        暂无决策数据
      </div>
    </div>

    <!-- 效果最好的决策 -->
    <div class="card" style="margin-bottom:20px">
      <div style="font-weight:600;margin-bottom:16px">🏆 效果最好的决策</div>

      <table v-if="topDecisions.length > 0">
        <thead>
          <tr>
            <th>广告 ID</th>
            <th>广告名称</th>
            <th>决策类型</th>
            <th style="text-align:right">前 ROAS</th>
            <th style="text-align:right">后 ROAS</th>
            <th style="text-align:right">ROAS 变化</th>
            <th style="text-align:right">花费变化</th>
            <th style="text-align:right">评分</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="impact in topDecisions" :key="impact.id">
            <td style="font-family:monospace;font-size:12px">{{ impact.object_id }}</td>
            <td>{{ impact.object_name }}</td>
            <td>
              <span class="badge badge-info" style="font-size:12px">
                {{ getDecisionAction(impact.decision_id) }}
              </span>
            </td>
            <td style="text-align:right">{{ impact.before_roas ? impact.before_roas.toFixed(2) : '-' }}x</td>
            <td style="text-align:right">{{ impact.after_roas ? impact.after_roas.toFixed(2) : '-' }}x</td>
            <td style="text-align:right" :class="impact.delta_roas_pct >= 0 ? 'stat-up' : 'stat-down'">
              {{ impact.delta_roas_pct > 0 ? '+' : '' }}{{ impact.delta_roas_pct.toFixed(1) }}%
            </td>
            <td style="text-align:right">
              ${{ (impact.after_spend - impact.before_spend).toFixed(2) }}
            </td>
            <td style="text-align:right;color:var(--success);font-weight:600">
              {{ impact.effectiveness_score.toFixed(2) }}
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else style="padding:20px;text-align:center;color:var(--text-muted)">
        暂无数据
      </div>
    </div>

    <!-- 效果最差的决策（需要反思） -->
    <div class="card">
      <div style="font-weight:600;margin-bottom:16px">⚠️ 效果最差的决策（需要反思）</div>

      <table v-if="bottomDecisions.length > 0">
        <thead>
          <tr>
            <th>广告 ID</th>
            <th>广告名称</th>
            <th>决策类型</th>
            <th style="text-align:right">前 ROAS</th>
            <th style="text-align:right">后 ROAS</th>
            <th style="text-align:right">ROAS 变化</th>
            <th style="text-align:right">转化变化</th>
            <th style="text-align:right">评分</th>
            <th style="width:200px">备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="impact in bottomDecisions" :key="impact.id">
            <td style="font-family:monospace;font-size:12px">{{ impact.object_id }}</td>
            <td>{{ impact.object_name }}</td>
            <td>
              <span class="badge badge-danger" style="font-size:12px">
                {{ getDecisionAction(impact.decision_id) }}
              </span>
            </td>
            <td style="text-align:right">{{ impact.before_roas ? impact.before_roas.toFixed(2) : '-' }}x</td>
            <td style="text-align:right">{{ impact.after_roas ? impact.after_roas.toFixed(2) : '-' }}x</td>
            <td style="text-align:right;color:var(--danger)">
              {{ impact.delta_roas_pct < 0 ? '' : '+' }}{{ impact.delta_roas_pct.toFixed(1) }}%
            </td>
            <td style="text-align:right;color:var(--danger)">
              {{ impact.delta_conversion > 0 ? '+' : '' }}{{ impact.delta_conversion?.toFixed(0) || '-' }}
            </td>
            <td style="text-align:right;color:var(--danger);font-weight:600">
              {{ impact.effectiveness_score.toFixed(2) }}
            </td>
            <td>
              <input
                v-model="impact.review_notes"
                type="text"
                placeholder="输入反思备注"
                style="width:100%;padding:4px 8px;font-size:12px;border:1px solid var(--border);border-radius:4px"
                @blur="saveReview(impact)"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else style="padding:20px;text-align:center;color:var(--text-muted)">
        暂无数据
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api'


const daysFilter = ref(30)
const summary = ref({})
const byAction = ref({})
const topDecisions = ref([])
const bottomDecisions = ref([])

const translateAction = (action) => {
  const map = {
    pause: '暂停',
    enable: '启用',
    increase_budget: '加预算',
    decrease_budget: '降预算',
    increase_bid: '加价',
    decrease_bid: '降价',
    heat_up: '加热',
    adjust_bid: '调整出价',
  }
  return map[action] || action
}

const getDecisionAction = async (decisionId) => {
  // 实际应该从 API 获取，这里简化为返回类型
  return 'pause'
}

async function load() {
  try {
    const advertiserId = localStorage.getItem('current_advertiser_id') || 'test'

    const res = await api.get(`/decisions/impact-report/${advertiserId}`, {
      params: { days: daysFilter.value },
    })

    summary.value = res.summary || res.data?.summary || {}
    byAction.value = res.by_action || res.data?.by_action || {}

    // 获取效果最好和最差的决策
    const topRes = await api.get(`/decisions/top-effective/${advertiserId}`, {
      params: { limit: 5 },
    })
    topDecisions.value = topRes.items || topRes.data?.items || []

    const bottomRes = await api.get(`/decisions/bottom-effective/${advertiserId}`, {
      params: { limit: 5 },
    })
    bottomDecisions.value = bottomRes.items || bottomRes.data?.items || []
  } catch (e) {
    console.error('Failed to load impact report:', e)
  }
}

async function saveReview(impact) {
  try {
    await api.patch(`/decisions/impacts/${impact.id}`, {
      review_notes: impact.review_notes,
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

.badge-info {
  background: #d1ecf1;
  color: #0c5460;
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
