# AI Matrix Skill 模块化框架

## 📁 目录结构

```
ai-matrix/
├── skills/                          # 全局 Skill 库
│   ├── _templates/                  # Skill 创建模板
│   │   └── SKILL.md
│   ├── marketplace.json              # 技能市场索引
│   │
│   ├── content/                     # 内容创作类
│   │   ├── xhs_writer/              # 小红书文案
│   │   │   ├── SKILL.md             # 技能定义（必需）
│   │   │   ├── templates/           # 文案模板
│   │   │   └── examples/            # 优秀案例
│   │   ├── wechat_writer/           # 公众号文案
│   │   ├── video_script/             # 视频脚本
│   │   └── poster_generator/        # 海报生成
│   │
│   └── analysis/                    # 分析类
│       ├── data_analyzer/            # 数据分析
│       └── trend_detector/          # 趋势洞察
│
└── workspace/{agent_id}/skills/      # Agent 专属 Skills（可选）
```

## 🔧 使用方式

### 1. 在 Agent 中引用 Skill

编辑 `workspace/{agent_id}/agent.md`，添加技能引用：

```markdown
## 可用技能

### 技能 1: 小红书文案
类型：xhs_writer
触发词：种草、推荐、小红书
使用方式：直接调用

### 技能 2: 数据分析
类型：data_analyzer
触发词：分析、统计、数据
使用方式：直接调用
```

### 2. 编程方式使用

```python
from backend.core.skill_base import SkillLoader, SkillChain

# 加载 Agent 的所有 Skills
loader = SkillLoader(agent_id="xhs")

# 列出所有可用 Skills
for skill in loader.get_all_skills():
    print(f"{skill.skill_id}: {skill.name}")

# 根据关键词匹配 Skill
matched = loader.match_skills("帮我写一篇小红书种草文案")
for skill in matched:
    print(f"匹配到: {skill.name}")

# 创建 Skill 链
chain = SkillChain(agent_id="xhs")
chain.add_skill("xhs_writer")
prompt = chain.build_prompt("帮我写一篇五一民宿推荐")
```

## 📝 SKILL.md 标准格式

```yaml
---
id: skill_id                    # 唯一标识（英文）
name: 技能显示名称               # 中文显示名
type: content                   # 类型：content | analysis | tool | template
trigger: keyword                # 触发：keyword | intent | chain | manual
description: 简短描述            # 功能说明
keywords:                        # 关键词列表
  - 种草
  - 推荐
  - 民宿
intent_patterns:                 # 意图模式（可选）
  - 帮我写一篇小红书
priority: 10                     # 优先级（数字越大越优先）
enabled: true                    # 是否启用
config:                          # 自定义配置
  default_length: medium
---

# 技能详细说明

这里是技能的核心提示词内容...
```

## ➕ 创建新 Skill

1. **复制模板**：
```bash
cp skills/_templates/SKILL.md skills/content/your_skill/SKILL.md
```

2. **编辑 SKILL.md**：填入技能定义

3. **添加资源**（可选）：
```
skills/content/your_skill/
├── SKILL.md
├── templates/      # 模板文件
│   └── template1.md
└── examples/       # 示例文件
    └── example1.md
```

4. **更新 marketplace.json**（可选）：
```json
{
  "id": "your_skill",
  "name": "你的技能",
  "category": "content",
  "tags": ["标签1", "标签2"],
  "agent_ids": ["agent1", "agent2"],
  "description": "技能描述"
}
```

## 🔍 Skill 匹配机制

### 关键词匹配
当用户输入包含 Skill 定义的 keywords 时，自动触发。

### 意图识别
当用户输入匹配 intent_patterns 时触发（优先级低于关键词）。

### 手动调用
在 prompt 中明确指定使用某个 Skill。

## 📊 已有的 Skills

| Skill ID | 名称 | 类型 | 适用 Agent |
|----------|------|------|-----------|
| xhs_writer | 小红书文案 | content | xhs |
| wechat_writer | 公众号文案 | content | wechat |
| video_script | 视频脚本 | content | shortvideo |
| poster_generator | 海报生成 | content | poster |
| data_analyzer | 数据分析 | analysis | intelligence, dashboard |
| trend_detector | 趋势洞察 | analysis | intelligence |
