# (C) 2026 GoodData Corporation
"""Whether an eval kind sends one chat message per run or drives a whole conversation.

The distinction decides what a latency figure means. gen-ai starts one trace per chat message
(its session is the conversation), so a single-shot run is exactly one trace and its latency
is that trace's response time, while a multi-turn run spans several traces and has both a
per-trace and a whole-conversation latency. The report keeps the two apart for that reason.

The classification is by kind, not by how many turns a particular run happened to take: an item
belongs to exactly one section however its runs went.
"""

from __future__ import annotations

from typing import Literal

InteractionMode = Literal["single_shot", "multi_turn"]

SINGLE_SHOT: InteractionMode = "single_shot"
MULTI_TURN: InteractionMode = "multi_turn"
INTERACTION_MODES: tuple[InteractionMode, ...] = (SINGLE_SHOT, MULTI_TURN)

# Agentic kinds that still send exactly one chat message per run: no simulated user, no
# follow-up turns. Named explicitly, and checked against the runner's full list in the tests,
# so a new agentic kind cannot be classified by accident.
SINGLE_TURN_AGENTIC_KINDS = frozenset(
    {
        "agentic_general_question",
        "agentic_guardrail",
        "agentic_search",
        "agentic_dashboard_summary",
    }
)

# Kinds that drive a simulated user or fixture turns until the agent has produced its output.
MULTI_TURN_KINDS = frozenset(
    {
        "vis_agentic",
        "agentic_visualization",
        "agentic_metric_skill",
        "agentic_alert_skill",
        "agentic_dashboard_skill",
        "agentic_document_skill",
        "agentic_conversation",
        "agentic_kda_skill",
        "agentic_anomaly_detection",
        "agentic_what_if",
    }
)


def interaction_mode(test_kind: str) -> InteractionMode:
    """Single-shot unless the kind is one of the multi-turn ones.

    Every non-agentic kind sends one chat message (or one summary request), so the default is
    the safe side for them.
    """
    return MULTI_TURN if test_kind in MULTI_TURN_KINDS else SINGLE_SHOT
