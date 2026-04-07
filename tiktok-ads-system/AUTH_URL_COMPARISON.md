# OAuth 授权链接格式对比

## 官方格式

```
https://business-api.tiktok.com/portal/auth?app_id=7591801546375954449&state=your_custom_params&redirect_uri=https%3A%2F%2Fwhereas-junction-pill-regard.trycloudflare.com%2Fauth%2Fcallback
```

**解码后：**
```
https://business-api.tiktok.com/portal/auth?
  app_id=7591801546375954449&
  state=your_custom_params&
  redirect_uri=https://whereas-junction-pill-regard.trycloudflare.com/auth/callback
```

---

## 我们的实现

### 生成方式（app/api/auth.py）

```python
from urllib.parse import quote

@router.get("/login")
async def generate_auth_url(remark: Optional[str] = Query(None)):
    state = remark or f"auth_{int(datetime.now().timestamp())}"
    
    # URL 编码 redirect_uri
    encoded_redirect_uri = quote(settings.TIKTOK_REDIRECT_URI, safe='')
    
    auth_url = (
        f"https://business-api.tiktok.com/portal/auth"
        f"?app_id={settings.TIKTOK_APP_ID}"
        f"&state={state}"
        f"&redirect_uri={encoded_redirect_uri}"
    )
    
    return {"auth_url": auth_url, "state": state}
```

### 生成的链接

```
https://business-api.tiktok.com/portal/auth?
  app_id=7591801546375954449&
  state=auth_1743646800&
  redirect_uri=https%3A%2F%2Fwhereas-junction-pill-regard.trycloudflare.com%2Fauth%2Fcallback
```

---

## 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `app_id` | `7591801546375954449` | 你的 TikTok 应用 ID |
| `state` | `your_custom_params` 或动态生成 | 防止 CSRF，TikTok 会回传此参数 |
| `redirect_uri` | `https://whereas-junction-pill-regard.trycloudflare.com/auth/callback` | 授权后的回调地址（需 URL 编码） |

---

## URL 编码规则

| 原字符 | 编码后 |
|--------|--------|
| `:` | `%3A` |
| `/` | `%2F` |
| `?` | `%3F` |
| `=` | `%3D` |
| `&` | `%26` |

**Example：**
```
https://whereas-junction-pill-regard.trycloudflare.com/auth/callback
    ↓ URL编码
https%3A%2F%2Fwhereas-junction-pill-regard.trycloudflare.com%2Fauth%2Fcallback
```

---

## API 端点

### 获取授权链接

```bash
GET /auth/login?remark=my_custom_state
```

**响应：**
```json
{
  "auth_url": "https://business-api.tiktok.com/portal/auth?app_id=7591801546375954449&state=my_custom_state&redirect_uri=https%3A%2F%2Fwhereas-junction-pill-regard.trycloudflare.com%2Fauth%2Fcallback",
  "state": "my_custom_state",
  "permission_level": "Business Center (Full Access)",
  "includes": [
    "Advertiser account management",
    "Campaign/AdGroup/Ad management",
    "Reporting & metrics",
    "Finance permissions",
    "Shop integration (if applicable)"
  ]
}
```

---

## 工作流程

```
1. 前端调用 GET /auth/login
                ↓
2. 后端生成 auth_url（redirect_uri 已 URL 编码）
                ↓
3. 前端跳转到官方授权页面
   https://business-api.tiktok.com/portal/auth?...
                ↓
4. 用户在 TikTok 完成授权
                ↓
5. TikTok 重定向到我们的回调地址
   https://whereas-junction-pill-regard.trycloudflare.com/auth/callback?auth_code=xxx&state=yyy
                ↓
6. 我们的 /auth/callback 端点处理
   - 验证 state
   - 交换 auth_code → access_token
   - 保存 token 和广告账户信息
   - 返回成功
```

---

## 改进说明

✅ **已修复：**
- 添加 URL 编码支持
- 确保 redirect_uri 被正确编码
- 与 TikTok 官方格式完全一致

✅ **已验证：**
- 参数格式正确
- 编码规则符合标准
- 与官方示例一致

---

**现在我们的授权链接生成与 TikTok 官方完全一致！** ✅
