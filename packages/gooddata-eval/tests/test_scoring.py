# (C) 2026 GoodData Corporation
from datetime import date

from gooddata_eval.core.models import CreatedVisualization
from gooddata_eval.core.scoring import (
    check_filters,
    check_viz_type,
    get_dimension_uri_set,
    get_metric_uri_set,
    normalized_filters,
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


# --- ranking-filter `attribute` is optional on single-dimension visualizations (QA-28615) ---
#
# `attribute` is NotRequired in the AAC schema and AFM ranks over the whole result when it is
# absent, so on a one-dimension chart "omitted" and "the sole dimension" mean the same filter.
# The comparator used to demand an exact match and failed those as filters_correct=False.

_M = {"m_sales": {"using": "metric/net_sales"}}
# same URI behind two different aliases — normalization must be alias-independent
_ONE_DIM_A = {**_M, "d_product_id": {"using": "label/product_id"}}
_ONE_DIM_B = {**_M, "d_product": {"using": "label/product_id"}}
_TWO_DIM = {**_M, "d_brand": {"using": "label/product_brand"}, "d_city": {"using": "label/customer_city"}}


def _rank_viz(fields, dims, **filter_overrides):
    rank = {"type": "ranking_filter", "using": "m_sales", "top": 1, **filter_overrides}
    return _viz(
        type="bar_chart",
        query={"fields": fields, "filter_by": {"f_rank": rank}},
        metrics=["m_sales"],
        view_by=dims,
    )


def test_ranking_attribute_optional_on_single_dimension_viz():
    """Expected names the attribute, actual omits it — one dimension, so they are equivalent."""
    expected = _rank_viz(_ONE_DIM_A, ["d_product_id"], attribute="d_product_id")
    actual = _rank_viz(_ONE_DIM_B, ["d_product"])
    scores = check_filters(expected, actual)
    assert scores.ranking_ok is True
    assert scores.all_ok is True


def test_ranking_attribute_optional_is_symmetric():
    """Reverse direction: the dataset omits the attribute and the agent supplies it."""
    expected = _rank_viz(_ONE_DIM_A, ["d_product_id"])
    actual = _rank_viz(_ONE_DIM_B, ["d_product"], attribute="d_product")
    assert check_filters(expected, actual).ranking_ok is True


def test_ranking_attribute_none_and_empty_are_the_same_as_omitted():
    expected = _rank_viz(_ONE_DIM_A, ["d_product_id"], attribute="d_product_id")
    for omitted in ({"attribute": None}, {"attribute": ""}):
        actual = _rank_viz(_ONE_DIM_B, ["d_product"], **omitted)
        assert check_filters(expected, actual).ranking_ok is True, omitted


def test_ranking_attribute_still_required_on_multi_dimension_viz():
    """Two dimensions: omitting the attribute ranks over the tuple, so it stays strict."""
    expected = _rank_viz(_TWO_DIM, ["d_brand", "d_city"], attribute="d_brand")
    actual = _rank_viz(_TWO_DIM, ["d_brand", "d_city"])
    assert check_filters(expected, actual).ranking_ok is False


def test_ranking_attribute_omitted_does_not_mask_a_wrong_top_n():
    expected = _rank_viz(_ONE_DIM_A, ["d_product_id"], attribute="d_product_id", top=1)
    actual = _rank_viz(_ONE_DIM_B, ["d_product"], top=5)
    assert check_filters(expected, actual).ranking_ok is False


def test_ranking_attribute_omitted_does_not_mask_a_wrong_dimension():
    expected = _rank_viz(_ONE_DIM_A, ["d_product_id"], attribute="d_product_id")
    actual = _rank_viz(_TWO_DIM, ["d_brand"])  # single dim, but a different one
    assert check_filters(expected, actual).ranking_ok is False


def test_validate_cross_references_never_raises_on_empty_or_none_uris():
    """Each of these used to raise AttributeError/TypeError instead of returning a score.

    Every case carries its expected verdict: `attribute` is optional so None/"" are valid,
    while a non-string attribute or a missing/None `using` must be reported as an error.
    Asserting the verdict is what stops a malformed filter from silently passing as valid.
    """
    cases = [
        ({"type": "ranking_filter", "using": "m_sales", "top": 5, "attribute": None}, True),
        ({"type": "ranking_filter", "using": "m_sales", "top": 5, "attribute": ""}, True),
        ({"type": "ranking_filter", "using": "m_sales", "top": 5, "attribute": []}, False),
        ({"type": "ranking_filter", "using": None, "top": 5}, False),
        ({"type": "ranking_filter", "top": 5}, False),
    ]
    for rank, expected_ok in cases:
        viz = _viz(query={"fields": _M, "filter_by": {"f_rank": rank}})
        ok, errors = validate_cross_references(viz)
        assert isinstance(ok, bool) and isinstance(errors, list), rank
        assert ok is expected_ok, rank
        assert bool(errors) is not expected_ok, rank


def test_validate_cross_references_accepts_omitted_attribute_but_flags_missing_using():
    omitted = _viz(query={"fields": _M, "filter_by": {"f": {"type": "ranking_filter", "using": "m_sales", "top": 5}}})
    assert validate_cross_references(omitted) == (True, [])

    no_using = _viz(query={"fields": _M, "filter_by": {"f": {"type": "ranking_filter", "top": 5}}})
    ok, errors = validate_cross_references(no_using)
    assert ok is False
    assert "is required" in errors[0]


def test_normalized_filters_groups_by_scored_category():
    """The three categories `check_filters` scores separately, in the form it compares."""
    viz = CreatedVisualization.model_validate(
        {
            "id": "x",
            "type": "bar_chart",
            "query": {
                "fields": {"m": {"using": "metric/spend"}, "d": {"using": "label/merchant.name"}},
                "filter_by": {
                    "f0": {
                        "type": "date_filter",
                        "using": "dataset/date",
                        "granularity": "MONTH",
                        "from": -1,
                        "to": -1,
                    },
                    "f1": {"type": "ranking_filter", "using": "m", "top": 5},
                    "f2": {"type": "attribute_filter", "using": "label/region", "state": {"include": ["EMEA"]}},
                },
            },
            "metrics": ["m"],
            "view_by": ["d"],
        }
    )
    grouped = normalized_filters(viz)
    assert set(grouped) == {"date", "ranking", "attribute"}
    assert all(len(v) == 1 for v in grouped.values())
    # The ranking entry carries the substituted sole dimension, matching what equality sees.
    assert '"dim_uri": "label/merchant.name"' in grouped["ranking"][0]


def test_normalized_filters_is_empty_per_category_when_unfiltered():
    viz = CreatedVisualization.model_validate(
        {
            "id": "x",
            "type": "headline",
            "query": {"fields": {"m": {"using": "metric/spend"}}, "filter_by": {}},
            "metrics": ["m"],
        }
    )
    assert normalized_filters(viz) == {"date": [], "ranking": [], "attribute": []}


# --- relative vs absolute date filters denote the same period ---
#
# The agent answers "last month" either relatively (granularity MONTH, from -1, to -1)
# or absolutely (from 2026-08-01, to 2026-08-31). Compared literally these never match,
# so a correct answer in whichever encoding the fixture did not happen to use was scored
# as a wrong date period. Both forms now collapse to the same absolute span.

_TODAY = date(2026, 9, 9)


def _date_viz(**overrides):
    f = {"using": "dataset/dt_transactions", "type": "date_filter"}
    f.update(overrides)
    return _viz(query={"fields": {}, "filter_by": {"f_d": f}})


def test_check_filters_relative_and_absolute_last_month_agree():
    expected = _date_viz(**{"from": -1, "to": -1, "granularity": "MONTH"})
    actual = _date_viz(**{"from": "2026-08-01", "to": "2026-08-31", "granularity": None})
    assert check_filters(expected, actual, _TODAY).date_ok is True


def test_check_filters_absolute_spanning_two_months_still_differs_from_one():
    """Normalization must not flatten a genuinely wrong window into a match."""
    expected = _date_viz(**{"from": -1, "to": -1, "granularity": "MONTH"})
    actual = _date_viz(**{"from": "2026-07-01", "to": "2026-08-31", "granularity": None})
    assert check_filters(expected, actual, _TODAY).date_ok is False


def test_check_filters_day_offsets_resolve_and_off_by_one_still_fails():
    expected = _date_viz(**{"from": -89, "to": 0, "granularity": "DAY"})
    assert check_filters(expected, _date_viz(**{"from": "2026-06-12", "to": "2026-09-09"}), _TODAY).date_ok is True
    assert check_filters(expected, _date_viz(**{"from": -90, "to": 0, "granularity": "DAY"}), _TODAY).date_ok is False


def test_check_filters_quarter_and_year_offsets_resolve():
    q = _date_viz(**{"from": -1, "to": -1, "granularity": "QUARTER"})
    assert check_filters(q, _date_viz(**{"from": "2026-04-01", "to": "2026-06-30"}), _TODAY).date_ok is True
    y = _date_viz(**{"from": 0, "to": 0, "granularity": "YEAR"})
    assert check_filters(y, _date_viz(**{"from": "2026-01-01", "to": "2026-12-31"}), _TODAY).date_ok is True


def test_check_filters_week_granularity_falls_back_to_literal_comparison():
    """WEEK start-of-week convention varies, so it is compared literally rather than guessed."""
    expected = _date_viz(**{"from": -2, "to": -1, "granularity": "WEEK"})
    assert check_filters(expected, _date_viz(**{"from": -2, "to": -1, "granularity": "WEEK"}), _TODAY).date_ok is True
    assert check_filters(expected, _date_viz(**{"from": -13, "to": 0, "granularity": "DAY"}), _TODAY).date_ok is False


def test_check_filters_date_still_distinguishes_the_dataset_it_hangs_off():
    expected = _date_viz(**{"from": -1, "to": -1, "granularity": "MONTH"})
    actual = _date_viz(using="dataset/dt_date", **{"from": -1, "to": -1, "granularity": "MONTH"})
    assert check_filters(expected, actual, _TODAY).date_ok is False
