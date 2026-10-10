# (C) 2026 GoodData Corporation
import json
import re
from datetime import date

import pytest
from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.evaluators.visualization import _evaluate_visualization, execution_signals
from gooddata_eval.core.models import ChatResult, CreatedVisualization, DatasetItem, ToolCallEvent


def _item(expected_viz) -> DatasetItem:
    return DatasetItem(
        id="i1",
        dataset_name="d",
        test_kind="visualization",
        question="Show revenue by quarter",
        expected_output={"visualization": expected_viz},
    )


def _expected():
    return {
        "id": "x",
        "type": "column_chart",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}, "d_q": {"using": "label/date.quarter"}},
            "filter_by": {},
        },
        "metrics": ["m_rev"],
        "view_by": ["d_q"],
    }


def _chat_result_with(viz_obj) -> ChatResult:
    return ChatResult.model_validate(
        {"createdVisualizations": {"objects": [viz_obj], "reasoning": ""}, "toolCallEvents": []}
    )


def test_evaluator_passes_on_exact_match():
    ev = get_evaluator("visualization")
    actual = dict(_expected())
    result = ev.evaluate(_item(_expected()), _chat_result_with(actual))
    assert result.passed is True
    assert result.rank_key[0] is True


def test_evaluator_fails_when_no_visualization_created():
    ev = get_evaluator("visualization")
    empty = ChatResult.model_validate({"textResponse": "what metric?", "toolCallEvents": []})
    result = ev.evaluate(_item(_expected()), empty)
    assert result.passed is False
    assert result.detail["visualization_created"] is False


def test_evaluator_matches_any_candidate_in_list():
    ev = get_evaluator("visualization")
    wrong = {**_expected(), "view_by": ["m_rev"]}  # nonsense, won't match
    right = _expected()
    item = _item([wrong, right])
    result = ev.evaluate(item, _chat_result_with(dict(_expected())))
    assert result.passed is True


def test_evaluator_detects_skill_activated():
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["visualization"]}',
                    "result": None,
                }
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is True


def test_evaluator_skill_not_activated_when_set_skills_absent():
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is False


def test_evaluator_skill_not_activated_when_wrong_skill_name():
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {"functionName": "set_skills", "functionArguments": '{"skill_names": ["search"]}', "result": None}
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is False


def test_evaluator_skill_unrecognised_name_in_arguments_dropped_by_result():
    """When arguments requested 'visualization' but the service result dropped it,
    it must not be credited as active."""
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["visualization"]}',
                    "result": json.dumps({"skills_to_activate": ["search"]}),
                }
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is False


def test_evaluator_skill_dependency_pulled_in_by_result_is_credited():
    """When arguments did not name 'visualization' but the service result pulled it in
    as a dependency, it must be credited as active."""
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["dashboard_builder"]}',
                    "result": json.dumps({"skills_to_activate": ["dashboard_builder", "visualization"]}),
                }
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is True


def test_evaluator_skill_fallback_when_result_missing():
    """When the result is missing (legacy trace), fallback to arguments."""
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["visualization"]}',
                    "result": None,
                }
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is True


def test_evaluator_skill_fallback_when_result_unparseable():
    """When the result is unparseable non-JSON text, fallback to arguments."""
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["visualization"]}',
                    "result": "502 Bad Gateway",
                }
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is True


def test_evaluator_skill_fallback_when_call_errored():
    """When the result indicates the tool call errored, fallback to arguments."""
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "set_skills",
                    "functionArguments": '{"skill_names": ["visualization"]}',
                    "result": json.dumps({"status": "error", "message": "Failed to set skills"}),
                }
            ],
        }
    )
    result = ev.evaluate(_item(_expected()), chat)
    assert result.detail["skill_activated"] is True


def _ranked(attribute: str | None, dim_alias: str = "d_q"):
    """Single-dimension chart with a top-1 ranking filter, optionally naming the attribute."""
    rank = {"type": "ranking_filter", "using": "m_rev", "top": 1}
    if attribute is not None:
        rank["attribute"] = attribute
    return {
        "id": "x",
        "type": "column_chart",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}, dim_alias: {"using": "label/date.quarter"}},
            "filter_by": {"f_rank": rank},
        },
        "metrics": ["m_rev"],
        "view_by": [dim_alias],
    }


def test_evaluator_passes_when_agent_omits_ranking_attribute_on_single_dim_viz():
    """QA-28615: the omitted attribute resolves to the sole dimension, so the case must pass."""
    ev = get_evaluator("visualization")
    expected = _ranked("d_q")
    actual = _ranked(None, dim_alias="d_quarter")  # different alias, attribute omitted
    result = ev.evaluate(_item(expected), _chat_result_with(actual))
    assert result.detail["filter_ranking_score"] is True
    assert result.detail["filters_correct"] is True
    assert result.passed is True


def _dated(granularity: str, frm: int, to: int):
    return {
        "id": "x",
        "type": "column_chart",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}, "d_q": {"using": "label/date.quarter"}},
            "filter_by": {
                "f_date": {
                    "type": "date_filter",
                    "using": "dataset/date",
                    "granularity": granularity,
                    "from": frm,
                    "to": to,
                }
            },
        },
        "metrics": ["m_rev"],
        "view_by": ["d_q"],
    }


def test_detail_reports_the_filters_that_were_compared():
    """A `filter_date_score` of False is undiagnosable from a finished run without them:
    two encodings of the same period compare unequal and the booleans don't say which."""
    ev = get_evaluator("visualization")
    result = ev.evaluate(_item(_dated("MONTH", -11, 0)), _chat_result_with(_dated("MONTH", -12, -1)))

    assert result.detail["filter_date_score"] is False
    expected, actual = result.detail["expected_filters"], result.detail["actual_filters"]
    # Relative offsets are reported as the absolute span they resolve to, so the two
    # periods are legible side by side and visibly different -- which is the point.
    assert re.search(r'"from": "\d{4}-\d{2}-\d{2}"', expected["date"][0])
    assert re.search(r'"from": "\d{4}-\d{2}-\d{2}"', actual["date"][0])
    assert expected["date"] != actual["date"]
    assert expected["ranking"] == actual["ranking"] == []
    assert expected["attribute"] == actual["attribute"] == []


def test_detail_filters_are_empty_when_no_visualization_was_created():
    ev = get_evaluator("visualization")
    empty = ChatResult.model_validate({"textResponse": "what metric?", "toolCallEvents": []})
    result = ev.evaluate(_item(_dated("MONTH", -11, 0)), empty)
    assert result.detail["actual_filters"] == {"date": [], "ranking": [], "attribute": []}
    assert len(result.detail["expected_filters"]["date"]) == 1


def _date_filtered_viz():
    return {
        "id": "x",
        "type": "table",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}},
            "filter_by": {
                "f": {"type": "date_filter", "using": "dataset/dt", "from": -1, "to": -1, "granularity": "MONTH"}
            },
        },
        "metrics": ["m_rev"],
    }


def test_reported_filters_use_the_same_date_anchor_as_the_score():
    """The filters reported in detail must be resolved against the anchor the score used.

    check_filters shares one anchor across its two sides, but the reported filters were
    resolved by separate normalized_filters calls, each taking its own date.today(). A run
    straddling midnight could therefore report periods the verdict was never computed from.
    Pinning an explicit anchor here fails unless it reaches every one of those calls.
    """
    viz = CreatedVisualization.model_validate(_date_filtered_viz())
    result = _evaluate_visualization(viz, viz, today=date(2026, 3, 15))

    # -1 MONTH from 2026-03-15 is February 2026, not whatever month the suite runs in.
    assert result.filter_date_score is True
    assert '"from": "2026-02-01"' in result.expected_filters["date"][0]
    assert '"to": "2026-02-28"' in result.expected_filters["date"][0]
    assert result.expected_filters["date"] == result.actual_filters["date"]


# ── execution signals ───────────────────────────────────────────────────────

_CREATE = ToolCallEvent(
    functionName="create_adhoc_visualization",
    functionArguments='{"visualization": {"type": "headline_chart"}}',
    result='{"status":"success","ref":"viz_1"}',
)
# Shapes as recorded on a live sonnet55 run: the raw value and the display string the agent quotes.
_EXECUTE = ToolCallEvent(
    functionName="execute_visualization",
    functionArguments='{"visualization_ref": "viz_1", "max_rows": 10}',
    result=(
        '{"success":true,"data":{"output_format":"rows","columns":[],'
        '"rows":[{"Units Per Transaction":18.303635747929686}],'
        '"formatted_rows":[{"Units Per Transaction":"18.30"}],"row_count":1,"truncated":false}}'
    ),
)


def test_a_built_and_run_chart_whose_value_the_reply_quotes():
    assert execution_signals([_CREATE, _EXECUTE], "The average customer buys **18.30** items per order.") == (
        True,
        True,
    )


def test_a_built_chart_that_was_never_run():
    assert execution_signals([_CREATE], "Here is the visualization of Star Wars sets.") == (False, None)


def test_a_figure_stated_without_running_the_chart_does_not_match():
    assert execution_signals([_CREATE], "There are 15,587 Star Wars sets.") == (False, False)


def test_a_figure_that_differs_from_the_executed_value():
    assert execution_signals([_CREATE, _EXECUTE], "Customers buy 21.5 items per order.") == (True, False)


def test_a_failed_execution_or_one_for_another_ref_does_not_count():
    failed = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": "viz_1"}',
        result='{"success":false,"error":"boom"}',
    )
    foreign = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": "viz_9"}',
        result='{"success":true,"data":{"rows":[]}}',
    )
    assert execution_signals([_CREATE, failed, foreign], None) == (False, None)


@pytest.mark.parametrize(
    ("value", "text"),
    [(1234567.0, "about 1.2M"), (0.4567, "45.7%"), (15587.0, "$15,587"), (950.0, "950 sets")],
)
def test_a_stated_number_matches_a_rounding_of_the_raw_value(value, text):
    execute = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": "viz_1"}',
        result=f'{{"success":true,"data":{{"rows":[{{"v":{value}}}]}}}}',
    )
    assert execution_signals([_CREATE, execute], text) == (True, True)


def _item_requiring_execution(expected_viz) -> DatasetItem:
    return DatasetItem(
        id="i1",
        dataset_name="d",
        test_kind="visualization",
        question="What is revenue?",
        expected_output={"visualization": expected_viz, "requires_execution": True},
    )


def test_a_correct_chart_fails_when_execution_is_required_and_missing():
    ev = get_evaluator("visualization")
    result = ev.evaluate(_item_requiring_execution(_expected()), _chat_result_with(dict(_expected())))
    assert result.passed is False
    assert result.detail["executed"] is False
    assert result.detail["execution"]["required"] is True


def test_a_correct_chart_passes_when_execution_is_required_and_done():
    ev = get_evaluator("visualization")
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [dict(_expected())], "reasoning": ""},
            "toolCallEvents": [_CREATE.model_dump(by_alias=True), _EXECUTE.model_dump(by_alias=True)],
        }
    )
    result = ev.evaluate(_item_requiring_execution(_expected()), chat)
    assert result.passed is True
    assert result.detail["executed"] is True


def test_an_unrun_chart_still_passes_when_the_item_does_not_require_execution():
    result = get_evaluator("visualization").evaluate(_item(_expected()), _chat_result_with(dict(_expected())))
    assert result.passed is True
    assert result.detail["execution"]["executed"] is False
    # Not gating, so not a top-level check that quality_score would count.
    assert "executed" not in result.detail


def test_a_tool_result_that_is_not_a_json_object_is_skipped_not_raised():
    odd_create = ToolCallEvent(functionName="create_adhoc_visualization", functionArguments="{}", result='["viz_1"]')
    odd_execute = ToolCallEvent(functionName="execute_visualization", functionArguments='"viz_1"', result='"ok"')
    assert execution_signals([odd_create, _CREATE, odd_execute, _EXECUTE], None) == (True, None)


def test_a_sign_after_the_currency_symbol_is_read():
    execute = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": "viz_1"}',
        result='{"success":true,"data":{"rows":[{"v":-1234}]}}',
    )
    assert execution_signals([_CREATE, execute], "a loss of $-1,234") == (True, True)


def test_a_number_without_the_scale_does_not_quote_a_scaled_display_string():
    execute = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": "viz_1"}',
        result='{"success":true,"data":{"rows":[{"v":1200000}],"formatted_rows":[{"v":"1.2M"}]}}',
    )
    assert execution_signals([_CREATE, execute], "Revenue was 1.2.") == (True, False)
    assert execution_signals([_CREATE, execute], "Revenue was 1.2M.") == (True, True)


def test_malformed_rows_in_a_successful_result_are_skipped_not_raised():
    execute = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": "viz_1"}',
        result='{"success":true,"data":{"rows":42,"formatted_rows":"x"}}',
    )
    assert execution_signals([_CREATE, execute], "It is 42.") == (True, False)


def test_a_percent_is_compared_with_the_fraction_times_100():
    execute = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": "viz_1"}',
        result='{"success":true,"data":{"rows":[{"v":0.1}]}}',
    )
    assert execution_signals([_CREATE, execute], "a 10% share") == (True, True)
    assert execution_signals([_CREATE, execute], "a 0.1% share") == (True, False)


def test_a_ref_that_is_not_a_string_is_skipped_not_raised():
    execute = ToolCallEvent(
        functionName="execute_visualization",
        functionArguments='{"visualization_ref": ["viz_1"]}',
        result='{"success":true,"data":{"rows":[]}}',
    )
    assert execution_signals([_CREATE, execute], None) == (False, None)
