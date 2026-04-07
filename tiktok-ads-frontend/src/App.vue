<template>
  <div class="layout">
    <!-- 侧边栏 -->
    <nav class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">🎯</span>
        <span class="logo-text">TikTok Ads</span>
      </div>

      <!-- 全局筛选器 -->
      <div class="global-filter">
        <select v-model="globalShopId" @change="onShopChange" class="shop-select">
          <option value="">🏪 全部店铺</option>
          <option v-for="s in globalFilterStore.shops" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
      </div>

      <div class="sidebar-nav">
        <template v-for="group in navGroups" :key="group.label">
          <div v-if="group.label" class="nav-group-label">{{ group.label }}</div>
          <router-link
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="nav-item"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
            <span v-if="getBadge(item.badge)" class="nav-badge">{{ getBadge(item.badge) }}</span>
          </router-link>
        </template>
      </div>

      <div class="sidebar-footer">
        <div class="system-status">
          <span :class="['status-dot', systemOnline ? 'online' : 'offline']"></span>
          {{ systemOnline ? '系统运行中' : '系统离线' }}
        </div>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import { dashboardApi, api } from './api'
import { useGlobalFilterStore } from './stores/globalFilter'

const systemOnline = ref(false)
const pendingDecisions = ref(0)
const unresolved = ref(0)

const globalFilterStore = useGlobalFilterStore()
const globalShopId = ref('')

// provide 给所有子页面
provide('globalShopId', globalShopId)
provide('globalShopIdRef', globalShopId)

const navGroups = [
  {
    label: '',
    items: [
      { path: '/advertisers',       icon: '🏢', label: '广告户管理' },
      { path: '/orders-by-shop',    icon: '🏪', label: '店铺列表' },
      { path: '/campaigns',         icon: '📋', label: '广告列表' },
      { path: '/creatives',         icon: '🎬', label: '创意列表' },
      { path: '/creative-manager',  icon: '📤', label: '视频管理' },
      { path: '/creative-dashboard', icon: '📊', label: '状态分布概览' },
    ]
  },
]

const getBadge = (key) => {
  if (!key) return null
  if (key === 'alerts') return unresolved.value || null
  if (key === 'decisions') return pendingDecisions.value || null
  return null
}

async function onShopChange() {
  const shop = globalFilterStore.shops.find(s => s.id === globalShopId.value)
  globalFilterStore.setShop(globalShopId.value, shop?.name || '')
}

async function loadShops() {
  try {
    const data = await api.get('/shop-summary/list')
    const list = data.data?.items || data.items || data.shops || data.data || []
    globalFilterStore.setShops(list)
  } catch (e) {
    console.error('Load shops failed', e)
  }
}

onMounted(async () => {
  await loadShops()
  try {
    const data = await dashboardApi.overview()
    systemOnline.value = true
    unresolved.value = data.alerts?.unresolved || 0
    pendingDecisions.value = data.pending_decisions || 0
  } catch {
    systemOnline.value = false
  }
})
</script>

<style scoped>
.layout { display: flex; height: 100vh; overflow: hidden; }

.sidebar {
  width: 220px; flex-shrink: 0;
  background: var(--bg-card);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
}

.sidebar-logo {
  display: flex; align-items: center; gap: 10px;
  padding: 20px 16px; border-bottom: 1px solid var(--border);
  font-weight: 700; font-size: 16px;
}
.logo-icon { font-size: 22px; }

/* 全局筛选器 */
.global-filter {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
}
.shop-select {
  width: 100%;
  background: var(--bg-hover);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  outline: none;
}
.shop-select:focus { border-color: var(--primary); }

.sidebar-nav { flex: 1; padding: 8px 8px; overflow-y: auto; }

/* 分组标题 */
.nav-group-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 8px 12px 4px;
  margin-top: 4px;
  opacity: 0.6;
}

.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 12px; border-radius: 8px;
  color: var(--text-muted); text-decoration: none;
  font-size: 13px; font-weight: 500;
  transition: all 0.15s;
  margin-bottom: 2px;
}
.nav-item:hover { background: var(--bg-hover); color: var(--text); }
.nav-item.router-link-active { background: rgba(99,102,241,0.15); color: var(--primary); }
.nav-icon { font-size: 16px; width: 20px; text-align: center; }
.nav-badge {
  margin-left: auto;
  background: var(--danger); color: #fff;
  font-size: 10px; font-weight: 700;
  padding: 1px 6px; border-radius: 99px;
  min-width: 18px; text-align: center;
}

.sidebar-footer {
  padding: 12px 16px; border-top: 1px solid var(--border);
}
.system-status { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text-muted); }
.status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.status-dot.online  { background: var(--success); box-shadow: 0 0 6px var(--success); }
.status-dot.offline { background: var(--danger); }

.main-content { flex: 1; overflow-y: auto; }
</style>
