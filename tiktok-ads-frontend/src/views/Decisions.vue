<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">决策中心</div>
        <div class="page-subtitle">LLM 智能决策记录，高置信度自动执行，低置信度等待人工审批</div>
      </div>
      <div style="display:flex;gap:8px">
        <select v-model="filter.status" @change="load" style="width:130px">
          <option value="">全部状态</option>
          <option value="PENDING">⏳ 待审批</option>
          <option value="AUTO_EXECUTED">✅ 已自动执行</option>
          <option value="MANUAL_APPROVED">👍 已人工批准</option>
          <option value="MANUAL_REJECTED">❌ 已拒绝</option>
          <option value="FAILED">💥 执行失败</option>
        </select>
        <button class="btn btn-ghost" @click="load">🔄 刷新</button>
      </div>
    </div>

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>状态</th>
            <th>决策动作</th>
            <th>广告账户</th>
            <th>操作对象</th>
            <th>置信度</th>
            <th>决策理由</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in decisions" :key="d.id">
            <td><span :class="['badge', statusClass(d.status)]">{{ statusLabel(d.status) }}</span></td>
            <td>
              <span :class="['badge', actionClass(d.action)]">{{ actionLabel(d.action) }}</span>
            </td>
            <td style="font-size:12px;color:var(--text-muted)">{{ d.advertiser_id }}</td>
            <td style="font-size:12px;max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                :title="d.object_name || d.object_id">
              {{ d.object_name || d.object_id || '-' }}
            </td>
            <td>
              <div style="display:flex;align-items:center;gap:6px">
                <div style="width:60px;height:6px;background:var(--border);border-radius:3px;overflow:hidden">
                  <div :style="{ width: (d.confidence*100)+'%', height:'100%', background: confColor(d.confidence) }"></div>
                </div>
                <span style="font-size:12px">{{ (d.confidence*100).toFixed(0) }}%</span>
              </div>
            </td>
            <td style="font-size:12px;color:var(--text-muted);max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                :title="d.reason">{{ d.reason || '-' }}</td>
            <td style="font-size:12px;color:var(--text-muted);white-space:nowrap">{{ fmtTime(d.created_at) }}</td>
            <td>
              <div style="display:flex;gap:4px" v-if="d.status === 'PENDING'">
                <button class="btn btn-success" style="padding:4px 8px;font-size:12px" @click="approve(d)">批准</button>
                <button class="btn btn-danger"  style="padding:4px 8px;font-size:12px" @click="reject(d)">拒绝</button>
              </div>
              <button v-else-if="d.status === 'AUTO_EXECUTED' || d.status === 'MANUAL_APPROVED'"
                class="btn btn-ghost" style="padding:4px 8px;font-size:12px" @click="rollback(d)">
                ↩ 回滚
              </button>
              <span v-else style="color:var(--text-muted);font-size:12px">-</span>
            </td>
          </tr>
          <tr v-if="!decisions.length">
            <td colspan="8">
              <div class="empty-state"><div class="empty-icon">🤖</div><div>暂无决策记录</div></div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { decisionApi } from '../api'

const decisions = ref([])
const filter = ref({ status: '' })

const fmtTime = t => t ? new Date(t).toLocaleString('zh-CN') : '-'
const confColor = c => c >= 0.85 ? '#10b981' : c >= 0.7 ? '#f59e0b' : '#ef4444'

const statusClass = s => ({
  PENDING: 'badge-warning', AUTO_EXECUTED: 'badge-success', MANUAL_APPROVED: 'badge-success',
  MANUAL_REJECTED: 'badge-critical', FAILED: 'badge-critical', SKIPPED: 'badge-info',
}[s] || 'badge-info')

const statusLabel = s => ({
  PENDING: '⏳ 待审批', AUTO_EXECUTED: '✅ 自动执行', MANUAL_APPROVED: '👍 已批准',
  MANUAL_REJECTED: '❌ 已拒绝', FAILED: '💥 失败', SKIPPED: '⏭ 跳过',
}[s] || s)

const actionClass = a => (['pause','decrease_budget','decrease_bid'].includes(a) ? 'badge-critical' :
  ['enable','increase_budget','increase_bid'].includes(a) ? 'badge-success' : 'badge-info')

const actionLabel = a => ({
  pause: '⏸ 暂停', enable: '▶️ 启用',
  increase_budget: '💰↑ 提预算', decrease_budget: '💰↓ 降预算',
  increase_bid: '📈 提出价', decrease_bid: '📉 降出价',
  replace_creative: '🎨 换创意', no_action: '👀 观察',
}[a] || a)

async function load() {
  const params = { limit: 100 }
  if (filter.value.status) params.status = filter.value.status
  const data = await decisionApi.list(params)
  decisions.value = data.items || []
}

async function approve(d) {
  await decisionApi.approve(d.id)
  d.status = 'MANUAL_APPROVED'
}

async function reject(d) {
  await decisionApi.reject(d.id)
  d.status = 'MANUAL_REJECTED'
}

async function rollback(d) {
  if (!confirm(`确定回滚决策 #${d.id}（${actionLabel(d.action)}）吗？`)) return
  await decisionApi.rollback(d.id)
  await load()
}

onMounted(load)
</script>
