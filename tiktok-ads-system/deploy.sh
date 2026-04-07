#!/bin/bash
# TikTok Ads System 一键部署脚本
# 在服务器上执行: bash deploy.sh

set -e

PROJECT_DIR="/www/wwwroot/ads.tongtools.com"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="tiktok-ads"

echo "=== TikTok Ads System 部署开始 ==="

# 1. 建项目目录
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 2. 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo ">>> 创建虚拟环境..."
    python3 -m venv venv
fi

# 3. 激活虚拟环境并安装依赖
echo ">>> 安装依赖..."
source $VENV_DIR/bin/activate
pip install --upgrade pip -q
pip install \
    fastapi==0.115.0 \
    "uvicorn[standard]==0.30.6" \
    sqlalchemy==2.0.35 \
    alembic==1.13.3 \
    aiomysql==0.2.0 \
    pymysql==1.1.1 \
    redis==5.1.1 \
    httpx==0.27.2 \
    apscheduler==3.10.4 \
    python-dotenv==1.0.1 \
    pydantic==2.9.2 \
    "pydantic-settings==2.5.2" \
    "openai==1.51.2" \
    loguru==0.7.2 \
    "python-jose[cryptography]==3.3.0" \
    "passlib[bcrypt]==1.7.4" \
    -q

echo ">>> 依赖安装完成"

# 4. 创建 systemd 服务
cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=TikTok Ads Intelligence System
After=network.target mysql.service

[Service]
Type=simple
User=root
WorkingDirectory=${PROJECT_DIR}
Environment=PATH=${VENV_DIR}/bin
ExecStart=${VENV_DIR}/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001 --workers 1
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 5. 配置 Nginx
cat > /www/server/panel/vhost/nginx/ads.tongtools.com.conf << 'NGINX_EOF'
server {
    listen 80;
    server_name ads.tongtools.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }

    # OAuth 回调
    location /auth/callback {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX_EOF

echo ">>> Nginx 配置已写入"

# 6. 启动服务
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl restart ${SERVICE_NAME}

# 7. 重载 Nginx
nginx -t && nginx -s reload

echo ""
echo "=== 部署完成 ==="
echo "服务状态: $(systemctl is-active ${SERVICE_NAME})"
echo "API 文档: http://ads.tongtools.com/docs"
echo ""
echo "查看日志: journalctl -u ${SERVICE_NAME} -f"
