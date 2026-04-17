<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">🚀 创建涨粉 Campaign</div>
        <div class="page-subtitle">选择 TK 账号，创建 Campaign，自动匹配合适的素材和 Ad Account</div>
      </div>
      <button class="btn btn-ghost" @click="$router.push('/growth')">← 返回大盘</button>
    </div>

    <!-- 步骤条 -->
    <div class="card" style="margin-top:16px">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:24px;font-size:14px">
        <div :class="['step', step>=1?'active':'']">1. 选择账号</div>
        <div style="color:var(--border)">→</div>
        <div :class="['step', step>=2?'active':'']">2. 确认配置</div>
        <div style="color:var(--border)">→</div>
        <div :class="['step', step>=3?'active':'']">3. 确认创建</div>
      </div>

      <!-- 步骤1：选择 TK 账号 -->
      <div v-if="step === 1">
        <div style="display:flex;gap:8px;margin-bottom:16px;align-items:center">
          <input v-model="searchKw" placeholder="搜索账号…" style="max-width:200px" />
          <select v-model="filterStatus" style="width:120px">
            <option value="">全部状态</option>
            <option value="IDLE">IDLE</option>
            <option value="COMPLETED">已完成</option>
          </select>
          <span style="color:var(--text-muted);font-size:13px">选 {{ selected.length }} 个</span>
        </div>

        <div v-if="loadingAccounts" style="text-align:center;padding:40px;color:var(--text-muted)">加载中…</div>
        <div v-else-if="!availableAccounts.length" class="empty-state">
          <div>无可用的 TK 账号（IDLE 状态）</div>
          <button class="btn btn-primary" style="margin-top:12px" @click="$router.push('/growth/tk-accounts')">先去录入账号</button>
        </div>
        <template v-else>
          <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px">
            <div
              v-for="acc in filteredAccounts"
              :key="acc.account_id"
              :class="['account-card', selected.includes(acc.account_id) ? 'selected' : '']"
              @click="toggleSelect(acc.account_id)"
            >
              <div style="font-weight:600">@{{ acc.account_id }}</div>
              <div style="font-size:12px;color:var(--text-muted)">
                粉丝: {{ acc.follower_count ? acc.follower_count.toLocaleString() : '—' }}
              </div>
              <div style="font-size:12px;color:var(--text-muted)">
                目标: {{ acc.target_follower_count.toLocaleString() }}
              </div>
              <div style="font-size:12px">
                目标成本: <b>${{ acc.target_cost_per_10k }}</b>
              </div>
            </div>
          </div>
        </template>

        <div style="margin-top:20px;display:flex;justify-content:flex-end">
          <button class="btn btn-primary" :disabled="!selected.length" @click="step=2">
            下一步 ({{ selected.length }} 个) →
          </button>
        </div>
      </div>

      <!-- 步骤2：广告户 + 逐号选素材 -->
      <div v-if="step === 2">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px">
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:6px">目标万粉成本 (USD) *</div>
            <input v-model.number="config.target_cost_per_10k" type="number" style="width:100%" />
            <div style="font-size:11px;color:var(--text-muted);margin-top:4px">预算 = 目标增量 × 此值 / 10000（TikTok 硬上限，烧完自动停）</div>
          </div>
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:6px">Ad Account *</div>
            <select v-model="config.ad_account_id" @change="loadMaterialPool" style="width:100%">
              <option value="">请选择（素材按户过滤）</option>
              <option v-for="acc in adAccounts" :key="acc.advertiser_id" :value="acc.advertiser_id">
                {{ acc.advertiser_name }} ({{ acc.currency }} {{ acc.balance }}, USD≈${{ acc.balance_usd || '?' }})
              </option>
            </select>
          </div>
        </div>

        <div v-if="!config.ad_account_id" style="text-align:center;padding:24px;color:var(--text-muted)">
          先选广告账户，系统会加载该户下已授权的素材供分配
        </div>
        <template v-else>
          <div style="font-weight:600;margin-bottom:12px">
            为每个账号选素材（默认推荐样本数 ≥ 3 的低成本素材，可改）
          </div>
          <table>
            <thead>
              <tr>
                <th>TK 账号</th>
                <th>目标增量</th>
                <th>预计预算 USD</th>
                <th>素材</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="accId in selected" :key="accId">
                <td><b>@{{ accId }}</b></td>
                <td>{{ (accountsById[accId] && accountsById[accId].target_follower_count - (accountsById[accId].follower_count || 0)).toLocaleString() }}</td>
                <td>${{ estimateBudget(accId) }}</td>
                <td>
                  <select v-model="materialChoice[accId]" style="width:260px">
                    <option :value="null">
                      {{ recommendedMaterialId ? '自动推荐（' + materialLabel(recommendedMaterialId) + '）' : '— 请选择 —' }}
                    </option>
                    <option
                      v-for="m in materialPool"
                      :key="m.id"
                      :value="m.id"
                    >
                      {{ materialLabel(m.id) }}
                    </option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="!materialPool.length" style="color:var(--warning);margin-top:12px;font-size:13px">
            ⚠️ 该广告户下没有已授权的素材。先去 <a href="/growth/creatives" style="color:var(--primary)">素材库</a> 绑定 auth_code。
          </div>
        </template>

        <div style="display:flex;justify-content:space-between;margin-top:20px">
          <button class="btn btn-ghost" @click="step=1">← 上一步</button>
          <button class="btn btn-primary" :disabled="!canProceedStep2" @click="step=3">创建 Campaign →</button>
        </div>
      </div>

      <!-- 步骤3：创建确认 -->
      <div v-if="step === 3">
        <div v-if="creating" style="text-align:center;padding:40px">
          <div style="margin-bottom:12px">创建中…</div>
          <div style="color:var(--text-muted);font-size:13px">这可能需要几分钟，请勿关闭页面</div>
        </div>
        <div v-else>
          <div style="margin-bottom:16px">
            即将为 <b>{{ selected.length }}</b> 个账号创建 Campaign：
          </div>
          <div style="background:var(--bg);padding:12px;border-radius:8px;margin-bottom:20px;max-height:200px;overflow-y:auto">
            <div v-for="accId in selected" :key="accId" style="font-size:13px;margin-bottom:4px">
              @{{ accId }} → 预算 ${{ estimateBudget(accId) }}
            </div>
          </div>
          <div style="display:flex;justify-content:space-between">
            <button class="btn btn-ghost" @click="step=2">← 上一步</button>
            <button class="btn btn-primary" @click="doCreate">确认创建</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建结果 -->
    <div v-if="createResult" class="card" style="margin-top:16px">
      <div style="font-weight:600;margin-bottom:12px">创建结果</div>
      <div v-if="createResult.created.length" style="margin-bottom:12px">
        ✅ 成功创建 {{ createResult.created.length }} 个 Campaign
      </div>
      <div v-if="createResult.errors && createResult.errors.length">
        <div style="color:var(--danger);margin-bottom:8px">❌ {{ createResult.errors.length }} 个失败</div>
        <div v-for="e in createResult.errors" :key="e.account_id" style="font-size:13px;color:var(--text-muted)">
          @{{ e.account_id }}: {{ e.error }}
        </div>
      </div>
      <div style="margin-top:16px">
        <button class="btn btn-primary" @click="$router.push('/growth')">去大盘查看</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { growthApi } from '../api'

const step = ref(1)
const loadingAccounts = ref(false)
const accounts = ref([])
const adAccounts = ref([])
const selected = ref([])
const searchKw = ref('')
const filterStatus = ref('IDLE')
const creating = ref(false)
const createResult = ref(null)

const config = ref({
  target_cost_per_10k: 35,
  ad_account_id: '',
})

const materialPool = ref([])           // 当前广告户下的可用素材
const materialChoice = ref({})         // { [tk_account_id]: material_id | null }
const accountsById = computed(() => Object.fromEntries(accounts.value.map(a => [a.account_id, a])))

// 推荐素材：该广告户下 sample_count>=3 且 avg_cost_per_10k 最低
const recommendedMaterialId = computed(() => {
  const qualified = materialPool.value.filter(m => (m.sample_count || 0) >= 3 && m.avg_cost_per_10k)
  if (!qualified.length) return null
  return qualified.sort((a, b) => a.avg_cost_per_10k - b.avg_cost_per_10k)[0].id
})

// 所有 TK 都确认过素材（null = 使用推荐，已算选好；但如果没有推荐也没手选，禁用下一步）
const canProceedStep2 = computed(() => {
  if (!config.value.ad_account_id) return false
  if (!materialPool.value.length) return false
  for (const accId of selected.value) {
    const choice = materialChoice.value[accId]
    if (choice === undefined) return false
    if (choice === null && !recommendedMaterialId.value) return false
  }
  return true
})

function materialLabel(id) {
  const m = materialPool.value.find(x => x.id === id)
  if (!m) return `素材 #${id}`
  const cost = m.avg_cost_per_10k ? `$${m.avg_cost_per_10k.toFixed(1)}/10k` : '无样本'
  const samples = m.sample_count || 0
  return `${(m.item_id || m.video_id || '').slice(0, 14)}… · ${cost} · n=${samples}`
}

async function loadMaterialPool() {
  materialPool.value = []
  materialChoice.value = {}
  if (!config.value.ad_account_id) return
  try {
    const res = await growthApi.listCreatives({
      advertiser_id: config.value.ad_account_id,
      authorized_only: true,
      page_size: 100,
    })
    materialPool.value = res.materials || []
    // 默认推荐：都设为 null（= 用 recommendedMaterialId 推荐）
    for (const accId of selected.value) {
      materialChoice.value[accId] = null
    }
  } catch (e) {
    console.error(e)
  }
}

const availableAccounts = computed(() =>
  accounts.value.filter(a => {
    if (filterStatus.value && a.status !== filterStatus.value) return false
    if (searchKw.value && !a.account_id.toLowerCase().includes(searchKw.value.toLowerCase())) return false
    return true
  })
)

function toggleSelect(id) {
  const idx = selected.value.indexOf(id)
  if (idx >= 0) selected.value.splice(idx, 1)
  else selected.value.push(id)
}

function estimateBudget(accId) {
  const acc = accounts.value.find(a => a.account_id === accId)
  if (!acc) return '—'
  const increment = Math.max(0, acc.target_follower_count - (acc.follower_count || 0))
  // 与后端 BudgetCalculator.BUFFER_MULTIPLIER=1.0 一致，不再 ×1.2
  return (increment * (config.value.target_cost_per_10k / 10000)).toFixed(2)
}

async function loadAccounts() {
  loadingAccounts.value = true
  try {
    const res = await growthApi.listTkAccounts({ page_size: 100 })
    accounts.value = res.accounts || []
  } catch (e) {
    console.error(e)
  } finally {
    loadingAccounts.value = false
  }
}

async function loadAdAccounts() {
  try {
    const res = await growthApi.listAdAccounts()
    adAccounts.value = res.accounts || []
  } catch (e) {
    console.error(e)
  }
}

async function doCreate() {
  creating.value = true
  createResult.value = null
  try {
    const assignments = selected.value.map(accId => ({
      tk_account_id: accId,
      // null/undefined → 后端用推荐规则；否则用手选
      material_id: materialChoice.value[accId] || undefined,
    }))
    const res = await growthApi.createCampaigns({
      assignments,
      ad_account_id: config.value.ad_account_id || undefined,
      target_cost_per_10k: config.value.target_cost_per_10k,
    })
    createResult.value = res
  } catch (e) {
    alert('创建失败: ' + (e.response?.data?.detail || e.message || e))
  } finally {
    creating.value = false
  }
}

onMounted(() => {
  loadAccounts()
  loadAdAccounts()
})
</script>

<style scoped>
.account-card {
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.account-card:hover { border-color: var(--primary); background: var(--bg); }
.account-card.selected { border-color: var(--primary); background: color-mix(in srgb, var(--primary) 8%, transparent); }
.step { padding: 6px 12px; border-radius: 20px; background: var(--bg); color: var(--text-muted); font-size: 13px; }
.step.active { background: var(--primary); color: #fff; }
</style>
