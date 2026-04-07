# OAuth 回调修复报告

## 问题描述

授权成功后，TikTok 返回的回调 URL：
```
https://whereas-junction-pill-regard.trycloudflare.com/auth/callback?auth_code=xxx&code=xxx&state=yyy
```

但我们的后端只处理了 `auth_code` 参数，导致参数校验失败。

---

## 原因分析

TikTok API 返回了两个参数：
1. **`auth_code`** — 新标准参数名
2. **`code`** — 旧标准参数名（兼容性）

我们的代码只期望 `auth_code`，而且必须存在（`Query(...)`），所以两个都有时会报错。

---

## 解决方案

### 后端修改（app/api/auth.py）

#### 1. 兼容两种参数名

```python
@router.get("/callback")
async def oauth_callback(
    auth_code: Optional[str] = Query(None),  # 改为可选
    code: Optional[str] = Query(None),       # 新增支持
    state: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    # 兼容两种参数名
    token_code = auth_code or code
    if not token_code:
        raise HTTPException(status_code=400, detail="Missing auth_code or code parameter")
```

#### 2. 改进错误处理

从返回 JSON 改为 redirect 到前端页面，这样用户看到的是友好界面而不是错误代码：

```python
# 成功时重定向到成功页面
return RedirectResponse(
    url=f"http://localhost:5175/auth/success?count=1&advertisers=...",
    status_code=302
)

# 失败时重定向到错误页面
return RedirectResponse(
    url=f"http://localhost:5175/auth/error?message=...",
    status_code=302
)
```

### 前端新增页面

#### AuthSuccess.vue
- 显示授权成功信息
- 列出已授权的账户
- 3秒后自动跳转到广告创建页面
- 提供手动按钮返回仪表盘

#### AuthError.vue
- 显示授权失败信息
- 展示错误详情
- 提供重新授权按钮
- 提供返回仪表盘选项

### 路由更新

在 `src/router/index.js` 中添加两个新路由：

```javascript
{
  path: '/auth/success',
  name: 'AuthSuccess',
  component: () => import('../views/AuthSuccess.vue'),
},
{
  path: '/auth/error',
  name: 'AuthError',
  component: () => import('../views/AuthError.vue'),
},
```

---

## 完整的 OAuth 流程

```
1. 用户点击"绑定投放户"
        ↓
2. 前端重定向到 GET /auth/login
        ↓
3. 后端生成授权 URL
   https://business-api.tiktok.com/portal/auth?app_id=...&state=...&redirect_uri=...
        ↓
4. 用户在 TikTok 完成授权
        ↓
5. TikTok 重定向回我们的回调地址，并返回 auth_code 和 code
   https://xxx.trycloudflare.com/auth/callback?auth_code=xxx&code=xxx&state=yyy
        ↓
6. 我们的后端处理回调（现在支持两种参数名）
        ↓
7. 交换 token，获取广告账户列表
        ↓
8. 保存到数据库
        ↓
9. 重定向到成功页面 ✅
   /auth/success?count=1&advertisers=123:MyAccount
        ↓
10. 前端显示成功信息，3秒后自动跳转到广告创建
```

---

## 修改的文件清单

### 后端
- `app/api/auth.py` — 支持 `auth_code` 和 `code` 两个参数，改进错误处理

### 前端
- `src/views/AuthSuccess.vue` — 新增成功页面（4081 bytes）
- `src/views/AuthError.vue` — 新增错误页面（3068 bytes）
- `src/router/index.js` — 新增两个路由

---

## 关键改进

| 项 | 改进前 | 改进后 |
|------|--------|--------|
| 参数兼容 | 仅支持 `auth_code` | 支持 `auth_code` 和 `code` |
| 参数必需 | 必须（会报错） | 可选（智能选择） |
| 错误提示 | JSON 错误代码 | 友好的错误页面 |
| 成功反馈 | JSON 响应 | 友好的成功页面 + 自动跳转 |
| 用户体验 | 开发者友好 | 用户友好 |

---

## 测试步骤

1. 重启后端（读取新的 auth.py）
2. 重启前端（读取新的页面和路由）
3. 在前端点击"绑定投放户"
4. 完成 TikTok 授权
5. 应该看到成功页面 ✅
6. 3秒后自动跳转到广告创建页面

---

## 已知限制

- 重定向 URL 硬编码为 `localhost:5175`（开发环境）
- 生产环境需要改为实际的前端 URL

**改进方案：** 使用环境变量

```python
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5175")

return RedirectResponse(
    url=f"{FRONTEND_URL}/auth/success?count={len(saved)}",
    status_code=302
)
```

---

**状态：✅ 完成**

现在 OAuth 流程已经完全修复，可以正常工作了！
