"""AI 客户端管理服务"""
from openai import AsyncOpenAI
from config.api_config import get_api_config
from config.settings import AI_PROVIDER

# 全局客户端缓存
_client_cache = {}
_client_errors = {}


def get_client(provider: str = None) -> AsyncOpenAI:
    """获取 AI 客户端（带容错）"""
    global _client_cache, _client_errors

    # 使用指定的 provider 或默认的 AI_PROVIDER
    target_provider = provider or AI_PROVIDER

    # 检查该 provider 是否连续失败超过3次
    if _client_errors.get(target_provider, 0) >= 3:
        # 尝试其他可用的 provider
        from config.api_config import API_CONFIGS
        for p, config in API_CONFIGS.items():
            if p != target_provider and config["api_key"] and _client_errors.get(p, 0) < 3:
                print(f"切换到备用 AI Provider: {p}")
                target_provider = p
                break

    if target_provider not in _client_cache:
        config = get_api_config(target_provider)
        api_key = config["api_key"]
        if not api_key:
            raise ValueError(f"未设置 {target_provider} 的 API Key，请检查 .env 文件")
        _client_cache[target_provider] = AsyncOpenAI(api_key=api_key, base_url=config["base_url"])

    return _client_cache[target_provider]


def mark_provider_error(provider: str):
    """标记 provider 错误"""
    global _client_errors
    _client_errors[provider] = _client_errors.get(provider, 0) + 1
    # 清除该 provider 的缓存客户端
    if provider in _client_cache:
        del _client_cache[provider]


def mark_provider_success(provider: str):
    """标记 provider 成功，重置错误计数"""
    global _client_errors
    _client_errors[provider] = 0
