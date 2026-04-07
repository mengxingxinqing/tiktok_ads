import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/advertisers' },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { title: '总览' },
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('../views/Alerts.vue'),
    meta: { title: '告警中心' },
  },
  {
    path: '/decisions',
    name: 'Decisions',
    component: () => import('../views/Decisions.vue'),
    meta: { title: '决策中心' },
  },
  {
    path: '/creative-dashboard',
    name: 'CreativeDashboard',
    component: () => import('../views/CreativeDashboard.vue'),
    meta: { title: '创意大盘' },
  },
  {
    path: '/creatives',
    name: 'Creatives',
    component: () => import('../views/Creatives.vue'),
    meta: { title: '创意监控' },
  },
  {
    path: '/creative-manager',
    name: 'CreativeManager',
    component: () => import('../views/CreativeManager.vue'),
    meta: { title: '视频创意管理' },
  },
  {
    path: '/creatives-advanced',
    name: 'CreativesAdvanced',
    component: () => import('../views/CreativesAdvanced.vue'),
    meta: { title: '创意管理（高级筛选）' },
  },
  {
    path: '/advertisers',
    name: 'Advertisers',
    component: () => import('../views/Advertisers.vue'),
    meta: { title: '广告账户' },
  },
  {
    path: '/ads/create',
    name: 'AdCreation',
    component: () => import('../views/AdCreation.vue'),
    meta: { title: '创建Ads广告' },
  },
  {
    path: '/campaigns',
    name: 'Campaigns',
    component: () => import('../views/Campaigns.vue'),
    meta: { title: '广告看板' },
  },
  {
    path: '/gmvmax',
    name: 'GMVMaxDashboard',
    component: () => import('../views/GMVMaxDashboard.vue'),
    meta: { title: 'GMVMax 大盘' },
  },
  {
    path: '/channel',
    name: 'ChannelAnalysis',
    component: () => import('../views/ChannelAnalysis.vue'),
    meta: { title: '渠道分析' },
  },
  {
    path: '/creative-groups',
    name: 'CreativeGroups',
    component: () => import('../views/CreativeGroups.vue'),
    meta: { title: '创意分组' },
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/Products.vue'),
    meta: { title: '商品监控' },
  },
  {
    path: '/growth-planning',
    name: 'GrowthPlanning',
    component: () => import('../views/GrowthPlanning.vue'),
    meta: { title: '梯度增长规划' },
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('../views/Orders.vue'),
    meta: { title: '订单分析' },
  },
  {
    path: '/orders-by-shop',
    name: 'OrdersByShop',
    component: () => import('../views/OrdersByShop.vue'),
    meta: { title: '店铺管理' },
  },
  {
    path: '/decision-impact',
    name: 'DecisionImpact',
    component: () => import('../views/DecisionImpact.vue'),
    meta: { title: '决策效果评估' },
  },
  {
    path: '/creative-heatup',
    name: 'CreativeHeatup',
    component: () => import('../views/CreativeHeatup.vue'),
    meta: { title: '创意加热追踪' },
  },
  {
    path: '/actions',
    name: 'Actions',
    component: () => import('../views/Actions.vue'),
    meta: { title: '快捷操作' },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { title: '系统设置' },
  },
  {
    path: '/auth/success',
    name: 'AuthSuccess',
    component: () => import('../views/AuthSuccess.vue'),
    meta: { title: '授权成功' },
  },
  {
    path: '/auth/error',
    name: 'AuthError',
    component: () => import('../views/AuthError.vue'),
    meta: { title: '授权失败' },
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
