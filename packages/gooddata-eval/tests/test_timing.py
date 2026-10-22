# (C) 2026 GoodData Corporation
"""Tests for PhaseTimings and the [timer] diagnostic gate."""

import statistics
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import pytest
from gooddata_eval.core.timing import (
    TIMERS_ENV_VAR,
    PhaseTimings,
    TraceRecorder,
    latency_stats,
    log_timer,
    note_trace_latency,
    percentile,
    sum_timings,
    timers_enabled,
    trimmed_mean,
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

    assert stats == {
        "n": 4,
        "mean": 2.5,
        "trimmed_mean": None,
        "min": 1.0,
        "p50": 2.5,
        "p70": 3.1,
        "p90": 3.7,
        "p99": 3.97,
        "max": 4.0,
    }


def test_latency_stats_never_decreases_from_p50_to_max():
    stats = latency_stats([0.4, 12.0, 3.3, 3.3, 7.9, 0.9, 21.5])

    ladder = [stats[k] for k in ("min", "p50", "p70", "p90", "p99", "max")]
    assert ladder == sorted(ladder)


def test_latency_stats_of_one_run_collapses_to_that_run():
    stats = latency_stats([3.25])

    assert stats == {
        "n": 1,
        "mean": 3.25,
        "trimmed_mean": None,
        "min": 3.25,
        "p50": 3.25,
        "p70": 3.25,
        "p90": 3.25,
        "p99": 3.25,
        "max": 3.25,
    }


def test_trimmed_mean_drops_the_fastest_and_slowest_tenth_before_averaging():
    # Ten samples drop one from each end: the 0.1s and the 100s no longer move the average.
    samples = [0.1, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 100.0]

    assert trimmed_mean(samples) == pytest.approx(2.0)
    assert sum(samples) / len(samples) == pytest.approx(11.61)  # the plain mean is dragged far above it


def test_trimmed_mean_is_not_the_median():
    # The median is one middle value; the trimmed mean still averages what is left, so the two
    # differ whenever the middle 80% is not symmetric.
    samples = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 9.0, 9.0]

    assert statistics.median(samples) == 1.0
    assert trimmed_mean(samples) == pytest.approx(2.0)


@pytest.mark.parametrize(("n", "dropped_each_end"), [(10, 1), (19, 1), (20, 2), (25, 2), (100, 10)])
def test_trimmed_mean_cut_is_the_floor_of_a_tenth_of_the_sample_per_end(n, dropped_each_end):
    samples = [float(i) for i in range(n)]

    kept = samples[dropped_each_end : n - dropped_each_end]
    assert trimmed_mean(samples) == pytest.approx(sum(kept) / len(kept))


@pytest.mark.parametrize("n", [1, 2, 5, 9])
def test_trimmed_mean_is_none_when_nothing_can_be_trimmed(n):
    # Below ten samples a 10% trim removes nothing, so the figure would just be the plain mean
    # under a name that promises otherwise.
    assert trimmed_mean([float(i) for i in range(n)]) is None


def test_trimmed_mean_of_an_empty_sample_raises():
    with pytest.raises(ValueError, match="empty"):
        trimmed_mean([])


def test_latency_stats_carries_the_trimmed_mean_once_there_are_ten_samples():
    stats = latency_stats([100.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.1])

    assert stats["trimmed_mean"] == 2.0
    assert stats["mean"] == 11.61


def test_a_recorder_collects_each_noted_trace_in_order():
    recorder = TraceRecorder()
    for seconds in (1.5, 0.5, 2.0):
        note_trace_latency(seconds)

    assert recorder.stop() == [1.5, 0.5, 2.0]


def test_noting_a_trace_with_no_recorder_is_a_no_op():
    # A library caller or a test has no recorder; the chat client still calls this.
    note_trace_latency(3.0)


def test_a_turn_without_timing_is_not_recorded():
    recorder = TraceRecorder()
    note_trace_latency(None)

    assert recorder.stop() == []


def test_stopping_detaches_the_recorder_and_is_safe_twice():
    recorder = TraceRecorder()
    note_trace_latency(1.0)
    assert recorder.stop() == [1.0]

    note_trace_latency(9.0)  # after stop: nobody is listening

    assert recorder.stop() == [1.0]


def test_discarding_drops_what_was_recorded_and_detaches():
    recorder = TraceRecorder()
    note_trace_latency(1.0)

    recorder.discard()
    note_trace_latency(9.0)  # after discard: nobody is listening

    assert recorder.stop() == []


def test_concurrent_items_each_record_only_their_own_traces():
    """Items run in worker threads under --concurrency; one item's turns must never land in
    another's list."""

    def item(base: float) -> list[float]:
        recorder = TraceRecorder()
        try:
            for step in range(5):
                note_trace_latency(base + step)
        finally:
            recorded = recorder.stop()
        return recorded

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(item, [0.0, 100.0, 200.0, 300.0]))

    assert results == [[b + s for s in range(5)] for b in (0.0, 100.0, 200.0, 300.0)]
