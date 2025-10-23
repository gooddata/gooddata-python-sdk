# (C) 2025 GoodData Corporation

import time
import threading
import functools
from typing import Callable, Any, Literal


class RateLimiter:
    """
    Rate limiter usable as a decorator and as a context manager.
      - Shared instance decorator:   limiter = RateLimiter(); @limiter
      - Per-function decorator:      @RateLimiter(calls_per_second=2)
      - Context manager:             with RateLimiter(2): ...
    """

    def __init__(self, calls_per_second: float = 1.0) -> None:
        if calls_per_second <= 0:
            raise ValueError("calls_per_second must be greater than 0")

        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second

        self._lock = threading.Lock()
        self._last_call_time = 0.0

    def wait_if_needed(self) -> float:
        """Sleep if needed to maintain the rate limit, return actual sleep time."""
        with self._lock:
            now = time.monotonic()
            since_last = now - self._last_call_time

            if since_last < self.min_interval:
                sleep_time = self.min_interval - since_last
                time.sleep(sleep_time)
                self._last_call_time = time.monotonic()
                return sleep_time
            else:
                self._last_call_time = now
                return 0.0

    # Decorator support
    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.wait_if_needed()
            return func(*args, **kwargs)

        return wrapper

    # Context manager support
    def __enter__(self) -> "RateLimiter":
        self.wait_if_needed()
        return self

    def __exit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> Literal[False]:
        return False

    def reset(self) -> None:
        """Reset the limiter (useful in tests)."""
        with self._lock:
            self._last_call_time = 0.0
