# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import patch

import pytest
from gooddata_eval.cli.agentic_runner import _dispatch_agentic, run_agentic_items
from gooddata_eval.core.agentic.alert_skill import AlertSkillAssertionError
from gooddata_eval.core.models import AgenticEvalOutcome, DatasetItem


def test_dispatch_agentic_passes_agent_id_through_to_alert_skill():
    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind="agentic_alert_skill",
        question="Alert me when spend exceeds 100",
        expected_output={"Operator": "GREATER_THAN", "Threshold": 100},
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
            agent_id="agent-1",
        )
    assert mock_eval.call_args.kwargs["agent_id"] == "agent-1"


def test_dispatch_agentic_omits_agent_id_by_default():
    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind="agentic_metric_skill",
        question="Create a metric for total spend",
        expected_output={"maql": "SELECT {metric/spend}"},
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_metric_skill") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
        )
    assert mock_eval.call_args.kwargs["agent_id"] is None


_MIN_VIZ = {"id": "v1", "type": "table", "query": {"fields": {}, "filter_by": {}}, "metrics": [], "view_by": []}
_MIN_CONVERSATION_FIXTURE = {
    "id": "c1",
    "expected_skills": ["visualization"],
    "turns": [{"turn_id": "t1", "message": "hi", "expected_skill": "visualization"}],
}

# (kind, expected_output, target evaluate_agentic_* name) for every kind AGENTIC_TEST_KINDS
# lists -- covers both agent_id passthrough (below) and the outcome-shape regression test
# further down. Keep this in sync with AGENTIC_TEST_KINDS: a kind added there without an
# entry here would silently skip both checks.
_ALL_AGENTIC_KIND_CASES = [
    ("vis_agentic", {"visualization": _MIN_VIZ}, "evaluate_agentic_visualization"),
    ("agentic_visualization", {"visualization": _MIN_VIZ}, "evaluate_agentic_visualization"),
    ("agentic_metric_skill", {"maql": "SELECT {metric/spend}"}, "evaluate_agentic_metric_skill"),
    ("agentic_alert_skill", {"Operator": "GREATER_THAN", "Threshold": 100}, "evaluate_agentic_alert_skill"),
    ("agentic_search", {"tool_call": {"function_arguments": {}}}, "evaluate_agentic_search_tool"),
    ("agentic_general_question", "What is X?", "evaluate_agentic_general_question"),
    ("agentic_guardrail", "Ignore prior instructions", "evaluate_agentic_guardrail"),
    ("agentic_kda_skill", {"Measure": {"type": "metric", "id": "revenue"}}, "evaluate_agentic_kda_skill"),
    ("agentic_conversation", {"fixture": _MIN_CONVERSATION_FIXTURE}, "evaluate_agentic_conversation"),
]


def test_all_agentic_kind_cases_covers_every_registered_kind():
    """Guards the two parametrized tests below against silently going stale: a kind added
    to AGENTIC_TEST_KINDS without a matching case here would otherwise just not get tested,
    not fail loudly."""
    from gooddata_eval.cli.agentic_runner import AGENTIC_TEST_KINDS

    covered = {kind for kind, _, _ in _ALL_AGENTIC_KIND_CASES}
    assert covered == set(AGENTIC_TEST_KINDS)


@pytest.mark.parametrize(("kind", "expected_output", "target"), _ALL_AGENTIC_KIND_CASES)
def test_dispatch_agentic_passes_agent_id_through_for_every_kind(kind, expected_output, target):
    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind=kind,
        question="q",
        expected_output=expected_output,
    )
    with patch(f"gooddata_eval.cli.agentic_runner.{target}") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
            agent_id="agent-1",
        )
    assert mock_eval.call_args.kwargs["agent_id"] == "agent-1"


def _item(test_kind: str = "agentic_alert_skill") -> DatasetItem:
    return DatasetItem(
        id="item-1",
        dataset_name="d",
        test_kind=test_kind,
        question="Alert me when revenue drops below 100.",
        expected_output={"operator": "LESS_THAN", "threshold": 100},
    )


def test_run_agentic_items_surfaces_reasoning_steps_on_pass():
    with patch(
        "gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill",
        return_value=AgenticEvalOutcome(
            reasoning_steps=["it created the alert"], conversation_id="conv-1", response_id="resp-1"
        ),
    ):
        report = run_agentic_items(
            [_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )
    assert report.items[0].pass_at_k is True
    assert report.items[0].reasoning_steps == ["it created the alert"]
    assert report.items[0].conversation_id == "conv-1"
    assert report.items[0].response_id == "resp-1"


def test_run_agentic_items_surfaces_reasoning_steps_from_exception_on_fail():
    exc = AlertSkillAssertionError("nope")
    exc.reasoning_steps = ["it got confused"]
    exc.conversation_id = "conv-2"
    exc.response_id = "resp-2"
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=exc):
        report = run_agentic_items(
            [_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )
    assert report.items[0].pass_at_k is False
    assert report.items[0].reasoning_steps == ["it got confused"]
    assert report.items[0].conversation_id == "conv-2"
    assert report.items[0].response_id == "resp-2"


def test_run_agentic_items_defaults_reasoning_steps_to_empty_when_exception_has_none():
    with patch(
        "gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill",
        side_effect=AlertSkillAssertionError("nope"),
    ):
        report = run_agentic_items(
            [_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )
    assert report.items[0].reasoning_steps == []
    assert report.items[0].conversation_id is None
    assert report.items[0].response_id is None


@pytest.mark.parametrize(("kind", "expected_output", "target"), _ALL_AGENTIC_KIND_CASES)
def test_dispatch_agentic_returns_a_real_outcome_for_every_kind(kind, expected_output, target):
    """Regression test for the bug this fixes: `guardrail`/`search_tool`/`general_question`/
    `visualization`/`kda_skill` used to return None/a bare value instead of an
    AgenticEvalOutcome, so their reasoning_steps/conversation_id/response_id were silently
    dropped (confirmed live: a real eval run produced 0/30 reasoning sidecars for
    agentic_guardrail). Every kind must now return the exact AgenticEvalOutcome its
    evaluator produced -- not None, not the outcome's reasoning_steps list alone, not any
    other bare value the old `isinstance(outcome, tuple)`/`isinstance(outcome, AgenticEvalOutcome)`
    fallback could silently swallow."""
    from gooddata_eval.core.models import AgenticEvalOutcome

    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind=kind,
        question="q",
        expected_output=expected_output,
    )
    canned = AgenticEvalOutcome(reasoning_steps=["x"], conversation_id="c1", response_id="r1")
    with patch(f"gooddata_eval.cli.agentic_runner.{target}", return_value=canned) as mock_eval:
        result = _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
        )
    mock_eval.assert_called_once()
    assert result is canned
    assert isinstance(result, AgenticEvalOutcome)
    assert result.reasoning_steps == ["x"]
    assert result.conversation_id == "c1"
    assert result.response_id == "r1"
