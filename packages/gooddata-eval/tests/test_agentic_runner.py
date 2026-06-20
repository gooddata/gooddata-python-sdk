# (C) 2026 GoodData Corporation
"""Tests for the multi-turn agentic evaluation runner (cli/agentic_runner.py).

This is a separate evaluation path from the single-turn `run_items` runner: it
serves the agentic test kinds (vis_agentic, agentic_*), routing each to its
`evaluate_agentic_*` function. Here we cover the pure expected_output parser and
the dispatch routing with the evaluators mocked.
"""
from unittest.mock import patch

import pytest

from gooddata_eval.cli.agentic_runner import (
    AGENTIC_TEST_KINDS,
    _dispatch_agentic,
    _parse_visualization_expected,
)
from gooddata_eval.core.models import DatasetItem


def _viz(id_="v1"):
    return {
        "id": id_,
        "type": "column_chart",
        "query": {"fields": {"m_rev": {"using": "metric/revenue"}}, "filter_by": {}},
        "metrics": ["m_rev"],
        "view_by": [],
    }


def test_parse_visualization_expected_outputs_format():
    out = _parse_visualization_expected({"expected_outputs": [{"visualization": _viz("a")}, {"visualization": _viz("b")}]})
    assert [v.id for v in out] == ["a", "b"]


def test_parse_visualization_single_dict():
    out = _parse_visualization_expected({"visualization": _viz("solo")})
    assert len(out) == 1 and out[0].id == "solo"


def test_parse_visualization_multi_list_under_key():
    out = _parse_visualization_expected({"visualization": [_viz("a"), _viz("b")]})
    assert [v.id for v in out] == ["a", "b"]


def test_parse_visualization_bare_list():
    out = _parse_visualization_expected([{"visualization": _viz("a")}, _viz("b")])
    assert [v.id for v in out] == ["a", "b"]


def test_parse_visualization_invalid_type_raises():
    with pytest.raises(ValueError, match="Cannot parse agentic_visualization"):
        _parse_visualization_expected("not a viz")


def _dispatch(item: DatasetItem):
    _dispatch_agentic(
        item,
        host="h",
        token="t",
        workspace_id="ws",
        k=1,
        langfuse=None,
        run_ts="2026-06-20T00:00:00Z",
        model_version_override=None,
    )


@pytest.mark.parametrize(
    "kind, expected_output, target",
    [
        ("vis_agentic", {"visualization": _viz()}, "evaluate_agentic_visualization"),
        ("agentic_visualization", {"expected_outputs": [{"visualization": _viz()}]}, "evaluate_agentic_visualization"),
        ("agentic_metric_skill", {"maql": "x"}, "evaluate_agentic_metric_skill"),
        ("agentic_alert_skill", {"Operator": "LESS_THAN"}, "evaluate_agentic_alert_skill"),
        ("agentic_search", {"tool_call": {"function_arguments": {"keywords": ["x"]}}}, "evaluate_agentic_search_tool"),
        ("agentic_general_question", "an answer", "evaluate_agentic_general_question"),
        ("agentic_guardrail", "a refusal", "evaluate_agentic_guardrail"),
        ("agentic_conversation", {"fixture": {"id": "c1", "expected_skills": [], "turns": []}}, "evaluate_agentic_conversation"),
    ],
)
def test_dispatch_routes_each_agentic_kind(kind, expected_output, target):
    item = DatasetItem(id="i1", dataset_name="d", test_kind=kind, question="q", expected_output=expected_output)
    with patch(f"gooddata_eval.cli.agentic_runner.{target}") as mock_eval:
        _dispatch(item)
    mock_eval.assert_called_once()
    assert mock_eval.call_args.kwargs["workspace_id"] == "ws"


def test_dispatch_unknown_kind_raises():
    item = DatasetItem(id="i1", dataset_name="d", test_kind="agentic_bogus", question="q", expected_output={})
    with pytest.raises(ValueError, match="Unknown agentic test kind"):
        _dispatch(item)


def test_all_parametrized_kinds_are_declared_agentic():
    # Guard: every kind we route is in the canonical AGENTIC_TEST_KINDS set.
    routed = {
        "vis_agentic",
        "agentic_visualization",
        "agentic_metric_skill",
        "agentic_alert_skill",
        "agentic_search",
        "agentic_general_question",
        "agentic_guardrail",
        "agentic_conversation",
    }
    assert routed == set(AGENTIC_TEST_KINDS)
