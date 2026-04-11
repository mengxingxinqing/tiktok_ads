<template>
  <div class="page">
    <!-- 头部 -->
    <div class="page-header" style="flex-wrap:wrap;gap:12px">
      <div>
        <div class="page-title">🎬 创意监控</div>
        <div class="page-subtitle">花费效率 · 转化表现 · 生命周期一览</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <select v-model="selectedShopId" @change="onShopChange" style="width:140px;font-size:12px">
          <option value="">🏪 全部店铺</option>
          <option v-for="s in globalFilterStore.shops" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
        <input type="date" v-model="dateRange.start" style="width:130px;font-size:12px" @change="loadCreatives" />
        <span style="color:var(--text-muted)">~</span>
        <input type="date" v-model="dateRange.end" style="width:130px;font-size:12px" @change="loadCreatives" />
        <select v-model="sortBy" @change="loadCreatives" style="width:110px;font-size:12px">
          <option value="total_spend">按花费</option>
          <option value="total_revenue">按 GMV</option>
          <option value="avg_roi">按 ROI</option>
          <option value="total_orders">按订单</option>
        </select>
        <button class="btn btn-primary" style="padding:4px 12px" @click="creativePage=1;loadCreatives()">刷新</button>
      </div>
    </div>

    <!-- 素材加热弹窗（Creative Boost Session） -->
    <div v-if="heatupModal.show" class="modal-overlay" @click.self="heatupModal.show=false">
      <div class="modal card" style="width:380px">
        <div style="font-size:15px;font-weight:700;margin-bottom:12px">🔥 素材加热</div>
        <div style="font-size:13px;margin-bottom:4px">{{ heatupModal.name }}</div>
        <div style="font-size:11px;color:var(--text-muted);margin-bottom:12px;font-family:monospace">
          Campaign: {{ heatupModal.campaignId }} / Item: {{ heatupModal.itemId }}
        </div>
        <div style="margin-bottom:10px">
          <label style="font-size:12px;color:var(--text-muted)">加热预算（USD，最低 $50）</label>
          <input v-model.number="heatupModal.budget" type="number" min="50" step="10" placeholder="50" style="width:100%;margin-top:4px" />
        </div>
        <div style="margin-bottom:12px">
          <label style="font-size:12px;color:var(--text-muted)">加热天数</label>
          <select v-model.number="heatupModal.days" style="width:100%;margin-top:4px">
            <option :value="1">1 天</option>
            <option :value="3">3 天</option>
            <option :value="7">7 天</option>
          </select>
        </div>
        <div style="background:var(--bg);border-radius:6px;padding:8px 12px;margin-bottom:12px;font-size:12px;color:var(--text-muted)">
          为该素材分配额外预算增加曝光，不影响 Campaign 整体预算设置。
        </div>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button class="btn btn-ghost" style="padding:4px 14px" @click="heatupModal.show=false">取消</button>
          <button class="btn btn-primary" style="padding:4px 14px" :disabled="heatupModal.loading" @click="confirmHeatup">
            {{ heatupModal.loading ? '提交中…' : '确认加热' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 预览弹窗 -->
    <div v-if="previewModal.show" class="modal-overlay" @click.self="previewModal.show=false">
      <div class="modal card preview-modal">
        <div class="preview-header">
          <div class="preview-title">{{ previewModal.name || '创意预览' }}</div>
          <button class="btn btn-ghost" style="padding:4px 8px;font-size:16px" @click="previewModal.show=false">✕</button>
        </div>
        <div class="preview-body">
          <!-- TikTok 视频（新窗口打开） -->
          <div v-if="previewModal.tiktokUrl" style="text-align:center">
            <img v-if="previewModal.imageUrl" :src="previewModal.imageUrl"
                 style="max-width:100%;max-height:50vh;border-radius:8px;object-fit:contain;cursor:pointer"
                 @click="window.open(previewModal.tiktokUrl, '_blank')" />
            <div style="margin-top:10px">
              <a :href="previewModal.tiktokUrl" target="_blank" class="btn btn-primary" style="padding:6px 16px;text-decoration:none;display:inline-flex;align-items:center;gap:6px">
                ▶ 在 TikTok 观看视频
              </a>
            </div>
          </div>
          <!-- 仅有商品图 -->
          <div v-else-if="previewModal.imageUrl" class="preview-image-wrap">
            <img :src="previewModal.imageUrl" style="max-width:100%;max-height:60vh;border-radius:8px;object-fit:contain" />
          </div>
          <div v-else class="preview-placeholder">
            <div style="font-size:48px;opacity:0.3">🎬</div>
            <div style="color:var(--text-muted);font-size:13px;margin-top:8px">暂无预览</div>
          </div>
        </div>
        <div class="preview-info" v-if="previewModal.item">
          <div class="preview-info-row">
            <div class="info-item"><span class="info-label">花费</span><span class="info-value">${{ fmt2(previewModal.item.total_spend||0) }}</span></div>
            <div class="info-item"><span class="info-label">转化</span><span class="info-value">{{ previewModal.item.total_orders||0 }}</span></div>
            <div class="info-item"><span class="info-label">ROAS</span><span class="info-value" :style="{color:roas(previewModal.item)>=1?'var(--success)':'var(--danger)'}">{{ fmt2(roas(previewModal.item)) }}</span></div>
            <div class="info-item"><span class="info-label">阶段</span><span :class="['badge', stageClassMap[previewModal.item.stage]||'badge-info']" style="font-size:11px">{{ stageLabelMap[previewModal.item.stage]||'—' }}</span></div>
          </div>
          <div style="font-family:monospace;font-size:11px;color:var(--text-muted);margin-top:6px">ID: {{ previewModal.id }}</div>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toast.show" :class="['toast', toast.type]">{{ toast.msg }}</div>

    <!-- 创意列表 -->
    <div class="card">
      <div v-if="loading" style="padding:40px;text-align:center;color:var(--text-muted)">加载中…</div>
      <div v-else-if="!creatives.length" class="empty-state">
        <div class="empty-icon">🎬</div>
        <div>暂无创意数据</div>
      </div>
      <template v-else>
        <table>
          <thead>
            <tr>
              <th style="min-width:200px">创意</th>
              <th>花费</th>
              <th>ROI</th>
              <th>GMV</th>
              <th>展示</th>
              <th>点击</th>
              <th>下单</th>
              <th>生命周期</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in pagedCreatives" :key="item.item_id||item.video_id">
              <!-- 创意缩略图+名称 -->
              <td>
                <div class="creative-cell" @click="openPreview(item)">
                  <div class="creative-thumb">
                    <img v-if="item.image_url||item.cover_url" :src="item.image_url||item.cover_url"
                         class="thumb-img" @error="$event.target.style.display='none'" />
                    <div v-else class="thumb-placeholder">🎬</div>
                    <div class="thumb-play-icon">▶</div>
                  </div>
                  <div style="min-width:0;flex:1">
                    <div class="creative-name" :title="creativeName(item)">{{ creativeName(item) }}</div>
                    <div style="font-family:monospace;font-size:10px;color:var(--text-muted)">ID: {{ item.item_id||item.video_id||'-' }}</div>
                  </div>
                </div>
              </td>
              <!-- 花费 -->
              <td style="font-weight:600">${{ fmt2(item.total_spend||item.spend||0) }}</td>
              <!-- ROI -->
              <td>
                <span :style="{color:roas(item)>=1?'var(--success)':'var(--danger)',fontWeight:600}">
                  {{ roas(item) > 0 ? fmt2(roas(item)) + 'x' : '-' }}
                </span>
              </td>
              <!-- GMV -->
              <td style="color:var(--success);font-weight:600">${{ fmt2(item.total_revenue||0) }}</td>
              <!-- 展示：数量 | CPM | 点击率 -->
              <td>
                <div>{{ fmtNum(item.total_impressions||0) }}</div>
                <div style="font-size:11px;color:var(--text-muted)">CPM ${{ cpm(item) }} · 点击率 {{ ctr(item) }}</div>
              </td>
              <!-- 点击：数量 | 转化率 -->
              <td>
                <div>{{ fmtNum(item.total_clicks||0) }}</div>
                <div style="font-size:11px;color:var(--text-muted)">转化率 {{ cvr(item) }}</div>
              </td>
              <!-- 下单 -->
              <td style="font-weight:600">{{ item.total_orders||0 }}</td>
              <!-- 生命周期 -->
              <td>
                <span :class="['badge', stageClassMap[item.stage]||'badge-info']"
                      :title="stageTooltip(item)"
                      style="cursor:help">
                  {{ stageLabelMap[item.stage]||item.stage||'—' }}
                </span>
                <div style="font-size:11px;color:var(--text-muted);margin-top:2px">{{ item.active_days||0 }}天</div>
              </td>
              <!-- 操作 -->
              <td>
                <div style="display:flex;gap:4px">
                  <button class="btn btn-ghost action-btn" title="预览" @click.stop="openPreview(item)">👁️</button>
                  <button class="btn btn-ghost action-btn" title="排除创意" style="color:var(--danger)"
                    :disabled="rowLoading[rowKey(item)] || item.is_auto_selected" @click="pauseItem(item)">
                    {{ rowLoading[rowKey(item)] === 'pause' ? '…' : '🚫' }}
                  </button>
                  <button class="btn btn-ghost action-btn" title="加热" style="color:var(--warning)"
                    :disabled="rowLoading[rowKey(item)]" @click="openHeatup(item)">📈</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="creatives.length > pageSize" class="pager">
          <button class="btn btn-ghost" style="padding:3px 10px" :disabled="creativePage<=1" @click="creativePage--">上一页</button>
          <span style="color:var(--text-muted)">{{ creativePage }} / {{ totalPages }} (共{{ creatives.length }}条)</span>
          <button class="btn btn-ghost" style="padding:3px 10px" :disabled="creativePage>=totalPages" @click="creativePage++">下一页</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { api } from '../api'
import { useGlobalFilterStore } from '../stores/globalFilter'

const globalFilterStore = useGlobalFilterStore()

const selectedShopId = ref('')
const sortBy = ref('total_spend')
const dateRange = ref({ start: '', end: '' })
const creatives = ref([])
const loading = ref(false)
const creativePage = ref(1)
const pageSize = 20

const rowLoading = ref({})
const heatupModal = ref({ show: false, campaignId: '', itemId: '', name: '', budget: 50, days: 1, loading: false, item: null })
const previewModal = ref({ show: false, name: '', imageUrl: '', videoUrl: '', id: '', item: null })
const toast = ref({ show: false, msg: '', type: 'success' })

const totalPages = computed(() => Math.ceil(creatives.value.length / pageSize))
const pagedCreatives = computed(() => {
  const start = (creativePage.value - 1) * pageSize
  return creatives.value.slice(start, start + pageSize)
})

const stageClassMap = { WARM_UP:'badge-info', GROWTH:'badge-success', PEAK:'badge-success', DECAY:'badge-warning', FATIGUE:'badge-danger', DEAD:'badge-danger', AUTO:'badge-info', UNKNOWN:'badge-info' }
const stageLabelMap = { WARM_UP:'🌱 学习', GROWTH:'📈 上升', PEAK:'⭐ 峰值', DECAY:'📉 衰退', FATIGUE:'💀 疲劳', DEAD:'☠️ 停投', AUTO:'🤖 自动', UNKNOWN:'❓ 未知' }

function fmt2(v) { return Number(v||0).toFixed(2) }

function stageTooltip(item) {
  const parts = []
  if (item.reason) parts.push(item.reason)
  if (item.trend) parts.push(`趋势: ${item.trend === 'up' ? '↑上升' : item.trend === 'down' ? '↓下降' : '→稳定'}`)
  if (item.daily_avg_spend) parts.push(`日均花费: $${Number(item.daily_avg_spend).toFixed(2)}`)
  if (item.active_days) parts.push(`活跃天数: ${item.active_days}`)
  if (item.recommendation) {
    const recMap = { boost: '建议加投', observe: '继续观察', reduce: '建议减投', drop: '建议暂停' }
    parts.push(`建议: ${recMap[item.recommendation] || item.recommendation}`)
  }
  return parts.join('\n') || '暂无判定信息'
}
function fmtNum(v) { return Number(v||0).toLocaleString() }

function cpm(item) {
  const spend = item.total_spend||item.spend||0
  const imp = item.total_impressions||item.impressions||0
  return imp > 0 ? ((spend/imp)*1000).toFixed(2) : '—'
}

function ctr(item) {
  const imp = item.total_impressions||item.impressions||0
  const clk = item.total_clicks||item.clicks||0
  return imp > 0 ? ((clk/imp)*100).toFixed(2)+'%' : '—'
}

function cvr(item) {
  const clk = item.total_clicks||item.clicks||0
  const ord = item.total_orders||item.conversions||0
  return clk > 0 ? ((ord/clk)*100).toFixed(2)+'%' : '—'
}

function roas(item) {
  const spend = item.total_spend||item.spend||0
  const rev = item.total_revenue||item.revenue||0
  return spend > 0 ? rev/spend : 0
}

function creativeName(item) {
  return item.product_name || item.creative_name || item.label || ('创意 #' + (item.item_id || item.video_id || '').slice(-6))
}

function openPreview(item) {
  previewModal.value = {
    show: true,
    name: creativeName(item),
    imageUrl: item.image_url || item.cover_url || '',
    videoUrl: '',
    tiktokUrl: item.tiktok_url || '',
    id: item.item_id || item.video_id || '',
    item: item,
  }
}

function rowKey(item) { return item.adgroup_id || item.video_id || item.item_id || '' }

async function onShopChange() {
  creativePage.value = 1
  await loadCreatives()
}

async function loadCreatives() {
  loading.value = true
  try {
    const params = { sort_by: sortBy.value, sort_order: 'desc' }
    if (dateRange.value.start) params.start_date = dateRange.value.start
    if (dateRange.value.end) params.end_date = dateRange.value.end
    const res = await api.get('/creatives/gmvmax-creatives', { params })
    creatives.value = Array.isArray(res.items) ? res.items : []
    creativePage.value = 1
  } catch (e) { console.error('Load creatives failed', e); creatives.value = [] }
  finally { loading.value = false }
}

async function pauseItem(item) {
  const key = rowKey(item)
  const itemId = item.item_id
  const campaignId = item.campaign_id
  const advertiserId = item.advertiser_id
  if (!itemId || !advertiserId) { showToast('缺少创意或账户信息', 'error'); return }
  if (!confirm(`确认排除创意「${creativeName(item)}」？\n排除后该创意将不再投放。`)) return
  rowLoading.value[key] = 'pause'
  try {
    await api.post('/gmvmax/creative/exclude', {
      advertiser_id: advertiserId,
      campaign_id: campaignId || '',
      item_id: itemId,
    })
    showToast('创意已排除')
    // 从列表中移除
    creatives.value = creatives.value.filter(c => c.item_id !== itemId)
  } catch (e) {
    showToast('排除失败: ' + (e.response?.data?.detail || e.message || ''), 'error')
  }
  finally { delete rowLoading.value[key] }
}

function openHeatup(item) {
  if (!item.campaign_id) { showToast('暂无 Campaign ID', 'error'); return }
  heatupModal.value = {
    show: true,
    campaignId: item.campaign_id,
    itemId: item.item_id || '',
    name: creativeName(item),
    budget: 50,
    days: 1,
    loading: false,
    item,
  }
}

async function confirmHeatup() {
  const { campaignId, itemId, budget, days, item } = heatupModal.value
  if (!budget || budget < 50) { showToast('最低预算 $50', 'error'); return }
  heatupModal.value.loading = true
  try {
    await api.post('/gmvmax/creative-boost/create', {
      advertiser_id: item?.advertiser_id,
      campaign_id: campaignId,
      item_id: itemId,
      video_id: item?.video_id || '',
      budget,
      duration_days: days,
    })
    showToast(`加热成功！预算 $${budget}，持续 ${days} 天`)
    heatupModal.value.show = false
  } catch (e) { showToast('加热失败: ' + (e.response?.data?.detail || e.message), 'error') }
  finally { heatupModal.value.loading = false }
}

let toastTimer = null
function showToast(msg, type = 'success') {
  toast.value = { show: true, msg, type }
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value.show = false }, 3000)
}

onMounted(loadCreatives)
</script>

<style scoped>
.page-header { display:flex; justify-content:space-between; align-items:flex-start; }

.action-btn { padding:3px 8px; font-size:14px; min-width:32px; }
.pager { display:flex;justify-content:center;align-items:center;gap:8px;margin-top:12px;font-size:13px; }
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; z-index:999; }
.modal { max-width:90vw; }

.toast {
  position:fixed; bottom:24px; right:24px;
  padding:10px 18px; border-radius:8px; font-size:13px; font-weight:600;
  z-index:9999; animation:slideIn 0.2s ease;
}
.toast.success { background:var(--success); color:#fff; }
.toast.error   { background:var(--danger);  color:#fff; }
@keyframes slideIn { from { transform:translateY(20px); opacity:0 } to { transform:translateY(0); opacity:1 } }

/* 缩略图 */
.creative-cell { display:flex; align-items:center; gap:10px; cursor:pointer; border-radius:6px; padding:2px; transition:background 0.15s; }
.creative-cell:hover { background:var(--bg-hover); }
.creative-thumb { position:relative; width:48px; height:64px; flex-shrink:0; border-radius:6px; overflow:hidden; background:var(--bg-hover); border:1px solid var(--border); }
.thumb-img { width:100%; height:100%; object-fit:cover; display:block; }
.thumb-placeholder { width:100%; height:100%; display:flex; align-items:center; justify-content:center; font-size:20px; opacity:0.4; }
.thumb-play-icon { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:14px; color:#fff; opacity:0; background:rgba(0,0,0,0.35); transition:opacity 0.15s; }
.creative-cell:hover .thumb-play-icon { opacity:1; }
.creative-name { font-size:13px; font-weight:500; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:160px; line-height:1.4; }

/* 预览弹窗 */
.preview-modal { width:480px; max-width:90vw; }
.preview-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.preview-title { font-size:15px; font-weight:700; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.preview-body { display:flex; justify-content:center; align-items:center; min-height:200px; }
.preview-image-wrap, .preview-video-wrap { display:flex; justify-content:center; }
.preview-placeholder { display:flex; flex-direction:column; align-items:center; justify-content:center; padding:40px; }
.preview-info { margin-top:12px; padding-top:10px; border-top:1px solid var(--border); }
.preview-info-row { display:flex; gap:16px; flex-wrap:wrap; }
.info-item { display:flex; flex-direction:column; gap:2px; }
.info-label { font-size:10px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; }
.info-value { font-size:14px; font-weight:600; }
</style>
