"""
清理抓取的 TikTok API 文档，去掉 browser-use state 的标签和导航菜单
"""
import os
import re

DOCS_DIR = r"E:\code\tiktok-ads-system\docs\tiktok-api"


def clean_doc(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    lines = raw.split('\n')

    # 提取头部（标题、doc_id、source、分隔线）
    header_lines = []
    content_start = 0
    for i, line in enumerate(lines):
        header_lines.append(line)
        if line.strip() == '---':
            content_start = i + 1
            break

    # 处理内容部分
    content_lines = lines[content_start:]
    cleaned = []
    in_nav = True  # 开始时在导航菜单区域
    seen = set()

    for line in content_lines:
        stripped = line.strip()

        # 跳过空行（但保留它们用于段落分隔）
        if not stripped:
            if cleaned and cleaned[-1] != '':
                cleaned.append('')
            continue

        # 跳过 browser-use state 元数据
        if any(stripped.startswith(prefix) for prefix in [
            'viewport:', 'page:', 'scroll:', '|scroll element',
            'scrolled:', 'amount:', 'url:', 'clicked:',
        ]):
            continue

        # 跳过 SVG 注释
        if '<!-- SVG content collapsed -->' in stripped:
            continue

        # 去掉元素标签标记: [123]<div /> 或 *[123]<span /> 等
        clean = re.sub(r'^\s*\*?\[?\d+\]<[^>]+/?>\s*', '', stripped)

        # 去掉 *[123]<xxx /> 行（纯标签行，没有文本）
        if not clean or clean == stripped and re.match(r'^\*?\[\d+\]<', stripped):
            continue

        clean = clean.strip()
        if not clean or len(clean) < 2:
            continue

        # 检测导航菜单结束
        # 导航菜单特征：短文本、标题类（About the Guide, Overview, Marketing API 等）
        if in_nav:
            nav_patterns = [
                'About the Guide', 'Overview', "What's New", 'Get Started',
                'FAQs', 'Use Cases', 'Marketing API', 'Organic API',
                'Business Messaging API', 'API Reference', 'API Playground',
                'API Service Status Page', 'SDK', 'Appendix',
                'Business Center', 'Creatives', 'Catalog Management',
                'TikTok Store', 'Campaign Management', 'Guides',
                'Audience Management', 'Reporting', 'Ad Measurement',
                'Campaign', 'Ad group', 'Ad', 'Get started',
            ]
            # 如果这行是长文本（>80字符），说明已经进入正文
            if len(clean) > 80:
                in_nav = False
            elif clean in nav_patterns:
                continue
            # 如果遇到短的但不在导航列表里的，也可能是正文标题
            elif len(clean) > 20 and clean not in nav_patterns:
                in_nav = False

        if in_nav:
            continue

        # 去重
        if clean in seen and len(clean) < 60:
            continue
        seen.add(clean)

        # 跳过 UI 元素
        if clean in ['Yes', 'No', 'EN', 'Log in', 'Was the information helpful?']:
            continue

        # 跳过页脚
        if '2026 TikTok for Business' in clean or 'Terms & policies' in clean or 'Privacy & cookie policy' in clean:
            continue

        cleaned.append(clean)

    # 组合最终文档
    header = '\n'.join(header_lines)
    body = '\n'.join(cleaned)

    # 进一步格式化：连续的单行文本合并为段落
    body = re.sub(r'\n(?!\n|#|-|\||```)', ' ', body)
    # 恢复标题和列表前的换行
    body = re.sub(r' (#{1,6} )', r'\n\n\1', body)
    body = re.sub(r' (- )', r'\n\1', body)
    body = re.sub(r' (\| )', r'\n\1', body)

    result = header + '\n\n' + body.strip() + '\n'
    return result


def main():
    files = sorted(f for f in os.listdir(DOCS_DIR) if f.endswith('.md'))
    print(f"Cleaning {len(files)} files in {DOCS_DIR}\n")

    for fname in files:
        filepath = os.path.join(DOCS_DIR, fname)
        try:
            cleaned = clean_doc(filepath)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            print(f"  ✅ {fname}: {len(cleaned):,} chars")
        except Exception as e:
            print(f"  ❌ {fname}: {e}")

    print("\nDone!")


if __name__ == "__main__":
    main()
