<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">店铺管理</div>
        <div class="page-subtitle">店铺信息、收益核算、转化指标</div>
      </div>
      <button class="btn btn-ghost" @click="load">刷新</button>
    </div>

    <div v-if="loading" style="padding:40px;text-align:center;color:var(--text-muted)">加载中...</div>

    <div v-else-if="!shops.length" class="card">
      <div class="empty-state">
        <div class="empty-icon">🏪</div>
        <div>暂无店铺数据</div>
      </div>
    </div>

    <!-- Shop cards -->
    <div v-for="shop in shops" :key="shop.store_id" class="card" style="margin-bottom:16px">
      <!-- Section 1: Basic info -->
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px">
        <div>
          <div style="font-size:18px;font-weight:700">{{ shop.store_name }}</div>
          <div style="font-size:12px;color:var(--text-muted);font-family:monospace;margin-top:2px">店铺 ID: {{ shop.store_id }}</div>
          <div v-if="shop.advertiser_id" style="font-size:12px;color:var(--text-muted);margin-top:4px">
            关联投放户: <span style="font-weight:600;color:var(--text)">{{ advName(shop.advertiser_id) }}</span>
            <span style="font-family:monospace;margin-left:4px">({{ shop.advertiser_id }})</span>
          </div>
        </div>
        <div style="display:flex;gap:6px">
          <span class="badge badge-info">{{ shop.region }}</span>
          <span class="badge badge-info">{{ shop.store_type }}</span>
        </div>
      </div>

      <!-- Section 2: Core metrics -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px">
        <div class="metric-mini"><div class="metric-mini-label">总花费</div><div class="metric-mini-value">${{ fmtNum(shop.total_spend) }}</div></div>
        <div class="metric-mini"><div class="metric-mini-label">总收入</div><div class="metric-mini-value" style="color:var(--success)">${{ fmtNum(shop.total_revenue) }}</div></div>
        <div class="metric-mini"><div class="metric-mini-label">总订单</div><div class="metric-mini-value">{{ shop.total_orders }}</div></div>
        <div class="metric-mini"><div class="metric-mini-label">ROI</div><div class="metric-mini-value" :style="{color:shop.overall_roi>=1?'var(--success)':'var(--danger)'}">{{ shop.overall_roi?.toFixed(2) || '-' }}</div></div>
      </div>

      <!-- Section 3: Funnel -->
      <div style="background:var(--bg);border-radius:8px;padding:12px;margin-bottom:16px">
        <div style="font-size:13px;font-weight:600;margin-bottom:8px">转化漏斗</div>
        <div style="display:flex;align-items:center;justify-content:center;gap:16px;font-size:14px">
          <div style="text-align:center">
            <div style="font-size:20px;font-weight:700">{{ fmtBig(shop.total_impressions) }}</div>
            <div style="font-size:11px;color:var(--text-muted)">展示</div>
          </div>
          <div style="text-align:center;color:var(--text-muted)">
            →<br><span style="font-size:11px;font-weight:600">{{ shop.click_rate || '-' }}%</span>
          </div>
          <div style="text-align:center">
            <div style="font-size:20px;font-weight:700;color:#f59e0b">{{ fmtBig(shop.total_clicks) }}</div>
            <div style="font-size:11px;color:var(--text-muted)">点击</div>
          </div>
          <div style="text-align:center;color:var(--text-muted)">
            →<br><span style="font-size:11px;font-weight:600">{{ shop.order_rate || '-' }}%</span>
          </div>
          <div style="text-align:center">
            <div style="font-size:20px;font-weight:700;color:var(--success)">{{ shop.total_orders }}</div>
            <div style="font-size:11px;color:var(--text-muted)">下单</div>
          </div>
        </div>
        <div style="text-align:center;margin-top:8px;font-size:12px;color:var(--text-muted)">
          展示→下单率: <span style="font-weight:600">{{ shop.impression_to_order_rate || '-' }}%</span>
        </div>
      </div>

      <!-- Section 4: Asset stats -->
      <div style="display:flex;gap:24px;font-size:13px">
        <div><span style="color:var(--text-muted)">商品数</span> <span style="font-weight:600;margin-left:4px">{{ shop.total_products }}</span></div>
        <div><span style="color:var(--text-muted)">创意数</span> <span style="font-weight:600;margin-left:4px">{{ shop.total_creatives }}</span></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api, advertiserApi } from '../api'

const shops = ref([])
const advertisers = ref([])
const loading = ref(false)

const fmtNum = v => Number(v || 0).toFixed(2)
const fmtBig = v => Number(v || 0).toLocaleString()

function advName(advId) {
  const a = advertisers.value.find(x => x.advertiser_id === advId)
  return a?.name || a?.advertiser_name || advId
}

async function load() {
  loading.value = true
  try {
    const [shopRes, advRes] = await Promise.all([
      api.get('/shops/list'),
      advertiserApi.list(),
    ])
    shops.value = shopRes.shops || []
    advertisers.value = advRes.advertisers || []
  } catch (e) {
    console.error('Load shops failed', e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.metric-mini {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 12px;
  text-align: center;
}
.metric-mini-label { font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
.metric-mini-value { font-size: 20px; font-weight: 700; }
</style>
