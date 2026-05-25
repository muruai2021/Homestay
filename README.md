# 猩伙伴民宿 AI 智能体矩阵
# XHB Homestay AI Agent Matrix

---

## 项目简介 | Project Overview

**猩伙伴民宿 AI 智能体矩阵** 是一站式民宿智能运营平台，基于通义千问大模型构建，提供内容创作、情报洞察、运营管理等全方位的 AI 能力支持。

XHB Homestay AI Agent Matrix is an all-in-one intelligent homestay operations platform built on Qwen LLM, providing comprehensive AI capabilities for content creation, market intelligence, and operations management.

---

## 核心功能 | Core Features

### 🏠 首页门户 | Homepage Portal
极简风格入口导航，快速访问所有功能模块，实时显示运营数据预览卡片。

Minimalist navigation with quick access to all modules, real-time operations data preview cards.

### 📕 小红书文案智能体 | Xiaohongshu Copywriting Agent
**输入 | Input**: 产品名称、使用场景
**输出 | Output**: 150-200字种草文案，带 Emoji 表情、话题标签

Product/scene input → 150-200 word viral posts with emojis & hashtags

### 📝 公众号文章智能体 | WeChat Article Agent
**输入 | Input**: 文章关键词、分类（产品/知识/感悟/故事/品宣）、目标客户群画像
**输出 | Output**: 1500-2000字专业公众号文章，含标题优化、正文结构化、金句埋点

Keyword + category → 1500-2000 word articles with optimized titles, structured body, key quotes

### 🎬 短视频文案智能体 | Short Video Script Agent
**输入 | Input**: 视频主题、风格偏好
**输出 | Output**: 30-60秒口播脚本，含分镜建议、BGM推荐、关键台词、3秒开场设计

Topic + style → 30-60s video scripts with storyboards, background music, key dialogues, 3s opening

### 🔍 民宿情报洞察智能体 | Market Intelligence Agent
**输入 | Input**: 行业关键词（如"民宿营销策略"）
**输出 | Output**: 基于通义千问联网搜索的深度洞察报告

Industry keywords → In-depth insights report via Qwen web search

### 🖼️ 民宿海报生成智能体 | Poster Generation Agent
**输入 | Input**: 文案内容、图片尺寸（3:4/16:9/1:1/4:3）
**输出 | Output**: AI 生成的海报图片描述词，一键生成民宿宣传海报

Copy + dimensions → AI-generated poster prompts for one-click homestay promotion posters

### 🤖 猩伙伴 AI 运营助手 | AI Operations Assistant
7×24小时智能客服，基于知识库回答，Markdown 格式化输出。

24/7 AI customer service based on knowledge base with Markdown formatting.

### 📊 运营管理驾驶舱 | Operations Dashboard
今日/本月订单统计、营收数据看板、入住率分析、客户评分追踪、订单来源分布（携程/美团/飞猪/直订）。

Order stats, revenue dashboard, occupancy analysis, customer ratings tracking, booking source distribution.

---

## 技术架构 | Tech Stack

### 后端 | Backend
- **框架 | Framework**: Python 3.10+ / FastAPI
- **AI 引擎 | AI Engine**: 通义千问 qwen-plus (阿里云百炼 | Alibaba Cloud Bailian)
- **联网搜索 | Web Search**: 必应搜索集成 | Bing Search integration
- **图像生成 | Image Gen**: 通义万相 API (wan2.6-t2i)
- **部署端口 | Port**: 9002

### 前端 | Frontend
- **技术 | Tech**: 原生 HTML/CSS/JavaScript | Vanilla HTML/CSS/JavaScript
- **Markdown**: marked.js
- **样式 | Styling**: 自定义极简现代风格 CSS | Custom minimalist CSS
- **响应式 | Responsive**: 桌面 + 移动端适配 | Desktop & Mobile

---

## 项目结构 | Project Structure

```
Homestay/
├── main.py                    # FastAPI 主入口 | Main entry point
├── requirements.txt           # Python 依赖 | Dependencies
├── .env                       # 环境配置 (API密钥) | Config (API keys)
│
├── backend/                   # 后端服务 | Backend
│   ├── api/                   # API 路由 | API routes
│   │   ├── agent.py          # 智能体对话 | Agent chat
│   │   ├── generation.py     # 内容生成 | Content generation
│   │   ├── dashboard.py      # 仪表盘 | Dashboard
│   │   ├── file.py           # 文件操作 | File operations
│   │   └── settings.py       # 系统设置 | Settings
│   ├── config/               # 配置管理 | Configuration
│   ├── core/                 # 核心组件 | Core components
│   │   ├── agent_loader.py   # 智能体加载 | Agent loader
│   │   ├── session_manager.py # 会话管理 | Session manager
│   │   ├── prompt_builder.py # 提示词构建 | Prompt builder
│   │   └── skill_base.py     # 技能管理 | Skill management
│   ├── models/               # 数据模型 | Data models
│   └── services/             # 外部服务 | External services
│
├── web/                       # 前端页面 | Frontend
├── xhb-gw/                    # 官网静态文件 | Official site
├── dashboard/                 # 运营数据看板 | Operations dashboard
├── ai-admin/                  # AI 管理后台 | AI admin panel
│
├── workspace/                 # 智能体工作区 | Agent workspaces
├── skills/                    # AI 技能模块 | AI skill modules
└── knowledge_base/           # AI 知识库 | AI knowledge base
```

---

## 快速部署 | Quick Deployment

### 环境要求 | Requirements
- Python 3.10+
- 通义千问 API Key (阿里云百炼平台 | Alibaba Cloud Bailian)

### 步骤 | Steps

```bash
# 1. 安装依赖 | Install dependencies
pip install -r requirements.txt

# 2. 配置 API Key
# 编辑 .env 文件 | Edit .env file
DASHSCOPE_API_KEY=your_api_key_here
AI_PROVIDER=qwen

# 3. 启动服务 | Start server
python main.py
```

访问 | Access: `http://服务器IP:9002` → `http://server-ip:9002`

---

## API 接口 | API Endpoints

| 接口 | Method | 说明 | Description |
|------|--------|------|-------------|
| `/health` | GET | 健康检查 | Health check |
| `/api/agent/chat` | POST | 智能体对话 | Agent chat |
| `/api/agent/generate` | POST | 内容生成 | Content generation |
| `/api/intelligence` | POST | 情报收集(联网) | Intelligence (web search) |
| `/api/xhs-copy` | POST | 小红书文案 | XHS copywriting |
| `/api/short-video` | POST | 短视频文案 | Short video scripts |
| `/api/poster` | POST | 海报提示词 | Poster prompts |
| `/api/generate-poster` | POST | 海报图片生成 | Poster image generation |
| `/api/dashboard` | GET | 运营数据 | Operations data |
| `/api/settings` | GET/POST | 设置管理 | Settings |
| `/api/token-stats` | GET | Token 统计 | Token statistics |

---

## 安全特性 | Security Features

- **输入隔离 | Input Sanitization**: 问候语拦截 + Prompt 注入检测
- **净化处理 | Sanitization**: 移除控制字符和多余空白
- **会话管理 | Session Management**: 独立的会话文件存储

---

## 更新日志 | Changelog

### v2.0 (2026-04-02)
- ✨ 新增通义千问联网搜索功能 | Added Qwen web search
- ✨ 统一模块容器宽度 900px | Unified container width to 900px
- 🔧 优化情报收集智能体体验 | Optimized intelligence agent
- 🐛 修复多项问题 | Fixed multiple issues

---

## 联系方式 | Contact

**猩伙伴民宿 - 长沙城市知己**
**XHB Homestay - Changsha City Companion**

*Built with ❤️ based on 阿里云通义千问 | Built on Alibaba Cloud Qwen LLM*