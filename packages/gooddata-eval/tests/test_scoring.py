# (C) 2026 GoodData Corporation
from datetime import date

import pytest
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


# --- attribute-filter element order must not decide the verdict ---
#
# `_normalize_attribute_filter` passes `state` through untouched and the caller serialises
# it with json.dumps(..., sort_keys=True). sort_keys orders the DICT KEYS (field_uri,
# state, type) and never the LIST under state["include"], so two filters selecting the
# same elements in a different order compare unequal.
#
# Found from a real eval run (gdc-mic-ai-evaluation, micai_diagnose_master, 2026-09-10):
# a question filtering cross-border traffic scored metrics_correct=True,
# dimensions_correct=True, filters_correct=False, because the fixture listed
# ["Inter-region", "Intra-region"] and the agent emitted ["Intra-region", "Inter-region"].
# Element order is not something an agent has any reason to keep stable between runs, so
# every question needing a multi-value attribute filter passes or fails partly at random.


def test_attribute_filter_include_order_does_not_change_the_verdict():
    def viz(values):
        return _viz(
            query={
                "fields": {},
                "filter_by": {
                    "f_a": {
                        "type": "attribute_filter",
                        "using": "label/cross_border_name",
                        "state": {"include": values},
                    }
                },
            }
        )

    expected = viz(["Inter-region", "Intra-region"])
    actual = viz(["Intra-region", "Inter-region"])
    assert check_filters(expected, actual).attribute_ok is True


def test_attribute_filter_exclude_order_does_not_change_the_verdict():
    def viz(values):
        return _viz(
            query={
                "fields": {},
                "filter_by": {
                    "f_a": {
                        "type": "attribute_filter",
                        "using": "label/region",
                        "state": {"exclude": values},
                    }
                },
            }
        )

    assert check_filters(viz(["EMEA", "APAC"]), viz(["APAC", "EMEA"])).attribute_ok is True


def test_attribute_filter_with_different_elements_still_fails():
    """The fix must not make the comparison permissive -- a genuinely different set
    of elements is still a mismatch."""

    def viz(values):
        return _viz(
            query={
                "fields": {},
                "filter_by": {
                    "f_a": {
                        "type": "attribute_filter",
                        "using": "label/region",
                        "state": {"include": values},
                    }
                },
            }
        )

    assert check_filters(viz(["EMEA", "APAC"]), viz(["EMEA", "LATAM"])).attribute_ok is False


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


def test_check_filters_week_us_resolves_to_a_sunday_start_week():
    """WEEK_US is well defined (Sunday-start), unlike a bare WEEK."""
    expected = _date_viz(**{"from": 0, "to": 0, "granularity": "WEEK_US"})
    # 2026-09-09 is a Wednesday; its WEEK_US bucket runs Sun 09-06 .. Sat 09-12.
    assert check_filters(expected, _date_viz(**{"from": "2026-09-06", "to": "2026-09-12"}), _TODAY).date_ok is True
    assert check_filters(expected, _date_viz(**{"from": "2026-09-06", "to": "2026-09-09"}), _TODAY).date_ok is False


def test_check_filters_bare_week_granularity_falls_back_to_literal_comparison():
    """A bare WEEK is not in the AAC enum and names no convention, so it is not guessed."""
    expected = _date_viz(**{"from": -2, "to": -1, "granularity": "WEEK"})
    assert check_filters(expected, _date_viz(**{"from": -2, "to": -1, "granularity": "WEEK"}), _TODAY).date_ok is True
    assert check_filters(expected, _date_viz(**{"from": -13, "to": 0, "granularity": "DAY"}), _TODAY).date_ok is False


def test_check_filters_date_still_distinguishes_the_dataset_it_hangs_off():
    expected = _date_viz(**{"from": -1, "to": -1, "granularity": "MONTH"})
    actual = _date_viz(using="dataset/dt_date", **{"from": -1, "to": -1, "granularity": "MONTH"})
    assert check_filters(expected, actual, _TODAY).date_ok is False


@pytest.mark.parametrize(
    ("granularity", "offset"),
    [
        ("YEAR", -_TODAY.year),  # lands on year 0
        ("DAY", -(10**9)),  # past timedelta's magnitude limit
        ("WEEK_US", -(10**8)),
        ("MONTH", -30000),
        ("QUARTER", -10000),
    ],
)
def test_check_filters_out_of_range_offsets_fall_back_instead_of_raising(granularity, offset):
    """An offset outside the representable date range must not abort scoring.

    Every granularity can be pushed past date's 1..9999 year range (or timedelta's
    magnitude limit). Letting the ValueError/OverflowError escape would fail the whole
    item on one malformed filter, so the span resolves to None and the filter goes back
    to literal comparison -- which still matches an identically malformed expectation.
    """
    expected = _date_viz(**{"from": offset, "to": 0, "granularity": granularity})
    assert check_filters(expected, _date_viz(**{"from": offset, "to": 0, "granularity": granularity}), _TODAY).date_ok
    assert not check_filters(expected, _date_viz(**{"from": -1, "to": -1, "granularity": "MONTH"}), _TODAY).date_ok


def _attr_viz(values, key="include", using="label/cross_border_name"):
    return _viz(
        query={
            "fields": {"m": {"using": "metric/approval_rate"}},
            "filter_by": {"f": {"type": "attribute_filter", "using": using, "state": {key: values}}},
        },
        metrics=["m"],
    )


def test_attribute_filter_elements_compare_as_a_set_not_a_sequence():
    """`include`/`exclude` name a set of elements, so element order must not decide a verdict.

    json.dumps(sort_keys=True) orders the dict KEYS and leaves the lists alone, so the same
    filter emitted in a different order compared unequal -- and the agent has no reason to
    keep that order stable between runs. The failure reported as `filters_correct: false`,
    indistinguishable from the agent genuinely filtering wrongly.
    """
    expected = _attr_viz(["Inter-region", "Intra-region"])
    assert check_filters(expected, _attr_viz(["Inter-region", "Intra-region"])).attribute_ok is True
    assert check_filters(expected, _attr_viz(["Intra-region", "Inter-region"])).attribute_ok is True


def test_a_three_element_attribute_filter_is_order_insensitive():
    """Two elements need 2 permutations, three need 6 -- admitting them as extra fixture
    candidates grows factorially, which is why this belongs in normalisation."""
    expected = _attr_viz(["A", "B", "C"])
    for actual in (["C", "A", "B"], ["B", "C", "A"], ["C", "B", "A"]):
        assert check_filters(expected, _attr_viz(actual)).attribute_ok is True


def test_exclude_elements_are_order_insensitive_too():
    expected = _attr_viz(["Domestic", "Unknown"], key="exclude")
    assert check_filters(expected, _attr_viz(["Unknown", "Domestic"], key="exclude")).attribute_ok is True


def test_ordering_does_not_mask_a_genuinely_different_element_set():
    """The guard against the fix being "pass everything": different elements still fail."""
    expected = _attr_viz(["Inter-region", "Intra-region"])
    assert check_filters(expected, _attr_viz(["Inter-region"])).attribute_ok is False
    assert check_filters(expected, _attr_viz(["Inter-region", "Domestic"])).attribute_ok is False


def test_include_and_exclude_of_the_same_elements_still_differ():
    """Sorting must not collapse the two state keys into each other."""
    inc = _attr_viz(["Domestic", "Unknown"], key="include")
    exc = _attr_viz(["Unknown", "Domestic"], key="exclude")
    assert check_filters(inc, exc).attribute_ok is False


def test_the_same_elements_on_a_different_label_still_differ():
    expected = _attr_viz(["A", "B"], using="label/cross_border_name")
    assert check_filters(expected, _attr_viz(["B", "A"], using="label/region_name")).attribute_ok is False


def test_a_mixed_type_element_list_does_not_crash_scoring():
    """A malformed list would raise TypeError from a bare sorted(), and a crash inside
    scoring is worse than the mismatch this fixes. validate_cross_references reports
    malformed filter values separately, so this only has to stay comparable."""
    expected = _attr_viz(["A", 2])
    assert check_filters(expected, _attr_viz([2, "A"])).attribute_ok is True
    assert check_filters(expected, _attr_viz(["A", 3])).attribute_ok is False


def test_elements_that_stringify_alike_but_differ_in_type_still_sort_stably():
    """`key=str` collapsed 1 and "1" to the same sort key, so Python's stable sort left
    their relative order exactly as the agent emitted it and the ordering bug survived for
    that pair alone. The key is the element's canonical JSON instead, which distinguishes
    the types the comparison downstream also distinguishes."""
    assert check_filters(_attr_viz([1, "1"]), _attr_viz(["1", 1])).attribute_ok is True
    # ...without making the two types interchangeable: one element is not the other set.
    assert check_filters(_attr_viz([1]), _attr_viz(["1"])).attribute_ok is False


def test_heterogeneous_element_lists_sort_without_raising():
    """Every value here is parsed JSON, so json.dumps cannot fail on it -- which is what
    makes it usable as a total ordering where a bare sort would raise."""
    mixed = [None, True, 2, "a", 1.5]
    assert check_filters(_attr_viz(mixed), _attr_viz(list(reversed(mixed)))).attribute_ok is True
