<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">广告账户</div>
        <div class="page-subtitle">管理已授权的 TikTok 广告账户</div>
      </div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-ghost" @click="refreshBalance" :disabled="balanceLoading" style="font-size:12px">
          {{ balanceLoading ? '刷新中...' : '🔄 刷新余额' }}
        </button>
        <button class="btn btn-primary" @click="showAuthModal = true">+ 授权新账户</button>
      </div>
    </div>

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>账户</th><th>余额</th>
            <th>Token 状态</th><th>Token 到期</th><th>最后同步</th><th>状态</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="a in advertisers" :key="a.advertiser_id">
            <td>
              <div style="font-weight:500">{{ a.name || a.advertiser_name || '-' }}</div>
              <div style="font-size:11px;color:var(--text-muted);font-family:monospace">{{ a.advertiser_id }}</div>
            </td>
            <td>
              <div v-if="a.balance != null" style="font-weight:600">
                {{ a.currency || '$' }}{{ Number(a.balance).toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2}) }}
              </div>
              <div v-if="a.cash != null || a.grant != null" style="font-size:11px;color:var(--text-muted)">
                <span v-if="a.cash != null">现金 {{ Number(a.cash).toFixed(2) }}</span>
                <span v-if="a.grant != null"> / 赠款 {{ Number(a.grant).toFixed(2) }}</span>
              </div>
              <div v-if="a.balance == null" style="color:var(--text-muted);font-size:12px">-</div>
            </td>
            <td>
              <span :class="['badge', a.is_token_valid ? 'badge-success' : 'badge-critical']">
                {{ a.is_token_valid ? '✅ 有效' : '⚠️ 已过期' }}
              </span>
            </td>
            <td style="font-size:12px;color:var(--text-muted)">{{ fmtTime(a.access_token_expire_at) }}</td>
            <td style="font-size:12px;color:var(--text-muted)">{{ fmtTime(a.last_sync_at) || '未同步' }}</td>
            <td>
              <span :class="['badge', a.is_active ? 'badge-success' : 'badge-info']">
                {{ a.is_active ? '运行中' : '已停用' }}
              </span>
            </td>
            <td>
              <button class="btn btn-danger-text" @click="confirmDelete(a)">删除</button>
            </td>
          </tr>
          <tr v-if="!advertisers.length">
            <td colspan="7">
              <div class="empty-state">
                <div class="empty-icon">🏢</div>
                <div>暂无授权账户</div>
                <div style="margin-top:12px">
                  <button class="btn btn-primary" @click="showAuthModal = true">立即授权第一个账户</button>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 删除确认弹窗 -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal card">
        <div style="font-size:16px;font-weight:700;margin-bottom:16px;color:var(--danger, #ef4444)">确认删除广告账户</div>
        <div style="color:var(--text-muted);font-size:13px;margin-bottom:16px;line-height:1.8">
          即将删除账户 <strong>{{ deleteTarget.name || deleteTarget.advertiser_name || deleteTarget.advertiser_id }}</strong>
          <span style="font-family:monospace;font-size:12px">({{ deleteTarget.advertiser_id }})</span>，
          此操作将<strong style="color:var(--danger, #ef4444)">永久清除</strong>该账户下的所有数据，包括：
          <ul style="margin:8px 0 0 16px;padding:0">
            <li>投放指标快照</li>
            <li>创意数据及创意分组</li>
            <li>决策记录及效果追踪</li>
            <li>告警记录、日报、商品成本等</li>
          </ul>
        </div>
        <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:20px">
          <button class="btn btn-ghost" @click="deleteTarget = null" :disabled="deleting">取消</button>
          <button class="btn btn-danger" @click="doDelete" :disabled="deleting">
            {{ deleting ? '删除中...' : '确认删除' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 授权弹窗 -->
    <div v-if="showAuthModal" class="modal-overlay" @click.self="showAuthModal = false">
      <div class="modal card">
        <div style="font-size:16px;font-weight:700;margin-bottom:16px">授权新广告账户</div>
        <div style="color:var(--text-muted);font-size:13px;margin-bottom:16px;line-height:1.6">
          点击下方按钮生成授权链接，将链接发给广告账户管理员，他们完成授权后账户会自动出现在列表中。
        </div>
        <div style="display:flex;gap:8px;margin-bottom:12px">
          <input v-model="authRemark" placeholder="备注（可选，如账户名称）" style="flex:1" />
          <button class="btn btn-primary" @click="genAuthUrl">生成授权链接</button>
        </div>
        <div v-if="authUrl" style="margin-top:12px">
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:6px">授权链接：</div>
          <div style="background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:10px;font-size:12px;word-break:break-all">
            {{ authUrl }}
          </div>
          <button class="btn btn-ghost" style="margin-top:8px" @click="copyUrl">📋 复制链接</button>
        </div>
        <div style="display:flex;justify-content:flex-end;margin-top:20px">
          <button class="btn btn-ghost" @click="showAuthModal = false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { advertiserApi } from '../api'

const advertisers = ref([])
const showAuthModal = ref(false)
const authRemark = ref('')
const authUrl = ref('')
const deleteTarget = ref(null)
const deleting = ref(false)
const balanceLoading = ref(false)

const fmtTime = t => t ? new Date(t).toLocaleString('zh-CN') : null

async function load() {
  const data = await advertiserApi.list()
  advertisers.value = data.advertisers || []
}

async function refreshBalance() {
  balanceLoading.value = true
  try {
    const res = await advertiserApi.refreshBalance()
    // 刷新列表拿最新缓存余额
    await load()
  } catch (e) {
    console.error('Refresh balance failed', e)
  } finally {
    balanceLoading.value = false
  }
}

async function genAuthUrl() {
  const data = await advertiserApi.getAuthUrl(authRemark.value)
  authUrl.value = data.auth_url
}

function copyUrl() {
  navigator.clipboard.writeText(authUrl.value)
  alert('已复制到剪贴板')
}

function confirmDelete(advertiser) {
  deleteTarget.value = advertiser
}

async function doDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await advertiserApi.delete(deleteTarget.value.advertiser_id)
    deleteTarget.value = null
    await load()
  } catch (e) {
    alert('删除失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  await load()
  // 后台刷新余额，不阻塞页面
  refreshBalance()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center; z-index: 999;
}
.modal { width: 520px; max-width: 90vw; }
.btn-danger-text {
  background: none; border: none; color: var(--danger, #ef4444);
  cursor: pointer; font-size: 12px; padding: 4px 8px; border-radius: 4px;
}
.btn-danger-text:hover { background: rgba(239,68,68,0.1); }
.btn-danger {
  background: var(--danger, #ef4444); color: #fff; border: none;
  padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px;
}
.btn-danger:hover { background: #dc2626; }
.btn-danger:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
