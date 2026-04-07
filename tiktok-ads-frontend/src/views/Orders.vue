<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">订单分析</div>
        <div class="page-subtitle">商品维度订单数据、转化追踪</div>
      </div>
    </div>

    <!-- Summary cards -->
    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-label">总订单数</div>
        <div class="metric-value">{{ summary.total_orders || 0 }}</div>
        <div class="metric-sub">{{ dateRange.start }} ~ {{ dateRange.end }}</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">总销售额</div>
        <div class="metric-value">${{ fmt(summary.total_revenue) }}</div>
        <div class="metric-sub">GMVMax 报表数据</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">总广告花费</div>
        <div class="metric-value">${{ fmt(summary.total_spend) }}</div>
        <div class="metric-sub">含所有 Campaign</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">平均客单价</div>
        <div class="metric-value">${{ fmt(summary.avg_order_value) }}</div>
        <div class="metric-sub">销售额 / 订单数</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">整体 ROI</div>
        <div class="metric-value" :class="(summary.overall_roi || 0) >= 1 ? 'success' : 'danger'">
          {{ (summary.overall_roi || 0).toFixed(2) }}x
        </div>
        <div class="metric-sub">收入 / 花费</div>
      </div>
    </div>

    <!-- Filter bar -->
    <div class="card filter-bar">
      <div class="filter-row">
        <label class="filter-label">日期范围</label>
        <input v-model="dateRange.start" type="date" class="filter-input" />
        <span class="filter-sep">-</span>
        <input v-model="dateRange.end" type="date" class="filter-input" />
        <button class="btn btn-primary" @click="search">查询</button>
        <button class="btn btn-ghost" @click="reset">重置</button>
      </div>
    </div>

    <!-- Main table -->
    <div class="card">
      <div class="card-header">
        <span class="card-title">商品订单明细</span>
        <span class="record-count">共 {{ orders.length }} 条记录</span>
      </div>

      <div v-if="loading" class="loading-state">加载中...</div>

      <div v-else-if="orders.length === 0" class="empty-state">
        <div class="empty-icon">📦</div>
        <div>暂无订单数据</div>
        <div class="empty-hint">检查日期范围或稍后再试</div>
      </div>

      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th style="text-align:left">日期</th>
              <th style="text-align:left">商品</th>
              <th style="text-align:right">订单数</th>
              <th style="text-align:right">销售额</th>
              <th style="text-align:right">广告花费</th>
              <th style="text-align:right">ROI</th>
              <th style="text-align:right">单笔成本</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in ordersPaged" :key="row.campaign_id + '-' + row.stat_date + '-' + idx">
              <td class="col-date">{{ row.stat_date }}</td>
              <td class="col-product">
                <div class="product-cell">
                  <img
                    v-if="products[row.campaign_id]?.image_url"
                    :src="products[row.campaign_id].image_url"
                    class="product-thumb"
                    alt=""
                  />
                  <div class="product-info">
                    <div class="product-name" :title="products[row.campaign_id]?.product_name || row.campaign_id">
                      {{ products[row.campaign_id]?.product_name || row.campaign_id }}
                    </div>
                    <span v-if="row.campaign_type === 'GMVMAX'" class="badge badge-info">GMVMax</span>
                  </div>
                </div>
              </td>
              <td style="text-align:right;font-weight:600">{{ row.orders || 0 }}</td>
              <td style="text-align:right">${{ fmt(row.revenue) }}</td>
              <td style="text-align:right">${{ fmt(row.spend) }}</td>
              <td style="text-align:right;font-weight:600" :class="roiClass(row.roi)">
                {{ row.roi ? row.roi.toFixed(2) + 'x' : '-' }}
              </td>
              <td style="text-align:right">${{ fmt(row.cost_per_order) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button class="btn btn-ghost btn-sm" :disabled="page <= 1" @click="page--">上一页</button>
        <span class="page-info">{{ page }} / {{ totalPages }}</span>
        <button class="btn btn-ghost btn-sm" :disabled="page >= totalPages" @click="page++">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'

const orders = ref([])
const products = ref({})
const summary = ref({})
const pageSize = 20
const page = ref(1)
const dateRange = ref({
  start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
  end: new Date().toISOString().split('T')[0],
})
const loading = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(orders.value.length / pageSize)))

const ordersPaged = computed(() => {
  const start = (page.value - 1) * pageSize
  return orders.value.slice(start, start + pageSize)
})

async function load() {
  loading.value = true
  try {
    const advertiserId = localStorage.getItem('current_advertiser_id') || '7615246831711862800'

    const [orderRes, itemRes] = await Promise.all([
      api.get(`/orders/report/${advertiserId}`, {
        params: { start_date: dateRange.value.start, end_date: dateRange.value.end }
      }),
      api.get('/creatives/gmvmax-items', { params: { days: 30, enrich: true } }),
    ])

    // Build product map for enrichment
    const itemList = orderRes.items || itemRes.items || []
    itemList.forEach(item => {
      products.value[item.item_group_id] = {
        product_name: item.product_name,
        image_url: item.image_url,
      }
    })

    summary.value = orderRes.summary || {}

    // Only show rows with orders > 0 or spend > 0
    const allOrders = orderRes.orders || []
    orders.value = allOrders.filter(o => o.orders > 0 || o.spend > 0)
    orders.value.sort((a, b) => (b.stat_date < a.stat_date ? -1 : 1))
    page.value = 1
  } catch (e) {
    console.error('Load orders failed', e)
  } finally {
    loading.value = false
  }
}

function search() {
  page.value = 1
  load()
}

function reset() {
  dateRange.value = {
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0],
  }
  page.value = 1
  load()
}

const fmt = v => Number(v || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

function roiClass(roi) {
  if (!roi) return ''
  return roi >= 1 ? 'stat-up' : 'stat-down'
}

onMounted(load)
</script>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

@media (max-width: 1200px) {
  .metrics-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
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

.metric-value.success {
  color: var(--success);
}

.metric-value.danger {
  color: var(--danger);
}

.metric-sub {
  font-size: 12px;
  color: var(--text-muted);
}

/* Filter bar */
.filter-bar {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-muted);
}

.filter-input {
  width: 140px;
  padding: 6px 10px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg);
  color: var(--text);
  font-size: 13px;
}

.filter-sep {
  color: var(--text-muted);
}

/* Card header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-title {
  font-weight: 600;
  font-size: 15px;
}

.record-count {
  font-size: 12px;
  color: var(--text-muted);
}

/* Table */
.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

thead th {
  padding: 10px 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}

tbody td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

tbody tr:hover {
  background: var(--hover-bg, rgba(0, 0, 0, 0.02));
}

.col-date {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
}

/* Product cell */
.col-product {
  max-width: 260px;
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.product-thumb {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid var(--border);
  flex-shrink: 0;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.product-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.page-info {
  font-size: 13px;
  color: var(--text-muted);
}

.btn-sm {
  padding: 4px 12px;
  font-size: 12px;
}

/* States */
.loading-state {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
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

.empty-hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 8px;
}

.stat-up {
  color: var(--success);
}

.stat-down {
  color: var(--danger);
}

.badge-info {
  display: inline-block;
  background: #d1ecf1;
  color: #0c5460;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 500;
}
</style>
