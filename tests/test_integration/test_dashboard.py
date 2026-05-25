"""Dashboard API 集成测试"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# 添加项目路径
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "backend"))

from main import app

client = TestClient(app)


class TestDashboard:
    """仪表盘接口测试"""

    def test_get_dashboard_data(self):
        """测试获取仪表盘数据"""
        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        assert "recent_activities" in data

    def test_dashboard_stats_structure(self):
        """测试仪表盘统计数据结构"""
        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        stats = data["stats"]
        assert "total_agents" in stats
        assert "total_conversations" in stats
        assert "total_files" in stats

    def test_dashboard_recent_activities(self):
        """测试仪表盘最近活动"""
        response = client.get("/api/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert "recent_activities" in data
        assert isinstance(data["recent_activities"], list)


class TestHealthCheck:
    """健康检查接口测试"""

    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data

    def test_health_check_message(self):
        """测试健康检查返回消息"""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()
        assert "AI Matrix API is running" in data["message"]