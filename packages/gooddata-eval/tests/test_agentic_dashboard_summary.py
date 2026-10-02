# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import gooddata_sdk
import gooddata_sdk.table as table_module
import pytest
from gooddata_eval.core.agentic.dashboard_summary import (
    DashboardSummaryAssertionError,
    DashboardWidget,
    _execute_widget,
    _insight_widgets,
    build_dashboard_user_context,
    evaluate_agentic_dashboard_summary,
    run_agentic_dashboard_summary,
)
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult

_MODULE = "gooddata_eval.core.agentic.dashboard_summary"


def _widget(local_id: str, viz_id: str, title: str = "A chart") -> dict:
    return {
        "localIdentifier": local_id,
        "title": title,
        "insight": {"identifier": {"id": viz_id, "type": "visualizationObject"}},
    }


def _summary_result(text: str = "## Executive Summary\n- Approvals trended up.") -> ChatResult:
    return ChatResult.model_validate({"textResponse": text, "toolCallEvents": [], "reasoningSteps": []})


# ── layout walking ──────────────────────────────────────────────────────────


def test_insight_widgets_walks_nested_sections_and_tabs():
    """Widget depth is not fixed: sections nest widgets, and a tab-based dashboard nests
    those again, so the walk cannot assume a path."""
    content = {
        "version": "3",
        "tabs": [
            {"localIdentifier": "tab1", "sections": [{"items": [_widget("w1", "viz-1")]}]},
            {"localIdentifier": "tab2", "sections": [{"items": [_widget("w2", "viz-2"), _widget("w3", "viz-3")]}]},
        ],
    }
    assert [w.widget_id for w in _insight_widgets(content)] == ["w1", "w2", "w3"]
    assert [w.visualization_id for w in _insight_widgets(content)] == ["viz-1", "viz-2", "viz-3"]


def test_insight_widgets_skips_widgets_with_nothing_to_execute():
    """Rich text and unresolved widgets carry no insight identifier, so there is nothing to
    execute and nothing the summarize scope could use."""
    content = {
        "sections": [
            {"items": [_widget("w1", "viz-1"), {"localIdentifier": "rt", "richText": {"content": "hello"}}]},
            {"items": [{"localIdentifier": "broken", "insight": {}}]},
        ]
    }
    assert [w.widget_id for w in _insight_widgets(content)] == ["w1"]


def test_insight_widgets_does_not_repeat_a_widget_reached_twice():
    """The walk descends into every value, so a layout that references one widget from two
    places must still yield it once -- a duplicate would be executed twice."""
    shared = _widget("w1", "viz-1")
    content = {"sections": [{"items": [shared]}], "alsoHere": {"items": [shared]}}
    assert [w.widget_id for w in _insight_widgets(content)] == ["w1"]


def test_insight_widget_falls_back_to_the_visualization_id_when_unnamed():
    content = {"items": [{"insight": {"identifier": {"id": "viz-1"}}}]}
    (widget,) = _insight_widgets(content)
    assert widget.widget_id == "viz-1"
    assert widget.title == "viz-1"


# ── context building ────────────────────────────────────────────────────────


def _patched_dashboard(widgets: list[dict], title: str = "Sales"):
    return patch(f"{_MODULE}._fetch_dashboard", return_value=(title, {"sections": [{"items": widgets}]}))


def test_build_user_context_carries_a_result_id_per_widget():
    sdk = MagicMock()
    with (
        _patched_dashboard([_widget("w1", "viz-1"), _widget("w2", "viz-2")]),
        patch(f"{_MODULE}._execute_widget", side_effect=["res-1", "res-2"]),
    ):
        context, widgets = build_dashboard_user_context(sdk, "http://h", "tok", "ws1", "dash-1")

    dashboard = context["view"]["dashboard"]
    assert dashboard["id"] == "dash-1"
    assert dashboard["title"] == "Sales"
    assert [w["resultId"] for w in dashboard["widgets"]] == ["res-1", "res-2"]
    assert [w["widgetType"] for w in dashboard["widgets"]] == ["insight", "insight"]
    assert [w.result_id for w in widgets] == ["res-1", "res-2"]


def test_a_widget_that_fails_to_execute_is_reported_but_left_out_of_the_context():
    """The skill drops any widget without a result_id, so sending one would be a silent
    no-op -- but the report still has to show the summary covered less than the dashboard."""
    sdk = MagicMock()
    with (
        _patched_dashboard([_widget("w1", "viz-1"), _widget("w2", "viz-2")]),
        patch(f"{_MODULE}._execute_widget", side_effect=["res-1", RuntimeError("execution blew up")]),
    ):
        context, widgets = build_dashboard_user_context(sdk, "http://h", "tok", "ws1", "dash-1")

    assert [w["widgetId"] for w in context["view"]["dashboard"]["widgets"]] == ["w1"]
    assert len(widgets) == 2
    assert widgets[1].result_id is None


def test_max_widgets_caps_the_executions():
    """A thirty-widget dashboard costs thirty executions per item; the cap bounds that."""
    sdk = MagicMock()
    layout = [_widget(f"w{i}", f"viz-{i}") for i in range(5)]
    with (
        _patched_dashboard(layout),
        patch(f"{_MODULE}._execute_widget", return_value="res") as execute,
    ):
        _, widgets = build_dashboard_user_context(sdk, "http://h", "tok", "ws1", "dash-1", max_widgets=2)

    assert len(widgets) == 2
    assert execute.call_count == 2


# ── runs ────────────────────────────────────────────────────────────────────


def _run(chat_side_effect, *, k=1, passed=True, widgets=2):
    client = MagicMock()
    client.create_conversation.side_effect = [f"conv-{i}" for i in range(1, k + 2)]
    client.send_message.side_effect = chat_side_effect
    evaluation = ItemEvaluation(passed=passed, rank_key=(int(passed), 1.0), detail={"actual_output": "text"})
    evaluator = MagicMock()
    evaluator.evaluate.return_value = evaluation
    layout = [_widget(f"w{i}", f"viz-{i}") for i in range(widgets)]
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.GoodDataSdk"),
        patch(f"{_MODULE}.DashboardSummaryEvaluator", return_value=evaluator),
        _patched_dashboard(layout),
        patch(f"{_MODULE}._execute_widget", return_value="res"),
    ):
        return run_agentic_dashboard_summary(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            dashboard_id="dash-1",
            expected_output={"must_include": ["x"]},
            k=k,
        )


def test_a_passing_run_records_how_much_of_the_dashboard_it_covered():
    summary = _run([_summary_result()])
    assert summary.pass_at_k is True
    assert summary.best.widgets_total == 2
    assert summary.best.widgets_executed == 2


def test_widgets_are_executed_once_and_reused_across_k_runs():
    """Result ids identify cached executions, so re-running them per K would multiply the
    most expensive part of the item without changing what the assistant sees."""
    client = MagicMock()
    client.create_conversation.side_effect = ["conv-1", "conv-2", "conv-3"]
    client.send_message.return_value = _summary_result()
    evaluator = MagicMock()
    evaluator.evaluate.return_value = ItemEvaluation(passed=True, rank_key=(1, 1.0), detail={"actual_output": "t"})
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.GoodDataSdk"),
        patch(f"{_MODULE}.DashboardSummaryEvaluator", return_value=evaluator),
        _patched_dashboard([_widget("w1", "viz-1")]),
        patch(f"{_MODULE}._execute_widget", return_value="res") as execute,
    ):
        summary = run_agentic_dashboard_summary(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            dashboard_id="dash-1",
            expected_output={"must_include": ["x"]},
            k=3,
        )

    assert len(summary.run_results) == 3
    assert execute.call_count == 1


def test_a_chat_error_is_recorded_on_the_run_rather_than_raised():
    """Raising would discard the K-runs already completed and leave the item with no
    verdict at all -- the same failure mode fixed for the other agentic kinds."""
    summary = _run([ChatError("gen-ai fell over")])

    assert summary.pass_at_k is False
    run = summary.run_results[0]
    assert run.chat_error is not None
    assert "gen-ai fell over" in run.chat_error
    assert run.passed is False
    assert run.evaluation.error is not None


def test_a_chat_error_on_a_later_run_does_not_discard_the_earlier_one():
    summary = _run([_summary_result(), ChatError("boom")], k=2)

    assert len(summary.run_results) == 2
    assert summary.run_results[0].chat_error is None
    assert summary.run_results[1].chat_error is not None
    assert summary.pass_at_k is True  # run 0 still counts
    # The chat-error run is unscored, so it cannot certify that every run passed.
    assert summary.pass_power_k is False


def test_the_best_run_is_never_a_chat_error_when_a_graded_run_exists():
    summary = _run([ChatError("boom"), _summary_result()], k=2)
    assert summary.best.chat_error is None


# ── evaluate_* wrapper ──────────────────────────────────────────────────────


def _evaluate(passed: bool):
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _summary_result()
    evaluator = MagicMock()
    evaluator.evaluate.return_value = ItemEvaluation(
        passed=passed, rank_key=(int(passed), 1.0), detail={"actual_output": "text", "include_0": passed}
    )
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.GoodDataSdk"),
        patch(f"{_MODULE}.DashboardSummaryEvaluator", return_value=evaluator),
        _patched_dashboard([_widget("w1", "viz-1"), _widget("w2", "viz-2")]),
        patch(f"{_MODULE}._execute_widget", side_effect=["res-1", RuntimeError("dead")]),
    ):
        return evaluate_agentic_dashboard_summary(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            dashboard_id="dash-1",
            expected_output={"must_include": ["x"]},
        )


def test_detail_reports_coverage_and_the_latency_breakdown():
    outcome = _evaluate(passed=True)
    # A rubric naming a widget that never executed fails for a reason that is not the
    # agent's, so the ratio has to be visible without opening the trace.
    assert outcome.detail["widgets_total"] == 2
    assert outcome.detail["widgets_executed"] == 1
    assert "latency_breakdown" in outcome.detail
    assert outcome.detail["include_0"] is True
    assert outcome.conversation_id == "conv-1"


def test_a_failing_item_raises_with_the_same_detail_attached():
    with pytest.raises(DashboardSummaryAssertionError) as exc_info:
        _evaluate(passed=False)

    error = exc_info.value
    assert "1/2 widgets executed" in str(error)
    assert error.detail["widgets_executed"] == 1
    assert error.runs_passed == 0
    assert error.runs_effective == 1
    assert error.conversation_id == "conv-1"


def test_dashboard_widget_defaults_to_no_result():
    assert DashboardWidget(widget_id="w", title="t", visualization_id="v").result_id is None


def test_only_visualizations_keeps_just_the_named_charts():
    """A fixture asserting on a handful of charts should not pay to execute thirty. Names
    are matched against the visualization id and the widget id, since a fixture author
    reading a dashboard's AAC sees both."""
    sdk = MagicMock()
    layout = [_widget("w0", "viz-0"), _widget("w1", "viz-1"), _widget("w2", "viz-2")]
    with (
        _patched_dashboard(layout),
        patch(f"{_MODULE}._execute_widget", return_value="res") as execute,
    ):
        _, widgets = build_dashboard_user_context(
            sdk, "http://h", "tok", "ws1", "dash-1", only_visualizations=["viz-1", "w2"]
        )

    assert [w.widget_id for w in widgets] == ["w1", "w2"]
    assert execute.call_count == 2


def test_only_visualizations_and_max_widgets_compose():
    sdk = MagicMock()
    layout = [_widget(f"w{i}", f"viz-{i}") for i in range(4)]
    with (
        _patched_dashboard(layout),
        patch(f"{_MODULE}._execute_widget", return_value="res"),
    ):
        _, widgets = build_dashboard_user_context(
            sdk,
            "http://h",
            "tok",
            "ws1",
            "dash-1",
            only_visualizations=["viz-1", "viz-2", "viz-3"],
            max_widgets=2,
        )

    assert [w.widget_id for w in widgets] == ["w1", "w2"]


def test_a_failed_conversation_creation_does_not_discard_completed_runs():
    """create_conversation sat outside any handler, so a transient failure on run 2 of 3
    threw away run 1 -- the same failure mode the ChatError path already guards."""
    client = MagicMock()
    client.create_conversation.side_effect = ["conv-1", RuntimeError("no conversation for you"), "conv-3"]
    client.send_message.return_value = _summary_result()
    evaluator = MagicMock()
    evaluator.evaluate.return_value = ItemEvaluation(passed=True, rank_key=(1, 1.0), detail={"actual_output": "t"})
    with (
        patch(f"{_MODULE}.ChatClient", return_value=client),
        patch(f"{_MODULE}.GoodDataSdk"),
        patch(f"{_MODULE}.DashboardSummaryEvaluator", return_value=evaluator),
        _patched_dashboard([_widget("w1", "viz-1")]),
        patch(f"{_MODULE}._execute_widget", return_value="res"),
    ):
        summary = run_agentic_dashboard_summary(
            host="http://h",
            token="tok",
            workspace_id="ws1",
            dashboard_id="dash-1",
            expected_output={"must_include": ["x"]},
            k=3,
        )

    assert len(summary.run_results) == 3
    assert [r.chat_error is None for r in summary.run_results] == [True, False, True]
    assert "conversation creation failed" in summary.run_results[1].chat_error
    assert summary.pass_at_k is True
    # The lost run has no conversation to score, so it must not certify an all-passed item.
    assert summary.pass_power_k is False


def test_execute_widget_fails_loudly_when_the_sdk_moves_its_private_helpers():
    """gooddata-sdk is depended on as ~=1.74.0, so a patch release may rename the private
    helpers this borrows. Without the check that surfaces as an AttributeError on the first
    widget of a run rather than as the dependency problem it is."""
    stripped = MagicMock(spec=[])  # a gooddata_sdk.table exposing none of the three helpers
    # Both bindings: `import a.b as c` reads the parent package's attribute, while
    # sys.modules is what keeps a re-import from restoring the real one.
    with (
        patch.dict("sys.modules", {"gooddata_sdk.table": stripped}),
        patch.object(gooddata_sdk, "table", stripped),
        pytest.raises(RuntimeError, match="no longer provides"),
    ):
        _execute_widget(MagicMock(), "ws1", "viz-1")


def test_execute_widget_guard_passes_against_the_installed_sdk():
    """The guard must not be a permanent tripwire: the helpers exist in the pinned version,
    so a real call gets past it and fails (if at all) on the network, not on the check."""
    for name in ("_vis_is_table", "_get_exec_for_pivot", "get_exec_for_non_pivot"):
        assert hasattr(table_module, name), f"gooddata_sdk.table.{name} is gone -- update _execute_widget"
