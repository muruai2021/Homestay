"""搜索服务"""
import httpx
from config.settings import DASHSCOPE_API_KEY
from openai import AsyncOpenAI


async def baidu_search(query: str, max_results: int = 5) -> dict:
    """使用通义千问进行联网搜索（通过 enable_search 参数）"""
    try:
        # 创建客户端
        client = AsyncOpenAI(
            api_key=DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        # 构建搜索提示
        search_prompt = f"""请搜索关于"{query}"的最新信息。

请给出详细的搜索结果，包含：
1. 关键发现
2. 最新动态
3. 行业趋势
4. 数据统计（如有）
5. 来源链接

要求信息来源权威、内容准确、时效性强。"""

        # 使用 enable_search 参数开启联网搜索
        response = await client.chat.completions.create(
            model="qwen-plus",  # 使用 plus 模型
            messages=[
                {"role": "system", "content": "你是一个联网搜索助手，可以搜索最新信息。请提供准确、权威的搜索结果。"},
                {"role": "user", "content": search_prompt}
            ],
            extra_body={"enable_search": True},  # 开启联网搜索
            temperature=0.7,
            max_tokens=3000
        )

        result = response.choices[0].message.content

        return {
            "success": True,
            "query": query,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
