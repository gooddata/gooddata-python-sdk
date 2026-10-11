# (C) 2026 GoodData Corporation
"""Tests for PhaseTimings and the [timer] diagnostic gate."""

import statistics
import threading
from unittest.mock import patch

import pytest
from gooddata_eval.core.timing import (
    TIMERS_ENV_VAR,
    PhaseTimings,
    latency_stats,
    log_timer,
    percentile,
    sum_timings,
    timers_enabled,
)


def test_timers_are_off_by_default(monkeypatch):
    # An 18-item --runs 2 run emits 72 [timer] lines, burying the per-item progress
    # output. The numbers survive in latency_breakdown_s either way, so the prints are
    # opt-in diagnostics.
    monkeypatch.delenv(TIMERS_ENV_VAR, raising=False)
    assert timers_enabled() is False


@pytest.mark.parametrize(
    ("value", "expected"),
    [("1", True), ("true", True), ("YES", True), ("on", True), ("0", False), ("false", False), ("", False)],
)
def test_timers_env_var_parsing_treats_explicit_off_values_as_off(monkeypatch, value, expected):
    # Same trap that silently disabled trace linking: bool("0") is True in Python, so a
    # bare truthiness check reads GD_EVAL_TIMERS=0 as ON.
    monkeypatch.setenv(TIMERS_ENV_VAR, value)
    assert timers_enabled() is expected


def test_log_timer_prints_nothing_when_disabled(monkeypatch):
    monkeypatch.setenv(TIMERS_ENV_VAR, "0")
    printed: list[str] = []
    with patch("sys.stdout") as out:
        out.write.side_effect = printed.append
        log_timer("[timer] should not appear")

    assert printed == []


def test_log_timer_emits_one_write_when_enabled(monkeypatch):
    # One write, not print()'s two (text then newline): these lines are emitted from
    # trace-link worker threads' peers and must not interleave mid-line with progress.
    monkeypatch.setenv(TIMERS_ENV_VAR, "1")
    printed: list[str] = []
    with patch("sys.stdout") as out:
        out.write.side_effect = printed.append
        log_timer("[timer] hello")

    assert printed == ["[timer] hello\n"]


def test_log_timer_is_safe_from_several_threads(monkeypatch):
    monkeypatch.setenv(TIMERS_ENV_VAR, "1")
    errors: list[BaseException] = []

    def emit() -> None:
        try:
            for _ in range(20):
                log_timer("[timer] concurrent")
        except BaseException as exc:  # noqa: BLE001 - recorded, asserted below
            errors.append(exc)

    threads = [threading.Thread(target=emit) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == []


def test_phase_timings_add_is_fieldwise():
    a = PhaseTimings(agent_s=1.0, judge_s=2.0)
    b = PhaseTimings(agent_s=0.5, simulated_user_s=3.0, langfuse_s=4.0)
    total = a + b

    assert (total.agent_s, total.judge_s, total.simulated_user_s, total.langfuse_s) == (1.5, 2.0, 3.0, 4.0)


def test_as_dict_rounds_every_phase():
    timings = PhaseTimings(agent_s=1.23456, judge_s=2.0, simulated_user_s=0.0, langfuse_s=31.5)

    assert timings.as_dict() == {"agent_s": 1.235, "judge_s": 2.0, "simulated_user_s": 0.0, "langfuse_s": 31.5}


def test_sum_timings_of_nothing_is_all_zeroes():
    assert sum_timings([]) == PhaseTimings()


def test_percentile_interpolates_between_closest_ranks():
    # rank = 0.9 * 3 = 2.7 -> 3.0 + 0.7 * (4.0 - 3.0)
    assert percentile([1.0, 2.0, 3.0, 4.0], 90) == pytest.approx(3.7)


@pytest.mark.parametrize("n", [1, 2, 3, 4, 7, 10, 99])
def test_p50_is_the_median_for_any_sample_size(n):
    # The report prints P50 as the median and carries no separate median field, so the
    # two must never disagree -- nearest-rank would differ on every even-sized sample.
    samples = [float(i * i) for i in range(1, n + 1)]

    assert percentile(samples, 50) == pytest.approx(statistics.median(samples))


def test_percentile_of_a_single_sample_is_that_sample():
    assert percentile([2.5], 99) == 2.5


def test_percentile_of_an_empty_sample_raises():
    with pytest.raises(ValueError, match="empty"):
        percentile([], 50)


def test_latency_stats_of_nothing_is_none():
    # None rather than zeroes: a run with no timed runs has no latency, not a 0s one.
    assert latency_stats([]) is None


def test_latency_stats_orders_an_unsorted_sample_and_reports_every_figure():
    stats = latency_stats([4.0, 1.0, 3.0, 2.0])

    assert stats == {"n": 4, "mean": 2.5, "min": 1.0, "p50": 2.5, "p70": 3.1, "p90": 3.7, "p99": 3.97, "max": 4.0}


def test_latency_stats_never_decreases_from_p50_to_max():
    stats = latency_stats([0.4, 12.0, 3.3, 3.3, 7.9, 0.9, 21.5])

    ladder = [stats[k] for k in ("min", "p50", "p70", "p90", "p99", "max")]
    assert ladder == sorted(ladder)


def test_latency_stats_of_one_run_collapses_to_that_run():
    stats = latency_stats([3.25])

    assert stats == {"n": 1, "mean": 3.25, "min": 3.25, "p50": 3.25, "p70": 3.25, "p90": 3.25, "p99": 3.25, "max": 3.25}
