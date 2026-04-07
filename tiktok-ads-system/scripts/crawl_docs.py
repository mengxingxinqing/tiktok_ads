"""
用 browser-use CLI 的 python 模式批量抓取 TikTok Business API 文档
"""
import subprocess
import time
import json
import os
import re

DOCS_DIR = r"E:\code\tiktok-ads-system\docs\tiktok-api"
os.makedirs(DOCS_DIR, exist_ok=True)

# 关键文档页面列表
DOC_PAGES = {
    # === GMVMax / Upgraded Smart+ ===
    "01_upgraded_smart_plus_overview.md": {
        "url": "https://business-api.tiktok.com/portal/docs/upgraded-smart-campaign/v1.3",
        "title": "Upgraded Smart+ Campaign (GMVMax) - Overview",
    },
    "02_upgraded_smart_plus_endpoints.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1802889279588353",
        "title": "Upgraded Smart+ API Endpoints",
    },
    "03_upgraded_smart_plus_workflows.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1802889594931201",
        "title": "Upgraded Smart+ Workflows & Code Examples",
    },
    "04_upgraded_smart_plus_retrieve_data.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1802890076061697",
        "title": "Retrieve Data for Upgraded Smart+, Smart+, and Manual Campaigns",
    },
    "05_upgraded_smart_plus_compatibility.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1802890175422466",
        "title": "Compatibility Changes for Upgraded Smart+ Campaigns",
    },
    # === Legacy Smart+ (GMVMax原始接口) ===
    "06_legacy_smart_plus.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1789477738498050",
        "title": "Legacy Smart+ Campaign (Original GMVMax)",
    },
    # === Campaign Management ===
    "10_campaign_create.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739318962329602",
        "title": "Campaign - Create",
    },
    "11_campaign_advertising_objective.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739726020258818",
        "title": "Campaign - Advertising Objective",
    },
    "12_campaign_budget.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739381696045058",
        "title": "Campaign - Budget",
    },
    "13_shopping_ads.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1740473739392001",
        "title": "Shopping Ads - Create",
    },
    # === Creatives / Video ===
    "20_video_upload.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1737587322856449",
        "title": "Video Upload API",
    },
    "21_video_info_search.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1740050161973250",
        "title": "Video Info & Search API",
    },
    "22_image_upload.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1737587322856450",
        "title": "Image Upload API",
    },
    "23_creative_overview.md": {
        "url": "https://business-api.tiktok.com/portal/docs/creatives-overview/v1.3",
        "title": "Creatives Overview",
    },
    "24_identity_management.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1740218475032578",
        "title": "Identity Management",
    },
    # === TikTok Store / Shop ===
    "30_tiktok_store_overview.md": {
        "url": "https://business-api.tiktok.com/portal/docs/tiktok-store-overview/v1.3",
        "title": "TikTok Store Overview",
    },
    "31_store_get.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739381752981505",
        "title": "Store - Get Information",
    },
    "32_store_product.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739381816805378",
        "title": "Store - Product Management",
    },
    # === Reporting ===
    "40_reporting_overview.md": {
        "url": "https://business-api.tiktok.com/portal/docs/reporting-overview/v1.3",
        "title": "Reporting Overview",
    },
    "41_integrated_report.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1738864915188737",
        "title": "Integrated Report API",
    },
    "42_report_metrics.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1738864928947201",
        "title": "Report Metrics & Dimensions",
    },
    # === Ads (Ad Group / Ad) ===
    "50_ad_group_create.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739499616346114",
        "title": "Ad Group - Create",
    },
    "51_ad_create.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739953377508354",
        "title": "Ad - Create",
    },
    "52_ad_status_update.md": {
        "url": "https://business-api.tiktok.com/portal/docs?id=1739953422970882",
        "title": "Ad - Status Update",
    },
}


def run_bu(cmd):
    """执行 browser-use 命令"""
    result = subprocess.run(
        f"browser-use {cmd}",
        shell=True, capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip()


def extract_page_content(url, title, max_scrolls=8):
    """提取单个页面的完整文档内容"""
    print(f"  Opening: {url}")
    run_bu(f'open "{url}"')
    time.sleep(3)

    all_text = []
    seen_text = set()

    for i in range(max_scrolls):
        state = run_bu("state")
        # 从 state 中提取文本内容（去掉元素标签行）
        lines = state.split('\n')
        content_started = False
        for line in lines:
            # 跳过纯导航菜单项
            stripped = line.strip()
            if not stripped:
                continue
            # 去掉元素标签标记
            clean = re.sub(r'^\s*\*?\[?\d+\]<[^>]+>\s*', '', stripped)
            clean = re.sub(r'^\s*\*?\|scroll element.*$', '', clean)
            clean = re.sub(r'<!-- SVG content collapsed -->', '', clean)
            clean = clean.strip()

            if not clean or len(clean) < 3:
                continue
            # 跳过重复的菜单项
            if clean in seen_text:
                continue
            # 跳过明显的 UI 元素
            if clean in ['Yes', 'No', 'EN', 'Log in', 'scroll', 'scrolled: down']:
                continue

            seen_text.add(clean)
            all_text.append(clean)

        run_bu("scroll down --amount 1500")
        time.sleep(1)

    # 组装 Markdown
    content = f"# {title}\n\n"
    content += f"Source: {url}\n\n"
    content += "---\n\n"

    # 简单清理 - 去掉导航菜单部分，保留正文
    in_content = False
    content_lines = []
    for text in all_text:
        # 检测正文开始（通常在标题之后）
        if title.split(' - ')[0].lower() in text.lower() or in_content:
            in_content = True
            content_lines.append(text)

    if not content_lines:
        # fallback: 使用所有文本
        content_lines = all_text

    content += '\n\n'.join(content_lines)
    return content


def main():
    # 先打开浏览器
    run_bu('open "https://business-api.tiktok.com/portal/docs"')
    time.sleep(3)

    for filename, info in DOC_PAGES.items():
        print(f"\n{'='*60}")
        print(f"  {info['title']}")
        print(f"{'='*60}")

        try:
            content = extract_page_content(info['url'], info['title'])
            filepath = os.path.join(DOCS_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Saved: {filepath} ({len(content)} chars)")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    run_bu("close")
    print(f"\n{'='*60}")
    print(f"  Done! Files saved to {DOCS_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
