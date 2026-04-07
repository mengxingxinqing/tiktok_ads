<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">系统设置</div>
        <div class="page-subtitle">基本配置与告警规则管理</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >{{ tab.label }}</button>
    </div>

    <!-- Tab 1: 基本设置 -->
    <div v-if="activeTab === 'basic'">
      <!-- 飞书通知 -->
      <div class="card" style="margin-bottom:16px">
        <div style="font-size:15px;font-weight:600;margin-bottom:16px">🔔 飞书通知</div>
        <div style="display:flex;gap:8px;margin-bottom:12px">
          <input v-model="webhookUrl" placeholder="飞书群机器人 Webhook URL" style="flex:1" />
          <button class="btn btn-primary" @click="testFeishu" :disabled="testing">
            {{ testing ? '测试中…' : '测试连通性' }}
          </button>
        </div>
        <div v-if="testResult" :style="{ color: testResult.ok ? 'var(--success)' : 'var(--danger)', fontSize: '13px' }">
          {{ testResult.ok ? '✅ 飞书通知发送成功！' : '❌ 发送失败：' + testResult.msg }}
        </div>
        <div style="color:var(--text-muted);font-size:12px;margin-top:8px">
          在飞书群 → 设置 → 群机器人 → 添加机器人 → 自定义机器人，获取 Webhook URL
        </div>
      </div>

      <!-- 系统操作 -->
      <div class="card" style="margin-bottom:16px">
        <div style="font-size:15px;font-weight:600;margin-bottom:16px">⚙️ 系统操作</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
          <button class="btn btn-ghost" @click="triggerSync" :disabled="syncing">
            {{ syncing ? '同步中…' : '🔄 立即同步数据' }}
          </button>
          <button class="btn btn-ghost" @click="triggerReport">
            📊 立即发送日报
          </button>
        </div>
        <div v-if="actionMsg" style="color:var(--success);font-size:13px;margin-top:10px">{{ actionMsg }}</div>
      </div>

      <!-- 系统信息 -->
      <div class="card">
        <div style="font-size:15px;font-weight:600;margin-bottom:16px">ℹ️ 系统信息</div>
        <table style="width:auto">
          <tr><td style="color:var(--text-muted);padding-right:40px">API 地址</td><td>{{ apiBase }}</td></tr>
          <tr><td style="color:var(--text-muted)">TikTok App ID</td><td>7591801546375954449</td></tr>
          <tr><td style="color:var(--text-muted)">回调地址</td><td>{{ apiBase }}/auth/callback</td></tr>
          <tr><td style="color:var(--text-muted)">API 文档</td>
            <td><a :href="apiBase + '/docs'" target="_blank" style="color:var(--primary)">{{ apiBase }}/docs ↗</a></td>
          </tr>
        </table>
      </div>
    </div>

    <!-- Tab 2: 告警规则 -->
    <div v-if="activeTab === 'rules'">
      <div v-if="loadingRules" style="padding:40px;text-align:center;color:var(--text-muted)">加载规则中...</div>
      <div v-else-if="ruleError" style="padding:20px;color:var(--danger)">{{ ruleError }}</div>
      <template v-else>
        <div v-for="(groupRules, category) in groupedRules" :key="category" style="margin-bottom:24px">
          <div class="rules-group-title">{{ category }}</div>
          <div class="card rules-card">
            <div
              v-for="(rule, idx) in groupRules"
              :key="rule.rule_key"
              class="rule-item"
              :class="{ 'rule-item-last': idx === groupRules.length - 1 }"
            >
              <div class="rule-header">
                <div class="rule-left">
                  <!-- 开关 -->
                  <label class="toggle-switch">
                    <input
                      type="checkbox"
                      :checked="rule.is_enabled"
                      @change="toggleRule(rule)"
                    />
                    <span class="toggle-track"></span>
                  </label>
                  <div>
                    <div class="rule-name">{{ rule.name }}</div>
                    <div class="rule-desc">{{ rule.description }}</div>
                  </div>
                </div>
                <span class="rule-severity" :class="'sev-' + rule.severity?.toLowerCase()">
                  {{ { CRITICAL: '紧急', WARNING: '警告', INFO: '信息' }[rule.severity] || rule.severity }}
                </span>
              </div>

              <!-- 参数编辑 -->
              <div v-if="rule.params && Object.keys(rule.params).length" class="rule-params">
                <div
                  v-for="(val, paramKey) in rule.params"
                  :key="paramKey"
                  class="param-item"
                >
                  <span class="param-key">{{ paramKey }}:</span>
                  <template v-if="editingParam?.ruleKey === rule.rule_key && editingParam?.paramKey === paramKey">
                    <input
                      class="param-input"
                      v-model="editingParam.value"
                      @blur="saveParam(rule)"
                      @keyup.enter="saveParam(rule)"
                      @keyup.esc="editingParam = null"
                      autofocus
                    />
                  </template>
                  <span
                    v-else
                    class="param-value"
                    @click="startEditParam(rule, paramKey, val)"
                    title="点击编辑"
                  >{{ val }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="Object.keys(groupedRules).length === 0" style="padding:40px;text-align:center;color:var(--text-muted)">
          暂无规则数据
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi, api } from '../api'

const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

// ── Tabs ──────────────────────────────────────────────
const tabs = [
  { key: 'basic', label: '⚙️ 基本设置' },
  { key: 'rules', label: '🚨 告警规则' },
]
const activeTab = ref('basic')

// ── Tab 1: 基本设置 ──────────────────────────────────
const webhookUrl = ref('')
const testing = ref(false)
const testResult = ref(null)
const syncing = ref(false)
const actionMsg = ref('')

async function testFeishu() {
  if (!webhookUrl.value) return alert('请输入 Webhook URL')
  testing.value = true
  testResult.value = null
  try {
    const data = await adminApi.testFeishu(webhookUrl.value)
    testResult.value = { ok: data.success, msg: '' }
  } catch (e) {
    testResult.value = { ok: false, msg: e.message }
  } finally {
    testing.value = false
  }
}

async function triggerSync() {
  syncing.value = true
  try {
    await adminApi.triggerSync()
    actionMsg.value = '✅ 同步任务已触发，后台运行中...'
    setTimeout(() => actionMsg.value = '', 5000)
  } finally {
    syncing.value = false
  }
}

async function triggerReport() {
  await adminApi.triggerReport()
  actionMsg.value = '✅ 日报已触发，请检查飞书消息'
  setTimeout(() => actionMsg.value = '', 5000)
}

// ── Tab 2: 告警规则 ──────────────────────────────────
const rules = ref([])
const loadingRules = ref(false)
const ruleError = ref('')
const editingParam = ref(null) // { ruleKey, paramKey, value }

const groupedRules = computed(() => {
  const groups = {}
  for (const rule of rules.value) {
    const cat = rule.category || '其他规则'
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(rule)
  }
  return groups
})

async function loadRules() {
  loadingRules.value = true
  ruleError.value = ''
  try {
    const data = await api.get('/rules')
    rules.value = data.data?.items || data.items || data.rules || data.data || []
  } catch (e) {
    ruleError.value = '加载规则失败：' + (e.response?.data?.detail || e.message)
  } finally {
    loadingRules.value = false
  }
}

async function toggleRule(rule) {
  const newEnabled = !rule.is_enabled
  rule.is_enabled = newEnabled
  try {
    await api.put(`/rules/${rule.rule_key}`, { is_enabled: newEnabled })
  } catch (e) {
    rule.is_enabled = !newEnabled // rollback
    console.error('Toggle rule failed', e)
  }
}

function startEditParam(rule, paramKey, val) {
  editingParam.value = { ruleKey: rule.rule_key, paramKey, value: String(val) }
}

async function saveParam(rule) {
  if (!editingParam.value) return
  const { ruleKey, paramKey, value } = editingParam.value
  if (ruleKey !== rule.rule_key) return

  // parse value (number or string)
  let parsed = value
  const num = Number(value)
  if (!isNaN(num) && value.trim() !== '') parsed = num

  // update local
  const oldVal = rule.params[paramKey]
  rule.params[paramKey] = parsed
  editingParam.value = null

  try {
    await api.put(`/rules/${ruleKey}`, { params: { ...rule.params } })
  } catch (e) {
    rule.params[paramKey] = oldVal // rollback
    console.error('Save param failed', e)
  }
}

onMounted(() => {
  loadRules()
})
</script>

<style scoped>
/* Tabs */
.tab-bar {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0;
}
.tab-btn {
  padding: 8px 18px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: -1px;
  transition: all 0.15s;
}
.tab-btn:hover { color: var(--text); }
.tab-btn.active { color: var(--primary); border-bottom-color: var(--primary); }

/* Rules */
.rules-group-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 8px;
  padding-left: 4px;
}
.rules-card { padding: 0; overflow: hidden; }
.rule-item {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
}
.rule-item-last { border-bottom: none; }
.rule-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.rule-left {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}
.rule-name { font-size: 13px; font-weight: 600; color: var(--text); }
.rule-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }

.rule-severity {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  flex-shrink: 0;
}
.sev-critical { background: rgba(239,68,68,0.2); color: #f87171; }
.sev-warning  { background: rgba(234,179,8,0.2);  color: #facc15; }
.sev-info     { background: rgba(99,102,241,0.2); color: var(--primary); }

.rule-params {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
  padding-left: 44px;
}
.param-item {
  display: flex;
  align-items: center;
  gap: 4px;
  background: var(--bg-hover);
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 3px 8px;
  font-size: 12px;
}
.param-key { color: var(--text-muted); }
.param-value {
  color: var(--primary);
  font-weight: 600;
  cursor: pointer;
  border-bottom: 1px dashed var(--primary);
  padding-bottom: 1px;
}
.param-value:hover { opacity: 0.8; }
.param-input {
  width: 64px;
  padding: 1px 4px;
  font-size: 12px;
  background: var(--bg-card);
  border: 1px solid var(--primary);
  border-radius: 3px;
  color: var(--text);
  outline: none;
}

/* Toggle switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 36px;
  height: 20px;
  flex-shrink: 0;
  margin-top: 2px;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.toggle-track {
  position: absolute;
  inset: 0;
  background: var(--border);
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s;
}
.toggle-track::before {
  content: '';
  position: absolute;
  width: 14px; height: 14px;
  left: 3px; top: 3px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
}
.toggle-switch input:checked + .toggle-track { background: var(--primary); }
.toggle-switch input:checked + .toggle-track::before { transform: translateX(16px); }
</style>
