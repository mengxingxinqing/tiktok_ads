<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">商品监控</div>
        <div class="page-subtitle">商品数据分析、成本配置、收益核算</div>
      </div>
    </div>

    <!-- Tab buttons -->
    <div style="display:flex;gap:4px;margin-bottom:16px">
      <button :class="['btn', tab==='data'?'btn-primary':'btn-ghost']" @click="tab='data'; loadItems()">🛍️ 商品数据</button>
      <button :class="['btn', tab==='profit'?'btn-primary':'btn-ghost']" @click="tab='profit'; loadProfit()">📊 收益核算</button>
    </div>

    <!-- ==================== Tab 1: 商品数据 ==================== -->
    <div v-if="tab==='data'" class="card">
      <div style="display:flex;gap:8px;align-items:center;margin-bottom:12px;flex-wrap:wrap">
        <input v-model="itemFilter.search" placeholder="搜索商品名称/ID" style="width:180px" @keyup.enter="itemPage=1; loadItems()" />
        <select v-model="itemFilter.sort_by" style="width:120px">
          <option value="total_spend">花费</option>
          <option value="total_orders">订单</option>
          <option value="total_revenue">收入</option>
          <option value="avg_roi">ROI</option>
          <option value="avg_cost_per_order">单笔成本</option>
        </select>
        <button class="btn btn-ghost" style="padding:4px 10px;font-size:14px"
          @click="itemFilter.sort_order = itemFilter.sort_order === 'desc' ? 'asc' : 'desc'">
          {{ itemFilter.sort_order === 'desc' ? '↓ 降序' : '↑ 升序' }}
        </button>
        <button class="btn btn-primary" style="padding:4px 12px" @click="itemPage=1; loadItems()">搜索</button>
        <button class="btn btn-ghost" style="padding:4px 12px" @click="itemFilter={search:'',sort_by:'total_spend',sort_order:'desc'}; itemPage=1; loadItems()">重置</button>
      </div>

      <div v-if="!itemsPaged.length" class="empty-state">
        <div class="empty-icon">🛍️</div>
        <div>暂无商品数据</div>
      </div>
      <table v-else>
        <thead>
          <tr>
            <th style="min-width:240px">商品</th>
            <th>总花费</th><th>总订单</th><th>总收入</th><th>ROI</th><th>单笔成本</th><th>活跃天数</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in itemsPaged" :key="item.item_group_id">
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <img v-if="item.image_url" :src="item.image_url" style="width:36px;height:36px;border-radius:4px;object-fit:cover;flex-shrink:0" />
                <div style="min-width:0">
                  <div style="font-size:13px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:200px" :title="item.product_name||item.item_group_id">
                    {{ item.product_name || item.item_group_id }}
                  </div>
                  <div v-if="item.category" style="font-size:11px;color:var(--text-muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:200px">
                    {{ item.category.split(' > ').pop() }}
                  </div>
                </div>
              </div>
            </td>
            <td style="font-weight:600">${{ Number(item.total_spend).toFixed(2) }}</td>
            <td style="text-align:center;font-weight:600">{{ item.total_orders }}</td>
            <td style="font-weight:600;color:var(--success)">${{ Number(item.total_revenue).toFixed(2) }}</td>
            <td><span :style="{color:item.avg_roi>=1?'var(--success)':'var(--danger)',fontWeight:600}">{{ item.avg_roi.toFixed(2) }}</span></td>
            <td>${{ Number(item.avg_cost_per_order).toFixed(2) }}</td>
            <td style="text-align:center">{{ item.active_days }}</td>
            <td>
              <button class="btn btn-ghost" style="padding:4px 10px;font-size:12px"
                @click="openCostModal(item)">
                {{ hasCostConfig(item) ? '✏️ 编辑成本' : '💰 配置成本' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- 分页 -->
      <div v-if="items.length > pageSize" style="display:flex;justify-content:center;align-items:center;gap:8px;margin-top:12px;font-size:13px">
        <button class="btn btn-ghost" style="padding:3px 10px" :disabled="itemPage<=1" @click="itemPage--">上一页</button>
        <span style="color:var(--text-muted)">{{ itemPage }} / {{ Math.ceil(items.length/pageSize) }} (共{{ items.length }}条)</span>
        <button class="btn btn-ghost" style="padding:3px 10px" :disabled="itemPage>=Math.ceil(items.length/pageSize)" @click="itemPage++">下一页</button>
      </div>
    </div>

    <!-- ==================== Tab 2: 收益核算 ==================== -->
    <div v-if="tab==='profit'" class="card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
        <span style="font-weight:600">📊 利润报表（近 {{ reportDays }} 天）</span>
        <div style="display:flex;gap:6px">
          <button v-for="d in [7,14,30]" :key="d"
            :class="['btn btn-ghost', reportDays===d ? 'btn-primary' : '']"
            style="padding:4px 10px;font-size:12px"
            @click="reportDays=d; loadProfit()">{{ d }}天</button>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>广告账户</th><th>日期</th><th>广告花费</th><th>估算 GMV</th>
            <th>真实利润</th><th>利润率</th><th>真实 ROAS</th><th>保本 ROAS</th><th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in report" :key="r.advertiser_id+r.stat_date">
            <td style="font-size:12px;color:var(--text-muted)" :title="r.advertiser_id">{{ truncateId(r.advertiser_id) }}</td>
            <td style="font-size:12px">{{ r.stat_date }}</td>
            <td>${{ fmt(r.ad_spend) }}</td>
            <td>{{ r.gmv_estimated ? '$'+fmt(r.gmv_estimated) : '-' }}</td>
            <td :class="r.real_profit > 0 ? 'stat-up' : 'stat-down'" style="font-weight:600">
              {{ r.real_profit != null ? '$'+fmt(r.real_profit) : '-' }}
            </td>
            <td>{{ r.real_margin != null ? r.real_margin+'%' : '-' }}</td>
            <td>{{ r.real_roas != null ? r.real_roas+'x' : '-' }}</td>
            <td>
              <span v-if="r.break_even_roas" style="font-size:12px;color:var(--warning)">
                {{ r.break_even_roas }}x
              </span>
              <span v-else style="color:var(--text-muted);font-size:12px">未配置</span>
            </td>
            <td>
              <span v-if="r.real_profit != null" :class="['badge', r.is_profitable ? 'badge-success' : 'badge-critical']">
                {{ r.is_profitable ? '盈利' : '亏损' }}
              </span>
              <span v-else class="badge badge-info">无成本配置</span>
            </td>
          </tr>
          <tr v-if="!report.length">
            <td colspan="9">
              <div class="empty-state"><div class="empty-icon">📊</div><div>暂无报表数据</div></div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ==================== 添加/编辑成本弹窗 ==================== -->
    <div v-if="modal.show" class="modal-overlay" @click.self="modal.show=false">
      <div class="modal card" style="width:580px">
        <div style="font-size:15px;font-weight:700;margin-bottom:20px">
          {{ modal.id ? '编辑' : '添加' }}商品成本配置
        </div>
        <div class="form-grid">
          <div class="form-row">
            <label>商品 ID *</label>
            <input v-model="modal.product_id" placeholder="TikTok Shop product_id" />
          </div>
          <div class="form-row">
            <label>SKU ID</label>
            <input v-model="modal.sku_id" placeholder="可选，精确到 SKU" />
          </div>
          <div class="form-row">
            <label>商品名称</label>
            <input v-model="modal.product_name" placeholder="备注用" />
          </div>
          <div class="form-row">
            <label>平均售价 ($)</label>
            <input v-model.number="modal.selling_price" type="number" min="0" step="0.01" />
          </div>
          <div class="form-row">
            <label>货品成本 ($/件)</label>
            <input v-model.number="modal.product_cost" type="number" min="0" step="0.01" />
          </div>
          <div class="form-row">
            <label>头程运费 ($/件)</label>
            <input v-model.number="modal.freight_inbound" type="number" min="0" step="0.01" />
          </div>
          <div class="form-row">
            <label>尾程运费 ($/件)</label>
            <input v-model.number="modal.freight_outbound" type="number" min="0" step="0.01" />
          </div>
          <div class="form-row">
            <label>达人佣金率 (%)</label>
            <input v-model.number="modal.affiliate_rate" type="number" min="0" max="100" step="0.1" />
          </div>
          <div class="form-row">
            <label>平台佣金率 (%)</label>
            <input v-model.number="modal.platform_fee_rate" type="number" min="0" max="50" step="0.1" />
          </div>
          <div class="form-row">
            <label>退货率 (%)</label>
            <input v-model.number="modal.return_rate" type="number" min="0" max="100" step="0.1" />
          </div>
          <div class="form-row">
            <label>货损率 (%)</label>
            <input v-model.number="modal.damage_rate" type="number" min="0" max="100" step="0.1" />
          </div>
          <div class="form-row">
            <label>投放返点率 (%)</label>
            <input v-model.number="modal.ad_rebate_rate" type="number" min="0" max="100" step="0.1" placeholder="平台激励，如 3%" />
          </div>
          <div class="form-row" style="grid-column:span 2">
            <label>备注</label>
            <input v-model="modal.notes" placeholder="如：2026-04升价后更新，返点3%" />
          </div>
        </div>

        <!-- 实时保本计算 -->
        <div v-if="modal.selling_price > 0 && modal.product_cost >= 0" class="preview-box">
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:8px">📐 实时保本计算</div>
          <div class="preview-grid">
            <span>每件固定成本</span>
            <span>${{ fixedCost.toFixed(2) }}</span>
            <span>每件可变成本率</span>
            <span>{{ variableRate.toFixed(1) }}%</span>
            <span style="font-weight:600;color:var(--warning)">保本 ROAS</span>
            <span style="font-weight:600;color:var(--warning)">{{ breakEvenRoas || '—' }}</span>
          </div>
        </div>

        <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:20px">
          <button class="btn btn-ghost" @click="modal.show=false">取消</button>
          <button class="btn btn-primary" @click="saveCost">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'

// ── shared state ──
const tab = ref('data')
const pageSize = 20

// ── Tab 1: 商品数据 ──
const items = ref([])
const itemPage = ref(1)
const itemFilter = ref({ search: '', sort_by: 'total_spend', sort_order: 'desc' })

const itemsPaged = computed(() => {
  const start = (itemPage.value - 1) * pageSize
  return items.value.slice(start, start + pageSize)
})

async function loadItems() {
  try {
    const params = { days: 30, enrich: false, sort_by: itemFilter.value.sort_by, sort_order: itemFilter.value.sort_order }
    if (itemFilter.value.search) params.item_group_id = itemFilter.value.search
    const res = await api.get('/creatives/gmvmax-items', { params })
    items.value = res.data?.items || res.items || []
    // 异步补充商品名称和图片，不阻塞列表展示
    enrichItems()
  } catch (e) { console.error('Load gmvmax items failed', e) }
}

async function enrichItems() {
  try {
    const params = { days: 30, enrich: true, sort_by: itemFilter.value.sort_by, sort_order: itemFilter.value.sort_order }
    if (itemFilter.value.search) params.item_group_id = itemFilter.value.search
    const res = await api.get('/creatives/gmvmax-items', { params, timeout: 30000 })
    const enriched = res.data?.items || res.items || []
    if (enriched.length) items.value = enriched
  } catch (e) { /* 补充信息失败不影响主列表 */ }
}

// ── 成本配置 (inline in 商品列表) ──
const costs = ref([])

const defaultModal = () => ({
  show: false, id: null,
  product_id: '', sku_id: '', product_name: '',
  selling_price: 0, product_cost: 0, freight_inbound: 0, freight_outbound: 0,
  affiliate_rate: 0, platform_fee_rate: 5, return_rate: 0, damage_rate: 0, ad_rebate_rate: 0, notes: '',
})
const modal = ref(defaultModal())

const fixedCost = computed(() =>
  (modal.value.product_cost || 0) + (modal.value.freight_inbound || 0) + (modal.value.freight_outbound || 0)
)
const variableRate = computed(() =>
  (modal.value.affiliate_rate || 0) + (modal.value.platform_fee_rate || 0)
)
const breakEvenRoas = computed(() => {
  const price = modal.value.selling_price || 0
  if (!price) return null
  const netPrice = price * (1 - (modal.value.return_rate || 0) / 100 - (modal.value.damage_rate || 0) / 100)
  const margin = netPrice * (1 - variableRate.value / 100) - fixedCost.value
  if (margin <= 0) return '∞（无法保本）'
  return (netPrice / margin).toFixed(2) + 'x'
})

async function loadCosts() {
  try {
    const res = await api.get('/products/costs')
    costs.value = res.items || []
  } catch (e) { console.error('Load costs failed', e) }
}


function openModal(item = null) {
  if (item) {
    modal.value = { show: true, id: item.id, ...item }
  } else {
    modal.value = { ...defaultModal(), show: true }
  }
}

function quickConfig(product) {
  modal.value = {
    ...defaultModal(),
    show: true,
    product_id: product.item_group_id || product.product_id,
    product_name: product.product_name || '',
    selling_price: product.selling_price || 0,
  }
}

function hasCostConfig(item) {
  return costs.value.some(c => c.product_id === item.item_group_id)
}

function openCostModal(item) {
  const existing = costs.value.find(c => c.product_id === item.item_group_id)
  if (existing) {
    openModal(existing)
  } else {
    modal.value = {
      ...defaultModal(),
      show: true,
      product_id: item.item_group_id,
      product_name: item.product_name || '',
      selling_price: item.price ? parseFloat(item.price) : 0,
    }
  }
}

async function saveCost() {
  try {
    const { show, id, advertiser_id, ...body } = modal.value
    await api.post('/products/costs', body)
    modal.value.show = false
    await Promise.all([loadCosts(), loadItems()])
  } catch (e) {
    alert('保存失败: ' + (e.response?.data?.detail || e.message))
  }
}

async function deleteCost(c) {
  if (!confirm(`确定删除「${c.product_name || c.product_id}」的成本配置？`)) return
  try {
    await api.delete(`/products/costs/${c.id}`)
    await loadCosts()
  } catch (e) {
    alert('删除失败: ' + (e.response?.data?.detail || e.message))
  }
}

// ── Tab 3: 收益核算 ──
const report = ref([])
const reportDays = ref(7)

async function loadProfit() {
  try {
    const res = await api.get('/products/profit-report', { params: { days: reportDays.value } })
    report.value = res.data || []
  } catch (e) { console.error('Load profit report failed', e) }
}

// ── helpers ──
const fmt = v => Number(v || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const truncateId = (id) => {
  if (!id) return '-'
  const s = String(id)
  return s.length > 10 ? 'GMVMax...' + s.slice(-4) : s
}

// ── init ──
onMounted(async () => {
  await Promise.all([loadItems(), loadCosts()])
})
</script>

<style scoped>
.form-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.form-row { display:flex; flex-direction:column; gap:4px; }
.form-row label { font-size:12px; color:var(--text-muted); }
.form-row input { width:100%; }
.preview-box {
  background: var(--bg); border: 1px solid var(--border);
  border-radius:8px; padding:12px; margin-top:12px;
}
.preview-grid {
  display:grid; grid-template-columns:1fr auto; gap:6px 20px;
  font-size:13px;
}
.modal-overlay { position:fixed;inset:0;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;z-index:999; }
.modal { max-width:90vw; max-height:90vh; overflow-y:auto; }
</style>
