# (C) 2026 GoodData Corporation
"""The item-level `date_filter_from_context` key: a date filter taken from the dashboard in `user_context`.

Without the key, every case here must score exactly as the stated candidates alone do.
"""

import json
from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic import visualization as agentic_visualization
from gooddata_eval.core.agentic.visualization import (
    AgenticRunSummary,
    VisualizationAssertionError,
    evaluate_agentic_visualization,
    run_agentic_visualization,
)
from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.evaluators.visualization import (
    ContextDateFilter,
    EvaluationResult,
    ExpectationOptions,
    _evaluate_against_candidates,
    check_context_date_filter,
    context_date_candidates,
    dashboard_date_filters,
    date_dataset_uri,
    evaluation_result_detail,
    expectation_options,
)
from gooddata_eval.core.models import ChatResult, CreatedVisualization, DatasetItem
from gooddata_eval.core.runner import _run_one_item

_TODAY = date(2026, 11, 12)

# The dashboard of globalmart_visualization_charts_ctx: a common date filter, no dataset named.
_USER_CONTEXT = {
    "view": {
        "dashboard": {
            "id": "dashboard_033",
            "title": "Order Lines & Margin",
            "filters": [{"type": "date_filter", "granularity": "MONTH", "from": -11, "to": 0}],
        }
    }
}
_INHERITED = {
    "type": "date_filter",
    "using": "dataset/transaction_date",
    "granularity": "MONTH",
    "from": -11,
    "to": 0,
}
_ANY = ContextDateFilter()
_TRANSACTION_DATE = ContextDateFilter(dataset="dataset/transaction_date")


def _headline(filter_by: dict | None = None, metric: str = "metric/gross_margin_percent") -> dict:
    return {
        "id": "v",
        "type": "headline_chart",
        "query": {"fields": {"m": {"using": metric}}, "filter_by": filter_by or {}},
        "metrics": ["m"],
    }


def _viz(filter_by: dict | None = None) -> CreatedVisualization:
    return CreatedVisualization.model_validate(_headline(filter_by))


def _date(frm: int, to: int, granularity: str = "MONTH", using: str = "dataset/transaction_date") -> dict:
    return {"type": "date_filter", "using": using, "granularity": granularity, "from": frm, "to": to}


def _context(*filters: dict) -> dict:
    return {"view": {"dashboard": {"id": "d", "filters": list(filters)}}}


def _score(
    actual_filter_by: dict | None,
    expected_filter_by: dict | None = None,
    key: ContextDateFilter | None = _ANY,
    user_context: object = _USER_CONTEXT,
) -> EvaluationResult:
    ev, _ = _evaluate_against_candidates(
        [_viz(expected_filter_by)],
        _viz(actual_filter_by),
        True,
        _TODAY,
        user_context=user_context,
        context_date_filter=key,
    )
    return ev


# ── parsing the key ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("raw", "parsed"),
    [
        (False, None),
        (True, _ANY),
        ({"dataset": "dataset/transaction_date"}, _TRANSACTION_DATE),
        ({"dataset": "transaction_date"}, _TRANSACTION_DATE),
    ],
)
def test_the_key_parses(raw: object, parsed: ContextDateFilter | None) -> None:
    options = expectation_options({"visualization": _headline(), "date_filter_from_context": raw})
    assert options.date_filter_from_context == parsed


def test_an_absent_key_parses_to_none() -> None:
    assert expectation_options({"visualization": _headline()}).date_filter_from_context is None


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "yes",
        1,
        {},
        {"dataset": ""},
        {"dataset": 1},
        {"dataset": "x", "extra": 1},
        {"dataset": "datset/transaction_date"},
        {"dataset": "label/region"},
        {"dataset": "dataset/"},
    ],
)
def test_a_malformed_key_is_refused(raw: object) -> None:
    with pytest.raises(ValueError, match="date_filter_from_context"):
        expectation_options({"visualization": _headline(), "date_filter_from_context": raw})


def test_the_key_on_an_item_without_a_chart_is_refused() -> None:
    with pytest.raises(ValueError, match="date_filter_from_context"):
        expectation_options({"expects_visualization": False, "date_filter_from_context": True})


@pytest.mark.parametrize("user_context", [None, {}, {"view": {}}, {"view": {"dashboard": {"id": "d"}}}, "text"])
def test_the_key_without_a_dashboard_date_filter_in_context_is_refused(user_context: object) -> None:
    with pytest.raises(ValueError, match="no date filter"):
        check_context_date_filter(ExpectationOptions(date_filter_from_context=_ANY), user_context)


def test_without_the_key_any_context_is_fine() -> None:
    check_context_date_filter(ExpectationOptions(), None)


@pytest.mark.parametrize(
    ("raw", "uri"),
    [
        ("order_date", "dataset/order_date"),
        ("dataset/order_date", "dataset/order_date"),
        ("datset/order_date", None),
        ("label/region", None),
        ("dataset/", None),
        ("", None),
        (None, None),
    ],
)
def test_date_dataset_uri(raw: object, uri: str | None) -> None:
    assert date_dataset_uri(raw) == uri


@pytest.mark.parametrize("malformed", ["text", {"view": "x"}, {"view": {"dashboard": {"filters": "x"}}}])
def test_a_malformed_context_yields_no_dashboard_filter(malformed: object) -> None:
    assert dashboard_date_filters(malformed) == []


# ── scoring with the key ─────────────────────────────────────────────────────


def test_the_dashboard_period_passes_and_is_marked_inherited() -> None:
    ev = _score({"f_transaction_date": _INHERITED})
    assert ev.strict_pass is True
    assert ev.filter_date_score is True
    assert ev.filter_date_inherited_dataset == "dataset/transaction_date"


def test_no_date_filter_still_passes_without_being_inherited() -> None:
    ev = _score({})
    assert ev.strict_pass is True
    assert ev.filter_date_inherited is False


def test_a_period_other_than_the_dashboards_fails() -> None:
    ev = _score({"f": _date(-5, 0)})
    assert ev.filter_date_score is False
    assert ev.filter_date_inherited is False


@pytest.mark.parametrize(
    ("expected_filter", "actual_filter", "date_ok"),
    [
        (_date(-1, -1, "YEAR"), _INHERITED, False),
        (_date(-1, -1, "YEAR"), _date(-1, -1, "YEAR"), True),
        (_INHERITED, _INHERITED, True),
    ],
)
def test_a_candidate_stating_a_date_filter_is_not_extended(
    expected_filter: dict, actual_filter: dict, date_ok: bool
) -> None:
    ev = _score({"f": actual_filter}, {"f": expected_filter})
    assert ev.filter_date_score is date_ok
    assert ev.filter_date_inherited is False


def test_the_common_filter_with_true_takes_the_charts_dataset() -> None:
    ev = _score({"f": _date(-11, 0, using="dataset/order_date")})
    assert ev.filter_date_score is True
    assert ev.filter_date_inherited_dataset == "dataset/order_date"


@pytest.mark.parametrize(
    ("actual_dataset", "date_ok"), [("dataset/transaction_date", True), ("dataset/ship_date", False)]
)
def test_a_stated_dataset_accepts_only_that_one(actual_dataset: str, date_ok: bool) -> None:
    ev = _score({"f": _date(-11, 0, using=actual_dataset)}, key=_TRANSACTION_DATE)
    assert ev.filter_date_score is date_ok
    assert ev.filter_date_inherited is date_ok


@pytest.mark.parametrize("dashboard_using", ["order_date", "dataset/order_date"])
@pytest.mark.parametrize(("actual_dataset", "date_ok"), [("dataset/order_date", True), ("dataset/ship_date", False)])
def test_a_dashboard_filter_naming_a_dataset_accepts_only_that_one(
    dashboard_using: str, actual_dataset: str, date_ok: bool
) -> None:
    context = _context({"type": "date_filter", "using": dashboard_using, "granularity": "MONTH", "from": -11, "to": 0})
    ev = _score({"f": _date(-11, 0, using=actual_dataset)}, user_context=context)
    assert ev.filter_date_score is date_ok


def test_a_stated_dataset_wins_over_the_dashboard_filters() -> None:
    context = _context(_date(-11, 0, using="dataset/order_date"))
    ev = _score({"f": _INHERITED}, key=_TRANSACTION_DATE, user_context=context)
    assert ev.filter_date_inherited_dataset == "dataset/transaction_date"


def test_a_chart_date_filter_naming_no_dataset_matches_nothing() -> None:
    nameless = {k: v for k, v in _date(-11, 0).items() if k != "using"}
    ev = _score({"f": nameless})
    assert ev.filter_date_score is False


def test_the_same_span_written_absolutely_is_accepted() -> None:
    absolute = {"type": "date_filter", "using": "dataset/transaction_date", "from": "2025-12-01", "to": "2026-11-30"}
    ev = _score({"f": absolute})
    assert ev.filter_date_score is True
    assert ev.filter_date_inherited is True


def test_two_chart_date_filters_fail_even_if_one_is_the_dashboards() -> None:
    ev = _score({"a": _INHERITED, "b": _date(-1, -1, "YEAR", using="dataset/order_date")})
    assert ev.filter_date_score is False
    assert ev.filter_date_inherited is False


def test_any_of_several_dashboard_date_filters_matches() -> None:
    context = _context(
        {"type": "attribute_filter", "using": "label/region"},
        {"type": "date_filter", "granularity": "YEAR", "from": 0, "to": 0},
        {"type": "date_filter", "granularity": "MONTH", "from": -11, "to": 0},
    )
    assert len(dashboard_date_filters(context)) == 2
    assert _score({"f": _INHERITED}, user_context=context).filter_date_score is True


def test_ranking_and_attribute_filters_are_not_relaxed() -> None:
    attribute = {"type": "attribute_filter", "using": "label/region", "state": {"include": ["EMEA"]}}
    ev = _score({"f": _INHERITED, "r": attribute})
    assert ev.filter_date_score is True
    assert ev.filter_attribute_score is False
    assert ev.strict_pass is False


def test_derived_candidates_keep_the_stated_filters() -> None:
    attribute = {"type": "attribute_filter", "using": "label/region", "state": {"include": ["EMEA"]}}
    expected = _viz({"context_date_filter": attribute})
    derived = context_date_candidates([expected], _viz({"f": _INHERITED}), _USER_CONTEXT, _ANY)
    assert len(derived) == 1
    candidate, origin, dataset = derived[0]
    assert origin is expected
    assert dataset == "dataset/transaction_date"
    assert candidate.query.filter_by["context_date_filter"] == attribute
    assert candidate.query.filter_by["_context_date_filter"] == _INHERITED
    assert expected.query.filter_by == {"context_date_filter": attribute}


def test_a_dashboard_filter_whose_using_is_not_a_date_dataset_adds_no_candidate() -> None:
    context = _context({"type": "date_filter", "using": "label/region", "granularity": "MONTH", "from": -11, "to": 0})
    assert context_date_candidates([_viz()], _viz({"f": _INHERITED}), context, _ANY) == []
    assert _score({"f": _INHERITED}, user_context=context).filter_date_score is False


def test_a_matched_derived_candidate_reports_the_stated_one() -> None:
    expected = [_viz()]
    ev, best = _evaluate_against_candidates(
        expected, _viz({"f": _INHERITED}), True, _TODAY, user_context=_USER_CONTEXT, context_date_filter=_ANY
    )
    assert best is expected[0]
    assert ev.filter_date_inherited_dataset == "dataset/transaction_date"
    assert len(ev.expected_filters["date"]) == 1


def test_a_stated_candidate_matching_the_date_beats_a_derived_one_it_ties_with() -> None:
    stated_dated, stated_plain = _viz({"f": _INHERITED}), _viz()
    wrong_metric = CreatedVisualization.model_validate(_headline({"f": _INHERITED}, metric="metric/revenue"))
    ev, best = _evaluate_against_candidates(
        [stated_dated, stated_plain],
        wrong_metric,
        True,
        _TODAY,
        user_context=_USER_CONTEXT,
        context_date_filter=_ANY,
    )
    assert best is stated_dated
    assert ev.filter_date_score is True
    assert ev.filter_date_inherited is False


def test_a_stated_candidate_matching_the_date_wins_the_stated_ones_it_ties_with() -> None:
    region = {"type": "attribute_filter", "using": "label/region", "state": {"include": ["EMEA"]}}
    other_region = {**region, "state": {"include": ["APAC"]}}
    right_metric_wrong_region = _viz({"a": other_region})
    wrong_metric_right_filters = CreatedVisualization.model_validate(
        _headline({"d": _INHERITED, "a": region}, metric="metric/revenue")
    )
    candidates = [right_metric_wrong_region, wrong_metric_right_filters]
    actual = _viz({"d": _INHERITED, "a": region})
    ev, best = _evaluate_against_candidates(
        candidates, actual, True, _TODAY, user_context=_USER_CONTEXT, context_date_filter=_ANY
    )
    assert best is wrong_metric_right_filters
    assert ev.filter_date_inherited is False
    _, best_without_key = _evaluate_against_candidates(candidates, actual, True, _TODAY)
    assert best_without_key is right_metric_wrong_region


@pytest.mark.parametrize("using", ["label/region", "transaction_date", "datset/transaction_date"])
def test_a_chart_date_filter_not_on_a_dataset_uri_matches_nothing(using: str) -> None:
    ev = _score({"f": _date(-11, 0, using=using)})
    assert ev.filter_date_score is False
    assert ev.strict_pass is False
    assert ev.filter_date_inherited is False


def test_the_stated_candidate_is_returned_when_it_ties() -> None:
    expected = [_viz()]
    _, best = _evaluate_against_candidates(
        expected, _viz(), True, _TODAY, user_context=_USER_CONTEXT, context_date_filter=_ANY
    )
    assert best is expected[0]


# ── without the key nothing changes ──────────────────────────────────────────


@pytest.mark.parametrize(
    "actual_filter_by",
    [{}, {"f": _INHERITED}, {"f": _date(-5, 0)}, {"a": _INHERITED, "b": _date(0, 0, "YEAR")}],
)
@pytest.mark.parametrize("expected_filter_by", [{}, {"f": _date(-1, -1, "YEAR")}])
def test_without_the_key_the_detail_is_byte_identical(expected_filter_by: dict, actual_filter_by: dict) -> None:
    expected, actual = [_viz(expected_filter_by)], _viz(actual_filter_by)
    before, _ = _evaluate_against_candidates(expected, actual, True, _TODAY)
    after, _ = _evaluate_against_candidates(expected, actual, True, _TODAY, user_context=_USER_CONTEXT)
    assert after == before
    dump = json.dumps(evaluation_result_detail(before), sort_keys=True, default=sorted)
    assert json.dumps(evaluation_result_detail(after), sort_keys=True, default=sorted) == dump
    assert "filter_date_context" not in dump


# ── the item from the ticket, through both evaluation paths ─────────────────


def _item(expected_output: dict) -> DatasetItem:
    return DatasetItem(
        id="globalmart_visualization_charts_ctx_2",
        dataset_name="globalmart_visualization_charts_ctx",
        test_kind="visualization",
        question="Show Gross Margin Percent as a headline.",
        expected_output=expected_output,
        user_context=_USER_CONTEXT,
    )


def _chat(metric: str = "metric/gross_margin_percent", filter_by: dict | None = None) -> ChatResult:
    return ChatResult.model_validate(
        {
            "createdVisualizations": {
                "objects": [_headline(filter_by or {"f_transaction_date": _INHERITED}, metric=metric)],
                "reasoning": "",
            },
            "toolCallEvents": [],
        }
    )


def test_single_shot_fails_without_the_key() -> None:
    result = get_evaluator("visualization").evaluate(_item({"visualization": _headline()}), _chat())
    assert result.passed is False
    assert result.detail["filter_date_score"] is False
    assert "filter_date_context" not in result.detail


def test_single_shot_passes_with_the_key() -> None:
    item = _item({"visualization": _headline(), "date_filter_from_context": True})
    result = get_evaluator("visualization").evaluate(item, _chat())
    assert result.passed is True
    assert result.detail["filter_date_score"] is True
    assert result.detail["filter_date_context"] == {"inherited": True, "dataset": "dataset/transaction_date"}


def test_single_shot_refuses_the_key_without_a_dashboard_date_filter() -> None:
    item = _item({"visualization": _headline(), "date_filter_from_context": True})
    item = item.model_copy(update={"user_context": None})
    with pytest.raises(ValueError, match="no date filter"):
        get_evaluator("visualization").evaluate(item, _chat())


@pytest.mark.parametrize(
    ("expected_output", "user_context", "error"),
    [
        ({"visualization": _headline(), "date_filter_from_context": True}, None, "no date filter"),
        ({"visualization": _headline(), "date_filter_from_context": {"dataset": "label/x"}}, _USER_CONTEXT, "dataset"),
        ({"visualization": _headline(), "answer_must_inlcude": ["x"]}, _USER_CONTEXT, "answer_must_inlcude"),
    ],
)
def test_single_shot_runner_refuses_a_malformed_item_before_asking(
    expected_output: dict, user_context: dict | None, error: str
) -> None:
    item = _item(expected_output).model_copy(update={"user_context": user_context})
    backend = MagicMock()
    report = _run_one_item(item, backend, runs=2)
    backend.ask.assert_not_called()
    assert report.runs == 0
    assert report.error is not None
    assert report.error.startswith("ValueError:")
    assert error in report.error


def test_single_shot_runner_asks_for_a_valid_item() -> None:
    item = _item({"visualization": _headline(), "date_filter_from_context": True})
    backend = MagicMock()
    backend.ask.return_value = _chat()
    report = _run_one_item(item, backend, runs=1)
    backend.ask.assert_called_once()
    assert report.error is None
    assert report.pass_at_k is True


def _agentic_client(chat: ChatResult) -> MagicMock:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = chat
    return client


def _run(
    chat: ChatResult, options: ExpectationOptions | None, user_context: object = _USER_CONTEXT
) -> AgenticRunSummary:
    with patch.object(agentic_visualization, "ChatClient", return_value=_agentic_client(chat)):
        return run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show Gross Margin Percent as a headline.",
            expected_outputs=[_viz()],
            k=1,
            user_context=user_context,
            options=options,
        )


@pytest.mark.parametrize(
    ("options", "passes"),
    [(None, False), (ExpectationOptions(), False), (ExpectationOptions(date_filter_from_context=_ANY), True)],
)
def test_agentic_run(options: ExpectationOptions | None, passes: bool) -> None:
    ev = _run(_chat(), options).best.eval_result
    assert ev.strict_pass is passes
    assert ev.filter_date_score is passes
    assert ev.filter_date_inherited is passes


def test_agentic_run_refuses_the_key_before_any_request() -> None:
    client = _agentic_client(_chat())
    with (
        patch.object(agentic_visualization, "ChatClient", return_value=client),
        pytest.raises(ValueError, match="no date filter"),
    ):
        run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="q",
            expected_outputs=[_viz()],
            k=1,
            user_context=None,
            options=ExpectationOptions(date_filter_from_context=_ANY),
        )
    client.create_conversation.assert_not_called()


def _summary_message(chat: ChatResult, options: ExpectationOptions | None) -> str:
    with (
        patch.object(agentic_visualization, "ChatClient", return_value=_agentic_client(chat)),
        pytest.raises(VisualizationAssertionError) as exc_info,
    ):
        evaluate_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show Gross Margin Percent as a headline.",
            expected_outputs=[_viz()],
            k=1,
            user_context=_USER_CONTEXT,
            options=options,
        )
    return str(exc_info.value)


def test_strict_check_summary_shows_the_matched_dashboard_filter() -> None:
    message = _summary_message(_chat(metric="metric/revenue"), ExpectationOptions(date_filter_from_context=_ANY))
    assert "    date      : True (matches the dashboard date filter in user_context)\n" in message
    assert "Metrics Correct       : False" in message
    assert "context_date_filter" not in message


def test_strict_check_summary_is_unchanged_without_the_key() -> None:
    message = _summary_message(_chat(), None)
    assert "    date      : False\n" in message
    assert "dashboard date filter" not in message


def test_failed_checks_do_not_blame_the_matched_date_filter() -> None:
    attribute = {"type": "attribute_filter", "using": "label/region", "state": {"include": ["x"]}}
    chat = _chat(filter_by={"f_transaction_date": _INHERITED, "a": attribute})
    run = _run(chat, ExpectationOptions(date_filter_from_context=_ANY)).best
    assert run.eval_result.filter_date_inherited is True
    assert run.eval_result.filters_correct is False
    parts = [c.get("part") for c in agentic_visualization._failed_checks(run) if c.get("name") == "filters_correct"]
    assert "date" not in parts
    assert "attribute" in parts
