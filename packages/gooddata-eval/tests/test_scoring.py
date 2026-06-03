# (C) 2026 GoodData Corporation
from gooddata_eval.core.models import CreatedVisualization
from gooddata_eval.core.scoring import (
    check_filters,
    check_viz_type,
    get_dimension_uri_set,
    get_metric_uri_set,
    uri_to_display_name,
    validate_cross_references,
)


def _viz(**kw) -> CreatedVisualization:
    base = {"id": "v", "type": "", "query": {"fields": {}, "filter_by": {}}}
    base.update(kw)
    return CreatedVisualization.model_validate(base)


def test_metric_and_dimension_uri_sets_resolve_aliases():
    viz = _viz(
        query={
            "fields": {"m_rev": {"using": "metric/revenue"}, "d_q": {"using": "label/date.quarter"}},
            "filter_by": {},
        },
        metrics=["m_rev"],
        view_by=["d_q"],
    )
    assert get_metric_uri_set(viz) == {"metric/revenue"}
    assert get_dimension_uri_set(viz) == {"label/date.quarter"}


def test_uri_to_display_name():
    assert uri_to_display_name("metric/net_sales") == "net sales"
    assert uri_to_display_name("label/date.month") == "date - month"


def test_validate_cross_references_flags_bad_ranking_using():
    viz = _viz(
        query={
            "fields": {"d_q": {"using": "label/date.quarter"}},
            "filter_by": {"f_rank": {"type": "ranking_filter", "top": 5, "using": "d_q"}},
        }
    )
    ok, errors = validate_cross_references(viz)
    assert ok is False
    assert errors and "ranking filter" in errors[0]


def test_check_viz_type_empty_expected_is_wildcard():
    expected = _viz(type="")
    actual = _viz(type="column_chart")
    assert check_viz_type(expected, actual) is True


def test_check_viz_type_strict_match_normalizes():
    expected = _viz(type="column_chart")
    actual = _viz(type="COLUMN")
    assert check_viz_type(expected, actual) is True


def test_check_filters_exact_attribute_match():
    f = {"f_a": {"type": "attribute_filter", "using": "label/region", "state": {"include": ["EMEA"]}}}
    expected = _viz(query={"fields": {}, "filter_by": f})
    actual = _viz(query={"fields": {}, "filter_by": f})
    scores = check_filters(expected, actual)
    assert scores.all_ok is True
