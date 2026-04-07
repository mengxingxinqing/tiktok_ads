<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">创建 GMVMax 广告</div>
        <div class="page-subtitle">选择店铺 → 选择商品 → 配置参数 → 创建投放</div>
      </div>
    </div>

    <!-- Step indicator -->
    <div class="step-indicator">
      <div v-for="(s, i) in steps" :key="i" class="step-item">
        <div class="step-dot" :class="{ done: step > i, active: step === i }">
          {{ step > i ? '\u2713' : i + 1 }}
        </div>
        <div class="step-name" :class="{ active: step === i, done: step > i }">{{ s }}</div>
        <div v-if="i < steps.length - 1" class="step-line"></div>
      </div>
    </div>

    <!-- Step 0: 选择店铺 -->
    <div v-if="step === 0" class="card">
      <h3 class="section-title">选择店铺</h3>

      <div v-if="shopsLoading" class="empty-state">加载店铺中...</div>
      <div v-else-if="shops.length === 0" class="empty-state">暂无可用店铺</div>

      <div v-else class="shop-grid">
        <div
          v-for="shop in shops" :key="shop.store_id"
          class="shop-card" :class="{ selected: form.store_id === shop.store_id }"
          @click="selectShop(shop)"
        >
          <div class="shop-name">{{ shop.store_name }}</div>
          <div class="shop-meta">
            <span class="badge-region">{{ shop.region || 'N/A' }}</span>
          </div>
          <div class="shop-stats">
            <div class="shop-stat">
              <span class="stat-label">商品数</span>
              <span class="stat-value">{{ shop.total_products ?? '-' }}</span>
            </div>
            <div class="shop-stat">
              <span class="stat-label">总收入</span>
              <span class="stat-value">${{ formatNum(shop.total_revenue) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="step-actions">
        <span></span>
        <button class="btn btn-primary" :disabled="!form.store_id" @click="goStep(1)">下一步 →</button>
      </div>
    </div>

    <!-- Step 1: 选择商品 -->
    <div v-else-if="step === 1" class="card">
      <h3 class="section-title">选择商品 <span class="optional-tag">可选</span></h3>
      <p class="section-desc">选择要投放的商品，或跳过以投放全部商品。</p>

      <div v-if="productsLoading" class="empty-state">加载商品中...</div>
      <div v-else-if="products.length === 0" class="empty-state">该店铺暂无商品数据</div>

      <div v-else>
        <div class="product-toolbar">
          <span class="selected-count">已选 {{ form.selected_products.length }} / {{ products.length }} 件商品</span>
          <button class="btn btn-ghost btn-sm" @click="form.selected_products = []">清除选择</button>
        </div>
        <div class="product-grid">
          <div
            v-for="p in products" :key="p.item_group_id"
            class="product-card" :class="{ selected: form.selected_products.includes(p.item_group_id) }"
            @click="toggleProduct(p.item_group_id)"
          >
            <div class="product-img-wrap">
              <img v-if="p.image_url" :src="p.image_url" class="product-img" />
              <div v-else class="product-img-placeholder">No img</div>
              <div v-if="form.selected_products.includes(p.item_group_id)" class="product-check">&check;</div>
            </div>
            <div class="product-info">
              <div class="product-name">{{ p.product_name || p.item_group_id }}</div>
              <div class="product-detail">
                <span v-if="p.price" class="product-price">${{ p.price }}</span>
                <span v-if="p.category" class="product-cat">{{ p.category }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="step-actions">
        <button class="btn btn-ghost" @click="goStep(0)">← 上一步</button>
        <button class="btn btn-primary" @click="goStep(2)">
          {{ form.selected_products.length > 0 ? '下一步 →' : '跳过，全部商品投放 →' }}
        </button>
      </div>
    </div>

    <!-- Step 2: 广告配置（预算 + ROI目标 + 名称） -->
    <div v-else-if="step === 2" class="card">
      <h3 class="section-title">广告配置</h3>

      <div class="form-group">
        <label>每日预算 (USD)</label>
        <div class="budget-row">
          <span class="budget-sign">$</span>
          <input v-model.number="form.daily_budget" type="number" min="1" max="99999" placeholder="100" />
        </div>
        <div class="form-hint">建议 $50 - $500 / 天</div>
      </div>

      <div class="form-group">
        <label>ROI 目标</label>
        <div class="budget-row">
          <input v-model.number="form.roas_goal" type="number" min="0" step="0.1" placeholder="2.0" />
          <span class="budget-sign">x</span>
        </div>
        <div class="form-hint">目标投资回报率，如 2.0 表示每花 $1 期望产出 $2 GMV</div>
      </div>

      <div class="form-group">
        <label>广告计划名称</label>
        <input v-model="form.campaign_name" type="text" placeholder="输入计划名称" />
        <div class="form-hint">建议格式：店铺名_GMVMax_日期</div>
      </div>

      <div class="step-actions">
        <button class="btn btn-ghost" @click="goStep(1)">← 上一步</button>
        <button
          class="btn btn-success"
          :disabled="creating || !form.campaign_name || !form.daily_budget"
          @click="createAds"
        >
          {{ creating ? '创建中...' : '创建广告' }}
        </button>
      </div>
    </div>

    <!-- Step 3: 创建结果 -->
    <div v-else-if="step === 3" class="card">
      <h3 class="section-title">创建结果</h3>

      <div class="results-summary">
        <div class="result-stat" :class="result.status === 'success' ? 'success' : 'error'">
          <span class="result-stat-icon">{{ result.status === 'success' ? '✅' : '❌' }}</span>
          <span>{{ result.status === 'success' ? '创建成功' : '创建失败' }}</span>
        </div>
      </div>

      <div v-if="result.status === 'success'" class="result-detail-card">
        <div class="result-row">
          <span class="result-label">计划名称</span>
          <span>{{ form.campaign_name }}</span>
        </div>
        <div class="result-row" v-if="result.campaign_id">
          <span class="result-label">Campaign ID</span>
          <span class="mono">{{ result.campaign_id }}</span>
        </div>
        <div class="result-row">
          <span class="result-label">每日预算</span>
          <span>${{ form.daily_budget }}</span>
        </div>
        <div class="result-row">
          <span class="result-label">ROI 目标</span>
          <span>{{ form.roas_goal }}x</span>
        </div>
        <div class="result-row">
          <span class="result-label">店铺</span>
          <span>{{ form.store_name }}</span>
        </div>
        <div class="result-row" v-if="form.selected_products.length">
          <span class="result-label">商品数</span>
          <span>{{ form.selected_products.length }} 件</span>
        </div>
        <div class="result-row" v-else>
          <span class="result-label">商品</span>
          <span>全部商品</span>
        </div>
      </div>

      <div v-else class="result-error-msg">
        {{ result.error }}
      </div>

      <div class="step-actions">
        <router-link to="/dashboard" class="btn btn-ghost">返回首页</router-link>
        <button class="btn btn-primary" @click="resetForm">创建新广告</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../api/index'

const steps = ['选择店铺', '选择商品', '广告配置', '创建结果']
const step = ref(0)

const shops = ref([])
const shopsLoading = ref(false)
const products = ref([])
const productsLoading = ref(false)
const creating = ref(false)
const result = ref({})

const form = ref({
  store_id: '',
  store_name: '',
  advertiser_id: '',
  bc_id: '',
  selected_products: [],
  campaign_name: '',
  daily_budget: 100,
  roas_goal: 2.0,
})

function formatNum(n) {
  if (n == null) return '-'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return String(n)
}

function todayStr() {
  const d = new Date()
  return d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0')
}

function goStep(s) { step.value = s }

// --- Step 0: 加载店铺 ---
async function loadShops() {
  shopsLoading.value = true
  try {
    const res = await api.get('/shops/list', { params: { days: 30 } })
    shops.value = res.list || res.shops || res || []
  } catch (e) {
    console.error('Failed to load shops:', e)
    shops.value = []
  } finally {
    shopsLoading.value = false
  }
}

function selectShop(shop) {
  form.value.store_id = shop.store_id
  form.value.store_name = shop.store_name || shop.name || ''
  form.value.advertiser_id = shop.advertiser_id || ''
  form.value.bc_id = shop.bc_id || ''
  form.value.campaign_name = (form.value.store_name || 'Shop') + '_GMVMax_' + todayStr()
  form.value.selected_products = []
  loadProducts()
}

// --- Step 1: 加载商品 ---
async function loadProducts() {
  productsLoading.value = true
  try {
    const res = await api.get(`/shops/${form.value.store_id}/detail`, { params: { days: 30 } })
    products.value = res.products || res.items || res.list || []
  } catch (e) {
    console.error('Failed to load products:', e)
    products.value = []
  } finally {
    productsLoading.value = false
  }
}

function toggleProduct(itemGroupId) {
  const idx = form.value.selected_products.indexOf(itemGroupId)
  if (idx > -1) form.value.selected_products.splice(idx, 1)
  else form.value.selected_products.push(itemGroupId)
}

// --- Step 2: 创建广告 ---
async function createAds() {
  creating.value = true
  result.value = {}

  try {
    const res = await api.post('/ads/gmvmax/campaign/create-full', {
      advertiser_id: form.value.advertiser_id,
      campaign_name: form.value.campaign_name,
      daily_budget: form.value.daily_budget,
      roas_goal: form.value.roas_goal,
      shop_id: form.value.store_id,
      item_group_ids: form.value.selected_products.length > 0 ? form.value.selected_products : undefined,
    })
    result.value = {
      status: 'success',
      campaign_id: res.data?.campaign_id || res.campaign_id,
    }
  } catch (e) {
    result.value = {
      status: 'error',
      error: e.response?.data?.detail || e.message,
    }
  }

  step.value = 3
  creating.value = false
}

function resetForm() {
  step.value = 0
  form.value = {
    store_id: '',
    store_name: '',
    advertiser_id: '',
    bc_id: '',
    selected_products: [],
    campaign_name: '',
    daily_budget: 100,
    roas_goal: 2.0,
  }
  result.value = {}
}

onMounted(loadShops)
</script>

<style scoped>
.page { padding: 24px; max-width: 960px; margin: 0 auto; }
.page-header { margin-bottom: 24px; }
.page-title { font-size: 20px; font-weight: 700; }
.page-subtitle { font-size: 13px; color: var(--text-muted); margin-top: 4px; }

/* Step indicator */
.step-indicator { display: flex; gap: 0; margin-bottom: 24px; }
.step-item { display: flex; align-items: center; flex: 1; }
.step-dot { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; background: var(--border); color: var(--text-muted); flex-shrink: 0; transition: all 0.2s; }
.step-dot.active { background: var(--primary); color: #fff; }
.step-dot.done { background: var(--success); color: #fff; }
.step-name { margin-left: 8px; font-size: 13px; font-weight: 500; color: var(--text-muted); white-space: nowrap; transition: color 0.2s; }
.step-name.active { color: var(--primary); }
.step-name.done { color: var(--success); }
.step-line { flex: 1; height: 1px; background: var(--border); margin: 0 12px; }

/* Card */
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; }
.section-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: var(--text); }
.section-desc { font-size: 13px; color: var(--text-muted); margin: -8px 0 16px; }
.optional-tag { font-size: 11px; font-weight: 400; color: var(--text-muted); background: var(--bg-hover); padding: 1px 6px; border-radius: 3px; margin-left: 4px; }
.empty-state { text-align: center; padding: 40px; color: var(--text-muted); }

/* Shop grid */
.shop-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; margin-bottom: 16px; }
.shop-card { padding: 16px; border: 1px solid var(--border); border-radius: 8px; cursor: pointer; transition: all 0.15s; }
.shop-card:hover { border-color: var(--primary); background: var(--bg-hover); }
.shop-card.selected { border-color: var(--primary); background: rgba(99,102,241,0.1); box-shadow: 0 0 0 1px var(--primary); }
.shop-name { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
.shop-meta { margin-bottom: 10px; }
.badge-region { display: inline-block; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 99px; background: rgba(59,130,246,0.15); color: #60a5fa; }
.shop-stats { display: flex; gap: 16px; }
.shop-stat { display: flex; flex-direction: column; gap: 2px; }
.stat-label { font-size: 11px; color: var(--text-muted); }
.stat-value { font-size: 13px; font-weight: 600; }

/* Product grid */
.product-toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.selected-count { font-size: 13px; color: var(--text-muted); }
.btn-sm { padding: 4px 10px; font-size: 12px; }
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-bottom: 16px; }
.product-card { border: 1px solid var(--border); border-radius: 8px; overflow: hidden; cursor: pointer; transition: all 0.15s; }
.product-card:hover { border-color: var(--primary); }
.product-card.selected { border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary); }
.product-img-wrap { position: relative; width: 100%; aspect-ratio: 1; background: var(--bg); overflow: hidden; }
.product-img { width: 100%; height: 100%; object-fit: cover; }
.product-img-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 12px; }
.product-check { position: absolute; top: 6px; right: 6px; width: 22px; height: 22px; border-radius: 50%; background: var(--primary); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; }
.product-info { padding: 8px 10px; }
.product-name { font-size: 12px; font-weight: 500; line-height: 1.3; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.product-detail { display: flex; gap: 8px; margin-top: 4px; font-size: 11px; }
.product-price { color: var(--success); font-weight: 600; }
.product-cat { color: var(--text-muted); }

/* Form */
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: var(--text); }
input, textarea { width: 100%; background: var(--bg); border: 1px solid var(--border); color: var(--text); border-radius: 6px; padding: 8px 10px; font-size: 13px; font-family: inherit; }
input:focus, textarea:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.budget-row { display: flex; align-items: center; gap: 8px; }
.budget-sign { color: var(--text-muted); font-weight: 600; }
.budget-row input { flex: 1; }
.form-hint { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

/* Results */
.results-summary { display: flex; justify-content: center; margin-bottom: 20px; }
.result-stat { display: flex; flex-direction: column; align-items: center; padding: 24px 40px; border-radius: 8px; font-size: 15px; font-weight: 600; }
.result-stat.success { background: rgba(16,185,129,0.1); color: var(--success); }
.result-stat.error { background: rgba(239,68,68,0.1); color: var(--danger); }
.result-stat-icon { font-size: 36px; margin-bottom: 8px; }
.result-detail-card { border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-bottom: 16px; }
.result-row { display: flex; justify-content: space-between; padding: 10px 16px; border-bottom: 1px solid var(--border); font-size: 13px; }
.result-row:last-child { border-bottom: none; }
.result-label { color: var(--text-muted); }
.mono { font-family: monospace; font-size: 12px; }
.result-error-msg { padding: 16px; background: rgba(239,68,68,0.08); border-radius: 8px; color: var(--danger); font-size: 13px; margin-bottom: 16px; }

/* Step actions */
.step-actions { display: flex; justify-content: space-between; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border); }

/* Buttons */
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 6px; border: none; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s; text-decoration: none; }
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover:not(:disabled) { background: var(--primary-hover); }
.btn-ghost { background: transparent; color: var(--text-muted); border: 1px solid var(--border); }
.btn-ghost:hover:not(:disabled) { background: var(--bg-hover); color: var(--text); }
.btn-success { background: var(--success); color: #fff; }
.btn-success:hover:not(:disabled) { background: #059669; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 768px) {
  .shop-grid { grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); }
  .product-grid { grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); }
  .step-name { display: none; }
  .step-line { margin: 0 6px; }
}
</style>
