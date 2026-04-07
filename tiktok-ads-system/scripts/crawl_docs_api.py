"""
通过 TikTok 内部文档 API 直接获取文档内容
1. tree/get 获取文档树和 doc_id
2. node/get 获取每个文档的具体内容
"""
import requests
import json
import os
import re
import time
from html import unescape

DOCS_DIR = r"E:\code\tiktok-ads-system\docs\tiktok-api"
os.makedirs(DOCS_DIR, exist_ok=True)

IDENTIFY_KEY = "c0138ffadd90a955c1f0670a56fe348d1d40680b3c89461e09f78ed26785164b"
BASE_URL = "https://business-api.tiktok.com/gateway/api/doc/client"

# 关键词过滤 — 只抓取包含这些关键词的文档
KEYWORDS = [
    'gmv max', 'gmvmax', 'smart+', 'smart plus',
    'campaign', 'ad group', 'adgroup',
    'video', 'upload', 'image', 'file', 'creative',
    'identity', 'store', 'shop', 'product',
    'report', 'metric', 'dimension',
    'budget', 'bidding', 'targeting',
    'shopping ads', 'catalog',
]

# 排除的关键词
EXCLUDE = [
    'deprecated', 'to be deprecated', 'to-be-deprecated',
    'messaging', 'organic', 'mentions', 'tto',
    'lead generation', 'automotive', 'app pre-registration',
    'community interaction', 'custom conversion',
    'offline event', 'web event', 'app event',
    'reach & frequency', 'topview', 'pangle',
    'playable', 'music', 'brand profile', 'brand safety',
    'negative keyword', 'showcase', 'page ',
    'super split', 'dsa report', 'video insight',
    'comment', 'bc management', 'bc payment', 'bc asset',
    'bc billing', 'bc partner', 'bc member', 'bc invoice',
]


def get_tree():
    """获取文档树"""
    url = f"{BASE_URL}/platform/tree/get/"
    params = {
        "language": "ENGLISH",
        "identify_key": IDENTIFY_KEY,
        "is_need_content": "false",
    }
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()
    if data["code"] != 0:
        raise Exception(f"Failed to get tree: {data}")
    return data["data"]["primary_doc_list"]


def get_node(doc_id):
    """获取单个文档内容"""
    url = f"{BASE_URL}/node/get/"
    params = {
        "language": "ENGLISH",
        "identify_key": IDENTIFY_KEY,
        "doc_id": str(doc_id),
    }
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()
    if data["code"] != 0:
        return None
    return data["data"]


def flatten_tree(nodes, parent_path=""):
    """展开文档树为平面列表"""
    result = []
    for node in nodes:
        title = node.get("title", "").strip()
        path = f"{parent_path}/{title}" if parent_path else title
        doc_id = node.get("doc_id")
        doc_type = node.get("type", "")

        result.append({
            "doc_id": doc_id,
            "title": title,
            "path": path,
            "type": doc_type,
            "has_children": bool(node.get("child_docs")),
        })

        if node.get("child_docs"):
            result.extend(flatten_tree(node["child_docs"], path))

    return result


def is_relevant(doc):
    """判断文档是否是我们需要的"""
    title_lower = doc["title"].lower()
    path_lower = doc["path"].lower()

    # 排除
    for ex in EXCLUDE:
        if ex in title_lower:
            return False

    # 包含
    for kw in KEYWORDS:
        if kw in title_lower or kw in path_lower:
            return True

    return False


def html_to_markdown(html_content):
    """简单的 HTML 转 Markdown"""
    if not html_content:
        return ""

    text = html_content

    # 标题
    for i in range(6, 0, -1):
        text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', lambda m: f"\n{'#' * i} {m.group(1).strip()}\n", text, flags=re.DOTALL)

    # 表格 — 保留基本结构
    text = re.sub(r'<table[^>]*>', '\n', text)
    text = re.sub(r'</table>', '\n', text)
    text = re.sub(r'<thead[^>]*>', '', text)
    text = re.sub(r'</thead>', '', text)
    text = re.sub(r'<tbody[^>]*>', '', text)
    text = re.sub(r'</tbody>', '', text)
    text = re.sub(r'<tr[^>]*>', '\n| ', text)
    text = re.sub(r'</tr>', ' |', text)
    text = re.sub(r'<th[^>]*>(.*?)</th>', lambda m: m.group(1).strip() + ' | ', text, flags=re.DOTALL)
    text = re.sub(r'<td[^>]*>(.*?)</td>', lambda m: m.group(1).strip() + ' | ', text, flags=re.DOTALL)

    # 代码块
    text = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', lambda m: f"\n```\n{m.group(1)}\n```\n", text, flags=re.DOTALL)
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)

    # 链接
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)

    # 列表
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'\n- \1', text, flags=re.DOTALL)
    text = re.sub(r'<[ou]l[^>]*>', '', text)
    text = re.sub(r'</[ou]l>', '', text)

    # 段落和换行
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<div[^>]*>', '\n', text)
    text = re.sub(r'</div>', '', text)

    # 粗体和斜体
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)

    # 清除剩余 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)

    # HTML entities
    text = unescape(text)

    # 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def main():
    print("Fetching document tree...")
    tree = get_tree()

    print("Flattening tree...")
    all_docs = flatten_tree(tree)
    print(f"  Total documents: {len(all_docs)}")

    # 过滤
    relevant = [d for d in all_docs if is_relevant(d)]
    print(f"  Relevant documents: {len(relevant)}")

    # 保存文档树索引
    index_path = os.path.join(DOCS_DIR, "00_index.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# TikTok Business API - Document Index\n\n")
        for doc in relevant:
            f.write(f"- [{doc['title']}](#{doc['doc_id']}) — {doc['path']}\n")
    print(f"  Index saved: {index_path}")

    # 逐个获取文档内容
    success = 0
    failed = 0

    for i, doc in enumerate(relevant):
        print(f"\n[{i+1}/{len(relevant)}] {doc['title']}...", end=" ", flush=True)

        try:
            node = get_node(doc["doc_id"])
            if not node:
                print("NO DATA")
                failed += 1
                continue

            content = node.get("content", "")
            if not content:
                print("EMPTY")
                failed += 1
                continue

            # 转换 HTML 到 Markdown
            md_content = html_to_markdown(content)

            # 安全文件名
            safe_title = re.sub(r'[^a-zA-Z0-9_\- ]', '', doc['title']).strip().replace(' ', '_').lower()
            safe_title = safe_title[:60]
            filename = f"{safe_title}.md"

            filepath = os.path.join(DOCS_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {doc['title']}\n\n")
                f.write(f"**Doc ID**: {doc['doc_id']}\n")
                f.write(f"**Path**: {doc['path']}\n\n")
                f.write("---\n\n")
                f.write(md_content)
                f.write("\n")

            print(f"OK ({len(md_content):,} chars)")
            success += 1

            # 稍微延迟避免限流
            if (i + 1) % 10 == 0:
                time.sleep(1)

        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"  Results: {success} success, {failed} failed")
    print(f"  Total relevant: {len(relevant)}")
    print(f"  Saved to: {DOCS_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
