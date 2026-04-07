import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 15000,
})

api.interceptors.response.use(
  res => res.data,
  err => {
    console.error('API Error:', err.response?.data || err.message)
    return Promise.reject(err)
  }
)

export const dashboardApi = {
  overview: () => api.get('/dashboard/overview'),
  spendTrend: (days = 7) => api.get('/dashboard/spend-trend', { params: { days } }),
  topAds: (metric = 'spend', limit = 20) => api.get('/dashboard/top-ads', { params: { metric, limit } }),
}

export const alertApi = {
  list: (params = {}) => api.get('/alerts', { params }),
  resolve: (id) => api.post(`/alerts/${id}/resolve`),
}

export const decisionApi = {
  list: (params = {}) => api.get('/decisions', { params }),
  approve: (id) => api.post(`/decisions/${id}/approve`),
  reject: (id) => api.post(`/decisions/${id}/reject`),
  rollback: (id) => api.post(`/decisions/${id}/rollback`),
}

export const advertiserApi = {
  list: () => api.get('/auth/advertisers'),
  getAuthUrl: (remark) => api.get('/auth/login', { params: { remark } }),
  delete: (advertiserId) => api.delete(`/auth/advertisers/${advertiserId}`),
  refreshBalance: () => api.post('/auth/balance/refresh'),
}

export const creativeApi = {
  list: (params = {}) => api.get('/creatives', { params }),
  stats: (advertiserId) => api.get('/creatives/stats/overview', { params: advertiserId ? { advertiser_id: advertiserId } : {} }),
  trend: (videoId, advertiserId, days = 14) => api.get(`/creatives/${videoId}/trend`, { params: { advertiser_id: advertiserId, days } }),
  fatigue: (advertiserId) => api.get('/creatives/fatigue', { params: advertiserId ? { advertiser_id: advertiserId } : {} }),
}

export const boostApi = {
  candidates: (advertiserId) => api.get('/boost/candidates', { params: advertiserId ? { advertiser_id: advertiserId } : {} }),
  scan: (advertiserId) => api.post(`/boost/scan/${advertiserId}`),
}

export const adminApi = {
  triggerSync: () => api.post('/admin/sync/trigger'),
  triggerReport: () => api.post('/admin/report/trigger'),
  testFeishu: (webhookUrl) => api.post('/admin/feishu/test', null, { params: { webhook_url: webhookUrl } }),
}

export const adsApi = {
  createCampaign: (payload) => api.post('/ads/campaign/create', payload),
  createFullCampaign: (payload) => api.post('/ads/campaign/create-full', payload),
  uploadVideo: (formData) => api.post('/ads/video/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  uploadImage: (formData) => api.post('/ads/image/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
}

// 导出 api 客户端本身，方便直接使用
export { api }
