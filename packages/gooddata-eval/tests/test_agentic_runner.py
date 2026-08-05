# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import patch

from gooddata_eval.cli.agentic_runner import run_agentic_items
from gooddata_eval.core.agentic.alert_skill import AlertSkillAssertionError
from gooddata_eval.core.models import DatasetItem


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
        return_value=(["it created the alert"], "conv-1", "resp-1"),
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


def test_run_agentic_items_defaults_reasoning_steps_to_empty_for_untouched_kinds():
    # general_question/guardrail/search_tool/visualization still return None -- unchanged.
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_guardrail", return_value=None):
        report = run_agentic_items(
            [_item(test_kind="agentic_guardrail")],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )
    assert report.items[0].pass_at_k is True
    assert report.items[0].reasoning_steps == []
    assert report.items[0].conversation_id is None
    assert report.items[0].response_id is None
