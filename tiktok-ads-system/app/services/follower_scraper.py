"""
TikTok 粉丝数爬虫 — Playwright 方案

策略：真实浏览器渲染，访问 TikTok 主页解析粉丝数
- 支持大规模账号（批次 + 间隔防封）
- 随机 User-Agent
- 每批次之间延迟
"""
from playwright.sync_api import sync_playwright
from loguru import logger
from typing import Optional, List, Dict
import re
import time
import random


class TikTokFollowerScraper:
    """
    TikTok 粉丝数爬虫（Playwright 方案）
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    ]

    def __init__(
        self,
        interval: float = 2.5,
        batch_size: int = 10,
        batch_delay: float = 10.0,
        max_retries: int = 2,
        headless: bool = True,
    ):
        self.interval = interval
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.max_retries = max_retries
        self.headless = headless

    def _random_ua(self) -> str:
        return random.choice(self.USER_AGENTS)

    def get_follower_count(self, username: str) -> Optional[int]:
        """
        获取单个账号粉丝数
        """
        username = username.lstrip("@")
        url = f"https://www.tiktok.com/@{username}"

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(
                    headless=self.headless,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                    ],
                )
                context = browser.new_context(
                    user_agent=self._random_ua(),
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                    timezone_id="America/New_York",
                )
                page = context.new_page()

                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(4000)

                count = self._extract(page)

                page.close()
                context.close()
                browser.close()
                return count

            except Exception as e:
                logger.debug(f"[Scraper] @{username} error: {e}")
                return None

    def get_follower_counts_batch(self, usernames: List[str]) -> Dict[str, Optional[int]]:
        """
        批量获取粉丝数（支持大规模）
        """
        results = {}
        total = len(usernames)

        for i, username in enumerate(usernames):
            username = username.lstrip("@")
            count = self.get_follower_count(username)
            results[username] = count

            status = f"{count:,}" if count is not None else "FAILED"
            logger.info(f"[Scraper] [{i+1}/{total}] @{username}: {status}")

            if i < total - 1:
                sleep = self.interval + random.uniform(0, 1.5)
                time.sleep(sleep)

        return results

    def _extract(self, page) -> Optional[int]:
        """从页面提取粉丝数"""
        try:
            content = page.content()
            patterns = [
                r'"followerCount"\s*:\s*(\d+)',
                r'"follower_count"\s*:\s*(\d+)',
                r'"fansCount"\s*:\s*(\d+)',
            ]
            for p in patterns:
                m = re.search(p, content)
                if m:
                    return int(m.group(1))

            selectors = [
                '[data-e2e="follower-count"]',
                '[data-e2e="followers-count"]',
                'strong[data-e2e="followers"]',
                'span[data-e2e="followers"]',
            ]
            for sel in selectors:
                try:
                    el = page.locator(sel).first
                    if el.count() > 0:
                        txt = el.inner_text()
                        nums = re.findall(r"[\d,]+", txt.replace(",", ""))
                        if nums and int(nums[0]) > 0:
                            return int(nums[0].replace(",", ""))
                except Exception:
                    pass

            try:
                body_text = page.inner_text("body")
                m = re.search(r"Fans?\s*([\d,]+)", body_text, re.IGNORECASE)
                if m:
                    return int(m.group(1).replace(",", ""))
            except Exception:
                pass

        except Exception as e:
            logger.debug(f"[Scraper] extract error: {e}")

        return None


# 同步入口（供 Celery Task 调用）
def sync_get_followers(usernames: List[str]) -> Dict[str, Optional[int]]:
    scraper = TikTokFollowerScraper()
    return scraper.get_follower_counts_batch(usernames)


def sync_get_follower_count(username: str) -> Optional[int]:
    scraper = TikTokFollowerScraper()
    return scraper.get_follower_count(username)
