# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.dashboard_skill import (
    DashboardSkillAssertionError,
    _date_range_text,
    _extract_tool_result,
    _skill_activated,
    _widgets_of,
    build_simulated_reply,
    evaluate_agentic_dashboard_skill,
    evaluate_dashboard_response,
    run_agentic_dashboard_skill,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent

# Ids and titles are the ones the eval layout seeds; shapes are trimmed from real runs of
# `agent_dashboard_skill` against ecommerce_demo.
_TOTAL_CUSTOMERS = "9f2a657a-22e1-4791-8216-7a354bb8de5d"
_ACTIVE_CUSTOMERS = "dc8575f5-27e5-44be-a2dc-23d54b7777e7"
_RETURN_CUSTOMERS = "4cea4177-37c5-4196-8aab-c6bf60dc1f22"
_ACTIVITY_BY_HOUR = "f1027458-1123-4f4d-af20-0e21b1d5e009"
_NET_SALES = "700d732d-67e1-4658-a6e0-c6b8edbb6d49"

_ALL_TIME_FILTER = {"type": "date_filter", "granularity": "MONTH"}
_THIS_YEAR_FILTER = {"to": 0, "from": 0, "type": "date_filter", "granularity": "YEAR"}
_LAST_MONTH_FILTER = {"to": -1, "from": -1, "type": "date_filter", "granularity": "MONTH"}


def _widget(title: str, visualization: str, *, columns: int = 6) -> dict:
    return {"rows": 22, "columns": columns, "title": title, "visualization": visualization}


def _dashboard_part(
    widgets: list[dict],
    *,
    date_filter: dict,
    visualizations: list[str] | None = None,
    new_visualizations: list[str] | None = None,
    part_type: str = "dashboard",
    tabs: list[dict] | None = None,
) -> dict:
    default_tabs = [
        {
            "id": "overview",
            "title": "Overview",
            "filters": {"date": date_filter},
            "sections": [{"title": "Customer KPIs", "widgets": widgets}],
        }
    ]
    referenced = visualizations if visualizations is not None else [w["visualization"] for w in widgets]
    return {
        "type": part_type,
        "dashboard": {
            "id": "customer_overview_fafd7270",
            "type": "dashboard",
            "version": "3",
            "title": "Customer Overview",
            "tabs": tabs if tabs is not None else default_tabs,
        },
        "saved_dashboard_id": None,
        "references": {
            "datasets": [],
            "datedatasets": [],
            "visualizations": [{"id": vid, "type": "headline_chart", "title": vid} for vid in referenced],
            "new_visualizations": [{"id": vid, "type": "bar_chart", "title": vid} for vid in new_visualizations or []],
        },
    }


def _draft_result(new_visualization_count: int = 0, widget_count: int = 2) -> dict:
    return {
        "status": "success",
        "ref": "dash_1",
        "widget_count": widget_count,
        "new_visualization_count": new_visualization_count,
    }


def _tool_call(name: str, result: dict | None = None, arguments: dict | None = None) -> dict:
    return {
        "functionName": name,
        "functionArguments": "{}" if arguments is None else json.dumps(arguments),
        "result": None if result is None else json.dumps(result),
    }


def _chat_result(
    *, tool_calls: list[dict] | None = None, parts: list[dict] | None = None, text: str = ""
) -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "toolCallEvents": tool_calls or [],
            "unhandledParts": parts or [],
            "streamEnded": True,
        }
    )


_DC05_EXPECTED = {
    "type": "dashboard",
    "saved_dashboard_id": None,
    "visualizations": [
        {"id": _TOTAL_CUSTOMERS, "title": "Total Customers"},
        {"id": _ACTIVE_CUSTOMERS, "title": "Active Customers"},
    ],
    "date_range": {"granularity": "YEAR", "from": 0, "to": 0},
    "min_new_visualizations": 0,
}

_DC03_EXPECTED = {
    "type": "dashboard",
    "saved_dashboard_id": None,
    "visualizations": [
        {"id": _ACTIVITY_BY_HOUR, "title": "Activity by Hour"},
        {"id": None, "title": "Net Orders by Customer Age"},
    ],
    "date_range": None,
    "min_new_visualizations": 1,
}


# ── editing fixtures ────────────────────────────────────────────────────────
# Shapes trimmed from real edit runs: the base a saved dashboard relays is version 2 with
# `sections` at the root and no `tabs`, and it carries the id it was loaded from.
_ORDER_STATUS = "bc9120de-8d50-4c92-be62-6bbbda34208d"
_TOP_10_SPENDERS = "607e9724-37ed-44f6-9fb4-55676d58df6e"
_OVERVIEW_DASHBOARD = "092929af-375a-4e9c-964f-2add8cdbd259"


_SAVED_FILTERS = {
    "0_dateFilter": {"type": "date_filter", "granularity": "MONTH", "from": -1, "to": -1},
    "c47fea61aa7247cca2bab2096ce6e297": {"type": "attribute_filter", "using": "label/customer_country"},
    "1b0255ea4bfd4f11a832a8649abd73b2": {"type": "attribute_filter", "using": "label/product_category"},
}


def _edit_base_part(
    widgets: list[dict] | None = None,
    *,
    saved_dashboard_id: str = _OVERVIEW_DASHBOARD,
    visualizations: list[str] | None = None,
    filters: dict | None = None,
) -> dict:
    widgets = widgets if widgets is not None else [_widget("Order status", _ORDER_STATUS, columns=4)]
    referenced = visualizations if visualizations is not None else [w["visualization"] for w in widgets]
    return {
        "type": "dashboard",
        "dashboard": {
            "id": "overview",
            "type": "dashboard",
            "version": "2",
            "title": "1. Overview",
            "filters": _SAVED_FILTERS if filters is None else filters,
            "sections": [{"title": "Products overview", "widgets": widgets}],
        },
        "saved_dashboard_id": saved_dashboard_id,
        "references": {
            "visualizations": [{"id": vid, "type": "bar_chart", "title": vid} for vid in referenced],
            "new_visualizations": [],
        },
    }


def _patch_part(
    operations: list[dict],
    *,
    dashboard_id: str = _OVERVIEW_DASHBOARD,
    visualizations: list[str] | None = None,
    new_visualizations: list[str] | None = None,
) -> dict:
    return {
        "type": "dashboardPatch",
        "patch": {
            "dashboard_id": dashboard_id,
            "operations": operations,
            "references": {
                "visualizations": [{"id": v, "type": "bar_chart", "title": v} for v in visualizations or []],
                "new_visualizations": [{"id": v, "type": "bar_chart", "title": v} for v in new_visualizations or []],
            },
        },
    }


def _patch_result(new_visualization_count: int = 0) -> dict:
    return {
        "status": "success",
        "ref": "patch_1",
        "widget_count": 1,
        "new_visualization_count": new_visualization_count,
        "resized_count": 0,
        "operation_count": 3,
    }


_DE01_EXPECTED = {
    "type": "dashboardPatch",
    "saved_dashboard_id": _OVERVIEW_DASHBOARD,
    "visualizations": [{"id": _ORDER_STATUS, "title": "Order funnel", "columns": 4}],
    "min_new_visualizations": 0,
}


class TestExtractDraftResult:
    def test_returns_the_successful_payload(self):
        events = _as_events([_tool_call("draft_dashboard", _draft_result())])
        assert _extract_tool_result(events, "draft_dashboard") == _draft_result()

    def test_a_retry_is_not_shadowed_by_the_earlier_failure(self):
        events = _as_events(
            [
                _tool_call("draft_dashboard", {"status": "error", "message": "unknown visualization"}),
                _tool_call("draft_dashboard", _draft_result(widget_count=9)),
            ]
        )
        assert _extract_tool_result(events, "draft_dashboard") == _draft_result(widget_count=9)

    def test_a_failed_only_turn_yields_nothing(self):
        events = _as_events([_tool_call("draft_dashboard", {"status": "error"})])
        assert _extract_tool_result(events, "draft_dashboard") is None

    def test_a_call_without_a_result_yields_nothing(self):
        assert _extract_tool_result(_as_events([_tool_call("draft_dashboard")]), "draft_dashboard") is None


class TestBuilderSkillActivated:
    def test_reads_the_set_skills_result(self):
        events = _as_events([_tool_call("set_skills", {"skills_to_activate": ["dashboard_builder"]})])
        assert _skill_activated(events, "dashboard_builder") is True

    def test_activation_alongside_other_skills_counts(self):
        events = _as_events([_tool_call("set_skills", {"skills_to_activate": ["dashboard_builder", "search"]})])
        assert _skill_activated(events, "dashboard_builder") is True

    def test_a_different_skill_does_not_count(self):
        events = _as_events([_tool_call("set_skills", {"skills_to_activate": ["visualization"]})])
        assert _skill_activated(events, "dashboard_builder") is False


class TestEvaluateDraft:
    def test_passes_when_the_draft_carries_the_expected_charts(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert ev.strict_pass
        assert ev.failures == []

    def test_charts_the_agent_added_on_its_own_do_not_fail_the_case(self):
        part = _dashboard_part(
            [
                _widget("Total Customers", _TOTAL_CUSTOMERS),
                _widget("Active Customers", _ACTIVE_CUSTOMERS),
                _widget("Return Customers", _RETURN_CUSTOMERS),
            ],
            date_filter=_THIS_YEAR_FILTER,
        )
        assert evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True).strict_pass

    def test_a_missing_expected_chart_fails(self):
        part = _dashboard_part([_widget("Total Customers", _TOTAL_CUSTOMERS)], date_filter=_THIS_YEAR_FILTER)
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert not ev.charts_matched
        assert any("Active Customers" in f for f in ev.failures)

    def test_a_model_chosen_title_is_noted_rather_than_failed(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Customers (active)", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert ev.charts_matched
        assert ev.strict_pass
        assert any("Customers (active)" in n for n in ev.notes)

    def test_title_comparison_ignores_case_and_whitespace(self):
        part = _dashboard_part(
            [_widget("total   customers", _TOTAL_CUSTOMERS), _widget("ACTIVE CUSTOMERS", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        assert evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True).charts_matched

    def test_an_authored_chart_title_is_not_matched_by_prefix(self):
        """The layout holds both `Net Sales` and `Net Sales vs Orders`, so the authored-chart
        branch -- where the title is the only identity -- must not accept a longer title."""
        authored_id = "net_sales_vs_orders_11aa22bb"
        expected = {
            "type": "dashboard",
            "visualizations": [{"id": None, "title": "Net Sales"}],
            "date_range": None,
            "min_new_visualizations": 1,
        }
        part = _dashboard_part(
            [_widget("Net Sales vs Orders", authored_id)],
            date_filter=_ALL_TIME_FILTER,
            visualizations=[],
            new_visualizations=[authored_id],
        )
        ev = evaluate_dashboard_response(_draft_result(new_visualization_count=1), part, expected, skill_activated=True)
        assert not ev.charts_matched


class TestAdHocCharts:
    def test_an_authored_chart_is_matched_by_title(self):
        adhoc_id = "net_orders_by_customer_age_87e41365"
        part = _dashboard_part(
            [_widget("Activity by Hour", _ACTIVITY_BY_HOUR), _widget("Net Orders by Customer Age", adhoc_id)],
            date_filter=_ALL_TIME_FILTER,
            visualizations=[_ACTIVITY_BY_HOUR],
            new_visualizations=[adhoc_id],
        )
        ev = evaluate_dashboard_response(
            _draft_result(new_visualization_count=1), part, _DC03_EXPECTED, skill_activated=True
        )
        assert ev.strict_pass

    def test_an_existing_chart_of_the_same_title_does_not_satisfy_an_authored_one(self):
        existing_id = "b1d1f1a0-0000-4000-8000-000000000000"
        part = _dashboard_part(
            [_widget("Activity by Hour", _ACTIVITY_BY_HOUR), _widget("Net Orders by Customer Age", existing_id)],
            date_filter=_ALL_TIME_FILTER,
            visualizations=[_ACTIVITY_BY_HOUR, existing_id],
            new_visualizations=[],
        )
        ev = evaluate_dashboard_response(
            _draft_result(new_visualization_count=1), part, _DC03_EXPECTED, skill_activated=True
        )
        assert not ev.charts_matched

    def test_a_missing_count_is_reported_as_an_envelope_change(self):
        """Never "expected at least 0 authored chart(s), tool reported None" -- an assertion
        demanding zero that still fails reads as a broken test, and it would fail every
        fixture whose min_new_visualizations is 0 at once."""
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        ev = evaluate_dashboard_response(
            {"status": "success", "ref": "dash_1", "widget_count": 2}, part, _DC05_EXPECTED, skill_activated=True
        )
        assert not ev.new_visualizations_met
        assert ev.failures == ["the draft_dashboard result carries no new_visualization_count (got None)"]

    def test_a_real_shortfall_names_the_numbers(self):
        adhoc_id = "net_orders_by_customer_age_87e41365"
        part = _dashboard_part(
            [_widget("Activity by Hour", _ACTIVITY_BY_HOUR), _widget("Net Orders by Customer Age", adhoc_id)],
            date_filter=_ALL_TIME_FILTER,
            visualizations=[_ACTIVITY_BY_HOUR],
            new_visualizations=[adhoc_id],
        )
        ev = evaluate_dashboard_response(_draft_result(new_visualization_count=0), part, _DC03_EXPECTED, True)
        assert any("expected at least 1 authored chart(s), tool reported 0" in f for f in ev.failures)

    def test_too_few_authored_charts_fails(self):
        adhoc_id = "net_orders_by_customer_age_87e41365"
        part = _dashboard_part(
            [_widget("Activity by Hour", _ACTIVITY_BY_HOUR), _widget("Net Orders by Customer Age", adhoc_id)],
            date_filter=_ALL_TIME_FILTER,
            visualizations=[_ACTIVITY_BY_HOUR],
            new_visualizations=[adhoc_id],
        )
        ev = evaluate_dashboard_response(
            _draft_result(new_visualization_count=0), part, _DC03_EXPECTED, skill_activated=True
        )
        assert not ev.new_visualizations_met


class TestReferences:
    """gen-ai rejects a draft naming an unresolvable chart before it can succeed, so a widget
    missing from the references means its reference building degraded -- a platform fault that
    must not be scored as the agent's."""

    def test_a_reference_the_response_did_not_carry_is_a_note(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
            visualizations=[_TOTAL_CUSTOMERS],
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert ev.strict_pass
        assert not ev.references_carried
        assert any(_ACTIVE_CUSTOMERS in n for n in ev.notes)

    def test_references_degrading_to_empty_does_not_fail_an_existing_chart_case(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
            visualizations=[],
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert ev.strict_pass
        assert not ev.references_carried

    def test_an_authored_chart_still_needs_the_references_and_says_so(self):
        part = _dashboard_part(
            [_widget("Activity by Hour", _ACTIVITY_BY_HOUR), _widget("Net Orders by Customer Age", "adhoc_1")],
            date_filter=_ALL_TIME_FILTER,
            visualizations=[],
            new_visualizations=[],
        )
        ev = evaluate_dashboard_response(_draft_result(new_visualization_count=1), part, _DC03_EXPECTED, True)
        assert not ev.charts_matched
        assert any("listed no authored charts" in f for f in ev.failures)


class TestDateRange:
    def test_all_time_accepts_a_filter_without_bounds(self):
        expected = {**_DC03_EXPECTED, "visualizations": [], "min_new_visualizations": 0}
        part = _dashboard_part([], date_filter=_ALL_TIME_FILTER, visualizations=[])
        assert evaluate_dashboard_response(_draft_result(), part, expected, skill_activated=True).date_range_correct

    def test_all_time_rejects_a_bounded_filter(self):
        expected = {**_DC03_EXPECTED, "visualizations": [], "min_new_visualizations": 0}
        part = _dashboard_part([], date_filter=_THIS_YEAR_FILTER, visualizations=[])
        assert not evaluate_dashboard_response(_draft_result(), part, expected, skill_activated=True).date_range_correct

    def test_a_bounded_range_must_match_every_field(self):
        expected = {
            **_DC05_EXPECTED,
            "visualizations": [],
            "date_range": {"granularity": "MONTH", "from": -1, "to": -1},
        }
        part = _dashboard_part([], date_filter=_LAST_MONTH_FILTER, visualizations=[])
        assert evaluate_dashboard_response(_draft_result(), part, expected, skill_activated=True).date_range_correct

    def test_a_wrong_granularity_fails(self):
        expected = {**_DC05_EXPECTED, "visualizations": []}
        part = _dashboard_part([], date_filter={"to": 0, "from": 0, "granularity": "MONTH"}, visualizations=[])
        assert not evaluate_dashboard_response(_draft_result(), part, expected, skill_activated=True).date_range_correct

    def test_every_tab_is_checked(self):
        expected = {**_DC05_EXPECTED, "visualizations": []}
        tabs = [
            {"id": "a", "filters": {"date": _THIS_YEAR_FILTER}, "sections": []},
            {"id": "b", "filters": {"date": _ALL_TIME_FILTER}, "sections": []},
        ]
        part = _dashboard_part([], date_filter=_THIS_YEAR_FILTER, visualizations=[], tabs=tabs)
        ev = evaluate_dashboard_response(_draft_result(), part, expected, skill_activated=True)
        assert not ev.date_range_correct
        assert any("'b'" in f for f in ev.failures)


class TestDiagnostics:
    """Reported beside the gate so the decisions that moved them out of it stay reviewable."""

    def test_a_model_chosen_title_is_scored_even_though_it_does_not_fail(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Customers (active)", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert ev.strict_pass
        assert ev.diagnostics["titles_matched"] is False

    def test_a_clean_draft_reports_both_chart_level_observations(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert ev.diagnostics == {"references_carried": True, "titles_matched": True}

    def test_a_run_without_a_part_claims_nothing_about_charts(self):
        """Reporting these as true would say references and titles were fine on a run that
        produced neither."""
        ev = evaluate_dashboard_response(None, None, _DC05_EXPECTED, skill_activated=False)
        assert ev.diagnostics == {}

    def test_every_title_the_id_appears_under_is_named(self):
        part = _dashboard_part(
            [
                _widget("Customers (active)", _ACTIVE_CUSTOMERS),
                _widget("Active users", _ACTIVE_CUSTOMERS),
                _widget("Total Customers", _TOTAL_CUSTOMERS),
            ],
            date_filter=_THIS_YEAR_FILTER,
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        note = next(n for n in ev.notes if _ACTIVE_CUSTOMERS in n)
        assert "Customers (active)" in note
        assert "Active users" in note

    def test_a_title_placed_correctly_once_is_not_reported(self):
        part = _dashboard_part(
            [
                _widget("Active Customers", _ACTIVE_CUSTOMERS),
                _widget("Active Customers (copy)", _ACTIVE_CUSTOMERS),
                _widget("Total Customers", _TOTAL_CUSTOMERS),
            ],
            date_filter=_THIS_YEAR_FILTER,
        )
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert ev.diagnostics["titles_matched"] is True


class TestMissingPieces:
    def test_no_draft_reports_the_missing_draft(self):
        ev = evaluate_dashboard_response(None, None, _DC05_EXPECTED, skill_activated=False)
        assert not ev.drafted
        assert not ev.strict_pass
        assert any("never produced a successful draft_dashboard" in f for f in ev.failures)

    def test_a_draft_without_its_part_reports_the_missing_part(self):
        ev = evaluate_dashboard_response(_draft_result(), None, _DC05_EXPECTED, skill_activated=True)
        assert ev.drafted
        assert not ev.part_present
        assert any("'dashboard' part" in f for f in ev.failures)

    def test_an_edit_without_its_patch_part_names_what_is_missing(self):
        base = _edit_base_part()
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, skill_activated=True)
        assert not ev.part_present
        assert any("'dashboardPatch' part" in f for f in ev.failures)


class TestEditing:
    """Editing scores the document the patch produces, never the base it shipped with."""

    def test_a_rename_that_landed_passes(self):
        base = _edit_base_part()
        patch = _patch_part(
            [
                {"op": "test", "path": "/sections/0/widgets/0/visualization", "value": _ORDER_STATUS},
                {"op": "replace", "path": "/sections/0/widgets/0/title", "value": "Order funnel"},
            ],
            visualizations=[_ORDER_STATUS],
        )
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, True, patch_part=patch)
        assert ev.strict_pass
        assert ev.failures == []

    def test_a_rename_that_never_happened_fails(self):
        """The base still says "Order status". Scoring the base instead of the result would
        pass this case with the change missing."""
        base = _edit_base_part()
        patch = _patch_part([{"op": "test", "path": "/sections/0/widgets/0/visualization", "value": _ORDER_STATUS}])
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, True, patch_part=patch)
        assert not ev.charts_matched
        assert any("expected 'Order funnel'" in f for f in ev.failures)

    def test_a_resize_is_scored_on_the_width(self):
        expected = {
            "type": "dashboardPatch",
            "saved_dashboard_id": _OVERVIEW_DASHBOARD,
            "visualizations": [{"id": _TOP_10_SPENDERS, "title": "Top 10 Spenders", "columns": 12}],
            "min_new_visualizations": 0,
        }
        base = _edit_base_part([_widget("Top 10 Spenders", _TOP_10_SPENDERS, columns=6)])
        widened = _patch_part(
            [{"op": "replace", "path": "/sections/0/widgets/0/columns", "value": 12}],
            visualizations=[_TOP_10_SPENDERS],
        )
        assert evaluate_dashboard_response(_patch_result(), base, expected, True, patch_part=widened).strict_pass

        untouched = _patch_part([], visualizations=[_TOP_10_SPENDERS])
        ev = evaluate_dashboard_response(_patch_result(), base, expected, True, patch_part=untouched)
        assert not ev.charts_matched
        assert any("6 column(s) wide, expected 12" in f for f in ev.failures)

    def test_an_added_chart_is_read_from_the_patch_references(self):
        adhoc = "net_orders_by_customer_age_1eded609"
        expected = {
            "type": "dashboardPatch",
            "saved_dashboard_id": _OVERVIEW_DASHBOARD,
            "visualizations": [{"id": None, "title": "Net Orders by Customer Age", "columns": 6}],
            "min_new_visualizations": 1,
        }
        base = _edit_base_part()
        patch = _patch_part(
            [
                {
                    "op": "add",
                    "path": "/sections/0/widgets/1",
                    "value": _widget("Net Orders by Customer Age", adhoc),
                }
            ],
            new_visualizations=[adhoc],
        )
        ev = evaluate_dashboard_response(
            _patch_result(new_visualization_count=1), base, expected, True, patch_part=patch
        )
        assert ev.strict_pass

    def test_a_failing_test_guard_fails_the_case(self):
        """The guard pins the widget the agent is about to touch. If it does not hold, the
        patch was written against a document other than the one it shipped."""
        base = _edit_base_part()
        patch = _patch_part(
            [
                {"op": "test", "path": "/sections/0/widgets/0/visualization", "value": "some-other-chart"},
                {"op": "replace", "path": "/sections/0/widgets/0/title", "value": "Order funnel"},
            ]
        )
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, True, patch_part=patch)
        assert not ev.patch_applies
        assert any("does not apply" in f for f in ev.failures)

    def test_the_patch_and_the_response_must_address_the_expected_dashboard(self):
        base = _edit_base_part(saved_dashboard_id="a-different-dashboard")
        patch = _patch_part([], dashboard_id="a-third-dashboard")
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, True, patch_part=patch)
        assert not ev.saved_dashboard_id_correct
        assert sum("addresses dashboard" in f for f in ev.failures) == 2

    def test_a_new_draft_must_not_claim_a_saved_id(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        part["saved_dashboard_id"] = "already-saved"
        ev = evaluate_dashboard_response(_draft_result(), part, _DC05_EXPECTED, skill_activated=True)
        assert not ev.saved_dashboard_id_correct
        assert any("must not be saved yet" in f for f in ev.failures)

    def test_an_edit_answered_by_the_builder_is_a_routing_failure(self):
        base = _edit_base_part()
        patch = _patch_part(
            [{"op": "replace", "path": "/sections/0/widgets/0/title", "value": "Order funnel"}],
            visualizations=[_ORDER_STATUS],
        )
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, False, patch_part=patch)
        assert not ev.strict_pass
        assert ev.strict_checks["dashboard_skill_activated"] is False

    def test_the_titles_score_never_disagrees_with_the_gate(self):
        """An edit gates on the title through charts_matched. The score has to say the same
        thing -- "titles fine" beside a failed rename is worse than no score at all."""
        base = _edit_base_part()
        patch = _patch_part([], visualizations=[_ORDER_STATUS])
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, True, patch_part=patch)
        assert ev.strict_checks["charts_matched"] is False
        assert ev.diagnostics["titles_matched"] is False

    def test_an_edit_may_record_any_range_the_saved_dashboard_carries(self):
        """Only creation reaches the simulated user, so only creation has to state a range the
        reply can phrase. An edit records what the dashboard already has -- a rolling window
        the reply could not say aloud is still something the check can compare."""
        client = MagicMock()
        rolling = {**_DE01_EXPECTED, "date_range": {"granularity": "MONTH", "from": -11, "to": 0}}
        client.send_message.return_value = _chat_result()
        _run_with(client, rolling)  # accepted: no ValueError
        with pytest.raises(ValueError, match="unsupported date_range"):
            _run_with(client, {**_DC05_EXPECTED, "date_range": {"granularity": "MONTH", "from": -11, "to": 0}})

    def test_a_patch_that_does_not_apply_claims_nothing_about_charts(self):
        """part_present is true -- both parts arrived -- but nothing was scored, so the
        chart-level observations must not report success."""
        base = _edit_base_part()
        patch = _patch_part([{"op": "test", "path": "/sections/0/widgets/0/visualization", "value": "someone-else"}])
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, True, patch_part=patch)
        assert ev.part_present
        assert not ev.patch_applies
        assert ev.diagnostics == {}

    def test_an_edit_that_asks_back_stops_rather_than_sending_the_creation_reply(self):
        """The creation reply names charts and a date range, which answers nothing a rename or
        a resize could have asked. Sending it anyway would hide which cases need a reply of
        their own."""
        client = MagicMock()
        client.send_message.return_value = _chat_result(
            tool_calls=[_tool_call("set_skills", {"skills_to_activate": ["dashboard_editor"]})],
            text="Which widget did you mean?",
        )
        summary = _run_with(client, _DE01_EXPECTED, max_iterations=None)
        assert client.send_message.call_count == 1
        assert summary.best.total_turns == 1
        assert not summary.pass_at_k

    def test_a_creation_case_still_gets_its_clarifying_round(self):
        """The same cap that an edit never reaches is still spent on creation."""
        client = MagicMock()
        client.send_message.return_value = _chat_result(text="Which charts would you like?")
        _run_with(client, _DC05_EXPECTED, max_iterations=None)
        assert client.send_message.call_count > 1

    def test_the_date_filter_is_not_looked_at_without_a_date_range_key(self):
        """A dashboard the user has not opened carries no filter context, so an edit says
        nothing about the date range and the check must not invent an answer."""
        assert "date_range" not in _DE01_EXPECTED
        base = _edit_base_part()
        patch = _patch_part(
            [{"op": "replace", "path": "/sections/0/widgets/0/title", "value": "Order funnel"}],
            visualizations=[_ORDER_STATUS],
        )
        ev = evaluate_dashboard_response(_patch_result(), base, _DE01_EXPECTED, True, patch_part=patch)
        assert ev.date_range_correct
        assert ev.strict_pass


class TestPreservedFilters:
    """GDAI-2450: an edit that was not asked to touch the date range or the filters must leave
    them alone. The expectation opts in -- a case that says nothing about them is not checked,
    so the edit cases that are about something else stay unaffected."""

    _RENAME = [{"op": "replace", "path": "/sections/0/widgets/0/title", "value": "Order funnel"}]
    _EXPECTED_FILTERS = [
        {"using": "label/customer_country", "selection": "all"},
        {"using": "label/product_category", "selection": "all"},
    ]
    _DE01_WITH_FILTERS = {
        **_DE01_EXPECTED,
        "date_range": {"granularity": "MONTH", "from": -1, "to": -1},
        "filters": _EXPECTED_FILTERS,
    }

    def _score(self, expected: dict, *, filters: dict | None = None):
        base = _edit_base_part(filters=filters)
        patch = _patch_part(self._RENAME, visualizations=[_ORDER_STATUS])
        return evaluate_dashboard_response(_patch_result(), base, expected, True, patch_part=patch)

    def test_an_untouched_dashboard_keeps_its_range_and_filters(self):
        ev = self._score(self._DE01_WITH_FILTERS)
        assert ev.strict_pass
        assert ev.failures == []

    def test_a_date_range_reset_to_all_time_fails(self):
        """The shape the bug produces: the range is gone, the granularity left behind."""
        reset = {**_SAVED_FILTERS, "0_dateFilter": {"type": "date_filter", "granularity": "MONTH"}}
        ev = self._score(self._DE01_WITH_FILTERS, filters=reset)
        assert not ev.date_range_correct
        assert ev.filters_correct
        assert any("date from expected -1, got None" in f for f in ev.failures)

    def test_a_dropped_attribute_filter_fails(self):
        dropped = {k: v for k, v in _SAVED_FILTERS.items() if "customer_country" not in str(v)}
        ev = self._score(self._DE01_WITH_FILTERS, filters=dropped)
        assert not ev.filters_correct
        assert any("no attribute filter on 'label/customer_country'" in f for f in ev.failures)

    def test_a_filter_narrowed_to_a_selection_fails(self):
        narrowed = {
            **_SAVED_FILTERS,
            "c47fea61aa7247cca2bab2096ce6e297": {
                "type": "attribute_filter",
                "using": "label/customer_country",
                "state": {"include": ["United States"]},
            },
        }
        ev = self._score(self._DE01_WITH_FILTERS, filters=narrowed)
        assert not ev.filters_correct
        assert any("expected all" in f for f in ev.failures)

    def test_a_case_that_says_nothing_about_them_is_not_checked(self):
        """The question DE-02 and DE-03 answer: adding the keys to one case leaves the others
        alone, because absence means "do not look" for both keys."""
        assert "date_range" not in _DE01_EXPECTED
        assert "filters" not in _DE01_EXPECTED
        wrecked = {"0_dateFilter": {"type": "date_filter", "granularity": "YEAR", "from": 0, "to": 0}}
        ev = self._score(_DE01_EXPECTED, filters=wrecked)
        assert ev.strict_pass
        assert ev.date_range_correct
        assert ev.filters_correct

    @pytest.mark.parametrize(
        ("broken", "match"),
        [
            ({"date_range": "last month"}, "date_range must be an object or null"),
            ({"date_range": [-1, -1]}, "date_range must be an object or null"),
            ({"filters": {"label/customer_country": "all"}}, "filters must be a list"),
            ({"filters": ["label/customer_country"]}, "filter expectation must be an object"),
        ],
    )
    def test_a_malformed_shape_is_rejected_before_any_request(self, broken, match):
        """Shape is checked on both kinds of case. An edit skips only the *phrasing* check, so
        without this a string date_range would reach scoring and die there with an
        AttributeError -- after the run had already been spent."""
        client = MagicMock()
        with pytest.raises(ValueError, match=match):
            _run_with(client, {**self._DE01_WITH_FILTERS, **broken})
        client.send_message.assert_not_called()

    def test_an_unreadable_filter_expectation_is_rejected_up_front(self):
        client = MagicMock()
        expected = {**self._DE01_WITH_FILTERS, "filters": [{"using": "label/x", "selection": "some"}]}
        with pytest.raises(ValueError, match="needs 'selection'"):
            _run_with(client, expected)
        client.send_message.assert_not_called()

    def test_a_filter_expectation_without_a_label_is_rejected_up_front(self):
        client = MagicMock()
        expected = {**self._DE01_WITH_FILTERS, "filters": [{"selection": "all"}]}
        with pytest.raises(ValueError, match="needs the label it filters on"):
            _run_with(client, expected)
        client.send_message.assert_not_called()


class TestLayoutShapes:
    def test_widgets_are_read_from_root_sections(self):
        """A saved dashboard relayed for editing is version 2: sections at the root, no tabs."""
        base = _edit_base_part([_widget("A", "id-a"), _widget("B", "id-b")])["dashboard"]
        assert "tabs" not in base
        assert [w["visualization"] for w in _widgets_of(base)] == ["id-a", "id-b"]

    def test_widgets_are_read_from_tabs_when_present(self):
        drafted = _dashboard_part([_widget("A", "id-a")], date_filter=_ALL_TIME_FILTER)["dashboard"]
        assert [w["visualization"] for w in _widgets_of(drafted)] == ["id-a"]


class TestSimulatedReply:
    def test_existing_charts_are_listed_verbatim(self):
        expected = {
            "visualizations": [
                {"id": _TOTAL_CUSTOMERS, "title": "Total Customers"},
                {"id": _ACTIVE_CUSTOMERS, "title": "Active Customers"},
            ],
            "date_range": {"granularity": "YEAR", "from": 0, "to": 0},
        }
        assert build_simulated_reply(expected) == (
            "Please use these charts: Total Customers, Active Customers. "
            "Date range: this year. "
            "Anything else is up to you. Please create the dashboard now."
        )

    def test_an_authored_chart_is_appended(self):
        assert build_simulated_reply(_DC03_EXPECTED) == (
            'Please use these charts: Activity by Hour, and a new chart titled "Net Orders by Customer Age". '
            "Date range: all time. "
            "Anything else is up to you. Please create the dashboard now."
        )

    def test_an_authored_chart_alone_reads_naturally(self):
        expected = {"visualizations": [{"id": None, "title": "Net Orders by Customer Age"}], "date_range": None}
        assert 'Please use these charts: a new chart titled "Net Orders by Customer Age".' in build_simulated_reply(
            expected
        )

    @pytest.mark.parametrize(
        ("date_range", "text"),
        [
            (None, "all time"),
            ({"granularity": "YEAR", "from": 0, "to": 0}, "this year"),
            ({"granularity": "MONTH", "from": -1, "to": -1}, "last month"),
        ],
    )
    def test_date_range_wording(self, date_range, text):
        assert _date_range_text(date_range) == text

    def test_an_unsupported_range_fails_loudly(self):
        with pytest.raises(ValueError, match="unsupported date_range"):
            _date_range_text({"granularity": "MONTH", "from": -3, "to": -1})


class TestFixtureValidation:
    """A hand-written fixture has to fail before the run spends an API call."""

    def test_an_expectation_without_charts_is_rejected(self):
        client = MagicMock()
        with pytest.raises(ValueError, match="no visualizations"):
            _run_with(client, {"type": "dashboard", "visualizations": [], "date_range": None})
        client.send_message.assert_not_called()

    def test_an_unparseable_minimum_is_rejected_up_front(self):
        client = MagicMock()
        with pytest.raises(ValueError, match="min_new_visualizations is not a number"):
            _run_with(client, {**_DC05_EXPECTED, "min_new_visualizations": "two"})
        client.send_message.assert_not_called()

    def test_a_negative_minimum_is_rejected_up_front(self):
        """A negative bound makes the comparison true for any count, switching the check off
        without saying so -- which is the drift this validation exists to prevent."""
        client = MagicMock()
        with pytest.raises(ValueError, match="must not be negative"):
            _run_with(client, {**_DC05_EXPECTED, "min_new_visualizations": -1})
        client.send_message.assert_not_called()

    def test_an_unphrasable_date_range_is_rejected_up_front(self):
        """Not left to the clarify branch: the same fixture would otherwise pass when the model
        drafts straight away and crash when it asks, depending on the run."""
        client = MagicMock()
        expected = {**_DC05_EXPECTED, "date_range": {"granularity": "MONTH", "from": -11, "to": 0}}
        with pytest.raises(ValueError, match="unsupported date_range"):
            _run_with(client, expected)
        client.send_message.assert_not_called()


class TestRunLoop:
    def test_a_first_turn_draft_never_reaches_the_simulated_user(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        client = MagicMock()
        client.send_message.return_value = _chat_result(
            tool_calls=[
                _tool_call("set_skills", {"skills_to_activate": ["dashboard_builder"]}),
                _tool_call("draft_dashboard", _draft_result()),
            ],
            parts=[part],
        )
        summary = _run_with(client, _DC05_EXPECTED)
        assert client.send_message.call_count == 1
        assert summary.pass_at_k
        assert summary.best.evaluation.skill_activated

    def test_a_clarifying_turn_is_answered_from_the_expectation(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        client = MagicMock()
        client.send_message.side_effect = [
            _chat_result(
                tool_calls=[_tool_call("set_skills", {"skills_to_activate": ["dashboard_builder"]})],
                text="What time range should the dashboard default to?",
            ),
            _chat_result(tool_calls=[_tool_call("draft_dashboard", _draft_result())], parts=[part]),
        ]
        summary = _run_with(client, _DC05_EXPECTED)
        assert client.send_message.call_count == 2
        assert client.send_message.call_args_list[1].args[1] == build_simulated_reply(_DC05_EXPECTED)
        assert summary.pass_at_k
        assert summary.best.total_turns == 2

    def test_the_question_goes_once_and_every_later_turn_repeats_the_same_reply(self):
        """The reply is built from the expectation, so it cannot change between turns. The
        rounds after the first are slack for a turn that produced nothing, not an attempt to
        say something new -- which is why they are allowed to be identical."""
        client = MagicMock()
        client.send_message.return_value = _chat_result(text="Which charts would you like?")
        _run_with(client, _DC05_EXPECTED, max_iterations=None)
        sent = [call.args[1] for call in client.send_message.call_args_list]
        assert sent[0] == "Could you create a dashboard?"
        assert set(sent[1:]) == {build_simulated_reply(_DC05_EXPECTED)}

    def test_a_wasted_first_turn_still_leaves_the_reply_a_chance(self):
        """The case this slack exists for: the opening turn comes back without a draft, and the
        cap must not have been spent by it."""
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        client = MagicMock()
        client.send_message.side_effect = [
            _chat_result(text="Sorry, something went wrong on our side."),
            _chat_result(text="Which charts would you like?"),
            _chat_result(
                tool_calls=[
                    _tool_call("set_skills", {"skills_to_activate": ["dashboard_builder"]}),
                    _tool_call("draft_dashboard", _draft_result()),
                ],
                parts=[part],
            ),
        ]
        summary = _run_with(client, _DC05_EXPECTED, max_iterations=None)
        assert summary.pass_at_k
        assert summary.best.total_turns == 3

    def test_the_last_dashboard_part_of_a_turn_wins(self):
        """Matches _extract_tool_result taking the last successful call: a turn that drafts and
        then refines must be read as the state it left behind."""
        superseded = _dashboard_part([_widget("Total Customers", _TOTAL_CUSTOMERS)], date_filter=_THIS_YEAR_FILTER)
        final = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        client = MagicMock()
        client.send_message.return_value = _chat_result(
            tool_calls=[
                _tool_call("set_skills", {"skills_to_activate": ["dashboard_builder"]}),
                _tool_call("draft_dashboard", _draft_result()),
            ],
            parts=[superseded, final],
        )
        assert _run_with(client, _DC05_EXPECTED).pass_at_k

    def test_the_loop_is_capped(self):
        client = MagicMock()
        client.send_message.return_value = _chat_result(text="Which charts would you like?")
        summary = _run_with(client, _DC05_EXPECTED, max_iterations=2)
        assert client.send_message.call_count == 2
        assert not summary.pass_at_k
        assert not summary.best.evaluation.drafted

    def test_an_empty_turn_stops_the_loop(self):
        client = MagicMock()
        client.send_message.return_value = _chat_result()
        summary = _run_with(client, _DC05_EXPECTED, max_iterations=5)
        assert client.send_message.call_count == 1
        assert not summary.pass_at_k

    def test_a_caller_supplied_conversation_is_not_deleted(self):
        client = MagicMock()
        client.send_message.return_value = _chat_result()
        _run_with(client, _DC05_EXPECTED, initial_conversation_id="conv-1")
        client.create_conversation.assert_not_called()
        client.delete_conversation.assert_not_called()


class TestEvaluateEntryPoint:
    def test_a_failing_run_raises_with_the_failures_attached(self):
        client = MagicMock()
        client.send_message.return_value = _chat_result(text="Which charts would you like?")
        with pytest.raises(DashboardSkillAssertionError) as excinfo:
            _evaluate_with(client, _DC05_EXPECTED)
        message = str(excinfo.value)
        assert "No set_skills call activated dashboard_builder" in message
        assert excinfo.value.detail["dashboard_drafted"] is False
        assert excinfo.value.conversation_id == "conv-1"

    def test_a_mis_routed_edit_names_the_skill_the_fixture_asked_for(self):
        """The builder answering an edit activates dashboard_builder perfectly well. Naming it
        in the failure sends the reader after a feature flag that is already on, past the real
        problem -- and the tool having succeeded is exactly when they most need the right name."""
        client = MagicMock()
        client.send_message.return_value = _chat_result(
            tool_calls=[
                _tool_call("set_skills", {"skills_to_activate": ["dashboard_builder"]}),
                _tool_call("draft_dashboard", _draft_result()),
            ],
        )
        with pytest.raises(DashboardSkillAssertionError) as excinfo:
            _evaluate_with(client, _DE01_EXPECTED)
        message = str(excinfo.value)
        assert "activated dashboard_builder instead of dashboard_editor" in message
        assert "routing failure, not the flag" in message
        assert "feature flag" not in message

    def test_no_dashboard_skill_at_all_points_at_the_feature_flag(self):
        """The other failure wearing the same missing skill: neither dashboard skill was
        activated, so the flag that registers both is the thing to look at."""
        client = MagicMock()
        client.send_message.return_value = _chat_result(
            tool_calls=[_tool_call("set_skills", {"skills_to_activate": ["search"]})],
        )
        with pytest.raises(DashboardSkillAssertionError) as excinfo:
            _evaluate_with(client, _DE01_EXPECTED)
        message = str(excinfo.value)
        assert "dashboard_editor or dashboard_builder" in message
        assert "one feature flag registers both" in message

    def test_a_passing_run_returns_the_outcome(self):
        part = _dashboard_part(
            [_widget("Total Customers", _TOTAL_CUSTOMERS), _widget("Active Customers", _ACTIVE_CUSTOMERS)],
            date_filter=_THIS_YEAR_FILTER,
        )
        client = MagicMock()
        client.send_message.return_value = _chat_result(
            tool_calls=[
                _tool_call("set_skills", {"skills_to_activate": ["dashboard_builder"]}),
                _tool_call("draft_dashboard", _draft_result()),
            ],
            parts=[part],
        )
        outcome = _evaluate_with(client, _DC05_EXPECTED)
        assert outcome.runs_passed == 1
        assert outcome.runs_effective == 1
        assert outcome.detail["charts_matched"] is True


def _as_events(raw: list[dict]) -> list[ToolCallEvent]:
    return [ToolCallEvent.model_validate(e) for e in raw]


def _run_with(client, expected_output, *, max_iterations=7, initial_conversation_id="conv-1"):
    """``max_iterations=None`` exercises the module default rather than overriding it."""
    kwargs = {} if max_iterations is None else {"max_iterations": max_iterations}
    with patch("gooddata_eval.core.agentic.dashboard_skill.ChatClient", return_value=client):
        return run_agentic_dashboard_skill(
            host="https://example.invalid",
            token="token",
            workspace_id="ws",
            question="Could you create a dashboard?",
            expected_output=expected_output,
            initial_conversation_id=initial_conversation_id,
            **kwargs,
        )


def _evaluate_with(client, expected_output):
    with patch("gooddata_eval.core.agentic.dashboard_skill.ChatClient", return_value=client):
        return evaluate_agentic_dashboard_skill(
            host="https://example.invalid",
            token="token",
            workspace_id="ws",
            question="Could you create a dashboard?",
            expected_output=expected_output,
            initial_conversation_id="conv-1",
        )
