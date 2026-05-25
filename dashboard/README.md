# 猩伙伴民宿运营看板 - 使用说明

## 项目概述

猩伙伴民宿运营看板是一套全自动化数据管道，支持从百居易（MyHostex）民宿管理系统抓取订单数据，并在本地看板中实时展示。

---

## 一、快速启动

### 方式一：一键启动（推荐）

双击运行 `启动看板.bat`，自动启动服务器并打开浏览器。

### 方式二：手动启动

```bash
cd projects\myhostex-dashboard
node server.js
```

然后浏览器访问：`http://127.0.0.1:3000/dashboard-v2.html`

---

## 二、数据更新

### 手动更新

```bash
node update-data.js
```

### 定时自动更新（Windows计划任务）

系统会自动配置每天早上8:00自动运行抓取脚本。

**手动创建计划任务命令：**

```bash
schtasks /create /tn "猩伙伴数据更新" /tr "cmd /c cd /d C:\Users\murut\.openclaw\workspace-designer\projects\myhostex-dashboard && node update-data.js" /sc daily /st 08:00 /f
```

**查看现有计划任务：**
```bash
schtasks /query /tn "猩伙伴数据更新"
```

**删除计划任务：**
```bash
schtasks /delete /tn "猩伙伴数据更新" /f
```

---

## 三、文件说明

| 文件 | 说明 |
|------|------|
| `dashboard-v2.html` | 看板主页面 |
| `myhostex_all_orders.json` | 订单数据源（由抓取脚本自动更新） |
| `myhostex_all_orders.backup.json` | 数据备份（自动生成） |
| `scrape_status.json` | 抓取状态记录 |
| `last_updated.txt` | 最后更新时间戳 |
| `error.log` | 错误日志 |
| `update-data.js` | 数据抓取脚本 |
| `server.js` | 本地HTTP服务器 |
| `启动看板.bat` | 一键启动 |
| `定时抓取.bat` | 定时任务调用的脚本 |

---

## 四、健壮性机制

| 场景 | 处理方式 |
|------|---------|
| 网络断开 | 自动重试3次，每次间隔30秒 |
| 连续3次失败 | 从备份恢复数据，标记警告状态 |
| JSON文件损坏 | 自动使用上一次成功的备份 |
| 浏览器未登录 | 报错退出，不覆盖有效数据 |

---

## 五、状态文件说明

### scrape_status.json

```json
{
  "lastRun": "2026/4/21 08:00:00",      // 上次运行时间
  "lastSuccess": "2026/4/21 08:00:12",  // 上次成功时间
  "consecutiveFailures": 0,              // 连续失败次数
  "lastError": null                       // 最后错误信息
}
```

### last_updated.txt

纯文本，存储最后一次成功更新的时间。

---

## 六、技术栈

- **数据抓取**：Puppeteer CDP + 百居易隐藏API
- **静态服务器**：Node.js原生http模块（无额外依赖）
- **数据存储**：JSON + Excel（xlsx）
- **定时任务**：Windows Task Scheduler

---

## 七、依赖安装

```bash
npm install puppeteer-core xlsx
```

> 注意：puppeteer-core 依赖已有 Chrome/Edge 浏览器（通过 CDP 端口 18800 连接）

---

## 八、注意事项

1. **首次使用前**：先在浏览器中手动打开并登录百居易（myhostex.com），确保登录状态有效
2. **数据过滤**：页面默认只显示2026年4月1日及以后的订单
3. **关闭服务器**：服务器在后台持续运行，关闭CMD窗口即可停止
4. **查看日志**：错误日志记录在 `error.log` 文件中
