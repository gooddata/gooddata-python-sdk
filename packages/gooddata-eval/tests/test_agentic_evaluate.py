# (C) 2026 GoodData Corporation
"""Tests for the evaluate_agentic_* orchestrators across all agentic kinds.

Each orchestrator: runs run_agentic_*, optionally logs to Langfuse, and raises a
kind-specific AssertionError when pass_at_k is False. The run function and
Langfuse are mocked — no network.
"""
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from gooddata_eval.core.agentic import (
    alert_skill,
    general_question,
    guardrail,
    metric_skill,
    search_tool,
)

# (module, run_fn_name, error_class, expected_kwarg, expected_value)
_CASES = [
    (metric_skill, "run_agentic_metric_skill", "MetricSkillAssertionError", "expected_output", {"maql": "x"}),
    (alert_skill, "run_agentic_alert_skill", "AlertSkillAssertionError", "expected_output", {"Operator": "LESS_THAN"}),
    (search_tool, "run_agentic_search_tool", "SearchToolAssertionError", "expected_tool_call", {"keywords": ["x"]}),
    (general_question, "run_agentic_general_question", "GeneralQuestionAssertionError", "expected_output", "an answer"),
    (guardrail, "run_agentic_guardrail", "GuardrailAssertionError", "expected_output", "a refusal"),
]


def _call(module, expected_kwarg, expected_value):
    evaluate = getattr(module, f"evaluate_agentic_{module.__name__.split('.')[-1]}")
    return evaluate, {
        "host": "h",
        "token": "t",
        "workspace_id": "ws",
        "question": "q",
        expected_kwarg: expected_value,
        # langfuse non-None but empty dataset_item_id → langfuse branch is skipped.
        "langfuse": MagicMock(),
        "dataset_item_id": "",
    }


@pytest.mark.parametrize("module, run_fn, err, kw, val", _CASES)
def test_evaluate_passes_without_raising(module, run_fn, err, kw, val):
    evaluate, kwargs = _call(module, kw, val)
    with patch.object(module, run_fn, return_value=SimpleNamespace(pass_at_k=True, run_results=[])):
        assert evaluate(**kwargs) is None  # pass → no raise


@pytest.mark.parametrize("module, run_fn, err, kw, val", _CASES)
def test_evaluate_raises_on_failure(module, run_fn, err, kw, val):
    evaluate, kwargs = _call(module, kw, val)
    # best uses MagicMock so any kind-specific attribute the error message reads
    # resolves to a str-able value.
    fake_summary = SimpleNamespace(pass_at_k=False, run_results=[], best=MagicMock())
    error_class = getattr(module, err)
    with patch.object(module, run_fn, return_value=fake_summary):
        with pytest.raises(error_class):
            evaluate(**kwargs)


def test_evaluate_general_question_logs_to_langfuse():
    """The Langfuse branch runs when a client and dataset_item_id are present."""
    run = SimpleNamespace(conversation_id="c1", passed=True, llm_judge_score=0.9)
    summary = SimpleNamespace(pass_at_k=True, run_results=[run], best=SimpleNamespace(passed=True))
    fake_lf = MagicMock()
    trace = SimpleNamespace(id="trace-1", latency=2.0, total_cost=0.01)

    with (
        patch.object(general_question, "run_agentic_general_question", return_value=summary),
        patch("gooddata_eval.core.agentic._langfuse.build_run_context", return_value=("base", {})),
        patch("gooddata_eval.core.agentic._langfuse.find_traces_per_conversation", return_value={"c1": trace}),
        patch("gooddata_eval.core.agentic._langfuse.log_quality_and_value_scores") as mock_logqv,
        patch("gooddata_eval.core.agentic._langfuse.score_safe") as mock_score,
    ):
        general_question.evaluate_agentic_general_question(
            host="h",
            token="t",
            workspace_id="ws",
            question="q",
            expected_output="an answer",
            langfuse=fake_lf,
            dataset_item_id="item-1",
        )

    assert mock_score.called
    assert mock_logqv.called
