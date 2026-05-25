"""
民宿运营智能体矩阵 - 主入口
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "backend"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# 导入配置和路由
from config.settings import HOST, PORT, RELOAD
from api import agent, generation, file, settings, dashboard

# 创建 FastAPI 应用
app = FastAPI(
    title="AI Matrix API",
    description="民宿运营智能体矩阵 - AI Powered Homestay Operations",
    version="1.0.0"
)

# CORS 中间件 - 生产环境应指定具体域名
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:9002").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agent.router, prefix="/api/agent", tags=["智能体"])
app.include_router(generation.router, prefix="/api", tags=["内容生成"])
app.include_router(file.router, prefix="/api/file", tags=["文件操作"])
app.include_router(settings.router, prefix="/api", tags=["系统设置"])
app.include_router(dashboard.router, prefix="/api", tags=["仪表盘"])

# 静态文件目录
web_dir = root_dir / "web"
xhb_gw_dir = root_dir / "xhb-gw"
dashboard_dir = root_dir / "dashboard"
print(f"[静态文件] web目录: {web_dir}")
print(f"[静态文件] xhb-gw目录: {xhb_gw_dir}")
print(f"[静态文件] dashboard目录: {dashboard_dir}")

# HTML页面路由
@app.get("/")
async def serve_index():
    """服务猩伙伴民宿官网首页"""
    file_path = xhb_gw_dir / "index.html"
    return FileResponse(str(file_path))

@app.get("/ai")
async def serve_ai_matrix():
    """服务AI员工矩阵"""
    file_path = web_dir / "index.html"
    return FileResponse(str(file_path))

# xhb-gw 子目录路由
@app.get("/xhb-gw/{filename}")
async def serve_xhb_gw(filename: str):
    """服务xhb-gw静态文件"""
    if filename.endswith('.html'):
        file_path = xhb_gw_dir / filename
    else:
        # 静态资源
        if '/' in filename:
            file_path = xhb_gw_dir / filename
        else:
            file_path = xhb_gw_dir / filename
    
    if file_path.exists():
        media_type = "text/html"
        if filename.endswith('.css'): media_type = "text/css"
        elif filename.endswith('.js'): media_type = "application/javascript"
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')): media_type = "image/*"
        return FileResponse(str(file_path), media_type=media_type)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/ai/manage.html")
async def serve_ai_manage():
    """服务AI下的管理页 - 运营数据看板"""
    file_path = dashboard_dir / "dashboard-v2.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/manage.html")
async def serve_manage():
    """服务管理页 - 运营数据看板"""
    file_path = dashboard_dir / "dashboard-v2.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/index.html")
async def serve_index_html():
    """服务 index.html"""
    file_path = web_dir / "index.html"
    return FileResponse(str(file_path))

@app.get("/agent-template.html")
async def serve_agent_template():
    """服务智能体模板页"""
    file_path = web_dir / "agent-template.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

# 静态资源路由
@app.get("/css/{filename}")
async def serve_css(filename: str):
    """服务CSS文件"""
    file_path = web_dir / "css" / filename
    if file_path.exists():
        return FileResponse(str(file_path), media_type="text/css")
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/js/{filename}")
async def serve_js(filename: str):
    """服务JS文件"""
    file_path = web_dir / "js" / filename
    if file_path.exists():
        return FileResponse(str(file_path), media_type="application/javascript")
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/avatars/{filename}")
async def serve_avatars(filename: str):
    """服务头像文件"""
    file_path = web_dir / "avatars" / filename
    if file_path.exists():
        return FileResponse(str(file_path))
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

# Dashboard 数据文件路由
@app.get("/dashboard/{filename}")
async def serve_dashboard_file(filename: str):
    """服务 dashboard 目录下的数据文件"""
    # 安全检查：只允许特定扩展名
    allowed_exts = ['.json', '.txt', '.xlsx']
    ext = '.' + filename.split('.')[-1] if '.' in filename else ''
    if ext.lower() not in allowed_exts:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="不允许访问此文件类型")

    file_path = dashboard_dir / filename
    if file_path.exists():
        # 根据扩展名设置 content-type
        if filename.endswith('.json'):
            return FileResponse(str(file_path), media_type="application/json")
        elif filename.endswith('.txt'):
            return FileResponse(str(file_path), media_type="text/plain")
        elif filename.endswith('.xlsx'):
            return FileResponse(str(file_path), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return FileResponse(str(file_path))
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not Found")

print("[静态文件] 路由注册完成")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD
    )
