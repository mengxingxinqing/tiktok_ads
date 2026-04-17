import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
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

// ===================== 智能涨粉模块 API =====================

export const growthApi = {
  // TK 账号
  listTkAccounts: (params = {}) => api.get('/growth/tk-accounts', { params }),
  createTkAccount: (payload) => api.post('/growth/tk-accounts', null, { params: payload }),
  // axios.patch(url, data, config) —— 第二参是 body。后端用 Query()，body 必须传 null
  updateTkAccount: (accountId, payload) =>
    api.patch(`/growth/tk-accounts/${accountId}`, null, { params: payload }),
  refreshFollowers: (accountId) => api.post(`/growth/tk-accounts/${accountId}/refresh-followers`),

  // 素材库
  listCreatives: (params = {}) => api.get('/growth/creatives', { params }),
  createCreative: (payload) => api.post('/growth/creatives', null, { params: payload }),
  bindAuthCode: ({ advertiser_id, auth_code, tk_account_id }) =>
    api.post('/growth/creatives/bind-auth-code', null, {
      params: { advertiser_id, auth_code, tk_account_id },
    }),

  // Campaign
  listCampaigns: (params = {}) => api.get('/growth/campaigns', { params }),
  // payload: { assignments: [{tk_account_id, material_id?}], ad_account_id?, target_cost_per_10k }
  createCampaigns: (payload) => api.post('/growth/campaigns', payload),
  startCampaign: (campaignId) => api.post(`/growth/campaigns/${campaignId}/start`),
  stopCampaign: (campaignId, reason = 'MANUAL') =>
    api.post(`/growth/campaigns/${campaignId}/stop`, null, { params: { reason } }),

  // Ad Account
  listAdAccounts: () => api.get('/growth/ad-accounts'),
  syncAdAccounts: (bc_advertiser_id) =>
    api.post('/growth/ad-accounts/sync', null, {
      params: bc_advertiser_id ? { bc_advertiser_id } : {},
    }),
  // 涨粉模块独立授权（与 gmvmax 的 advertisers 表隔离）
  getAuthUrl: (remark) =>
    api.get('/growth/auth/login', { params: remark ? { remark } : {} }),
  updateAdAccountPriority: (advertiserId, priority) =>
    api.patch(`/growth/ad-accounts/${advertiserId}/priority`, null, { params: { priority } }),
  toggleAdAccountAllowUse: (advertiserId, allow_use) =>
    api.patch(`/growth/ad-accounts/${advertiserId}/allow-use`, null, { params: { allow_use } }),

  // 汇率
  listExchangeRates: () => api.get('/growth/exchange-rates'),
  upsertExchangeRate: (currency, rate) =>
    api.post('/growth/exchange-rates', null, { params: { currency, rate } }),
}

// 导出 api 客户端本身，方便直接使用
export { api }
