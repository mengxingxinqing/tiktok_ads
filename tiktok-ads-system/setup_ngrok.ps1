# TikTok Ads System - ngrok 快速启动脚本
# 使用方式: .\setup_ngrok.ps1 -token YOUR_NGROK_TOKEN

param(
    [Parameter(Mandatory=$false)]
    [string]$token = "",
    [Parameter(Mandatory=$false)]
    [int]$port = 8000
)

Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   TikTok Ads System - ngrok Setup        ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan

# 1. 检查 ngrok 是否安装
Write-Host "`n[1/4] 检查 ngrok 安装状态..." -ForegroundColor Yellow
$ngrokPath = where.exe ngrok 2>$null
if (-not $ngrokPath) {
    Write-Host "❌ ngrok 未安装" -ForegroundColor Red
    Write-Host "请先下载 ngrok: https://ngrok.com/download" -ForegroundColor Yellow
    Write-Host "然后运行: ngrok config add-authtoken YOUR_TOKEN" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ ngrok 已安装: $ngrokPath" -ForegroundColor Green

# 2. 如果提供了 token，更新配置
if ($token) {
    Write-Host "`n[2/4] 更新 ngrok token..." -ForegroundColor Yellow
    & ngrok config add-authtoken $token
    Write-Host "✅ ngrok token 已更新" -ForegroundColor Green
} else {
    Write-Host "`n[2/4] 跳过 token 设置（已配置）" -ForegroundColor Green
}

# 3. 获取公网 URL
Write-Host "`n[3/4] 启动 ngrok（等待获取公网 URL）..." -ForegroundColor Yellow

# 在后台启动 ngrok
$ngrokProcess = Start-Process ngrok -ArgumentList "http $port --bind-tls=true" -PassThru -NoNewWindow
Start-Sleep -Seconds 3

# 从 ngrok API 获取 URL
$ngrokUrl = $null
try {
    $response = Invoke-WebRequest -Uri "http://localhost:4040/api/tunnels" -ErrorAction Stop
    $tunnels = $response.Content | ConvertFrom-Json
    $ngrokUrl = $tunnels.tunnels[0].public_url
    
    if ($ngrokUrl) {
        Write-Host "✅ 公网 URL: $ngrokUrl" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  无法获取 ngrok URL，请手动检查 ngrok 是否正常启动" -ForegroundColor Yellow
    Write-Host "访问 http://localhost:4040 查看 ngrok 状态" -ForegroundColor Yellow
}

# 4. 更新 .env 配置
Write-Host "`n[4/4] 更新 .env 配置..." -ForegroundColor Yellow

if ($ngrokUrl) {
    $envFile = ".\\.env"
    $redirectUri = "$ngrokUrl/auth/callback"
    
    if (Test-Path $envFile) {
        $content = Get-Content $envFile -Raw
        
        # 更新或添加 TIKTOK_REDIRECT_URI
        if ($content -match 'TIKTOK_REDIRECT_URI=') {
            $content = $content -replace 'TIKTOK_REDIRECT_URI=.*', "TIKTOK_REDIRECT_URI=$redirectUri"
        } else {
            $content += "`nTIKTOK_REDIRECT_URI=$redirectUri"
        }
        
        # 如果需要，也更新 VITE_API_BASE（前端）
        $apiBase = "$ngrokUrl"
        if ($content -match 'VITE_API_BASE=') {
            $content = $content -replace 'VITE_API_BASE=.*', "VITE_API_BASE=$apiBase"
        } else {
            $content += "`nVITE_API_BASE=$apiBase"
        }
        
        Set-Content $envFile $content
        Write-Host "✅ .env 已更新" -ForegroundColor Green
        Write-Host "   TIKTOK_REDIRECT_URI=$redirectUri" -ForegroundColor Cyan
    } else {
        Write-Host "❌ 找不到 .env 文件" -ForegroundColor Red
    }
}

Write-Host "`n╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         ngrok 已启动！                    ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host "`n📋 重要信息:" -ForegroundColor Yellow
Write-Host "  - ngrok 公网 URL: $ngrokUrl"
Write-Host "  - 本地后端: http://localhost:$port"
Write-Host "  - ngrok 网页控制台: http://localhost:4040"
Write-Host "  - OAuth 回调: $ngrokUrl/auth/callback"

Write-Host "`n📝 下一步:" -ForegroundColor Yellow
Write-Host "  1. 重启后端应用 (会自动读取新的 .env)"
Write-Host "  2. 测试 OAuth 授权流程"
Write-Host "  3. ngrok 会持续运行，直到你关闭此窗口"

Write-Host "`n💡 提示:" -ForegroundColor Cyan
Write-Host "  - 如果 ngrok 地址变化，需要重新运行此脚本"
Write-Host "  - 在 TikTok 应用配置中也要更新 Redirect URI"
Write-Host "  - 开发完成后，改回 localhost 配置"

# 保持 ngrok 进程运行
Write-Host "`n⏳ ngrok 正在运行，按 Ctrl+C 停止..." -ForegroundColor Yellow
Wait-Process -Id $ngrokProcess.Id
