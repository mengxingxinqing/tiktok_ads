"""
使用 browser-use 抓取 TikTok Business API 文档
目标：GMVMax、店铺、数据报表、创意/视频、Ads 相关接口文档
输出：Markdown 文件到 docs/ 目录
"""
import asyncio
import os
import sys

from langchain_openai import ChatOpenAI
from browser_use import Agent

# LLM 配置（使用项目 .env 中的配置）
LLM_API_BASE = "https://api.tongtools.com"
LLM_API_KEY = "sk-apTZr7qZ8K1vAjTlMmAVSh5Hx8Nx0OqOvIPszsud50bhjkcv"
LLM_MODEL = "gpt-4o"

DOCS_DIR = r"E:\code\tiktok-ads-system\docs"

llm = ChatOpenAI(
    model=LLM_MODEL,
    base_url=f"{LLM_API_BASE}/v1",
    api_key=LLM_API_KEY,
    temperature=0,
)

# 要抓取的文档主题和对应的入口页面
DOC_TASKS = [
    {
        "name": "gmvmax_api",
        "filename": "tiktok_gmvmax_api.md",
        "prompt": """
Navigate to https://business-api.tiktok.com/portal/docs?id=1802889279588353
This is the TikTok Business API documentation portal.

Find and read ALL documentation related to GMV Max (GMVMax) campaigns, including:
1. GMV Max Campaign creation/management APIs
2. GMV Max creative management (add/remove videos)
3. GMV Max campaign budget/status operations
4. GMV Max reporting/metrics APIs
5. Any GMV Max specific parameters and enums

For each API endpoint found, extract:
- Endpoint URL and HTTP method
- Required and optional parameters (name, type, description)
- Request body format
- Response format with field descriptions
- Any important notes or limitations

Format everything as a well-structured Markdown document with clear sections.
Output the COMPLETE document content - do not summarize or abbreviate.
""",
    },
    {
        "name": "shop_store_api",
        "filename": "tiktok_shop_store_api.md",
        "prompt": """
Navigate to https://business-api.tiktok.com/portal/docs?id=1739381752981505
This is the TikTok Business API documentation portal.

Find and read ALL documentation related to TikTok Shop / Store APIs, including:
1. Store/Shop information APIs (get store info, list stores)
2. Product management APIs (list products, get product details)
3. Order management APIs (list orders, order details)
4. Shop authorization and linking APIs
5. Any seller-related APIs

For each API endpoint found, extract:
- Endpoint URL and HTTP method
- Required and optional parameters (name, type, description)
- Request body format
- Response format with field descriptions
- Any important notes or limitations

Format everything as a well-structured Markdown document with clear sections.
Output the COMPLETE document content - do not summarize or abbreviate.
""",
    },
    {
        "name": "reporting_api",
        "filename": "tiktok_reporting_data_api.md",
        "prompt": """
Navigate to https://business-api.tiktok.com/portal/docs?id=1738864915188737
This is the TikTok Business API documentation portal.

Find and read ALL documentation related to TikTok Ads Reporting and Data APIs, including:
1. Integrated Report API (report/integrated/get)
2. Audience Report API
3. Metrics and dimensions available
4. Data levels (CAMPAIGN, AD_GROUP, AD, etc.)
5. GMVMax specific reporting fields
6. Attribution settings
7. Report data format and pagination

For each API endpoint found, extract:
- Endpoint URL and HTTP method
- Required and optional parameters (name, type, description)
- Available metrics and dimensions lists
- Response format with field descriptions
- Any important notes, rate limits, or data freshness info

Format everything as a well-structured Markdown document with clear sections.
Output the COMPLETE document content - do not summarize or abbreviate.
""",
    },
    {
        "name": "creative_video_api",
        "filename": "tiktok_creative_video_api.md",
        "prompt": """
Navigate to https://business-api.tiktok.com/portal/docs?id=1737587322856449
This is the TikTok Business API documentation portal.

Find and read ALL documentation related to Creative and Video management APIs, including:
1. Video upload APIs (file upload, URL upload, chunk upload)
2. Video info/search APIs
3. Image upload APIs
4. Creative management APIs
5. Ad creative specifications and requirements
6. Video review status and moderation
7. Identity/persona management for video posting

For each API endpoint found, extract:
- Endpoint URL and HTTP method
- Required and optional parameters (name, type, description)
- File upload requirements (format, size limits, etc.)
- Request body format
- Response format with field descriptions
- Any important notes or limitations

Format everything as a well-structured Markdown document with clear sections.
Output the COMPLETE document content - do not summarize or abbreviate.
""",
    },
    {
        "name": "ads_campaign_api",
        "filename": "tiktok_ads_campaign_api.md",
        "prompt": """
Navigate to https://business-api.tiktok.com/portal/docs?id=1739381752981505
This is the TikTok Business API documentation portal.

Find and read ALL documentation related to Ads and Campaign management APIs, including:
1. Campaign CRUD APIs (create, read, update, delete campaigns)
2. Ad Group CRUD APIs
3. Ad CRUD APIs
4. Campaign/AdGroup/Ad status management (enable, disable, delete)
5. Budget management APIs
6. Targeting and audience settings
7. Bidding strategies and optimization goals
8. Campaign objective types and their parameters

For each API endpoint found, extract:
- Endpoint URL and HTTP method
- Required and optional parameters (name, type, description)
- Request body format
- Response format with field descriptions
- Enum values for important fields (objective_type, budget_mode, bid_type, etc.)
- Any important notes or limitations

Format everything as a well-structured Markdown document with clear sections.
Output the COMPLETE document content - do not summarize or abbreviate.
""",
    },
]


async def crawl_single_doc(task: dict) -> str:
    """使用 browser-use 抓取单个文档主题"""
    print(f"\n{'='*60}")
    print(f"  Crawling: {task['name']}")
    print(f"{'='*60}")

    agent = Agent(
        task=task["prompt"],
        llm=llm,
        max_actions_per_step=5,
    )

    result = await agent.run(max_steps=30)

    # 提取最终结果
    final_result = result.final_result()
    if final_result:
        return final_result

    # fallback: 从 history 提取
    history = result.history
    if history:
        last = history[-1]
        if hasattr(last, 'result') and last.result:
            return str(last.result)

    return ""


async def main():
    os.makedirs(DOCS_DIR, exist_ok=True)

    for task in DOC_TASKS:
        try:
            content = await crawl_single_doc(task)
            if content:
                filepath = os.path.join(DOCS_DIR, task["filename"])
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"\n  ✅ Saved: {filepath}")
                print(f"     Size: {len(content)} chars")
            else:
                print(f"\n  ❌ No content returned for {task['name']}")
        except Exception as e:
            print(f"\n  ❌ Error crawling {task['name']}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"  Done! Check {DOCS_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
