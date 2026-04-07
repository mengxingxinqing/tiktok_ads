# TikTok Ads System - 宝塔部署指南

> 服务器: 123.60.90.100  
> 域名: https://ads.tongtools.com  
> 宝塔面板: https://123.60.90.100:17449/591c895f

---

## 一、宝塔面板操作（手动，约 10 分钟）

### 1. 创建网站

1. 打开宝塔面板 → **网站** → **添加站点**
2. 填写：
   - 域名: `ads.tongtools.com`
   - 根目录: `/www/wwwroot/tiktok-ads/frontend`
   - PHP版本: **纯静态**
   - 数据库: **MySQL** → 数据库名 `tk_ads` → 用户名 `tk_ads` → 密码 `FcsyN4Da7pdwXaZa`
3. 点击提交

### 2. 申请 SSL 证书

1. 网站列表 → 点击 `ads.tongtools.com` → **SSL**
2. 选择 **Let's Encrypt** → 勾选域名 → 申请
3. 开启 **强制 HTTPS**

### 3. 安装 Python 项目管理器（如果没有）

1. **软件商店** → 搜索 **Python项目管理器** → 安装
2. 安装完成后，进入 Python 项目管理器
3. **版本管理** → 安装 **Python 3.11**（编译约 5-10 分钟）

### 4. 创建 Python 项目

1. Python 项目管理器 → **添加项目**
2. 填写：
   - 项目名称: `tiktok-ads`
   - 项目路径: `/www/wwwroot/tiktok-ads/backend`
   - Python版本: `3.11`
   - 框架: `python`
   - 启动方式: **命令行启动**
   - 启动命令: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8890 --workers 2`
   - 是否开机启动: ✅
3. 点击确定

### 5. 配置 Nginx 反向代理

1. 网站列表 → 点击 `ads.tongtools.com` → **配置文件**
2. 替换为以下配置（保留 SSL 证书路径不变）：

---

## 二、自动化部署（脚本完成）

完成上面的宝塔面板手动配置后，后续所有代码更新都通过脚本完成：

```bash
# 首次部署（上传代码 + 安装依赖 + 配置 Nginx + 启动）
python deploy/deploy.py init

# 日常更新（上传代码 + 重启）
python deploy/deploy.py

# 仅更新后端
python deploy/deploy.py backend

# 仅更新前端
python deploy/deploy.py frontend

# 查看日志
python deploy/deploy.py logs

# 重启服务
python deploy/deploy.py restart
```

---

## 三、Nginx 完整配置

在宝塔的站点配置文件中使用：

```nginx
server {
    listen 80;
    server_name ads.tongtools.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ads.tongtools.com;

    # SSL（宝塔自动管理，路径不要改）
    ssl_certificate    /www/server/panel/vhost/cert/ads.tongtools.com/fullchain.pem;
    ssl_certificate_key  /www/server/panel/vhost/cert/ads.tongtools.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # 前端静态文件
    root /www/wwwroot/tiktok-ads/frontend;
    index index.html;

    # 后端 API 路由 → 转发到 uvicorn
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

    # SPA fallback（前端路由）
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    access_log /www/wwwlogs/ads.tongtools.com.log;
    error_log /www/wwwlogs/ads.tongtools.com.error.log;
}
```

---

## 四、目录结构

```
/www/wwwroot/tiktok-ads/
├── backend/           # 后端代码
│   ├── app/           # FastAPI 应用
│   ├── requirements.txt
│   ├── .env           # 生产环境配置
│   └── venv/          # Python 虚拟环境（宝塔 Python 管理器创建）
├── frontend/          # 前端构建产物（npm run build 的输出）
│   ├── index.html
│   └── assets/
└── logs/              # 日志
    └── backend.log
```

---

## 五、环境变量 (.env)

部署到服务器上的 `/www/wwwroot/tiktok-ads/backend/.env`：

```env
TIKTOK_APP_ID=7591801546375954449
TIKTOK_APP_SECRET=d4e8663d1401b5e42f907d7e9095481b3843f285
TIKTOK_REDIRECT_URI=https://ads.tongtools.com/auth/callback

LLM_API_BASE=https://api.tongtools.com
LLM_API_KEY=sk-apTZr7qZ8K1vAjTlMmAVSh5Hx8Nx0OqOvIPszsud50bhjkcv
LLM_MODEL=gpt-5

DATABASE_URL=mysql+aiomysql://tk_ads:FcsyN4Da7pdwXaZa@localhost:3306/tk_ads?charset=utf8mb4
REDIS_URL=redis://localhost:6379/0

SECRET_KEY=tiktok-ads-prod-x7k9m2p4q8r1s5t3
DEBUG=false
LOG_LEVEL=INFO
SYNC_INTERVAL_MINUTES=30
```

---

## 六、常见问题

### Q: 后端启动失败？
```bash
# 查看日志
tail -50 /www/wwwroot/tiktok-ads/logs/backend.log
# 或宝塔 Python 项目管理器查看日志
```

### Q: 前端页面空白？
- 检查 Nginx 配置中 `root` 路径是否正确
- 检查 `frontend/index.html` 是否存在
- Nginx reload: `nginx -s reload`

### Q: API 返回 502？
- 后端未启动，检查 Python 项目管理器
- 端口不对，确认后端监听 8890

### Q: 数据库连接失败？
- 检查 `.env` 中 `DATABASE_URL` 的用户名密码
- 检查 MySQL 是否运行: `systemctl status mysql`
