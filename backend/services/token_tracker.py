"""Token 统计服务"""
from datetime import datetime
from typing import Dict, List

# Token 统计记录
token_stats = {
    "total_tokens": 0,
    "total_cost": 0.0,
    "last_update": datetime.now().isoformat()
}

# 详细记录
token_records: List[Dict] = []


def add_token_record(agent_id: str, tokens: int, cost: float, model: str):
    """添加 Token 记录"""
    global token_stats, token_records

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
    """获取 Token 统计"""
    return token_stats


def get_token_records(limit: int = 50) -> List[Dict]:
    """获取 Token 记录"""
    return token_records[-limit:]
