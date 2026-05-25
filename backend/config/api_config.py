"""API 配置模块"""
from config.settings import DEEPSEEK_API_KEY, DASHSCOPE_API_KEY, MINIMAX_API_KEY, AI_PROVIDER
import os

# API 配置
API_CONFIGS = {
    "deepseek": {
        "api_key": DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat"
    },
    "qwen": {
        "api_key": DASHSCOPE_API_KEY,
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus"
    },
    "qwen_image": {
        "api_key": DASHSCOPE_API_KEY,
        "image_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation"
    },
    "minimax": {
        "api_key": MINIMAX_API_KEY,
        "base_url": "https://api.minimaxi.com/v1",
        "model": "image-01"
    },
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo"
    }
}

def get_api_config(provider: str = None) -> dict:
    """获取 API 配置"""
    target = provider or AI_PROVIDER
    return API_CONFIGS.get(target, API_CONFIGS["qwen"])