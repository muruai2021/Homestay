"""配置加载模块"""
import os
from pathlib import Path

# 项目根目录 (C:\project\ai-matrix)
# settings.py 在 backend/config/settings.py，所以需要 parent.parent.parent
BASE_DIR = Path(__file__).parent.parent.parent

# 加载环境变量
from dotenv import load_dotenv
env_path = BASE_DIR / ".env"
load_dotenv(env_path, override=True)

# 强制从 .env 读取配置（忽略系统环境变量）
_DEEPSEEK_API_KEY = ""
_DASHSCOPE_API_KEY = ""
_MINIMAX_API_KEY = ""
_DASHSCOPE_IMAGE_URL = ""
_AI_PROVIDER = "qwen"
_BAIDU_SEARCH_KEY = ""

if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key == "DEEPSEEK_API_KEY":
                    _DEEPSEEK_API_KEY = value
                elif key == "DASHSCOPE_API_KEY":
                    _DASHSCOPE_API_KEY = value
                elif key == "MINIMAX_API_KEY":
                    _MINIMAX_API_KEY = value
                elif key == "DASHSCOPE_IMAGE_URL":
                    _DASHSCOPE_IMAGE_URL = value
                elif key == "AI_PROVIDER":
                    _AI_PROVIDER = value
                elif key == "BAIDU_SEARCH_KEY":
                    _BAIDU_SEARCH_KEY = value

# 配置常量
AI_PROVIDER = _AI_PROVIDER
DEEPSEEK_API_KEY = _DEEPSEEK_API_KEY
DASHSCOPE_API_KEY = _DASHSCOPE_API_KEY
MINIMAX_API_KEY = _MINIMAX_API_KEY
DASHSCOPE_IMAGE_URL = _DASHSCOPE_IMAGE_URL
BAIDU_SEARCH_KEY = _BAIDU_SEARCH_KEY

# 加载"我是谁"提示词
IAM_PROMPT = ""
iam_file = BASE_DIR / "knowledge_base" / "我是谁.md"
if iam_file.exists():
    with open(iam_file, "r", encoding="utf-8") as f:
        IAM_PROMPT = f.read().strip()

# 员工登录密码（从环境变量读取）
STAFF_PASSWORD = os.environ.get("STAFF_PASSWORD", "")

# 服务器配置
HOST = "0.0.0.0"
PORT = 9002
RELOAD = False

# 工作空间目录
WORKSPACE_DIR = BASE_DIR / "workspace"

# 验证配置
print(f"[配置] 从 .env 加载 AI_PROVIDER = {AI_PROVIDER}")
print(f"[配置] 工作空间目录 = {WORKSPACE_DIR}")
