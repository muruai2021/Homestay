# 猩伙伴民宿 AI 智能体矩阵

## 项目概述

**猩伙伴民宿 AI 智能体矩阵**是一站式民宿智能运营平台，基于通义千问大模型构建，提供内容创作、情报洞察、运营管理、客户服务等全方位 AI 能力。

- **项目类型**：FastAPI 后端 + 静态前端（SaaS 平台）
- **核心用户**：民宿运营者、内容营销人员
- **部署端口**：9002

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Python 3.10+ / FastAPI | ASGI 服务，RESTful API |
| **AI 引擎** | 阿里云百炼（通义千问 qwen-plus） | 默认 AI 提供者 |
| **联网搜索** | 必应搜索集成 | 情报洞察功能 |
| **前端** | 原生 HTML/CSS/JS | 极简现代风格，响应式 |
| **配置** | .env 文件 | API 密钥等敏感配置 |

---

## 项目结构

```
Homestay/                          # 项目根目录
├── main.py                        # FastAPI 主入口 (uvicorn)
├── requirements.txt               # Python 依赖
├── .env                          # 环境配置（API密钥）
├── README.md                      # 项目文档
│
├── backend/                      # 后端服务
│   ├── api/                      # API 路由
│   │   ├── agent.py              # 智能体对话 (/api/agent/*)
│   │   ├── generation.py         # 内容生成 (/api/xhs-copy, /api/short-video, etc.)
│   │   ├── dashboard.py          # 运营数据 (/api/dashboard)
│   │   ├── file.py               # 文件操作 (/api/file/*)
│   │   └── settings.py           # 系统设置 (/api/settings)
│   ├── config/                   # 配置管理
│   │   ├── settings.py           # 主配置（路径、AI_PROVIDER 等）
│   │   └── api_config.py         # API 配置
│   ├── core/                     # 核心组件
│   │   ├── agent_loader.py       # 智能体上下文加载
│   │   ├── session_manager.py    # 会话管理
│   │   ├── prompt_builder.py     # 提示词构建
│   │   ├── skill_base.py         # 技能加载与执行
│   │   └── file_manager.py       # 文件管理
│   ├── models/                   # 数据模型
│   │   └── schemas.py            # Pydantic Schemas
│   └── services/                 # 外部服务
│       ├── ai_client.py          # AI 客户端（通义千问/DeepSeek）
│       ├── search_service.py     # 搜索服务
│       └── token_tracker.py      # Token 用量追踪
│
├── web/                          # AI 员工矩阵前端
├── xhb-gw/                       # 官网静态文件
├── dashboard/                    # 运营数据看板
├── ai-admin/                     # AI 管理后台
│
├── workspace/                    # 智能体工作区（按 agent_id 划分）
│   ├── chat/                     # 运营助手工作区
│   ├── xhs/                      # 小红书文案工作区
│   ├── poster/                   # 海报生成工作区
│   ├── wechat/                   # 公众号文章工作区
│   ├── shortvideo/               # 短视频文案工作区
│   ├── intelligence/             # 情报洞察工作区
│   └── knowledge/                # 知识库问答工作区
│
├── skills/                       # AI 技能模块（Skill 框架）
│   ├── _templates/               # Skill 创建模板
│   ├── content/                 # 内容创作类技能
│   │   └── xhs_writer/          # 小红书文案技能
│   └── analysis/                # 分析类技能
│       └── data_analyzer/        # 数据分析技能
│
└── knowledge_base/              # AI 知识库
    └── 我是谁.md                 # "我是谁"提示词
```

---

## 核心概念

### 智能体（Agent）

项目采用**智能体架构**，每个 AI 功能模块（小红书、公众号、客服等）都是独立的 Agent：

| Agent ID | 功能 | 工作区目录 |
|----------|------|-----------|
| `chat` | 运营助手 | `workspace/chat/` |
| `xhs` | 小红书文案 | `workspace/xhs/` |
| `poster` | 海报生成 | `workspace/poster/` |
| `wechat` | 公众号文章 | `workspace/wechat/` |
| `shortvideo` | 短视频文案 | `workspace/shortvideo/` |
| `intelligence` | 情报洞察（联网） | `workspace/intelligence/` |
| `customer` | 官网客服 | `workspace/customer/` |

### 上下文加载机制

`AgentLoader` 组合完整上下文：
```
系统提示词 + Skills提示词 + 会话记录 + 用户输入
```

工作区目录结构（每个 Agent）：
- `agent.md` - Agent 定义和提示词
- `memory/` - 会话历史存储
- `skills/` - Agent 专属 Skills

### Skill 框架

`skills/` 目录下是可复用的技能模块，基于 `skill_base.py` 加载：

```python
# 使用方式
loader = SkillLoader(agent_id="xhs")
matched = loader.match_skills("帮我写一篇小红书种草文案")
chain = SkillChain(agent_id="xhs")
chain.add_skill("xhs_writer")
```

---

## 编码规范

### Python

| 类型 | 规范 | 示例 |
|------|------|------|
| 函数 | snake_case | `get_agent_id()`, `load_sessions()` |
| 类 | PascalCase | `AgentLoader`, `SessionManager` |
| 常量 | UPPER_SNAKE | `AI_PROVIDER`, `MAX_RETRY_COUNT` |
| 私有变量 | `_single_leading` | `_deepseek_api_key` |

### API 设计

- **版本前缀**：`/api/v1/`（如 `/api/agent/chat`）
- **路由注册**：`app.include_router(agent.router, prefix="/api/agent")`
- **错误处理**：统一 HTTPException，状态码 4xx/5xx

### 安全

- **输入隔离**：`agent.py` 中的 `GREETING_PATTERNS` 和 `INJECTION_PATTERNS`
- **Prompt 注入检测**：正则匹配常见注入模式
- **敏感配置**：通过 `.env` 管理，不进 Git

---

## 启动与部署

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 .env
echo "DASHSCOPE_API_KEY=your_key" > .env
echo "AI_PROVIDER=qwen" >> .env

# 启动开发服务器
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 9002
```

**访问**：
- 官网首页：`http://localhost:9002/`
- AI 矩阵：`http://localhost:9002/ai`
- API 文档：`http://localhost:9002/docs`

---

## 测试

```bash
# 运行测试
pytest

# 指定目录
pytest tests/

# 查看覆盖率
pytest --cov=. --cov-report=html
```

---

## 关键文件

| 文件 | 用途 |
|------|------|
| `backend/core/agent_loader.py` | 智能体上下文加载核心逻辑 |
| `backend/api/agent.py` | 智能体对话 API + 输入安全检测 |
| `backend/core/skill_base.py` | Skill 框架实现 |
| `backend/services/ai_client.py` | 多 AI 提供者客户端 |
| `backend/config/settings.py` | 配置加载（从 .env） |

---

## 设计决策

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-04 | 选用通义千问作为默认 AI | 阿里云百炼平台集成，中文能力强 |
| 2026-04 | 采用 Agent + Skills 架构 | 模块化，复用性强，支持动态加载 |
| 2026-04 | 输入隔离层 | 防范 Prompt 注入攻击 |

---

## 注意事项

1. **API 密钥**：所有 AI 提供者密钥存储在 `.env`，不提交到 Git
2. **会话存储**：工作区 `memory/` 目录下存储会话历史
3. **CORS**：生产环境需在 `ALLOWED_ORIGINS` 中指定具体域名
4. **静态文件**：前端为纯静态 HTML，无构建步骤