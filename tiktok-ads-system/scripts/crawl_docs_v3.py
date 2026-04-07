"""
用 browser-use CLI 通过左侧导航菜单逐个点击文档页面来抓取
每次点击菜单后，用 state 提取页面内容，滚动获取完整内容
"""
import subprocess
import time
import os
import re

DOCS_DIR = r"E:\code\tiktok-ads-system\docs\tiktok-api"
os.makedirs(DOCS_DIR, exist_ok=True)


def run_bu(cmd, timeout=30):
    try:
        result = subprocess.run(
            f"browser-use {cmd}",
            shell=True, capture_output=True, text=True, timeout=timeout,
            encoding='utf-8', errors='replace'
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"


def find_element_by_title(title):
    """从 state 输出中找到指定 title 的元素 index"""
    state = run_bu("state", timeout=15)
    # 找 div title=XXX 的元素
    pattern = rf'\[(\d+)\]<div title={re.escape(title)}'
    match = re.search(pattern, state)
    if match:
        return int(match.group(1))
    return None


def click_and_wait(idx, wait=3):
    run_bu(f"click {idx}")
    time.sleep(wait)


def get_full_page_content(max_scrolls=6):
    """获取当前文档页面的完整内容（多次滚动）"""
    all_content = []
    seen = set()

    for i in range(max_scrolls):
        state = run_bu("state", timeout=20)
        lines = state.split('\n')

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            # 清理 element markers
            clean = re.sub(r'^\s*\*?\[?\d+\]<[^>]+/?>\s*', '', stripped)
            clean = re.sub(r'<!-- SVG content collapsed -->', '', clean)
            clean = re.sub(r'^\*?\|scroll element.*$', '', clean)
            clean = clean.strip()
            if not clean or len(clean) < 3:
                continue
            if clean not in seen:
                seen.add(clean)
                all_content.append(clean)

        run_bu("scroll down --amount 1500")
        time.sleep(1)

    return all_content


def extract_doc_content(all_lines):
    """从完整的 state 文本中提取文档正文（跳过左侧导航菜单）"""
    # 找文档正文的开始位置
    # 导航菜单包含的短词列表
    nav_keywords = {
        'About the Guide', 'Overview', "What's New", 'Get Started',
        'FAQs', 'Use Cases', 'Marketing API', 'Organic API',
        'Business Messaging API', 'API Reference', 'API Playground',
        'API Service Status Page', 'SDK', 'Appendix',
        'Business Center', 'Creatives', 'Catalog Management',
        'TikTok Store', 'Campaign Management', 'Guides',
        'Audience Management', 'Reporting', 'Ad Measurement',
        'Campaign', 'Ad group', 'Ad', 'Get started',
        'Mapping between campaign features in TikTok Ads Manager and API configurations',
        'Create a campaign', 'Copy a campaign', 'Advertising objective',
        'Reach & Frequency', 'TopView', 'Budget', 'Promote campaign',
        'Realtime API', 'Dedicated Campaign', 'Super Split Test',
        '(To be deprecated) Legacy Smart+ Campaign',
        'Upgraded Smart+ Campaign',
        'Retrieve data for Upgrade Smart+, Smart+, and Manual Campaigns',
        'Compatibility changes for Upgraded Smart+ Campaigns',
    }

    ui_elements = {'Yes', 'No', 'EN', 'Log in', 'Was the information helpful?'}
    footer_patterns = ['2026 TikTok for Business', 'Terms & policies', 'Privacy & cookie policy']

    # 找到正文开始：第一行长度 > 60 字符的文本
    content_start = 0
    for i, line in enumerate(all_lines):
        if len(line) > 80 and line not in nav_keywords:
            content_start = i
            break

    # 也可能是标题行（较短但不在导航列表中）
    if content_start == 0:
        for i, line in enumerate(all_lines):
            if line not in nav_keywords and line not in ui_elements and len(line) > 15:
                # 检查是否连续有几行非导航内容
                if i + 1 < len(all_lines) and all_lines[i + 1] not in nav_keywords:
                    content_start = i
                    break

    result = []
    for line in all_lines[content_start:]:
        if line in ui_elements:
            continue
        if any(p in line for p in footer_patterns):
            continue
        if line in nav_keywords:
            continue
        result.append(line)

    return result


def save_doc(filename, title, content_lines):
    """保存为 markdown 文件"""
    md = f"# {title}\n\n---\n\n"
    md += '\n\n'.join(content_lines)
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"  ✅ {filename}: {len(md):,} chars, {len(content_lines)} paragraphs")


def crawl_by_navigation():
    """通过左侧导航菜单逐个打开文档页面"""
    # 打开文档首页
    print("Opening docs portal...")
    run_bu('open "https://business-api.tiktok.com/portal/docs"')
    time.sleep(5)

    # 展开 Marketing API
    idx = find_element_by_title("Marketing API")
    if idx:
        click_and_wait(idx, 2)
        print("Expanded Marketing API")

    # ===== 1. Campaign Management =====
    print("\n=== Campaign Management ===")
    idx = find_element_by_title("Campaign Management")
    if idx:
        click_and_wait(idx, 2)

    # Campaign Management > Guides
    idx = find_element_by_title("Guides")
    if idx:
        click_and_wait(idx, 2)

    # Campaign > expand
    idx = find_element_by_title("Campaign")
    if idx:
        click_and_wait(idx, 2)

    # --- Upgraded Smart+ ---
    pages_campaign = [
        ("Upgraded Smart+ Campaign", "01_smart_plus_overview.md", "Upgraded Smart+ Campaign (GMVMax)"),
        ("Retrieve data for Upgrade Smart+, Smart+, and Manual Campaigns", "02_smart_plus_retrieve_data.md", "Retrieve Data for Smart+ Campaigns"),
        ("Compatibility changes for Upgraded Smart+ Campaigns", "03_smart_plus_compatibility.md", "Smart+ Compatibility Changes"),
        ("(To be deprecated) Legacy Smart+ Campaign", "04_legacy_smart_plus.md", "Legacy Smart+ Campaign (GMVMax Original)"),
        ("Create a campaign", "10_campaign_create.md", "Campaign - Create"),
        ("Copy a campaign", "11_campaign_copy.md", "Campaign - Copy"),
        ("Budget", "12_campaign_budget.md", "Campaign Budget"),
        ("Promote campaign", "13_promote_campaign.md", "Promote Campaign"),
    ]

    for nav_title, filename, doc_title in pages_campaign:
        print(f"\n  > {nav_title}")
        idx = find_element_by_title(nav_title)
        if idx:
            click_and_wait(idx, 3)
            all_lines = get_full_page_content(max_scrolls=5)
            content = extract_doc_content(all_lines)
            if content:
                save_doc(filename, doc_title, content)
            else:
                print(f"  ⚠ No content found for {nav_title}")
        else:
            print(f"  ⚠ Menu item not found: {nav_title}")

    # --- Advertising objective expand ---
    idx = find_element_by_title("Advertising objective")
    if idx:
        click_and_wait(idx, 2)

    pages_adv_obj = [
        ("Advertising objective", "14_advertising_objective.md", "Advertising Objective"),
    ]
    for nav_title, filename, doc_title in pages_adv_obj:
        idx = find_element_by_title(nav_title)
        if idx:
            click_and_wait(idx, 3)
            all_lines = get_full_page_content(5)
            content = extract_doc_content(all_lines)
            if content:
                save_doc(filename, doc_title, content)

    # --- Ad group ---
    print("\n=== Ad Group ===")
    idx = find_element_by_title("Ad group")
    if idx:
        click_and_wait(idx, 2)

    ad_group_pages = [
        ("Ad group", "20_adgroup_overview.md", "Ad Group Overview"),
    ]
    for nav_title, filename, doc_title in ad_group_pages:
        idx = find_element_by_title(nav_title)
        if idx:
            click_and_wait(idx, 3)
            all_lines = get_full_page_content(5)
            content = extract_doc_content(all_lines)
            if content:
                save_doc(filename, doc_title, content)

    # --- Ad ---
    print("\n=== Ad ===")
    idx = find_element_by_title("Ad")
    if idx:
        click_and_wait(idx, 2)

    ad_pages = [
        ("Ad", "25_ad_overview.md", "Ad Overview"),
    ]
    for nav_title, filename, doc_title in ad_pages:
        idx = find_element_by_title(nav_title)
        if idx:
            click_and_wait(idx, 3)
            all_lines = get_full_page_content(5)
            content = extract_doc_content(all_lines)
            if content:
                save_doc(filename, doc_title, content)

    # ===== 2. Creatives =====
    print("\n=== Creatives ===")
    idx = find_element_by_title("Creatives")
    if idx:
        click_and_wait(idx, 2)

    creative_pages = [
        ("Creatives", "30_creatives_overview.md", "Creatives Overview"),
    ]
    for nav_title, filename, doc_title in creative_pages:
        idx = find_element_by_title(nav_title)
        if idx:
            click_and_wait(idx, 3)
            all_lines = get_full_page_content(5)
            content = extract_doc_content(all_lines)
            if content:
                save_doc(filename, doc_title, content)

    # ===== 3. TikTok Store =====
    print("\n=== TikTok Store ===")
    idx = find_element_by_title("TikTok Store")
    if idx:
        click_and_wait(idx, 2)

    store_pages = [
        ("TikTok Store", "40_store_overview.md", "TikTok Store Overview"),
    ]
    for nav_title, filename, doc_title in store_pages:
        idx = find_element_by_title(nav_title)
        if idx:
            click_and_wait(idx, 3)
            all_lines = get_full_page_content(5)
            content = extract_doc_content(all_lines)
            if content:
                save_doc(filename, doc_title, content)

    # ===== 4. Reporting =====
    print("\n=== Reporting ===")
    idx = find_element_by_title("Reporting")
    if idx:
        click_and_wait(idx, 2)

    reporting_pages = [
        ("Reporting", "50_reporting_overview.md", "Reporting Overview"),
    ]
    for nav_title, filename, doc_title in reporting_pages:
        idx = find_element_by_title(nav_title)
        if idx:
            click_and_wait(idx, 3)
            all_lines = get_full_page_content(5)
            content = extract_doc_content(all_lines)
            if content:
                save_doc(filename, doc_title, content)

    # ===== 5. API Reference (核心 endpoint 文档) =====
    print("\n=== API Reference ===")
    idx = find_element_by_title("API Reference")
    if idx:
        click_and_wait(idx, 2)

    # 获取 API Reference 子菜单
    state = run_bu("state", timeout=20)
    # 查找 GMV Max, Files, Reporting 等子菜单
    api_ref_items = re.findall(r'\[(\d+)\]<div title=([^/]+?) />', state)
    gmvmax_items = [(idx, title) for idx, title in api_ref_items
                    if any(kw in title.lower() for kw in ['gmv', 'file', 'report', 'campaign', 'identity', 'store', 'shop', 'creative', 'image', 'video'])]

    print(f"  Found {len(gmvmax_items)} API Reference items")

    for elem_idx, elem_title in gmvmax_items:
        print(f"\n  > API Ref: {elem_title}")
        click_and_wait(int(elem_idx), 3)
        all_lines = get_full_page_content(8)  # API docs are longer
        content = extract_doc_content(all_lines)
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', elem_title.strip()).lower()
        filename = f"60_apiref_{safe_name}.md"
        if content:
            save_doc(filename, f"API Reference - {elem_title.strip()}", content)

    run_bu("close")
    print(f"\n{'='*60}")
    print(f"  Done! Files saved to {DOCS_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    crawl_by_navigation()
