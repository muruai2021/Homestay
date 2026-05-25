"""文件操作 API 路由"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from models.schemas import FileReadRequest, FileWriteRequest, FileCreateDocRequest
from core.file_manager import FileManager
from core.agent_loader import get_agent_id
import os
import json
from datetime import datetime
from pathlib import Path

router = APIRouter()

# 文件上传目录
UPLOAD_DIR = Path(__file__).parent.parent.parent / "workspace" / "民宿服务小助手"


@router.post("/read")
async def read_file(request: FileReadRequest):
    """读取文件"""
    try:
        agent_name = get_agent_id(request.agent_id)
        file_mgr = FileManager(agent_name)
        content = file_mgr.read_file(request.filename)
        return {"success": True, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/write")
async def write_file(request: FileWriteRequest):
    """写入文件"""
    try:
        agent_name = get_agent_id(request.agent_id)
        file_mgr = FileManager(agent_name)
        file_mgr.write_file(request.filename, request.content)
        return {"success": True, "message": "文件已保存"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-doc")
async def create_document(request: FileCreateDocRequest):
    """创建文档"""
    try:
        agent_name = get_agent_id(request.agent_id)
        file_mgr = FileManager(agent_name)
        file_mgr.create_document(request.filename, request.title, request.content)
        return {"success": True, "message": "文档已创建"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_id}/list")
async def list_files(agent_id: str):
    """列出文件"""
    try:
        agent_name = get_agent_id(agent_id)
        file_mgr = FileManager(agent_name)
        files = file_mgr.list_files()
        return {"success": True, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_file(
    agent_id: str = "knowledge",
    category: str = "其他资料",
    file: UploadFile = File(...)
):
    """
    上传文件并转换为 Markdown 格式
    
    - agent_id: 智能体ID（固定为 knowledge）
    - category: 分类（政策文件/运营手册/培训资料/其他资料）
    - file: 上传的文件（PDF/Word/TXT/MD）
    """
    try:
        # 验证文件格式
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return {
                "success": False,
                "error": f"不支持的文件格式，仅支持: {', '.join(allowed_extensions)}"
            }
        
        # 检查文件大小（50MB 限制）
        contents = await file.read()
        if len(contents) > 50 * 1024 * 1024:
            return {"success": False, "error": "文件大小超过 50MB 限制"}
        
        # 重置文件指针
        await file.seek(0)
        
        # 确定保存路径
        knowledge_dir = UPLOAD_DIR / "knowledge" / category
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(file.filename)[0]
        md_filename = f"{timestamp}_{base_name}.md"
        md_path = knowledge_dir / md_filename
        
        # 读取并转换内容
        content = contents.decode('utf-8', errors='ignore')
        
        # 简单处理：如果是文本/TXT/MD，直接保存
        if file_ext in ['.txt', '.md']:
            markdown_content = content
        else:
            # 复杂格式暂存为文本，后续可扩展 PDF/Word 解析
            markdown_content = f"""# {base_name}

> 来源文件: {file.filename}
> 上传时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> 分类: {category}

---

{content}
"""
        
        # 保存 Markdown 文件
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # 更新 metadata.json
        metadata_path = UPLOAD_DIR / "knowledge" / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        else:
            metadata = {"created_at": datetime.now().strftime("%Y-%m-%d"), "categories": [], "documents": []}
        
        # 添加文档记录
        metadata["documents"].append({
            "filename": md_filename,
            "original_name": file.filename,
            "original_format": file_ext,
            "category": category,
            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "size": len(contents)
        })
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return {
            "success": True,
            "message": f"文件已成功上传并转换为 Markdown",
            "filename": md_filename,
            "category": category,
            "size": len(contents),
            "path": str(md_path.relative_to(UPLOAD_DIR.parent.parent))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge/list")
async def list_knowledge():
    """列出知识库中的所有文档"""
    try:
        metadata_path = UPLOAD_DIR / "knowledge" / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            return {"success": True, "data": metadata}
        return {"success": True, "data": {"documents": [], "categories": []}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge/{category}")
async def get_knowledge_by_category(category: str):
    """获取指定分类下的所有文档"""
    try:
        knowledge_dir = UPLOAD_DIR / "knowledge" / category
        if not knowledge_dir.exists():
            return {"success": True, "documents": []}
        
        files = []
        for f in knowledge_dir.iterdir():
            if f.suffix == '.md':
                files.append({
                    "name": f.name,
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return {"success": True, "category": category, "documents": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
