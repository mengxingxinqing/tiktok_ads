<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">📈 梯度增长规划</div>
        <div class="page-subtitle">为新投放生成冷启动 1-10 天的预算计划，三档方案可选</div>
      </div>
      <button class="btn btn-primary" @click="openModal">+ 生成新计划</button>
    </div>

    <!-- 历史推荐列表 -->
    <div class="card">
      <div style="font-weight: 600; margin-bottom: 16px">📋 历史推荐</div>
      <table v-if="recommendations.length > 0">
        <thead>
          <tr>
            <th>对象名称</th><th>当前阶段</th><th>当前花费</th><th>当前 Hook</th>
            <th>推荐方案</th><th>置信度</th><th>状态</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rec in recommendations" :key="rec.id">
            <td style="font-weight: 600">{{ rec.object_name }}</td>
            <td><span class="badge">{{ stageLabel(rec.current_stage) }}</span></td>
            <td>${{ fmt(rec.current_spend) }}</td>
            <td>{{ rec.current_hook.toFixed(1) }}%</td>
            <td style="font-weight: 600">{{ planLabel(rec.recommended) }}</td>
            <td>{{ rec.confidence }}%</td>
            <td><span :class="['badge', rec.status === 'active' ? 'badge-info' : 'badge-success']">
              {{ recStatusLabel(rec.status) }}
            </span></td>
            <td>
              <button class="btn btn-ghost" style="padding:4px 8px;font-size:12px" @click="viewDetail(rec)">
                查看
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <div class="empty-icon">📊</div>
        <div>还没有梯度增长计划</div>
        <div style="margin-top: 8px">
          <button class="btn btn-primary" @click="openModal">创建第一个计划</button>
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="modal.show" class="modal-overlay" @click.self="modal.show=false">
      <div class="modal card" style="width:800px; max-height:90vh; overflow-y:auto">
        <div style="font-size:18px; font-weight:700; margin-bottom:20px">
          📈 {{ modal.recommendation?.object_name || '梯度增长计划' }}
        </div>

        <div v-if="modal.recommendation" style="display: grid; grid-template-columns: 1fr 1fr; gap:16px; margin-bottom:20px">
          <div>
            <span style="color:var(--text-muted); font-size:12px">当前阶段</span>
            <div style="font-size:20px; font-weight:600; margin-top:4px">{{ modal.recommendation.current_stage }}</div>
          </div>
          <div>
            <span style="color:var(--text-muted); font-size:12px">推荐置信度</span>
            <div style="font-size:20px; font-weight:600; margin-top:4px">{{ modal.recommendation.confidence }}%</div>
          </div>
        </div>

        <!-- 三个方案对比 -->
        <div style="margin-bottom:20px">
          <div style="font-weight:600; margin-bottom:12px">三个梯度方案</div>
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap:12px">
            <div
              v-for="(plan, key) in parsedPlans"
              :key="key"
              :class="['plan-box', modal.selectedPlan === key ? 'selected' : '']"
              @click="modal.selectedPlan = key"
            >
              <div style="font-weight:600; margin-bottom:8px">{{ plan.name }}</div>
              <div style="font-size:12px; color:var(--text-muted); margin-bottom:12px">{{ plan.description }}</div>

              <div style="background:var(--bg); padding:8px; border-radius:6px; margin-bottom:12px">
                <div style="font-size:11px; color:var(--text-muted)">日预算计划（前 10 天）</div>
                <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap:4px; margin-top:6px; font-size:11px">
                  <div v-for="(amount, day) in plan.daily_budget" :key="day" style="text-align:center">
                    <div style="color:var(--text-muted)">Day {{ day + 1 }}</div>
                    <div style="font-weight:600">${{ fmt(amount) }}</div>
                  </div>
                </div>
              </div>

              <div style="font-size:12px; color:var(--text-muted)">
                <strong style="color:inherit">逻辑：</strong> {{ plan.rationale }}
              </div>
            </div>
          </div>
        </div>

        <!-- 风险提示 -->
        <div v-if="modal.recommendation?.risk_notes" style="background:var(--info-bg); padding:12px; border-radius:8px; margin-bottom:20px; border-left:3px solid var(--info)">
          <div style="font-weight:600; color:var(--info); margin-bottom:4px">⚠️ 风险提示</div>
          <div style="font-size:13px; line-height:1.5">{{ modal.recommendation.risk_notes }}</div>
        </div>

        <!-- 按钮 -->
        <div style="display:flex; justify-content:flex-end; gap:8px">
          <button class="btn btn-ghost" @click="modal.show=false">取消</button>
          <button
            class="btn btn-primary"
            @click="applyPlan(modal.recommendation.id, modal.selectedPlan)"
            :disabled="!modal.selectedPlan"
          >
            应用 {{ modal.selectedPlan }} 方案
          </button>
        </div>
      </div>
    </div>

    <!-- 生成新计划弹窗 -->
    <div v-if="createModal.show" class="modal-overlay" @click.self="createModal.show=false">
      <div class="modal card" style="width:500px">
        <div style="font-size:16px; font-weight:700; margin-bottom:20px">🚀 生成新的梯度增长计划</div>

        <div style="display: grid; gap:12px">
          <div>
            <label style="font-size:12px; color:var(--text-muted)">广告账户 ID *</label>
            <input v-model="createModal.advertiser_id" placeholder="advertiser_id" />
          </div>
          <div>
            <label style="font-size:12px; color:var(--text-muted)">投放对象类型 *</label>
            <select v-model="createModal.object_type">
              <option value="CAMPAIGN">Campaign</option>
              <option value="ADGROUP">AdGroup</option>
              <option value="VIDEO">Video</option>
            </select>
          </div>
          <div>
            <label style="font-size:12px; color:var(--text-muted)">对象 ID *</label>
            <input v-model="createModal.object_id" placeholder="campaign_id / adgroup_id / video_id" />
          </div>
          <div>
            <label style="font-size:12px; color:var(--text-muted)">对象名称 *</label>
            <input v-model="createModal.object_name" placeholder="Human-readable name" />
          </div>
          <div>
            <label style="font-size:12px; color:var(--text-muted)">当前日花费 ($) *</label>
            <input v-model.number="createModal.current_spend" type="number" min="0" step="0.01" />
          </div>
          <div>
            <label style="font-size:12px; color:var(--text-muted)">当前 Hook Rate (%) *</label>
            <input v-model.number="createModal.current_hook" type="number" min="0" max="100" step="0.1" />
          </div>
          <div>
            <label style="font-size:12px; color:var(--text-muted)">已运行天数 *</label>
            <input v-model.number="createModal.days_running" type="number" min="0" step="1" />
          </div>
        </div>

        <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:20px">
          <button class="btn btn-ghost" @click="createModal.show=false">取消</button>
          <button class="btn btn-primary" @click="generatePlan" :disabled="!canGenerate">
            {{ generating ? '生成中...' : '生成计划' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../api'

const recommendations = ref([])
const generating = ref(false)

const fmt = (v) => Number(v || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const stageLabel = s => ({ WARM_UP: '冷启动', GROWTH: '上升期', PEAK: '峰值期', DECAY: '衰退期', FATIGUE: '疲劳期', UNKNOWN: '未知' }[s] || s)
const planLabel = p => ({ conservative: '保守', standard: '标准', aggressive: '激进' }[p] || p)
const recStatusLabel = s => ({ active: '进行中', completed: '已完成', cancelled: '已取消' }[s] || s)

const modal = ref({ show: false, recommendation: null, selectedPlan: null })
const createModal = ref({
  show: false,
  advertiser_id: '',
  object_type: 'CAMPAIGN',
  object_id: '',
  object_name: '',
  current_spend: 50,
  current_hook: 0,
  days_running: 1,
})

const canGenerate = computed(() => 
  createModal.value.advertiser_id && 
  createModal.value.object_id && 
  createModal.value.object_name && 
  createModal.value.current_spend > 0
)

const parsedPlans = computed(() => {
  if (!modal.value.recommendation) return {}
  try {
    return {
      conservative: JSON.parse(modal.value.recommendation.conservative_plan),
      standard: JSON.parse(modal.value.recommendation.standard_plan),
      aggressive: JSON.parse(modal.value.recommendation.aggressive_plan),
    }
  } catch {
    return {}
  }
})

function openModal() {
  createModal.value.show = true
}

function viewDetail(rec) {
  modal.value.recommendation = rec
  modal.value.selectedPlan = null
  modal.value.show = true
}

async function generatePlan() {
  generating.value = true
  try {
    const res = await api.post(`/analytics/growth-recommendation`, {
      advertiser_id: createModal.value.advertiser_id,
      object_type: createModal.value.object_type,
      object_id: createModal.value.object_id,
      object_name: createModal.value.object_name,
      current_daily_spend: createModal.value.current_spend,
      current_hook_rate: createModal.value.current_hook,
      days_running: createModal.value.days_running,
    })

    // 打开详情弹窗展示结果
    modal.value.recommendation = res.data
    modal.value.selectedPlan = null
    modal.value.show = true
    createModal.value.show = false

    // 刷新列表
    await load()
  } catch (e) {
    alert('生成失败: ' + e.message)
  } finally {
    generating.value = false
  }
}

async function applyPlan(recommendationId, chosenPlan) {
  try {
    await api.post(`/analytics/growth-recommendation/${recommendationId}/apply`, {
      chosen_plan: chosenPlan,
    })
    alert('已应用 ' + chosenPlan + ' 方案')
    modal.value.show = false
    await load()
  } catch (e) {
    alert('应用失败: ' + e.message)
  }
}

async function load() {
  try {
    const advertiserId = localStorage.getItem('current_advertiser_id') || 'test'
    const res = await api.get(`/analytics/growth-recommendation/${advertiserId}`)
    recommendations.value = res.data || []
  } catch (e) {
    console.error('Failed to load recommendations:', e)
  }
}

onMounted(load)
</script>

<style scoped>
.plan-box {
  padding: 16px;
  background: var(--bg);
  border: 2px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.plan-box:hover {
  border-color: var(--primary);
}

.plan-box.selected {
  border-color: var(--primary);
  background: var(--primary-bg);
  box-shadow: 0 0 0 3px var(--primary-shadow);
}
</style>
