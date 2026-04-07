<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">🗂️ 创意分组</div>
        <div class="page-subtitle">按内容方向分组 · 组内汇总 · 组间对比</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <select v-model="filter.days" @change="loadAll" style="width:100px">
          <option value="7">近7天</option>
          <option value="14">近14天</option>
          <option value="30">近30天</option>
        </select>
        <button class="btn btn-primary" @click="showCreateModal = true">+ 新建分组</button>
      </div>
    </div>

    <!-- 主体：左侧分组列表 + 右侧内容 -->
    <div class="layout-main">

      <!-- 左：分组列表 -->
      <div class="groups-sidebar">
        <div class="sidebar-title">我的分组</div>

        <div
          v-for="g in groups" :key="g.id"
          class="group-item"
          :class="{ active: activeGroupId === g.id }"
          @click="selectGroup(g)"
        >
          <div class="group-dot" :style="{ background: g.color }"></div>
          <div class="group-info">
            <div class="group-name">{{ g.name }}</div>
            <div class="group-meta">{{ g.total_creatives || 0 }} 个创意</div>
          </div>
          <div class="group-actions" @click.stop>
            <button class="icon-btn" @click="openEdit(g)" title="编辑">✏️</button>
            <button class="icon-btn danger" @click="deleteGroup(g)" title="删除">🗑️</button>
          </div>
        </div>

        <div v-if="!groups.length" class="empty-groups">
          <div>暂无分组</div>
          <div style="font-size:11px;margin-top:4px">点击「新建分组」开始</div>
        </div>

        <!-- 对比模式按钮 -->
        <div class="compare-section" v-if="groups.length >= 2">
          <div class="sidebar-title" style="margin-top:16px">对比模式</div>
          <div v-for="g in groups" :key="'cmp-'+g.id" class="compare-check">
            <label>
              <input type="checkbox" :value="g.id" v-model="compareIds" :disabled="compareIds.length >= 3 && !compareIds.includes(g.id)">
              <span class="compare-dot" :style="{ background: g.color }"></span>
              {{ g.name }}
            </label>
          </div>
          <button
            class="btn btn-primary"
            style="width:100%;margin-top:8px;font-size:12px"
            :disabled="compareIds.length < 2"
            @click="runCompare"
          >
            {{ compareIds.length < 2 ? '选 2-3 个分组' : `对比 ${compareIds.length} 个分组` }}
          </button>
        </div>
      </div>

      <!-- 右：内容区域 -->
      <div class="content-area">

        <!-- 对比视图 -->
        <div v-if="compareMode && compareData.length">
          <div class="card">
            <div class="card-header">
              <span>📊 分组对比</span>
              <button class="btn btn-ghost" style="font-size:12px" @click="compareMode=false">✕ 退出对比</button>
            </div>
            <div class="compare-grid" :style="{ gridTemplateColumns: `repeat(${compareData.length}, 1fr)` }">
              <div v-for="g in compareData" :key="g.group_id" class="compare-col">
                <div class="compare-header" :style="{ borderColor: g.color }">
                  <span class="compare-dot-lg" :style="{ background: g.color }"></span>
                  <span class="compare-name">{{ g.name }}</span>
                </div>
                <div class="compare-metric" v-for="m in compareMetrics(g)" :key="m.label">
                  <div class="m-label">{{ m.label }}</div>
                  <div class="m-value" :class="m.cls">{{ m.value }}</div>
                </div>
              </div>
            </div>
            <!-- 胜出标注 -->
            <div class="winner-row">
              <div v-for="metric in winnerMetrics" :key="metric.key" class="winner-item">
                <span class="winner-label">{{ metric.label }}</span>
                <span class="winner-badge" :style="{ background: getWinner(metric.key)?.color }">
                  {{ getWinner(metric.key)?.name || '-' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 分组详情视图 -->
        <div v-else-if="activeGroup">
          <!-- 分组统计卡片 -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-label">💰 总花费</div>
              <div class="stat-value">${{ fmt(activeStats.metrics?.total_spend) }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">📈 总展示</div>
              <div class="stat-value">{{ fmtNum(activeStats.metrics?.total_impressions) }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">🎯 平均 CTR</div>
              <div class="stat-value" :class="activeStats.metrics?.avg_ctr > 1 ? 'good' : ''">
                {{ fmtPct(activeStats.metrics?.avg_ctr) }}
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-label">🪝 Hook Rate</div>
              <div class="stat-value" :class="activeStats.metrics?.avg_hook_rate > 0.3 ? 'good' : ''">
                {{ fmtPct(activeStats.metrics?.avg_hook_rate) }}
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-label">⏱️ Hold Rate</div>
              <div class="stat-value">{{ fmtPct(activeStats.metrics?.avg_hold_rate) }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">🛒 总转化</div>
              <div class="stat-value">{{ activeStats.metrics?.total_conversion || 0 }}</div>
            </div>
          </div>

          <!-- 最佳创意 -->
          <div v-if="activeStats.metrics?.best_creative" class="card" style="margin-bottom:12px">
            <div class="card-header">🏆 最佳创意（花费最高）</div>
            <div class="best-creative">
              <div class="bc-id">{{ activeStats.metrics.best_creative.video_id }}</div>
              <div class="bc-name">{{ activeStats.metrics.best_creative.creative_name || '-' }}</div>
              <div class="bc-metrics">
                💰 ${{ fmt(activeStats.metrics.best_creative.spend) }}
                · CTR {{ fmtPct(activeStats.metrics.best_creative.ctr) }}
              </div>
            </div>
          </div>

          <!-- 分组内创意列表 -->
          <div class="card">
            <div class="card-header">
              <span>
                <span class="group-dot-sm" :style="{ background: activeGroup.color }"></span>
                {{ activeGroup.name }} 的创意（{{ groupItems.length }}）
              </span>
              <button class="btn btn-ghost" style="font-size:12px" @click="showAddItems=true">+ 添加创意</button>
            </div>

            <div v-if="!groupItems.length" class="empty-state" style="padding:30px 0">
              <div class="empty-icon">🎬</div>
              <div>还没有创意，点击「+ 添加创意」</div>
            </div>
            <table v-else style="font-size:12px">
              <thead>
                <tr>
                  <th>视频 ID</th>
                  <th>创意名</th>
                  <th>花费</th>
                  <th>展示</th>
                  <th>CTR</th>
                  <th>Hook Rate</th>
                  <th>状态</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in groupItems" :key="item.video_id">
                  <td style="font-family:monospace;font-size:11px">{{ item.video_id?.slice(-8) }}</td>
                  <td style="max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" :title="item.creative_name">
                    {{ item.creative_name || '-' }}
                  </td>
                  <td>${{ fmt(item.total_spend) }}</td>
                  <td>{{ fmtNum(item.total_impression) }}</td>
                  <td :class="item.latest_ctr > 1 ? 'good' : ''">{{ fmtPct(item.latest_ctr) }}</td>
                  <td :class="item.latest_hook_rate > 0.3 ? 'good' : ''">{{ fmtPct(item.latest_hook_rate) }}</td>
                  <td>
                    <span class="lifecycle-badge" :class="item.lifecycle_stage?.toLowerCase()">
                      {{ lifecycleLabel(item.lifecycle_stage) }}
                    </span>
                  </td>
                  <td>
                    <button class="icon-btn danger" @click="removeItem(item.video_id)" title="移出分组">✕</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-main">
          <div class="empty-icon">🗂️</div>
          <div>从左侧选择一个分组</div>
          <div style="font-size:12px;color:var(--text-muted);margin-top:8px">或新建分组开始管理创意</div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑分组弹窗 -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click.self="closeModals">
      <div class="modal card">
        <div class="modal-title">{{ showEditModal ? '编辑分组' : '新建分组' }}</div>
        <div class="form-row">
          <label>分组名称</label>
          <input v-model="form.name" placeholder="如：美妆测评、开箱流、UGC素人" />
        </div>
        <div class="form-row">
          <label>描述（可选）</label>
          <input v-model="form.description" placeholder="分组说明" />
        </div>
        <div class="form-row">
          <label>标签颜色</label>
          <div class="color-picker">
            <div
              v-for="c in colorOptions" :key="c"
              class="color-dot"
              :class="{ selected: form.color === c }"
              :style="{ background: c }"
              @click="form.color = c"
            ></div>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-ghost" @click="closeModals">取消</button>
          <button class="btn btn-primary" @click="saveGroup" :disabled="!form.name">
            {{ showEditModal ? '保存' : '创建' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 添加创意弹窗 -->
    <div v-if="showAddItems" class="modal-overlay" @click.self="showAddItems=false">
      <div class="modal card" style="width:600px;max-width:95vw">
        <div class="modal-title">添加创意到「{{ activeGroup?.name }}」</div>
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:12px">
          从下方选择创意，或直接输入 video_id
        </div>
        <!-- 搜索框 -->
        <input v-model="addSearch" placeholder="搜索创意名称 或 输入 video_id..." style="width:100%;margin-bottom:12px" />
        <!-- 创意列表 -->
        <div class="add-items-list">
          <div
            v-for="c in filteredCreatives" :key="c.video_id"
            class="add-item"
            :class="{ selected: addSelected.includes(c.video_id) }"
            @click="toggleAddItem(c.video_id)"
          >
            <input type="checkbox" :checked="addSelected.includes(c.video_id)" readonly />
            <div class="add-item-info">
              <div class="add-item-name">{{ c.creative_name || c.video_id }}</div>
              <div class="add-item-meta">花费 ${{ fmt(c.total_spend) }} · {{ lifecycleLabel(c.lifecycle_stage) }}</div>
            </div>
          </div>
          <div v-if="!filteredCreatives.length" style="padding:20px;text-align:center;color:var(--text-muted)">
            没有匹配的创意
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-ghost" @click="showAddItems=false">取消</button>
          <button class="btn btn-primary" @click="confirmAddItems" :disabled="!addSelected.length">
            添加 {{ addSelected.length }} 个创意
          </button>
        </div>
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

// ── state ──────────────────────────────────────────
const groups = ref([])
const activeGroupId = ref(null)
const activeGroup = ref(null)
const activeStats = ref({})
const groupItems = ref([])
const compareIds = ref([])
const compareData = ref([])
const compareMode = ref(false)
const allCreatives = ref([])

const showCreateModal = ref(false)
const showEditModal = ref(false)
const showAddItems = ref(false)
const addSearch = ref('')
const addSelected = ref([])

const form = ref({ name: '', description: '', color: '#6366f1' })

const colorOptions = [
  '#6366f1', '#3b82f6', '#10b981', '#f59e0b',
  '#ef4444', '#ec4899', '#8b5cf6', '#06b6d4',
]

const winnerMetrics = [
  { key: 'total_spend', label: '花费最高', higher: true },
  { key: 'avg_ctr', label: 'CTR 最优', higher: true },
  { key: 'avg_hook_rate', label: 'Hook Rate 最优', higher: true },
  { key: 'total_conversion', label: '转化最多', higher: true },
]

// ── helpers ────────────────────────────────────────
const fmt = v => v ? Number(v).toFixed(2) : '0.00'
const fmtNum = v => v ? Number(v).toLocaleString() : '0'
const fmtPct = v => v ? (Number(v) * 100).toFixed(2) + '%' : '0%'

const lifecycleLabel = s => ({
  WARM_UP: '🌱 冷启动', GROWTH: '📈 上升', PEAK: '⭐ 峰值', DECAY: '📉 衰退'
}[s] || s || '-')

// ── computed ───────────────────────────────────────
const filteredCreatives = computed(() => {
  if (!addSearch.value) return allCreatives.value.slice(0, 50)
  const q = addSearch.value.toLowerCase()
  return allCreatives.value.filter(c =>
    (c.creative_name || '').toLowerCase().includes(q) || c.video_id.includes(q)
  ).slice(0, 50)
})

const compareMetrics = (g) => [
  { label: '💰 总花费', value: `$${fmt(g.metrics?.total_spend)}`, cls: '' },
  { label: '👁️ 总展示', value: fmtNum(g.metrics?.total_impressions), cls: '' },
  { label: '🎯 平均CTR', value: fmtPct(g.metrics?.avg_ctr), cls: g.metrics?.avg_ctr > 0.01 ? 'good' : '' },
  { label: '🪝 Hook Rate', value: fmtPct(g.metrics?.avg_hook_rate), cls: g.metrics?.avg_hook_rate > 0.3 ? 'good' : '' },
  { label: '⏱️ Hold Rate', value: fmtPct(g.metrics?.avg_hold_rate), cls: '' },
  { label: '🛒 总转化', value: g.metrics?.total_conversion || 0, cls: '' },
  { label: '📦 创意数', value: g.total_creatives || 0, cls: '' },
]

const getWinner = (metricKey) => {
  if (!compareData.value.length) return null
  const higher = winnerMetrics.find(m => m.key === metricKey)?.higher
  let best = null
  for (const g of compareData.value) {
    const val = g.metrics?.[metricKey] || 0
    if (!best || (higher ? val > best.val : val < best.val)) {
      best = { ...g, val }
    }
  }
  return best
}

// ── loaders ────────────────────────────────────────
async function loadAll() {
  try {
    const data = await api.get('/creative-groups')
    groups.value = data.items || data.groups || data || []
  } catch (e) { groups.value = [] }
}


async function selectGroup(g) {
  activeGroupId.value = g.id
  activeGroup.value = g
  compareMode.value = false
  await Promise.all([loadGroupStats(g.id), loadGroupItems(g.id)])
}

async function loadGroupStats(groupId) {
  try {
    const data = await api.get(`/creative-groups/${groupId}/stats`, {
      params: { days: filter.value.days }
    })
    activeStats.value = data
  } catch { activeStats.value = {} }
}

async function loadGroupItems(groupId) {
  try {
    const data = await api.get(`/creative-groups/${groupId}/items`)
    groupItems.value = data.items || data || []
  } catch { groupItems.value = [] }
}

async function runCompare() {
  try {
    const ids = compareIds.value.join(',')
    const data = await api.get('/creative-groups/compare', {
      params: { group_ids: ids, days: filter.value.days }
    })
    compareData.value = data.groups || []
    compareMode.value = true
  } catch (e) { console.error(e) }
}

// ── CRUD ──────────────────────────────────────────
async function saveGroup() {
  const payload = {
    name: form.value.name,
    description: form.value.description,
    color: form.value.color,
  }

  try {
    if (showEditModal.value) {
      await api.put(`/creative-groups/${activeGroup.value.id}`, payload)
    } else {
      await api.post('/creative-groups', payload)
    }
    closeModals()
    await loadAll()
  } catch (e) { console.error(e) }
}

function openEdit(g) {
  activeGroup.value = g
  form.value = { name: g.name, description: g.description || '', color: g.color }
  showEditModal.value = true
}

async function deleteGroup(g) {
  if (!confirm(`确定删除分组「${g.name}」？`)) return
  try {
    await api.delete(`/creative-groups/${g.id}`)
    if (activeGroupId.value === g.id) {
      activeGroupId.value = null
      activeGroup.value = null
    }
    await loadAll()
  } catch (e) { console.error(e) }
}

async function removeItem(videoId) {
  try {
    await api.delete(`/creative-groups/${activeGroupId.value}/items/${videoId}`)
    await loadGroupItems(activeGroupId.value)
    await loadGroupStats(activeGroupId.value)
    await loadAll()
  } catch (e) { console.error(e) }
}

// 添加创意
async function openAddItems() {
  addSearch.value = ''
  addSelected.value = []
  if (!allCreatives.value.length) {
    const data = await api.get('/creatives', { params: { page_size: 200 } })
    allCreatives.value = data.items || data || []
  }
  showAddItems.value = true
}

function toggleAddItem(videoId) {
  const idx = addSelected.value.indexOf(videoId)
  if (idx >= 0) addSelected.value.splice(idx, 1)
  else addSelected.value.push(videoId)
}

async function confirmAddItems() {
  try {
    await api.post(`/creative-groups/${activeGroupId.value}/items`, {
      video_ids: addSelected.value,
    })
    showAddItems.value = false
    await loadGroupItems(activeGroupId.value)
    await loadGroupStats(activeGroupId.value)
    await loadAll()
  } catch (e) { console.error(e) }
}

function closeModals() {
  showCreateModal.value = false
  showEditModal.value = false
  form.value = { name: '', description: '', color: '#6366f1' }
}

// 监听加载按钮
const origShowAddItems = showAddItems
watch(showAddItems, async (val) => {
  if (val && !allCreatives.value.length) {
    try {
      const data = await api.get('/creatives', { params: { page_size: 200 } })
      allCreatives.value = data.items || data || []
    } catch {}
  }
})

import { watch } from 'vue'

onMounted(loadAll)
</script>

<style scoped>
.layout-main { display: grid; grid-template-columns: 240px 1fr; gap: 16px; }
@media (max-width: 768px) { .layout-main { grid-template-columns: 1fr; } }

.groups-sidebar { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 12px; height: fit-content; }
.sidebar-title { font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }

.group-item { display: flex; align-items: center; gap: 8px; padding: 8px; border-radius: 6px; cursor: pointer; transition: background 0.15s; margin-bottom: 2px; }
.group-item:hover { background: var(--bg-hover); }
.group-item.active { background: rgba(99,102,241,0.15); }
.group-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.group-info { flex: 1; min-width: 0; }
.group-name { font-size: 13px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.group-meta { font-size: 11px; color: var(--text-muted); }
.group-actions { display: none; gap: 4px; }
.group-item:hover .group-actions { display: flex; }
.icon-btn { background: none; border: none; cursor: pointer; padding: 2px 4px; border-radius: 3px; font-size: 13px; }
.icon-btn:hover { background: var(--bg-hover); }
.icon-btn.danger:hover { color: var(--danger); }
.empty-groups { text-align: center; padding: 20px 0; font-size: 12px; color: var(--text-muted); }

.compare-section { border-top: 1px solid var(--border); padding-top: 12px; }
.compare-check { padding: 4px 0; font-size: 12px; }
.compare-check label { display: flex; align-items: center; gap: 6px; cursor: pointer; }
.compare-dot { width: 8px; height: 8px; border-radius: 50%; }

.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 12px; }
@media (max-width: 900px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px; }
.stat-label { font-size: 11px; color: var(--text-muted); margin-bottom: 6px; }
.stat-value { font-size: 20px; font-weight: 700; }
.stat-value.good { color: var(--success); }

.best-creative { padding: 8px 16px; display: flex; align-items: center; gap: 12px; }
.bc-id { font-family: monospace; font-size: 11px; color: var(--text-muted); }
.bc-name { flex: 1; font-size: 13px; }
.bc-metrics { font-size: 12px; color: var(--text-muted); }

table { width: 100%; border-collapse: collapse; }
th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); font-size: 12px; }
th { color: var(--text-muted); font-size: 11px; }
td.good { color: var(--success); }
.lifecycle-badge { padding: 2px 6px; border-radius: 4px; font-size: 10px; background: var(--bg-hover); }

.compare-grid { display: grid; gap: 0; }
.compare-col { padding: 16px; border-right: 1px solid var(--border); }
.compare-col:last-child { border-right: none; }
.compare-header { display: flex; align-items: center; gap: 8px; border-bottom: 3px solid; padding-bottom: 10px; margin-bottom: 12px; }
.compare-dot-lg { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.compare-name { font-size: 14px; font-weight: 600; }
.compare-metric { padding: 6px 0; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; }
.m-label { font-size: 12px; color: var(--text-muted); }
.m-value { font-size: 13px; font-weight: 500; }
.m-value.good { color: var(--success); }
.winner-row { display: flex; flex-wrap: wrap; gap: 12px; padding: 12px 16px; background: var(--bg); }
.winner-item { display: flex; align-items: center; gap: 8px; font-size: 12px; }
.winner-label { color: var(--text-muted); }
.winner-badge { padding: 2px 8px; border-radius: 4px; color: white; font-size: 11px; font-weight: 600; }

.empty-main { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 300px; color: var(--text-muted); }
.empty-icon { font-size: 48px; margin-bottom: 12px; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { width: 480px; max-width: 95vw; padding: 24px; }
.modal-title { font-size: 16px; font-weight: 600; margin-bottom: 20px; }
.form-row { margin-bottom: 14px; }
.form-row label { display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 6px; }
.form-row input { width: 100%; }
.color-picker { display: flex; gap: 8px; flex-wrap: wrap; }
.color-dot { width: 24px; height: 24px; border-radius: 50%; cursor: pointer; border: 2px solid transparent; transition: border 0.15s; }
.color-dot.selected { border-color: white; }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 20px; }

.add-items-list { max-height: 300px; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; }
.add-item { display: flex; align-items: center; gap: 10px; padding: 10px 12px; cursor: pointer; border-bottom: 1px solid var(--border); transition: background 0.15s; }
.add-item:hover { background: var(--bg-hover); }
.add-item.selected { background: rgba(99,102,241,0.1); }
.add-item-name { font-size: 13px; }
.add-item-meta { font-size: 11px; color: var(--text-muted); }

.group-dot-sm { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
</style>
