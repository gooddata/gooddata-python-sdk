# (C) 2026 GoodData Corporation
import json
import re
from datetime import date

import pytest
from gooddata_eval.core.chat.sse_client import ADHOC_VIZ_ID
from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.evaluators.visualization import (
    ExpectationOptions,
    _evaluate_visualization,
    execution_signals,
    expectation_options,
)
from gooddata_eval.core.models import ChatResult, CreatedVisualization, DatasetItem, ToolCallEvent
from gooddata_eval.core.scoring import get_dimension_uri_set, get_metric_uri_set


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


# -- Extended chart types (QA-29722): shapes trimmed from ecommerce_demo runs -----------------

_EXT_FIELDS = {
    "m_net_sales": {"using": "metric/net_sales"},
    "m_margin": {"using": "metric/gross_profit_margin"},
    "m_orders": {"using": "metric/of_orders"},
    "d_category": {"using": "label/product_category"},
    "d_country": {"using": "label/customer_country"},
    "d_brand": {"using": "label/product_brand"},
    "d_month": {"using": "label/date.month"},
}


def _ext(type_: str, **buckets) -> dict:
    return {"type": type_, "query": {"fields": _EXT_FIELDS, "filter_by": {}}, **buckets}


def _score(expected: dict, actual: dict):
    return _evaluate_visualization(
        CreatedVisualization.model_validate(expected), CreatedVisualization.model_validate(actual)
    )


def test_a_repeater_scores_the_same_with_its_metric_in_metrics_or_in_columns():
    expected = _ext("repeater_chart", metrics=["m_net_sales"], rows=["d_category"], view_by=["d_month"])
    in_metrics = _ext(
        "repeater_chart",
        metrics=[{"field": "m_net_sales", "display_as": "line"}],
        rows=["d_category"],
        view_by=["d_month"],
    )
    in_columns = _ext(
        "repeater_chart",
        rows=["d_category"],
        view_by=["d_month"],
        columns=["d_category_column", {"field": "m_net_sales", "display_as": "line"}],
    )
    in_columns["query"] = {"fields": {**_EXT_FIELDS, "d_category_column": {"using": "label/product_category"}}}
    for actual in (in_metrics, in_columns):
        ev = _score({**expected, "buckets_strict": True}, actual)
        assert ev.metrics_correct, ev.actual_metric_uris
        assert ev.dimensions_correct, ev.actual_dim_uris
        assert ev.buckets_correct is True, ev.actual_buckets
        assert ev.strict_pass


def test_sankey_ends_are_dimensions_and_their_direction_is_checked_under_buckets_strict():
    expected = _ext("sankey_chart", metrics=["m_net_sales"], **{"from": "d_category", "to": "d_country"})
    right = _score({**expected, "buckets_strict": True}, expected)
    assert right.expected_dim_uris == {"label/product_category", "label/customer_country"}
    assert right.strict_pass

    reversed_ends = _ext("sankey_chart", metrics=["m_net_sales"], **{"from": "d_country", "to": "d_category"})
    loose = _score(expected, reversed_ends)
    strict = _score({**expected, "buckets_strict": True}, reversed_ends)
    assert loose.strict_pass, "without buckets_strict the union of the ends is all that counts"
    assert strict.buckets_correct is False
    assert not strict.strict_pass


def test_a_missing_sankey_destination_fails_the_dimension_check():
    expected = _ext("sankey_chart", metrics=["m_net_sales"], **{"from": "d_category", "to": "d_country"})
    no_destination = _ext("sankey_chart", metrics=["m_net_sales"], **{"from": "d_category"})
    assert not _score(expected, no_destination).dimensions_correct


def test_a_heatmap_with_rows_and_columns_swapped_fails_only_under_buckets_strict():
    expected = _ext("heatmap_chart", metrics=["m_net_sales"], view_by=["d_brand"], segment_by=["d_country"])
    swapped = _ext("heatmap_chart", metrics=["m_net_sales"], view_by=["d_country"], segment_by=["d_brand"])
    assert _score(expected, swapped).strict_pass
    ev = _score({**expected, "buckets_strict": True}, swapped)
    assert ev.buckets_correct is False
    assert ev.expected_buckets["view_by"] == ["label/product_brand"]
    assert ev.actual_buckets["view_by"] == ["label/customer_country"]


def test_bubble_size_counts_as_a_metric_and_order_holds_the_x_position():
    expected = _ext(
        "bubble_chart",
        metrics=[None, "m_margin"],
        size_by=["m_orders"],
        view_by=["d_brand"],
        metrics_ordered=True,
        buckets_strict=True,
    )
    right = _ext("bubble_chart", metrics=[None, "m_margin"], size_by=["m_orders"], view_by=["d_brand"])
    ev = _score(expected, right)
    assert ev.expected_metric_uris == {"metric/gross_profit_margin", "metric/of_orders"}
    assert ev.strict_pass, ev.metric_layout_problems

    margin_on_x = _ext("bubble_chart", metrics=["m_margin"], size_by=["m_orders"], view_by=["d_brand"])
    ev = _score(expected, margin_on_x)
    assert not ev.metrics_correct
    assert ev.metric_layout_problems and "metric order" in ev.metric_layout_problems[0]


def test_bullet_roles_are_positional_only_when_metrics_ordered():
    roles = ["m_net_sales", "m_orders", "m_margin"]
    expected = _ext("bullet_chart", metrics=roles, view_by=["d_category"])
    shuffled = _ext("bullet_chart", metrics=["m_orders", "m_net_sales", "m_margin"], view_by=["d_category"])
    assert _score(expected, shuffled).metrics_correct
    assert not _score({**expected, "metrics_ordered": True}, shuffled).metrics_correct


def test_combo_axes_are_checked_for_every_metric_that_names_one():
    expected = _ext(
        "combo_chart",
        metrics=[{"field": "m_net_sales", "axis": "primary"}, {"field": "m_margin", "axis": "secondary"}],
        view_by=["d_category"],
    )
    assert _score(expected, expected).strict_pass
    both_primary = _ext(
        "combo_chart",
        metrics=[{"field": "m_net_sales", "axis": "primary"}, {"field": "m_margin", "axis": "primary"}],
        view_by=["d_category"],
    )
    ev = _score(expected, both_primary)
    assert not ev.metrics_correct
    assert "metric axes" in ev.metric_layout_problems[0]


def test_combo_axes_read_a_metric_without_an_axis_as_primary():
    expected = _ext(
        "combo_chart",
        metrics=[{"field": "m_net_sales", "axis": "primary"}, {"field": "m_margin", "axis": "secondary"}],
        view_by=["d_category"],
    )
    for primary in ("m_net_sales", {"field": "m_net_sales"}):
        actual = _ext(
            "combo_chart", metrics=[primary, {"field": "m_margin", "axis": "secondary"}], view_by=["d_category"]
        )
        ev = _score(expected, actual)
        assert ev.metrics_correct, ev.metric_layout_problems
    secondary_unstated = _ext("combo_chart", metrics=["m_net_sales", "m_margin"], view_by=["d_category"])
    ev = _score(expected, secondary_unstated)
    assert not ev.metrics_correct
    assert "'metric/gross_profit_margin': 'primary'" in ev.metric_layout_problems[0]


def test_a_field_the_chart_aggregates_itself_counts_as_a_metric_in_columns():
    fields = {**_EXT_FIELDS, "c_orders": {"using": "attribute/order_id", "aggregation": "COUNT"}}
    repeater = _ext("repeater_chart", rows=["d_category"], columns=[{"field": "c_orders", "display_as": "line"}])
    repeater["query"] = {"fields": fields, "filter_by": {}}
    viz = CreatedVisualization.model_validate(repeater)
    assert get_metric_uri_set(viz) == {"attribute/order_id"}
    assert get_dimension_uri_set(viz) == {"label/product_category"}


def test_a_sankey_source_is_written_under_its_aac_name():
    """`from` is a Python keyword: the field is `from_`, but no dump may write that name."""
    viz = CreatedVisualization.model_validate(
        _ext("sankey_chart", metrics=["m_net_sales"], **{"from": "d_category", "to": "d_country"})
    )
    for dumped in (viz.model_dump(exclude_none=True), viz.model_dump(mode="json")):
        assert dumped["from"] == "d_category"
        assert "from_" not in dumped
    assert '"from":"d_category"' in viz.model_dump_json()
    assert list(viz.model_dump()).index("from") < list(viz.model_dump()).index("to")
    assert CreatedVisualization.model_validate(viz.model_dump()).from_ == "d_category"


def test_bucket_check_is_absent_from_the_detail_unless_asked_for():
    ev = get_evaluator("visualization")
    plain = ev.evaluate(_item(_expected()), _chat_result_with(dict(_expected())))
    assert "buckets_correct" not in plain.detail
    strict = ev.evaluate(_item({**_expected(), "buckets_strict": True}), _chat_result_with(dict(_expected())))
    assert strict.detail["buckets_correct"] is True


def test_expectation_switches_are_left_out_of_a_recorded_output():
    viz = CreatedVisualization.model_validate({**_expected(), "buckets_strict": True, "metrics_ordered": True})
    dumped = viz.model_dump(exclude_none=True)
    assert "buckets_strict" not in dumped
    assert "metrics_ordered" not in dumped


# -- Item-level options (QA-29722) ------------------------------------------------------------


def _item_with(expected_output: dict) -> DatasetItem:
    return DatasetItem(
        id="i1", dataset_name="d", test_kind="visualization", question="q", expected_output=expected_output
    )


def test_an_item_without_a_chart_passes_on_a_question_and_fails_on_a_chart():
    ev = get_evaluator("visualization")
    expected = {"expects_visualization": False, "answer_must_include": ["destination"]}
    asked = ChatResult.model_validate(
        {"textResponse": "A Sankey chart needs a source and a destination. Which destination?", "toolCallEvents": []}
    )
    result = ev.evaluate(_item_with(expected), asked)
    assert result.passed, result.detail
    assert result.detail["no_chart"] is True
    assert "metrics_correct" not in result.detail
    built = ev.evaluate(_item_with(expected), _chat_result_with(_expected()))
    assert not built.passed
    assert built.detail["no_chart"] is False


def test_a_no_chart_expectation_that_lists_charts_is_rejected():
    with pytest.raises(ValueError, match="must not list 'visualization' candidates"):
        get_evaluator("visualization").evaluate(
            _item_with({"expects_visualization": False, "visualization": _expected()}), _chat_result_with(_expected())
        )


def test_answer_patterns_ignore_case_and_read_a_typographic_apostrophe():
    ev = get_evaluator("visualization")
    reply = {
        "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
        "textResponse": "Gantt charts aren’t supported here, so I created the closest option.",
        "toolCallEvents": [],
    }
    included = ev.evaluate(
        _item_with({"visualization": _expected(), "answer_must_include": ["AREN'T SUPPORTED"]}),
        ChatResult.model_validate(reply),
    )
    assert included.passed, included.detail
    forbidden = ev.evaluate(
        _item_with({"visualization": _expected(), "answer_must_not_match": ["n't supported"]}),
        ChatResult.model_validate(reply),
    )
    assert not forbidden.passed
    assert forbidden.detail["answer_correct"] is False
    assert "n't supported" in forbidden.detail["answer_problems"][0]


def test_an_invalid_answer_pattern_is_rejected():
    with pytest.raises(ValueError, match="invalid regular expression"):
        get_evaluator("visualization").evaluate(
            _item_with({"visualization": _expected(), "answer_must_include": ["(unclosed"]}),
            _chat_result_with(_expected()),
        )


def test_a_chart_only_in_the_tool_arguments_fails_when_the_part_is_required():
    ev = get_evaluator("visualization")
    expected = {"visualization": _expected(), "requires_visualization_part": True}
    shown = ev.evaluate(_item_with(expected), _chat_result_with(_expected()))
    assert shown.passed and shown.detail["part_present"] is True
    fallback = ev.evaluate(_item_with(expected), _chat_result_with({**_expected(), "id": ADHOC_VIZ_ID}))
    assert not fallback.passed and fallback.detail["part_present"] is False
    unasked = ev.evaluate(_item(_expected()), _chat_result_with({**_expected(), "id": ADHOC_VIZ_ID}))
    assert unasked.passed and "part_present" not in unasked.detail


def test_a_format_intent_is_read_from_the_chart_tool_call():
    ev = get_evaluator("visualization")
    args = {
        "visualization": {
            **_expected(),
            "metrics": [
                {
                    "field": "m_rev",
                    "format": "#,##0.0M",
                    "format_example": {"value": 4221301265.5, "shown_as": "4,221,301,265.5M"},
                }
            ],
        }
    }
    chat = ChatResult.model_validate(
        {
            "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
            "toolCallEvents": [
                {
                    "functionName": "create_adhoc_visualization",
                    "functionArguments": json.dumps(args),
                    "result": json.dumps({"status": "success", "ref": "viz_1"}),
                }
            ],
        }
    )
    expected = {
        "visualization": _expected(),
        "format_intents": {"metric/revenue": {"divide_by": 1000000, "decimals": 1, "suffix": "M"}},
    }
    result = ev.evaluate(_item_with(expected), chat)
    assert not result.passed
    assert result.detail["format_correct"] is False
    assert "4,221,301,265.5M" in result.detail["format_problems"][0]


def test_an_optional_chart_passes_on_either_an_answer_or_the_right_chart():
    ev = get_evaluator("visualization")
    expected = {"visualization": _expected(), "visualization_optional": True, "answer_must_include": ["cannot|which"]}
    asked = ChatResult.model_validate({"textResponse": "Which measure should the donut show?", "toolCallEvents": []})
    by_answer = ev.evaluate(_item_with(expected), asked)
    assert by_answer.passed and by_answer.detail["no_chart"] is True
    built = {
        "createdVisualizations": {"objects": [_expected()], "reasoning": ""},
        "textResponse": "A donut cannot show two measures, so I created a column chart.",
        "toolCallEvents": [],
    }
    by_chart = ev.evaluate(_item_with(expected), ChatResult.model_validate(built))
    assert by_chart.passed and by_chart.detail["metrics_correct"] is True
    wrong_chart = {**built, "createdVisualizations": {"objects": [{**_expected(), "type": "line_chart"}]}}
    assert not ev.evaluate(_item_with(expected), ChatResult.model_validate(wrong_chart)).passed


def test_an_optional_chart_cannot_also_rule_the_chart_out():
    with pytest.raises(ValueError, match="contradict"):
        get_evaluator("visualization").evaluate(
            _item_with({"expects_visualization": False, "visualization_optional": True}), _chat_result_with(_expected())
        )


@pytest.mark.parametrize(
    ("expected_output", "message"),
    [
        ({"visualization": _expected(), "answer_must_include": "destination"}, "must be a list of regular"),
        ({"visualization": _expected(), "answer_must_not_match": [""]}, "must be a list of regular"),
        ({"expects_visualization": "no"}, "expects_visualization must be true or false"),
        ({"visualization": _expected(), "visualization_optional": 1}, "visualization_optional must be true or false"),
        ({"visualization": _expected(), "requires_visualization_part": "yes"}, "requires_visualization_part must be"),
        ({"expects_visualization": False, "requires_visualization_part": True}, "cannot state format_intents"),
        (
            {"expects_visualization": False, "format_intents": {"metric/revenue": None}},
            "cannot state format_intents",
        ),
        ({"expects_visualization": False, "expected_outputs": []}, "must not list 'visualization' candidates"),
    ],
)
def test_a_malformed_expectation_option_is_rejected(expected_output, message):
    with pytest.raises(ValueError, match=message):
        expectation_options(expected_output)


def test_an_expectation_that_is_not_an_object_reads_the_defaults():
    assert expectation_options([{"visualization": _expected()}]) == ExpectationOptions()


@pytest.mark.parametrize(
    "expected_output",
    [{"expects_visualization": False}, {"visualization": _expected(), "visualization_optional": True}],
)
def test_an_empty_turn_fails_an_item_that_accepts_no_chart(expected_output):
    result = get_evaluator("visualization").evaluate(
        _item_with(expected_output), ChatResult.model_validate({"toolCallEvents": []})
    )
    assert not result.passed
    assert result.detail["answer_correct"] is False
    assert result.detail["answer_problems"] == ["the agent returned neither a chart nor an answer"]


def _fallback_chat(text: str) -> ChatResult:
    """A turn whose chart exists only as the fallback built from the tool arguments: the user saw none."""
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "createdVisualizations": {"objects": [{**_expected(), "id": ADHOC_VIZ_ID}], "reasoning": ""},
            "toolCallEvents": [],
        }
    )


@pytest.mark.parametrize(
    "expected_output",
    [{"expects_visualization": False}, {"visualization": _expected(), "visualization_optional": True}],
    ids=["no_chart", "visualization_optional"],
)
def test_a_fallback_chart_the_user_never_saw_is_no_chart(expected_output: dict) -> None:
    """A failed `create_adhoc_visualization` call still leaves its arguments as the fallback chart."""
    result = get_evaluator("visualization").evaluate(
        _item_with(expected_output), _fallback_chat("Which destination should the sankey flow to?")
    )
    assert result.passed, result.detail
    assert result.detail["no_chart"] is True


@pytest.mark.parametrize(
    ("expected_output", "message"),
    [
        ({"expects_visualization": False, "answer_must_inlcude": ["destination"]}, r"states \['answer_must_inlcude'\]"),
        ({"visualization": {**_expected(), "bucket_stric": True}}, r"chart states \['bucket_stric'\]"),
        (
            {"expected_outputs": [{"visualization": {**_expected(), "size": ["m_rev"]}}]},
            r"chart states \['size'\]",
        ),
    ],
    ids=["item_key", "chart_key", "chart_key_in_expected_outputs"],
)
def test_a_key_the_evaluator_does_not_read_is_rejected(expected_output: dict, message: str) -> None:
    """A misspelled key would otherwise be dropped, and the check it asks for would never run."""
    with pytest.raises(ValueError, match=message):
        expectation_options(expected_output)
