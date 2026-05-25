"""数据模型（Pydantic Schemas）"""
from pydantic import BaseModel, Field
from typing import List, Optional


# ========== 公众号文章生成 ==========
class Audience(BaseModel):
    """目标受众"""
    age: Optional[str] = "25-40"
    occupation: Optional[str] = "旅行者"
    interests: Optional[List[str]] = []
    pain_points: Optional[List[str]] = []


class ArticleRequest(BaseModel):
    """公众号文章生成请求"""
    topic: str
    audience: Optional[Audience] = None
    category: Optional[str] = "知识类（干货）"
    length: Optional[int] = 1500


# ========== 聊天模式 ==========
class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    history: Optional[List[dict]] = None


# ========== 情报洞察 ==========
class IntelligenceRequest(BaseModel):
    """情报洞察请求"""
    topic: str
    focus_areas: Optional[List[str]] = []


# ========== 小红书文案 ==========
class XhsRequest(BaseModel):
    """小红书文案请求"""
    product: str
    scene: Optional[str] = ""


# ========== 短视频文案 ==========
class ShortVideoRequest(BaseModel):
    """短视频文案请求"""
    topic: str
    style: Optional[str] = ""
    duration: Optional[int] = 60


# ========== 海报生成 ==========
class PosterRequest(BaseModel):
    """海报生成请求"""
    content: str
    image_ratio: str = "--ar 3:4"


# ========== 设置 ==========
class SettingsRequest(BaseModel):
    """设置请求"""
    ai_provider: Optional[str] = None
    model: Optional[str] = None
    api_key: Optional[str] = None


# ========== 智能体 ==========
class AgentChatRequest(BaseModel):
    """智能体聊天请求"""
    agent_id: str
    message: str
    mode: str = "chat"  # chat 或 generate
    session_id: Optional[str] = None  # 会话ID，支持多会话
    history: Optional[List[dict]] = None
    enable_search: bool = False  # 是否启用联网搜索


class AgentGenerateRequest(BaseModel):
    """智能体生成请求"""
    task: str = ""  # 兼容前端
    prompt: str = ""  # 兼容后端
    agent_id: str = ""
    mode: str = "generate"
    history: Optional[List[dict]] = None
    
    def __init__(self, **data):
        # 统一字段：前端发 task，后端用 prompt
        if 'task' in data and 'prompt' not in data:
            data['prompt'] = data['task']
        super().__init__(**data)


class AgentInfoRequest(BaseModel):
    """智能体信息请求"""
    agent_id: str


class SaveChatRequest(BaseModel):
    """保存聊天记录请求"""
    messages: list


# ========== 文件操作 ==========
class FileReadRequest(BaseModel):
    """文件读取请求"""
    agent_id: str
    filename: str


class FileWriteRequest(BaseModel):
    """文件写入请求"""
    agent_id: str
    filename: str
    content: str


class FileCreateDocRequest(BaseModel):
    """创建文档请求"""
    agent_id: str
    filename: str
    title: str
    content: str
