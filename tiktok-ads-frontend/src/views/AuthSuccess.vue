<template>
  <div class="auth-success-page">
    <div class="success-container">
      <div class="success-icon">✅</div>
      
      <h1>授权成功！</h1>
      
      <p class="message">
        已成功授权 <span class="highlight">{{ advertiserCount }}</span> 个广告账户
      </p>

      <div v-if="advertisers.length > 0" class="advertiser-list">
        <h3>已授权的账户：</h3>
        <div v-for="(adv, index) in advertisers" :key="index" class="advertiser-item">
          <span class="id">{{ adv.id }}</span>
          <span class="name">{{ adv.name }}</span>
        </div>
      </div>

      <div class="button-group">
        <router-link to="/ads/create" class="btn btn-primary">
          🎬 立即创建广告
        </router-link>
        <router-link to="/dashboard" class="btn btn-secondary">
          📊 返回仪表盘
        </router-link>
      </div>

      <p class="footer-text">
        你现在可以在系统中创建和管理广告了！
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const advertiserCount = ref(0)
const advertisers = ref([])

onMounted(() => {
  // 从 URL 参数中解析
  const count = route.query.count || 0
  const advertiserStr = route.query.advertisers || ''
  
  advertiserCount.value = parseInt(count)
  
  if (advertiserStr) {
    const items = advertiserStr.split(',')
    advertisers.value = items.map(item => {
      const [id, name] = item.split(':')
      return { id, name: decodeURIComponent(name) }
    })
  }

  // 3秒后自动跳转到广告创建页面
  setTimeout(() => {
    router.push('/ads/create')
  }, 3000)
})
</script>

<style scoped>
.auth-success-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  padding: 20px;
}

.success-container {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 60px 40px;
  max-width: 600px;
  text-align: center;
  box-shadow: var(--shadow);
}

.success-icon {
  font-size: 80px;
  margin-bottom: 30px;
  animation: scaleIn 0.5s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

h1 {
  font-size: 32px;
  color: var(--text);
  margin: 0 0 20px 0;
  font-weight: 600;
}

.message {
  font-size: 16px;
  color: var(--text-muted);
  margin: 20px 0;
  line-height: 1.6;
}

.highlight {
  color: var(--success);
  font-weight: 600;
  font-size: 20px;
}

.advertiser-list {
  margin: 40px 0;
  text-align: left;
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 8px;
  padding: 20px;
}

.advertiser-list h3 {
  margin: 0 0 15px 0;
  color: var(--text);
  font-size: 14px;
  font-weight: 600;
}

.advertiser-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(16, 185, 129, 0.1);
}

.advertiser-item:last-child {
  border-bottom: none;
}

.advertiser-item .id {
  background: var(--primary);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Monaco', monospace;
  min-width: 120px;
  text-align: center;
}

.advertiser-item .name {
  color: var(--text);
  flex: 1;
  font-size: 14px;
}

.button-group {
  display: flex;
  gap: 12px;
  margin: 40px 0;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
}

.btn-secondary {
  background: var(--border);
  color: var(--text);
}

.btn-secondary:hover {
  background: var(--bg-hover);
  transform: translateY(-2px);
}

.footer-text {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 30px;
  margin-bottom: 0;
}
</style>
