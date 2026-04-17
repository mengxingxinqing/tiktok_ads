<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">📈 智能涨粉</div>
        <div class="page-subtitle">自动投放 · 实时监控 · 达标停投</div>
      </div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-primary" @click="$router.push('/growth/campaigns')">+ 新建 Campaign</button>
        <button class="btn btn-ghost" @click="$router.push('/growth/tk-accounts')">🎯 TK账号</button>
        <button class="btn btn-ghost" @click="authorize" title="涨粉模块独立授权，与 gmvmax 数据完全隔离">
          🔐 授权广告户
        </button>
        <button class="btn btn-ghost" @click="syncAdAccounts" :disabled="syncing">
          {{ syncing ? '同步中…' : '🔄 同步广告户' }}
        </button>
      </div>
    </div>

    <!-- 核心指标 -->
    <div class="metrics-grid" style="margin-top:16px">
      <div class="metric-card">
        <div class="metric-label">🎯 运行中</div>
        <div class="metric-value">{{ stats.running }}</div>
        <div class="metric-sub">Campaign</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">✅ 达标</div>
        <div class="metric-value" style="color:var(--success)">{{ stats.completed }}</div>
        <div class="metric-sub">完成</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">💰 累计花费</div>
        <div class="metric-value">${{ fmt(stats.totalSpend) }}</div>
        <div class="metric-sub">USD</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">👥 累计涨粉</div>
        <div class="metric-value">{{ fmt(stats.totalFollowers) }}</div>
        <div class="metric-sub">粉丝</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">📊 平均万粉成本</div>
        <div class="metric-value">${{ stats.avgCost }}</div>
        <div class="metric-sub">预设 $35</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">📦 素材库</div>
        <div class="metric-value">{{ stats.materialCount }}</div>
        <div class="metric-sub">个素材</div>
      </div>
    </div>

    <!-- Tab -->
    <div class="tab-bar" style="margin-top:20px">
      <button class="tab-btn" :class="{active: tab==='running'}" @click="tab='running'">
        🔄 运行中 ({{ runningCampaigns.length }})
      </button>
      <button class="tab-btn" :class="{active: tab==='pending'}" @click="tab='pending'">
        ⏳ 待启动 ({{ pendingCampaigns.length }})
      </button>
      <button class="tab-btn" :class="{active: tab==='completed'}" @click="tab='completed'">
        ✅ 已完成 ({{ completedCampaigns.length }})
      </button>
    </div>

    <!-- 运行中 Campaign -->
    <div v-if="tab==='running'" class="card" style="margin-top:16px">
      <div v-if="loading" style="text-align:center;padding:40px;color:var(--text-muted)">加载中…</div>
      <div v-else-if="!runningCampaigns.length" class="empty-state">
        <div class="empty-icon">🎉</div>
        <div>暂无运行中的 Campaign</div>
        <button class="btn btn-primary" style="margin-top:12px" @click="$router.push('/growth/campaigns')">创建第一个</button>
      </div>
      <template v-else>
        <table>
          <thead>
            <tr>
              <th>TK账号</th>
              <th>Ad账户</th>
              <th>预算进度</th>
              <th>粉丝进度</th>
              <th>当前单粉成本</th>
              <th>开始</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in runningCampaigns" :key="c.campaign_id">
              <td><b>@{{ c.tk_account_id }}</b></td>
              <td style="font-size:12px;color:var(--text-muted)">{{ c.ad_account_id }}</td>
              <!-- 预算进度 -->
              <td>
                <div style="font-size:13px">
                  <b>${{ fmt(c.total_spend) }}</b> / ${{ fmt(c.budget) }}
                </div>
                <div style="font-size:11px;color:var(--text-muted)">
                  已烧 {{ Math.round((c.total_spend / c.budget) * 100 || 0) }}%
                </div>
              </td>
              <!-- 粉丝进度 -->
              <td>
                <div style="font-size:13px">
                  <b style="color:var(--success)">+{{ c.followers_gained || 0 }}</b> / +{{ c.target_followers }}
                </div>
                <div style="font-size:11px;color:var(--text-muted)">
                  达成 {{ Math.round(((c.followers_gained || 0) / c.target_followers) * 100 || 0) }}%
                </div>
              </td>
              <!-- 当前单粉成本 vs target -->
              <td>
                <span :style="{color: costColor(c), fontWeight: 600}">
                  ${{ costPer10k(c) }}/10k
                </span>
                <div style="font-size:11px;color:var(--text-muted)">
                  目标 ${{ c.target_cost_per_10k || 35 }}/10k
                  <span v-if="isCostOverLimit(c)" style="color:var(--danger)"> ⚠️超标</span>
                </div>
              </td>
              <td style="font-size:12px;color:var(--text-muted)">{{ fmtTime(c.start_time) }}</td>
              <td>
                <button class="btn btn-ghost" style="padding:4px 8px;font-size:12px" @click="stopCampaign(c.campaign_id)">停止</button>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
    </div>

    <!-- 待启动 -->
    <div v-if="tab==='pending'" class="card" style="margin-top:16px">
      <div v-if="!pendingCampaigns.length" class="empty-state">
        <div class="empty-icon">⏳</div>
        <div>暂无待启动的 Campaign</div>
      </div>
      <template v-else>
        <table>
          <thead>
            <tr>
              <th>TK账号</th><th>Ad账户</th><th>目标增量</th><th>预算(USD)</th><th>状态</th><th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in pendingCampaigns" :key="c.campaign_id">
              <td><b>@{{ c.tk_account_id }}</b></td>
              <td style="font-size:12px;color:var(--text-muted)">{{ c.ad_account_id }}</td>
              <td>{{ c.target_followers }}</td>
              <td>${{ c.budget }}</td>
              <td><span class="badge">待启动</span></td>
              <td>
                <button class="btn btn-primary" style="padding:4px 10px;font-size:12px" @click="startCampaign(c.campaign_id)">▶ 启动</button>
                <button class="btn btn-ghost" style="padding:4px 8px;font-size:12px;margin-left:4px" @click="deleteCampaign(c.campaign_id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
    </div>

    <!-- 已完成 -->
    <div v-if="tab==='completed'" class="card" style="margin-top:16px">
      <div v-if="!completedCampaigns.length" class="empty-state">
        <div class="empty-icon">📋</div>
        <div>暂无已完成的 Campaign</div>
      </div>
      <template v-else>
        <table>
          <thead>
            <tr>
              <th>TK账号</th><th>涨粉</th><th>花费(USD)</th><th>万粉成本</th><th>停止原因</th><th>完成时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in completedCampaigns" :key="c.campaign_id">
              <td><b>@{{ c.tk_account_id }}</b></td>
              <td><b style="color:var(--success)">+{{ c.followers_gained }}</b></td>
              <td>${{ fmt(c.total_spend) }}</td>
              <td>
                <span :style="{color: costColor(c)}">${{ costPer10k(c) }}</span>
              </td>
              <td><span class="badge">{{ c.auto_stop_reason || '—' }}</span></td>
              <td style="font-size:12px;color:var(--text-muted)">{{ fmtTime(c.end_time) }}</td>
            </tr>
          </tbody>
        </table>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { growthApi } from '../api'

const tab = ref('running')
const loading = ref(false)
const campaigns = ref([])
const syncing = ref(false)

const stats = ref({
  running: 0, completed: 0, totalSpend: 0, totalFollowers: 0,
  avgCost: 35, materialCount: 0,
})

const runningCampaigns = computed(() => campaigns.value.filter(c => c.status === 'RUNNING'))
const pendingCampaigns = computed(() => campaigns.value.filter(c => c.status === 'PENDING'))
const completedCampaigns = computed(() => campaigns.value.filter(c => ['COMPLETED', 'FAILED', 'PAUSED'].includes(c.status)))

async function load() {
  loading.value = true
  try {
    const [gcRes, matRes] = await Promise.all([
      growthApi.listCampaigns({ page_size: 100 }),
      growthApi.listCreatives({ page_size: 1 }),
    ])
    campaigns.value = gcRes.campaigns || []

    const running = runningCampaigns.value
    const completed = completedCampaigns.value
    const totalSpend = [...running, ...completed].reduce((s, c) => s + (c.total_spend || 0), 0)
    const totalFollowers = [...running, ...completed].reduce((s, c) => s + (c.followers_gained || 0), 0)
    stats.value = {
      running: running.length,
      completed: completed.length,
      totalSpend,
      totalFollowers,
      avgCost: totalFollowers > 0 ? (totalSpend / totalFollowers * 10000).toFixed(2) : 35,
      materialCount: matRes.total || 0,
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function authorize() {
  try {
    const res = await growthApi.getAuthUrl('growth')
    if (!res.auth_url) {
      alert('生成授权 URL 失败')
      return
    }
    const url = res.auth_url
    // 优先用 Clipboard API；不支持时回退 textarea + execCommand
    let copied = false
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(url)
        copied = true
      } else {
        const ta = document.createElement('textarea')
        ta.value = url
        ta.style.position = 'fixed'
        ta.style.left = '-9999px'
        document.body.appendChild(ta)
        ta.select()
        copied = document.execCommand('copy')
        document.body.removeChild(ta)
      }
    } catch (e) {
      copied = false
    }
    if (copied) {
      alert('✅ 授权链接已复制到剪贴板，请发给广告户管理员：\n\n' + url)
    } else {
      prompt('复制以下授权链接，发给广告户管理员：', url)
    }
  } catch (e) {
    alert('生成授权 URL 失败: ' + (e.response?.data?.detail || e.message || e))
  }
}

async function syncAdAccounts() {
  syncing.value = true
  try {
    const res = await growthApi.syncAdAccounts()
    alert(`同步完成：新增 ${res.created || 0}，更新 ${res.updated || 0}，失败 ${res.failed || 0}`)
    await load()
  } catch (e) {
    alert('同步失败: ' + (e.response?.data?.detail || e.message || e))
  } finally {
    syncing.value = false
  }
}

async function startCampaign(id) {
  try {
    await growthApi.startCampaign(id)
    await load()
  } catch (e) { alert('启动失败: ' + (e.message || e)) }
}

async function stopCampaign(id) {
  if (!confirm('确认停止该 Campaign？')) return
  try {
    await growthApi.stopCampaign(id, 'MANUAL')
    await load()
  } catch (e) { alert('停止失败: ' + (e.message || e)) }
}

async function deleteCampaign(id) {
  // 只删除 PENDING 状态的
  try {
    await growthApi.stopCampaign(id, 'MANUAL')
    await load()
  } catch (e) { /* ignore */ }
}

function costPer10k(c) {
  if (!c.followers_gained || c.followers_gained <= 0) return '—'
  return (c.total_spend / c.followers_gained * 10000).toFixed(2)
}

function costColor(c) {
  const cost = parseFloat(costPer10k(c))
  const target = c.target_cost_per_10k || 35
  if (!cost || cost === 0) return ''
  if (cost <= target) return 'var(--success)'
  if (cost <= target * 1.2) return 'var(--warning)'
  return 'var(--danger)'
}

function isCostOverLimit(c) {
  const cost = parseFloat(costPer10k(c))
  const target = c.target_cost_per_10k || 35
  return cost && cost > target * 1.1
}

function fmt(n) {
  if (!n && n !== 0) return '0'
  return Number(n).toLocaleString('en', { maximumFractionDigits: 2 })
}

function fmtTime(ts) {
  if (!ts) return '—'
  return new Date(ts).toLocaleString('zh-CN', { hour12: false }).slice(0, 16)
}

onMounted(load)
</script>
