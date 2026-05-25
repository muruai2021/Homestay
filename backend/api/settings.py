"""设置相关 API 路由"""
from fastapi import APIRouter
from services.token_tracker import get_token_stats, get_token_records

router = APIRouter()


@router.get("/settings")
async def get_settings():
    """获取设置"""
    return {
        "ai_provider": "qwen",
        "model": "qwen-plus"
    }


@router.post("/settings")
async def update_settings(request: dict):
    """更新设置"""
    # 实现逻辑（从 main.py 迁移）
    return {"success": True, "message": "设置已更新"}


@router.get("/token-stats")
async def get_token_stats_endpoint():
    """获取 Token 统计"""
    return get_token_stats()


@router.get("/token-records")
async def get_token_records_endpoint(limit: int = 50):
    """获取 Token 记录"""
    return {"records": get_token_records(limit)}
