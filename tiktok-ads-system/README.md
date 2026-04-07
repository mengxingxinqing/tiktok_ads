# TikTok 广告投放检测和智能决策系统

## 项目结构

```
tiktok-ads-system/
├── app/
│   ├── api/
│   │   └── auth.py          # OAuth 授权接口
│   ├── core/
│   │   ├── config.py        # 配置（读取 .env）
│   │   └── database.py      # 数据库连接
│   ├── models/
│   │   ├── advertiser.py    # 广告账户 + Token 管理
│   │   ├── metrics.py       # 指标快照（历史数据）
│   │   ├── decision.py      # LLM 决策记录
│   │   └── alert.py         # 告警记录
│   ├── services/
│   │   └── tiktok_client.py # TikTok API 客户端（限速+重试）
│   ├── tasks/
│   │   └── sync_task.py     # 30分钟定时同步任务
│   └── main.py              # FastAPI 入口
├── requirements.txt
├── .env.example
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
copy .env.example .env
# 编辑 .env，填入数据库连接等配置
```

### 3. 启动 PostgreSQL 和 Redis

```bash
# 方式一：Docker
docker run -d --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:16
docker run -d --name redis -p 6379:6379 redis:7

# 方式二：本地安装
```

### 4. 启动服务

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 5. 访问 API 文档

http://localhost:8000/docs

## OAuth 授权流程

1. 访问 `GET /auth/login` 获取授权 URL
2. 将 URL 发给广告主，让他们点击授权
3. TikTok 回调到 `https://ads.tongtools.com/auth/callback`
4. 系统自动完成 token 换取和存储

## 迭代计划

- [x] P0: 项目骨架 + 数据库模型 + OAuth 授权
- [ ] P1: 数据采集调度（30分钟同步）
- [ ] P2: 异常检测引擎
- [ ] P3: LLM 智能决策
- [ ] P4: Vue.js Dashboard
