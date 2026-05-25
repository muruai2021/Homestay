"""提示词构建器模块"""
from typing import Optional
from core.agent_loader import AgentLoader


class PromptBuilder:
    """提示词构建器"""
    
    def __init__(self, agent_loader: AgentLoader):
        self.agent_loader = agent_loader
    
    def build_chat_prompt(self, user_input: str) -> str:
        """
        构建聊天模式提示词
        
        Args:
            user_input: 用户输入
        
        Returns:
            格式化的提示词
        """
        system_prompt = self.agent_loader.system_prompt
        
        # 构建聊天提示词
        prompt = f"""{system_prompt}

请根据我的需求进行对话。"""
        
        return prompt
    
    def build_generate_prompt(self, user_input: str, task: Optional[str] = None) -> str:
        """
        构建生成模式提示词
        
        Args:
            user_input: 用户输入
            task: 任务类型（可选）
        
        Returns:
            格式化的提示词
        """
        system_prompt = self.agent_loader.system_prompt
        capabilities = self.agent_loader.capabilities
        
        # 构建生成提示词
        prompt = f"""{system_prompt}

## 任务
{user_input}

## 要求
- 输出内容要完整、专业
- 根据能力范围：{", ".join(capabilities) if capabilities else "通用"}"""
        
        return prompt
    
    def build_with_skill(self, skill_prompt: str) -> str:
        """
        结合 Skill 提示词
        
        Args:
            skill_prompt: Skill 增强内容
        
        Returns:
            完整提示词
        """
        base = self.agent_loader.system_prompt
        
        if skill_prompt:
            return f"""{base}

{skill_prompt}"""
        
        return base
    
    def build_with_context(self, user_input: str, context: dict) -> str:
        """
        结合上下文的提示词
        
        Args:
            user_input: 用户输入
            context: 上下文信息
        
        Returns:
            完整提示词
        """
        prompt_parts = []
        
        # 基础系统提示词
        prompt_parts.append(self.agent_loader.system_prompt)
        
        # 附加上下文
        if context:
            context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])
            prompt_parts.append(f"\n## 上下文\n{context_str}")
        
        # 用户输入
        prompt_parts.append(f"\n## 需求\n{user_input}")
        
        return "\n".join(prompt_parts)