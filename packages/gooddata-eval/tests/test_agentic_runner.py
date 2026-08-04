# (C) 2026 GoodData Corporation
import pytest
from gooddata_eval.cli import agentic_runner as runner_mod
from gooddata_eval.cli.agentic_runner import _dispatch_agentic
from gooddata_eval.core.models import DatasetItem

_MINIMAL_EXPECTED_OUTPUT = {
    "vis_agentic": {"visualization": {"id": "v1", "type": "column_chart", "query": {"fields": {}}}},
    "agentic_visualization": {"visualization": {"id": "v1", "type": "column_chart", "query": {"fields": {}}}},
    "agentic_metric_skill": {},
    "agentic_alert_skill": {},
    "agentic_search": {},
    "agentic_general_question": "some expected text",
    "agentic_guardrail": "some expected text",
    "agentic_conversation": {"id": "conv1", "expected_skills": [], "turns": []},
}

_EVALUATE_FN_NAME = {
    "vis_agentic": "evaluate_agentic_visualization",
    "agentic_visualization": "evaluate_agentic_visualization",
    "agentic_metric_skill": "evaluate_agentic_metric_skill",
    "agentic_alert_skill": "evaluate_agentic_alert_skill",
    "agentic_search": "evaluate_agentic_search_tool",
    "agentic_general_question": "evaluate_agentic_general_question",
    "agentic_guardrail": "evaluate_agentic_guardrail",
    "agentic_conversation": "evaluate_agentic_conversation",
}


@pytest.mark.parametrize("kind", sorted(_MINIMAL_EXPECTED_OUTPUT))
def test_dispatch_agentic_forwards_reasoning_effort(monkeypatch, kind):
    """Every agentic kind must forward reasoning_effort to its evaluate_agentic_* function."""
    captured: dict = {}

    def _fake_evaluate(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(runner_mod, _EVALUATE_FN_NAME[kind], _fake_evaluate)

    item = DatasetItem(
        id="i1",
        dataset_name="d",
        test_kind=kind,
        question="q",
        expected_output=_MINIMAL_EXPECTED_OUTPUT[kind],
    )

    _dispatch_agentic(item, "https://h", "tok", "ws", 1, None, "run-ts", None, reasoning_effort="HIGH")

    assert captured.get("reasoning_effort") == "HIGH"


def test_dispatch_agentic_defaults_reasoning_effort_to_none(monkeypatch):
    captured: dict = {}

    def _fake_evaluate(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(runner_mod, "evaluate_agentic_guardrail", _fake_evaluate)

    item = DatasetItem(
        id="i1", dataset_name="d", test_kind="agentic_guardrail", question="q", expected_output="expected"
    )

    _dispatch_agentic(item, "https://h", "tok", "ws", 1, None, "run-ts", None)

    assert captured.get("reasoning_effort") is None
