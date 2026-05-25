"""Generation API 集成测试"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import sys
from pathlib import Path

# 添加项目路径
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "backend"))

from main import app

client = TestClient(app)


class MockChoice:
    """模拟 choice 对象"""
    def __init__(self, content: str = ""):
        self.delta = MagicMock()
        self.delta.content = content


class MockChunk:
    """模拟流式响应 chunk"""
    def __init__(self, content: str = ""):
        self.choices = [MockChoice(content)]


class TestXhsCopy:
    """小红书文案生成接口测试"""

    def _get_mock_response(self):
        """创建模拟的流式响应"""
        chunks = ["这是", "一条", "模拟", "的", "小红书", "文案"]
        mock_response = MagicMock()
        mock_response.__aiter__ = lambda self: iter([MockChunk(c) for c in chunks])
        return mock_response

    @pytest.fixture
    def mock_ai_client(self):
        """Mock AI client"""
        with patch('api.generation.get_client') as mock_get_client:
            mock_client = MagicMock()
            mock_response = self._get_mock_response()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client
            yield mock_get_client

    def test_xhs_copy_basic(self, mock_ai_client):
        """测试基本的小红书文案生成"""
        response = client.post(
            "/api/xhs-copy",
            json={
                "product": "猩伙伴民宿大床房",
                "scene": "周末度假"
            }
        )

        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_xhs_copy_without_scene(self, mock_ai_client):
        """测试不带场景参数的小红书文案生成"""
        response = client.post(
            "/api/xhs-copy",
            json={
                "product": "猩伙伴民宿"
            }
        )

        assert response.status_code == 200

    def test_xhs_copy_empty_product(self, mock_ai_client):
        """测试空产品名称的处理"""
        response = client.post(
            "/api/xhs-copy",
            json={
                "product": ""
            }
        )

        # 空产品仍会发送请求
        assert response.status_code == 200


class TestShortVideo:
    """短视频文案生成接口测试"""

    def _get_mock_response(self):
        """创建模拟的流式响应"""
        chunks = ["这是", "一条", "模拟", "的", "短视频", "脚本"]
        mock_response = MagicMock()
        mock_response.__aiter__ = lambda self: iter([MockChunk(c) for c in chunks])
        return mock_response

    @pytest.fixture
    def mock_ai_client(self):
        """Mock AI client"""
        with patch('api.generation.get_client') as mock_get_client:
            mock_client = MagicMock()
            mock_response = self._get_mock_response()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client
            yield mock_get_client

    def test_short_video_basic(self, mock_ai_client):
        """测试基本的短视频脚本生成"""
        response = client.post(
            "/api/short-video",
            json={
                "topic": "民宿体验",
                "style": "温馨风格",
                "duration": 60
            }
        )

        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_short_video_with_defaults(self, mock_ai_client):
        """测试使用默认参数的短视频脚本生成"""
        response = client.post(
            "/api/short-video",
            json={
                "topic": "民宿推荐"
            }
        )

        assert response.status_code == 200

    def test_short_video_different_durations(self, mock_ai_client):
        """测试不同长度的短视频脚本"""
        for duration in [15, 30, 60, 120]:
            response = client.post(
                "/api/short-video",
                json={
                    "topic": "民宿体验",
                    "duration": duration
                }
            )
            assert response.status_code == 200


class TestPoster:
    """海报生成接口测试"""

    def _get_mock_response(self):
        """创建模拟的非流式响应"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"image_description": "描述", "text_description": "文字", "scene_description": "场景", "style_description": "风格"}'
        return mock_response

    @pytest.fixture
    def mock_ai_client(self):
        """Mock AI client"""
        with patch('api.generation.get_client') as mock_get_client:
            mock_client = MagicMock()
            mock_response = self._get_mock_response()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client
            yield mock_get_client

    def test_poster_basic(self, mock_ai_client):
        """测试基本的海报提示词生成"""
        response = client.post(
            "/api/poster",
            json={
                "content": "猩伙伴民宿，旅途中的家",
                "image_ratio": "--ar 3:4"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "prompts" in data

    def test_poster_without_ratio(self, mock_ai_client):
        """测试不带比例参数的海报生成"""
        response = client.post(
            "/api/poster",
            json={
                "content": "猩伙伴民宿宣传海报"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_poster_different_ratios(self, mock_ai_client):
        """测试不同比例的海报"""
        ratios = ["--ar 1:1", "--ar 3:4", "--ar 16:9", "--ar 9:16"]
        for ratio in ratios:
            response = client.post(
                "/api/poster",
                json={
                    "content": "民宿海报",
                    "image_ratio": ratio
                }
            )
            assert response.status_code == 200


class TestIntelligence:
    """情报收集接口测试"""

    @pytest.fixture
    def mock_search(self):
        """Mock 搜索服务"""
        mock_result = {
            "results": [
                {"title": "民宿发展趋势", "content": "2024年民宿市场分析报告..."},
                {"title": "热门旅游目的地", "content": "上半年最受欢迎的旅游目的地..."},
                {"title": "旅行者偏好分析", "content": "新时代旅行者的住宿偏好..."}
            ]
        }
        with patch('api.generation.baidu_search', new=AsyncMock(return_value=mock_result)):
            yield

    def test_intelligence_basic(self, mock_search):
        """测试基本的情报收集"""
        response = client.post(
            "/api/intelligence",
            json={
                "topic": "民宿市场趋势",
                "focus_areas": ["市场分析", "用户偏好"]
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_intelligence_without_focus_areas(self, mock_search):
        """测试不带聚焦领域的情报收集"""
        response = client.post(
            "/api/intelligence",
            json={
                "topic": "旅游业发展"
            }
        )

        assert response.status_code == 200

    def test_intelligence_empty_focus_areas(self, mock_search):
        """测试空聚焦领域列表"""
        response = client.post(
            "/api/intelligence",
            json={
                "topic": "民宿运营",
                "focus_areas": []
            }
        )

        assert response.status_code == 200


class TestWechatArticle:
    """公众号文章生成接口测试"""

    def _get_mock_response(self):
        """创建模拟的流式响应"""
        chunks = ["这是", "一篇", "模拟", "的", "公众号", "文章"]
        mock_response = MagicMock()
        mock_response.__aiter__ = lambda self: iter([MockChunk(c) for c in chunks])
        return mock_response

    @pytest.fixture
    def mock_ai_client(self):
        """Mock AI client"""
        with patch('api.generation.get_client') as mock_get_client:
            mock_client = MagicMock()
            mock_response = self._get_mock_response()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client
            yield mock_get_client

    def test_wechat_article_basic(self, mock_ai_client):
        """测试基本的公众号文章生成"""
        response = client.post(
            "/api/wechat-article",
            json={
                "topic": "民宿运营指南",
                "length": 1500
            }
        )

        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_wechat_article_with_audience(self, mock_ai_client):
        """测试带目标受众的文章生成"""
        response = client.post(
            "/api/wechat-article",
            json={
                "topic": "民宿体验分享",
                "audience": {
                    "age": "25-40",
                    "occupation": "年轻旅行者",
                    "interests": ["旅行", "摄影"]
                }
            }
        )

        assert response.status_code == 200

    def test_wechat_article_with_category(self, mock_ai_client):
        """测试带分类的文章生成"""
        response = client.post(
            "/api/wechat-article",
            json={
                "topic": "民宿运营技巧",
                "category": "经验类（分享）"
            }
        )

        assert response.status_code == 200


class TestChat:
    """通用聊天接口测试"""

    def _get_mock_response(self):
        """创建模拟的流式响应"""
        chunks = ["这是", "一条", "模拟", "的", "聊天", "响应"]
        mock_response = MagicMock()
        mock_response.__aiter__ = lambda self: iter([MockChunk(c) for c in chunks])
        return mock_response

    @pytest.fixture
    def mock_ai_client(self):
        """Mock AI client"""
        with patch('api.generation.get_client') as mock_get_client:
            mock_client = MagicMock()
            mock_response = self._get_mock_response()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client
            yield mock_get_client

    def test_chat_basic(self, mock_ai_client):
        """测试基本的聊天功能"""
        response = client.post(
            "/api/chat",
            json={
                "message": "你好，帮我推荐一家民宿"
            }
        )

        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]

    def test_chat_with_history(self, mock_ai_client):
        """测试带历史记录的聊天"""
        response = client.post(
            "/api/chat",
            json={
                "message": "继续刚才的话题",
                "history": [
                    {"role": "user", "content": "我想找一个适合家庭出游的民宿"},
                    {"role": "assistant", "content": "好的，请问您对位置有什么偏好？"}
                ]
            }
        )

        assert response.status_code == 200

    def test_chat_empty_message(self, mock_ai_client):
        """测试空消息处理"""
        response = client.post(
            "/api/chat",
            json={
                "message": ""
            }
        )

        assert response.status_code == 200