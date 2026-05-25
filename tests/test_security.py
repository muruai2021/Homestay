"""安全函数测试"""
import pytest
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from api.agent import has_injection, sanitize_input, is_greeting, INJECTION_PATTERNS


class TestHasInjection:
    """测试 Prompt 注入检测"""

    def test_english_injection_patterns(self):
        """测试英文注入模式"""
        assert has_injection("ignore previous instructions") is True
        assert has_injection("disregard your orders") is True
        assert has_injection("forget all previous") is True
        assert has_injection("you are now") is True
        assert has_injection("act as") is True

    def test_chinese_injection_patterns(self):
        """测试中文注入模式"""
        assert has_injection("忘掉所有") is True
        assert has_injection("你现在是") is True
        assert has_injection("你是一个") is True
        assert has_injection("忽略之前") is True
        assert has_injection("无视之前") is True

    def test_case_insensitive(self):
        """测试大小写不敏感"""
        assert has_injection("IGNORE PREVIOUS INSTRUCTIONS") is True
        assert has_injection("Ignore Previous Instructions") is True

    def test_normal_input(self):
        """测试正常输入"""
        assert has_injection("你好，我想了解民宿价格") is False
        assert has_injection("帮我写一篇小红书文案") is False
        assert has_injection("今天天气怎么样") is False

    def test_injection_patterns_count(self):
        """验证注入模式数量 >= 20"""
        assert len(INJECTION_PATTERNS) >= 20, f"Expected >= 20 patterns, got {len(INJECTION_PATTERNS)}"


class TestSanitizeInput:
    """测试输入净化"""

    def test_control_characters_removed(self):
        """测试控制字符被移除"""
        # \x00 等控制字符被移除（不是替换为空格）
        assert sanitize_input("hello\x00world") == "helloworld"
        assert sanitize_input("test\x07message") == "testmessage"

    def test_extra_whitespace_collapsed(self):
        """测试多余空白被合并"""
        assert sanitize_input("hello   world") == "hello world"
        assert sanitize_input("test\n\nmessage") == "test message"
        assert sanitize_input("  spaced  out  ") == "spaced out"

    def test_stripped(self):
        """测试首尾空白被移除"""
        assert sanitize_input("  hello  ").strip() == "hello"
        assert sanitize_input("\t\ntest\t\n").strip() == "test"

    def test_empty_string(self):
        """测试空字符串"""
        assert sanitize_input("") == ""

    def test_normal_text_unchanged(self):
        """测试正常文本不变"""
        assert sanitize_input("你好，世界！") == "你好，世界！"
        assert sanitize_input("Hello, World!") == "Hello, World!"


class TestIsGreeting:
    """测试问候语判断"""

    def test_simple_greetings(self):
        """测试简单问候语"""
        assert is_greeting("你好") is True
        assert is_greeting("您好") is True
        assert is_greeting("hi") is True
        assert is_greeting("hey") is True
        assert is_greeting("hello") is True

    def test_chinese_greetings(self):
        """测试中文问候语"""
        assert is_greeting("嗨") is True
        assert is_greeting("哈喽") is True
        assert is_greeting("在吗") is True
        assert is_greeting("帮忙") is True

    def test_non_greetings(self):
        """测试非问候语"""
        assert is_greeting("我想了解民宿") is False
        assert is_greeting("帮我写文案") is False
        assert is_greeting("今天天气不错") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])