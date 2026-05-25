"""智能体加载器模块 - 上下文组合: 系统提示词 + Skills提示词 + 会话记录 + 用户输入"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, List, Tuple

# 基础路径
BASE_DIR = Path(__file__).parent.parent.parent
AGENTS_DIR = BASE_DIR / "skills" / "agents"
WORKSPACE_DIR = BASE_DIR / "workspace"


# 智能体映射表 (agent_id -> workspace目录名)
# 目录已统一使用英文命名
AGENT_MAP = {
    "chat": "chat",           # 运营助手（内部使用）
    "poster": "poster",
    "xhs": "xhs",
    "shortvideo": "shortvideo",   # 短视频方案
    "short_video": "shortvideo",   # 兼容旧ID
    "wechat": "wechat",
    "intelligence": "intelligence",
    "knowledge": "knowledge",
    "customer": "customer",   # 官网客服（接待客户）
}


def get_agent_id(agent_id: str) -> str:
    """
    根据 agent_id 返回 agent_name
    
    Args:
        agent_id: 智能体ID (如 "chat", "poster" 等)
    
    Returns:
        智能体名称
    """
    return AGENT_MAP.get(agent_id, "通用智能体")


class AgentLoader:
    """智能体上下文加载器 - 完整上下文组合"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.workspace_dir = WORKSPACE_DIR / agent_name
        
        # 查找实际目录（可能有中文别名）
        self._actual_dir = self._find_actual_dir()
        
        if self._actual_dir:
            self.workspace_dir = self._actual_dir
        
        # 文件路径
        self.soul_md_path = self.workspace_dir / "soul.md"
        self.agent_md_path = self.workspace_dir / "agent.md"
        self.agents_md_path = self.workspace_dir / "AGENTS.md"
        self.skills_dir = self.workspace_dir / "skills"
        
        # 加载配置
        self.config = self._load_config()
    
    def _find_actual_dir(self) -> Optional[Path]:
        """查找实际的工作目录（处理中文别名）"""
        if not WORKSPACE_DIR.exists():
            return None
        
        # 尝试直接匹配
        if (WORKSPACE_DIR / self.agent_name).exists():
            return WORKSPACE_DIR / self.agent_name
        
        # 遍历查找相似目录名
        agent_name_lower = self.agent_name.lower()
        for d in WORKSPACE_DIR.iterdir():
            if d.is_dir() and agent_name_lower in d.name.lower():
                return d
        
        return None
    
    # ==================== 1. 系统提示词加载 ====================
    
    def _load_system_prompt(self) -> str:
        """加载系统提示词 - 优先级: soul.md > agent.md > AGENTS.md"""
        # 1.1 尝试加载 soul.md
        if self.soul_md_path.exists():
            try:
                with open(self.soul_md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    print(f"[AgentLoader] 已加载 soul.md: {self.agent_name}")
                    return content
            except Exception as e:
                print(f"[AgentLoader] 加载 soul.md 失败: {e}")
        
        # 1.2 尝试加载 agent.md
        if self.agent_md_path.exists():
            try:
                with open(self.agent_md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    print(f"[AgentLoader] 已加载 agent.md: {self.agent_name}")
                    return content
            except Exception as e:
                print(f"[AgentLoader] 加载 agent.md 失败: {e}")
        
        # 1.3 尝试加载 AGENTS.md (取其中的系统提示词部分)
        if self.agents_md_path.exists():
            try:
                with open(self.agents_md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 提取系统提示词部分（简单处理：跳过头部信息）
                    lines = content.split('\n')
                    prompt_lines = []
                    capture = False
                    for line in lines:
                        if line.startswith('## 上下文加载') or line.startswith('# '):
                            if prompt_lines:
                                break
                            capture = True
                            continue
                        if capture:
                            prompt_lines.append(line)
                    if prompt_lines:
                        print(f"[AgentLoader] 已从 AGENTS.md 提取系统提示词: {self.agent_name}")
                        return '\n'.join(prompt_lines).strip()
            except Exception as e:
                print(f"[AgentLoader] 加载 AGENTS.md 失败: {e}")
        
        return ""
    
    # ==================== 2. Skills 提示词加载 ====================
    
    def _load_skills_prompt(self) -> str:
        """加载 Skills 提示词 - 只加载主 SKILL.md，避免全量加载"""
        if not self.skills_dir.exists():
            return ""
        
        # 只加载根目录的 SKILL.md，不递归子目录
        main_skill = self.skills_dir / "SKILL.md"
        if main_skill.exists():
            try:
                with open(main_skill, "r", encoding="utf-8") as f:
                    content = f.read()
                    print(f"[AgentLoader] 已加载 Skills: {self.agent_name}")
                    return content
            except Exception as e:
                print(f"[AgentLoader] 加载 SKILL.md 失败: {e}")
        
        return ""
    
    # ==================== 3. 会话记录加载 ====================
    
    def _load_session_history(self, max_turns: int = 10) -> str:
        """加载会话历史 - 优先级: .history.json > sessions.md > sessions.json"""
        history_content = []
        
        # 3.1 尝试 .history.json
        history_json = self.workspace_dir / ".history.json"
        if history_json.exists():
            try:
                with open(history_json, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    if isinstance(history, list) and history:
                        # 取最近 max_turns 轮对话
                        recent = history[-max_turns:] if len(history) > max_turns else history
                        for item in recent:
                            if isinstance(item, dict):
                                role = item.get('role', 'user')
                                content = item.get('content', '')
                                history_content.append(f"{role}: {content}")
                        print(f"[AgentLoader] 已加载 .history.json: {len(recent)} 条记录")
            except Exception as e:
                print(f"[AgentLoader] 加载 .history.json 失败: {e}")
        
        # 3.2 尝试 sessions.md
        if not history_content:
            sessions_md = self.workspace_dir / "sessions.md"
            if sessions_md.exists():
                try:
                    with open(sessions_md, "r", encoding="utf-8") as f:
                        content = f.read()
                        # 取最后 2000 字符
                        history_content.append(content[-2000:] if len(content) > 2000 else content)
                        print(f"[AgentLoader] 已加载 sessions.md")
                except Exception as e:
                    print(f"[AgentLoader] 加载 sessions.md 失败: {e}")
        
        # 3.3 尝试 sessions.json
        if not history_content:
            sessions_json = self.workspace_dir / "sessions.json"
            if sessions_json.exists():
                try:
                    with open(sessions_json, "r", encoding="utf-8") as f:
                        history = json.load(f)
                        if isinstance(history, list) and history:
                            recent = history[-max_turns:] if len(history) > max_turns else history
                            for item in recent:
                                if isinstance(item, dict):
                                    role = item.get('role', 'user')
                                    content = item.get('content', '')
                                    history_content.append(f"{role}: {content}")
                            print(f"[AgentLoader] 已加载 sessions.json: {len(recent)} 条记录")
                except Exception as e:
                    print(f"[AgentLoader] 加载 sessions.json 失败: {e}")
        
        if history_content:
            return "\n\n".join(history_content)
        return ""
    
    # ==================== 完整上下文组合 ====================
    
    def get_full_context(self, user_input: str = "", session_history: List[Dict] = None) -> str:
        """
        获取完整上下文 - 核心方法
        
        上下文组合逻辑:
        ```
        完整上下文 = 系统提示词 + Skills提示词 + 会话记录 + 用户输入
        ```
        
        Args:
            user_input: 用户当前输入
            session_history: 会话历史（可选，会覆盖文件加载）
        
        Returns:
            格式化的完整上下文
        """
        context_parts = []
        
        # 1. 系统提示词 (最高优先级)
        system_prompt = self._load_system_prompt()
        if system_prompt:
            context_parts.append(f"【系统提示词】\n{system_prompt}")
        
        # 2. Skills 提示词
        skills_prompt = self._load_skills_prompt()
        if skills_prompt:
            context_parts.append(f"\n【技能提示词】\n{skills_prompt}")
        
        # 3. 会话记录
        if session_history:
            # 使用传入的会话历史
            history_parts = []
            for item in session_history[-10:]:  # 取最近10轮
                role = item.get('role', 'user')
                content = item.get('content', '')
                history_parts.append(f"{role}: {content}")
            if history_parts:
                context_parts.append(f"\n【最近对话记录】\n" + "\n".join(history_parts))
        else:
            # 从文件加载会话历史
            session_record = self._load_session_history()
            if session_record:
                context_parts.append(f"\n【历史对话记录】\n{session_record}")
        
        # 4. 用户输入 (最后)
        if user_input:
            context_parts.append(f"\n【当前任务】\n{user_input}")
        
        return "\n\n".join(context_parts)
    
    # ==================== 兼容旧接口 ====================
    
    def _load_config(self) -> Dict:
        """加载智能体配置"""
        config_file = AGENTS_DIR / f"{self.agent_name}.json"
        
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        return {
            "name": self.agent_name,
            "description": "AI员工",
            "system_prompt": self._load_system_prompt(),
            "capabilities": ["对话", "生成"],
            "constraints": []
        }
    
    @property
    def system_prompt(self) -> str:
        """获取系统提示词（兼容旧接口）"""
        return self._load_system_prompt()
    
    @property
    def description(self) -> str:
        """获取描述"""
        return self.config.get("description", "")
    
    @property
    def capabilities(self) -> List[str]:
        """获取能力列表"""
        return self.config.get("capabilities", [])
    
    @property
    def constraints(self) -> List[str]:
        """获取约束列表"""
        return self.config.get("constraints", [])
    
    def get_prompt_with_context(self, user_input: str = "") -> str:
        """兼容旧接口"""
        return self.get_full_context(user_input)
