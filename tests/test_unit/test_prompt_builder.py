"""PromptBuilder 单元测试"""
import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from core.prompt_builder import PromptBuilder


class MockAgentLoader:
    """Mock AgentLoader for testing"""

    def __init__(self):
        self._system_prompt = "You are a helpful AI assistant."
        self._capabilities = ["capability1", "capability2"]

    @property
    def system_prompt(self):
        return self._system_prompt

    @property
    def capabilities(self):
        return self._capabilities


class TestPromptBuilderBasics:
    """PromptBuilder 基础功能测试"""

    @pytest.fixture
    def mock_loader(self):
        return MockAgentLoader()

    @pytest.fixture
    def builder(self, mock_loader):
        return PromptBuilder(mock_loader)

    def test_init(self, mock_loader):
        """测试初始化"""
        builder = PromptBuilder(mock_loader)
        assert builder.agent_loader == mock_loader

    def test_build_chat_prompt(self, builder, mock_loader):
        """测试构建聊天提示词"""
        result = builder.build_chat_prompt("Hello")
        assert mock_loader.system_prompt in result
        assert "对话" in result

    def test_build_chat_prompt_returns_string(self, builder):
        """测试 build_chat_prompt 返回字符串"""
        result = builder.build_chat_prompt("test input")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_build_generate_prompt(self, builder, mock_loader):
        """测试构建生成模式提示词"""
        result = builder.build_generate_prompt("Write a story", "creative")
        assert mock_loader.system_prompt in result
        assert "Write a story" in result
        assert "任务" in result
        assert "要求" in result

    def test_build_generate_prompt_with_capabilities(self, builder):
        """测试生成提示词包含能力描述"""
        result = builder.build_generate_prompt("Write a story")
        assert "capability1" in result
        assert "capability2" in result

    def test_build_with_skill(self, builder, mock_loader):
        """测试结合 Skill 提示词"""
        skill_prompt = "Additional skill instructions"
        result = builder.build_with_skill(skill_prompt)
        assert mock_loader.system_prompt in result
        assert skill_prompt in result

    def test_build_with_skill_empty(self, builder, mock_loader):
        """测试空 Skill 提示词"""
        result = builder.build_with_skill("")
        assert result == mock_loader.system_prompt

    def test_build_with_context(self, builder, mock_loader):
        """测试结合上下文的提示词"""
        context = {"key1": "value1", "key2": "value2"}
        result = builder.build_with_context("User request", context)

        assert mock_loader.system_prompt in result
        assert "User request" in result
        assert "key1: value1" in result
        assert "key2: value2" in result
        assert "上下文" in result
        assert "需求" in result

    def test_build_with_context_empty(self, builder, mock_loader):
        """测试空上下文"""
        result = builder.build_with_context("User request", {})
        assert mock_loader.system_prompt in result
        assert "上下文" not in result


class TestPromptBuilderEdgeCases:
    """PromptBuilder 边界情况测试"""

    @pytest.fixture
    def mock_loader(self):
        loader = MockAgentLoader()
        loader._capabilities = []  # 空能力列表
        return loader

    @pytest.fixture
    def builder(self, mock_loader):
        return PromptBuilder(mock_loader)

    def test_build_generate_prompt_empty_capabilities(self, builder):
        """测试空能力列表"""
        result = builder.build_generate_prompt("test")
        assert "通用" in result

    def test_build_with_context_none(self, builder, mock_loader):
        """测试 None 上下文"""
        result = builder.build_with_context("test", None)
        assert mock_loader.system_prompt in result

    def test_build_with_context_empty_values(self, builder, mock_loader):
        """测试上下文值为空"""
        context = {"key1": "", "key2": "value2"}
        result = builder.build_with_context("test", context)
        assert "key1:" in result
        assert "key2: value2" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])