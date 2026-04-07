# Token 管理策略

## 当前 TikTok API 的 Token 特性

根据实际的 OAuth 响应，TikTok API 有以下特点：

```
access_token：有效期 24 小时
refresh_token：不提供
```

这与传统的 OAuth 2.0 略有不同。

---

## 原有的问题

我们最初假设会有 `refresh_token`，但 TikTok 没有提供。这导致：

```python
# ❌ 错误做法
access_token = token_data["access_token"]        # 获取成功
refresh_token = token_data["refresh_token"]      # KeyError!
```

---

## 解决方案

### 1. **Token 刷新策略**

由于没有 `refresh_token`，我们有以下选择：

#### 方案 A：重新授权（推荐）
- 当 token 将要过期时（提前 1 小时）
- 让商家重新授权
- 这样可以获得新的 access_token

**优点：**
- 简单直接
- 符合 TikTok 的 OAuth 流程
- 安全性高

**缺点：**
- 需要商家手动授权

#### 方案 B：后台自动刷新（需要特殊权限）
- 某些 API 可能支持使用 `app_secret` 直接刷新
- 但 TikTok Business API 文档中没有明确说明

---

### 2. **当前实现**

#### 数据库模型
```python
class Advertiser(Base, TimestampMixin):
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)  # 现在可选
    access_token_expire_at = Column(DateTime(timezone=True))
    refresh_token_expire_at = Column(DateTime(timezone=True), nullable=True)
```

#### OAuth 处理
```python
# ✅ 正确做法
token_data = await TikTokClient.exchange_token(auth_code)

access_token = token_data.get("access_token")          # 必需
refresh_token = token_data.get("refresh_token")        # 可选，可能为 None

if not access_token:
    raise HTTPException(status_code=400, detail="No access_token")

# 计算过期时间
access_expire = now + timedelta(hours=23, minutes=30)  # 保留30分钟缓冲
refresh_expire = now + timedelta(days=364) if refresh_token else None
```

---

### 3. **Token 有效期监控**

创建定期任务，检查即将过期的 tokens：

```python
# 每小时运行一次
async def check_token_expiry():
    # 查询即将过期的 advertisers（在24小时内）
    advertisers = await db.execute(
        select(Advertiser).where(
            Advertiser.access_token_expire_at <= now() + timedelta(hours=24),
            Advertiser.is_active == True
        )
    )
    
    for advertiser in advertisers:
        # 发送提醒
        await send_notification(
            user_id=advertiser.user_id,
            message=f"Your TikTok token expires in {hours_left} hours. Please re-authorize."
        )
```

---

### 4. **重新授权流程**

当 token 过期时：

```
1. 系统检测到 token 已过期
   ↓
2. 返回 401 或 403 错误
   ↓
3. 系统或客户端跳转到授权页面
   ↓
4. 商家重新授权
   ↓
5. 获取新的 access_token
   ↓
6. 更新数据库
   ↓
7. 继续使用
```

---

## 实施清单

- [x] 修改 Advertiser 模型，refresh_token 可选
- [x] 修改数据库表结构
- [x] 更新 OAuth 处理逻辑
- [x] 增强日志记录
- [ ] 实现 Token 过期检查任务
- [ ] 实现 Token 过期提醒通知
- [ ] 在 API 响应中返回 token 有效期信息
- [ ] 在前端显示 token 有效期倒计时

---

## 代码示例

### 检查 Token 是否过期

```python
from datetime import datetime, timezone, timedelta

def is_token_valid(advertiser: Advertiser) -> bool:
    """检查 token 是否仍然有效"""
    if not advertiser.access_token_expire_at:
        return True  # 没有过期信息，假设有效
    
    now = datetime.now(timezone.utc)
    # 提前 30 分钟标记为过期，给予充足刷新时间
    threshold = advertiser.access_token_expire_at - timedelta(minutes=30)
    
    return now < threshold

def hours_until_expiry(advertiser: Advertiser) -> float:
    """计算还有多少小时直到 token 过期"""
    if not advertiser.access_token_expire_at:
        return float('inf')  # 不知道
    
    now = datetime.now(timezone.utc)
    delta = advertiser.access_token_expire_at - now
    
    return delta.total_seconds() / 3600  # 转换为小时
```

### 在 API 端点中使用

```python
@router.get("/advertisers")
async def list_advertisers(db: AsyncSession = Depends(get_db)):
    """列出所有已授权的广告账户"""
    result = await db.execute(select(Advertiser).where(Advertiser.is_active == True))
    advertisers = result.scalars().all()

    return {
        "total": len(advertisers),
        "advertisers": [
            {
                "advertiser_id": a.advertiser_id,
                "name": a.advertiser_name,
                "is_token_valid": is_token_valid(a),
                "hours_until_expiry": hours_until_expiry(a),
                "access_token_expire_at": a.access_token_expire_at,
                # ... 其他字段
            }
            for a in advertisers
        ],
    }
```

---

## TikTok API 限制总结

| 特性 | 值 | 备注 |
|------|-----|------|
| access_token 有效期 | 24 小时 | 必需刷新 |
| refresh_token | 不提供 | 无法自动刷新 |
| 刷新方式 | 重新授权 | 需要用户参与 |
| 建议刷新间隔 | < 24 小时 | 提前 1 小时刷新 |
| 刷新通知 | 后台定时任务 | 检查并通知用户 |

---

## 最佳实践

1. **监控 Token 有效期**
   - 定期检查即将过期的 tokens
   - 至少每 6 小时检查一次

2. **提前通知用户**
   - Token 还有 24 小时时发送通知
   - Token 还有 1 小时时发送紧急通知

3. **优雅降级**
   - 当 API 返回 401/403 时，自动跳转到授权页面
   - 显示友好的错误信息

4. **错误恢复**
   - 缓存已知的有效 tokens
   - 失败自动重试一次
   - 提供手动授权选项

---

**关键结论：** 由于 TikTok 不提供 refresh_token，我们需要依赖定期重新授权。系统会在 token 即将过期时提醒用户。

