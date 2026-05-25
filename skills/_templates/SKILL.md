---
id: skill_template
name: Skill 标准模板
type: template
trigger: manual
description: 新建 Skill 时的标准模板，定义 Skill 的标准格式
keywords: []
priority: 0
enabled: true
config:
  version: "1.0"
---

# Skill 标准模板

## 概述
简要说明这个 Skill 的功能和使用场景。

## 触发条件
- **触发方式**：`keyword` | `intent` | `chain` | `manual`
- **关键词**：（当触发方式为 keyword 时）例如：分析、统计、报告
- **意图模式**：（当触发方式为 intent 时）例如：用户想要了解某方面的数据

## 执行流程
1. 步骤一：...
2. 步骤二：...
3. 步骤三：...

## 输入参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| param1 | string | 是 | 参数1说明 |

## 输出格式
描述输出的格式，例如：
```json
{
  "result": "结果",
  "confidence": 0.95
}
```

## 示例

### 示例 1
**输入**：用户说"帮我分析一下本月数据"
**输出**：一份完整的数据分析报告

### 示例 2
...

## 注意事项
- 注意点1
- 注意点2
