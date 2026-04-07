<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">🎬 创意监控（高级筛选）</div>
        <div class="page-subtitle">按状态、Ad ID、店铺、商品、创建日期等多维度管理创意</div>
      </div>
      <button class="btn btn-ghost" @click="load">🔄 刷新</button>
    </div>

    <!-- 筛选面板 -->
    <div class="card" style="margin-bottom:20px">
      <div style="font-weight:600;margin-bottom:12px">🔍 高级筛选</div>
      
      <div class="filter-grid">
        <!-- 1. 创意状态 -->
        <div class="filter-group">
          <label>1️⃣ 创意状态</label>
          <select v-model="filters.status" @change="load" style="width:100%">
            <option value="">全部状态</option>
            <option value="PENDING_REVIEW">⏳ 待审核</option>
            <option value="APPROVED">✅ 审核通过</option>
            <option value="REJECTED">❌ 审核不通过</option>
            <option value="UNDER_LEARNING">🧠 学习中</option>
            <option value="ACTIVE">🟢 投放中</option>
            <option value="PAUSED">⏸️ 手动暂停</option>
            <option value="FATIGUE">💀 疲劳</option>
            <option value="DISABLED">🚫 已禁用</option>
            <option value="ARCHIVED">📦 已归档</option>
          </select>
        </div>

        <!-- 2. 广告 ID -->
        <div class="filter-group">
          <label>2️⃣ 广告 ID</label>
          <input v-model="filters.ad_id" placeholder="输入 Ad ID 搜索" @change="load" />
        </div>

        <!-- 3. 店铺 -->
        <div class="filter-group">
          <label>3️⃣ 店铺</label>
          <select v-model="filters.shop_id" @change="load" style="width:100%">
            <option value="">全部店铺</option>
            <option v-for="shop in shopList" :key="shop.id" :value="shop.id">
              {{ shop.name }}
            </option>
          </select>
        </div>

        <!-- 4. 商品 -->
        <div class="filter-group">
          <label>4️⃣ 商品</label>
          <select v-model="filters.product_id" @change="load" style="width:100%">
            <option value="">全部商品</option>
            <option v-for="product in productList" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </div>

        <!-- 5. 创建日期 -->
        <div class="filter-group">
          <label>5️⃣ 创建日期</label>
          <div style="display:flex;gap:4px">
            <input v-model="filters.created_from" type="date" style="flex:1" @change="load" />
            <span style="align-self:center">~</span>
            <input v-model="filters.created_to" type="date" style="flex:1" @change="load" />
          </div>
        </div>

        <!-- 额外筛选 -->
        <div class="filter-group">
          <label>生命周期阶段</label>
          <select v-model="filters.lifecycle" @change="load" style="width:100%">
            <option value="">全部阶段</option>
            <option value="WARM_UP">🌱 冷启动</option>
            <option value="GROWTH">📈 上升期</option>
            <option value="PEAK">⭐ 峰值期</option>
            <option value="DECAY">📉 衰退期</option>
            <option value="FATIGUE">💀 疲劳</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Hook Rate</label>
          <div style="display:flex;gap:4px">
            <input v-model.number="filters.hook_rate_min" type="number" placeholder="最小 %" style="flex:1" @change="load" />
            <span style="align-self:center">~</span>
            <input v-model.number="filters.hook_rate_max" type="number" placeholder="最大 %" style="flex:1" @change="load" />
          </div>
        </div>
      </div>
    </div>

    <!-- 统计概览 -->
    <div class="metrics-grid" style="margin-bottom:20px">
      <div class="metric-card">
        <div class="metric-label">📊 筛选结果</div>
        <div class="metric-value">{{ creatives.length }}</div>
        <div class="metric-sub">共 {{ stats.total }} 个创意</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">⏳ 待审核</div>
        <div class="metric-value" style="color:var(--warning)">{{ stats.pending_review || 0 }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">✅ 已审核通过</div>
        <div class="metric-value" style="color:var(--success)">{{ stats.approved || 0 }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">❌ 审核不通过</div>
        <div class="metric-value" style="color:var(--danger)">{{ stats.rejected || 0 }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">🟢 投放中</div>
        <div class="metric-value" style="color:var(--success)">{{ stats.active || 0 }}</div>
      </div>

      <div class="metric-card">
        <div class="metric-label">💀 疲劳创意</div>
        <div class="metric-value" style="color:var(--danger)">{{ stats.fatigue || 0 }}</div>
      </div>
    </div>

    <!-- 创意列表 -->
    <div class="card">
      <div style="font-weight:600;margin-bottom:12px">创意详情表</div>

      <table v-if="creatives.length > 0">
        <thead>
          <tr>
            <th>创意 ID</th>
            <th>创意名</th>
            <th style="text-align:center">审核状态</th>
            <th style="text-align:center">投放状态</th>
            <th style="text-align:center">生命周期</th>
            <th>广告 ID</th>
            <th>店铺</th>
            <th>商品</th>
            <th style="text-align:right">Hook Rate</th>
            <th style="text-align:right">Hold Rate</th>
            <th style="text-align:right">ROAS</th>
            <th>创建日期</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="creative in creatives" :key="creative.id">
            <!-- 创意 ID -->
            <td style="font-family:monospace;font-size:12px">{{ creative.video_id }}</td>

            <!-- 创意名 -->
            <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis">
              {{ creative.creative_name || '-' }}
            </td>

            <!-- 审核状态 -->
            <td style="text-align:center">
              <span :class="['badge', statusBadgeClass(creative.status)]">
                {{ translateStatus(creative.status) }}
              </span>
            </td>

            <!-- 投放状态 -->
            <td style="text-align:center">
              <span v-if="creative.status === 'ACTIVE'" class="badge badge-success">🟢 投放中</span>
              <span v-else-if="creative.status === 'PAUSED'" class="badge badge-warning">⏸️ 暂停</span>
              <span v-else-if="creative.status === 'FATIGUE'" class="badge badge-danger">💀 疲劳</span>
              <span v-else class="badge badge-info">{{ translateStatus(creative.status) }}</span>
            </td>

            <!-- 生命周期 -->
            <td style="text-align:center">
              <span :class="['badge', lifecycleBadgeClass(creative.lifecycle_stage)]">
                {{ translateLifecycle(creative.lifecycle_stage) }}
              </span>
            </td>

            <!-- 广告 ID -->
            <td style="font-size:12px;color:var(--text-muted);font-family:monospace">
              {{ creative.ad_id || '-' }}
            </td>

            <!-- 店铺 -->
            <td style="font-size:13px">{{ creative.shop_name || '-' }}</td>

            <!-- 商品 -->
            <td style="font-size:13px">{{ creative.product_name || '-' }}</td>

            <!-- Hook Rate -->
            <td style="text-align:right;font-weight:600" :class="creative.latest_hook_rate > 60 ? 'stat-up' : 'stat-down'">
              {{ creative.latest_hook_rate ? creative.latest_hook_rate.toFixed(1) : '-' }}%
            </td>

            <!-- Hold Rate -->
            <td style="text-align:right">
              {{ creative.latest_hold_rate ? creative.latest_hold_rate.toFixed(1) : '-' }}%
            </td>

            <!-- ROAS -->
            <td style="text-align:right">
              {{ creative.latest_roas ? creative.latest_roas.toFixed(2) : '-' }}x
            </td>

            <!-- 创建日期 -->
            <td style="font-size:12px;color:var(--text-muted)">
              {{ formatDate(creative.created_at) }}
            </td>

            <!-- 操作 -->
            <td>
              <div style="display:flex;gap:4px">
                <button v-if="creative.status === 'ACTIVE'" class="btn btn-ghost" style="padding:4px 8px;font-size:11px"
                  @click="pauseCreative(creative)">暂停</button>
                <button v-if="creative.status === 'PAUSED'" class="btn btn-ghost" style="padding:4px 8px;font-size:11px"
                  @click="enableCreative(creative)">启用</button>
                <button v-if="creative.lifecycle_stage === 'GROWTH'" class="btn btn-primary" style="padding:4px 8px;font-size:11px"
                  @click="heatupCreative(creative)">🔥 加热</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-else class="empty-state">
        <div class="empty-icon">🎬</div>
        <div>没有符合条件的创意</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:8px">
          尝试调整筛选条件
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '../api'


const filters = ref({
  status: '',
  ad_id: '',
  shop_id: '',
  product_id: '',
  created_from: '',
  created_to: '',
  lifecycle: '',
  hook_rate_min: 0,
  hook_rate_max: 100,
})

const creatives = ref([])
const shopList = ref([])
const productList = ref([])
const stats = ref({})

const translateStatus = (status) => {
  const map = {
    PENDING_REVIEW: '⏳ 待审核',
    APPROVED: '✅ 审核通过',
    REJECTED: '❌ 审核不通过',
    UNDER_LEARNING: '🧠 学习中',
    ACTIVE: '🟢 投放中',
    PAUSED: '⏸️ 暂停',
    FATIGUE: '💀 疲劳',
    DISABLED: '🚫 禁用',
    ARCHIVED: '📦 归档',
  }
  return map[status] || status
}

const translateLifecycle = (stage) => {
  const map = {
    WARM_UP: '🌱 冷启动',
    GROWTH: '📈 上升',
    PEAK: '⭐ 峰值',
    DECAY: '📉 衰退',
    FATIGUE: '💀 疲劳',
    UNKNOWN: '❓ 未知',
  }
  return map[stage] || stage
}

const statusBadgeClass = (status) => {
  const map = {
    PENDING_REVIEW: 'badge-warning',
    APPROVED: 'badge-success',
    REJECTED: 'badge-danger',
    ACTIVE: 'badge-success',
    PAUSED: 'badge-warning',
    FATIGUE: 'badge-danger',
  }
  return map[status] || 'badge-info'
}

const lifecycleBadgeClass = (stage) => {
  const map = {
    WARM_UP: 'badge-info',
    GROWTH: 'badge-success',
    PEAK: 'badge-success',
    DECAY: 'badge-warning',
    FATIGUE: 'badge-danger',
  }
  return map[stage] || 'badge-info'
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

async function load() {
  try {
    const advertiserId = localStorage.getItem('current_advertiser_id') || 'test'

    const res = await api.get(`/creatives/list-advanced/${advertiserId}`, {
      params: {
        ...filters.value,
        status: filters.value.status || undefined,
        ad_id: filters.value.ad_id || undefined,
        shop_id: filters.value.shop_id || undefined,
        product_id: filters.value.product_id || undefined,
        lifecycle: filters.value.lifecycle || undefined,
      },
    })

    creatives.value = res.items || res.data?.items || []
    stats.value = res.stats || res.data?.stats || {}
  } catch (e) {
    console.error('Failed to load creatives:', e)
  }
}

async function pauseCreative(creative) {
  // TODO: 实现暂停创意操作
  alert(`暂停创意 ${creative.video_id}`)
}

async function enableCreative(creative) {
  // TODO: 实现启用创意操作
  alert(`启用创意 ${creative.video_id}`)
}

async function heatupCreative(creative) {
  // TODO: 跳转到加热页面或打开加热弹窗
  alert(`加热创意 ${creative.video_id}`)
}

onMounted(load)
</script>

<style scoped>
.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-group label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
}

.filter-group input,
.filter-group select {
  padding: 8px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 13px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.metric-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-label {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
}

.metric-sub {
  font-size: 11px;
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

.empty-state {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}
</style>
