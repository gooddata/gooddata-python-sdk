# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic._kda_expectation import (
    KDA_FIELD_SCORES,
    check_kda_fields,
    parse_kda_expectation,
)
from gooddata_eval.core.agentic.kda_skill import (
    AgenticKdaSummary,
    KdaSkillAssertionError,
    _extract_kda_calls,
    evaluate_agentic_kda_skill,
    run_agentic_kda_skill,
)
from gooddata_eval.core.models import AgenticEvalOutcome, ChatResult, ToolCallEvent

# Shapes trimmed from nightly kda_skill traces on the globalmart fixture.
_REGION = "label/dim_geography_region.region_name"
_EXPECTED = {
    "check_fields": True,
    "Measure": {"id": "total_sales_amount_daily_store", "type": "metric"},
    "Date Attribute": "transaction_date.quarter",
    "Analyzed Period": "2024-4",
    "Reference Period": "2024-3",
    "Filters": [{"type": "attribute_filter", "state": {"exclude": ["United States East"]}, "using": _REGION}],
    "Summary": {
        "change": -1273867.76,
        "analyzed_value": 13868253.55,
        "reference_value": 15142121.31,
        "absolute_tolerance": 0.01,
    },
}
_CREATE = {
    "measure": {"id": "total_sales_amount_daily_store", "type": "metric", "aggregation": None},
    "date_attribute_id": "transaction_date.quarter",
    "analyzed_period": "2024-4",
    "reference_period": "2024-3",
    "filters": [{"type": "attribute_filter", "using": _REGION, "state": {"exclude": ["United States East"]}}],
}
_EXECUTE = {
    "success": True,
    "data": {
        "summary": {
            "reference_value": 15142121.31,
            "analyzed_value": 13868253.55,
            "change": -1273867.7599999998,
            "change_percentage": -8.412743062352336,
        }
    },
}
# 2a9704f3: the dashboard chart uses the transaction date, the question reads as the return date.
_BY_TRANSACTION: dict[str, Any] = {
    "Date Attribute": "transaction_date.quarter",
    "Summary": {"analyzed_value": 184, "reference_value": 163, "change": 21},
}
_BY_RETURN: dict[str, Any] = {
    "Date Attribute": "return_date.quarter",
    "Summary": {"analyzed_value": 191, "reference_value": 156, "change": 35},
}
_ANY_OF = {
    "check_fields": True,
    "Measure": {"id": "total_quantity_returned_returns", "type": "metric"},
    "Analyzed Period": "2026-2",
    "Reference Period": "2025-2",
    "Filters": [],
    "any_of": [_BY_TRANSACTION, _BY_RETURN],
}


def _with(base: dict, **changes: Any) -> dict:
    return {**base, **changes}


def _summary(analyzed: float, reference: float) -> dict:
    return {
        "success": True,
        "data": {"summary": {"analyzed_value": analyzed, "reference_value": reference, "change": analyzed - reference}},
    }


# --------------------------------------------------------------------------- #
# parse_kda_expectation


def test_items_without_check_fields_are_not_field_checked() -> None:
    assert not parse_kda_expectation({"Measure": {"id": "m", "type": "metric"}}).check_fields
    assert not parse_kda_expectation(_with(_EXPECTED, check_fields=False)).check_fields
    assert not parse_kda_expectation("not a dict").check_fields
    assert check_kda_fields(parse_kda_expectation({}), _CREATE, _EXECUTE) is None


def test_check_fields_reads_every_field() -> None:
    (option,) = parse_kda_expectation(_EXPECTED).options
    assert option.date_attribute == "transaction_date.quarter"
    assert option.summary == {"change": -1273867.76, "analyzed_value": 13868253.55, "reference_value": 15142121.31}
    assert option.tolerance == 0.01


@pytest.mark.parametrize(
    ("expected", "message"),
    [
        (_with(_EXPECTED, check_fields="yes"), "check_fields must be true or false"),
        ({k: v for k, v in _EXPECTED.items() if k != "Summary"}, "lacks Summary"),
        ({k: v for k, v in _EXPECTED.items() if k != "Filters"}, "lacks Filters"),
        (_with(_EXPECTED, Sumary={}), "unknown keys"),
        (_with(_EXPECTED, Measure={"type": "metric"}), "non-empty string id"),
        (_with(_EXPECTED, Measure=[]), "at least one candidate"),
        (_with(_EXPECTED, Measure={"id": "m", "type": "metric", "agg": "SUM"}), "unknown keys"),
        (_with(_EXPECTED, **{"Analyzed Period": ""}), "Analyzed Period must be a non-empty string"),
        (_with(_EXPECTED, **{"Date Attribute": True}), "Date Attribute must be a non-empty string"),
        (_with(_EXPECTED, **{"Date Attribute": 2024}), "Date Attribute must be a non-empty string"),
        (_with(_EXPECTED, Filters=["region"]), "Filters must hold objects"),
        (_with(_EXPECTED, Summary="13868253.55"), "Summary must be an object"),
        (_with(_EXPECTED, Summary={"change": True}), "change must be a number"),
        (_with(_EXPECTED, Summary={"change": "inf"}), "change must be a number"),
        (_with(_EXPECTED, Filters=None), "Filters must be a list"),
        (
            _with(_EXPECTED, Filters=[{"type": "date_filter", "using": "dataset/transaction_date"}]),
            "must not hold a date_filter",
        ),
        (_with(_EXPECTED, Summary={"absolute_tolerance": 0.01}), "at least one of"),
        (_with(_EXPECTED, Summary={"change": "a lot"}), "change must be a number"),
        (_with(_EXPECTED, Summary={"change": 1, "absolute_tolerance": "abc"}), "absolute_tolerance"),
        (_with(_EXPECTED, Summary={"change": 1, "absolute_tolerance": -1}), "absolute_tolerance"),
        (_with(_EXPECTED, Summary={"change": 1, "change_pct": 3}), "unknown keys"),
        ({k: v for k, v in _ANY_OF.items() if k != "check_fields"}, "any_of is read only with check_fields"),
        (_with(_ANY_OF, check_fields=False), "any_of is read only with check_fields"),
        (_with(_ANY_OF, any_of=[_BY_TRANSACTION]), "at least two"),
        (_with(_ANY_OF, any_of=[_BY_TRANSACTION, {}]), "at least two"),
        (_with(_ANY_OF, any_of=[_BY_TRANSACTION, {"check_fields": True}]), "may state only"),
        (_with(_ANY_OF, any_of=[_BY_TRANSACTION, {"Summary": {"change": 1}}]), "any_of[1] lacks Date Attribute"),
        (_with(_EXPECTED, Measure={"id": "m", "type": "Metric"}), "type must be one of"),
        (_with(_EXPECTED, Measure={"id": "m", "type": "facts"}), "type must be one of"),
        (_with(_EXPECTED, Measure={"id": "m", "type": "fact", "aggregation": "TOTAL"}), "aggregation must be one of"),
        (_with(_EXPECTED, Filters=[{"type": "attribute_filter", "state": {"include": ["A"]}}]), "non-empty using"),
        (
            _with(_EXPECTED, Filters=[{"type": "attribute_filter", "using": _REGION, "state": {"exclude": "East"}}]),
            "non-empty list of strings",
        ),
        (
            _with(_EXPECTED, Filters=[{"type": "attribute_filter", "using": _REGION, "state": {"include": []}}]),
            "non-empty list of strings",
        ),
        (
            _with(_EXPECTED, Filters=[{"type": "attribute_filter", "using": _REGION, "state": {"include": [None]}}]),
            "non-empty list of strings",
        ),
        (
            _with(
                _EXPECTED,
                Filters=[{"type": "attribute_filter", "using": _REGION, "state": {"include": ["A"], "exclude": ["B"]}}],
            ),
            "exactly one of include, exclude",
        ),
    ],
)
def test_malformed_field_checks_are_rejected(expected: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message.replace("[", r"\[").replace("]", r"\]")):
        parse_kda_expectation(expected)


@pytest.mark.parametrize(
    ("respelt", "canonical"),
    [("check fields", "check_fields"), ("Check_Fields", "check_fields"), ("any of", "any_of"), ("any-of", "any_of")],
)
def test_a_respelt_opt_in_key_is_rejected_not_ignored(respelt: str, canonical: str) -> None:
    expected = {k: v for k, v in _EXPECTED.items() if k != "check_fields"} | {respelt: True}
    with pytest.raises(ValueError, match=f"write '{canonical}', not '{respelt}'"):
        parse_kda_expectation(expected)


def test_aggregation_is_read_in_any_case() -> None:
    (option,) = parse_kda_expectation(
        _with(_EXPECTED, Measure={"id": "sales_amount", "type": "fact", "aggregation": "sum"})
    ).options
    assert option.measures[0]["aggregation"] == "sum"


def test_tolerance_given_as_a_string_is_read_as_a_number() -> None:
    (option,) = parse_kda_expectation(_with(_EXPECTED, Summary={"change": 1, "absolute_tolerance": "1E-2"})).options
    assert option.tolerance == 0.01


def test_tolerance_defaults_to_a_cent() -> None:
    (option,) = parse_kda_expectation(_with(_EXPECTED, Summary={"change": 1})).options
    assert option.tolerance == 0.01


def test_field_scores_are_named_after_the_fields() -> None:
    assert KDA_FIELD_SCORES == (
        "kda_measure_correct",
        "kda_date_attribute_correct",
        "kda_analyzed_period_correct",
        "kda_reference_period_correct",
        "kda_filters_correct",
        "kda_summary_correct",
    )


# --------------------------------------------------------------------------- #
# check_kda_fields


def test_a_matching_run_passes_every_field() -> None:
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), _CREATE, _EXECUTE)
    assert result is not None
    assert result.passed
    assert result.option_index == 0


def test_no_create_call_means_nothing_to_check() -> None:
    assert check_kda_fields(parse_kda_expectation(_EXPECTED), None, None) is None


def test_a_date_filter_the_agent_adds_is_ignored() -> None:
    create = _with(
        _CREATE,
        filters=[
            *_CREATE["filters"],
            {"type": "date_filter", "using": "dataset/transaction_date", "from": "2024-07-01", "to": "2024-12-31"},
        ],
    )
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), create, _EXECUTE)
    assert result is not None
    assert result.passed
    assert result.actual["filters"] == _CREATE["filters"]


def test_a_date_filter_that_changes_the_numbers_fails_summary() -> None:
    """ce857c85: the agent's own week bounds cut a day out of the reference week."""
    expected = _with(
        _EXPECTED,
        **{"Date Attribute": "return_date.week", "Analyzed Period": "2026-21", "Reference Period": "2026-20"},
        Filters=[],
        Summary={"analyzed_value": 1263.4, "reference_value": 2140.89},
    )
    create = _with(
        _CREATE,
        date_attribute_id="return_date.week",
        analyzed_period="2026-21",
        reference_period="2026-20",
        filters=[{"type": "date_filter", "using": "dataset/return_date", "from": "2026-05-11", "to": "2026-05-24"}],
    )
    result = check_kda_fields(parse_kda_expectation(expected), create, _summary(1263.4, 1972.36))
    assert result is not None
    assert result.checks == {
        "measure": True,
        "date_attribute": True,
        "analyzed_period": True,
        "reference_period": True,
        "filters": True,
        "summary": False,
    }


def test_an_extra_non_date_filter_fails_filters() -> None:
    """555dcae3: region South plus country United States instead of region United States South."""
    create = _with(
        _CREATE,
        filters=[
            {"type": "attribute_filter", "using": _REGION, "state": {"include": ["South"]}},
            {"type": "attribute_filter", "using": "label/sql_store_country.country_name", "state": {"include": ["US"]}},
        ],
    )
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), create, _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is False


@pytest.mark.parametrize("filters", [{"type": "attribute_filter"}, "none", 0, None])
def test_filters_that_are_not_a_list_fail_filters_and_are_reported(filters: object) -> None:
    spec = parse_kda_expectation(_with(_EXPECTED, Filters=[]))
    result = check_kda_fields(spec, _with(_CREATE, filters=filters), _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is False
    assert result.actual["filters"] == filters


def test_omitted_filters_are_no_filters() -> None:
    spec = parse_kda_expectation(_with(_EXPECTED, Filters=[]))
    create = {k: v for k, v in _CREATE.items() if k != "filters"}
    result = check_kda_fields(spec, create, _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is True


def test_a_missing_filter_fails_filters() -> None:
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), _with(_CREATE, filters=[]), _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is False


def test_include_and_exclude_are_different_filters() -> None:
    flipped = [{"type": "attribute_filter", "using": _REGION, "state": {"include": ["United States East"]}}]
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), _with(_CREATE, filters=flipped), _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is False


def test_a_filter_by_attribute_id_matches_one_by_label_id() -> None:
    by_attribute = [
        {
            "type": "attribute_filter",
            "using": "attribute/dim_geography_region.region_name",
            "state": {"exclude": ["United States East"]},
        }
    ]
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), _with(_CREATE, filters=by_attribute), _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is True


def test_filter_values_match_in_any_order() -> None:
    expected = _with(
        _EXPECTED,
        Filters=[{"type": "attribute_filter", "using": _REGION, "state": {"include": ["A", "B"]}}],
    )
    create = _with(_CREATE, filters=[{"type": "attribute_filter", "using": _REGION, "state": {"include": ["B", "A"]}}])
    result = check_kda_fields(parse_kda_expectation(expected), create, _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is True


def test_a_ranking_filter_matches_on_its_content_not_its_key_order() -> None:
    ranking = {"type": "ranking_filter", "using": "metric/net_sales", "top": 5}
    spec = parse_kda_expectation(_with(_EXPECTED, Filters=[ranking]))
    reordered = {"top": 5, "using": "metric/net_sales", "type": "ranking_filter"}
    same = check_kda_fields(spec, _with(_CREATE, filters=[reordered]), _EXECUTE)
    other = check_kda_fields(spec, _with(_CREATE, filters=[{**ranking, "top": 3}]), _EXECUTE)
    assert same is not None
    assert same.checks["filters"] is True
    assert other is not None
    assert other.checks["filters"] is False


@pytest.mark.parametrize(
    "malformed",
    [
        {"type": "attribute_filter", "state": {"exclude": ["United States East"]}},
        {"type": "attribute_filter", "using": 7, "state": {"exclude": ["United States East"]}},
        {"type": "attribute_filter", "using": _REGION, "state": {"exclude": "United States East"}},
        "label/dim_geography_region.region_name",
    ],
)
def test_a_malformed_filter_from_the_agent_fails_filters_without_an_error(malformed: object) -> None:
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), _with(_CREATE, filters=[malformed]), _EXECUTE)
    assert result is not None
    assert result.checks["filters"] is False


def test_another_measure_fails_measure() -> None:
    """ba0a7d21: the gift-card count picked from the dashboard's year chart."""
    create = _with(_CREATE, measure={"id": "gift_card_transaction_total_count", "type": "metric", "aggregation": None})
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), create, _EXECUTE)
    assert result is not None
    assert result.checks["measure"] is False


def test_measure_matches_any_listed_candidate() -> None:
    expected = _with(
        _EXPECTED,
        Measure=[{"id": "other", "type": "metric"}, {"id": "total_sales_amount_daily_store", "type": "metric"}],
    )
    result = check_kda_fields(parse_kda_expectation(expected), _CREATE, _EXECUTE)
    assert result is not None
    assert result.checks["measure"] is True


def test_measure_type_must_match() -> None:
    create = _with(_CREATE, measure={"id": "total_sales_amount_daily_store", "type": "fact", "aggregation": "SUM"})
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), create, _EXECUTE)
    assert result is not None
    assert result.checks["measure"] is False


def test_fact_aggregation_is_checked_only_when_expected() -> None:
    fact = {"id": "sales_amount", "type": "fact"}
    create = _with(_CREATE, measure={**fact, "aggregation": "sum"})
    spec_any = parse_kda_expectation(_with(_EXPECTED, Measure=fact))
    spec_sum = parse_kda_expectation(_with(_EXPECTED, Measure={**fact, "aggregation": "SUM"}))
    spec_avg = parse_kda_expectation(_with(_EXPECTED, Measure={**fact, "aggregation": "AVG"}))
    verdicts = [check_kda_fields(spec, create, _EXECUTE) for spec in (spec_any, spec_sum, spec_avg)]
    assert [v.checks["measure"] if v else None for v in verdicts] == [True, True, False]


def test_another_date_granularity_fails_date_attribute() -> None:
    """2af7ae17: months instead of quarters."""
    result = check_kda_fields(
        parse_kda_expectation(_EXPECTED), _with(_CREATE, date_attribute_id="transaction_date.month"), _EXECUTE
    )
    assert result is not None
    assert result.checks["date_attribute"] is False


def test_periods_are_compared_as_text() -> None:
    expected = _with(_EXPECTED, **{"Analyzed Period": 2024, "Reference Period": "2023"})
    create = _with(_CREATE, analyzed_period="2024", reference_period=2023)
    result = check_kda_fields(parse_kda_expectation(expected), create, _EXECUTE)
    assert result is not None
    assert result.checks["analyzed_period"] is True
    assert result.checks["reference_period"] is True


@pytest.mark.parametrize(
    ("expected", "actual", "same"),
    [
        ("2024-01", "2024-1", True),
        ("2026-03", "2026-3", True),
        ("2026-07-15", "2026-7-15", True),
        ("2024-3", "2024-Q3", False),
        ("2024-3", "2024-4", False),
    ],
)
def test_periods_match_on_their_numbers(expected: str, actual: str, same: bool) -> None:
    spec = parse_kda_expectation(_with(_EXPECTED, **{"Analyzed Period": expected}))
    result = check_kda_fields(spec, _with(_CREATE, analyzed_period=actual), _EXECUTE)
    assert result is not None
    assert result.checks["analyzed_period"] is same


def test_arguments_that_are_not_an_object_fail_every_field() -> None:
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), ["x"], _EXECUTE)
    assert result is not None
    assert not any(result.checks.values())


def test_swapped_periods_fail_both() -> None:
    create = _with(_CREATE, analyzed_period="2024-3", reference_period="2024-4")
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), create, _EXECUTE)
    assert result is not None
    assert result.checks["analyzed_period"] is False
    assert result.checks["reference_period"] is False


def test_summary_outside_the_tolerance_fails() -> None:
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), _CREATE, _summary(13868253.55, 15142121.33))
    assert result is not None
    assert result.checks["summary"] is False


@pytest.mark.parametrize(
    ("expected", "actual", "within"),
    [
        (100, 100.01, True),
        (100, 99.99, True),
        (100, 100.0101, False),
        (15142121.31, 15142121.32, True),
        (15142121.31, 15142121.33, False),
        (-1273867.76, -1273867.7599999998, True),
    ],
)
def test_the_tolerance_bound_is_inclusive(expected: float, actual: float, within: bool) -> None:
    spec = parse_kda_expectation(_with(_EXPECTED, Summary={"analyzed_value": expected}))
    result = check_kda_fields(spec, _CREATE, {"success": True, "data": {"summary": {"analyzed_value": actual}}})
    assert result is not None
    assert result.checks["summary"] is within


def test_summary_checks_only_the_values_the_item_states() -> None:
    expected = _with(_EXPECTED, Summary={"analyzed_value": 13868253.55})
    result = check_kda_fields(parse_kda_expectation(expected), _CREATE, _summary(13868253.55, 0))
    assert result is not None
    assert result.checks["summary"] is True


@pytest.mark.parametrize(
    "execute_result",
    [
        None,
        {"success": False, "data": {"summary": _EXECUTE["data"]["summary"]}},
        {"success": True, "data": {}},
        {"success": True, "data": {"summary": {"analyzed_value": "n/a"}}},
    ],
)
def test_summary_fails_without_a_usable_summary(execute_result: dict | None) -> None:
    result = check_kda_fields(parse_kda_expectation(_EXPECTED), _CREATE, execute_result)
    assert result is not None
    assert result.checks["summary"] is False
    assert result.checks["measure"] is True


def test_any_of_passes_on_either_option_and_names_it() -> None:
    spec = parse_kda_expectation(_ANY_OF)
    create = {
        "measure": {"id": "total_quantity_returned_returns", "type": "metric", "aggregation": None},
        "date_attribute_id": "return_date.quarter",
        "analyzed_period": "2026-2",
        "reference_period": "2025-2",
        "filters": [],
    }
    by_return = check_kda_fields(spec, create, _summary(191, 156))
    by_transaction = check_kda_fields(
        spec, _with(create, date_attribute_id="transaction_date.quarter"), _summary(184, 163)
    )
    assert by_return is not None
    assert by_return.passed
    assert by_return.option_index == 1
    assert by_transaction is not None
    assert by_transaction.passed
    assert by_transaction.option_index == 0


def test_the_simulated_user_answers_from_one_whole_any_of_option() -> None:
    """The base measure is replaced in every option, so offering it would steer the agent to a failing answer."""
    expected = _with(
        _ANY_OF,
        Measure={"id": "base_measure", "type": "metric"},
        any_of=[
            {**_BY_TRANSACTION, "Measure": {"id": "first", "type": "metric"}},
            {**_BY_RETURN, "Measure": {"id": "second", "type": "metric"}},
        ],
    )
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = [
        ChatResult.model_validate(
            {"textResponse": "Which date: transaction or return?", "toolCallEvents": [], "stream_ended": True}
        ),
        _chat_result(_CREATE, _EXECUTE),
    ]
    with (
        patch("gooddata_eval.core.agentic.kda_skill.ChatClient", return_value=client),
        patch(
            "gooddata_eval.core.agentic.kda_skill.generate_simulated_kda_response", return_value="Transaction date."
        ) as simulate,
    ):
        run_agentic_kda_skill(
            host="http://host", token="tok", workspace_id="ws1", question="q", expected_output=expected
        )
    _, measure_candidates, period_hint = simulate.call_args.args
    assert measure_candidates == {"id": "first", "type": "metric"}
    assert period_hint == "transaction_date.quarter, comparing 2026-2 to 2025-2"


def test_any_of_does_not_mix_one_options_date_with_anothers_summary() -> None:
    spec = parse_kda_expectation(_ANY_OF)
    create = {
        "measure": {"id": "total_quantity_returned_returns", "type": "metric"},
        "date_attribute_id": "return_date.quarter",
        "analyzed_period": "2026-2",
        "reference_period": "2025-2",
        "filters": [],
    }
    result = check_kda_fields(spec, create, _summary(184, 163))
    assert result is not None
    assert not result.passed
    assert result.option_index == 0  # a tie on five fields goes to the first option
    assert result.expected["date_attribute"] == "transaction_date.quarter"


# --------------------------------------------------------------------------- #
# run_agentic_kda_skill / evaluate_agentic_kda_skill


def _chat_result(create: dict, execute: dict) -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": "Here is the analysis.",
            "toolCallEvents": [
                {
                    "functionName": "create_key_driver_analysis",
                    "functionArguments": json.dumps(create),
                    "result": None,
                },
                {
                    "functionName": "execute_key_driver_analysis",
                    "functionArguments": "{}",
                    "result": json.dumps(execute),
                },
            ],
            "reasoningStepCount": 1,
            "reasoningSteps": [],
            "stream_ended": True,
        }
    )


def _client(create: dict = _CREATE, execute: dict = _EXECUTE) -> MagicMock:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = _chat_result(create, execute)
    return client


def _run(client: MagicMock, expected: dict) -> AgenticKdaSummary:
    with patch("gooddata_eval.core.agentic.kda_skill.ChatClient", return_value=client):
        return run_agentic_kda_skill(
            host="http://host", token="tok", workspace_id="ws1", question="q", expected_output=expected
        )


def test_a_run_matching_every_field_passes() -> None:
    ev = _run(_client(), _EXPECTED).best.evaluation
    assert ev.strict_pass
    assert ev.strict_checks["summary_correct"] is True


def test_a_wrong_field_fails_the_run() -> None:
    summary = _run(_client(create=_with(_CREATE, analyzed_period="2023-4")), _EXPECTED)
    ev = summary.best.evaluation
    assert not ev.strict_pass
    assert not summary.pass_at_k
    assert ev.strict_checks["analyzed_period_correct"] is False
    assert ev.success


def test_completion_only_items_ignore_wrong_fields() -> None:
    expected = {k: v for k, v in _EXPECTED.items() if k != "check_fields"}
    ev = _run(_client(create=_with(_CREATE, analyzed_period="2023-4")), expected).best.evaluation
    assert ev.strict_pass
    assert ev.fields is None
    assert set(ev.strict_checks) == {"triggered", "executed", "success", "turn_completed"}


def test_a_malformed_item_fails_before_any_request() -> None:
    client = _client()
    with pytest.raises(ValueError, match="lacks Summary"):
        _run(client, {k: v for k, v in _EXPECTED.items() if k != "Summary"})
    client.create_conversation.assert_not_called()
    client.send_message.assert_not_called()


def _evaluate(client: MagicMock, expected: dict, capture: dict | None = None) -> AgenticEvalOutcome:
    def _capture(_submit: object, _identity: object, **kwargs: Any) -> None:
        if capture is not None:
            capture["write_scores"] = kwargs["write_scores"]

    with (
        patch("gooddata_eval.core.agentic.kda_skill.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.kda_skill.submit_trace_scoring", _capture),
    ):
        return evaluate_agentic_kda_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="q",
            expected_output=expected,
            k=1,
            max_iterations=1,
            langfuse=MagicMock(),
            dataset_item_id="item-1",
        )


def _scores(capture: dict) -> dict:
    ctx = MagicMock()
    capture["write_scores"](ctx)
    return {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}


def test_field_scores_reach_langfuse() -> None:
    capture: dict = {}
    _evaluate(_client(), _EXPECTED, capture)
    scores = _scores(capture)
    assert {name: scores[name] for name in KDA_FIELD_SCORES} == dict.fromkeys(KDA_FIELD_SCORES, 1.0)
    assert scores["kda_triggered"] == 1.0


def test_completion_only_items_publish_no_field_scores() -> None:
    capture: dict = {}
    _evaluate(_client(), {k: v for k, v in _EXPECTED.items() if k != "check_fields"}, capture)
    assert not set(KDA_FIELD_SCORES) & set(_scores(capture))


def test_a_failing_field_is_reported_with_expected_and_actual() -> None:
    capture: dict = {}
    client = _client(create=_with(_CREATE, date_attribute_id="transaction_date.month"))
    with pytest.raises(KdaSkillAssertionError) as exc_info:
        _evaluate(client, _EXPECTED, capture)
    assert _scores(capture)["kda_date_attribute_correct"] == 0.0
    err = exc_info.value
    assert "date_attribute" in str(err)
    (failed_run,) = err.failed_runs
    assert {
        "name": "date_attribute_correct",
        "expected": "transaction_date.quarter",
        "actual": "transaction_date.month",
    } in failed_run["failed_checks"]
    assert err.detail["date_attribute_correct"] is False
    assert err.detail["field_option"] == 0


def test_a_malformed_item_fails_before_the_trace_opens() -> None:
    with (
        patch("gooddata_eval.core.agentic.kda_skill.open_item_trace") as mock_open,
        pytest.raises(ValueError, match="check_fields must be true or false"),
    ):
        evaluate_agentic_kda_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="q",
            expected_output=_with(_EXPECTED, check_fields="true"),
        )
    mock_open.assert_not_called()


def _event(name: str, arguments: object, result: object = None) -> ToolCallEvent:
    return ToolCallEvent.model_validate(
        {
            "functionName": name,
            "functionArguments": json.dumps(arguments),
            "result": None if result is None else json.dumps(result),
        }
    )


def test_execute_is_paired_with_the_create_whose_ref_it_names() -> None:
    first = _with(_CREATE, analyzed_period="2024-4")
    second = _with(_CREATE, analyzed_period="2023-4")
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", first, {"success": True, "kda_ref": "kda_1"}),
            _event("create_key_driver_analysis", second, {"success": True, "kda_ref": "kda_2"}),
            _event("execute_key_driver_analysis", {"kda_ref": "kda_1"}, _EXECUTE),
        ]
    )
    assert create_args == first
    assert execute_result == _EXECUTE


def test_an_execute_naming_an_unknown_ref_is_not_paired_with_another_create() -> None:
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", _CREATE, {"success": True, "kda_ref": "kda_1"}),
            _event("execute_key_driver_analysis", {"kda_ref": "kda_9"}, _EXECUTE),
        ]
    )
    assert create_args == _CREATE
    assert execute_result is None


@pytest.mark.parametrize("ref", [[], {}, None, 1])
def test_an_execute_with_a_malformed_ref_is_skipped_without_an_error(ref: object) -> None:
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", _CREATE, {"success": True, "kda_ref": "kda_1"}),
            _event("execute_key_driver_analysis", {"kda_ref": ref}, _EXECUTE),
        ]
    )
    assert create_args == _CREATE
    assert execute_result is None


def test_a_create_with_a_malformed_result_does_not_pair_without_a_ref() -> None:
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", _CREATE, []),
            _event("execute_key_driver_analysis", {"kda_ref": "kda_1"}, _EXECUTE),
        ]
    )
    assert create_args == _CREATE
    assert execute_result is None


def test_an_execute_with_malformed_arguments_is_no_execution() -> None:
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", _CREATE),
            _event("execute_key_driver_analysis", "kda_1", _EXECUTE),
        ]
    )
    assert create_args == _CREATE
    assert execute_result is None


def test_without_refs_an_execute_belongs_to_the_create_before_it() -> None:
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", _CREATE),
            _event("execute_key_driver_analysis", {"kda_ref": "kda_1"}, _EXECUTE),
        ]
    )
    assert create_args == _CREATE
    assert execute_result == _EXECUTE


def test_a_rejected_create_after_the_analysis_ran_is_ignored() -> None:
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", _CREATE, {"success": True, "kda_ref": "kda_1"}),
            _event("execute_key_driver_analysis", {"kda_ref": "kda_1"}, _EXECUTE),
            _event("create_key_driver_analysis", {"measure": {}}, {"success": False, "error": "bad date"}),
        ]
    )
    assert create_args == _CREATE
    assert execute_result == _EXECUTE


def test_a_rejected_create_then_a_retry_scores_the_retry() -> None:
    """0d6d3f7f: a snapshot date the measure cannot use, then the transaction date."""
    rejected = _with(_CREATE, date_attribute_id="snapshot_date.day")
    create_args, execute_result = _extract_kda_calls(
        [
            _event("create_key_driver_analysis", rejected, {"success": False, "error": "not valid for the measure"}),
            _event("create_key_driver_analysis", _CREATE, {"success": True, "kda_ref": "kda_1"}),
            _event("execute_key_driver_analysis", {"kda_ref": "kda_1"}, _EXECUTE),
        ]
    )
    assert create_args == _CREATE
    assert execute_result == _EXECUTE


def test_tool_calls_that_are_not_objects_do_not_break_the_run() -> None:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "Done.",
            "toolCallEvents": [
                {"functionName": "create_key_driver_analysis", "functionArguments": '["x"]', "result": None},
                {"functionName": "execute_key_driver_analysis", "functionArguments": '"kda_1"', "result": "[1]"},
            ],
            "reasoningStepCount": 1,
            "reasoningSteps": [],
            "stream_ended": True,
        }
    )
    ev = _run(client, _EXPECTED).best.evaluation
    assert ev.triggered
    assert not ev.executed
    assert not ev.strict_pass
