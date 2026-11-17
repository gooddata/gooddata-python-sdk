# (C) 2026 GoodData Corporation
"""Visualization scoring — ported from gdc-nas tavern-e2e app/vis_assertions/metrics.py."""

import calendar
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta

from gooddata_eval.core.granularity import canonical_date_uri
from gooddata_eval.core.models import AacBucketRef, AacQueryField, CreatedVisualization

# Maps dataset chart-type names (and agent enum values) to a canonical token.
_AAC_TYPE_MAP = {
    "line_chart": "LINE",
    "bar_chart": "BAR",
    "column_chart": "COLUMN",
    "pie_chart": "PIE",
    "table": "TABLE",
    "headline": "HEADLINE",
}


# Every `type` the AAC visualization schema defines. An expectation naming anything else is a typo.
AAC_VISUALIZATION_TYPES = frozenset(
    {
        "table",
        "headline_chart",
        "bar_chart",
        "column_chart",
        "line_chart",
        "area_chart",
        "pie_chart",
        "donut_chart",
        "scatter_chart",
        "bubble_chart",
        "treemap_chart",
        "pyramid_chart",
        "funnel_chart",
        "heatmap_chart",
        "bullet_chart",
        "waterfall_chart",
        "dependency_wheel_chart",
        "sankey_chart",
        "geo_chart",
        "geo_area_chart",
        "repeater_chart",
        "radar_chart",
        "combo_chart",
    }
)


@dataclass
class FilterScores:
    date_ok: bool
    ranking_ok: bool
    attribute_ok: bool

    @property
    def all_ok(self) -> bool:
        return self.date_ok and self.ranking_ok and self.attribute_ok


def resolve_alias_to_uri(alias: str, fields: Mapping[str, AacQueryField | str | dict]) -> str:
    """Resolve a field alias to its `using` URI; return the alias unchanged if absent.

    A field may be an `AacQueryField`, a bare uri string, or the raw `{"using": uri}`
    dict the AAC schema also allows -- generated specs carry the dict form before they
    are ever validated into a model.
    """
    field = fields.get(alias)
    if field is None:
        return alias
    if isinstance(field, str):
        return field
    if isinstance(field, dict):
        return field["using"]
    # Duck-type: works even when field is from a different module's AacQueryField class
    return field.using


BucketItem = AacBucketRef | str


def _ref_uri(ref: BucketItem, fields: Mapping[str, AacQueryField | str]) -> str:
    alias = ref.field if isinstance(ref, AacBucketRef) else ref
    return canonical_date_uri(resolve_alias_to_uri(alias, fields))


def _resolve_bucket_to_uri_set(
    bucket: list[BucketItem] | list[BucketItem | None], fields: dict[str, AacQueryField | str]
) -> set[str]:
    return {_ref_uri(ref, fields) for ref in bucket if ref is not None}


def _is_measure(ref: BucketItem, fields: dict[str, AacQueryField | str]) -> bool:
    """Whether a bucket item names a metric, a fact, or a field the chart aggregates itself."""
    alias = ref.field if isinstance(ref, AacBucketRef) else ref
    field = fields.get(alias)
    if isinstance(field, AacQueryField) and field.aggregation:
        return True
    return resolve_alias_to_uri(alias, fields).startswith(("metric/", "fact/"))


def _column_split(viz: CreatedVisualization) -> tuple[list[BucketItem], list[BucketItem]]:
    """`columns` split into its measures and its attributes.

    A table's `columns` holds attributes only. A repeater writes its metrics there too, as
    `{field, display_as}` entries next to a clone of its row attribute, and the same chart
    comes back with the metrics under `metrics` on another run. Splitting by what each item
    names scores both spellings alike.
    """
    measures = [ref for ref in viz.columns if _is_measure(ref, viz.query.fields)]
    attributes = [ref for ref in viz.columns if not _is_measure(ref, viz.query.fields)]
    return measures, attributes


def get_metric_uri_set(viz: CreatedVisualization) -> set[str]:
    measures_in_columns, _ = _column_split(viz)
    return _resolve_bucket_to_uri_set(viz.metrics + viz.size_by + measures_in_columns, viz.query.fields)


def get_dimension_uri_set(viz: CreatedVisualization) -> set[str]:
    _, attributes_in_columns = _column_split(viz)
    ends = [ref for ref in (viz.from_, viz.to) if ref is not None]
    all_dim_buckets = viz.view_by + viz.segment_by + viz.rows + attributes_in_columns + ends
    return _resolve_bucket_to_uri_set(all_dim_buckets, viz.query.fields)


def bucket_layout(viz: CreatedVisualization) -> dict[str, list[str]]:
    """Each bucket's fields, as uris, for comparing bucket by bucket.

    Sorted lists rather than sets so the layout reads in a report. An attribute in `columns`
    that already sits in `rows` or `view_by` is left out: the repeater adds that clone of
    its row attribute on its own, so it says nothing about where the agent put the field.
    """
    fields = viz.query.fields
    _, attributes_in_columns = _column_split(viz)
    placed = _resolve_bucket_to_uri_set(viz.rows + viz.view_by, fields)
    columns = _resolve_bucket_to_uri_set(attributes_in_columns, fields) - placed
    return {
        "view_by": sorted(_resolve_bucket_to_uri_set(viz.view_by, fields)),
        "segment_by": sorted(_resolve_bucket_to_uri_set(viz.segment_by, fields)),
        "rows": sorted(_resolve_bucket_to_uri_set(viz.rows, fields)),
        "columns": sorted(columns),
        "size_by": sorted(_resolve_bucket_to_uri_set(viz.size_by, fields)),
        "from": [_ref_uri(viz.from_, fields)] if viz.from_ is not None else [],
        "to": [_ref_uri(viz.to, fields)] if viz.to is not None else [],
    }


def check_buckets(expected: CreatedVisualization, actual: CreatedVisualization) -> bool | None:
    """Whether every field sits in the bucket the expectation puts it in; None when not asked.

    The dimension check compares the union of the buckets, so a heatmap with its rows and
    columns swapped, a treemap segment moved into `view_by`, or a sankey with source and
    destination reversed would all pass it.
    """
    if not expected.buckets_strict:
        return None
    return bucket_layout(actual) == bucket_layout(expected)


def ordered_metric_uris(viz: CreatedVisualization) -> list[str | None]:
    """The chart's `metrics` in order, a null entry kept as None."""
    return [None if ref is None else _ref_uri(ref, viz.query.fields) for ref in viz.metrics]


_PRIMARY_AXIS = "primary"


def metric_axes(viz: CreatedVisualization) -> dict[str, str]:
    """The axis each metric of a combo chart is drawn on, by metric uri."""
    axes: dict[str, str] = {}
    for ref in viz.metrics:
        if isinstance(ref, AacBucketRef):
            axis = (ref.model_extra or {}).get("axis")
            if isinstance(axis, str):
                axes[_ref_uri(ref, viz.query.fields)] = axis
    return axes


def check_metric_layout(expected: CreatedVisualization, actual: CreatedVisualization) -> list[str]:
    """What is wrong with the order and the axes of the metrics, when the expectation states them.

    Order is checked under `metrics_ordered`: a bullet chart reads actual, target and
    comparative by position, and a bubble chart x and y. An axis is checked for every
    expected metric entry that names one. An actual metric that names no axis, written as a
    plain alias or as an entry without `axis`, is drawn on the primary axis.
    """
    problems: list[str] = []
    if expected.metrics_ordered and ordered_metric_uris(actual) != ordered_metric_uris(expected):
        problems.append(f"metric order {ordered_metric_uris(actual)}, expected {ordered_metric_uris(expected)}")
    expected_axes = metric_axes(expected)
    if expected_axes:
        present = set(ordered_metric_uris(actual))
        actual_axes = {uri: _PRIMARY_AXIS for uri in present if uri is not None} | metric_axes(actual)
        wrong = {uri: actual_axes.get(uri) for uri, axis in expected_axes.items() if actual_axes.get(uri) != axis}
        if wrong:
            problems.append(f"metric axes {wrong}, expected {expected_axes}")
    return problems


def uri_to_display_name(uri: str) -> str:
    """Convert 'metric/net_sales' -> 'net sales', 'label/date.month' -> 'date - month'."""
    last = uri.split("/", 1)[-1]
    return last.replace(".", " - ").replace("_", " ")


def validate_cross_references(viz: CreatedVisualization) -> tuple[bool, list[str]]:
    """Validate ranking-filter `using`/`attribute` resolve to correct URI prefixes.

    Always returns `(ok, errors)` — a malformed filter produces an error entry, never an
    exception. Anything unusable (None, empty, non-string) used to reach `.startswith()`
    or `dict.get()` and blow up with AttributeError/TypeError mid-evaluation.

    `using` is required by the AAC schema, `attribute` is optional (see
    `_normalize_ranking_filter`), so an absent/None/empty `attribute` is accepted silently.
    """
    errors: list[str] = []
    fields = viz.query.fields
    for filter_key, filter_dict in viz.query.filter_by.items():
        if filter_dict.get("type") != "ranking_filter":
            continue
        using_val = filter_dict.get("using")
        if not isinstance(using_val, str) or not using_val:
            errors.append(f"ranking filter '{filter_key}': using={using_val!r} — a metric/ or fact/ URI is required")
        else:
            using_uri = resolve_alias_to_uri(using_val, fields)
            field_def = fields.get(using_val)
            is_adhoc_agg = isinstance(field_def, AacQueryField) and bool(field_def.aggregation)
            if not using_uri.startswith(("metric/", "fact/")) and not is_adhoc_agg:
                errors.append(
                    f"ranking filter '{filter_key}': using='{using_val}' "
                    f"resolves to '{using_uri}' — expected a metric/ or fact/ URI"
                )
        attr_val = filter_dict.get("attribute")
        if attr_val is None or attr_val == "":
            continue
        if not isinstance(attr_val, str):
            errors.append(
                f"ranking filter '{filter_key}': attribute={attr_val!r} — expected a label/ or attribute/ URI"
            )
            continue
        attr_uri = resolve_alias_to_uri(attr_val, fields)
        if not attr_uri.startswith(("label/", "attribute/")):
            errors.append(
                f"ranking filter '{filter_key}': attribute='{attr_val}' "
                f"resolves to '{attr_uri}' — expected a label/ or attribute/ URI"
            )
    return len(errors) == 0, errors


def _normalize_sort(sort: dict, fields: Mapping[str, AacQueryField | str | dict]) -> str:
    """One sort entry as a comparable string, aliases resolved to uris.

    The entry's own `type` decides which key names the fields: a `metric_sort` lists
    them under `metrics`, an `attribute_sort` names one under `by`. One agent build
    emits both keys on a metric sort, so reading `by` first would compare the wrong
    thing on a chart that is otherwise right.
    """
    if sort.get("type") == "attribute_sort":
        refs = [sort.get("by")]
    else:
        refs = list(sort.get("metrics") or [])
        if not refs and sort.get("by") is not None:
            refs = [sort["by"]]
    uris = [canonical_date_uri(resolve_alias_to_uri(ref, fields)) for ref in refs if isinstance(ref, str)]
    return json.dumps(
        {
            "type": sort.get("type") or "",
            "direction": (sort.get("direction") or "").upper(),
            "fields": uris,
        },
        sort_keys=True,
    )


def normalized_sorts(viz: CreatedVisualization) -> list[str]:
    """`query.sort_by` in the canonical form equality is tested on.

    Order is preserved: a chart sorted by region then by revenue is not the chart
    sorted by revenue then by region.
    """
    return [_normalize_sort(sort, viz.query.fields) for sort in viz.query.sort_by]


def check_sorts(expected: CreatedVisualization, actual: CreatedVisualization) -> bool:
    """Whether `actual` sorts the way `expected` does, when `expected` sorts at all.

    Deliberately not symmetric with the filter checks. An empty `sort_by` says the
    fixture records no sort, not that the chart must be unsorted -- a generated item
    inherits that emptiness from an insight whose author sorted in Analytical Designer
    and saved without the sort sticking. A spurious filter changes which rows a reader
    sees and is always wrong; a volunteered sort changes only their order, and on a time
    axis ascending is the order any renderer would pick unprompted.

    So a required sort is enforced and a volunteered one is free. The same holds when
    the fixture does sort: the recorded sorts must come first and in order, and a
    tiebreak the agent appends after them ("state descending, then city") is free too.
    The cost is that a genuinely wrong sort over an unsorted fixture goes ungraded, which
    is the lesser error while `sort_by: []` cannot distinguish "unsorted" from
    "unrecorded".
    """
    expected_sorts = normalized_sorts(expected)
    return normalized_sorts(actual)[: len(expected_sorts)] == expected_sorts


def _shift_month(anchor: date, offset: int) -> tuple[date, date]:
    """First and last day of the calendar month ``offset`` months from ``anchor``."""
    total = anchor.year * 12 + (anchor.month - 1) + offset
    year, month = divmod(total, 12)
    return date(year, month + 1, 1), date(year, month + 1, calendar.monthrange(year, month + 1)[1])


def _absolute_span(granularity: str, start_offset: int, end_offset: int, today: date) -> tuple[date, date] | None:
    """Resolve a relative date filter to the inclusive absolute span it denotes.

    Returns None for granularities this cannot resolve unambiguously -- notably a bare
    ``WEEK``, which is not in the AAC granularity enum and states no start-of-week
    convention. ``WEEK_US`` *is* well defined (Sunday-start), so it resolves.
    Guessing the bare case would trade a false negative for a false positive.

    An offset far enough out to leave the representable date range resolves to None
    rather than raising: every granularity here can be pushed past it (a YEAR offset of
    ``-today.year`` alone lands on year 0), and letting that escape would abort scoring
    for the whole item over one malformed filter. None puts the filter back on the
    literal-comparison path, which is what an unresolvable span already does.
    """
    gran = granularity.upper()
    try:
        if gran == "DAY":
            return today + timedelta(days=start_offset), today + timedelta(days=end_offset)
        if gran == "WEEK_US":
            sunday = today - timedelta(days=(today.weekday() + 1) % 7)
            return sunday + timedelta(weeks=start_offset), sunday + timedelta(weeks=end_offset, days=6)
        if gran == "MONTH":
            return _shift_month(today, start_offset)[0], _shift_month(today, end_offset)[1]
        if gran == "QUARTER":
            q_start_month = (today.month - 1) // 3 * 3 + 1
            anchor = date(today.year, q_start_month, 1)
            return _shift_month(anchor, start_offset * 3)[0], _shift_month(anchor, end_offset * 3 + 2)[1]
        if gran == "YEAR":
            return date(today.year + start_offset, 1, 1), date(today.year + end_offset, 12, 31)
    except (ValueError, OverflowError):
        return None
    return None


def _as_date(value: object) -> date | None:
    if isinstance(value, str):
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def _normalize_date_filter(filter_dict: dict, _fields: dict, today: date | None = None) -> dict:
    """Canonicalize a date filter, resolving relative offsets to an absolute span.

    The agent may answer "last month" either relatively (``granularity: MONTH,
    from: -1, to: -1``) or absolutely (``from: 2026-08-01, to: 2026-08-31``).
    Compared literally these never match, so a correct answer in the encoding the
    fixture did not happen to use was scored as a wrong date period. Both forms
    collapse to the same absolute span here.

    Resolution is relative to today, which is the same "today" the agent resolved
    against -- scoring runs in the same process as the turn. Re-scoring an archived
    result at a later date would therefore drift; nothing currently does that.
    """
    raw_from, raw_to = filter_dict.get("from"), filter_dict.get("to")
    granularity = filter_dict.get("granularity")
    span: tuple[date, date] | None = None

    if isinstance(raw_from, int) and isinstance(raw_to, int) and isinstance(granularity, str):
        span = _absolute_span(granularity, raw_from, raw_to, today or date.today())
    else:
        start, end = _as_date(raw_from), _as_date(raw_to)
        if start and end:
            span = (start, end)

    if span is not None:
        return {
            "type": "date_filter",
            "dataset_uri": filter_dict.get("using", ""),
            "from": span[0].isoformat(),
            "to": span[1].isoformat(),
        }
    # Unresolvable (e.g. the WEEK family): fall back to literal comparison.
    return {
        "type": "date_filter",
        "dataset_uri": filter_dict.get("using", ""),
        "from": raw_from,
        "to": raw_to,
        "granularity": granularity,
    }


def _sole_dimension_uri(viz: CreatedVisualization) -> str | None:
    """URI of the visualization's only dimension, or None when it has zero or several."""
    dim_uris = get_dimension_uri_set(viz)
    return next(iter(dim_uris)) if len(dim_uris) == 1 else None


def _normalize_ranking_filter(
    filter_dict: dict,
    fields: dict[str, AacQueryField | str],
    sole_dim_uri: str | None = None,
) -> dict:
    """Canonicalize a ranking filter so equivalent filters compare equal.

    `attribute` is optional in the AAC schema (gen-ai models it as `NotRequired[str]` /
    `str | None`), and when it is omitted AFM ranks over every dimension of the result. For a
    single-dimension visualization that is exactly "rank by that one dimension", so an omitted
    attribute is filled in with `sole_dim_uri` instead of comparing as an empty string — the
    agent and the dataset may legitimately express the same filter either way.

    The substitution is deliberately gated on there being exactly ONE dimension: with two or
    more, omitting `attribute` ranks over the dimension *tuple*, which is a different filter,
    so those stay strict. Callers pass the sole dimension of the visualization the filter
    belongs to, which makes the comparison symmetric — it does not matter which side omitted it.

    Missing, None and "" are all treated as "not specified"; so is a non-string, which
    `validate_cross_references` reports separately rather than crashing the comparison.
    """
    attr_val = filter_dict.get("attribute")
    if not isinstance(attr_val, str) or not attr_val:
        dim_uri = sole_dim_uri or ""
    else:
        dim_uri = resolve_alias_to_uri(attr_val, fields)
    using_val = filter_dict.get("using")
    entry: dict = {
        "type": "ranking_filter",
        "metric_uri": resolve_alias_to_uri(using_val, fields) if isinstance(using_val, str) else "",
        "dim_uri": dim_uri,
    }
    if "top" in filter_dict:
        entry["top"] = filter_dict["top"]
    if "bottom" in filter_dict:
        entry["bottom"] = filter_dict["bottom"]
    return entry


def _normalize_attribute_filter(filter_dict: dict, _fields: dict) -> dict:
    raw_state = filter_dict.get("state") or {}
    # Sort the element lists: `include`/`exclude` name a SET of elements, but the caller
    # serialises this dict with json.dumps(..., sort_keys=True), which orders the dict
    # KEYS and leaves the lists alone. Without this, the same filter written in a
    # different order compares unequal, and an agent has no reason to keep that order
    # stable between runs -- so a question needing a multi-element filter passed or
    # failed partly at random, reported as `filters_correct: false` and indistinguishable
    # from the agent genuinely filtering wrongly.
    #
    # The key is the element's own canonical JSON, not a bare sort and not str(): a bare
    # sort raises TypeError on a mixed-type list (["A", 2]), and a crash inside scoring is
    # worse than the mismatch this fixes -- while str() collapses 1 and "1" to the same
    # key, so the stable sort leaves THEIR order as it found it and the ordering bug
    # survives for exactly that pair. These values are always parsed JSON, so json.dumps
    # cannot fail on them and it distinguishes types the way the comparison downstream does.
    state = {
        k: (sorted(v, key=lambda element: json.dumps(element, sort_keys=True)) if isinstance(v, list) else v)
        for k, v in raw_state.items()
        if v
    }
    return {
        "type": "attribute_filter",
        "field_uri": filter_dict.get("using", ""),
        "state": state,
    }


def _split_and_normalize_filters(
    viz: CreatedVisualization, today: date | None = None
) -> tuple[set[str], set[str], set[str]]:
    date_set: set[str] = set()
    ranking_set: set[str] = set()
    attr_set: set[str] = set()
    fields = viz.query.fields
    sole_dim_uri = _sole_dimension_uri(viz)
    for filter_dict in viz.query.filter_by.values():
        ft = filter_dict.get("type")
        if ft == "date_filter":
            date_set.add(json.dumps(_normalize_date_filter(filter_dict, fields, today), sort_keys=True))
        elif ft == "ranking_filter":
            ranking_set.add(json.dumps(_normalize_ranking_filter(filter_dict, fields, sole_dim_uri), sort_keys=True))
        elif ft == "attribute_filter":
            attr_set.add(json.dumps(_normalize_attribute_filter(filter_dict, fields), sort_keys=True))
    return date_set, ranking_set, attr_set


def normalized_filters(viz: CreatedVisualization, today: date | None = None) -> dict[str, list[str]]:
    """A visualization's filters exactly as `check_filters` compares them.

    Grouped by the three categories it scores separately and sorted for stable output.
    Each entry is the canonical JSON string equality is tested on, so reporting the
    expected and actual side by side shows precisely why a category did not match —
    a `filter_date_score` of False otherwise gives no clue whether the period differed,
    the granularity did, or the dataset the filter hangs off did.
    """
    date_set, ranking_set, attr_set = _split_and_normalize_filters(viz, today)
    return {"date": sorted(date_set), "ranking": sorted(ranking_set), "attribute": sorted(attr_set)}


def check_filters(
    expected: CreatedVisualization, actual: CreatedVisualization, today: date | None = None
) -> FilterScores:
    # One anchor for both sides: resolving each against its own date.today() would
    # score inconsistently for a run that straddles midnight.
    today = today or date.today()
    exp_date, exp_rank, exp_attr = _split_and_normalize_filters(expected, today)
    act_date, act_rank, act_attr = _split_and_normalize_filters(actual, today)
    return FilterScores(
        date_ok=act_date == exp_date,
        ranking_ok=act_rank == exp_rank,
        attribute_ok=act_attr == exp_attr,
    )


def _normalize_viz_type(raw_type: str) -> str:
    return _AAC_TYPE_MAP.get(raw_type, raw_type.replace("_chart", "").upper())


def same_viz_type(expected: str, actual: str) -> bool:
    """Whether two chart-type names denote the same type, spelled either way."""
    return _normalize_viz_type(expected) == _normalize_viz_type(actual)


def check_viz_type(expected: CreatedVisualization, actual: CreatedVisualization) -> bool:
    if not expected.type:
        return True
    return _normalize_viz_type(expected.type) == _normalize_viz_type(actual.type)
