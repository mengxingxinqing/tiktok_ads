<template>
  <div class="auth-error-page">
    <div class="error-container">
      <div class="error-icon">❌</div>
      
      <h1>授权失败</h1>
      
      <p class="message">
        抱歉，授权过程中出现错误。
      </p>

      <div class="error-details">
        <div class="error-message">
          {{ errorMessage || '未知错误，请重试。' }}
        </div>
      </div>

      <div class="button-group">
        <button @click="retry" class="btn btn-primary">
          🔄 重新授权
        </button>
        <router-link to="/dashboard" class="btn btn-secondary">
          📊 返回仪表盘
        </router-link>
      </div>

      <p class="footer-text">
        如果问题持续，请联系技术支持。
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const errorMessage = ref('')

onMounted(() => {
  // 从 URL 参数中获取错误信息
  const msg = route.query.message
  if (msg) {
    errorMessage.value = decodeURIComponent(msg)
  }
})

const retry = () => {
  // 重新开始授权流程
  window.location.href = '/api/auth/login'
}
</script>

<style scoped>
.auth-error-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  padding: 20px;
}

.error-container {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 60px 40px;
  max-width: 600px;
  text-align: center;
  box-shadow: var(--shadow);
}

.error-icon {
  font-size: 80px;
  margin-bottom: 30px;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

h1 {
  font-size: 32px;
  color: var(--danger);
  margin: 0 0 20px 0;
  font-weight: 600;
}

.message {
  font-size: 16px;
  color: var(--text-muted);
  margin: 20px 0;
  line-height: 1.6;
}

.error-details {
  margin: 30px 0;
  text-align: left;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 16px;
  color: var(--danger);
  font-size: 14px;
  font-family: 'Monaco', monospace;
  word-break: break-all;
  line-height: 1.6;
  max-height: 200px;
  overflow-y: auto;
}

.button-group {
  display: flex;
  gap: 12px;
  margin: 40px 0;
  justify-content: center;
  flex-wrap: wrap;
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
