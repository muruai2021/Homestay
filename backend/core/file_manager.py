"""文件管理器模块"""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List


# 基础路径
BASE_DIR = Path(__file__).parent.parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"


class FileManager:
    """文件管理器"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.agent_workspace = WORKSPACE_DIR / agent_name
        self.outputs_dir = self.agent_workspace / "outputs"
        self._ensure_workspace()
    
    def _ensure_workspace(self):
        """确保工作空间存在"""
        self.agent_workspace.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def read_file(self, filename: str) -> str:
        """
        读取文件
        
        Args:
            filename: 文件名
        
        Returns:
            文件内容
        """
        file_path = self.outputs_dir / filename
        
        if not file_path.exists():
            # 尝试在工作空间根目录查找
            file_path = self.agent_workspace / filename
        
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        
        raise FileNotFoundError(f"文件不存在: {filename}")
    
    def write_file(self, filename: str, content: str):
        """
        写入文件
        
        Args:
            filename: 文件名
            content: 文件内容
        """
        file_path = self.outputs_dir / filename
        
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"[文件] 已保存: {file_path}")
    
    def create_document(self, filename: str, title: str, content: str):
        """
        创建文档
        
        Args:
            filename: 文件名
            title: 文档标题
            content: 文档内容
        """
        # Markdown 文档格式
        doc_content = f"""# {title}

{content}

---
*由 AI Matrix 生成 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        
        # 确保是 .md 扩展名
        if not filename.endswith(".md"):
            filename = filename + ".md"
        
        self.write_file(filename, doc_content)
    
    def list_files(self, pattern: str = "*") -> List[str]:
        """
        列出文件
        
        Args:
            pattern: 文件名模式
        
        Returns:
            文件列表
        """
        files = list(self.outputs_dir.glob(pattern))
        return [f.name for f in files if f.is_file()]
    
    def delete_file(self, filename: str) -> bool:
        """
        删除文件
        
        Args:
            filename: 文件名
        
        Returns:
            是否成功
        """
        file_path = self.outputs_dir / filename
        
        if file_path.exists():
            file_path.unlink()
            return True
        
        return False
    
    def get_file_info(self, filename: str) -> dict:
        """
        获取文件信息
        
        Args:
            filename: 文件名
        
        Returns:
            文件信息字典
        """
        file_path = self.outputs_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {filename}")
        
        stat = file_path.stat()
        
        return {
            "name": filename,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }