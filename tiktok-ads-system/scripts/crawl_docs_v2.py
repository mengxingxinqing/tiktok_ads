"""
用 browser-use CLI 批量抓取 TikTok Business API 文档
直接导航到 iframe 内部的 gateway URL，用 JS eval 提取正文内容
"""
import subprocess
import time
import os
import json
import re

DOCS_DIR = r"E:\code\tiktok-ads-system\docs\tiktok-api"
os.makedirs(DOCS_DIR, exist_ok=True)

IDENTIFY_KEY = "c0138ffadd90a955c1f0670a56fe348d1d40680b3c89461e09f78ed26785164b"

# doc_id 列表 — 从 TikTok Business API portal 的 iframe src 中获取
# 格式: (filename, title, doc_id_or_path)
# doc_id 是 iframe URL 中的 doc_id 参数
# path 是新版 portal URL 路径（portal/docs/xxx/v1.3）

DOC_PAGES = [
    # === Upgraded Smart+ (GMVMax) ===
    ("01_upgraded_smart_plus_overview", "Upgraded Smart+ Campaign Overview (GMVMax)", "1853452461203458"),
    ("02_upgraded_smart_plus_endpoints", "Upgraded Smart+ API Endpoints", "1802889279588353"),
    ("03_upgraded_smart_plus_workflows", "Upgraded Smart+ Workflows & Code Examples", "1802889594931201"),
    ("04_upgraded_smart_plus_retrieve_data", "Retrieve Data for Smart+ Campaigns", "1802890076061697"),
    ("05_upgraded_smart_plus_compatibility", "Compatibility Changes for Upgraded Smart+", "1802890175422466"),
    ("06_legacy_smart_plus", "Legacy Smart+ Campaign (Original GMVMax)", "1789477738498050"),

    # === Campaign Management ===
    ("10_campaign_overview", "Campaign Management Overview", "1739318962329602"),
    ("11_campaign_create", "Create a Campaign", "1739318962329602"),
    ("12_advertising_objective", "Advertising Objective", "1739726020258818"),
    ("13_campaign_budget", "Campaign Budget", "1739381696045058"),
    ("14_shopping_ads", "Shopping Ads Creation", "1740473739392001"),
    ("15_campaign_mapping", "Mapping TikTok Ads Manager to API", "1740473739392002"),

    # === Ad Group ===
    ("20_adgroup_create", "Ad Group - Create", "1739499616346114"),
    ("21_adgroup_targeting", "Ad Group - Targeting", "1739499616346115"),
    ("22_adgroup_bidding", "Ad Group - Bidding & Optimization", "1739499616346116"),

    # === Ad ===
    ("25_ad_create", "Ad - Create", "1739953377508354"),
    ("26_ad_status_update", "Ad - Status Update", "1739953422970882"),

    # === Creatives / Video ===
    ("30_creatives_overview", "Creatives Overview", "1739067914348545"),
    ("31_video_upload", "Video Upload API", "1737587322856449"),
    ("32_video_search", "Video Info & Search", "1740050161973250"),
    ("33_image_upload", "Image Upload API", "1737587322856450"),
    ("34_identity_management", "Identity Management", "1740218475032578"),
    ("35_creative_ad_formats", "Ad Formats & Creative Specs", "1740218475032579"),

    # === TikTok Store / Shop ===
    ("40_tiktok_store_overview", "TikTok Store Overview", "1739381752981505"),
    ("41_store_authorization", "Store Authorization", "1739381752981506"),
    ("42_store_product_get", "Store Product - Get", "1739381816805378"),

    # === Reporting ===
    ("50_reporting_overview", "Reporting Overview", "1738864848235521"),
    ("51_integrated_report", "Integrated Report API", "1738864915188737"),
    ("52_report_metrics_dimensions", "Report Metrics & Dimensions", "1738864928947201"),
    ("53_synchronous_report", "Synchronous Report", "1738864835805186"),
    ("54_async_report", "Asynchronous Report", "1738864860498946"),
]


def run_bu(cmd, timeout=30):
    """执行 browser-use 命令并返回输出"""
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


def get_gateway_url(doc_id):
    """构建 iframe 内部的 gateway URL"""
    return f"https://business-api.tiktok.com/gateway/docs/index?identify_key={IDENTIFY_KEY}&language=ENGLISH&doc_id={doc_id}"


def extract_content_js():
    """用 JS eval 提取文档正文内容"""
    js = r"""
(function() {
    // 查找文档内容容器
    const selectors = [
        '[class*=DocContent]',
        '[class*=docContent]',
        '[class*=Content_container]',
        '[class*=content__]',
        '.markdown-body',
        'article',
    ];
    let container = null;
    for (const sel of selectors) {
        container = document.querySelector(sel);
        if (container && container.innerText.length > 100) break;
    }
    if (!container) {
        // fallback: find largest div
        let maxLen = 0;
        document.querySelectorAll('div').forEach(d => {
            if (d.innerText.length > maxLen && d.innerText.length < 100000) {
                maxLen = d.innerText.length;
                container = d;
            }
        });
    }
    if (!container) return 'NO_CONTENT_FOUND';

    // 提取表格为 markdown 格式
    function tableToMd(table) {
        const rows = table.querySelectorAll('tr');
        if (!rows.length) return '';
        let md = '';
        rows.forEach((row, idx) => {
            const cells = row.querySelectorAll('th, td');
            const line = Array.from(cells).map(c => c.innerText.trim().replace(/\n/g, ' ')).join(' | ');
            md += '| ' + line + ' |\n';
            if (idx === 0) {
                md += '|' + Array.from(cells).map(() => '---').join('|') + '|\n';
            }
        });
        return md + '\n';
    }

    // 提取代码块
    function codeToMd(el) {
        const lang = el.className || '';
        const code = el.innerText;
        return '```' + (lang.includes('json') ? 'json' : lang.includes('python') ? 'python' : '') + '\n' + code + '\n```\n\n';
    }

    let result = '';
    const walker = document.createTreeWalker(container, NodeFilter.SHOW_ELEMENT);
    let node;
    const visited = new Set();

    while (node = walker.nextNode()) {
        if (visited.has(node)) continue;

        const tag = node.tagName;

        // 表格
        if (tag === 'TABLE') {
            result += tableToMd(node);
            visited.add(node);
            node.querySelectorAll('*').forEach(c => visited.add(c));
            continue;
        }

        // 代码块
        if (tag === 'PRE' || (tag === 'CODE' && node.innerText.length > 50)) {
            result += codeToMd(node);
            visited.add(node);
            node.querySelectorAll('*').forEach(c => visited.add(c));
            continue;
        }

        // 标题
        if (/^H[1-6]$/.test(tag)) {
            const level = parseInt(tag[1]);
            result += '#'.repeat(level) + ' ' + node.innerText.trim() + '\n\n';
            visited.add(node);
            continue;
        }

        // 段落和列表
        if (tag === 'P') {
            const text = node.innerText.trim();
            if (text && text.length > 5) result += text + '\n\n';
            visited.add(node);
            continue;
        }

        if (tag === 'LI') {
            result += '- ' + node.innerText.trim().replace(/\n/g, '\n  ') + '\n';
            visited.add(node);
            continue;
        }
    }

    // fallback: 如果 tree walker 没拿到多少内容
    if (result.trim().length < 200) {
        result = container.innerText;
    }

    return result.substring(0, 50000);
})()
""".strip()
    return run_bu(f'eval "{js}"', timeout=15)


def crawl_page(filename, title, doc_id):
    """抓取单个文档页面"""
    url = get_gateway_url(doc_id)
    print(f"  Opening doc_id={doc_id}...")

    run_bu(f'open "{url}"', timeout=20)
    time.sleep(3)

    # 提取内容
    raw = extract_content_js()

    if not raw or raw == "TIMEOUT" or "NO_CONTENT_FOUND" in raw:
        # fallback: 直接获取整个页面文本
        print("  Fallback: using state text...")
        state = run_bu("state", timeout=15)
        raw = state

    # 清理 "result: " 前缀
    if raw.startswith("result: "):
        raw = raw[8:]

    if not raw or len(raw) < 100:
        print(f"  ⚠ Very little content ({len(raw)} chars)")
        # 尝试滚动后再提取
        for _ in range(3):
            run_bu("scroll down --amount 1000")
            time.sleep(1)
        state = run_bu("state", timeout=15)
        raw = state

    # 构造 markdown
    md = f"# {title}\n\n"
    md += f"**Doc ID**: {doc_id}\n"
    md += f"**Source**: {url}\n\n"
    md += "---\n\n"
    md += raw

    filepath = os.path.join(DOCS_DIR, f"{filename}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f"  ✅ Saved: {filepath} ({len(md)} chars)")
    return len(md)


def main():
    print(f"{'='*60}")
    print(f"  TikTok Business API Docs Crawler")
    print(f"  Output: {DOCS_DIR}")
    print(f"  Pages to crawl: {len(DOC_PAGES)}")
    print(f"{'='*60}\n")

    total_chars = 0
    success = 0
    failed = 0

    for filename, title, doc_id in DOC_PAGES:
        print(f"\n[{success+failed+1}/{len(DOC_PAGES)}] {title}")
        try:
            chars = crawl_page(filename, title, doc_id)
            total_chars += chars
            success += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1

    run_bu("close")

    print(f"\n{'='*60}")
    print(f"  Results: {success} success, {failed} failed")
    print(f"  Total content: {total_chars:,} chars")
    print(f"  Files saved to: {DOCS_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
