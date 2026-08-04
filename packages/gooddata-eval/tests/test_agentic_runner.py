# (C) 2026 GoodData Corporation. All rights reserved.
from unittest.mock import patch

import pytest
from gooddata_eval.cli.agentic_runner import _dispatch_agentic
from gooddata_eval.core.models import DatasetItem


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


@pytest.mark.parametrize(
    ("kind", "expected_output", "target"),
    [
        ("vis_agentic", {"visualization": _MIN_VIZ}, "evaluate_agentic_visualization"),
        ("agentic_visualization", {"visualization": _MIN_VIZ}, "evaluate_agentic_visualization"),
        ("agentic_search", {"tool_call": {"function_arguments": {}}}, "evaluate_agentic_search_tool"),
        ("agentic_general_question", "What is X?", "evaluate_agentic_general_question"),
        ("agentic_guardrail", "Ignore prior instructions", "evaluate_agentic_guardrail"),
        ("agentic_conversation", {"fixture": _MIN_CONVERSATION_FIXTURE}, "evaluate_agentic_conversation"),
    ],
)
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
