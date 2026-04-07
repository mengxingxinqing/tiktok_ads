#!/bin/bash
# ==========================================
# TikTok Ads System - 一键部署/更新脚本
# 服务器: 123.60.90.100
# 域名: https://ads.tongtools.com
# ==========================================
#
# 架构:
#   Nginx (443/80) → /api/* → Gunicorn/Uvicorn (8890)
#                  → /*     → 前端静态文件
#
# 使用方式:
#   首次部署:  bash deploy.sh init
#   更新部署:  bash deploy.sh
#   仅后端:    bash deploy.sh backend
#   仅前端:    bash deploy.sh frontend
#   重启服务:  bash deploy.sh restart

set -e

# ========== 配置 ==========
SERVER="root@123.60.90.100"
SERVER_PASS="Tong1shuai"
REMOTE_DIR="/www/wwwroot/tiktok-ads"
DOMAIN="ads.tongtools.com"
BACKEND_PORT=8890
SERVICE_NAME="tiktok-ads"

LOCAL_BACKEND="e:/code/tiktok-ads-system"
LOCAL_FRONTEND="e:/code/tiktok-ads-frontend"

# ========== 工具函数 ==========
log() { echo -e "\033[36m[$(date +%H:%M:%S)]\033[0m $1"; }
err() { echo -e "\033[31m[ERROR]\033[0m $1"; exit 1; }

# SSH/SCP 包装
# 优先用 SSH Key，如果没有则用 sshpass
if command -v sshpass &>/dev/null; then
    remote() { sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no "$SERVER" "$@"; }
    upload() { sshpass -p "$SERVER_PASS" rsync -azP --delete -e "ssh -o StrictHostKeyChecking=no" "$@"; }
else
    remote() { ssh -o StrictHostKeyChecking=no "$SERVER" "$@"; }
    upload() { rsync -azP --delete -e "ssh -o StrictHostKeyChecking=no" "$@"; }
fi

# 检查连接
check_connection() {
    if ! remote "echo ok" &>/dev/null; then
        err "Cannot connect to $SERVER. Run 'bash deploy/setup-ssh.sh' first to set up SSH key auth."
    fi
    log "Server connection OK"
}

# ========== 前端构建 ==========
build_frontend() {
    log "Building frontend..."
    cd "$LOCAL_FRONTEND"
    npm install --legacy-peer-deps
    npm run build
    log "Frontend built → $(du -sh ../tiktok-ads-frontend-dist | cut -f1)"
}

# ========== 首次初始化 ==========
init_server() {
    log "Initializing server..."

    remote bash -s <<'REMOTE_INIT'
set -e

# 创建项目目录
mkdir -p /www/wwwroot/tiktok-ads/{backend,frontend,logs}

# 安装 Python 3.11+ (如果没有)
if ! command -v python3.11 &>/dev/null && ! python3 --version 2>&1 | grep -qE "3\.(1[1-9]|[2-9])"; then
    echo "Installing Python 3.11..."
    apt update && apt install -y python3.11 python3.11-venv python3.11-dev || \
    yum install -y python3.11 python3.11-devel || \
    echo "Please install Python 3.11+ manually"
fi

# 创建虚拟环境
cd /www/wwwroot/tiktok-ads/backend
if [ ! -d "venv" ]; then
    python3 -m venv venv || python3.11 -m venv venv
fi

# 安装 Node.js (如果没有)
if ! command -v node &>/dev/null; then
    echo "Node.js not found, please install via BT Panel"
fi

# 创建 systemd 服务
cat > /etc/systemd/system/tiktok-ads.service <<EOF
[Unit]
Description=TikTok Ads Backend
After=network.target mysql.service redis.service

[Service]
Type=simple
User=root
WorkingDirectory=/www/wwwroot/tiktok-ads/backend
Environment=PATH=/www/wwwroot/tiktok-ads/backend/venv/bin:/usr/local/bin:/usr/bin
ExecStart=/www/wwwroot/tiktok-ads/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8890 --workers 2 --log-level info
Restart=always
RestartSec=5
StandardOutput=append:/www/wwwroot/tiktok-ads/logs/backend.log
StandardError=append:/www/wwwroot/tiktok-ads/logs/backend.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable tiktok-ads

echo "Server initialized!"
REMOTE_INIT

    log "Server initialization done"
}

# ========== Nginx 配置 ==========
setup_nginx() {
    log "Setting up Nginx config..."

    remote bash -s <<'REMOTE_NGINX'
# 写 Nginx 配置（兼容宝塔）
cat > /www/server/panel/vhost/nginx/ads.tongtools.com.conf <<'EOF'
server {
    listen 80;
    server_name ads.tongtools.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ads.tongtools.com;

    # SSL 证书（宝塔自动申请的路径）
    ssl_certificate /www/server/panel/vhost/cert/ads.tongtools.com/fullchain.pem;
    ssl_certificate_key /www/server/panel/vhost/cert/ads.tongtools.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 前端静态文件
    root /www/wwwroot/tiktok-ads/frontend;
    index index.html;

    # API 请求转发到后端
    location /api/ {
        # 去掉 /api 前缀转发
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://127.0.0.1:8890;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        client_max_body_size 500M;
    }

    # 直接转发（不加 /api 前缀的后端路由）
    location ~ ^/(auth|dashboard|campaigns|creatives|products|orders|ads|shop-summary|gmvmax|health|alerts|decisions|settings|rules|boost|analytics|shops|creative-groups|creative-dashboard|comments|channel) {
        proxy_pass http://127.0.0.1:8890;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        client_max_body_size 500M;
    }

    # SPA fallback - 所有其他路由返回 index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态文件缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    access_log /www/wwwlogs/ads.tongtools.com.log;
    error_log /www/wwwlogs/ads.tongtools.com.error.log;
}
EOF

# 检测 Nginx 配置是否正确
nginx -t && nginx -s reload
echo "Nginx configured!"
REMOTE_NGINX

    log "Nginx setup done"
}

# ========== 部署后端 ==========
deploy_backend() {
    log "Deploying backend..."

    # 同步代码（排除不需要的文件）
    upload \
        --exclude 'venv/' \
        --exclude '__pycache__/' \
        --exclude '*.pyc' \
        --exclude '.env' \
        --exclude 'logs/' \
        --exclude '.git/' \
        --exclude 'scripts/' \
        --exclude 'docs/' \
        "$LOCAL_BACKEND/" "$SERVER:$REMOTE_DIR/backend/"

    # 远程安装依赖并重启
    remote bash -s <<'REMOTE_BACKEND'
set -e
cd /www/wwwroot/tiktok-ads/backend

# 安装/更新依赖
source venv/bin/activate
pip install -r requirements.txt -q --upgrade 2>&1 | tail -3

# 数据库迁移（如果有 alembic）
if [ -f "alembic.ini" ]; then
    alembic upgrade head 2>&1 || echo "Alembic migration skipped"
fi

# 重启服务
systemctl restart tiktok-ads
sleep 2

# 检查状态
if systemctl is-active --quiet tiktok-ads; then
    echo "Backend is running!"
else
    echo "Backend failed to start. Logs:"
    tail -20 /www/wwwroot/tiktok-ads/logs/backend.log
    exit 1
fi
REMOTE_BACKEND

    log "Backend deployed!"
}

# ========== 部署前端 ==========
deploy_frontend() {
    # 构建
    build_frontend

    log "Deploying frontend..."

    # 同步构建产物
    upload \
        "$LOCAL_FRONTEND/../tiktok-ads-frontend-dist/" \
        "$SERVER:$REMOTE_DIR/frontend/"

    log "Frontend deployed!"
}

# ========== 生产环境 .env ==========
setup_env() {
    log "Setting up production .env..."

    remote bash -s <<'REMOTE_ENV'
cat > /www/wwwroot/tiktok-ads/backend/.env <<'EOF'
# TikTok API
TIKTOK_APP_ID=7591801546375954449
TIKTOK_APP_SECRET=d4e8663d1401b5e42f907d7e9095481b3843f285
TIKTOK_REDIRECT_URI=https://ads.tongtools.com/auth/callback

# LLM
LLM_API_BASE=https://api.tongtools.com
LLM_API_KEY=sk-apTZr7qZ8K1vAjTlMmAVSh5Hx8Nx0OqOvIPszsud50bhjkcv
LLM_MODEL=gpt-5

# Database (生产环境，根据实际修改)
DATABASE_URL=mysql+aiomysql://tk_ads:FcsyN4Da7pdwXaZa@localhost:3306/tk_ads?charset=utf8mb4

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=tiktok-ads-prod-$(openssl rand -hex 16)
DEBUG=false
LOG_LEVEL=INFO
SYNC_INTERVAL_MINUTES=30
EOF

echo "Production .env created!"
REMOTE_ENV

    log "Production .env done"
}

# ========== 快速部署（默认） ==========
deploy_all() {
    deploy_backend
    deploy_frontend
    log "Full deployment complete!"
    log "Visit: https://$DOMAIN"
}

# ========== 重启 ==========
restart() {
    log "Restarting services..."
    remote "systemctl restart tiktok-ads && nginx -s reload"
    log "Services restarted"
}

# ========== 查看日志 ==========
logs() {
    remote "tail -100 /www/wwwroot/tiktok-ads/logs/backend.log"
}

# ========== 主入口 ==========
check_connection

case "${1:-deploy}" in
    init)
        init_server
        setup_env
        setup_nginx
        deploy_all
        ;;
    backend)
        deploy_backend
        ;;
    frontend)
        deploy_frontend
        ;;
    nginx)
        setup_nginx
        ;;
    env)
        setup_env
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    deploy|"")
        deploy_all
        ;;
    *)
        echo "Usage: bash deploy.sh [init|deploy|backend|frontend|nginx|env|restart|logs]"
        exit 1
        ;;
esac
