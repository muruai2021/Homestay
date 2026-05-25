"""仪表盘相关 API 路由"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "AI Matrix API is running"}


@router.get("/dashboard")
async def get_dashboard_data():
    """获取仪表盘数据"""
    # 实现逻辑（从 main.py 迁移）
    return {
        "stats": {
            "total_agents": 7,
            "total_conversations": 0,
            "total_files": 0
        },
        "recent_activities": []
    }
