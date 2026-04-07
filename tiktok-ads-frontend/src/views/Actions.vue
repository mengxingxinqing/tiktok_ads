<template>
  <div class="page">
    <!-- 头部 -->
    <div class="page-header">
      <div>
        <div class="page-title">⚡ 快捷操作</div>
        <div class="page-subtitle">投手专用 — 快速投放、批量管控、实时查看</div>
      </div>
    </div>

    <!-- ══ Toast ══ -->
    <div v-if="toast.show" :class="['toast', toast.type]">{{ toast.msg }}</div>

    <!-- ══ 改预算弹窗 ══ -->
    <div v-if="budgetModal.show" class="modal-overlay" @click.self="budgetModal.show=false">
      <div class="modal card" style="width:320px">
        <div style="font-size:15px;font-weight:700;margin-bottom:12px">💰 修改预算</div>
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:4px">{{ budgetModal.name }}</div>
        <div style="margin-bottom:12px">
          <label style="font-size:12px;color:var(--text-muted)">新日预算（USD）</label>
          <input v-model.number="budgetModal.budget" type="number" min="1" placeholder="输入新预算"
            style="width:100%;margin-top:4px" />
        </div>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button class="btn btn-ghost" style="padding:4px 14px" @click="budgetModal.show=false">取消</button>
          <button class="btn btn-primary" style="padding:4px 14px" :disabled="budgetModal.loading" @click="confirmBudget">
            {{ budgetModal.loading ? '提交中…' : '确认' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ══ 上半部分：两栏 ══ -->
    <div class="two-col">
      <!-- 左：上传创意 + 创建投放 -->
      <div class="card">
        <div class="card-section-title">🎬 上传创意 & 创建投放</div>

        <!-- ① 上传视频 -->
        <div class="step-row">
          <div class="step-num">①</div>
          <div class="step-content">
            <div class="step-label">上传视频</div>
            <input type="file" ref="videoInput" accept="video/*" style="display:none" @change="onVideoSelected" />
            <button class="btn btn-ghost" style="padding:4px 12px;font-size:12px" @click="videoInput?.click()">
              {{ createForm.videoFile ? '✅ ' + createForm.videoFile.name : '选择视频文件' }}
            </button>
            <div v-if="uploadProgress > 0 && uploadProgress < 100" style="margin-top:6px">
              <div class="progress-bar"><div class="progress-fill" :style="{width:uploadProgress+'%'}"></div></div>
              <div style="font-size:11px;color:var(--text-muted);margin-top:2px">上传中 {{ uploadProgress }}%</div>
            </div>
          </div>
        </div>

        <!-- ② 选择 Campaign -->
        <div class="step-row">
          <div class="step-num">②</div>
          <div class="step-content">
            <div class="step-label">选择 Campaign</div>
            <select v-model="createForm.campaignId" style="width:100%;font-size:12px">
              <option value="">— 选择 Campaign —</option>
              <option v-for="c in campaigns" :key="c.campaign_id" :value="c.campaign_id">{{ c.campaign_name }}</option>
            </select>
          </div>
        </div>

        <!-- ③ 广告名 -->
        <div class="step-row">
          <div class="step-num">③</div>
          <div class="step-content">
            <div class="step-label">广告名称</div>
            <input v-model="createForm.adName" placeholder="输入广告名称" style="width:100%" />
          </div>
        </div>

        <!-- ④ 一键投放 -->
        <div class="step-row">
          <div class="step-num">④</div>
          <div class="step-content">
            <div class="step-label">一键投放</div>
            <button class="btn btn-primary" style="padding:6px 18px" :disabled="creating || !createForm.videoFile || !createForm.campaignId" @click="createAd">
              {{ creating ? '⏳ 创建中…' : '🚀 创建' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 右：批量操作 -->
      <div class="card">
        <div class="card-section-title">⚙️ 批量操作</div>
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:12px">
          先在下方列表勾选广告组，再执行批量操作
        </div>

        <div style="margin-bottom:8px;font-size:13px;color:var(--text-muted)">
          已选 <strong style="color:var(--text)">{{ selectedAdgroups.length }}</strong> 个广告组
        </div>

        <div style="display:flex;flex-direction:column;gap:8px">
          <button class="btn btn-ghost" :disabled="!selectedAdgroups.length || batchLoading" @click="batchAction('pause')" style="justify-content:flex-start;gap:8px">
            {{ batchLoading==='pause'?'⏳ 处理中…':'⏸️ 批量暂停' }}
          </button>
          <button class="btn btn-ghost" :disabled="!selectedAdgroups.length || batchLoading" @click="batchAction('resume')" style="justify-content:flex-start;gap:8px">
            {{ batchLoading==='resume'?'⏳ 处理中…':'▶️ 批量恢复' }}
          </button>
          <div style="display:flex;gap:6px;align-items:center">
            <input v-model.number="batchBudget" type="number" min="1" placeholder="新预算 $" style="width:100px;font-size:12px" />
            <button class="btn btn-ghost" :disabled="!selectedAdgroups.length || !batchBudget || batchLoading" @click="batchAction('budget')" style="gap:8px">
              {{ batchLoading==='budget'?'⏳ 处理中…':'💰 批量调预算' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ 当前投放状态 ══ -->
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <div class="card-section-title" style="margin-bottom:0">📊 当前投放状态</div>
        <button class="btn btn-ghost" style="padding:4px 12px;font-size:12px" :disabled="loadingCampaigns" @click="loadCampaigns">
          {{ loadingCampaigns ? '加载中…' : '🔄 刷新' }}
        </button>
      </div>

      <div v-if="loadingCampaigns" style="padding:30px;text-align:center;color:var(--text-muted)">加载中…</div>
      <div v-else-if="!campaigns.length" class="empty-state">
        <div class="empty-icon">📋</div>
        <div>暂无 Campaign 数据</div>
      </div>

      <div v-for="camp in campaigns" :key="camp.campaign_id" class="campaign-item">
        <!-- Campaign 行 -->
        <div class="campaign-row" @click="toggleCampaign(camp.campaign_id)">
          <span class="expand-icon">{{ expandedCampaigns.has(camp.campaign_id) ? '▼' : '▶' }}</span>
          <span style="font-weight:600;flex:1">{{ camp.campaign_name }}</span>
          <span :class="['badge', camp.operation_status==='ENABLE'?'badge-success':'badge-info']" style="margin-right:8px">
            {{ camp.operation_status==='ENABLE'?'✅ 投放中':'⏸️ 已暂停' }}
          </span>
          <div style="display:flex;gap:4px" @click.stop>
            <button class="btn btn-ghost action-sm" :disabled="campLoading[camp.campaign_id]" @click="campStatusAction(camp,'DISABLE')">
              {{ campLoading[camp.campaign_id]==='pause'?'…':'⏸️' }}
            </button>
            <button class="btn btn-ghost action-sm" :disabled="campLoading[camp.campaign_id]" @click="campStatusAction(camp,'ENABLE')">
              {{ campLoading[camp.campaign_id]==='resume'?'…':'▶️' }}
            </button>
          </div>
        </div>

        <!-- 展开的广告组列表 -->
        <div v-if="expandedCampaigns.has(camp.campaign_id)" class="adgroup-list">
          <div v-if="adgroupLoading[camp.campaign_id]" style="padding:12px;text-align:center;color:var(--text-muted);font-size:12px">加载广告组…</div>
          <div v-else-if="!adgroups[camp.campaign_id]?.length" style="padding:12px;text-align:center;color:var(--text-muted);font-size:12px">暂无广告组</div>
          <div v-else v-for="ag in adgroups[camp.campaign_id]" :key="ag.adgroup_id" class="adgroup-row">
            <!-- 勾选 -->
            <input type="checkbox" :value="ag.adgroup_id" v-model="selectedAdgroups" style="margin-right:6px;cursor:pointer" />
            <!-- 名称 -->
            <span style="flex:1;font-size:12px">{{ ag.adgroup_name }}</span>
            <!-- 指标 -->
            <div class="ag-metrics">
              <span :class="['badge', ag.operation_status==='ENABLE'?'badge-success':'badge-info']" style="font-size:10px">
                {{ ag.operation_status==='ENABLE'?'✅':'⏸️' }}
              </span>
              <span class="metric-item" title="日预算">${{ fmt2(ag.budget||ag.daily_budget) }}</span>
              <span class="metric-item" title="今日花费" style="color:var(--warning)">${{ fmt2(ag.today_spend||ag.spend) }}</span>
              <span class="metric-item" title="今日GMV" style="color:var(--success)">${{ fmt2(ag.today_gmv||ag.revenue) }}</span>
              <span class="metric-item" title="ROI" :style="{color:roi(ag)>=1?'var(--success)':'var(--danger)'}">
                ROI {{ fmt2(roi(ag)) }}
              </span>
            </div>
            <!-- 操作 -->
            <div style="display:flex;gap:3px" @click.stop>
              <button class="btn btn-ghost action-sm" :disabled="rowLoading[ag.adgroup_id]" @click="adgroupAction(ag,'DISABLE')" title="暂停">
                {{ rowLoading[ag.adgroup_id]==='pause'?'…':'⏸️' }}
              </button>
              <button class="btn btn-ghost action-sm" :disabled="rowLoading[ag.adgroup_id]" @click="adgroupAction(ag,'ENABLE')" title="恢复">
                {{ rowLoading[ag.adgroup_id]==='resume'?'…':'▶️' }}
              </button>
              <button class="btn btn-ghost action-sm" style="color:var(--warning)" :disabled="rowLoading[ag.adgroup_id]" @click="openBudgetModal(ag)" title="改预算">
                💰
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { api } from '../api'

// ── Campaign & 广告组 ──
const campaigns = ref([])
const adgroups = reactive({})   // campaign_id → []
const loadingCampaigns = ref(false)
const adgroupLoading = reactive({})
const campLoading = reactive({})
const expandedCampaigns = ref(new Set())

// ── 创建投放 ──
const videoInput = ref(null)
const uploadProgress = ref(0)
const creating = ref(false)
const createForm = ref({ videoFile: null, campaignId: '', adName: '' })

// ── 批量操作 ──
const selectedAdgroups = ref([])
const batchBudget = ref(null)
const batchLoading = ref(false)

// ── 行级 loading ──
const rowLoading = reactive({})

// ── 预算弹窗 ──
const budgetModal = ref({ show: false, adgroupId: '', name: '', budget: 100, loading: false })

// ── Toast ──
const toast = ref({ show: false, msg: '', type: 'success' })
let toastTimer = null
function showToast(msg, type = 'success') {
  toast.value = { show: true, msg, type }
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value.show = false }, 3000)
}

// ── 格式化 ──
function fmt2(v) { return Number(v||0).toFixed(2) }
function roi(ag) {
  const spend = ag.today_spend||ag.spend||0
  const rev = ag.today_gmv||ag.revenue||0
  return spend > 0 ? rev/spend : 0
}

// ── 加载 Campaign ──
async function loadCampaigns() {
  loadingCampaigns.value = true
  try {
    const res = await api.get('/gmvmax/campaigns')
    campaigns.value = res.data?.items || res.items || res.data || res || []
  } catch (e) { console.error('Load campaigns failed', e); campaigns.value = [] }
  finally { loadingCampaigns.value = false }
}

// ── 展开/折叠 Campaign ──
async function toggleCampaign(id) {
  if (expandedCampaigns.value.has(id)) {
    expandedCampaigns.value.delete(id)
    return
  }
  expandedCampaigns.value.add(id)
  if (!adgroups[id]) {
    adgroupLoading[id] = true
    try {
      const res = await api.get(`/gmvmax/campaigns/${id}/adgroups`)
      adgroups[id] = res.data?.items || res.items || res.data || res || []
    } catch (e) { console.error('Load adgroups failed', e); adgroups[id] = [] }
    finally { adgroupLoading[id] = false }
  }
}

// ── Campaign 状态操作 ──
async function campStatusAction(camp, status) {
  const key = camp.campaign_id
  campLoading[key] = status === 'DISABLE' ? 'pause' : 'resume'
  try {
    await api.post('/gmvmax/campaign/status', { campaign_id: key, status })
    camp.operation_status = status === 'DISABLE' ? 'DISABLE' : 'ENABLE'
    showToast(status === 'DISABLE' ? 'Campaign 已暂停 ✓' : 'Campaign 已恢复 ✓')
  } catch (e) { showToast('操作失败', 'error') }
  finally { delete campLoading[key] }
}

// ── 广告组状态操作 ──
async function adgroupAction(ag, status) {
  const key = ag.adgroup_id
  rowLoading[key] = status === 'DISABLE' ? 'pause' : 'resume'
  try {
    await api.post('/gmvmax/adgroup/status', { adgroup_id: key, status })
    ag.operation_status = status === 'DISABLE' ? 'DISABLE' : 'ENABLE'
    showToast(status === 'DISABLE' ? '已暂停 ✓' : '已恢复 ✓')
  } catch (e) { showToast('操作失败', 'error') }
  finally { delete rowLoading[key] }
}

// ── 预算弹窗 ──
function openBudgetModal(ag) {
  budgetModal.value = { show: true, adgroupId: ag.adgroup_id, name: ag.adgroup_name, budget: ag.budget||ag.daily_budget||100, loading: false }
}
async function confirmBudget() {
  const { adgroupId, budget } = budgetModal.value
  if (!budget || budget <= 0) { showToast('请输入有效预算', 'error'); return }
  budgetModal.value.loading = true
  try {
    await api.post('/gmvmax/adgroup/budget', { adgroup_id: adgroupId, budget })
    // 更新本地数据
    for (const list of Object.values(adgroups)) {
      const ag = list.find(a => a.adgroup_id === adgroupId)
      if (ag) { ag.budget = budget; ag.daily_budget = budget }
    }
    showToast(`预算已更新 $${budget} ✓`)
    budgetModal.value.show = false
  } catch (e) { showToast('修改失败', 'error') }
  finally { budgetModal.value.loading = false }
}

// ── 批量操作 ──
async function batchAction(type) {
  if (!selectedAdgroups.value.length) return
  batchLoading.value = type
  const ids = selectedAdgroups.value
  try {
    if (type === 'pause') {
      await Promise.all(ids.map(id => api.post('/gmvmax/adgroup/status', { adgroup_id: id, status: 'DISABLE' })))
      showToast(`已批量暂停 ${ids.length} 个广告组 ✓`)
      // 更新本地状态
      updateLocalAdgroupStatus(ids, 'DISABLE')
    } else if (type === 'resume') {
      await Promise.all(ids.map(id => api.post('/gmvmax/adgroup/status', { adgroup_id: id, status: 'ENABLE' })))
      showToast(`已批量恢复 ${ids.length} 个广告组 ✓`)
      updateLocalAdgroupStatus(ids, 'ENABLE')
    } else if (type === 'budget') {
      await Promise.all(ids.map(id => api.post('/gmvmax/adgroup/budget', { adgroup_id: id, budget: batchBudget.value })))
      showToast(`已批量更新预算 $${batchBudget.value} ✓`)
    }
    selectedAdgroups.value = []
  } catch (e) { showToast('批量操作失败', 'error') }
  finally { batchLoading.value = false }
}

function updateLocalAdgroupStatus(ids, status) {
  for (const list of Object.values(adgroups)) {
    for (const ag of list) {
      if (ids.includes(ag.adgroup_id)) ag.operation_status = status
    }
  }
}

// ── 上传视频 ──
function onVideoSelected(e) {
  const file = e.target.files?.[0]
  if (file) createForm.value.videoFile = file
}

// ── 创建投放 ──
async function createAd() {
  if (!createForm.value.videoFile || !createForm.value.campaignId) return
  creating.value = true
  uploadProgress.value = 0
  try {
    const formData = new FormData()
    formData.append('video', createForm.value.videoFile)
    formData.append('campaign_id', createForm.value.campaignId)
    if (createForm.value.adName) formData.append('ad_name', createForm.value.adName)

    await api.post('/gmvmax/upload-and-create', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        uploadProgress.value = Math.round((e.loaded / e.total) * 100)
      }
    })
    showToast('投放创建成功 🚀 ✓')
    createForm.value = { videoFile: null, campaignId: '', adName: '' }
    uploadProgress.value = 0
    // 刷新 Campaign 列表
    await loadCampaigns()
  } catch (e) { showToast('创建失败', 'error') }
  finally { creating.value = false }
}

onMounted(loadCampaigns)
</script>

<style scoped>
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
@media (max-width: 768px) {
  .two-col { grid-template-columns: 1fr; }
}

.card-section-title {
  font-size: 14px; font-weight: 700;
  color: var(--text); margin-bottom: 14px;
}

/* 步骤行 */
.step-row {
  display: flex; align-items: flex-start; gap: 10px;
  margin-bottom: 14px;
}
.step-num {
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--primary); color: #fff;
  font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 2px;
}
.step-content { flex: 1; }
.step-label { font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }

/* 进度条 */
.progress-bar {
  height: 4px; background: var(--border); border-radius: 2px; overflow: hidden;
}
.progress-fill {
  height: 100%; background: var(--primary); transition: width 0.2s;
}

/* Campaign 列表 */
.campaign-item {
  border: 1px solid var(--border);
  border-radius: 8px; margin-bottom: 8px; overflow: hidden;
}
.campaign-row {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 12px; cursor: pointer;
  background: var(--bg-hover);
  transition: background 0.1s;
}
.campaign-row:hover { background: rgba(99,102,241,0.08); }
.expand-icon { font-size: 10px; color: var(--text-muted); }

/* 广告组列表 */
.adgroup-list { padding: 0 6px 6px; }
.adgroup-row {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 6px; border-bottom: 1px solid var(--border);
  font-size: 12px;
}
.adgroup-row:last-child { border-bottom: none; }

.ag-metrics {
  display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-right: 6px;
}
.metric-item {
  font-size: 11px; color: var(--text-muted); white-space: nowrap;
}

.action-sm { padding: 2px 6px; font-size: 13px; min-width: 28px; }

/* Modal */
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; z-index:999; }
.modal { max-width:90vw; }

/* Toast */
.toast {
  position:fixed; bottom:24px; right:24px;
  padding:10px 18px; border-radius:8px; font-size:13px; font-weight:600;
  z-index:9999; animation:slideIn 0.2s ease;
}
.toast.success { background:var(--success); color:#fff; }
.toast.error   { background:var(--danger);  color:#fff; }

@keyframes slideIn { from { transform:translateY(20px); opacity:0 } to { transform:translateY(0); opacity:1 } }
</style>
