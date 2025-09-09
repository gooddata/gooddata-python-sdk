# (C) 2025 GoodData Corporation

import time
import pytest
from gooddata_pipelines.utils.rate_limiter import RateLimiter


# ---------------------------
# Core wait + reset behavior
# ---------------------------


def test_rate_limiter_no_wait_needed():
    limiter = RateLimiter(calls_per_second=1000.0)  # Very fast limit
    waited = limiter.wait_if_needed()
    assert waited == pytest.approx(0.0, abs=0.001)


def test_rate_limiter_enforces_delay():
    limiter = RateLimiter(calls_per_second=2.0)
    limiter.wait_if_needed()
    start = time.time()
    waited = limiter.wait_if_needed()
    duration = time.time() - start

    assert waited >= 0.49
    assert duration < 0.65


def test_rate_limiter_respects_reset():
    limiter = RateLimiter(calls_per_second=1.0)
    limiter.wait_if_needed()
    limiter.reset()
    waited = limiter.wait_if_needed()
    assert waited == pytest.approx(0.0, abs=0.001)


def test_rate_limiter_min_interval_property():
    limiter = RateLimiter(calls_per_second=4.0)
    assert limiter.min_interval == pytest.approx(0.25, abs=1e-9)


# -----------------------------------------
# Decorator: shared instance (@limiter)
# -----------------------------------------


def test_rate_limiter_as_decorator_enforces_delay_shared_instance():
    limiter = RateLimiter(calls_per_second=2.0)
    ts = []

    @limiter
    def func():
        ts.append(time.time())

    func()
    func()

    assert len(ts) == 2
    assert ts[1] - ts[0] >= 0.49


def test_rate_limiter_decorator_shared_state_across_functions():
    limiter = RateLimiter(calls_per_second=2.0)
    ts = []

    @limiter
    def func_a():
        ts.append(time.time())

    @limiter
    def func_b():
        ts.append(time.time())

    func_a()
    func_b()  # should be throttled by the *same* limiter
    assert len(ts) == 2
    assert ts[1] - ts[0] >= 0.49


def test_multiple_limiters_independent_state_shared_instance_mode():
    limiter_a = RateLimiter(calls_per_second=2.0)
    limiter_b = RateLimiter(calls_per_second=2.0)

    ts_a = []
    ts_b = []

    @limiter_a
    def func_a():
        ts_a.append(time.time())

    @limiter_b
    def func_b():
        ts_b.append(time.time())

    func_a()
    func_b()

    # They should be ~simultaneous since they use different instances
    assert abs(ts_a[0] - ts_b[0]) < 0.05


# -------------------------------------------------------
# Decorator: per-function instance (@RateLimiter(...))
# -------------------------------------------------------


def test_per_function_decorator_enforces_delay_per_function():
    # Each function decorated this way gets its *own* limiter instance.
    ts = []

    @RateLimiter(calls_per_second=2.0)  # 0.5s
    def func():
        ts.append(time.time())

    func()
    func()
    assert len(ts) == 2
    assert ts[1] - ts[0] >= 0.49


def test_per_function_decorator_independent_state_between_functions():
    ts_a = []
    ts_b = []

    @RateLimiter(calls_per_second=2.0)
    def func_a():
        ts_a.append(time.time())

    @RateLimiter(calls_per_second=2.0)
    def func_b():
        ts_b.append(time.time())

    func_a()
    func_b()  # independent limiter, so no enforced delay between A and B
    assert abs(ts_a[0] - ts_b[0]) < 0.05


# -----------------------------
# Context manager usage
# -----------------------------


def test_context_manager_waits_on_enter():
    limiter = RateLimiter(calls_per_second=2.0)
    with limiter:
        t1 = time.time()
    with limiter:
        t2 = time.time()

    # The second 'with' should be at least 0.5s after the first 'with' enter
    assert t2 - t1 >= 0.49


def test_context_manager_multiple_uses_same_instance():
    limiter = RateLimiter(calls_per_second=3.0)
    times = []

    for _ in range(3):
        with limiter:
            times.append(time.time())

    intervals = [b - a for a, b in zip(times, times[1:])]
    for iv in intervals:
        assert iv >= 0.30  # a bit of slack for timing variance


def test_context_manager_propagates_exceptions():
    limiter = RateLimiter(calls_per_second=10.0)

    class Boom(Exception):
        pass

    with pytest.raises(Boom):
        with limiter:
            raise Boom("fail")
