<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">告警中心</div>
        <div class="page-subtitle">实时监控投放异常，自动触发 LLM 决策</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <select v-model="filter.severity" @change="load" style="width:100px">
          <option value="">全部等级</option>
          <option value="CRITICAL">🚨 紧急</option>
          <option value="WARNING">⚠️ 警告</option>
          <option value="INFO">ℹ️ 信息</option>
        </select>
        <button class="btn btn-ghost" @click="load">🔄 刷新</button>
      </div>
    </div>

    <div class="card">
      <div v-if="loading" style="text-align:center;padding:40px;color:var(--text-muted)">加载中…</div>
      <template v-else>
        <table>
          <thead>
            <tr>
              <th>等级</th>
              <th>告警标题</th>
              <th>广告账户</th>
              <th>对象</th>
              <th>类型</th>
              <th>时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in alerts" :key="a.id">
              <td>
                <span :class="['badge', severityClass(a.severity)]">
                  {{ severityLabel(a.severity) }}
                </span>
              </td>
              <td>
                <div style="font-weight:500">{{ a.title }}</div>
                <div style="font-size:12px;color:var(--text-muted);margin-top:2px">{{ a.message }}</div>
              </td>
              <td style="font-size:12px;color:var(--text-muted)">{{ a.advertiser_id }}</td>
              <td style="font-size:12px;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                  :title="a.object_name || a.object_id">
                {{ a.object_name || a.object_id || '-' }}
              </td>
              <td><code style="font-size:11px;background:var(--bg);padding:2px 6px;border-radius:4px">{{ alertTypeLabel(a.alert_type) }}</code></td>
              <td style="font-size:12px;color:var(--text-muted);white-space:nowrap">{{ fmtTime(a.created_at) }}</td>
              <td>
                <button class="btn btn-ghost" style="padding:4px 8px;font-size:12px"
                  @click="resolve(a)" :disabled="a.is_resolved">
                  {{ a.is_resolved ? '已解决' : '标记解决' }}
                </button>
              </td>
            </tr>
            <tr v-if="!alerts.length">
              <td colspan="7">
                <div class="empty-state">
                  <div class="empty-icon">✅</div>
                  <div>暂无未解决告警</div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { alertApi } from '../api'

const loading = ref(false)
const alerts = ref([])
const filter = ref({ severity: '', is_resolved: false })

const severityClass = s => ({ CRITICAL: 'badge-critical', WARNING: 'badge-warning', INFO: 'badge-info' }[s] || 'badge-info')
const severityLabel = s => ({ CRITICAL: '🚨 紧急', WARNING: '⚠️ 警告', INFO: 'ℹ️ 信息' }[s] || s)
const alertTypeLabel = t => ({
  SPEND_ANOMALY: '花费异常', CTR_DROP: '点击率下降', CVR_DROP: '转化率下降',
  BUDGET_DEPLETED: '预算耗尽', TOKEN_EXPIRY: 'Token 过期', AD_REJECTED: '广告被拒',
  ACCOUNT_SUSPENDED: '账户暂停', CPM_SPIKE: 'CPM 飙升', TREND_DECLINE: '趋势下滑',
  CMO_DROP: '订单成本飙升', ROI_BELOW_BREAKEVEN: 'ROI 低于保本线', BUDGET_EXCEED: '超预算',
}[t] || t)
const fmtTime = t => t ? new Date(t).toLocaleString('zh-CN') : '-'

async function load() {
  loading.value = true
  try {
    const params = { is_resolved: filter.value.is_resolved, limit: 100 }
    if (filter.value.severity) params.severity = filter.value.severity
    const data = await alertApi.list(params)
    alerts.value = data.items || []
  } finally {
    loading.value = false
  }
}

async function resolve(alert) {
  await alertApi.resolve(alert.id)
  alert.is_resolved = true
}

onMounted(load)
</script>
