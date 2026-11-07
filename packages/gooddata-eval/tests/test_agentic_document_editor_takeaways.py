# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from typing import Any

import pytest
from gooddata_eval.core.agentic._editor_takeaways import editor_takeaway_input
from gooddata_eval.core.models import TakeawayInput

_ABSOLUTE = {"type": "absolute", "granularity": "GDC.time.date", "from": "2026-01-01", "to": "2026-06-30"}
_RELATIVE = {"type": "relative", "granularity": "GDC.time.month", "from": -5, "to": 0}
_ORDER_DATE = {"identifier": {"id": "order_date", "type": "dataset"}}
_REGION = {"identifier": {"id": "region.name", "type": "label"}}
_TAKEAWAY = {"type": "takeaway", "id": "takeaway"}


def _chart(visualization: str, *, dataset: str | None = "order_date", **extra: Any) -> dict:
    return {
        "type": "visualization",
        "id": f"w_{visualization}",
        "visualization": {"identifier": visualization, "type": "insight"},
        **({"dateDataSet": {"identifier": dataset, "type": "dataset"}} if dataset else {}),
        **extra,
    }


def _page(*widgets: dict) -> dict:
    return {
        "id": "page2",
        "kind": "content",
        "layout": {"type": "column", "children": [{"type": "row", "children": [*widgets, _TAKEAWAY]}]},
    }


def _document(*, period: Any = _ABSOLUTE, filters: list[dict] | None = None, defaults: Any = None) -> dict:
    content: dict[str, Any] = {"pages": []}
    if filters is not None:
        content["filters"] = filters
    if defaults is not None:
        content["defaults"] = defaults
    return {"type": "document", "version": "2", "period": period, "content": content}


def _built(document: dict, page: dict, takeaway: dict = _TAKEAWAY) -> TakeawayInput:
    built = editor_takeaway_input(document, page, takeaway)
    assert isinstance(built, TakeawayInput), built
    return built


def _filters_of(built: TakeawayInput) -> list[list[dict]]:
    return [v.filters for v in built.visualizations if not isinstance(v, str)]


def _attribute_filter(values: list[str], *, negative: bool = False) -> dict:
    return {
        "attributeFilter": {
            "displayForm": _REGION,
            "negativeSelection": negative,
            "attributeElements": {"values": values},
        }
    }


def test_the_absolute_period_filters_each_chart_on_its_own_dataset() -> None:
    # given
    page = _page(_chart("revenue"), _chart("returns", dataset="return_date"))

    # when
    built = _built(_document(), page)

    # then
    assert [v.visualization_id for v in built.visualizations if not isinstance(v, str)] == ["revenue", "returns"]
    assert _filters_of(built) == [
        [{"absoluteDateFilter": {"dataset": _ORDER_DATE, "from": "2026-01-01", "to": "2026-06-30"}}],
        [
            {
                "absoluteDateFilter": {
                    "dataset": {"identifier": {"id": "return_date", "type": "dataset"}},
                    "from": "2026-01-01",
                    "to": "2026-06-30",
                }
            }
        ],
    ]
    assert built.filter_context == []
    assert built.max_characters is None
    assert built.agent_id is None


def test_a_relative_period_takes_the_afm_granularity() -> None:
    # when
    built = _built(_document(period=_RELATIVE), _page(_chart("revenue")))

    # then
    assert _filters_of(built) == [
        [{"relativeDateFilter": {"dataset": _ORDER_DATE, "granularity": "MONTH", "from": -5, "to": 0}}]
    ]


def test_a_granularity_without_an_afm_form_cannot_be_built() -> None:
    # when
    built = editor_takeaway_input(
        _document(period={**_RELATIVE, "granularity": "GDC.time.century"}), _page(_chart("revenue")), _TAKEAWAY
    )

    # then
    assert built == "relative date granularity 'GDC.time.century' has no AFM form"


@pytest.mark.parametrize(
    "chart",
    [_chart("revenue", ignoreDocumentPeriod=True), _chart("revenue", dataset=None)],
    ids=["ignores the period", "no date dataset"],
)
def test_a_chart_without_the_period_gets_no_date_filter(chart: dict) -> None:
    # when
    built = _built(_document(), _page(chart))

    # then
    assert _filters_of(built) == [[]]


def test_a_document_date_filter_on_the_charts_dataset_replaces_the_period() -> None:
    # given
    own = {
        "dateFilter": {"type": "relative", "granularity": "GDC.time.year", "from": -1, "to": -1, "dataSet": _ORDER_DATE}
    }
    other = {
        "dateFilter": {"type": "absolute", "from": "2020-01-01", "to": "2020-12-31", "dataSet": {"identifier": "x"}}
    }

    # when
    built = _built(_document(filters=[other, own]), _page(_chart("revenue", ignoreDocumentPeriod=True)))

    # then
    assert _filters_of(built) == [
        [{"relativeDateFilter": {"dataset": _ORDER_DATE, "granularity": "YEAR", "from": -1, "to": -1}}]
    ]


def test_a_document_date_filter_with_an_open_end_leaves_the_period() -> None:
    # given
    all_time = {"dateFilter": {"type": "relative", "granularity": "GDC.time.year", "dataSet": _ORDER_DATE}}

    # when
    built = _built(_document(filters=[all_time]), _page(_chart("revenue")))

    # then
    assert _filters_of(built) == [
        [{"absoluteDateFilter": {"dataset": _ORDER_DATE, "from": "2026-01-01", "to": "2026-06-30"}}]
    ]


def test_every_attribute_filter_reaches_every_chart_and_one_that_narrows_nothing_is_dropped() -> None:
    # given
    filters = [
        _attribute_filter(["West"]),
        _attribute_filter(["East"], negative=True),
        _attribute_filter([], negative=True),
    ]

    # when
    built = _built(_document(filters=filters), _page(_chart("revenue", dataset=None)))

    # then
    region = {"identifier": {"id": "region.name", "type": "label"}}
    assert _filters_of(built) == [
        [
            {"positiveAttributeFilter": {"label": region, "in": {"values": ["West"]}}},
            {"negativeAttributeFilter": {"label": region, "notIn": {"values": ["East"]}}},
        ]
    ]


def test_selected_elements_are_read_from_uris_and_then_from_values() -> None:
    # given
    by_uris = {"displayForm": _REGION, "negativeSelection": False, "attributeElements": {"uris": ["West"]}}
    by_values = {
        "displayForm": _REGION,
        "negativeSelection": True,
        "attributeElements": {"uris": [], "values": ["East"]},
    }

    # when
    built = _built(
        _document(filters=[{"attributeFilter": by_uris}, {"attributeFilter": by_values}]),
        _page(_chart("revenue", dataset=None)),
    )

    # then
    region = {"identifier": {"id": "region.name", "type": "label"}}
    assert _filters_of(built) == [
        [
            {"positiveAttributeFilter": {"label": region, "in": {"values": ["West"]}}},
            {"negativeAttributeFilter": {"label": region, "notIn": {"values": ["East"]}}},
        ]
    ]


def test_text_filters_on_whole_values_are_element_filters_and_an_empty_exclusion_is_dropped() -> None:
    # given
    filters = [
        {"arbitraryAttributeFilter": {"displayForm": _REGION, "values": ["West", None]}},
        {"arbitraryAttributeFilter": {"displayForm": _REGION, "values": ["East"], "negativeSelection": True}},
        {"arbitraryAttributeFilter": {"displayForm": _REGION, "values": [], "negativeSelection": True}},
    ]

    # when
    built = _built(_document(filters=filters), _page(_chart("revenue", dataset=None)))

    # then
    region = {"identifier": {"id": "region.name", "type": "label"}}
    assert _filters_of(built) == [
        [
            {"positiveAttributeFilter": {"label": region, "in": {"values": ["West", None]}}},
            {"negativeAttributeFilter": {"label": region, "notIn": {"values": ["East"]}}},
        ]
    ]


def test_a_text_filter_on_a_fragment_is_a_match_filter() -> None:
    # given
    match = {
        "displayForm": _REGION,
        "operator": "startsWith",
        "literal": "We",
        "caseSensitive": True,
        "negativeSelection": True,
    }

    # when
    built = _built(_document(filters=[{"matchAttributeFilter": match}]), _page(_chart("revenue", dataset=None)))

    # then
    assert _filters_of(built) == [
        [
            {
                "matchAttributeFilter": {
                    "label": {"identifier": {"id": "region.name", "type": "label"}},
                    "literal": "We",
                    "matchType": "STARTS_WITH",
                    "caseSensitive": True,
                    "negate": True,
                }
            }
        ]
    ]


def test_a_filter_kind_that_draws_no_chart_differently_is_skipped() -> None:
    # given
    measure_value = {"measureValueFilter": {"measure": {"identifier": "revenue"}, "condition": {}}}

    # when
    built = _built(_document(filters=[measure_value]), _page(_chart("revenue", dataset=None)))

    # then
    assert _filters_of(built) == [[]]


@pytest.mark.parametrize(
    "document_filter",
    [
        {"attributeFilter": {"displayForm": _REGION, "negativeSelection": False, "attributeElements": {"uris": []}}},
        {"matchAttributeFilter": {"displayForm": _REGION, "operator": "like", "literal": "We"}},
    ],
    ids=["empty selection", "unknown match operator"],
)
def test_a_document_filter_without_an_afm_form_cannot_be_built(document_filter: dict) -> None:
    # when
    built = editor_takeaway_input(_document(filters=[document_filter]), _page(_chart("revenue")), _TAKEAWAY)

    # then
    assert isinstance(built, str)
    assert "AFM form" in built


def test_the_takeaways_and_the_documents_instructions_are_sent_trimmed() -> None:
    # given
    takeaway = {**_TAKEAWAY, "generation": {"instructions": "  Focus on the West.  "}}
    defaults = {"takeaway": {"generation": {"instructions": "Write for executives."}}}

    # when
    built = _built(_document(defaults=defaults), _page(_chart("revenue")), takeaway)

    # then
    assert built.instructions.slot == "Focus on the West."
    assert built.instructions.document == "Write for executives."


def test_blank_instructions_are_left_out() -> None:
    # given
    takeaway = {**_TAKEAWAY, "generation": {"instructions": "   "}}
    defaults = {"takeaway": {"generation": {"instructions": ""}}}

    # when
    built = _built(_document(defaults=defaults), _page(_chart("revenue")), takeaway)

    # then
    assert built.instructions.slot is None
    assert built.instructions.document is None


def test_a_chart_drawn_twice_the_same_way_is_sent_once() -> None:
    # given
    page = _page(_chart("revenue"), _chart("revenue"), _chart("revenue", ignoreDocumentPeriod=True))

    # when
    built = _built(_document(), page)

    # then
    assert [len(f) for f in _filters_of(built)] == [1, 0]


def test_a_page_without_a_chart_cannot_be_built() -> None:
    # when
    built = editor_takeaway_input(_document(), _page(), _TAKEAWAY)

    # then
    assert built == "page 'page2' has no visualization to summarize"


def test_content_keys_at_the_top_level_are_read() -> None:
    # given
    document = {**_document(), "filters": [_attribute_filter(["West"])]}
    del document["content"]

    # when
    built = _built(document, _page(_chart("revenue", dataset=None)))

    # then
    assert len(_filters_of(built)[0]) == 1
