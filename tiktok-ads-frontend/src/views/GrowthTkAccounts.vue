<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">🎯 TK 账号管理</div>
        <div class="page-subtitle">录入 TK 账号，设定涨粉目标</div>
      </div>
      <div style="display:flex;gap:8px">
        <button class="btn btn-ghost" @click="showAdd=false; showBatch=true">📋 批量导入</button>
        <button class="btn btn-primary" @click="showAdd=true; showBatch=false">+ 录入账号</button>
      </div>
    </div>

    <!-- 录入弹窗 -->
    <div v-if="showAdd" class="modal-overlay" @click.self="showAdd=false">
      <div class="modal card" style="width:440px">
        <div style="font-weight:700;margin-bottom:16px">录入 TK 账号</div>
        <div style="display:flex;flex-direction:column;gap:12px">
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">账号 ID *</div>
            <input v-model="form.account_id" placeholder="如 wsmnx（不带@）" style="width:100%" />
          </div>
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">账号名称</div>
            <input v-model="form.account_name" placeholder="可留空，自动用账号ID" style="width:100%" />
          </div>
          <div>
            <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">主页 URL</div>
            <input v-model="form.profile_url" placeholder="可留空，自动生成" style="width:100%" />
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div>
              <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">目标粉丝数</div>
              <input v-model.number="form.target_follower_count" type="number" placeholder="10000" style="width:100%" />
            </div>
            <div>
              <div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">目标万粉成本(USD)</div>
              <input v-model.number="form.target_cost_per_10k" type="number" placeholder="35" style="width:100%" />
            </div>
          </div>
          <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:8px">
            <button class="btn btn-ghost" @click="showAdd=false">取消</button>
            <button class="btn btn-primary" @click="submitAdd">确认录入</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 批量导入弹窗 -->
    <div v-if="showBatch" class="modal-overlay" @click.self="showBatch=false">
      <div class="modal card" style="width:560px">
        <div style="font-weight:700;margin-bottom:16px">批量导入 TK 账号</div>
        <div style="margin-bottom:12px">
          <div style="font-size:13px;color:var(--text-muted);margin-bottom:8px">格式说明：每行一个账号，格式如下（逗号分隔）</div>
          <div style="background:var(--bg);padding:8px;border-radius:6px;font-size:12px;color:var(--text-muted);font-family:monospace">
            wsmnx, 10000, 35<br/>
            hongdatex.2, 20000<br/>
            another_user
          </div>
        </div>
        <textarea v-model="batchText" placeholder="wsmnx, 10000, 35&#10;hongdatex.2, 20000, 30&#10;..." rows="8" style="width:100%;margin-bottom:12px;font-family:monospace;font-size:13px"></textarea>
        <div style="display:flex;justify-content:flex-end;gap:8px">
          <button class="btn btn-ghost" @click="showBatch=false">取消</button>
          <button class="btn btn-primary" @click="submitBatch">确认导入</button>
        </div>
      </div>
    </div>

    <!-- 账号列表 -->
    <div class="card" style="margin-top:16px">
      <div style="margin-bottom:12px;display:flex;gap:8px;align-items:center">
        <select v-model="filter.status" @change="load" style="width:120px">
          <option value="">全部状态</option>
          <option value="IDLE">🟡 IDLE</option>
          <option value="RUNNING">🔵 运行中</option>
          <option value="COMPLETED">🟢 已完成</option>
          <option value="PAUSED">⚠️ 已暂停</option>
        </select>
        <button class="btn btn-ghost" @click="load">🔄 刷新</button>
      </div>

      <div v-if="loading" style="text-align:center;padding:40px;color:var(--text-muted)">加载中…</div>
      <div v-else-if="!accounts.length" class="empty-state">
        <div class="empty-icon">🎯</div>
        <div>暂无 TK 账号</div>
        <button class="btn btn-primary" style="margin-top:12px" @click="showAdd=true">录入第一个账号</button>
      </div>
      <template v-else>
        <table>
          <thead>
            <tr>
              <th>账号</th>
              <th>主页</th>
              <th>当前粉丝</th>
              <th>目标粉丝</th>
              <th>目标成本</th>
              <th>状态</th>
              <th>绑定账户</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in accounts" :key="a.id">
              <td>
                <b>@{{ a.account_id }}</b>
                <div style="font-size:11px;color:var(--text-muted)">{{ a.account_name }}</div>
              </td>
              <td>
                <a :href="a.profile_url" target="_blank" style="font-size:12px;color:var(--primary)">
                  {{ a.profile_url ? '查看主页 ↗' : '—' }}
                </a>
              </td>
              <td>
                <b>{{ a.follower_count ? a.follower_count.toLocaleString() : '—' }}</b>
                <div style="font-size:11px;color:var(--text-muted)">{{ a.follower_updated_at ? '刷新: '+fmtTime(a.follower_updated_at) : '' }}</div>
              </td>
              <td>{{ a.target_follower_count.toLocaleString() }}</td>
              <td>${{ a.target_cost_per_10k }}</td>
              <td>
                <span :class="['badge', statusClass(a.status)]">{{ a.status }}</span>
              </td>
              <td style="font-size:12px;color:var(--text-muted)">{{ a.bound_ad_account_id || '—' }}</td>
              <td>
                <div style="display:flex;gap:4px">
                  <button class="btn btn-ghost" style="padding:4px 8px;font-size:12px" @click="refreshFollowers(a)" title="刷新粉丝数">🔄</button>
                  <button class="btn btn-ghost" style="padding:4px 8px;font-size:12px" @click="editAccount(a)">✏️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { growthApi } from '../api'

const loading = ref(false)
const accounts = ref([])
const showAdd = ref(false)
const showBatch = ref(false)
const batchText = ref('')
const filter = ref({ status: '' })

const form = ref({
  account_id: '',
  account_name: '',
  profile_url: '',
  target_follower_count: 10000,
  target_cost_per_10k: 35,
})

async function load() {
  loading.value = true
  try {
    const params = {}
    if (filter.value.status) params.status = filter.value.status
    const res = await growthApi.listTkAccounts(params)
    accounts.value = res.accounts || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitAdd() {
  if (!form.value.account_id) return alert('请输入账号 ID')
  try {
    await growthApi.createTkAccount({
      account_id: form.value.account_id,
      account_name: form.value.account_name,
      profile_url: form.value.profile_url,
      target_follower_count: form.value.target_follower_count,
      target_cost_per_10k: form.value.target_cost_per_10k,
    })
    showAdd.value = false
    form.value = { account_id: '', account_name: '', profile_url: '', target_follower_count: 10000, target_cost_per_10k: 35 }
    await load()
  } catch (e) {
    alert('录入失败: ' + (e.message || e))
  }
}

async function submitBatch() {
  const lines = batchText.value.trim().split('\n').filter(l => l.trim())
  const results = []
  for (const line of lines) {
    const parts = line.split(',').map(p => p.trim())
    const account_id = parts[0]
    const target_follower_count = parseInt(parts[1]) || 10000
    const target_cost_per_10k = parseFloat(parts[2]) || 35
    if (!account_id) continue
    try {
      await growthApi.createTkAccount({ account_id, target_follower_count, target_cost_per_10k })
      results.push({ account_id, ok: true })
    } catch (e) {
      results.push({ account_id, ok: false, msg: e.message })
    }
  }
  alert(`导入完成：${results.filter(r=>r.ok).length}/${results.length} 成功`)
  showBatch.value = false
  await load()
}

async function refreshFollowers(a) {
  try {
    const res = await growthApi.refreshFollowers(a.account_id)
    if (res.follower_count !== null) {
      a.follower_count = res.follower_count
    } else {
      alert('刷新失败，账号可能不支持抓取')
    }
  } catch (e) {
    alert('刷新失败: ' + (e.message || e))
  }
}

function editAccount(a) {
  const target_follower_count = prompt('新目标粉丝数:', a.target_follower_count)
  if (target_follower_count === null) return
  growthApi.updateTkAccount(a.account_id, { target_follower_count: parseInt(target_follower_count) })
    .then(() => load())
    .catch(e => alert('更新失败: ' + (e.message || e)))
}

function statusClass(s) {
  return { IDLE: '', RUNNING: 'badge-info', COMPLETED: 'badge-success', PAUSED: 'badge-warning', FAILED: 'badge-danger' }[s] || ''
}

function fmtTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleString('zh-CN', { hour12: false }).slice(0, 16)
}

onMounted(load)
</script>
