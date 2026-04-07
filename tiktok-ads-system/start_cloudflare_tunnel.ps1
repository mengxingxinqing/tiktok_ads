# Cloudflare Tunnel 快速启动脚本
# 用于 TikTok Ads 系统内网穿透

Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  TikTok Ads - Cloudflare Tunnel Setup     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan

$port = 8000

Write-Host "`n[1/3] 启动 Cloudflare Tunnel..." -ForegroundColor Yellow
Write-Host "      本地端口: localhost:$port" -ForegroundColor Gray
Write-Host "      穿透方式: Cloudflare Tunnel (无需账户)" -ForegroundColor Gray

# 启动 Cloudflare Tunnel
# --url http://localhost:8000 指向本地应用
cloudflared tunnel --url http://localhost:$port --no-autoupdate

Write-Host "`n[2/3] 获取公网 URL..." -ForegroundColor Yellow
Write-Host "      请等待 cloudflared 显示公网 URL" -ForegroundColor Gray

Write-Host "`n[3/3] 更新 .env 配置..." -ForegroundColor Yellow
Write-Host "      复制输出的 URL（类似 https://xxx.trycloudflare.com）" -ForegroundColor Gray
Write-Host "      更新 .env 中的 TIKTOK_REDIRECT_URI" -ForegroundColor Gray

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📝 使用说明:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n1️⃣  Cloudflare Tunnel 启动后，会显示类似这样的 URL：" -ForegroundColor Cyan
Write-Host "    https://abc123.trycloudflare.com" -ForegroundColor Green

Write-Host "`n2️⃣  复制该 URL，编辑 .env 文件：" -ForegroundColor Cyan
Write-Host "    TIKTOK_REDIRECT_URI=https://abc123.trycloudflare.com/auth/callback" -ForegroundColor Green

Write-Host "`n3️⃣  重启后端应用，使新配置生效" -ForegroundColor Cyan

Write-Host "`n4️⃣  在 TikTok Developer Platform 中更新：" -ForegroundColor Cyan
Write-Host "    Redirect URI = https://abc123.trycloudflare.com/auth/callback" -ForegroundColor Green

Write-Host "`n💡 提示：" -ForegroundColor Yellow
Write-Host "  - Cloudflare Tunnel 免费版，每次启动 URL 都会变化" -ForegroundColor Gray
Write-Host "  - 无需注册账户，即开即用" -ForegroundColor Gray
Write-Host "  - 非常稳定和快速" -ForegroundColor Gray
Write-Host "  - 按 Ctrl+C 停止 Tunnel" -ForegroundColor Gray

Write-Host "`n⏳ Tunnel 正在运行中..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
