"""
梯度增时重试工具
"""
import asyncio
from typing import Callable, TypeVar, ParamSpec
from loguru import logger
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")


class RetryRunner:
    """
    梯度增时重试

    延迟序列：base_delay * (multiplier ^ attempt)
    示例：base=10s, multiplier=2.0
      → 第1次重试：10s
      → 第2次重试：20s
      → 第3次重试：40s
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 10.0,
        multiplier: float = 2.0,
        on_retry: Callable[[Exception, int], None] = None,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.multiplier = multiplier
        self.on_retry = on_retry

    def delay(self, attempt: int) -> float:
        """第 N 次重试的延迟秒数"""
        return self.base_delay * (self.multiplier ** attempt)

    async def run(self, fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        """异步重试入口"""
        last_error: Exception = None
        for attempt in range(self.max_retries):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait = self.delay(attempt)
                    logger.warning(f"[Retry] attempt {attempt+1} failed: {e}, retry in {wait:.1f}s")
                    if self.on_retry:
                        self.on_retry(e, attempt)
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"[Retry] all {self.max_retries} attempts failed")

        raise last_error

    def run_sync(self, fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        """同步重试入口（用于 Celery Task）"""
        import time
        last_error: Exception = None
        for attempt in range(self.max_retries):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait = self.delay(attempt)
                    logger.warning(f"[Retry] attempt {attempt+1} failed: {e}, retry in {wait:.1f}s")
                    if self.on_retry:
                        self.on_retry(e, attempt)
                    time.sleep(wait)
                else:
                    logger.error(f"[Retry] all {self.max_retries} attempts failed")
        raise last_error


def with_retry(
    max_retries: int = 3,
    base_delay: float = 10.0,
    multiplier: float = 2.0,
):
    """装饰器：为异步函数添加重试逻辑"""
    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        @wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            runner = RetryRunner(max_retries=max_retries, base_delay=base_delay, multiplier=multiplier)
            return await runner.run(fn, *args, **kwargs)
        return wrapper
    return decorator
