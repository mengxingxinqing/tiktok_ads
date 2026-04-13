<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">📋 广告看板</div>
        <div class="page-subtitle">所有推广计划一览，花费/GMV/ROI 实时数据</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <select v-model="filter.advertiser_id" @change="load" style="width:180px">
          <option value="">全部广告户</option>
          <option v-for="a in advertisers" :key="a.advertiser_id" :value="a.advertiser_id">
            {{ a.name || a.advertiser_id }}
          </option>
        </select>
        <select v-model="filter.days" @change="load" style="width:100px">
          <option value="7">近 7 天</option>
          <option value="14">近 14 天</option>
          <option value="30">近 30 天</option>
        </select>
        <select v-model="filter.sort" @change="sortCampaigns" style="width:110px">
          <option value="spend">按花费</option>
          <option value="revenue">按 GMV</option>
          <option value="roi">按 ROI</option>
          <option value="orders">按订单</option>
        </select>
        <button class="btn btn-ghost" @click="load">🔄 刷新</button>
      </div>
    </div>

    <!-- 汇总指标 -->
    <div class="summary-bar" v-if="campaigns.length">
      <div class="summary-item">
        <span class="summary-label">推广计划</span>
        <span class="summary-value">{{ campaigns.length }} 个</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">总花费</span>
        <span class="summary-value">${{ fmtNum(totalSpend) }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">总 GMV</span>
        <span class="summary-value" style="color:var(--success)">${{ fmtNum(totalRevenue) }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">总订单</span>
        <span class="summary-value">{{ totalOrders }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">整体 ROI</span>
        <span class="summary-value" :style="{color: overallRoi >= 1 ? 'var(--success)' : 'var(--danger)'}">
          {{ overallRoi.toFixed(2) }}x
        </span>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" style="padding:60px;text-align:center;color:var(--text-muted)">加载中...</div>

    <!-- 空状态 -->
    <div v-else-if="!campaigns.length" class="card">
      <div class="empty-state">
        <div class="empty-icon">📋</div>
        <div>暂无推广计划数据</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:8px">请先完成数据同步</div>
      </div>
    </div>

    <!-- Campaign 卡片列表 -->
    <div v-else class="campaign-list">
      <div v-for="c in campaigns" :key="c.campaign_id" class="campaign-card"
           :class="{'campaign-loss': c.avg_roi < 1 && c.total_spend > 5}"
           @click="toggleExpand(c)">
        <!-- 头部：名称 + 标签 -->
        <div class="campaign-header">
          <div style="min-width:0;flex:1">
            <div class="campaign-name" :title="c.campaign_name || c.campaign_id">
              {{ c.campaign_name || c.campaign_id }}
            </div>
            <div style="font-family:monospace;font-size:10px;color:var(--text-muted);margin-top:2px">
              {{ c.campaign_id }}
            </div>
          </div>
          <div style="display:flex;gap:6px;align-items:center">
            <span :class="['badge', c.campaign_type === 'GMVMAX' ? 'badge-info' : 'badge-success']" style="font-size:10px">
              {{ c.campaign_type === 'GMVMAX' ? '🚀 GMVMax' : '📢 竞价' }}
            </span>
            <span :class="['roi-pill', roiClass(c.avg_roi)]">
              ROI {{ c.avg_roi ? c.avg_roi.toFixed(2) + 'x' : '-' }}
            </span>
          </div>
        </div>

        <!-- 核心指标 -->
        <div class="campaign-metrics">
          <div class="cm-item">
            <div class="cm-label">💰 花费</div>
            <div class="cm-value">${{ fmtNum(c.total_spend) }}</div>
          </div>
          <div class="cm-item">
            <div class="cm-label">📈 GMV</div>
            <div class="cm-value" style="color:var(--success)">${{ fmtNum(c.total_revenue) }}</div>
          </div>
          <div class="cm-item">
            <div class="cm-label">🛒 订单</div>
            <div class="cm-value">{{ c.total_conversion || 0 }}</div>
          </div>
          <div class="cm-item">
            <div class="cm-label">🎯 客单价</div>
            <div class="cm-value">{{ c.total_conversion > 0 ? '$' + (c.total_revenue / c.total_conversion).toFixed(2) : '-' }}</div>
          </div>
          <div class="cm-item">
            <div class="cm-label">💸 单笔成本</div>
            <div class="cm-value">{{ c.total_conversion > 0 ? '$' + (c.total_spend / c.total_conversion).toFixed(2) : '-' }}</div>
          </div>
        </div>

        <!-- 花费 vs GMV 进度条 -->
        <div class="spend-gmv-bar">
          <div class="sgb-fill spend-fill" :style="{width: spendBarWidth(c) + '%'}"></div>
          <div class="sgb-fill gmv-fill" :style="{width: gmvBarWidth(c) + '%'}"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:10px;color:var(--text-muted);margin-top:2px">
          <span>■ 花费 ${{ fmtNum(c.total_spend) }}</span>
          <span style="color:var(--success)">■ GMV ${{ fmtNum(c.total_revenue) }}</span>
        </div>

        <!-- 操作按钮 -->
        <div style="display:flex;gap:8px;margin-top:8px" @click.stop>
          <button class="btn btn-ghost" style="padding:3px 10px;font-size:12px" @click="openUpload(c)">📤 上传视频</button>
        </div>

        <!-- 展开详情（每日趋势） -->
        <div v-if="expandedId === c.campaign_id" class="campaign-detail" @click.stop>
          <div style="font-size:12px;font-weight:600;margin-bottom:8px;color:var(--text-muted)">📊 每日趋势</div>
          <div v-if="loadingTrend" style="padding:16px;text-align:center;color:var(--text-muted);font-size:12px">加载中...</div>
          <table v-else-if="trendData.length" style="font-size:12px">
            <thead>
              <tr>
                <th>日期</th>
                <th>花费</th>
                <th>GMV</th>
                <th>订单</th>
                <th>ROI</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in trendData" :key="row.date"
                  :class="{'row-loss': row.roi < 1 && row.spend > 0}">
                <td>{{ row.date.slice(5) }}</td>
                <td>${{ Number(row.spend||0).toFixed(2) }}</td>
                <td style="color:var(--success)">${{ Number(row.gmv||0).toFixed(2) }}</td>
                <td>{{ row.orders || 0 }}</td>
                <td :class="roiClass(row.roi)">{{ row.roi ? row.roi.toFixed(2) + 'x' : '-' }}</td>
              </tr>
            </tbody>
          </table>
          <div v-else style="padding:12px;text-align:center;color:var(--text-muted);font-size:12px">无趋势数据</div>
        </div>
      </div>
    </div>

    <!-- 上传视频弹窗 -->
    <div v-if="uploadModal.show" class="modal-overlay" @click.self="uploadModal.show=false">
      <div class="modal card" style="width:440px">
        <div style="font-size:15px;font-weight:700;margin-bottom:12px">📤 上传视频到 Campaign</div>
        <div style="font-size:13px;color:var(--text-muted);margin-bottom:12px">
          {{ uploadModal.campaignName }} <span style="font-family:monospace;font-size:11px">({{ uploadModal.campaignId }})</span>
        </div>
        <div style="margin-bottom:12px">
          <label style="font-size:12px;color:var(--text-muted)">选择视频文件</label>
          <input type="file" accept="video/*" @change="onFileSelect" style="width:100%;margin-top:4px" />
        </div>
        <div v-if="uploadModal.file" style="font-size:12px;color:var(--text-muted);margin-bottom:12px">
          {{ uploadModal.file.name }} ({{ (uploadModal.file.size / 1024 / 1024).toFixed(1) }} MB)
        </div>
        <div v-if="uploadModal.progress > 0 && uploadModal.progress < 100" style="margin-bottom:12px">
          <div style="background:var(--bg);border-radius:4px;height:6px;overflow:hidden">
            <div :style="{width: uploadModal.progress + '%', height:'100%', background:'var(--primary)', transition:'width 0.3s'}"></div>
          </div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:4px;text-align:center">{{ uploadModal.progress }}%</div>
        </div>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button class="btn btn-ghost" style="padding:4px 14px" @click="uploadModal.show=false" :disabled="uploadModal.uploading">取消</button>
          <button class="btn btn-primary" style="padding:4px 14px" :disabled="!uploadModal.file || uploadModal.uploading" @click="doUpload">
            {{ uploadModal.uploading ? '上传中...' : '上传' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { api, advertiserApi } from '../api'
import { useGlobalFilterStore } from '../stores/globalFilter'

const globalFilterStore = useGlobalFilterStore()
const advertisers = ref([])
const campaigns = ref([])
const loading = ref(false)
const filter = ref({ advertiser_id: '', days: '30', sort: 'spend' })

// 监听全局店铺筛选器变化
watch(() => globalFilterStore.shopId, () => load())

// 展开趋势
const expandedId = ref(null)
const trendData = ref([])
const loadingTrend = ref(false)

// 汇总
const totalSpend = computed(() => campaigns.value.reduce((s, c) => s + (c.total_spend || 0), 0))
const totalRevenue = computed(() => campaigns.value.reduce((s, c) => s + (c.total_revenue || 0), 0))
const totalOrders = computed(() => campaigns.value.reduce((s, c) => s + (c.total_conversion || 0), 0))
const overallRoi = computed(() => totalSpend.value > 0 ? totalRevenue.value / totalSpend.value : 0)

// 格式化
const fmtNum = v => Number(v || 0).toFixed(2)
const roiClass = roi => {
  if (!roi || roi === 0) return ''
  if (roi >= 3) return 'roi-good'
  if (roi >= 1) return 'roi-ok'
  return 'roi-bad'
}

// 进度条
const spendBarWidth = c => {
  const max = Math.max(c.total_spend || 0, c.total_revenue || 0, 1)
  return ((c.total_spend || 0) / max * 100).toFixed(1)
}
const gmvBarWidth = c => {
  const max = Math.max(c.total_spend || 0, c.total_revenue || 0, 1)
  return ((c.total_revenue || 0) / max * 100).toFixed(1)
}

function sortCampaigns() {
  const key = filter.value.sort
  const map = { spend: 'total_spend', revenue: 'total_revenue', roi: 'avg_roi', orders: 'total_conversion' }
  const field = map[key] || 'total_spend'
  campaigns.value.sort((a, b) => (b[field] || 0) - (a[field] || 0))
}

async function load() {
  loading.value = true
  try {
    const params = { days: filter.value.days, page_size: 100 }
    if (filter.value.advertiser_id) params.advertiser_id = filter.value.advertiser_id
    if (globalFilterStore.shopId) params.store_id = globalFilterStore.shopId
    const data = await api.get('/campaigns', { params })
    campaigns.value = data.items || data.data?.items || []
    sortCampaigns()
  } catch (e) {
    console.error('Load campaigns failed', e)
    campaigns.value = []
  } finally {
    loading.value = false
  }
}

async function toggleExpand(c) {
  if (expandedId.value === c.campaign_id) {
    expandedId.value = null
    return
  }
  expandedId.value = c.campaign_id
  loadingTrend.value = true
  trendData.value = []
  try {
    const data = await api.get(`/campaigns/${c.campaign_id}/trend`, { params: { days: filter.value.days } })
    trendData.value = (data.trend || []).map(r => ({
      date: r.date,
      spend: r.spend || 0,
      gmv: r.gmv || 0,
      orders: r.orders || 0,
      roi: r.roi || 0,
    }))
  } catch (e) {
    console.error('Load trend failed', e)
    trendData.value = []
  } finally {
    loadingTrend.value = false
  }
}

// 上传视频
const uploadModal = ref({
  show: false, campaignId: '', campaignName: '', advertiserId: '',
  file: null, uploading: false, progress: 0,
})

function openUpload(c) {
  uploadModal.value = {
    show: true,
    campaignId: c.campaign_id,
    campaignName: c.campaign_name || c.campaign_id,
    advertiserId: c.advertiser_id,
    file: null,
    uploading: false,
    progress: 0,
  }
}

function onFileSelect(e) {
  uploadModal.value.file = e.target.files[0] || null
}

async function doUpload() {
  const { file, campaignId, advertiserId } = uploadModal.value
  if (!file) return
  uploadModal.value.uploading = true
  uploadModal.value.progress = 0
  try {
    // 1. 上传视频文件到 TikTok
    const formData = new FormData()
    formData.append('advertiser_id', advertiserId)
    formData.append('file', file)
    formData.append('video_name', file.name.replace(/\.[^.]+$/, ''))
    const uploadRes = await api.post('/ads/video/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: e => {
        if (e.total) uploadModal.value.progress = Math.round(e.loaded / e.total * 80)
      },
    })
    const videoId = uploadRes.video_id || uploadRes.data?.video_id
    if (!videoId) throw new Error('上传成功但未返回 video_id')
    uploadModal.value.progress = 90

    // 2. 将视频添加到 Campaign（GMVMax 创意）
    // 注：GMVMax 系统会自动将上传到素材库的视频纳入投放
    uploadModal.value.progress = 100
    alert(`上传成功！\nvideo_id: ${videoId}\n视频已添加到素材库，GMVMax 将自动纳入投放。`)
    uploadModal.value.show = false
  } catch (e) {
    const detail = e.response?.data?.detail
    const msg = Array.isArray(detail)
      ? detail.map(d => d.msg || JSON.stringify(d)).join('; ')
      : (detail || e.message)
    alert('上传失败: ' + msg)
  } finally {
    uploadModal.value.uploading = false
  }
}

async function loadAdvertisers() {
  try {
    const data = await advertiserApi.list()
    advertisers.value = data.advertisers || []
  } catch { advertisers.value = [] }
}

onMounted(async () => {
  await loadAdvertisers()
  await load()
})
</script>

<style scoped>
.summary-bar {
  display: flex; gap: 24px; padding: 14px 20px; margin-bottom: 16px;
  background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
}
.summary-item { display: flex; flex-direction: column; gap: 2px; }
.summary-label { font-size: 11px; color: var(--text-muted); }
.summary-value { font-size: 16px; font-weight: 700; }

.campaign-list { display: flex; flex-direction: column; gap: 12px; }

.campaign-card {
  background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px; cursor: pointer; transition: all 0.15s;
}
.campaign-card:hover { border-color: var(--primary); box-shadow: 0 2px 8px rgba(99,102,241,0.1); }
.campaign-loss { border-left: 3px solid var(--danger); }

.campaign-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.campaign-name { font-size: 14px; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 400px; }

.roi-pill {
  font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 99px;
}
.roi-good { background: rgba(16,185,129,0.15); color: #10b981; }
.roi-ok { background: rgba(245,158,11,0.15); color: #f59e0b; }
.roi-bad { background: rgba(239,68,68,0.15); color: #ef4444; }

.campaign-metrics {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 12px;
}
@media (max-width: 900px) { .campaign-metrics { grid-template-columns: repeat(3, 1fr); } }

.cm-item { display: flex; flex-direction: column; gap: 2px; }
.cm-label { font-size: 11px; color: var(--text-muted); }
.cm-value { font-size: 15px; font-weight: 600; }

.spend-gmv-bar {
  position: relative; height: 6px; border-radius: 3px;
  background: var(--border); overflow: hidden;
}
.sgb-fill { position: absolute; top: 0; left: 0; height: 100%; border-radius: 3px; }
.spend-fill { background: var(--primary); opacity: 0.6; z-index: 1; }
.gmv-fill { background: var(--success); opacity: 0.8; z-index: 2; }

.campaign-detail {
  margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border);
}
.campaign-detail table { width: 100%; border-collapse: collapse; }
.campaign-detail th, .campaign-detail td {
  padding: 6px 10px; text-align: left; border-bottom: 1px solid var(--border);
}
.campaign-detail th { color: var(--text-muted); font-size: 11px; font-weight: 600; }
.row-loss td { background: rgba(239,68,68,0.06); }
.modal-overlay { position:fixed; inset:0; background:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; z-index:999; }
.modal { max-width:90vw; }
</style>
