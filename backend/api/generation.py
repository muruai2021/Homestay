"""
生成相关 API 路由
支持 Skill 模块化 + 流式输出
"""
from fastapi import APIRouter, HTTPException
from models.schemas import (
    ArticleRequest, ChatRequest, IntelligenceRequest,
    XhsRequest, ShortVideoRequest, PosterRequest
)
from services.ai_client import get_client, mark_provider_error, mark_provider_success
from services.search_service import baidu_search
from config.settings import AI_PROVIDER
from config.api_config import get_api_config
from core.agent_loader import AgentLoader
from core.prompt_builder import PromptBuilder
from core.session_manager import SessionManager
from core.file_manager import FileManager
import json

router = APIRouter()


# ========== 通用生成调用（内部使用）==========
async def _call_generate_stream(agent_id: str, prompt: str, task_description: str):
    """
    通用流式生成调用，内部被各功能路由使用
    
    Args:
        agent_id: 智能体ID
        prompt: 用户输入
        task_description: 任务描述（用于 prompt 构建）
    
    Yields:
        流式文本 chunks
    """
    from fastapi.responses import StreamingResponse
    
    try:
        session_mgr = SessionManager(agent_id)
        prompt_builder = PromptBuilder(AgentLoader(agent_id))
        
        # 构建生成模式提示词
        prompt_content = prompt_builder.build_generate_prompt(task_description, prompt)
        
        # 构建消息列表
        messages = [{"role": "user", "content": prompt_content}]
        
        # 调用 AI
        client = get_client()
        model_name = get_api_config(AI_PROVIDER).get("model", "qwen-plus")
        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True
        )
        
        full_content = ""
        try:
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_content += content
                    yield content
            
            # 保存对话记录
            session_mgr.add_message("user", prompt)
            session_mgr.add_message("assistant", full_content)
            
            # 生成模式：自动保存文件到 workspace/{agent_id}/outputs/
            file_mgr = FileManager(agent_id)
            import time, re
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            # 清理非法字符：只保留字母、数字、中文和常见符号
            safe_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', prompt[:20])
            filename = f"outputs/{safe_name}_{timestamp}.md"
            save_result = file_mgr.write_file(filename, full_content)
            
            yield f"\n\n[文件已保存到: workspace/{agent_id}/outputs/{safe_name}_{timestamp}.md]"
            mark_provider_success("default")
            
        except Exception as e:
            mark_provider_error("default")
            yield f"\n\n[错误]: {str(e)}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== 公众号文章 ==========

@router.post("/wechat-article")
async def generate_wechat_article(request: ArticleRequest):
    """
    生成公众号文章
    聊天模式：走 /api/agent/chat
    生成模式：基于 Skill 构建提示词，流式返回完整文章
    """
    from fastapi.responses import StreamingResponse
    
    # 构建任务描述和用户输入
    topic = request.topic
    task_desc = (
        f"你是一位专业的公众号内容创作者，擅长撰写高质量、有深度、适合25-40岁旅行者阅读的公众号文章。\n"
        f"文章主题：{topic}\n"
        f"文章分类：{request.category if hasattr(request, 'category') else '知识类（干货）'}\n"
        f"写作要求：\n"
        f"1. 结构清晰，包含引人入胜的开头、充实的主体和有号召力的结尾\n"
        f"2. 语言专业但不晦涩，有温度有观点\n"
        f"3. 适当使用小标题、列表等格式增强可读性\n"
        f"4. 字数要求：{request.length if hasattr(request, 'length') and request.length else 1500}字左右\n"
        f"5. 结合实际案例或经验，让内容更有说服力\n"
        f"6. 结尾需要有明确的行动号召或互动问题\n"
        f"\n请直接生成文章内容，不需要询问任何问题。"
    )
    
    user_input = f"文章主题：{topic}"
    if hasattr(request, 'audience') and request.audience:
        user_input += f"\n目标受众：{request.audience}"
    
    async def generate():
        async for chunk in _call_generate_stream("wechat", user_input, task_desc):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/chat")
async def chat(request: ChatRequest):
    """通用聊天接口（代理到 agent.py）"""
    from fastapi.responses import StreamingResponse
    from core.agent_loader import get_agent_id, AgentLoader
    from core.prompt_builder import PromptBuilder
    
    agent_id = "default"
    
    async def generate():
        try:
            session_mgr = SessionManager(agent_id)
            prompt_builder = PromptBuilder(AgentLoader(agent_id))
            prompt_content = prompt_builder.build_chat_prompt(request.message)
            
            messages = []
            if request.history:
                messages.extend(request.history)
            messages.append({"role": "user", "content": prompt_content})
            
            client = get_client()
            response = await client.chat.completions.create(
                model="qwen-plus",
                messages=messages,
                stream=True
            )
            
            full_content = ""
            try:
                async for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_content += content
                        yield content
                
                session_mgr.add_message("user", request.message)
                session_mgr.add_message("assistant", full_content)
                mark_provider_success("default")
            except Exception as e:
                mark_provider_error("default")
                yield f"\n\n[错误]: {str(e)}"
        except Exception as e:
            yield f"\n\n[错误]: {str(e)}"
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/intelligence")
async def intelligence(request: IntelligenceRequest):
    """情报洞察（联网搜索 + AI 总结）"""
    result = await baidu_search(request.topic)
    return result


@router.post("/xhs-copy")
async def generate_xhs_copy(request: XhsRequest):
    """
    生成小红书文案
    基于 xhs_writer Skill 构建提示词，流式返回文案
    """
    from fastapi.responses import StreamingResponse
    
    product = request.product
    scene = request.scene if hasattr(request, 'scene') and request.scene else ""
    
    task_desc = (
        f"你是一位专业的小红书文案专家，擅长生成吸引眼球、引发共鸣的爆款种草文案。\n"
        f"产品/体验：{product}\n"
        f"使用场景：{scene if scene else '通用场景'}\n"
        f"\n"
        f"写作要求：\n"
        f"1. 标题（15-20字）：使用痛点式、数字式、疑问式或身份认同式技巧\n"
        f"2. 正文（150-200字）：开场情境带入 → 中段卖点突出（2-3个核心卖点，场景化语言） → 结尾互动引导\n"
        f"3. Emoji使用：每段1-2个，风格统一，常用✨💖🏠🌟📍🔥\n"
        f"4. 话题标签：5-8个精准标签，包含必选标签#民宿#长沙旅行和场景标签\n"
        f"5. 第一人称真实体验分享，增强可信度\n"
        f"\n"
        f"请直接生成文案，不需要询问任何问题。"
    )
    
    user_input = f"产品/体验：{product}"
    if scene:
        user_input += f"\n使用场景：{scene}"
    
    async def generate():
        async for chunk in _call_generate_stream("xhs", user_input, task_desc):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/short-video")
async def generate_short_video(request: ShortVideoRequest):
    """
    生成短视频文案/脚本
    基于 Skill 构建提示词，流式返回脚本
    """
    from fastapi.responses import StreamingResponse
    
    theme = request.topic
    style = request.style if hasattr(request, 'style') and request.style else "通用风格"
    duration = request.duration if hasattr(request, 'duration') and request.duration else 60
    
    task_desc = (
        f"你是一位专业的短视频脚本创作者，擅长为抖音/小红书平台创作吸引人的视频脚本。\n"
        f"视频主题：{theme}\n"
        f"视频风格：{style}\n"
        f"视频时长：约{duration}秒\n"
        f"\n"
        f"脚本结构要求：\n"
        f"1. 【开场Hook】（0-5秒）：用强悬念或共鸣点留住观众，如痛点提问或惊人数据\n"
        f"2. 【主体内容】（5-50秒）：\n"
        f"   - 分3-4个镜头/场景呈现\n"
        f"   - 每个镜头标注：画面描述 + 台词/旁白 + 时长\n"
        f"   - 植入2-3个核心卖点\n"
        f"3. 【结尾引导】（最后10秒）：\n"
        f"   - 行动号召：如关注、点赞、评论\n"
        f"   - 引流信息：如评论区见、主页链接\n"
        f"4. 【配乐建议】：推荐适合的音乐风格\n"
        f"5. 【拍摄建议】：简单的运镜和场地建议\n"
        f"\n"
        f"请直接生成完整脚本，不需要询问任何问题。"
    )
    
    user_input = f"视频主题：{theme}\n视频风格：{style}"
    
    async def generate():
        async for chunk in _call_generate_stream("shortvideo", user_input, task_desc):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/poster")
async def generate_poster_prompts(request: PosterRequest):
    """
    生成海报提示词（第一阶段）
    基于海报生成 Skill + AI，将文案拆解为4个维度的提示词
    """
    content = request.content
    ratio = request.image_ratio if hasattr(request, 'image_ratio') and request.image_ratio else "--ar 3:4"
    
    from core.agent_loader import AgentLoader
    from core.prompt_builder import PromptBuilder
    
    try:
        prompt_builder = PromptBuilder(AgentLoader("poster"))
        
        task_desc = (
            f"你是一位专业的海报设计师，擅长将一句文案拆解成专业的图像生成提示词。\n"
            f"用户文案：{content}\n"
            f"海报尺寸：{ratio}\n"
            f"\n"
            f"请从以下4个维度分析并生成提示词：\n"
            f"1. image_description（画面主体描述）：描述海报的主要视觉元素、主体人物或物体、背景场景\n"
            f"2. text_description（文字排版描述）：描述文案中文字的大小、位置、字体风格（标题/副标题/正文）\n"
            f"3. scene_description（场景氛围描述）：描述整体氛围、色调、光线、情绪（如：温馨、梦幻、现代简约）\n"
            f"4. style_description（艺术风格描述）：描述具体的艺术风格（如：油画风、水彩风、扁平插画、摄影写实、国潮风）\n"
            f"\n"
            f"请以 JSON 格式返回结果，格式如下：\n"
            f'{{"image_description": "...", "text_description": "...", "scene_description": "...", "style_description": "..."}}'
        )
        
        user_input = f"海报文案：{content}\n尺寸：{ratio}"
        
        # 构建消息
        prompt_content = prompt_builder.build_generate_prompt(task_desc, user_input)
        messages = [{"role": "user", "content": prompt_content}]
        
        client = get_client()
        response = await client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=False
        )
        
        full_content = response.choices[0].message.content.strip()
        
        # 尝试解析 JSON
        import re
        json_match = re.search(r'\{[\s\S]*\}', full_content)
        if json_match:
            prompts = json.loads(json_match.group())
            return {
                "success": True,
                "prompts": {
                    "image_description": prompts.get("image_description", ""),
                    "text_description": prompts.get("text_description", ""),
                    "scene_description": prompts.get("scene_description", ""),
                    "style_description": prompts.get("style_description", "")
                }
            }
        
        # JSON解析失败，返回原始内容
        return {
            "success": True,
            "prompts": {
                "image_description": full_content,
                "text_description": "",
                "scene_description": "",
                "style_description": ""
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提示词生成失败: {str(e)}")


@router.post("/generate-poster")
async def generate_poster_image(request: dict):
    """生成海报图片（使用图像生成 API）"""
    try:
        from core.poster_generator import create_poster_generator
        
        description = request.get("description", "")
        style = request.get("style", "现代简约")
        image_ratio = request.get("image_ratio", "3:4")
        
        if not description:
            raise HTTPException(status_code=400, detail="请提供海报描述")
        
        generator = create_poster_generator("poster")
        result = await generator.generate_image(
            description=description,
            style=style,
            ratio=image_ratio
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@router.get("/poster/history")
async def get_poster_history(limit: int = 10):
    """获取海报生成历史记录"""
    try:
        from core.poster_generator import create_poster_generator
        
        generator = create_poster_generator("poster")
        history = generator.get_recent_generations(limit=limit)
        
        return {
            "success": True,
            "history": history
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")
