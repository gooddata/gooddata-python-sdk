# (C) 2026 GoodData Corporation. All rights reserved.
"""The takeaway request the Publisher editor sends for an unwritten takeaway of a v2 document.

Every visualization on the page, in layout order, each under the filters it is drawn with, a
visualization drawn twice the same way sent once; ``filterContext`` empty; the takeaway's and the
document's instructions. A visualization is drawn with the period on its own date dataset unless it
ignores the period, a document date filter on that dataset with both ends set in the period's place
(keeping its ``emptyValueHandling`` and, for a relative one, its ``boundedFilter``),
and every document attribute and text filter that narrows the data. An attribute filter excluding
nothing and a text filter with no value narrow nothing and are left out; measure value filters
and any other kind are left out too, since the renderer draws no chart differently for them. Widget
and page filters, and ``ignoreDocumentFilters``, are stored but not applied, so they are not applied
here either.

Two parts of the editor's request are left out: ``maxCharacters``, which the editor derives from the
layout geometry and the theme, so the endpoint's default length applies; and resolving text variables
in the instructions, which are sent as written, as the editor does while it has no values for them.

Mirrors gdc-ui at commit 7e0f3719ca2 (``documentTakeawayRequest`` and ``copilotTakeaways`` of the
publisher's v2 editor); check them again when the editor's request changes.

Pure: no network.
"""

from __future__ import annotations

import json
from typing import Any

from gooddata_eval.core.models import TakeawayInput, TakeawayInstructions, TakeawayVisualization

# Publisher periods and dashboard date filters name granularities as GDC.time.*; AFM date filters
# take the platform enum.
_AFM_GRANULARITY = {
    "GDC.time.year": "YEAR",
    "GDC.time.quarter": "QUARTER",
    "GDC.time.month": "MONTH",
    "GDC.time.week_us": "WEEK",
    "GDC.time.week": "WEEK",
    "GDC.time.date": "DAY",
    "GDC.time.hour": "HOUR",
    "GDC.time.minute": "MINUTE",
    "GDC.time.second": "SECOND",
    "GDC.time.quarter_in_year": "QUARTER_OF_YEAR",
    "GDC.time.month_in_year": "MONTH_OF_YEAR",
    "GDC.time.week_in_year": "WEEK_OF_YEAR",
    "GDC.time.day_in_year": "DAY_OF_YEAR",
    "GDC.time.day_in_month": "DAY_OF_MONTH",
    "GDC.time.day_in_week": "DAY_OF_WEEK",
    "GDC.time.hour_in_day": "HOUR_OF_DAY",
    "GDC.time.minute_in_hour": "MINUTE_OF_HOUR",
    "GDC.time.minute_in_day": "MINUTE_OF_DAY",
    "GDC.time.second_in_day": "SECOND_OF_DAY",
    "GDC.time.second_in_minute": "SECOND_OF_MINUTE",
    "GDC.time.fiscal_month": "FISCAL_MONTH",
    "GDC.time.fiscal_quarter": "FISCAL_QUARTER",
    "GDC.time.fiscal_year": "FISCAL_YEAR",
}


class _Unbuildable(Exception):
    """The editor's request has a part this module cannot reproduce."""


def _identifier(reference: Any) -> str | None:
    """The id of a reference written as ``{"identifier": "..."}``, ``{"identifier": {"id": ...}}`` or a bare string."""
    if isinstance(reference, dict):
        reference = reference.get("identifier")
        if isinstance(reference, dict):
            reference = reference.get("id")
    return reference if isinstance(reference, str) else None


def _date_filter(
    dataset: str, kind: Any, granularity: Any, start: Any, end: Any, options: dict[str, Any] | None = None
) -> dict:
    """The AFM date filter; ``options`` are the document filter's ``emptyValueHandling`` and ``boundedFilter``."""
    dataset_ref = {"identifier": {"id": dataset, "type": "dataset"}}
    options = options or {}
    if kind == "absolute":
        return {
            "absoluteDateFilter": {
                "dataset": dataset_ref,
                "from": start,
                "to": end,
                **{key: value for key, value in options.items() if key == "emptyValueHandling"},
            }
        }
    if kind == "relative":
        afm_granularity = _AFM_GRANULARITY.get(granularity) if isinstance(granularity, str) else None
        if afm_granularity is None:
            raise _Unbuildable(f"relative date granularity {granularity!r} has no AFM form")
        return {
            "relativeDateFilter": {
                "dataset": dataset_ref,
                "granularity": afm_granularity,
                "from": start,
                "to": end,
                **options,
            }
        }
    raise _Unbuildable(f"date filter type {kind!r} has no AFM form")


def _narrows_the_date(date_filter: dict) -> bool:
    return date_filter.get("from") is not None and date_filter.get("to") is not None


def _date_filters(widget: dict, period: Any, filters: list[Any]) -> list[dict]:
    dataset = _identifier(widget.get("dateDataSet"))
    if dataset is None:
        return []
    for item in filters:
        date_filter = item.get("dateFilter") if isinstance(item, dict) else None
        if (
            isinstance(date_filter, dict)
            and _narrows_the_date(date_filter)
            and _identifier(date_filter.get("dataSet")) == dataset
        ):
            return [
                _date_filter(
                    dataset,
                    date_filter.get("type"),
                    date_filter.get("granularity"),
                    date_filter.get("from"),
                    date_filter.get("to"),
                    {
                        key: date_filter[key]
                        for key in ("emptyValueHandling", "boundedFilter")
                        if date_filter.get(key) is not None
                    },
                )
            ]
    if not isinstance(period, dict) or widget.get("ignoreDocumentPeriod") is True:
        return []
    return [_date_filter(dataset, period.get("type"), period.get("granularity"), period.get("from"), period.get("to"))]


_MATCH_TYPES = {"contains": "CONTAINS", "startsWith": "STARTS_WITH", "endsWith": "ENDS_WITH"}


def _label_ref(body: dict) -> dict:
    label = _identifier(body.get("displayForm"))
    if label is None:
        raise _Unbuildable(f"filter {body!r} names no label, so it has no AFM form")
    return {"identifier": {"id": label, "type": "label"}}


def _element_filter(label_ref: dict, values: list[Any], negative: bool) -> dict | None:
    """Selected elements as AFM; None for an exclusion of nothing, which keeps every row."""
    if negative:
        return {"negativeAttributeFilter": {"label": label_ref, "notIn": {"values": values}}} if values else None
    return {"positiveAttributeFilter": {"label": label_ref, "in": {"values": values}}}


def _attribute_filter(body: dict) -> dict | None:
    elements = body.get("attributeElements")
    elements = elements if isinstance(elements, dict) else {}
    values = elements.get("uris") or elements.get("values") or []
    if not isinstance(values, list):
        raise _Unbuildable(f"attribute filter {body!r} has no element list, so it has no AFM form")
    negative = body.get("negativeSelection") is True
    if not values and not negative:
        raise _Unbuildable(f"attribute filter {body!r} selects no element, which has no AFM form")
    return _element_filter(_label_ref(body), values, negative)


def _arbitrary_attribute_filter(body: dict) -> dict | None:
    values = body.get("values")
    if not isinstance(values, list):
        raise _Unbuildable(f"text filter {body!r} has no value list, so it has no AFM form")
    negative = body.get("negativeSelection") is True
    # Tiger drops a text filter without values, so the editor's request carries none.
    return _element_filter(_label_ref(body), values, negative) if values else None


def _match_attribute_filter(body: dict) -> dict:
    operator = body.get("operator")
    match_type = _MATCH_TYPES.get(operator) if isinstance(operator, str) else None
    literal = body.get("literal")
    if match_type is None or not isinstance(literal, str):
        raise _Unbuildable(f"text filter {body!r} has no AFM form")
    return {
        "matchAttributeFilter": {
            "label": _label_ref(body),
            "literal": literal,
            "matchType": match_type,
            "caseSensitive": body.get("caseSensitive") is True,
            "negate": body.get("negativeSelection") is True,
        }
    }


_ATTRIBUTE_KINDS = {
    "attributeFilter": _attribute_filter,
    "arbitraryAttributeFilter": _arbitrary_attribute_filter,
    "matchAttributeFilter": _match_attribute_filter,
}


def _attribute_filters(filters: list[Any]) -> list[dict]:
    """The AFM form of every document filter other than a date filter that narrows the data."""
    afm: list[dict] = []
    for item in filters:
        if not isinstance(item, dict):
            raise _Unbuildable(f"document filter {item!r} is not an object")
        kind = next((kind for kind in _ATTRIBUTE_KINDS if kind in item), None)
        if kind is None:
            continue
        body = item[kind]
        if not isinstance(body, dict):
            raise _Unbuildable(f"document filter {item!r} has no AFM form")
        converted = _ATTRIBUTE_KINDS[kind](body)
        if converted is not None:
            afm.append(converted)
    return afm


def _visualization_widgets(node: Any) -> list[dict]:
    """Every visualization widget with a visualization under ``node``, in layout order."""
    if not isinstance(node, dict):
        return []
    children = node.get("children")
    if isinstance(children, list):
        return [widget for child in children for widget in _visualization_widgets(child)]
    if node.get("type") == "visualization" and _identifier(node.get("visualization")) is not None:
        return [node]
    return []


def _instruction(text: Any) -> str | None:
    written = text.strip() if isinstance(text, str) else ""
    return written or None


def _generation_instructions(holder: Any) -> Any:
    generation = holder.get("generation") if isinstance(holder, dict) else None
    return generation.get("instructions") if isinstance(generation, dict) else None


def editor_takeaway_input(document: dict, page: dict, takeaway: dict) -> TakeawayInput | str:
    """The request the editor sends to write ``takeaway`` on ``page``, or why it cannot be built.

    ``document`` is a v2 document with its content keys under ``content`` or at the top level.
    """
    content = document.get("content")
    content = content if isinstance(content, dict) else document
    filters = content.get("filters") or []
    if not isinstance(filters, list):
        return f"document filters {filters!r} are not a list"
    try:
        attribute_filters = _attribute_filters(filters)
        placements: dict[str, TakeawayVisualization] = {}
        for widget in _visualization_widgets(page.get("layout")):
            placement = TakeawayVisualization(
                visualization_id=_identifier(widget.get("visualization")) or "",
                filters=[*_date_filters(widget, document.get("period"), filters), *attribute_filters],
            )
            placements.setdefault(json.dumps(placement.model_dump(), sort_keys=True), placement)
    except _Unbuildable as exc:
        return str(exc)
    if not placements:
        return f"page {page.get('id')!r} has no visualization to summarize"
    defaults = content.get("defaults")
    takeaway_defaults = defaults.get("takeaway") if isinstance(defaults, dict) else None
    return TakeawayInput(
        visualizations=list(placements.values()),
        filter_context=[],
        instructions=TakeawayInstructions(
            slot=_instruction(_generation_instructions(takeaway)),
            document=_instruction(_generation_instructions(takeaway_defaults)),
        ),
    )
