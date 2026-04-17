import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import http from 'node:http'

const BACKEND = 'http://localhost:8890'
const backendUrl = new URL(BACKEND)

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'api-proxy',
      configureServer(server) {
        // 在 Vite SPA fallback 之前拦截
        // 浏览器页面导航 Accept 含 text/html → 走 Vite SPA
        // API 请求 (axios/fetch) Accept 是 application/json → proxy 到后端
        server.middlewares.use((req, res, next) => {
          const accept = req.headers.accept || ''
          const url = req.url || ''

          // Vite 内部资源，不拦截
          if (url.startsWith('/@') || url.startsWith('/src/') || url.startsWith('/node_modules/') || url.includes('.hot-update.')) {
            return next()
          }

          // 页面导航请求（浏览器地址栏），走 Vite SPA
          if (accept.includes('text/html')) {
            return next()
          }

          // 其他请求（API）→ proxy 到后端
          // 与生产 nginx 行为一致：/api/ 前缀 rewrite 剥掉，后端 router 都是无 /api 的
          const strippedPath = url.startsWith('/api/') ? url.slice(4) : url
          const proxyReq = http.request({
            hostname: backendUrl.hostname,
            port: backendUrl.port,
            path: strippedPath,
            method: req.method,
            headers: { ...req.headers, host: backendUrl.host },
          }, (proxyRes) => {
            res.writeHead(proxyRes.statusCode, proxyRes.headers)
            proxyRes.pipe(res)
          })

          proxyReq.on('error', (err) => {
            res.writeHead(502)
            res.end(`Backend unavailable: ${err.message}`)
          })

          req.pipe(proxyReq)
        })
      },
    },
  ],
  appType: 'spa',
  server: {
    port: 8891,
    host: '0.0.0.0',
    strictPort: true,
  },
  build: {
    outDir: '../tiktok-ads-frontend-dist',
  },
})
