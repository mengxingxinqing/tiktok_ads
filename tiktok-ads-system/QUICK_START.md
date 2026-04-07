# 🚀 快速启动方案

由于网络限制无法安装 ngrok，我提供几个替代方案：

---

## 方案1：手动下载 ngrok（推荐）

### 步骤1：下载 ngrok
访问这些镜像之一：
- [ngrok 官网](https://ngrok.com/download) （可能被限制）
- [国内镜像源](https://www.npmjs.com/package/ngrok) 
- 或者找朋友帮你下载

### 步骤2：解压到项目目录
```
E:\code\tiktok-ads-system\ngrok\ngrok.exe
```

### 步骤3：配置 token
```bash
E:\code\tiktok-ads-system\ngrok\ngrok.exe config add-authtoken YOUR_TOKEN
```

### 步骤4：启动穿透
```bash
E:\code\tiktok-ads-system\ngrok\ngrok.exe http 8000
```

---

## 方案2：使用其他内网穿透工具

由于 ngrok 被限制，可以用这些替代品：

### A. **frp** (FastReverse Proxy)
- 开源免费
- 性能更好
- 支持 TCP/UDP/HTTP
- [下载](https://github.com/fatedier/frp/releases)

### B. **Cloudflare Tunnel**
```bash
# 安装 cloudflared
# 然后运行：
cloudflared tunnel --url http://localhost:8000
# 得到: https://xxx.trycloudflare.com
```

### C. **内网穿透应用**
- 花生壳（中国用户常用）
- NATAPP
- sunny-ngrok（国内镜像）

---

## 方案3：先不穿透，用 localhost 测试

如果暂时无法穿透，可以：

### 第一阶段：本地开发
```env
TIKTOK_REDIRECT_URI=http://localhost:8000/auth/callback
```

这样可以：
- ✅ 开发和测试所有功能（除了 OAuth）
- ✅ 创建广告的流程
- ✅ 数据监控和优化

### 第二阶段：部署到服务器后再用穿透
```env
TIKTOK_REDIRECT_URI=https://yourdomain.com/auth/callback
```

---

## 方案4：我为你准备的简化方案

如果以上都不方便，告诉我：

**你的 ngrok token 是什么？**

我可以：
1. 将 token 写入配置
2. 生成一个简化的启动脚本
3. 你自己去下载 ngrok 后，一键启动

---

## 目前推荐做法

### 推荐方案：先用本地 localhost 开发

```bash
# 1. 后端正常启动
cd E:\code\tiktok-ads-system
uvicorn app.main:app --reload

# 2. 前端正常启动
cd E:\code\tiktok-ads-frontend
npm run dev

# 3. 访问
http://localhost:5173

# 4. 可以创建广告、查看数据等所有功能
# 除了 OAuth 授权流程（因为 TikTok 需要公网 URL）
```

### 当你能下载 ngrok 后

```bash
# 运行启动脚本
.\setup_ngrok.ps1 -token YOUR_TOKEN

# 就可以完整测试 OAuth 了
```

---

## 你需要做的选择

### 选择1：继续等、找办法装 ngrok
- 优点：完整的 OAuth 流程测试
- 缺点：需要额外步骤

### 选择2：先用 localhost 开发，后续再穿透
- 优点：立即开始开发
- 缺点：暂时无法测试 OAuth

### 选择3：用其他穿透工具（frp/Cloudflare等）
- 优点：可能更容易安装
- 缺点：需要重新配置脚本

---

## 我的建议

**现在：直接启动系统！** 🚀

```bash
# 后端
cd E:\code\tiktok-ads-system
uvicorn app.main:app --reload

# 前端（新终端）
cd E:\code\tiktok-ads-frontend
npm run dev

# 访问 http://localhost:5173
```

**之后：当能装上 ngrok 时**

```bash
# 运行我为你准备的脚本
.\setup_ngrok.ps1 -token YOUR_TOKEN

# 完整功能就都能用了
```

---

## 我已经为你准备好的

✅ `setup_ngrok.ps1` — 一键启动脚本（等你装好 ngrok 后用）
✅ `ngrok.yml` — 配置文件
✅ `.env` — 动态配置支持
✅ `NGROK_SETUP.md` — 完整文档
✅ 所有后端 API — 已准备好
✅ 前端 UI — 已准备好

---

**你现在就可以用 localhost 开始开发了！**

不需要等穿透，所有广告创建、监控、优化的功能都能用。

准备好了吗？👇
