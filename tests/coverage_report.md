# 测试覆盖率报告

生成时间: 2026/05/25
项目路径: E:\project\Homestay\Homestay

## 当前覆盖率概览

| 模块 | 覆盖行数 | 总行数 | 覆盖率 | 目标 | 差距 |
|------|---------|--------|--------|------|------|
| backend/api/agent.py | 141 | 301 | 47% | 80% | -33% |
| backend/api/generation.py | 29 | 168 | 17% | 80% | -63% |
| backend/api/file.py | 24 | 104 | 23% | 80% | -57% |
| backend/core/agent_loader.py | 78 | 171 | 46% | 80% | -34% |
| backend/core/session_manager.py | 52 | 84 | 62% | 80% | -18% |
| backend/core/skill_base.py | 158 | 225 | 70% | 80% | -10% |
| backend/core/file_manager.py | 15 | 49 | 31% | 80% | -49% |
| backend/core/prompt_builder.py | 9 | 27 | 33% | 80% | -47% |
| backend/services/ai_client.py | 15 | 27 | 56% | 80% | -24% |
| backend/services/search_service.py | 4 | 12 | 33% | 80% | -47% |
| backend/services/token_tracker.py | 7 | 15 | 47% | 80% | -33% |
| backend/api/dashboard.py | 6 | 8 | 75% | 80% | -5% |
| backend/api/settings.py | 11 | 15 | 73% | 80% | -7% |
| backend/config/settings.py | 30 | 49 | 61% | 80% | -19% |
| **总计** | **650** | **1326** | **49%** | **80%** | **-31%** |

---

## 关键发现

### 1. 核心模块覆盖严重不足

- **agent.py** (47%): 核心聊天逻辑、Skill匹配、Prompt注入检测未充分测试
- **generation.py** (17%): 内容生成核心逻辑几乎全部未覆盖
- **file.py** (23%): 文件操作API覆盖不足

### 2. 安全函数测试缺口

以下安全相关函数**完全未测试**:
- `has_injection()` - Prompt注入检测
- `sanitize_input()` - 输入净化
- `is_greeting()` - 问候语拦截

### 3. 流式响应未测试

所有流式响应处理（`StreamingResponse`）均未进行Mock测试:
- `agent_chat()` 的流式返回
- `agent_generate()` 的流式返回
- `_call_generate_stream()` 内部方法

---

## 缺失测试详细列表

### 高优先级 (Critical - 覆盖率 < 50%)

#### 1. `backend/api/agent.py` (47%)

| 函数/代码块 | 未覆盖行 | 说明 |
|-------------|----------|------|
| `_build_skill_prompt()` | 83-107 | Skill自动匹配逻辑未测试 |
| `agent_chat()` 流式处理 | 185-214 | 流式响应完整流程未Mock |
| `agent_chat()` 搜索上下文 | 137-149 | 联网搜索功能未测试 |
| `agent_generate()` | 220-294 | 生成模式完整逻辑未测试 |
| `_poster_generate()` | 297-397 | 海报生成专用函数未测试 |
| `get_agent_info()` | 400-429 | 智能体信息获取未测试 |
| `list_agents()` | 488-514 | 智能体列表API未测试 |
| 会话管理API | 519-585 | 会话CRUD操作未测试 |

**需要添加的测试**:
```python
test_agent_chat_streaming_response()
test_agent_chat_with_search_enabled()
test_agent_chat_injection_detection()
test_agent_generate_with_skill_prompt()
test_poster_generate_success()
test_poster_generate_no_api_key_error()
test_get_agent_info_returns_config()
test_list_agents_returns_all()
test_session_crud_operations()
```

#### 2. `backend/api/generation.py` (17%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `_call_generate_stream()` | 24-87 | 通用流式生成核心逻辑 |
| `generate_wechat_article()` | 92-125 | 公众号文章生成 |
| `generate_xhs_copy()` | 184-218 | 小红书文案生成 |
| `generate_short_video()` | 221-260 | 短视频脚本生成 |
| `generate_poster_prompts()` | 264-335 | 海报提示词生成(含JSON解析) |
| `generate_poster_image()` | 338-363 | 海报图片生成 |
| `get_poster_history()` | 366-381 | 海报历史记录 |

**需要添加的测试**:
```python
test_call_generate_stream_success()
test_call_generate_stream_saves_to_file()
test_generate_wechat_article_streaming()
test_generate_xhs_copy_streaming()
test_generate_short_video_streaming()
test_generate_poster_prompts_json_parsing()
test_generate_poster_prompts_json_fallback()
test_generate_poster_image_success()
test_get_poster_history()
```

#### 3. `backend/api/file.py` (23%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `read_file()` | 17-26 | 文件读取 |
| `write_file()` | 29-38 | 文件写入 |
| `create_document()` | 41-50 | 文档创建 |
| `list_files()` | 53-62 | 文件列表 |
| `upload_file()` | 65-161 | 文件上传(多种格式) |
| `list_knowledge()` | 164-175 | 知识库列表 |
| `get_knowledge_by_category()` | 178-197 | 按分类获取知识 |

**需要添加的测试**:
```python
test_read_file_success()
test_read_file_not_found()
test_write_file_success()
test_create_document_success()
test_list_files()
test_upload_file_txt()
test_upload_file_pdf()
test_upload_file_unsupported_format()
test_upload_file_size_limit()
test_list_knowledge_empty()
test_list_knowledge_with_documents()
test_get_knowledge_by_category()
```

### 中优先级 (Medium - 覆盖率 50-70%)

#### 4. `backend/core/agent_loader.py` (46%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `_find_actual_dir()` | 63-78 | 中文目录别名查找 |
| `_load_skills_prompt()` | 131-147 | Skills提示词加载 |
| `_load_session_history()` | 151-206 | 会话历史加载(三种格式) |
| `get_full_context()` | 210-258 | 完整上下文组合 |
| `get_prompt_with_context()` | 298-300 | 兼容接口 |

**需要添加的测试**:
```python
test_find_actual_dir_with_chinese_name()
test_find_actual_dir_not_found()
test_load_skills_prompt()
test_load_session_history_json()
test_load_session_history_md()
test_load_session_history_sessions()
test_get_full_context_with_all_components()
test_get_full_context_with_session_history_param()
```

#### 5. `backend/core/session_manager.py` (62%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `flush_pending_writes()` | 74-81 | 批量写入强制刷新 |
| `get_messages_for_api()` | 118-130 | API格式消息转换 |
| `list_sessions()` 排序 | 164-165 | 按更新时间倒序 |
| `get_all_sessions_count()` | 174-180 | 统计会话总数 |

**需要添加的测试**:
```python
test_flush_pending_writes()
test_get_messages_for_api_format()
test_list_sessions_sorted_by_updated_at()
test_list_sessions_empty()
test_list_sessions_handles_corrupt_file()
test_get_all_sessions_count()
```

#### 6. `backend/core/skill_base.py` (70%)

| 类 | 方法 | 未覆盖行 | 说明 |
|----|------|----------|------|
| SkillLoader | `_load_templates()` | 244-254 | 模板加载 |
| SkillLoader | `_load_examples()` | 256-281 | 示例加载 |
| SkillLoader | `_parse_yaml_frontmatter()` | 233-242 | YAML解析 |
| SkillExecutor | `get_system_prompt()` | 334-358 | 系统提示词获取 |
| SkillExecutor | `get_template()` | 360-362 | 模板获取 |
| SkillExecutor | `get_example()` | 364-368 | 示例获取 |
| SkillChain | 全部方法 | 372-461 | Skill链式调用 |

**需要添加的测试**:
```python
test_parse_yaml_frontmatter_valid()
test_parse_yaml_frontmatter_invalid()
test_load_templates_multiple()
test_load_examples_with_metadata()
test_skill_executor_get_system_prompt()
test_skill_executor_get_template()
test_skill_chain_add_skill()
test_skill_chain_build_prompt()
test_skill_chain_auto_match()
```

#### 7. `backend/services/ai_client.py` (56%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `get_client()` 错误处理 | 21-26 | Provider失败切换 |
| `get_client()` 异常处理 | 33-35 | 无API Key异常 |
| `mark_provider_error()` | 38-44 | 错误标记逻辑 |
| `mark_provider_success()` | 47-50 | 成功重置逻辑 |

**需要添加的测试**:
```python
test_get_client_caches_client()
test_get_client_switches_on_error()
test_get_client_raises_without_api_key()
test_mark_provider_error_increments()
test_mark_provider_error_clears_cache()
test_mark_provider_success_resets()
```

#### 8. `backend/core/file_manager.py` (31%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `read_file()` | 17-20 | 文件读取 |
| `write_file()` | 24-25 | 文件写入 |
| `create_document()` | 37-47 | 文档创建 |
| `list_files()` | 57-65 | 文件列表 |
| `delete_file()` | 77-89 | 文件删除 |
| `get_file_info()` | 101-102 | 文件信息 |
| `ensure_directory()` | 114-120 | 目录确保 |
| 统计方法 | 132-139 | 使用统计 |

#### 9. `backend/core/prompt_builder.py` (33%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `build_chat_prompt()` | 22-29 | 聊天Prompt构建 |
| `build_generate_prompt()` | 42-55 | 生成Prompt构建 |
| `build_system_prompt()` | 67-74 | 系统Prompt构建 |
| `format_history()` | 87-100 | 历史格式化 |

#### 10. `backend/services/search_service.py` (33%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `baidu_search()` | 9-48 | 百度搜索全部逻辑 |

#### 11. `backend/services/token_tracker.py` (47%)

| 函数 | 未覆盖行 | 说明 |
|------|----------|------|
| `add_token_record()` | 20-34 | Token记录添加 |
| `get_token_summary()` | 39 | Token汇总获取 |
| `get_daily_usage()` | 44 | 日使用量统计 |

### 低优先级 (Lower - 覆盖率 > 70%)

#### 12. `backend/config/settings.py` (61%)

缺少配置加载和默认值处理的测试。

#### 13. `backend/api/dashboard.py` (75%)

大部分已覆盖，仅需补充边界情况测试。

#### 14. `backend/api/settings.py` (73%)

大部分已覆盖。

---

## 边界用例缺失

以下边界用例**完全未测试**:

1. **空输入处理**
   - 空字符串消息
   - None/Null值
   - 超长输入截断

2. **文件操作边界**
   - 文件不存在
   - 文件损坏/无法解析
   - 目录不存在
   - 权限错误

3. **JSON解析边界**
   - 非JSON格式响应
   - 截断的JSON
   - 畸形JSON字符

4. **并发场景**
   - 多会话同时写入
   - 批量写入刷新
   - 并发文件上传

5. **错误恢复**
   - API Key无效
   - 网络超时
   - Provider失败切换

6. **安全边界**
   - Prompt注入边界情况
   - 超长注入文本
   - 多层编码注入

---

## 覆盖率提升建议

### 1. 立即行动 (Critical - 阻断发布)

```
1. 添加 agent.py 流式响应 Mock 测试
   - Mock get_client() 返回值
   - Mock StreamingResponse 完整流程
   - 覆盖 160 行未覆盖代码

2. 添加 generation.py JSON解析边界测试
   - test_generate_poster_prompts_json_parsing_valid()
   - test_generate_poster_prompts_json_parsing_invalid_fallback()
   - 覆盖 139 行未覆盖代码

3. 添加安全函数测试
   - has_injection() 各种模式测试
   - sanitize_input() 边界字符测试
   - 覆盖 30+ 行关键代码
```

### 2. 短期优化 (High - 提升覆盖率)

```
1. 补充 file.py CRUD 测试
   - 使用 tempfile 创建测试文件
   - Mock 文件系统操作
   - 覆盖 80 行未覆盖代码

2. 补充 session_manager.py 批量写入测试
   - 测试 flush_pending_writes()
   - 测试并发写入
   - 覆盖 32 行未覆盖代码

3. 补充 agent_loader.py 上下文组合测试
   - 测试多种历史格式加载
   - 测试 Skill 提示词注入
   - 覆盖 93 行未覆盖代码
```

### 3. 中期完善 (Medium - 达到目标)

```
1. 补充 skill_base.py 完整测试
   - SkillLoader 扫描和匹配
   - SkillExecutor 执行
   - SkillChain 组合调用

2. 补充 services 层测试
   - ai_client 错误处理
   - search_service 搜索逻辑
   - token_tracker 统计逻辑

3. 添加 E2E 流式响应测试
   - 完整聊天流程
   - 完整生成流程
```

### 4. 长期建设 (Lower - 超越目标)

```
1. 添加性能测试
2. 添加并发压力测试
3. 添加安全渗透测试
4. 建立覆盖率门禁 (>80% 才能合并)
```

---

## 测试基础设施建议

### Mock 策略

```python
# 1. AI Client Mock
@pytest.fixture
def mock_ai_client():
    client = AsyncMock()
    response = AsyncMock()
    response.choices = [Mock(delta=Mock(content="测试响应"))]
    client.chat.completions.create.return_value = response
    return client

# 2. 文件系统 Mock
@pytest.fixture
def mock_file_system(tmp_path):
    # 创建测试目录结构
    return tmp_path

# 3. Session Manager Mock
@pytest.fixture
def mock_session():
    # 使用 tmp_path 创建隔离会话
    pass
```

### 覆盖率目标分解

| 阶段 | 目标覆盖率 | 时间 | 关键模块 |
|------|-----------|------|----------|
| Phase 1 | 60% | 第1周 | agent.py, generation.py |
| Phase 2 | 70% | 第2周 | file.py, session_manager.py |
| Phase 3 | 78% | 第3周 | skill_base.py, services |
| Phase 4 | 80%+ | 第4周 | 全模块覆盖+边界测试 |

---

## 附录: 未覆盖代码清单

### agent.py 完整缺失列表

```
行号  | 代码
------|----------------------------------
104  | skill_prompt = ""
105  | return skill_prompt
140  | search_context = ""
141-149 | 联网搜索逻辑
161  | system_prompt += f"\n\n{skill_prompt}"
163  | system_prompt += search_context
178  | messages.extend(session_history)
185-214 | 流式响应处理完整逻辑
228  | return await _poster_generate(...)
254-291 | agent_generate 完整逻辑
302-397 | _poster_generate 完整逻辑
422-426 | get_agent_info 读取文件逻辑
448-449 | get_agent_history 条件分支
464-465 | clear_agent_history
471-485 | save_chat_to_sessions
513-514 | list_agents 循环
522-534 | list_sessions
540-551 | create_session
557-569 | get_session_history
575-585 | delete_session
```

### generation.py 完整缺失列表

```
行号  | 代码
------|----------------------------------
36-87 | _call_generate_stream 完整逻辑
99-125 | generate_wechat_article
131-174 | chat 接口完整逻辑
180-181 | intelligence
190-218 | generate_xhs_copy
227-260 | generate_short_video
269-335 | generate_poster_prompts (含JSON解析)
341-363 | generate_poster_image
369-381 | get_poster_history
```

---

**报告生成**: 基于 `pytest --cov=backend --cov-report=term-missing` 输出
**测试框架**: pytest + pytest-cov
**总测试数**: 35 (27 通过, 8 失败)