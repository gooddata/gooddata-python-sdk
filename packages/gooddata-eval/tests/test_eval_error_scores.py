# (C) 2026 GoodData Corporation
"""Every agentic loop kind writes its Langfuse scores the same way (QA-30213, phase 1).

A run labelled ERROR gets an extra ``eval_error`` score beside its usual ones; every other run,
a chat API error included, is scored exactly as before and gets none. The visualization kind
has its own tests in test_outcome.py.
"""

from collections import defaultdict
from collections.abc import Callable, Iterator
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic import alert_skill, anomaly_detection, dashboard_skill, kda_skill, what_if
from gooddata_eval.core.agentic._outcome import RunLabels
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.models import ChatResult
from gooddata_eval.core.outcome import Outcome


@dataclass(frozen=True)
class _Kind:
    module: Any
    evaluate: Callable[..., Any]
    expected_output: dict
    simulated_user: str | None


_KINDS = {
    "alert_skill": _Kind(
        alert_skill,
        alert_skill.evaluate_agentic_alert_skill,
        {"operator": "GREATER_THAN", "threshold": 100},
        "generate_simulated_alert_response",
    ),
    "kda_skill": _Kind(
        kda_skill,
        kda_skill.evaluate_agentic_kda_skill,
        {"Measure": {"type": "metric", "id": "revenue"}},
        "generate_simulated_kda_response",
    ),
    "dashboard_skill": _Kind(
        dashboard_skill,
        dashboard_skill.evaluate_agentic_dashboard_skill,
        {
            "type": "dashboard",
            "saved_dashboard_id": None,
            "visualizations": [{"id": None, "title": "Revenue"}],
            "date_range": None,
            "min_new_visualizations": 1,
        },
        None,
    ),
    "anomaly_detection": _Kind(
        anomaly_detection,
        anomaly_detection.evaluate_agentic_anomaly_detection,
        {"metric": "metric/spend", "granularity": "MONTH"},
        "generate_simulated_anomaly_response",
    ),
    "what_if": _Kind(
        what_if,
        what_if.evaluate_agentic_what_if,
        {"metric_id": "revenue"},
        "generate_simulated_what_if_response",
    ),
}


class _ScoreCtx:
    """A RunTraceContext stand-in that keeps each run's scores apart, by run index."""

    def __init__(self) -> None:
        self.run_metadata: dict[str, Any] = {}
        self.scores: dict[int, list[tuple[str, Any, str | None]]] = defaultdict(list)

    def trace(self, _conversation_id: str) -> None:
        return None

    def run_name(self, run_idx: int) -> str:
        return f"run{run_idx}"

    @contextmanager
    def observe(self, _trace: object, run_idx: int, **_kwargs: Any) -> Iterator[int]:
        yield run_idx

    def score(self, trace_id: int, *, name: str, value: Any, data_type: str, comment: str | None = None) -> None:
        self.scores[trace_id].append((name, value, comment))

    def quality(self, trace_id: int, **_kwargs: Any) -> None:
        self.scores[trace_id].append(("quality_score", None, None))

    def names(self, run_idx: int) -> list[str]:
        return [name for name, _, _ in self.scores[run_idx]]


def _scores(kind: _Kind, labels: RunLabels | None = None) -> _ScoreCtx:
    """Run 1's chat call fails after its retries; run 2 answers without doing the task.

    ``labels`` replaces the labels the kind computes, to give run 1 a harness ERROR without
    driving each kind's own simulated-user loop."""
    client = MagicMock()
    client.create_conversation.side_effect = ["conv-1", "conv-2", "conv-3"]
    client.send_message.side_effect = [
        ChatError("gen-ai fell over"),
        ChatResult.model_validate({"textResponse": "I cannot help with that."}),
    ]
    captured: dict[str, Any] = {}

    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        captured["write_scores"] = kwargs["write_scores"]

    with ExitStack() as stack:
        stack.enter_context(patch.object(kind.module, "ChatClient", return_value=client))
        stack.enter_context(patch.object(kind.module, "submit_trace_scoring", _capture))
        if labels is not None:
            stack.enter_context(patch.object(kind.module, "label_runs", return_value=labels))
        if kind.simulated_user is not None:
            stack.enter_context(patch.object(kind.module, kind.simulated_user, return_value="please go on"))
        try:
            kind.evaluate(
                "http://host/api/v1/actions/workspaces/ws1/ai",
                "tok",
                "ws1",
                "Do the thing",
                kind.expected_output,
                k=2,
                max_iterations=1,
                langfuse=MagicMock(),
                dataset_item_id="item-1",
            )
        except AssertionError:
            pass  # the scored run fails; its scores are written before the raise
    ctx = _ScoreCtx()
    captured["write_scores"](ctx)
    return ctx


_USUAL_SCORES = {"pass_at_k", "pass_power_k", "gate_passed"}


@pytest.mark.parametrize("name", sorted(_KINDS))
def test_an_errored_run_gets_eval_error_beside_its_usual_scores(name) -> None:
    labels = RunLabels((Outcome.error("simulated_user_failed"), Outcome.failed("agent_silent")))
    ctx = _scores(_KINDS[name], labels)

    assert ("eval_error", 1, "simulated_user_failed") in ctx.scores[0]
    assert set(ctx.names(0)) >= _USUAL_SCORES
    assert "eval_error" not in ctx.names(1)
    assert set(ctx.names(1)) >= _USUAL_SCORES


@pytest.mark.parametrize("name", sorted(_KINDS))
def test_a_chat_error_run_is_scored_as_before_with_no_marker(name) -> None:
    ctx = _scores(_KINDS[name])

    for run_idx in (0, 1):
        names = ctx.names(run_idx)
        assert "eval_error" not in names
        assert set(names) >= _USUAL_SCORES
