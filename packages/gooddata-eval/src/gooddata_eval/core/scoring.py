# (C) 2026 GoodData Corporation
"""Visualization scoring — ported from gdc-nas tavern-e2e app/vis_assertions/metrics.py."""

import json
from dataclasses import dataclass

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


@dataclass
class FilterScores:
    date_ok: bool
    ranking_ok: bool
    attribute_ok: bool

    @property
    def all_ok(self) -> bool:
        return self.date_ok and self.ranking_ok and self.attribute_ok


def _resolve_alias_to_uri(alias: str, fields: dict[str, AacQueryField | str]) -> str:
    """Resolve a field alias to its `using` URI; return the alias unchanged if absent."""
    field = fields.get(alias)
    if field is None:
        return alias
    if isinstance(field, str):
        return field
    # Duck-type: works even when field is from a different module's AacQueryField class
    return field.using


def _resolve_bucket_to_uri_set(bucket: list[AacBucketRef | str], fields: dict[str, AacQueryField | str]) -> set[str]:
    uris: set[str] = set()
    for ref in bucket:
        alias = ref.field if isinstance(ref, AacBucketRef) else ref
        uris.add(_resolve_alias_to_uri(alias, fields))
    return uris


def get_metric_uri_set(viz: CreatedVisualization) -> set[str]:
    return _resolve_bucket_to_uri_set(viz.metrics, viz.query.fields)


def get_dimension_uri_set(viz: CreatedVisualization) -> set[str]:
    all_dim_buckets = viz.view_by + viz.segment_by + viz.rows + viz.columns
    return _resolve_bucket_to_uri_set(all_dim_buckets, viz.query.fields)


def uri_to_display_name(uri: str) -> str:
    """Convert 'metric/net_sales' -> 'net sales', 'label/date.month' -> 'date - month'."""
    last = uri.split("/", 1)[-1]
    return last.replace(".", " - ").replace("_", " ")


def validate_cross_references(viz: CreatedVisualization) -> tuple[bool, list[str]]:
    """Validate ranking-filter `using`/`attribute` resolve to correct URI prefixes."""
    errors: list[str] = []
    fields = viz.query.fields
    for filter_key, filter_dict in viz.query.filter_by.items():
        if filter_dict.get("type") != "ranking_filter":
            continue
        using_val = filter_dict.get("using", "")
        using_uri = _resolve_alias_to_uri(using_val, fields)
        field_def = fields.get(using_val)
        is_adhoc_agg = isinstance(field_def, AacQueryField) and bool(field_def.aggregation)
        if not using_uri.startswith(("metric/", "fact/")) and not is_adhoc_agg:
            errors.append(
                f"ranking filter '{filter_key}': using='{using_val}' "
                f"resolves to '{using_uri}' — expected a metric/ or fact/ URI"
            )
        if "attribute" in filter_dict:
            attr_val = filter_dict["attribute"]
            attr_uri = _resolve_alias_to_uri(attr_val, fields)
            if not attr_uri.startswith(("label/", "attribute/")):
                errors.append(
                    f"ranking filter '{filter_key}': attribute='{attr_val}' "
                    f"resolves to '{attr_uri}' — expected a label/ or attribute/ URI"
                )
    return len(errors) == 0, errors


def _normalize_date_filter(filter_dict: dict, _fields: dict) -> dict:
    return {
        "type": "date_filter",
        "dataset_uri": filter_dict.get("using", ""),
        "from": filter_dict.get("from"),
        "to": filter_dict.get("to"),
        "granularity": filter_dict.get("granularity"),
    }


def _normalize_ranking_filter(filter_dict: dict, fields: dict[str, AacQueryField | str]) -> dict:
    entry: dict = {
        "type": "ranking_filter",
        "metric_uri": _resolve_alias_to_uri(filter_dict.get("using", ""), fields),
        "dim_uri": _resolve_alias_to_uri(filter_dict.get("attribute", ""), fields),
    }
    if "top" in filter_dict:
        entry["top"] = filter_dict["top"]
    if "bottom" in filter_dict:
        entry["bottom"] = filter_dict["bottom"]
    return entry


def _normalize_attribute_filter(filter_dict: dict, _fields: dict) -> dict:
    raw_state = filter_dict.get("state") or {}
    state = {k: v for k, v in raw_state.items() if v}
    return {
        "type": "attribute_filter",
        "field_uri": filter_dict.get("using", ""),
        "state": state,
    }


def _split_and_normalize_filters(viz: CreatedVisualization) -> tuple[set[str], set[str], set[str]]:
    date_set: set[str] = set()
    ranking_set: set[str] = set()
    attr_set: set[str] = set()
    fields = viz.query.fields
    for filter_dict in viz.query.filter_by.values():
        ft = filter_dict.get("type")
        if ft == "date_filter":
            date_set.add(json.dumps(_normalize_date_filter(filter_dict, fields), sort_keys=True))
        elif ft == "ranking_filter":
            ranking_set.add(json.dumps(_normalize_ranking_filter(filter_dict, fields), sort_keys=True))
        elif ft == "attribute_filter":
            attr_set.add(json.dumps(_normalize_attribute_filter(filter_dict, fields), sort_keys=True))
    return date_set, ranking_set, attr_set


def check_filters(expected: CreatedVisualization, actual: CreatedVisualization) -> FilterScores:
    exp_date, exp_rank, exp_attr = _split_and_normalize_filters(expected)
    act_date, act_rank, act_attr = _split_and_normalize_filters(actual)
    return FilterScores(
        date_ok=act_date == exp_date,
        ranking_ok=act_rank == exp_rank,
        attribute_ok=act_attr == exp_attr,
    )


def _normalize_viz_type(raw_type: str) -> str:
    return _AAC_TYPE_MAP.get(raw_type, raw_type.replace("_chart", "").upper())


def check_viz_type(expected: CreatedVisualization, actual: CreatedVisualization) -> bool:
    if not expected.type:
        return True
    return _normalize_viz_type(expected.type) == _normalize_viz_type(actual.type)
