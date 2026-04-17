<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">🎬 素材库</div>
        <div class="page-subtitle">按万粉成本排序，优先使用低价高效素材</div>
      </div>
      <button class="btn btn-primary" @click="openBind">🔗 授权绑定 (Spark Ads)</button>
    </div>

    <!-- Spark Ads 授权绑定弹窗 -->
    <div v-if="showBind" class="modal-overlay" @click.self="showBind=false">
      <div class="modal card" style="width:500px">
        <div style="font-weight:700;margin-bottom:8px">🔗 绑定 Spark Ads 授权</div>
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:16px">
          在 TikTok App 中：视频 → 分享 → 授权广告 → 复制授权码（TAP Code）粘到下面
        </div>
        <div style="display:flex;flex-direction:column;gap:12px">
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">目标广告账户 *</div>
            <select v-model="bindForm.advertiser_id" style="width:100%">
              <option value="">请选择</option>
              <option v-for="a in adAccounts" :key="a.advertiser_id" :value="a.advertiser_id">
                {{ a.advertiser_name }} ({{ a.currency }} {{ a.balance }})
              </option>
            </select>
          </div>
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">授权码 (auth_code) *</div>
            <input v-model="bindForm.auth_code" placeholder="例如 TTXYZ..." style="width:100%;font-family:monospace" />
          </div>
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">关联 TK 账号（选填）</div>
            <input v-model="bindForm.tk_account_id" placeholder="如 wsmnx" style="width:100%" />
          </div>
          <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:8px">
            <button class="btn btn-ghost" @click="showBind=false">取消</button>
            <button class="btn btn-primary" @click="submitBind" :disabled="binding">
              {{ binding ? '绑定中…' : '提交' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 素材列表 -->
    <div class="card" style="margin-top:16px">
      <div style="margin-bottom:12px">
        <span style="color:var(--text-muted);font-size:13px">共 {{ total }} 个素材，按万粉成本升序排列</span>
      </div>

      <div v-if="loading" style="text-align:center;padding:40px;color:var(--text-muted)">加载中…</div>
      <div v-else-if="!materials.length" class="empty-state">
        <div class="empty-icon">🎬</div>
        <div>素材库为空</div>
        <div style="color:var(--text-muted);font-size:13px;margin-top:4px">添加第一个素材开始追踪万粉成本</div>
        <button class="btn btn-primary" style="margin-top:12px" @click="showAdd=true">添加素材</button>
      </div>
      <template v-else>
        <table>
          <thead>
            <tr>
              <th>素材</th>
              <th>广告户</th>
              <th>授权状态</th>
              <th>绑定 TK</th>
              <th>使用次数</th>
              <th>累计花费</th>
              <th>累计涨粉</th>
              <th>平均万粉成本</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in materials" :key="m.id || m.video_id">
              <td>
                <b style="font-size:12px">{{ (m.item_id || m.video_id || '').substring(0, 18) }}…</b>
                <div v-if="m.video_url" style="font-size:11px">
                  <a :href="m.video_url" target="_blank" style="color:var(--primary)">预览 ↗</a>
                </div>
              </td>
              <td style="font-size:12px;color:var(--text-muted)">{{ m.advertiser_id || '—' }}</td>
              <td>
                <span v-if="m.ad_auth_status === 'AUTHORIZED'" class="badge badge-success">已授权</span>
                <span v-else-if="m.ad_auth_status" class="badge badge-warning">{{ m.ad_auth_status }}</span>
                <span v-else class="badge">未绑定</span>
              </td>
              <td style="font-size:12px">{{ m.bound_tk_account_id ? '@'+m.bound_tk_account_id : '—' }}</td>
              <td><span class="badge">{{ m.sample_count || 0 }} 次</span></td>
              <td>${{ fmt(m.total_spend) }}</td>
              <td>{{ m.total_followers_gained ? '+'+m.total_followers_gained.toLocaleString() : '—' }}</td>
              <td>
                <b v-if="m.avg_cost_per_10k" :style="{color: costColor(m.avg_cost_per_10k)}">
                  ${{ m.avg_cost_per_10k.toFixed(2) }}
                </b>
                <span v-else style="color:var(--text-muted)">—</span>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分页 -->
        <div v-if="total > pageSize" style="margin-top:16px;display:flex;justify-content:center;gap:8px">
          <button class="btn btn-ghost" :disabled="page<=1" @click="page--; load()">上一页</button>
          <span style="color:var(--text-muted);font-size:13px;line-height:32px">{{ page }}/{{ Math.ceil(total/pageSize) }}</span>
          <button class="btn btn-ghost" :disabled="page>=Math.ceil(total/pageSize)" @click="page++; load()">下一页</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { growthApi } from '../api'

const loading = ref(false)
const materials = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const showBind = ref(false)
const binding = ref(false)
const adAccounts = ref([])

const bindForm = ref({
  advertiser_id: '',
  auth_code: '',
  tk_account_id: '',
})

async function load() {
  loading.value = true
  try {
    const res = await growthApi.listCreatives({ page: page.value, page_size: pageSize })
    materials.value = res.materials || []
    total.value = res.total || 0
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function loadAdAccounts() {
  try {
    const res = await growthApi.listAdAccounts()
    adAccounts.value = res.accounts || []
  } catch (e) { console.error(e) }
}

function openBind() {
  bindForm.value = { advertiser_id: '', auth_code: '', tk_account_id: '' }
  showBind.value = true
}

async function submitBind() {
  if (!bindForm.value.advertiser_id) return alert('请选择广告账户')
  if (!bindForm.value.auth_code) return alert('请填写 auth_code')
  binding.value = true
  try {
    await growthApi.bindAuthCode({
      advertiser_id: bindForm.value.advertiser_id,
      auth_code: bindForm.value.auth_code.trim(),
      tk_account_id: bindForm.value.tk_account_id.trim() || undefined,
    })
    showBind.value = false
    await load()
  } catch (e) {
    alert('绑定失败: ' + (e.response?.data?.detail || e.message || e))
  } finally {
    binding.value = false
  }
}

function costColor(cost) {
  if (!cost) return ''
  if (cost <= 30) return 'var(--success)'
  if (cost <= 50) return 'var(--warning)'
  return 'var(--danger)'
}

function costBadgeClass(m) {
  if (!m.avg_cost_per_10k) return ''
  const c = m.avg_cost_per_10k
  if (c <= 30) return 'badge-success'
  if (c <= 50) return 'badge-warning'
  return 'badge-danger'
}

function costLabel(m) {
  if (!m.avg_cost_per_10k) return '新素材'
  const c = m.avg_cost_per_10k
  if (c <= 30) return '高效'
  if (c <= 50) return '正常'
  return '高成本'
}

function fmt(n) {
  if (!n) return '0.00'
  return Number(n).toLocaleString('en', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

onMounted(() => {
  load()
  loadAdAccounts()
})
</script>
