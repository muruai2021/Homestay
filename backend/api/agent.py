"""智能体相关 API 路由"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import AgentChatRequest, AgentGenerateRequest, SaveChatRequest
from core.agent_loader import get_agent_id, AgentLoader
from core.session_manager import SessionManager
from core.prompt_builder import PromptBuilder
from core.file_manager import FileManager
from services.ai_client import get_client, mark_provider_error, mark_provider_success
from core.skill_base import SkillLoader, SkillExecutor
from config.settings import AI_PROVIDER, IAM_PROMPT
from config.api_config import get_api_config
from services.token_tracker import add_token_record
import json
import re


# ============ 输入隔离处理 ============

# 问候语模式
GREETING_PATTERNS = [
    r"^(你好|您好|hi|hey|hello|嗨|哈喽|在吗|帮忙)\s*$",
]

# Prompt 注入模式 - 增强版
INJECTION_PATTERNS = [
    # English patterns
    "ignore previous instructions",
    "disregard your orders",
    "forget all previous",
    "new instructions",
    "[system prompt]",
    "override your programming",
    "disregard your guidelines",
    "you are now",
    "act as",
    "pretend you are",
    "developer mode",
    "jailbreak",
    # Chinese patterns
    "忘掉所有",
    "你现在是",
    "你是一个",
    "忽略之前",
    "无视之前",
    "请扮演",
    "你现在扮演",
    "系统提示",
    "忽略系统",
    "打破规则",
    "绕过限制",
    "请忽略",
    "不要遵循",
]


def is_greeting(text: str) -> bool:
    """判断是否为问候语"""
    text = text.strip()
    for p in GREETING_PATTERNS:
        if re.match(p, text, re.IGNORECASE):
            return True
    return False


def has_injection(text: str) -> bool:
    """检测 Prompt 注入攻击"""
    text_lower = text.lower()
    return any(p.lower() in text_lower for p in INJECTION_PATTERNS)


def sanitize_input(text: str) -> str:
    """净化用户输入"""
    # 移除控制字符
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ============ Skill 提示词构建 ============

def _build_skill_prompt(agent_name: str, user_input: str) -> str:
    """
    自动匹配并加载相关 Skills 的提示词增强
    """
    skill_prompt = ""
    try:
        skill_loader = SkillLoader(agent_name)
        
        # 自动匹配 Skills（最多2个）
        matched_skills = skill_loader.match_skills(user_input)[:2]
        
        for skill in matched_skills:
            executor = SkillExecutor(skill)
            skill_content = executor.get_system_prompt()
            if skill_content:
                skill_prompt += f"\n\n## 技能增强: {skill.name}\n{skill_content}\n"
                print(f"[Skill] 已加载技能: {skill.name} (匹配关键词)")
        
        # 🔧 重要：不自动加载默认技能，避免覆盖 Agent 身份
        # 只有明确匹配到相关技能时才加载
                    
    except Exception as e:
        print(f"[Skill] Skill 加载失败: {e}")
    
    return skill_prompt


router = APIRouter()


@router.post("/chat")
async def agent_chat(request: AgentChatRequest):
    """智能体聊天接口"""
    try:
        # ========== 输入隔离处理 ==========
        user_input = sanitize_input(request.message)

        # 1. Prompt 注入检测
        if has_injection(user_input):
            return StreamingResponse(
                iter([b"\xe6\x8a\xb1\xe6\xad\x89\xef\xbc\x8c\xe6\x88\x91\xe6\x97\xa0\xe6\xb3\x95\xe5\xa4\x84\xe7\x90\x86\xe8\xbf\x99\xe7\xb1\xbb\xe8\xaf\xb7\xe6\xb1\x82\xe3\x80\x82"]),
                media_type="text/plain"
            )

# DISABLED:         # 2. 问候语拦截 → 直接返回简短问候，不触发 Agent
# DISABLED:         if is_greeting(user_input):
# DISABLED:             return StreamingResponse(
# DISABLED:                 iter([b"\xe4\xbd\xa0\xe5\xa5\xbd\xef\xbc\x81\xe6\x9c\x89\xe4\xbb\x80\xe4\xb9\x88\xe5\x8f\xaf\xe4\xbb\xa5\xe5\xb8\xae\xe4\xbd\xa0\xe7\x9a\x84\xe5\x90\x97\xef\xbc\x9f"]),
# DISABLED:                 media_type="text/plain"
# DISABLED:             )

        agent_name = get_agent_id(request.agent_id)
        session_mgr = SessionManager(agent_name, session_id=request.session_id)

        # 🔍 联网搜索功能
        search_context = ""
        if request.enable_search:
            try:
                from services.search_service import baidu_search
                search_results = await baidu_search(user_input, max_results=3)
                if search_results.get('results'):
                    search_context = "\n\n【联网搜索结果】\n"
                    for i, r in enumerate(search_results['results'][:3], 1):
                        search_context += f"{i}. {r.get('title', '')}: {r.get('content', '')}\n"
                    print(f"[Search] 已获取搜索结果: {len(search_results.get('results', []))}条")
            except Exception as e:
                print(f"[Search] 搜索失败: {e}")

        # 加载智能体提示词
        loader = AgentLoader(agent_name)
        prompt_builder = PromptBuilder(loader)

        # 🔧 自动匹配 Skills 增强提示词
        skill_prompt = _build_skill_prompt(agent_name, user_input)

        # 构建系统提示词（不包含用户输入）
        system_prompt = loader.get_prompt_with_context()
        if skill_prompt:
            system_prompt += f"\n\n{skill_prompt}"
        if search_context:
            system_prompt += search_context

        # 构建消息列表 (OpenAI API 格式)
        # 核心逻辑：system = 角色宪法， user = 即时任务
        # AI以角色身份响应用户输入
        messages = []
        # 1. 系统提示词 = 角色定义（宪法）
        messages.append({"role": "system", "content": system_prompt})
        # 2. 历史记录：优先使用前端传入，其次从会话文件加载
        if request.history:
            messages.extend(request.history)
        else:
            # 从会话文件加载历史
            session_history = session_mgr.get_messages_for_api(limit=10)
            if session_history:
                messages.extend(session_history)
        # 3. 用户输入 = 即时任务（直接传递，不加包装）
        messages.append({"role": "user", "content": user_input})


        # 调用 AI
        client = get_client()
        model_name = get_api_config(AI_PROVIDER).get("model", "qwen-plus")
        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True
        )

        # 返回流式响应
        async def generate():
            full_content_list = []
            try:
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_content_list.append(content)
                        yield content

                # 保存对话记录
                full_content = "".join(full_content_list)
                session_mgr.add_message("user", user_input)
                session_mgr.add_message("assistant", full_content)

                # 标记成功
                mark_provider_success(AI_PROVIDER)

            except Exception as e:
                mark_provider_error(AI_PROVIDER)
                yield f"\n\n[错误]: {str(e)}"

        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def agent_generate(request: AgentGenerateRequest):
    """智能体生成接口（生成模式，自动保存文件）"""
    try:
        agent_name = get_agent_id(request.agent_id)
        
        # ========== 海报生成智能体特殊处理 ==========
        if request.agent_id == "poster":
            return await _poster_generate(request, agent_name)
        
        # ========== 其他智能体：正常 LLM 生成流程 ==========
        session_mgr = SessionManager(agent_name)
        loader = AgentLoader(agent_name)

        # 🔧 自动匹配 Skills 增强提示词
        skill_prompt = _build_skill_prompt(agent_name, request.prompt)

        # 构建系统提示词（不包含用户输入）
        system_prompt = loader.get_prompt_with_context()
        if skill_prompt:
            system_prompt += f"\n\n{skill_prompt}"

        # 构建消息列表 (OpenAI API 格式) - 正确优先级
        messages = []
        # 1. 添加系统提示词
        messages.append({"role": "system", "content": system_prompt})
        # 2. 添加历史记录
        if request.history:
            messages.extend(request.history)
        # 3. 添加用户输入（独立消息）
        messages.append({"role": "user", "content": request.prompt})

        # 调用 AI
        client = get_client()
        response = await client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=True
        )

        # 返回流式响应
        async def generate():
            full_content_list = []
            try:
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_content_list.append(content)
                        yield content

                # 保存对话记录
                full_content = "".join(full_content_list)
                session_mgr.add_message("user", request.prompt)
                session_mgr.add_message("assistant", full_content)

                # 生成模式：自动保存文件
                file_mgr = FileManager(agent_name)
                import time
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"{request.prompt[:20]}_{timestamp}.md"
                file_mgr.write_file(filename, full_content)

                yield f"\n\n[文件已保存到: workspace/{agent_name}/outputs/{filename}]"

                # 标记成功
                mark_provider_success(AI_PROVIDER)

            except Exception as e:
                mark_provider_error(AI_PROVIDER)
                yield f"\n\n[错误]: {str(e)}"

        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _poster_generate(request: AgentGenerateRequest, agent_name: str):
    """
    海报生成智能体专用生成函数
    Skill + 图像 API 联动
    """
    from fastapi.responses import StreamingResponse
    
    async def generate():
        try:
            # 1. 保存用户消息
            session_mgr = SessionManager(agent_name)
            session_mgr.add_message("user", request.prompt)
            
            # 2. 构建海报生成提示词（使用 Skill 增强）
            from core.skill_base import SkillLoader
            skill_loader = SkillLoader(agent_name)
            
            # 加载 poster_generator Skill
            poster_skill = skill_loader.get_skill("poster_generator")
            skill_prompt = ""
            if poster_skill:
                skill_path = poster_skill.skill_path / "SKILL.md"
                if skill_path.exists():
                    with open(skill_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 移除 YAML 头部
                        if content.startswith("---"):
                            content = content.split("---", 2)[-1]
                        skill_prompt = content.strip()
            
            # 3. 构建图像生成提示词
            from core.poster_generator import create_poster_generator
            generator = create_poster_generator(agent_name)
            
            # 解析用户输入，提取风格和描述
            user_input = request.prompt
            
            # 简单解析：检测风格关键词
            style = "现代简约"
            if "清新" in user_input or "自然" in user_input:
                style = "清新自然"
            elif "轻奢" in user_input or "高级" in user_input:
                style = "轻奢高级"
            elif "简约" in user_input:
                style = "现代简约"
            
            # 提取描述（去掉风格词）
            description = user_input
            for s in ["现代简约", "清新自然", "轻奢高级", "风格", "海报"]:
                description = description.replace(s, "").strip()
            
            if not description:
                description = user_input
            
            # 构建增强提示词
            enhanced_prompt = f"""请为猩伙伴民宿设计一张{style}风格海报。

用户需求：{description}

"""
            if skill_prompt:
                enhanced_prompt += f"\n设计指导：\n{skill_prompt[:500]}\n"
            
            # 4. 调用图像生成 API
            result = await generator.generate_image(
                description=enhanced_prompt,
                style=style,
                ratio="3:4"
            )
            
            # 5. 流式返回结果
            if result.get("success"):
                image_url = result["image_url"]
                prompt = result.get("prompt", "")
                
                yield f"✨ **海报生成成功！**\n\n"
                yield f"📝 **提示词**：{prompt[:100]}...\n\n"
                yield f"🎨 **风格**：{style}\n\n"
                yield f"🖼️ **图片链接**：{image_url}\n\n"
                yield f'[👀 查看大图]({image_url})\n\n'
                yield f"💾 已自动保存到 workspace/{agent_name}/outputs/\n"
                
                # 保存到会话
                session_mgr.add_message("assistant", 
                    f"✨ 海报生成成功！\\n风格：{style}\\n图片：{image_url}")
                
                mark_provider_success(AI_PROVIDER)
            else:
                error = result.get("error", "未知错误")
                yield f"❌ **海报生成失败**：{error}\n\n"
                if "API_KEY" in error or "未配置" in error:
                    yield f"⚠️ 请检查 .env 文件中的 DASHSCOPE_API_KEY 配置\n"
                
                session_mgr.add_message("assistant", f"海报生成失败：{error}")
                mark_provider_error(AI_PROVIDER)
                
        except Exception as e:
            yield f"\n\n[错误]: {str(e)}"
            mark_provider_error(AI_PROVIDER)
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.get("/{agent_id}/info")
async def get_agent_info(agent_id: str):
    """获取智能体信息"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name)

        # 读取智能体配置
        import os
        workspace = os.path.join(os.path.dirname(__file__), "..", "..", "workspace", agent_name)

        agent_md = os.path.join(workspace, "agent.md")
        soul_md = os.path.join(workspace, "soul.md")
        user_md = os.path.join(workspace, "user.md")

        info = {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "context": session_mgr.get_context()
        }

        # 读取智能体定义
        if os.path.exists(agent_md):
            with open(agent_md, "r", encoding="utf-8") as f:
                info["agent_def"] = f.read()

        return info

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_id}/history")
async def get_agent_history(agent_id: str, limit: int = None, all_history: bool = False):
    """获取智能体对话历史"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name)

        # 如果指定 all_history=True，返回所有历史记录
        count = None if all_history else limit
        history = session_mgr.get_history(count) if count else session_mgr.get_history()

        return {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "history": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_id}/clear")
async def clear_agent_history(agent_id: str):
    """清空智能体对话历史"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name)
        session_mgr.clear_history()

        return {
            "success": True,
            "message": "对话历史已清空"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_id}/save")
async def save_chat_to_sessions(agent_id: str, request: SaveChatRequest):
    """保存聊天记录到sessions.md"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name)

        # 添加每条消息到历史
        for msg in request.messages:
            if "role" in msg and "content" in msg:
                session_mgr.add_message(msg["role"], msg["content"])

        return {
            "success": True,
            "message": "聊天记录已保存"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def list_agents():
    """列出所有智能体"""
    try:
        import os

        workspace = os.path.join(os.path.dirname(__file__), "..", "..", "workspace")
        agents = []

        for item in os.listdir(workspace):
            agent_dir = os.path.join(workspace, item)
            if os.path.isdir(agent_dir):
                # 读取配置
                config_file = os.path.join(agent_dir, "config.json")
                if os.path.exists(config_file):
                    with open(config_file, "r", encoding="utf-8") as f:
                        config = json.load(f)
                        agents.append({
                            "id": config.get("id", item),
                            "name": config.get("name", item),
                            "desc": config.get("desc", ""),
                            "icon": config.get("icon", "")
                        })

        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 会话管理 API ====================

@router.get("/{agent_id}/sessions")
async def list_sessions(agent_id: str):
    """列出指定智能体的所有会话"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name)
        sessions = session_mgr.list_sessions()
        
        return {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "sessions": sessions,
            "total": len(sessions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_id}/sessions")
async def create_session(agent_id: str):
    """创建新会话"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name)
        
        return {
            "success": True,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "session_id": session_mgr.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_id}/sessions/{session_id}")
async def get_session_history(agent_id: str, session_id: str, limit: int = 50):
    """获取指定会话的历史"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name, session_id=session_id)
        history = session_mgr.get_history(limit)
        
        return {
            "agent_id": agent_id,
            "agent_name": agent_name,
            "session_id": session_id,
            "history": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{agent_id}/sessions/{session_id}")
async def delete_session(agent_id: str, session_id: str):
    """删除指定会话"""
    try:
        agent_name = get_agent_id(agent_id)
        session_mgr = SessionManager(agent_name, session_id=session_id)
        session_mgr.delete_session(session_id)
        
        return {
            "success": True,
            "message": f"会话 {session_id} 已删除"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
