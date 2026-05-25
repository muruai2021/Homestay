"""会话管理器模块 - 支持 JSON 格式、多会话、时间戳"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 基础路径
BASE_DIR = Path(__file__).parent.parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"


class SessionManager:
    """会话管理器 - 支持多会话、JSON格式完整记录"""

    # 批量写入间隔（秒）
    _default_write_interval = 1.0

    def __init__(self, agent_name: str, session_id: str = None):
        self.agent_name = agent_name
        self.agent_workspace = WORKSPACE_DIR / agent_name
        self.sessions_dir = self.agent_workspace / "sessions"
        self.session_id = session_id or str(uuid.uuid4())
        self._ensure_workspace()
        # 实例级批量写入配置
        self._pending_writes: Dict[str, tuple] = {}  # session_id -> (session_data, timestamp)
        self._write_interval = self._default_write_interval
        self._last_write_time: Dict[str, float] = {}  # session_id -> last flush time
    
    def _ensure_workspace(self):
        """确保工作空间和会话目录存在"""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def session_file(self) -> Path:
        """当前会话文件路径"""
        return self.sessions_dir / f"{self.session_id}.json"
    
    def _load_session(self) -> Dict:
        """加载当前会话"""
        if self.session_file.exists():
            with open(self.session_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "session_id": self.session_id,
            "agent_name": self.agent_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": []
        }
    
    def _save_session(self, session_data: Dict, immediate: bool = False):
        """保存当前会话

        Args:
            session_data: 会话数据
            immediate: 是否立即写入（默认False，使用批量写入）
        """
        import time
        session_data["updated_at"] = datetime.now().isoformat()
        session_id = session_data.get("session_id", self.session_id)

        # 批量写入逻辑：只有超过写入间隔才真正写入磁盘
        current_time = time.time()
        last_write = self._last_write_time.get(session_id, 0)

        if immediate or (current_time - last_write) >= self._write_interval:
            # 立即写入
            with open(self.session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            self._last_write_time[session_id] = current_time
        else:
            # 记录待写入数据，下次批量写入
            self._pending_writes[session_id] = (session_data, current_time)

    def flush_pending_writes(self):
        """强制写入所有待处理的会话数据"""
        for session_id, (session_data, timestamp) in list(self._pending_writes.items()):
            session_file = self.sessions_dir / f"{session_id}.json"
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            self._last_write_time[session_id] = timestamp
        self._pending_writes.clear()
    
    def add_message(self, role: str, content: str):
        """
        添加对话消息
        
        Args:
            role: 角色 ("user" 或 "assistant")
            content: 消息内容
        """
        session_data = self._load_session()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        session_data["messages"].append(message)
        self._save_session(session_data)
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """
        获取当前会话历史
        
        Args:
            limit: 返回条数限制
        
        Returns:
            消息历史列表
        """
        session_data = self._load_session()
        messages = session_data.get("messages", [])
        
        # 只返回最近 limit 条
        return messages[-limit:] if len(messages) > limit else messages
    
    def get_messages_for_api(self, limit: int = 10) -> List[Dict]:
        """
        获取适合 API 格式的消息历史
        
        Args:
            limit: 返回条数限制
        
        Returns:
            格式化的消息列表 [{role: "user"/"assistant", content: "..."}]
        """
        messages = self.get_history(limit)
        # 直接返回 role + content 格式
        return [{"role": m["role"], "content": m["content"]} for m in messages]
    
    def clear_history(self):
        """清除当前会话历史"""
        session_data = self._load_session()
        session_data["messages"] = []
        self._save_session(session_data)
    
    def list_sessions(self) -> List[Dict]:
        """
        列出所有会话
        
        Returns:
            会话列表（按更新时间倒序）
        """
        sessions = []
        
        if not self.sessions_dir.exists():
            return sessions
        
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sessions.append({
                        "session_id": data.get("session_id"),
                        "created_at": data.get("created_at"),
                        "updated_at": data.get("updated_at"),
                        "message_count": len(data.get("messages", [])),
                        "last_message": data["messages"][-1]["content"][:50] if data.get("messages") else ""
                    })
            except Exception:
                continue
        
        # 按更新时间倒序
        sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return sessions
    
    def delete_session(self, session_id: str):
        """删除指定会话"""
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()
    
    @staticmethod
    def get_all_sessions_count(agent_name: str) -> int:
        """获取指定 Agent 的所有会话数量"""
        workspace = WORKSPACE_DIR / agent_name / "sessions"
        if not workspace.exists():
            return 0
        return len(list(workspace.glob("*.json")))
