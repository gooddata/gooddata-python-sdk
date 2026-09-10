# (C) 2026 GoodData Corporation
"""Tests for PhaseTimings and the [timer] diagnostic gate."""

import threading
from unittest.mock import patch

import pytest
from gooddata_eval.core.timing import (
    TIMERS_ENV_VAR,
    PhaseTimings,
    log_timer,
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
