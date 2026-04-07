# ngrok 内网穿透设置指南

## 📋 概述

本指南帮你快速设置 ngrok，将本地的 TikTok Ads 系统暴露到公网，以便进行 TikTok OAuth 授权流程的测试。

---

## 🚀 快速开始

### 步骤1：获取 ngrok 账户和 Token

1. 访问 [ngrok 官网](https://ngrok.com)
2. 点击 "Sign Up" 注册免费账户
3. 登录后，在 [Dashboard](https://dashboard.ngrok.com/auth/your-authtoken) 复制你的 Auth Token

### 步骤2：下载和安装 ngrok

#### Windows（推荐使用 PowerShell）

```powershell
# 方法1：如果已有 Chocolatey
choco install ngrok

# 方法2：如果已有 Scoop
scoop install ngrok

# 方法3：手动下载
# https://ngrok.com/download
# 下载 Windows 版本，解压到某个目录（如 C:\ngrok\）
```

#### macOS

```bash
brew install ngrok
```

#### Linux

```bash
# 访问 https://ngrok.com/download 下载对应版本
unzip ngrok-v3-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
```

### 步骤3：使用本项目的快速启动脚本

在项目目录运行：

```powershell
# Windows PowerShell
.\setup_ngrok.ps1 -token YOUR_NGROK_TOKEN

# 如果已经配置过 token，可以直接运行
.\setup_ngrok.ps1
```

**脚本会自动：**
1. ✅ 检查 ngrok 安装
2. ✅ 配置 ngrok token
3. ✅ 启动 ngrok 隧道
4. ✅ 获取公网 URL
5. ✅ 更新 `.env` 中的 `TIKTOK_REDIRECT_URI`

### 步骤4：重启后端应用

```bash
# 杀死旧的 Python 进程
# 然后重启：
uvicorn app.main:app --reload
```

### 步骤5：测试授权流程

1. 访问前端：http://localhost:5173
2. 点击"绑定投放户"
3. 会被重定向到 TikTok OAuth，使用 ngrok 的公网 URL
4. 授权成功！

---

## 📊 配置说明

### .env 配置三种模式

#### 模式1：本地开发（不需要穿透）

```env
TIKTOK_REDIRECT_URI=http://localhost:8000/auth/callback
```

**使用场景：**
- 仅在本地测试
- 不需要公网访问

#### 模式2：ngrok 穿透（开发+测试）

```env
TIKTOK_REDIRECT_URI=https://abc123.ngrok.io/auth/callback
```

**使用场景：**
- 本地开发，需要测试 OAuth 流程
- 需要公网测试，但不上生产
- 使用 `setup_ngrok.ps1` 会自动更新这个

**注意：**
- ngrok 免费版的 URL 每次重启都会变化
- 需要重新运行脚本更新配置
- 如果想固定 URL，可升级为付费版

#### 模式3：生产环境（自有域名）

```env
TIKTOK_REDIRECT_URI=https://ads.yourdomain.com/auth/callback
```

**使用场景：**
- 已部署到生产服务器
- 有自己的域名

---

## 🔧 常见问题

### Q1: ngrok 免费版可以用吗？
A: 可以，但有限制：
- ✅ 可以穿透 HTTP/HTTPS
- ✅ 可以穿透 TCP
- ❌ 每次重启 URL 会变化
- ❌ 请求数有限制（大约 40 req/min）
- ❌ 无法固定自定义域名

**对我们的影响：**
- 每次 ngrok 重启，需要重新运行 `setup_ngrok.ps1`
- 更新 .env 中的 TIKTOK_REDIRECT_URI
- 在 TikTok 应用设置中也要更新 Redirect URI

### Q2: 如何固定 ngrok URL？
A: 升级为付费版，使用自定义子域名：

```powershell
ngrok http 8000 --subdomain=my-tiktok-ads
# 得到: https://my-tiktok-ads.ngrok.io
```

然后在 .env 中设置：
```env
TIKTOK_REDIRECT_URI=https://my-tiktok-ads.ngrok.io/auth/callback
```

### Q3: ngrok 运行时提示 "auth failed"？
A: Token 不对或未配置，运行：

```bash
ngrok config add-authtoken YOUR_TOKEN
```

### Q4: 前端也需要穿透吗？
A: 不必要，但可以。

**推荐：**
- 前端仍然用 localhost:5173
- 后端用 ngrok 穿透（localhost:8000）
- 在 `.env` 中设置 `VITE_API_BASE=https://xxxxx.ngrok.io`

或者编辑 `ngrok.yml`，取消注释前端的穿透配置。

### Q5: 如何知道 ngrok 的公网 URL？

**方式1：查看脚本输出**
```
✅ 公网 URL: https://abc123.ngrok.io
```

**方式2：访问 ngrok 网页控制台**
```
http://localhost:4040
```

**方式3：命令行查询**
```bash
curl http://localhost:4040/api/tunnels
```

### Q6: 如何停止 ngrok？
A: 
- 关闭运行脚本的 PowerShell 窗口
- 或在命令行按 `Ctrl+C`

### Q7: ngrok 在 TikTok 应用配置中怎么设置？
A:

1. 登录 [TikTok 开发者平台](https://developers.tiktok.com)
2. 找到你的应用
3. 在 "Redirect URI" 字段中更新为：
   ```
   https://abc123.ngrok.io/auth/callback
   ```
4. 保存配置

---

## 🎯 完整流程示例

### 场景：本地开发 + OAuth 测试

```bash
# 1. 启动 ngrok
cd E:\code\tiktok-ads-system
.\setup_ngrok.ps1 -token YOUR_NGROK_TOKEN

# 输出：
# ✅ 公网 URL: https://abc123.ngrok.io

# 2. 更新 TikTok 应用配置
# 在 TikTok Developer Platform 中设置：
# Redirect URI = https://abc123.ngrok.io/auth/callback

# 3. 重启后端（会自动读取新的 .env）
# 在另一个终端：
cd E:\code\tiktok-ads-system
uvicorn app.main:app --reload

# 4. 启动前端
cd E:\code\tiktok-ads-frontend
npm run dev

# 5. 测试
# 访问 http://localhost:5173
# 点击"绑定投放户"
# 会被重定向到 TikTok OAuth
# 完成授权！
```

---

## 📚 更多信息

- [ngrok 官方文档](https://ngrok.com/docs)
- [ngrok HTTP Inspector](http://localhost:4040) （启动 ngrok 后访问）

---

## ⚠️ 安全提示

1. **不要公开你的 ngrok URL** — 它会暴露你的本地应用
2. **不要在生产环境用 ngrok** — 性能和稳定性都不够
3. **定期更换 Token** — 如果不小心泄露
4. **使用 HTTPS** — ngrok 自动提供 SSL/TLS

---

**准备好了吗？运行 `.\setup_ngrok.ps1` 开始吧！** 🚀
