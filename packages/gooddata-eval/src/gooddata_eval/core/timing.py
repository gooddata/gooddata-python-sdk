# (C) 2026 GoodData Corporation
"""Per-phase latency breakdown for one evaluated run or item.

Only the agent's own response time is a property of the system under test. A single total
that also blends the judge, the simulated user and the Langfuse round trips cannot tell you
which of the four got slower.
"""

from __future__ import annotations

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
