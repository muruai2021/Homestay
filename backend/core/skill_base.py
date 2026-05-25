"""
Skill 模块化框架核心
====================

设计原则：
1. Skill 与 Agent 分离 - Skill 是可复用功能单元
2. 标准化的 SKILL.md 格式 - 统一的技能定义
3. 依赖注入 - Agent 通过配置引用 Skill
4. 模板系统 - 支持 Skill 内部模板复用

目录结构：
----------
skills/                           # 全局 Skill 库
├── _templates/
│   └── SKILL.md                 # Skill 标准模板
├── content/                     # 内容创作类
│   ├── xhs_writer/
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   └── examples/
│   └── wechat_writer/
└── analysis/
    └── data_analyzer/

每个 Agent 的 workspace/
├── agent.md                     # 技能索引（引用 skills/）
├── soul.md                      # 身份定义
└── ...
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


# ============ 路径配置 ============
def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent.parent

def get_skills_root() -> Path:
    """获取全局 Skill 库路径"""
    return get_project_root() / "skills"

def get_agent_skills_dir(agent_id: str) -> Path:
    """获取 Agent 专属 Skills 目录"""
    return get_project_root() / "workspace" / agent_id / "skills"


# ============ Skill 定义 ============
class SkillType(Enum):
    """Skill 类型"""
    CONTENT = "content"           # 内容创作
    ANALYSIS = "analysis"         # 分析推理
    TOOL = "tool"                 # 工具类
    TEMPLATE = "template"          # 模板类


class SkillTrigger(Enum):
    """触发方式"""
    KEYWORD = "keyword"           # 关键词触发
    INTENT = "intent"            # 意图识别触发
    CHAIN = "chain"             # 任务链调用
    MANUAL = "manual"            # 手动调用


@dataclass
class SkillConfig:
    """Skill 配置"""
    name: str
    skill_id: str
    skill_type: SkillType
    trigger: SkillTrigger
    description: str
    
    # 触发条件
    keywords: List[str] = field(default_factory=list)  # 关键词列表
    intent_patterns: List[str] = field(default_factory=list)  # 意图模式
    
    # 执行配置
    enabled: bool = True
    priority: int = 0  # 优先级，数字越大越优先
    
    # 资源路径
    skill_path: Path = None
    
    # 模板和示例
    templates: Dict[str, str] = field(default_factory=dict)
    examples: List[Dict[str, str]] = field(default_factory=list)
    
    # Skill 内部配置
    config: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def templates_dir(self) -> Path:
        """模板目录"""
        return self.skill_path / "templates" if self.skill_path else None
    
    @property
    def examples_dir(self) -> Path:
        """示例目录"""
        return self.skill_path / "examples" if self.skill_path else None


# ============ Skill 加载器 ============
class SkillLoader:
    """
    Skill 加载器 - 统一管理所有 Skill 的加载和访问
    
    支持两层 Skill：
    1. 全局 Skill：skills/ 目录，所有 Agent 共享
    2. Agent 专属 Skill：workspace/{agent_id}/skills/
    """
    
    # Skill 标准文件名
    SKILL_MANIFEST = "SKILL.md"
    
    def __init__(self, agent_id: str = None):
        self.agent_id = agent_id
        self.project_root = get_project_root()
        self.global_skills_root = get_skills_root()
        
        # 加载的 Skill 缓存
        self._skills: Dict[str, SkillConfig] = {}
        self._agent_skills_dir = get_agent_skills_dir(agent_id) if agent_id else None
        
        # 扫描和加载
        self._scan_skills()
    
    def _scan_skills(self):
        """扫描并加载所有可用 Skill"""
        # 1. 加载全局 Skills
        if self.global_skills_root.exists():
            self._scan_skill_tree(self.global_skills_root, is_global=True)
        
        # 2. 加载 Agent 专属 Skills
        if self._agent_skills_dir and self._agent_skills_dir.exists():
            self._scan_skill_tree(self._agent_skills_dir, is_global=False)
    
    def _scan_skill_tree(self, root_dir: Path, is_global: bool = True):
        """
        递归扫描 Skill 目录树
        - 跳过以 _ 开头的目录
        - 在每个非 _ 目录中查找 SKILL.md
        """
        if not root_dir.exists():
            return
        
        for item in root_dir.iterdir():
            if item.is_dir():
                if item.name.startswith("_"):
                    # 跳过以 _ 开头的目录（如 _templates）
                    continue
                
                skill_file = item / self.SKILL_MANIFEST
                if skill_file.exists():
                    # 直接找到 SKILL.md，加载这个 Skill
                    skill_config = self._load_skill_manifest(skill_file, item, is_global)
                    if skill_config:
                        if skill_config.skill_id not in self._skills or not is_global:
                            self._skills[skill_config.skill_id] = skill_config
                else:
                    # 没有 SKILL.md，递归进入子目录
                    self._scan_skill_tree(item, is_global)
            elif item.is_file() and item.name == "marketplace.json":
                # marketplace.json 用于 Skill 市场索引（可选）
                pass
    
    def _load_skill_dir(self, skill_dir: Path, is_global: bool = True):
        """加载目录下的所有 Skill（兼容方法）"""
        self._scan_skill_tree(skill_dir, is_global)
    
    def _load_skill_manifest(self, manifest_path: Path, skill_dir: Path, is_global: bool) -> Optional[SkillConfig]:
        """加载单个 Skill 的 SKILL.md"""
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 YAML 头部元数据
            metadata = self._parse_yaml_frontmatter(content)
            
            if not metadata:
                return None
            
            skill_id = metadata.get("id", skill_dir.name)
            
            # 确定 Skill 类型
            skill_type_str = metadata.get("type", "content").lower()
            skill_type = SkillType.CONTENT
            for st in SkillType:
                if st.value == skill_type_str:
                    skill_type = st
                    break
            
            # 确定触发方式
            trigger_str = metadata.get("trigger", "keyword").lower()
            trigger = SkillTrigger.KEYWORD
            for tg in SkillTrigger:
                if tg.value == trigger_str:
                    trigger = tg
                    break
            
            skill_config = SkillConfig(
                name=metadata.get("name", skill_id),
                skill_id=skill_id,
                skill_type=skill_type,
                trigger=trigger,
                description=metadata.get("description", ""),
                keywords=metadata.get("keywords", []),
                intent_patterns=metadata.get("intent_patterns", []),
                enabled=metadata.get("enabled", True),
                priority=metadata.get("priority", 0),
                skill_path=skill_dir,
                config=metadata.get("config", {})
            )
            
            # 加载模板
            skill_config.templates = self._load_templates(skill_config.templates_dir)
            
            # 加载示例
            skill_config.examples = self._load_examples(skill_config.examples_dir)
            
            return skill_config
            
        except Exception as e:
            print(f"[SkillLoader] 加载 Skill manifest 失败 {manifest_path}: {e}")
            return None
    
    def _parse_yaml_frontmatter(self, content: str) -> Optional[Dict]:
        """解析 YAML 头部元数据"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    return yaml.safe_load(parts[1]) or {}
                except:
                    return None
        return None
    
    def _load_templates(self, templates_dir: Path) -> Dict[str, str]:
        """加载 Skill 模板"""
        templates = {}
        if templates_dir and templates_dir.exists():
            for tmpl_file in templates_dir.glob("*.md"):
                try:
                    with open(tmpl_file, 'r', encoding='utf-8') as f:
                        templates[tmpl_file.stem] = f.read()
                except Exception as e:
                    print(f"[SkillLoader] 加载模板失败 {tmpl_file}: {e}")
        return templates
    
    def _load_examples(self, examples_dir: Path) -> List[Dict[str, str]]:
        """加载 Skill 示例"""
        examples = []
        if examples_dir and examples_dir.exists():
            for example_file in examples_dir.glob("*.md"):
                try:
                    with open(example_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 解析示例元数据
                    metadata = self._parse_yaml_frontmatter(content)
                    if metadata:
                        examples.append({
                            "title": metadata.get("title", example_file.stem),
                            "input": metadata.get("input", ""),
                            "output": content.replace(content[:content.find("---")+3] if "---" in content else 0, "").strip() if "---" in content else content
                        })
                    else:
                        examples.append({
                            "title": example_file.stem,
                            "input": "",
                            "output": content
                        })
                except Exception as e:
                    print(f"[SkillLoader] 加载示例失败 {example_file}: {e}")
        return examples
    
    def get_skill(self, skill_id: str) -> Optional[SkillConfig]:
        """获取指定 Skill"""
        return self._skills.get(skill_id)
    
    def get_all_skills(self) -> List[SkillConfig]:
        """获取所有已加载的 Skill"""
        return list(self._skills.values())
    
    def get_skills_by_type(self, skill_type: SkillType) -> List[SkillConfig]:
        """按类型获取 Skill"""
        return [s for s in self._skills.values() if s.skill_type == skill_type]
    
    def match_skills(self, text: str) -> List[SkillConfig]:
        """根据输入文本匹配相关 Skill"""
        matched = []
        text_lower = text.lower()
        
        for skill in self._skills.values():
            if not skill.enabled:
                continue
            
            # 关键词匹配
            for kw in skill.keywords:
                if kw.lower() in text_lower:
                    matched.append((skill, 1.0))
                    break
            
            # 意图模式匹配
            for pattern in skill.intent_patterns:
                if pattern.lower() in text_lower:
                    matched.append((skill, 0.8))
                    break
        
        # 按优先级排序
        matched.sort(key=lambda x: (x[1], x[0].priority), reverse=True)
        return [s[0] for s in matched]
    
    def list_skill_ids(self) -> List[str]:
        """列出所有可用 Skill ID"""
        return list(self._skills.keys())


# ============ Skill 执行器 ============
class SkillExecutor:
    """
    Skill 执行器 - 负责 Skill 的实际执行
    """
    
    def __init__(self, skill: SkillConfig):
        self.skill = skill
    
    def get_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """
        获取 Skill 的系统提示词
        
        Args:
            context: 执行上下文，包含 user_input, agent_info 等
            
        Returns:
            完整的系统提示词
        """
        if not self.skill.skill_path:
            return ""
        
        # 读取 SKILL.md 内容作为技能定义
        skill_md_path = self.skill.skill_path / "SKILL.md"
        if skill_md_path.exists():
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 移除 YAML 头部，只保留正文
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    content = parts[2] if len(parts) >= 3 else ""
                return content.strip()
        
        return ""
    
    def get_template(self, template_name: str) -> Optional[str]:
        """获取指定模板"""
        return self.skill.templates.get(template_name)
    
    def get_example(self, index: int = 0) -> Optional[Dict[str, str]]:
        """获取示例"""
        if 0 <= index < len(self.skill.examples):
            return self.skill.examples[index]
        return None


# ============ Skill 组合器（用于 Agent） ============
class SkillChain:
    """
    Skill 链 - 组合多个 Skill 完成复杂任务
    
    使用方式：
    chain = SkillChain(agent_id="xhs")
    chain.add_skill("xhs_writer")
    chain.add_skill("trend_detector")  # 自动识别数据
    result = chain.execute(user_input)
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.loader = SkillLoader(agent_id)
        self.skills: List[SkillConfig] = []
        self.skill_executors: List[SkillExecutor] = []
    
    def add_skill(self, skill_id: str):
        """添加 Skill 到链"""
        skill = self.loader.get_skill(skill_id)
        if skill:
            self.skills.append(skill)
            self.skill_executors.append(SkillExecutor(skill))
    
    def build_prompt(self, user_input: str, mode: str = "chat") -> str:
        """
        构建组合 Skill 后的完整提示词
        
        Args:
            user_input: 用户输入
            mode: chat 或 generate
            
        Returns:
            完整提示词
        """
        prompt_parts = []
        
        # 1. 加载 Agent 自身配置（延迟导入避免循环）
        import sys
        from pathlib import Path
        # skill_base.py 在 backend/core/，agent_loader.py 在 core/
        project_root = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(project_root))
        from core.agent_loader import AgentLoader
        agent_loader = AgentLoader(self.agent_id)
        
        # 身份定义
        soul = agent_loader.load_file('soul')
        if soul:
            prompt_parts.append(f"# 身份定义\n{soul}")
        
        # 业务知识
        user_kb = agent_loader.load_file('user')
        if user_kb:
            prompt_parts.append(f"# 业务知识\n{user_kb}")
        
        # 对话上下文
        sessions = agent_loader.load_file('sessions')
        if sessions:
            prompt_parts.append(f"# 对话上下文\n{sessions}")
        
        # 2. 添加 Skill 技能
        if self.skills:
            skill_sections = []
            for i, (skill, executor) in enumerate(zip(self.skills, self.skill_executors)):
                skill_content = executor.get_system_prompt()
                if skill_content:
                    skill_sections.append(f"## 技能 {i+1}: {skill.name}\n{skill_content}")
            
            if skill_sections:
                prompt_parts.append(f"# 可用技能\n\n" + "\n\n".join(skill_sections))
        
        # 3. 用户输入
        prompt_parts.append(f"\n# 用户输入\n{user_input}")
        
        return "\n\n".join(prompt_parts)
    
    def auto_match_skills(self, user_input: str) -> int:
        """
        根据用户输入自动匹配 Skill
        
        Returns:
            匹配到的 Skill 数量
        """
        matched = self.loader.match_skills(user_input)
        for skill in matched[:3]:  # 最多匹配3个
            if skill not in self.skills:
                self.add_skill(skill.skill_id)
        return len(self.skills)
