# (C) 2026 GoodData Corporation
"""Number-format intents (GDAI-2592). The shown texts are the ones GoodData's formatter
produced for the patterns the assistant wrote on stg11, 2026-10-13."""

import json

import pytest
from gooddata_eval.core.models import ToolCallEvent
from gooddata_eval.core.number_format import check_format_intents, format_problem, validate_format_intents

_MILLIONS = {"divide_by": 1000000, "decimals": 1, "suffix": "M"}


@pytest.mark.parametrize(
    ("intent", "value", "shown"),
    [
        (_MILLIONS, 4221301265.5, "4,221.3M"),  # #,##0.0,,M
        (_MILLIONS, 4221301265.5, "4221.3 M"),  # #,,.0 M -- no grouping, a space: still millions
        ({"divide_by": 1000, "decimals": 1, "suffix": "K"}, 24096.1, "24.1K"),
        ({"kind": "auto_scale", "decimals": 1}, 4221301265.5, "4.2 B"),
        ({"kind": "auto_scale", "decimals": 1}, 24096.1, "24.1 K"),
        ({"kind": "percent", "decimals": 1}, 0.253, "25.3%"),
        ({"prefix": "$", "decimals": 0}, 1234.4, "$1,234"),
        ({"negative": "parentheses", "decimals": 0}, -1234.5, "(1,235)"),
        ({"negative": "parentheses", "decimals": 0}, -1234.5, "(1,234)"),  # either rounding of .5
    ],
)
def test_an_example_that_reads_as_asked_passes(intent, value, shown):
    assert format_problem(intent, {"value": value, "shown_as": shown}) is None


@pytest.mark.parametrize(
    ("intent", "value", "shown"),
    [
        (_MILLIONS, 4221301265.5, "4,221,301,265.5M"),  # #,##0.0M: a letter appended, nothing divided
        (_MILLIONS, 4221301265.5, "4,221M"),  # millions, but no decimal
        ({"kind": "auto_scale", "decimals": 1}, 4221301265.5, "4,221,301,265.5a"),  # numeral.js syntax
        ({"kind": "percent", "decimals": 1}, 0.253, "0.3%"),
        ({"negative": "parentheses", "decimals": 0}, -1234.5, "-1,235"),
    ],
)
def test_an_example_that_does_not_read_as_asked_fails(intent, value, shown):
    problem = format_problem(intent, {"value": value, "shown_as": shown})
    assert problem is not None and "expected" in problem


@pytest.mark.parametrize(
    ("intent", "value"),
    [
        (_MILLIONS, 12.0),  # below a million: a format that divides nothing reads the same
        ({"kind": "auto_scale", "decimals": 1}, 999.0),
        ({"negative": "parentheses", "decimals": 0}, 5.0),
    ],
)
def test_an_example_that_cannot_show_the_intent_fails(intent, value):
    assert "cannot show" in format_problem(intent, {"value": value, "shown_as": str(value)})


def test_a_missing_or_null_example_fails():
    assert format_problem(_MILLIONS, None) == "no format_example was written"
    assert "no numeric value" in format_problem(_MILLIONS, {"value": None, "shown_as": "N/A"})


def _create_call(metrics: list, status: str = "success") -> ToolCallEvent:
    args = {
        "visualization": {
            "type": "bar_chart",
            "query": {"fields": {"m": {"using": "metric/net_sales"}, "d": {"using": "label/product_category"}}},
            "metrics": metrics,
            "view_by": ["d"],
        }
    }
    return ToolCallEvent.model_validate(
        {
            "functionName": "create_adhoc_visualization",
            "functionArguments": json.dumps(args),
            "result": json.dumps({"status": status, "ref": "viz_1"}),
        }
    )


def test_the_last_successful_chart_call_is_the_one_read():
    wrong = _create_call(
        [
            {
                "field": "m",
                "format": "#,##0.0M",
                "format_example": {"value": 4221301265.5, "shown_as": "4,221,301,265.5M"},
            }
        ]
    )
    right = _create_call(
        [{"field": "m", "format": "#,##0.0,,M", "format_example": {"value": 4221301265.5, "shown_as": "4,221.3M"}}]
    )
    rejected = _create_call([{"field": "m", "format": "#,##0.0M"}], status="error")
    intents = {"metric/net_sales": _MILLIONS}
    assert check_format_intents(intents, [wrong, right, rejected]) == []
    problems = check_format_intents(intents, [right, wrong])
    assert problems and "4,221,301,265.5M" in problems[0]


def test_a_metric_without_a_format_fails_and_one_that_needs_none_must_carry_none():
    plain = _create_call(["m"])
    assert check_format_intents({"metric/net_sales": _MILLIONS}, [plain]) == ["metric/net_sales: no format was written"]
    assert check_format_intents({"metric/net_sales": None}, [plain]) == []
    formatted = _create_call([{"field": "m", "format": "$#,##0", "format_example": {"value": 1, "shown_as": "$1"}}])
    assert "none was asked for" in check_format_intents({"metric/net_sales": None}, [formatted])[0]


@pytest.mark.parametrize(
    ("intents", "message"),
    [
        ({}, "must map metric uris"),
        ({"label/x": None}, "metric/ or fact/ uris"),
        ({"metric/x": {"divide": 1000}}, "which is not one of"),
        ({"metric/x": {"kind": "scaled"}}, "kind must be one of"),
        ({"metric/x": {"decimals": -1}}, "decimals must be"),
        ({"metric/x": {"divide_by": 0}}, "divide_by must be"),
        ({"metric/x": {"negative": "red"}}, "negative must be"),
    ],
)
def test_a_malformed_intent_is_rejected(intents, message):
    with pytest.raises(ValueError, match=message):
        validate_format_intents(intents)


def test_a_null_intent_is_valid_and_a_scalar_one_is_rejected():
    validate_format_intents({"metric/x": None, "metric/y": _MILLIONS})
    with pytest.raises(ValueError, match="must be an object or null"):
        validate_format_intents({"metric/x": "millions"})


@pytest.mark.parametrize(
    ("intent", "value", "shown", "ok"),
    [
        ({"prefix": "$", "decimals": 0}, -1234.4, "-$1,234", True),  # sign before the prefix
        ({"prefix": "$", "decimals": 0}, -1234.4, "$-1,234", True),  # sign after the prefix
        ({"prefix": "$", "decimals": 0}, 1234.4, "1,234", False),  # the prefix is missing
        ({"decimals": 0}, 1234.4, "1,23,4", False),  # not a number GoodData writes
        ({"decimals": 0}, 1234.4, "about 1,234", False),
    ],
)
def test_the_sign_the_prefix_and_the_digits_of_the_shown_text_are_read(intent, value, shown, ok):
    assert (format_problem(intent, {"value": value, "shown_as": shown}) is None) is ok


def _call(function_name: str, arguments: dict) -> ToolCallEvent:
    return ToolCallEvent.model_validate(
        {
            "functionName": function_name,
            "functionArguments": json.dumps(arguments),
            "result": json.dumps({"status": "success", "ref": "viz_1"}),
        }
    )


def test_other_tool_calls_and_a_call_without_a_chart_are_not_read():
    formatted = _create_call(
        [{"field": "m", "format": "#,##0.0,,M", "format_example": {"value": 4221301265.5, "shown_as": "4,221.3M"}}]
    )
    other = _call("execute_visualization", {"visualization_ref": "viz_1"})
    no_chart = _call("create_adhoc_visualization", {"visualization": "viz_1"})
    assert check_format_intents({"metric/net_sales": _MILLIONS}, [formatted, other, no_chart]) == []


@pytest.mark.parametrize("bucket", ["size_by", "columns"])
def test_a_format_on_a_metric_outside_the_metrics_bucket_is_read(bucket):
    """A bubble chart sizes by a metric in `size_by`; a repeater writes its metrics into `columns`."""
    entry = {"field": "m", "format": "#,##0.0,,M", "format_example": {"value": 4221301265.5, "shown_as": "4,221.3M"}}
    call = _create_call([])
    arguments = json.loads(call.function_arguments)
    arguments["visualization"][bucket] = [entry]
    call = _call("create_adhoc_visualization", arguments)
    assert check_format_intents({"metric/net_sales": _MILLIONS}, [call]) == []


@pytest.mark.parametrize(
    ("intent", "value", "shown"),
    [
        ({"decimals": 2, "prefix": "$"}, 0.45, "$0.45"),  # no scaling asked: a ratio below 1 shows as is
        ({"decimals": 0}, 0, "0"),
        ({"kind": "percent", "negative": "parentheses", "decimals": 1}, -0.123, "(12.3%)"),
        ({"kind": "auto_scale", "negative": "parentheses", "decimals": 1}, -4221301265.5, "(4.2B)"),
    ],
    ids=["ratio", "zero", "percent_in_parentheses", "auto_scale_in_parentheses"],
)
def test_an_example_without_scaling_or_with_parentheses_on_a_kind_is_read(
    intent: dict, value: float, shown: str
) -> None:
    assert format_problem(intent, {"value": value, "shown_as": shown}) is None


def test_parentheses_on_a_percent_still_need_the_percent() -> None:
    intent = {"kind": "percent", "negative": "parentheses", "decimals": 1}
    assert "expected '(12.3%)'" in format_problem(intent, {"value": -0.123, "shown_as": "(0.1)"})
