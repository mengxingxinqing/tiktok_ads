"""
用 browser-use CLI 抓取关键 TikTok Business API endpoint 文档
策略：在 gateway 页面中，通过 JS 点击左侧菜单项加载文档，
然后提取右侧内容区文本
"""
import subprocess
import time
import os
import re
import json

DOCS_DIR = r"E:\code\tiktok-ads-system\docs\tiktok-api"
os.makedirs(DOCS_DIR, exist_ok=True)

# 需要抓取的关键文档页面标题（必须与菜单中的 title 完全匹配）
KEY_DOCS = [
    # GMV Max
    ("gmvmax_01_create_campaign", "Create a GMV Max Campaign"),
    ("gmvmax_02_get_campaigns", "Get GMV Max Campaigns"),
    ("gmvmax_03_get_details", "Get the details of a GMV Max Campaign"),
    ("gmvmax_04_update_campaign", "Update a GMV Max Campaign"),
    ("gmvmax_05_get_shops", "Get TikTok Shops for GMV Max Campaigns"),
    ("gmvmax_06_get_products", "Get products within a TikTok Shop"),
    ("gmvmax_07_get_identities", "Get identities for GMV Max Campaigns"),
    ("gmvmax_08_get_posts", "Get posts for a Product GMV Max Campaign"),
    ("gmvmax_09_remove_add_creatives", "Remove or add back creatives in a GMV Max Campaign"),
    ("gmvmax_10_run_report", "Run a GMV Max Campaign report"),
    ("gmvmax_11_metrics", "Metrics in GMV Max Campaign reports"),
    ("gmvmax_12_check_shop_availability", "Check the availability of a TikTok Shop for Product GMV Max Campaigns"),
    ("gmvmax_13_get_roi_target", "Get the recommended GMV Max ROI target and budget"),
    ("gmvmax_14_create_product_gmvmax", "Create Product GMV Max Campaigns"),
    ("gmvmax_15_create_live_gmvmax", "Create LIVE GMV Max Campaigns"),
    ("gmvmax_16_migrate", "Migrate to GMV Max Campaigns"),

    # Upgraded Smart+
    ("smart_01_create_campaign", "Create an Upgraded Smart+ Campaign"),
    ("smart_02_get_campaigns", "Get Upgraded Smart+ Campaigns"),
    ("smart_03_update_campaign", "Update an Upgraded Smart+ Campaign"),
    ("smart_04_create_adgroup", "Create an Upgraded Smart+ Ad Group"),
    ("smart_05_get_adgroups", "Get Upgraded Smart+ Ad Groups"),
    ("smart_06_update_adgroup", "Update an Upgraded Smart+ Ad Group"),
    ("smart_07_create_ad", "Create an Upgraded Smart+ Ad"),
    ("smart_08_get_ads", "Get Upgraded Smart+ Ads"),
    ("smart_09_update_ad", "Update an Upgraded Smart+ Ad"),
    ("smart_10_disable_enable_creatives", "Disable or enable creatives in an Upgraded Smart+ Ad"),
    ("smart_11_retrieve_data", "Retrieve data for Upgrade Smart+, Smart+, and Manual Campaigns"),

    # Campaign
    ("campaign_01_create", "Create a campaign"),
    ("campaign_02_get", "Get campaigns"),
    ("campaign_03_update", "Update a campaign"),
    ("campaign_04_update_status", "Update the operation statuses of campaigns"),
    ("campaign_05_copy", "Copy a campaign"),
    ("campaign_06_budget", "Get the balance and budget of ad accounts"),
    ("campaign_07_recommended_budgets", "Get recommended budgets"),

    # Ad Group
    ("adgroup_01_create", "Create an ad group"),
    ("adgroup_02_get", "Get ad groups"),
    ("adgroup_03_update", "Update an ad group"),
    ("adgroup_04_update_status", "Update the statuses of ad groups"),

    # Video / File
    ("file_01_upload_video", "Upload a video"),
    ("file_02_search_videos", "Search for videos"),
    ("file_03_get_video_info", "Get info about videos"),
    ("file_04_upload_image", "Upload an image"),
    ("file_05_search_images", "Search for images"),
    ("file_06_upload_file", "Upload a file"),

    # Identity
    ("identity_01_create", "Create an identity"),
    ("identity_02_get_list", "Get the identity list"),
    ("identity_03_get_info", "Get info about an identity"),

    # TikTok Store
    ("store_01_get_stores", "Get available stores under an ad account"),
    ("store_02_grant_auth", "Grant an ad account exclusive authorization for a TikTok Shop"),
    ("store_03_get_auth_status", "Get the TikTok Shop exclusive authorization status of an ad account"),

    # Reporting
    ("report_01_sync", "Run a synchronous report"),
    ("report_02_async_create", "Create an asynchronous report task"),
    ("report_03_async_status", "Get the status of an async report task"),
    ("report_04_async_download", "Download the output of an async report task"),
    ("report_05_basic_metrics", "Supported metrics for a dimension in basic reports"),
]


def run_bu(cmd, timeout=30):
    try:
        result = subprocess.run(
            f"browser-use {cmd}",
            shell=True, capture_output=True, text=True, timeout=timeout,
            encoding='utf-8', errors='replace'
        )
        return result.stdout.strip()
    except:
        return ""


def click_menu_by_title(title):
    """通过 JS 在 gateway iframe 内找到并点击菜单项"""
    # 用 JS 查找并点击
    js = f"""
(function() {{
    const items = document.querySelectorAll('[class*=DocMenu_list]');
    for (const item of items) {{
        if (item.getAttribute('title') === '{title.replace("'", "\\'")}') {{
            item.click();
            return 'clicked: ' + item.getAttribute('title');
        }}
    }}
    return 'not found: {title.replace("'", "\\'")}';
}})()
"""
    result = run_bu(f'eval "{js}"', timeout=10)
    return 'clicked' in result


def get_doc_content():
    """提取文档右侧的内容区文本"""
    js = r"""
(function() {
    const sel = [
        '[class*=DocContent]',
        '[class*=Content_container]',
        '[class*=content__]',
    ];
    let el = null;
    for (const s of sel) {
        el = document.querySelector(s);
        if (el && el.innerText.length > 50) break;
    }
    if (!el) return '';
    return el.innerText.substring(0, 30000);
})()
"""
    result = run_bu(f'eval "{js}"', timeout=15)
    if result and result.startswith("result: "):
        return result[8:]
    return ""


def main():
    print(f"Crawling {len(KEY_DOCS)} key API docs...\n")

    # 打开 gateway 文档页面
    run_bu('open "https://business-api.tiktok.com/gateway/docs/index?identify_key=c0138ffadd90a955c1f0670a56fe348d1d40680b3c89461e09f78ed26785164b&language=ENGLISH"', timeout=20)
    time.sleep(5)

    success = 0
    failed = 0

    for filename, title in KEY_DOCS:
        print(f"[{success+failed+1}/{len(KEY_DOCS)}] {title}...", end=" ", flush=True)

        clicked = click_menu_by_title(title)
        if not clicked:
            print("MENU NOT FOUND")
            failed += 1
            continue

        time.sleep(2)  # 等待内容加载

        content = get_doc_content()
        if not content or len(content) < 50:
            # 重试一次
            time.sleep(3)
            content = get_doc_content()

        if content and len(content) >= 50:
            filepath = os.path.join(DOCS_DIR, f"{filename}.md")
            md = f"# {title}\n\n---\n\n{content}\n"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md)
            print(f"OK ({len(content):,} chars)")
            success += 1
        else:
            print(f"NO CONTENT ({len(content) if content else 0} chars)")
            failed += 1

    run_bu("close")
    print(f"\n{'='*50}")
    print(f"  Done: {success} success, {failed} failed")
    print(f"  Saved to: {DOCS_DIR}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
