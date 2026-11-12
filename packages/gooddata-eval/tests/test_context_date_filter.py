# (C) 2026 GoodData Corporation
"""A date filter inherited from the dashboard in the item's `user_context`.

The rule is opt-in (`GD_EVAL_ACCEPT_CONTEXT_DATE_FILTER`, or `accept_context_date_filter=`).
With it off, every case here must score exactly as the strict comparison does.
"""

import json
from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic import visualization as agentic_visualization
from gooddata_eval.core.agentic.visualization import (
    VisualizationAssertionError,
    evaluate_agentic_visualization,
    run_agentic_visualization,
)
from gooddata_eval.core.evaluators import get_evaluator
from gooddata_eval.core.evaluators.visualization import _evaluate_against_candidates, evaluation_result_detail
from gooddata_eval.core.models import ChatResult, CreatedVisualization, DatasetItem
from gooddata_eval.core.scoring import check_filters, dashboard_date_filters

_ENV = "GD_EVAL_ACCEPT_CONTEXT_DATE_FILTER"
_TODAY = date(2026, 11, 12)

# The real item from the ticket: globalmart_visualization_charts_ctx_2, run 40229016049.
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


# ── the five acceptance-criteria cases (flag on) ─────────────────────────────


def test_inherited_dashboard_range_passes_and_is_marked_inherited():
    scores = check_filters(
        _viz(),
        _viz({"f_transaction_date": _INHERITED}),
        _TODAY,
        user_context=_USER_CONTEXT,
        accept_context_date_filter=True,
    )
    assert scores.date_ok is True
    assert scores.date_inherited is True
    assert scores.date_inherited_dataset == "dataset/transaction_date"
    assert scores.all_ok is True


def test_no_actual_date_filter_still_passes_without_being_inherited():
    scores = check_filters(_viz(), _viz(), _TODAY, user_context=_USER_CONTEXT, accept_context_date_filter=True)
    assert scores.date_ok is True
    assert scores.date_inherited is False


def test_a_range_other_than_the_dashboards_fails():
    scores = check_filters(
        _viz(), _viz({"f": _date(-5, 0)}), _TODAY, user_context=_USER_CONTEXT, accept_context_date_filter=True
    )
    assert scores.date_ok is False
    assert scores.date_inherited is False


@pytest.mark.parametrize(
    ("expected_filter", "actual_filter", "date_ok"),
    [
        # The question names a period: the dashboard's range is not good enough...
        (_date(-1, -1, "YEAR"), _INHERITED, False),
        # ...and the expected one still matches exactly, as before.
        (_date(-1, -1, "YEAR"), _date(-1, -1, "YEAR"), True),
        # Even an expected filter equal to the dashboard's is a strict match, not "inherited".
        (_INHERITED, _INHERITED, True),
    ],
)
def test_an_expected_date_filter_keeps_the_strict_comparison(expected_filter, actual_filter, date_ok):
    expected, actual = _viz({"f": expected_filter}), _viz({"f": actual_filter})
    scores = check_filters(expected, actual, _TODAY, user_context=_USER_CONTEXT, accept_context_date_filter=True)
    assert scores.date_ok is date_ok
    assert scores.date_inherited is False
    assert scores == check_filters(expected, actual, _TODAY)


@pytest.mark.parametrize("user_context", [None, {}, {"view": {}}, {"view": {"dashboard": {"id": "d"}}}])
def test_without_a_dashboard_date_filter_in_context_the_comparison_is_strict(user_context):
    scores = check_filters(
        _viz(), _viz({"f": _INHERITED}), _TODAY, user_context=user_context, accept_context_date_filter=True
    )
    assert scores.date_ok is False
    assert scores.date_inherited is False


# ── further edges of the rule ────────────────────────────────────────────────


def test_any_date_dataset_is_accepted_and_recorded():
    scores = check_filters(
        _viz(),
        _viz({"f": _date(-11, 0, using="dataset/order_date")}),
        _TODAY,
        user_context=_USER_CONTEXT,
        accept_context_date_filter=True,
    )
    assert scores.date_ok is True
    assert scores.date_inherited_dataset == "dataset/order_date"


def test_the_same_span_written_absolutely_is_accepted():
    # MONTH -11..0 on 2026-11-12 is 2025-12-01..2026-11-30.
    absolute = {"type": "date_filter", "using": "dataset/transaction_date", "from": "2025-12-01", "to": "2026-11-30"}
    scores = check_filters(
        _viz(), _viz({"f": absolute}), _TODAY, user_context=_USER_CONTEXT, accept_context_date_filter=True
    )
    assert scores.date_ok is True
    assert scores.date_inherited is True


def test_two_actual_date_filters_fail_even_if_one_is_the_dashboards():
    actual = _viz({"a": _INHERITED, "b": _date(-1, -1, "YEAR", using="dataset/order_date")})
    scores = check_filters(_viz(), actual, _TODAY, user_context=_USER_CONTEXT, accept_context_date_filter=True)
    assert scores.date_ok is False


def test_any_of_several_dashboard_date_filters_matches():
    context = {
        "view": {
            "dashboard": {
                "filters": [
                    {"type": "attribute_filter", "using": "label/region"},
                    {"type": "date_filter", "granularity": "YEAR", "from": 0, "to": 0},
                    {"type": "date_filter", "granularity": "MONTH", "from": -11, "to": 0},
                ]
            }
        }
    }
    assert len(dashboard_date_filters(context)) == 2
    scores = check_filters(
        _viz(), _viz({"f": _INHERITED}), _TODAY, user_context=context, accept_context_date_filter=True
    )
    assert scores.date_ok is True


def test_ranking_and_attribute_filters_are_not_relaxed():
    attribute = {"type": "attribute_filter", "using": "label/region", "state": {"include": ["EMEA"]}}
    scores = check_filters(
        _viz(),
        _viz({"f": _INHERITED, "r": attribute}),
        _TODAY,
        user_context=_USER_CONTEXT,
        accept_context_date_filter=True,
    )
    assert scores.date_ok is True
    assert scores.attribute_ok is False
    assert scores.all_ok is False


@pytest.mark.parametrize("malformed", ["text", {"view": "x"}, {"view": {"dashboard": {"filters": "x"}}}])
def test_a_malformed_context_is_ignored_not_raised(malformed):
    assert dashboard_date_filters(malformed) == []


# ── the flag ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("value", [None, "", "0", "false", "no", "off"])
def test_flag_off_scores_strictly(monkeypatch, value):
    if value is not None:
        monkeypatch.setenv(_ENV, value)
    expected, actual = _viz(), _viz({"f": _INHERITED})
    scores = check_filters(expected, actual, _TODAY, user_context=_USER_CONTEXT)
    assert scores.date_ok is False
    assert scores == check_filters(expected, actual, _TODAY)


@pytest.mark.parametrize("value", ["1", "true", "yes", "on"])
def test_flag_on_from_the_environment(monkeypatch, value):
    monkeypatch.setenv(_ENV, value)
    scores = check_filters(_viz(), _viz({"f": _INHERITED}), _TODAY, user_context=_USER_CONTEXT)
    assert scores.date_ok is True
    assert scores.date_inherited is True


def test_the_keyword_overrides_the_environment(monkeypatch):
    monkeypatch.setenv(_ENV, "1")
    scores = check_filters(
        _viz(), _viz({"f": _INHERITED}), _TODAY, user_context=_USER_CONTEXT, accept_context_date_filter=False
    )
    assert scores.date_ok is False


@pytest.mark.parametrize(
    "actual_filter_by",
    [{}, {"f": _INHERITED}, {"f": _date(-5, 0)}, {"a": _INHERITED, "b": _date(0, 0, "YEAR")}],
)
@pytest.mark.parametrize("expected_filter_by", [{}, {"f": _date(-1, -1, "YEAR")}])
def test_flag_off_detail_is_byte_identical_with_and_without_user_context(expected_filter_by, actual_filter_by):
    expected, actual = [_viz(expected_filter_by)], _viz(actual_filter_by)
    before, _ = _evaluate_against_candidates(expected, actual, True, _TODAY)
    after, _ = _evaluate_against_candidates(expected, actual, True, _TODAY, user_context=_USER_CONTEXT)
    assert after == before
    dump = json.dumps(evaluation_result_detail(before), sort_keys=True, default=sorted)
    assert json.dumps(evaluation_result_detail(after), sort_keys=True, default=sorted) == dump
    assert "filter_date_context" not in dump


# ── the real payload from the ticket, through both evaluation paths ──────────


def _ticket_item() -> DatasetItem:
    return DatasetItem(
        id="globalmart_visualization_charts_ctx_2",
        dataset_name="globalmart_visualization_charts_ctx",
        test_kind="visualization",
        question="Show Gross Margin Percent as a headline.",
        expected_output={"visualization": _headline()},
        user_context=_USER_CONTEXT,
    )


def _ticket_chat(metric: str = "metric/gross_margin_percent") -> ChatResult:
    return ChatResult.model_validate(
        {
            "createdVisualizations": {
                "objects": [_headline({"f_transaction_date": _INHERITED}, metric=metric)],
                "reasoning": "",
            },
            "toolCallEvents": [],
        }
    )


def test_ticket_item_single_shot_fails_with_the_flag_off():
    result = get_evaluator("visualization").evaluate(_ticket_item(), _ticket_chat())
    assert result.passed is False
    assert result.detail["filter_date_score"] is False
    assert "filter_date_context" not in result.detail


def test_ticket_item_single_shot_passes_with_the_flag_on(monkeypatch):
    monkeypatch.setenv(_ENV, "1")
    result = get_evaluator("visualization").evaluate(_ticket_item(), _ticket_chat())
    assert result.passed is True
    assert result.detail["filter_date_score"] is True
    assert result.detail["filter_date_context"] == {"inherited": True, "dataset": "dataset/transaction_date"}


def _agentic_client(chat: ChatResult) -> MagicMock:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.return_value = chat
    return client


@pytest.mark.parametrize(("flag", "passes"), [(None, False), ("1", True)])
def test_ticket_item_agentic_run(monkeypatch, flag, passes):
    if flag is not None:
        monkeypatch.setenv(_ENV, flag)
    with patch.object(agentic_visualization, "ChatClient", return_value=_agentic_client(_ticket_chat())):
        summary = run_agentic_visualization(
            host="https://example.com",
            token="tok",
            workspace_id="ws",
            question="Show Gross Margin Percent as a headline.",
            expected_outputs=[_viz()],
            k=1,
            user_context=_USER_CONTEXT,
        )
    ev = summary.best.eval_result
    assert ev.strict_pass is passes
    assert ev.filter_date_score is passes
    assert ev.filter_date_inherited is passes


def test_strict_check_summary_shows_the_inherited_date(monkeypatch):
    monkeypatch.setenv(_ENV, "1")
    # A wrong metric keeps the item failing, so the summary is printed.
    chat = _ticket_chat(metric="metric/revenue")
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
        )
    message = str(exc_info.value)
    assert "    date      : True (inherited from dashboard context)\n" in message
    assert "Metrics Correct       : False" in message


def test_strict_check_summary_is_unchanged_with_the_flag_off():
    with (
        patch.object(agentic_visualization, "ChatClient", return_value=_agentic_client(_ticket_chat())),
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
        )
    message = str(exc_info.value)
    assert "    date      : False\n" in message
    assert "inherited" not in message
