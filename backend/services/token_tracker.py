"""Token 统计服务"""
import threading
from datetime import datetime
from typing import Dict, List

# 线程锁保护全局变量
_token_lock = threading.Lock()

# Token 统计记录
token_stats = {
    "total_tokens": 0,
    "total_cost": 0.0,
    "last_update": datetime.now().isoformat()
}

# 详细记录
token_records: List[Dict] = []


def add_token_record(agent_id: str, tokens: int, cost: float, model: str):
    """添加 Token 记录（线程安全）"""
    global token_stats, token_records

    with _token_lock:
        token_stats["total_tokens"] += tokens
        token_stats["total_cost"] += cost
        token_stats["last_update"] = datetime.now().isoformat()

        token_records.append({
            "agent_id": agent_id,
            "tokens": tokens,
            "cost": cost,
            "model": model,
            "timestamp": datetime.now().isoformat()
        })

        # 只保留最近 100 条记录
        if len(token_records) > 100:
            token_records = token_records[-100:]


def get_token_stats() -> Dict:
    """获取 Token 统计（线程安全）"""
    with _token_lock:
        return dict(token_stats)  # 返回副本避免竞态


def get_token_records(limit: int = 50) -> List[Dict]:
    """获取 Token 记录（线程安全）"""
    with _token_lock:
        return list(token_records[-limit:])  # 返回副本
