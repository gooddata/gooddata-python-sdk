# (C) 2026 GoodData Corporation
"""Per-phase latency breakdown for one evaluated run or item.

Only the agent's own response time is a property of the system under test. A single total
that also blends the judge, the simulated user and the Langfuse round trips cannot tell you
which of the four got slower.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from contextvars import ContextVar, Token
from dataclasses import dataclass

from gooddata_eval.core._output import emit_line
from gooddata_eval.core.config import env_flag

# Gates the per-turn ``[timer]`` diagnostics; off by default (see the --timers flag).
# Nothing is lost by leaving them off -- the same measurements reach every ItemReport and
# the JSON report's ``latency_breakdown_s``; these lines only show them as they happen.
TIMERS_ENV_VAR = "GD_EVAL_TIMERS"


def timers_enabled() -> bool:
    """Whether ``[timer]`` diagnostics should be emitted."""
    return env_flag(TIMERS_ENV_VAR)


def log_timer(message: str) -> None:
    """Emit one ``[timer]`` line, if timers are enabled."""
    if timers_enabled():
        emit_line(message)


@dataclass
class PhaseTimings:
    """Seconds attributed to each phase of an evaluation.

    Fields accumulate across the turns of one conversation and across the K runs of one
    item, so an item's ``agent_s`` is the sum of every agent turn it took.
    """

    # The system under test: time inside ChatClient.send_message.
    agent_s: float = 0.0
    # Our grading of the answer (LLMJudge). Post-hoc -- never blocks the agent.
    judge_s: float = 0.0
    # Our simulated user composing the next turn. On the critical path by construction:
    # the agent cannot continue until this reply exists, so unlike the judge it can only
    # be made faster, never deferred.
    simulated_user_s: float = 0.0
    # Langfuse trace lookup and score writing. Deliberately NOT part of the item's critical
    # path -- the linker records it (see agentic/_trace_linker.py) and the report fills it in
    # here, so its cost stays visible without inflating the item's own latency.
    langfuse_s: float = 0.0

    def __add__(self, other: PhaseTimings) -> PhaseTimings:
        return PhaseTimings(
            agent_s=self.agent_s + other.agent_s,
            judge_s=self.judge_s + other.judge_s,
            simulated_user_s=self.simulated_user_s + other.simulated_user_s,
            langfuse_s=self.langfuse_s + other.langfuse_s,
        )

    def as_dict(self) -> dict[str, float]:
        """Rounded mapping for the JSON report."""
        return {
            "agent_s": round(self.agent_s, 3),
            "judge_s": round(self.judge_s, 3),
            "simulated_user_s": round(self.simulated_user_s, 3),
            "langfuse_s": round(self.langfuse_s, 3),
        }


def sum_timings(timings: list[PhaseTimings]) -> PhaseTimings:
    """Total across a list of per-run timings (empty list -> all zeroes)."""
    return sum(timings, PhaseTimings())


# The percentiles every report states. P50 is the median, so it is the only "median" the
# report carries -- a second field would only repeat it.
LATENCY_PERCENTILES = (50, 70, 90, 99)


def percentile(sorted_samples: Sequence[float], p: float) -> float:
    """The ``p``-th percentile of an ascending sample, by linear interpolation.

    Linear interpolation between closest ranks (``statistics.quantiles(method="inclusive")``,
    NumPy's default), so ``percentile(xs, 50)`` equals ``statistics.median(xs)`` for any
    sample. Unlike ``statistics.quantiles`` it is defined for a single sample. On a small
    sample the high percentiles sit at or near the maximum -- they cannot report a latency
    nobody observed beyond the slowest run.
    """
    if not sorted_samples:
        raise ValueError("percentile of an empty sample")
    rank = (len(sorted_samples) - 1) * p / 100
    lower = math.floor(rank)
    upper = min(lower + 1, len(sorted_samples) - 1)
    return sorted_samples[lower] + (sorted_samples[upper] - sorted_samples[lower]) * (rank - lower)


# Share of the sample dropped from EACH end before the trimmed mean: 10% leaves the middle 80%.
TRIM_PERCENT = 10


def trimmed_mean(sorted_samples: Sequence[float], percent: int = TRIM_PERCENT) -> float | None:
    """Mean of what is left after dropping the fastest and slowest ``percent`` % of the sample.

    Not the median: the median is one middle value (P50), this still averages, but without the
    outliers at either end. ``None`` when the sample is too small to drop at least one value
    from each end (fewer than ``100 / percent`` samples) -- the figure would silently be the
    plain mean. The cut is ``n * percent // 100`` from each end, so 25 samples drop two each.
    """
    if not sorted_samples:
        raise ValueError("trimmed mean of an empty sample")
    drop = len(sorted_samples) * percent // 100
    if drop == 0:
        return None
    kept = sorted_samples[drop : len(sorted_samples) - drop]
    return sum(kept) / len(kept)


def latency_stats(samples: Iterable[float]) -> dict[str, float | None] | None:
    """Distribution of per-run latencies in seconds, or ``None`` when there are none.

    ``n`` is the number of runs the figures are over: the percentiles are only as sharp as
    that sample, and a reader needs it to judge how far to trust P99. ``trimmed_mean`` is
    ``None`` until there are enough samples to trim.
    """
    ordered = sorted(samples)
    if not ordered:
        return None
    trimmed = trimmed_mean(ordered)
    return {
        "n": len(ordered),
        "mean": round(sum(ordered) / len(ordered), 3),
        "trimmed_mean": round(trimmed, 3) if trimmed is not None else None,
        "min": round(ordered[0], 3),
        **{f"p{p}": round(percentile(ordered, p), 3) for p in LATENCY_PERCENTILES},
        "max": round(ordered[-1], 3),
    }


# The response time of every chat turn the current item completed, in order. gen-ai opens one
# trace per chat message, so these are per-trace latencies: the time from sending the message
# to the end of its stream, with none of the judge, simulated-user or conversation set-up time
# that a whole-run figure carries. `ChatClient.send_message` is the only writer; recording it
# there means no evaluator has to remember to, and a new one is covered without an edit.
_trace_latencies: ContextVar[list[float] | None] = ContextVar("gd_eval_trace_latencies", default=None)


class TraceRecorder:
    """Collects the per-trace latencies of whatever runs between ``__init__`` and ``stop``.

    Scoped to the calling thread's context, so items evaluated concurrently each get their own
    list. Create it where the item starts and call ``stop`` in a ``finally``.
    """

    def __init__(self) -> None:
        self.latencies: list[float] = []
        self._token: Token[list[float] | None] | None = _trace_latencies.set(self.latencies)

    def stop(self) -> list[float]:
        """Detach from the context and return what was recorded. Safe to call twice."""
        if self._token is not None:
            _trace_latencies.reset(self._token)
            self._token = None
        return self.latencies

    def discard(self) -> None:
        """Detach and drop what was recorded, for an item whose turns have no scored run to sit beside."""
        self.stop()
        self.latencies.clear()


def note_trace_latency(seconds: float | None) -> None:
    """Record one completed chat turn on the active recorder, if there is one.

    A no-op without a recorder (a library caller, or a test) and for a turn that carries no
    timing, so the caller never has to check either.
    """
    sink = _trace_latencies.get()
    if sink is not None and seconds is not None:
        sink.append(seconds)


def run_latency_s(timings: PhaseTimings) -> float:
    """One run's own wall time, for a single run's ``PhaseTimings``.

    Excludes ``langfuse_s`` (deliberately off the critical path -- see
    ``PhaseTimings.langfuse_s``) so this stays comparable to the single-shot path's
    ``best_run_latency_s``, which times only the agent call and its grading.
    """
    return timings.agent_s + timings.judge_s + timings.simulated_user_s
