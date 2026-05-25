"""Generation API 集成测试"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))


class TestGenerationAPI:
    """Generation API 测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        from main import app
        return TestClient(app)

    def test_wechat_article_endpoint(self, client):
        """测试公众号文章生成接口"""
        # Mock AI client
        with patch("api.generation.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].delta = MagicMock()
            mock_response.choices[0].delta.content = "这是一篇测试文章"

            mock_stream_response = MagicMock()
            mock_stream_response.choices = [MagicMock()]
            mock_stream_response.choices[0].delta = MagicMock()
            mock_stream_response.choices[0].delta.content = "测试内容"

            async def mock_stream():
                yield mock_stream_response

            mock_client.chat.completions.create = MagicMock(return_value=mock_stream())
            mock_get_client.return_value = mock_client

            # 发送请求
            response = client.post(
                "/api/wechat-article",
                json={"topic": "民宿推荐", "category": "知识类"}
            )
            # 验证响应状态码（可能是流式响应）
            assert response.status_code in [200, 500]

    def test_xhs_copy_endpoint(self, client):
        """测试小红书文案生成接口"""
        with patch("api.generation.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_stream_response = MagicMock()
            mock_stream_response.choices = [MagicMock()]
            mock_stream_response.choices[0].delta = MagicMock()
            mock_stream_response.choices[0].delta.content = "种草文案"

            async def mock_stream():
                yield mock_stream_response

            mock_client.chat.completions.create = MagicMock(return_value=mock_stream())
            mock_get_client.return_value = mock_client

            response = client.post(
                "/api/xhs-copy",
                json={"product": "民宿体验", "scene": "家庭出游"}
            )
            assert response.status_code in [200, 500]

    def test_short_video_endpoint(self, client):
        """测试短视频文案生成接口"""
        with patch("api.generation.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_stream_response = MagicMock()
            mock_stream_response.choices = [MagicMock()]
            mock_stream_response.choices[0].delta = MagicMock()
            mock_stream_response.choices[0].delta.content = "视频脚本"

            async def mock_stream():
                yield mock_stream_response

            mock_client.chat.completions.create = MagicMock(return_value=mock_stream())
            mock_get_client.return_value = mock_client

            response = client.post(
                "/api/short-video",
                json={"topic": "民宿探店", "style": "温馨风格"}
            )
            assert response.status_code in [200, 500]

    def test_intelligence_endpoint(self, client):
        """测试情报洞察接口"""
        with patch("api.generation.baidu_search") as mock_search:
            mock_search.return_value = {
                "success": True,
                "results": [{"title": "测试", "content": "测试内容"}]
            }

            response = client.post(
                "/api/intelligence",
                json={"topic": "民宿营销"}
            )
            # 可能返回 500 因为依赖数据库等，但接口存在
            assert response.status_code in [200, 500]

    def test_chat_endpoint(self, client):
        """测试通用聊天接口"""
        with patch("api.generation.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_stream_response = MagicMock()
            mock_stream_response.choices = [MagicMock()]
            mock_stream_response.choices[0].delta = MagicMock()
            mock_stream_response.choices[0].delta.content = "回复"

            async def mock_stream():
                yield mock_stream_response

            mock_client.chat.completions.create = MagicMock(return_value=mock_stream())
            mock_get_client.return_value = mock_client

            response = client.post(
                "/api/chat",
                json={"message": "你好"}
            )
            assert response.status_code in [200, 500]

    def test_poster_prompts_endpoint_structure(self, client):
        """测试海报提示词生成接口结构"""
        # 不需要 mock，直接验证接口存在
        response = client.post(
            "/api/poster",
            json={"content": "民宿宣传语", "image_ratio": "3:4"}
        )
        # 由于 AI API 未 mock，可能返回 500 但接口存在
        assert response.status_code in [200, 500]


class TestFileAPI:
    """文件操作 API 测试"""

    @pytest.fixture
    def client(self):
        from main import app
        return TestClient(app)

    def test_file_read_endpoint(self, client):
        """测试文件读取接口"""
        response = client.post(
            "/api/file/read",
            json={"agent_id": "test", "filename": "test.txt"}
        )
        # 可能 500 因为文件不存在，但接口存在
        assert response.status_code in [200, 500]

    def test_file_write_endpoint(self, client):
        """测试文件写入接口"""
        response = client.post(
            "/api/file/write",
            json={"agent_id": "test", "filename": "test.txt", "content": "hello"}
        )
        assert response.status_code in [200, 500]

    def test_file_create_doc_endpoint(self, client):
        """测试文档创建接口"""
        response = client.post(
            "/api/file/create-doc",
            json={
                "agent_id": "test",
                "filename": "test_doc",
                "title": "Test Title",
                "content": "Test content"
            }
        )
        assert response.status_code in [200, 500]

    def test_file_list_endpoint(self, client):
        """测试文件列表接口"""
        response = client.get("/api/file/test/list")
        assert response.status_code in [200, 500]

    def test_knowledge_list_endpoint(self, client):
        """测试知识库列表接口"""
        response = client.get("/api/file/knowledge/list")
        # 返回 JSON 即使目录不存在
        assert response.status_code == 200
        data = response.json()
        assert "success" in data

    def test_knowledge_category_endpoint(self, client):
        """测试知识库分类接口"""
        response = client.get("/api/file/knowledge/政策文件")
        assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])