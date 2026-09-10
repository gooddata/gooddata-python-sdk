# (C) 2026 GoodData Corporation
import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from gooddata_eval.core.dataset import from_insights as from_insights_mod
from gooddata_eval.core.dataset.from_insights import (
    PromisedRanking,
    Unsupported,
    _rules_for,
    _validation_errors,
    ambiguous_fields,
    ambiguous_titles,
    build,
    build_display_names,
    contradictions,
    convert,
    derive,
    derived_candidates,
    derived_n,
    describe,
    display_name,
    element_counts,
    generate,
    granularity_phrase,
    insight_ids_on,
    langfuse_payload,
    list_ids,
    mint_id,
    pick_derived,
    rankable,
    rescued,
    resolve_type,
    spec_signature,
    title_direction,
)
from gooddata_eval.core.dataset.local import load_local_dataset
from gooddata_eval.core.models import CreatedVisualization
from gooddata_eval.core.scoring import check_filters, get_metric_uri_set, validate_cross_references

DATE_IDS = {"process_date"}


def viz(url, buckets, filters=(), sorts=(), **kw):
    return {
        "id": "v_x",
        "title": kw.pop("title", "X"),
        "content": {"visualizationUrl": url, "buckets": buckets, "filters": list(filters), "sorts": list(sorts)},
        **kw,
    }


def measure(local_id, obj_id, obj_type="metric", **definition):
    return {
        "measure": {
            "localIdentifier": local_id,
            "definition": {
                "measureDefinition": {"item": {"identifier": {"type": obj_type, "id": obj_id}}, **definition}
            },
        }
    }


def attribute(local_id, label_id):
    return {
        "attribute": {"localIdentifier": local_id, "displayForm": {"identifier": {"type": "label", "id": label_id}}}
    }


def test_headline_converts_to_scorable_single_metric_spec():
    spec = convert(
        viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "gross_revenue")]}]), DATE_IDS
    )
    assert spec["type"] == "headline"
    assert spec["_shape"] == "single_metric_callout"
    # The alias is arbitrary; what must survive is the URI gd-eval scores on.
    parsed = CreatedVisualization(**{k: v for k, v in spec.items() if k != "_shape"})

    assert get_metric_uri_set(parsed) == {"metric/gross_revenue"}


def test_breakdown_and_time_series_are_distinguished_by_date_instance():
    by_dim = convert(
        viz(
            "local:bar",
            [
                {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                {"localIdentifier": "view", "items": [attribute("a", "merchant.name")]},
            ],
        ),
        DATE_IDS,
    )
    by_time = convert(
        viz(
            "local:column",
            [
                {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                {"localIdentifier": "view", "items": [attribute("a", "process_date.month")]},
            ],
        ),
        DATE_IDS,
    )
    assert by_dim["_shape"] == "breakdown_by_dimension"
    assert by_time["_shape"] == "time_series"


def test_filters_round_trip_into_scorable_filter_by():
    spec = convert(
        viz(
            "local:bar",
            [
                {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                {"localIdentifier": "view", "items": [attribute("a", "merchant.name")]},
            ],
            filters=[
                {
                    "absoluteDateFilter": {
                        "dataSet": {"identifier": {"id": "process_date"}},
                        "from": "2025-01-01",
                        "to": "2025-12-31",
                    }
                },
                {
                    "positiveAttributeFilter": {
                        "displayForm": {"identifier": {"id": "region"}},
                        "in": {"values": ["EMEA"]},
                    }
                },
                {"rankingFilter": {"measures": ["m"], "attributes": ["a"], "operator": "TOP", "value": 5}},
            ],
        ),
        DATE_IDS,
    )
    assert spec["_shape"] == "filtered_view"
    parsed = CreatedVisualization(**{k: v for k, v in spec.items() if k != "_shape"})

    # Ranking-filter aliases must resolve to metric/ and label/ URIs or gd-eval rejects them.
    assert validate_cross_references(parsed) == (True, [])
    assert check_filters(parsed, parsed).all_ok


def test_relative_date_granularity_is_normalized():
    spec = convert(
        viz(
            "local:headline",
            [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
            filters=[
                {
                    "relativeDateFilter": {
                        "dataSet": {"identifier": {"id": "process_date"}},
                        "granularity": "GDC.time.quarter",
                        "from": -1,
                        "to": -1,
                    }
                }
            ],
        ),
        DATE_IDS,
    )
    assert spec["query"]["filter_by"]["f0"] == {
        "type": "date_filter",
        "using": "dataset/process_date",
        "granularity": "QUARTER",
        "from": -1,
        "to": -1,
    }


def test_fact_measure_carries_its_aggregation():
    spec = convert(
        viz(
            "local:headline",
            [{"localIdentifier": "measures", "items": [measure("m", "amount", "fact", aggregation="sum")]}],
        ),
        DATE_IDS,
    )
    assert spec["query"]["fields"]["m_amount"] == {"using": "fact/amount", "aggregation": "SUM"}


@pytest.mark.parametrize(
    "bad,reason",
    [
        ({"measure": {"localIdentifier": "m", "definition": {"arithmeticMeasure": {}}}}, "derived"),
        (
            {
                "measure": {
                    "localIdentifier": "m",
                    "definition": {
                        "measureDefinition": {
                            "item": {"identifier": {"type": "metric", "id": "x"}},
                            "filters": [{"positiveAttributeFilter": {}}],
                        }
                    },
                }
            },
            "measure-level",
        ),
    ],
)
def test_underivable_measures_are_skipped_not_guessed(bad, reason):
    with pytest.raises(Unsupported, match=reason):
        convert(viz("local:headline", [{"localIdentifier": "measures", "items": [bad]}]), DATE_IDS)


def test_uri_form_attribute_filter_is_skipped_rather_than_guessed():
    with pytest.raises(Unsupported, match="literal values"):
        convert(
            viz(
                "local:bar",
                [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
                filters=[
                    {
                        "positiveAttributeFilter": {
                            "displayForm": {"identifier": {"id": "region"}},
                            "in": {"uris": ["/obj/1?id=2"]},
                        }
                    }
                ],
            ),
            DATE_IDS,
        )


def test_treemap_is_mapped_not_dropped():
    spec = convert(viz("local:treemap", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS)
    assert spec["type"] == "treemap"


def test_unmapped_viz_url_fails_loudly():
    with pytest.raises(Unsupported, match="unmapped visualizationUrl"):
        convert(viz("local:brandnew", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS)


def test_insight_ids_on_walks_nested_dashboard_layout():
    analytics = {
        "analyticalDashboards": [
            {
                "id": "d1",
                "content": {
                    "layout": {
                        "sections": [
                            {
                                "items": [
                                    {"widget": {"type": "insight", "insight": {"identifier": {"id": "v_a"}}}},
                                    {
                                        "widget": {
                                            "type": "IDashboardLayoutNested",
                                            "sections": [
                                                {
                                                    "items": [
                                                        {
                                                            "widget": {
                                                                "type": "insight",
                                                                "insight": {"identifier": {"id": "v_b"}},
                                                            }
                                                        }
                                                    ]
                                                }
                                            ],
                                        }
                                    },
                                ]
                            }
                        ]
                    }
                },
            },
            {
                "id": "d2",
                "content": {
                    "layout": {
                        "sections": [
                            {"items": [{"widget": {"type": "insight", "insight": {"identifier": {"id": "v_c"}}}}]}
                        ]
                    }
                },
            },
        ]
    }
    assert insight_ids_on(analytics, ["d1"]) == {"v_a", "v_b"}
    assert insight_ids_on(analytics, ["d1", "d2"]) == {"v_a", "v_b", "v_c"}
    assert insight_ids_on(analytics, ["nope"]) == set()


def test_langfuse_payload_shape():
    envelope = {"id": "q1", "question": "How much?", "expected_output": {"visualization": {}}}
    payload = langfuse_payload([envelope], "cust", "ws1", "origin note")
    assert payload["dataset"] == "cust" and payload["workspace"] == "ws1"
    item = payload["items"][0]
    assert item["id"] == "q1"
    assert item["input"] == {"question": "How much?"}
    assert item["expected_output"] == {"visualization": {}}
    assert item["metadata"]["origin"] == "origin note"


def test_built_envelope_is_loadable_as_a_dataset_item(tmp_path):
    """The whole point: what this writes must be runnable by `gd-eval run` as-is."""

    spec = convert(
        viz(
            "local:column",
            [
                {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                {"localIdentifier": "view", "items": [attribute("a", "process_date.month")]},
            ],
        ),
        DATE_IDS,
    )
    envelope = build(spec, "How did spend trend by month?", "micai_diagnose_master", set())
    assert "_shape" not in envelope["expected_output"]["visualization"]
    assert _validation_errors(envelope) is None

    (tmp_path / f"{envelope['id']}.json").write_text(json.dumps(envelope, indent=2))
    items = load_local_dataset(tmp_path)
    assert [i.id for i in items] == [envelope["id"]]
    assert items[0].test_kind == "visualization"
    assert items[0].dataset_name == "micai_diagnose_master"


def test_mint_id_is_stable_and_collision_safe():
    q = "How did spend trend by month?"
    assert mint_id(q, set()) == "how-did-spend-trend-by-month"
    second = mint_id(q, {"how-did-spend-trend-by-month"})
    assert second.startswith("how-did-spend-trend-by-month-") and second != q


def test_list_ids_reads_ids_already_in_the_output_folder(tmp_path):
    (tmp_path / "a.json").write_text(json.dumps({"id": "already-there"}))
    (tmp_path / "broken.json").write_text("{not json")
    assert list_ids(tmp_path) == {"already-there"}


def test_langfuse_id_prefix_applies_to_the_export_only():
    envelope = {"id": "q1", "question": "How much?", "expected_output": {"visualization": {}}}
    payload = langfuse_payload([envelope], "cust", "ws1", "origin", id_prefix="loop3-")
    assert payload["items"][0]["id"] == "loop3-q1"
    assert envelope["id"] == "q1"


# --- the fixes: no title leakage, no contradictions, real sorts/filters ------

DISPLAY = {
    "metric/spend": "Spend Amount",
    "label/merchant.NAME": "Merchant Name",
    "label/process_date.month": "Process Date - Month",
    "dataset/process_date": "Process Date",
}


def spend_by_merchant(**kw):
    return viz(
        "local:bar",
        [
            {"localIdentifier": "measures", "items": [measure("m", "spend")]},
            {"localIdentifier": "view", "items": [attribute("a", "merchant.NAME")]},
        ],
        **kw,
    )


def test_brief_omits_title_and_chart_type_and_uses_display_names():
    spec = convert(
        spend_by_merchant(
            title="Top Merchants",
            sorts=[
                {
                    "measureSortItem": {
                        "direction": "desc",
                        "locators": [{"measureLocatorItem": {"measureIdentifier": "m"}}],
                    }
                },
            ],
        ),
        DATE_IDS,
    )
    brief = describe(spec, DISPLAY)
    assert "Top Merchants" not in brief
    assert "bar" not in brief.lower()
    assert "metric/spend" not in brief and "merchant.NAME" not in brief
    assert "metric: Spend Amount" in brief
    assert "broken down by: Merchant Name" in brief
    assert "sorted by: Spend Amount, descending" in brief


def test_filters_are_briefed_in_words_not_json():
    spec = convert(
        spend_by_merchant(
            filters=[
                {
                    "absoluteDateFilter": {
                        "dataSet": {"identifier": {"id": "process_date"}},
                        "from": "2025-01-01",
                        "to": "2025-12-31",
                    }
                },
                {"rankingFilter": {"measures": ["m"], "attributes": ["a"], "operator": "TOP", "value": 5}},
            ]
        ),
        DATE_IDS,
    )
    brief = describe(spec, DISPLAY)
    assert "date range 2025-01-01 to 2025-12-31 on Process Date" in brief
    assert "top 5 by Spend Amount, ranked within Merchant Name" in brief
    assert "{" not in brief


@pytest.mark.parametrize(
    "title",
    [
        "Products by Most Items Sold",
        # "Least"/"Worst"/"Largest" name a ranking as plainly as "Most" does. Missing any
        # of them lets a mis-specified insight through as a base, and `--enrich-ranked`
        # then derives a *top* N from a chart whose own title says the opposite.
        "Products by Least Items Sold",
        "Worst Performing Merchants",
        "Largest Accounts",
    ],
)
def test_degenerate_ranking_titles_are_skipped(title):
    with pytest.raises(Unsupported, match="promises a ranking"):
        convert(spend_by_merchant(title=title), DATE_IDS)


def test_degenerate_titles_are_skipped_rather_than_contradicted():
    with pytest.raises(Unsupported, match="promises a ranking"):
        convert(spend_by_merchant(title="Products by Most Items Sold"), DATE_IDS)
    with pytest.raises(Unsupported, match="promises a filter"):
        convert(spend_by_merchant(title="Spend for repeat purchases only"), DATE_IDS)


def test_a_real_sort_or_ranking_legitimises_a_ranking_title():
    spec = convert(
        spend_by_merchant(
            title="Top 5 Merchants", filters=[{"rankingFilter": {"measures": ["m"], "operator": "TOP", "value": 5}}]
        ),
        DATE_IDS,
    )
    assert spec["_shape"] == "filtered_view"
    sorted_spec = convert(
        spend_by_merchant(
            title="Merchants, Most Spend First",
            sorts=[{"attributeSortItem": {"attributeIdentifier": "a", "direction": "asc"}}],
        ),
        DATE_IDS,
    )
    assert sorted_spec["sort_by"] == [{"field": "d_merchant_name", "direction": "ASC"}]


def test_contradictions_flag_ranking_and_filter_language_the_spec_lacks():
    plain = convert(spend_by_merchant(), DATE_IDS)
    assert contradictions("Which merchants drove the most spend?", plain)
    assert contradictions("Show spend by merchant for last quarter", plain)
    assert contradictions("How does spend break down across merchants?", plain) == []

    ranked = convert(
        spend_by_merchant(filters=[{"rankingFilter": {"measures": ["m"], "operator": "TOP", "value": 5}}]), DATE_IDS
    )
    assert contradictions("What are the top 5 merchants by spend?", ranked) == []


def test_type_is_kept_only_when_the_question_names_the_chart_form():
    spec = convert(spend_by_merchant(), DATE_IDS)
    assert resolve_type(spec, "Show me spend by merchant as a bar chart") == "bar_chart"
    assert resolve_type(spec, "Which merchants did we spend the most with?") == ""


def test_build_blanks_type_for_a_question_that_names_no_chart_form():

    spec = convert(spend_by_merchant(), DATE_IDS)
    envelope = build(spec, "How does spend break down across merchants?", "p", set())
    assert envelope["expected_output"]["visualization"]["type"] == ""


def test_display_names_cover_metrics_facts_labels_and_date_granularities():
    names = build_display_names(
        {"metrics": [{"id": "m_spend", "title": "Spend Amount"}]},
        {
            "datasets": [
                {
                    "id": "merchant",
                    "title": "Merchant",
                    "facts": [{"id": "amt", "title": "Amount"}],
                    "attributes": [
                        {"id": "merchant.NAME", "title": "Merchant Name", "labels": []},
                        {
                            "id": "merchant.CTRY",
                            "title": "Country",
                            "labels": [{"id": "merchant.CTRY_ISO", "title": "Country ISO"}],
                        },
                    ],
                }
            ],
            "dateInstances": [{"id": "process_date", "title": "Process Date", "granularities": ["MONTH", "YEAR"]}],
        },
    )
    assert names["metric/m_spend"] == "Spend Amount"
    assert names["fact/amt"] == "Amount"
    assert names["label/merchant.NAME"] == "Merchant Name"
    assert names["label/merchant.CTRY_ISO"] == "Country ISO"
    assert names["label/process_date.month"] == "Process Date - Month"
    assert names["dataset/process_date"] == "Process Date"
    # No raw id ever reaches question text, even for something the LDM didn't name.
    assert display_name("metric/m_units_sold", names) == "M Units Sold"


# --- breakdown clause must match the spec's actual dimensions ---------------


def test_metric_echoed_as_its_own_dimension_is_a_hard_error():
    headline = convert(
        viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS
    )
    assert contradictions("Can you show me Spend Amount by Spend Amount?", headline, DISPLAY)
    assert contradictions("Can you show me Spend Amount broken down by Spend Amount?", headline, DISPLAY)
    assert contradictions("Can you show me Spend Amount?", headline, DISPLAY) == []


def test_unsubstituted_placeholder_is_a_hard_error():
    headline = convert(
        viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS
    )
    for bad in (
        "Can you show me Spend Amount by breakdown dimension?",
        "Can you show me Spend Amount by {dimension}?",
        "Can you show me Spend Amount by <split dimension>?",
    ):
        assert contradictions(bad, headline, DISPLAY), bad


def test_breakdown_promised_but_not_expected():
    headline = convert(
        viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS
    )
    assert contradictions("Can you show me Spend Amount by Merchant Name?", headline, DISPLAY)
    # Explicit negation is legitimate phrasing, not a contradiction.
    for ok in (
        "Can you show me Spend Amount with no breakdown?",
        "Can you show me Spend Amount without breaking it down by any dimension?",
    ):
        assert contradictions(ok, headline, DISPLAY) == [], ok


def test_breakdown_expected_but_not_asked_is_the_same_severity():
    spec = convert(spend_by_merchant(), DATE_IDS)
    assert contradictions("Can you show me Spend Amount?", spec, DISPLAY)
    assert contradictions("Can you show me Spend Amount by Merchant Name?", spec, DISPLAY) == []
    # Plurals and reordering still count as naming the dimension.
    assert contradictions("How does Spend Amount break down across merchants?", spec, DISPLAY) == []


def test_ranking_phrasing_without_a_dimension_is_not_a_false_breakdown():
    ranked = convert(
        viz(
            "local:headline",
            [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
            filters=[{"rankingFilter": {"measures": ["m"], "operator": "TOP", "value": 5}}],
        ),
        DATE_IDS,
    )
    assert contradictions("What is the top 5 by Spend Amount?", ranked, DISPLAY) == []


def test_every_reported_malformed_question_is_caught():
    """The 7 real failures from the gpt-5.4 run over the Loop workspace."""
    headline = convert(
        viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS
    )
    names = {"metric/spend": "Variant Exchange Ratio"}
    for bad in (
        "Can you show me Variant Exchange Ratio broken down by Variant Exchange Ratio?",
        "Can you show me the Variant Exchange Ratio by Variant Exchange Ratio?",
        "Can you show me Variant Exchange Ratio by breakdown dimension?",
    ):
        assert contradictions(bad, headline, names), bad
    assert contradictions("Can you show me Variant Exchange Ratio?", headline, names) == []


# --- AD's "All" filters and the singular ranking form -----------------------


@pytest.mark.parametrize(
    "noop",
    [
        {"negativeAttributeFilter": {"displayForm": {"identifier": {"id": "product_name"}}, "notIn": {"values": []}}},
        {"positiveAttributeFilter": {"displayForm": {"identifier": {"id": "product_name"}}, "in": {"values": []}}},
        {"relativeDateFilter": {"dataSet": {"identifier": {"id": "process_date"}}, "granularity": "GDC.time.month"}},
    ],
)
def test_all_selection_filters_are_dropped_not_fatal(noop):
    """AD writes an unset filter as an empty exclusion or an all-time window.

    It restricts nothing, so it must not appear in the spec -- and must not cost the
    insight, which is otherwise perfectly expressible.
    """
    spec = convert(spend_by_merchant(filters=[noop]), DATE_IDS)
    assert spec["query"]["filter_by"] == {}
    assert spec["_shape"] == "breakdown_by_dimension"


def test_dropped_noop_filter_does_not_leave_a_gap_in_filter_keys():
    spec = convert(
        spend_by_merchant(
            filters=[
                {"negativeAttributeFilter": {"displayForm": {"identifier": {"id": "x"}}, "notIn": {"values": []}}},
                {
                    "positiveAttributeFilter": {
                        "displayForm": {"identifier": {"id": "region"}},
                        "in": {"values": ["EMEA"]},
                    }
                },
            ]
        ),
        DATE_IDS,
    )
    assert list(spec["query"]["filter_by"]) == ["f0"]


def test_singular_ranking_filter_form_is_understood():
    """AD emits `measure: {localIdentifier}`, not only `measures: [localId]`."""
    spec = convert(
        spend_by_merchant(
            filters=[{"rankingFilter": {"measure": {"localIdentifier": "m"}, "operator": "TOP", "value": 3}}]
        ),
        DATE_IDS,
    )
    assert spec["query"]["filter_by"]["f0"] == {"type": "ranking_filter", "using": "m_spend", "top": 3}

    with_attribute = convert(
        spend_by_merchant(
            filters=[
                {
                    "rankingFilter": {
                        "measure": {"localIdentifier": "m"},
                        "attribute": {"localIdentifier": "a"},
                        "operator": "BOTTOM",
                        "value": 5,
                    }
                }
            ]
        ),
        DATE_IDS,
    )
    assert with_attribute["query"]["filter_by"]["f0"]["attribute"] == "d_merchant_name"
    assert with_attribute["query"]["filter_by"]["f0"]["bottom"] == 5


def test_uri_form_attribute_filter_is_still_skipped():
    """The guard the empty-values case was wrongly sharing: uris can't become literals."""
    with pytest.raises(Unsupported, match="literal values"):
        convert(
            spend_by_merchant(
                filters=[
                    {
                        "negativeAttributeFilter": {
                            "displayForm": {"identifier": {"id": "x"}},
                            "notIn": {"uris": ["/obj/1"]},
                        }
                    }
                ]
            ),
            DATE_IDS,
        )


# --- derived ranking variants -------------------------------------------------


def _bar(metric_id, label_id, **kw):
    return viz(
        "local:bar",
        [
            {"localIdentifier": "measures", "items": [measure("m", metric_id)]},
            {"localIdentifier": "view", "items": [attribute("a", label_id)]},
        ],
        **kw,
    )


def test_a_plain_single_metric_breakdown_is_rankable():
    spec = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    assert rankable(spec, DATE_IDS) == "d_merchant_name"


@pytest.mark.parametrize(
    "content,reason",
    [
        (
            viz(
                "local:bar",
                [
                    {
                        "localIdentifier": "measures",
                        "items": [measure("m", "spend"), measure("m2", "gross_revenue")],
                    },
                    {"localIdentifier": "view", "items": [attribute("a", "merchant.NAME")]},
                ],
            ),
            "two metrics leave 'top 3 by what?' unanswered",
        ),
        (
            viz(
                "local:bar",
                [
                    {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                    {"localIdentifier": "view", "items": [attribute("a", "merchant.NAME")]},
                    {"localIdentifier": "segment", "items": [attribute("b", "region.NAME")]},
                ],
            ),
            "a segment makes the N ambiguous between the pair and within a group",
        ),
        (
            viz(
                "local:line",
                [
                    {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                    {"localIdentifier": "trend", "items": [attribute("a", "process_date.month")]},
                ],
            ),
            "'top 3 months' is not a question anyone asks",
        ),
        (
            _bar("spend", "merchant.NAME", sorts=[{"attributeSortItem": {"attributeIdentifier": "a"}}]),
            "already sorts, so the shape is covered by the real insight",
        ),
    ],
)
def test_ineligible_bases_are_not_ranked(content, reason):
    assert rankable(convert(content, DATE_IDS), DATE_IDS) is None, reason


def test_headline_without_a_dimension_is_not_rankable():
    spec = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS)
    assert rankable(spec, DATE_IDS) is None


@pytest.mark.parametrize("count,expected", [(None, 3), (2, None), (4, None), (5, 3), (6, 3), (7, 5), (50, 5)])
def test_n_needs_headroom_over_the_element_count(count, expected):
    assert derived_n(count) == expected


def test_ranking_variant_limits_the_rows_and_keeps_the_base_intact():
    base = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    out = derive(base, "ranking_filter", 3, DATE_IDS)

    assert list(out["query"]["filter_by"].values()) == [{"type": "ranking_filter", "using": "m_spend", "top": 3}]
    assert out["sort_by"] == []
    assert out["_derived_from"] == "v_x"
    assert out["_derived_kind"] == "ranking_filter"
    assert out["id"] != base["id"]
    assert base["query"]["filter_by"] == {}, "the base spec must not be mutated"


def test_sort_variant_orders_without_limiting():
    out = derive(convert(_bar("spend", "merchant.NAME"), DATE_IDS), "sort_by", 3, DATE_IDS)

    assert out["sort_by"] == [{"field": "m_spend", "direction": "DESC"}]
    assert out["query"]["filter_by"] == {}, "a sort must not silently limit the rows"


def test_derived_variants_are_scorable_and_valid():
    base = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    for kind in ("ranking_filter", "sort_by"):
        envelope = build(derive(base, kind, 3, DATE_IDS), "Show the top 3 Merchants by Spend", "d", set())
        assert _validation_errors(envelope) is None
        CreatedVisualization.model_validate(envelope["expected_output"]["visualization"])


def test_a_derived_item_records_where_it_came_from():
    base = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    envelope = build(derive(base, "ranking_filter", 5, DATE_IDS), "Show the top 5 Merchants by Spend", "d", set())

    assert envelope["derived_from"] == "v_x"
    assert envelope["derived_kind"] == "ranking_filter"
    assert "_derived_from" not in envelope["expected_output"]["visualization"], "provenance is not part of the spec"

    payload = langfuse_payload([envelope], "d", "ws", "origin")
    assert payload["items"][0]["metadata"]["derived_from"] == "v_x"


def test_a_base_item_carries_no_provenance_keys():
    envelope = build(convert(_bar("spend", "merchant.NAME"), DATE_IDS), "Show Spend by Merchant", "d", set())
    assert "derived_from" not in envelope
    assert "derived_kind" not in langfuse_payload([envelope], "d", "ws", "o")["items"][0]["metadata"]


def test_derived_ranking_reads_as_a_ranking_not_a_breakdown():
    base = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    rules = _rules_for(derive(base, "ranking_filter", 3, DATE_IDS), DISPLAY)
    assert "the top 3 Merchant Name" in rules
    assert "exactly once" in rules
    assert "- Say the question is broken down by" not in rules, "the ranking line replaces the breakdown line"


def test_a_ranking_within_an_attribute_still_asks_for_the_breakdown():
    # `ranked within <attribute>` ranks inside each group, so the breakdown is real and
    # the question has to name it.
    spec = convert(spend_by_merchant(), DATE_IDS)
    spec["query"]["filter_by"]["f0"] = {
        "type": "ranking_filter",
        "using": "m_spend",
        "attribute": "d_merchant_name",
        "top": 3,
    }
    assert "- Say the question is broken down by" in _rules_for(spec, DISPLAY)


def test_a_derived_question_naming_the_ranking_is_not_a_contradiction():
    spec = derive(convert(_bar("spend", "merchant.NAME"), DATE_IDS), "ranking_filter", 3, DATE_IDS)
    assert contradictions("Show me the top 3 Merchant Name values by Spend", spec, DISPLAY) == []


def test_picks_spread_across_metrics_before_repeating_one():
    specs = [
        convert(_bar("spend", "merchant.NAME"), DATE_IDS),
        convert(_bar("spend", "region.NAME"), DATE_IDS),
        convert(_bar("gross_revenue", "merchant.NAME"), DATE_IDS),
    ]
    picked = pick_derived(specs, DATE_IDS, 2, counts={})

    metrics = {p["metrics"][0] for p in picked}
    assert len(metrics) == 2, "one popular metric must not take the whole budget"


def test_ranking_variants_are_exhausted_before_any_sort_variant():
    specs = [convert(_bar("spend", "merchant.NAME"), DATE_IDS), convert(_bar("gross_revenue", "region.NAME"), DATE_IDS)]

    assert [p["_derived_kind"] for p in pick_derived(specs, DATE_IDS, 2, counts={})] == [
        "ranking_filter",
        "ranking_filter",
    ]
    kinds = [p["_derived_kind"] for p in pick_derived(specs, DATE_IDS, 4, counts={})]
    assert sorted(kinds) == ["ranking_filter", "ranking_filter", "sort_by", "sort_by"]


def test_the_budget_is_a_hard_cap():
    specs = [convert(_bar("spend", f"d{i}.NAME"), DATE_IDS) for i in range(10)]
    assert len(pick_derived(specs, DATE_IDS, 3, counts={})) == 3


def test_a_low_cardinality_dimension_is_not_ranked():
    specs = [convert(_bar("spend", "merchant.NAME"), DATE_IDS)]
    assert pick_derived(specs, DATE_IDS, 5, counts={"label/merchant.NAME": 3}) == []


def test_n_follows_the_element_count():
    specs = [convert(_bar("spend", "merchant.NAME"), DATE_IDS)]
    picked = pick_derived(specs, DATE_IDS, 1, counts={"label/merchant.NAME": 40})
    assert next(iter(picked[0]["query"]["filter_by"].values()))["top"] == 5


def test_candidates_are_only_the_dimensions_a_derivation_would_need():
    specs = [
        convert(_bar("spend", "merchant.NAME"), DATE_IDS),
        convert(
            viz(
                "local:line",
                [
                    {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                    {"localIdentifier": "trend", "items": [attribute("a", "process_date.month")]},
                ],
            ),
            DATE_IDS,
        ),
    ]
    assert derived_candidates(specs, DATE_IDS) == {"label/merchant.NAME"}


def test_element_counts_stop_at_the_ceiling_and_survive_an_unservable_label():
    class _Content:
        def get_label_elements(self, workspace_id, label_id, limit=None):
            if label_id == "label/bad":
                raise RuntimeError("no such label")
            assert limit == 7, "counting further than the largest N plus headroom is wasted work"
            return ["v"] * limit

    class _Sdk:
        catalog_workspace_content = _Content()

    assert element_counts(_Sdk(), "ws", {"label/merchant.NAME", "label/bad"}) == {"label/merchant.NAME": 7}


# --- rescuing insights whose titles promised a ranking ------------------------


@pytest.mark.parametrize(
    "title,direction",
    [
        ("Top Returned Reasons", "top"),
        ("Products With the Highest Return Rate", "top"),
        ("Products by Most Items Sold", "top"),
        ("Largest Accounts", "top"),
        ("Products With the Lowest Return Rate", "bottom"),
        ("Products by Least Items Sold", "bottom"),
        ("Worst Performing Merchants", "bottom"),
        # Names both ends, so it names neither: implementing one would be a coin flip.
        ("Top and Bottom Products", None),
        ("Spend by Merchant", None),
    ],
)
def test_title_direction(title, direction):
    assert title_direction(title) == direction


def test_a_promised_ranking_carries_the_spec_and_the_intent():
    with pytest.raises(PromisedRanking) as caught:
        convert(spend_by_merchant(title="Top 10 Merchants by Spend"), DATE_IDS)

    assert caught.value.direction == "top"
    assert caught.value.n == 10
    assert caught.value.spec["metrics"] == ["m_spend"]
    assert isinstance(caught.value, Unsupported), "still unusable as a copied fixture"


def test_a_promised_ranking_without_a_number_leaves_n_open():
    with pytest.raises(PromisedRanking) as caught:
        convert(spend_by_merchant(title="Top Merchants"), DATE_IDS)
    assert caught.value.n is None


def test_an_ambiguous_ranking_title_is_a_plain_skip():
    with pytest.raises(Unsupported) as caught:
        convert(spend_by_merchant(title="Top and Bottom Merchants"), DATE_IDS)
    assert not isinstance(caught.value, PromisedRanking)


def _promised(title):
    with pytest.raises(PromisedRanking) as caught:
        convert(spend_by_merchant(title=title), DATE_IDS)
    return caught.value


def test_a_lowest_title_is_implemented_as_a_bottom_n():
    items = rescued([_promised("Merchants With the Lowest Spend")], DATE_IDS, {"label/merchant.NAME": 40})

    ranking = next(iter(items[0]["query"]["filter_by"].values()))
    assert ranking == {"type": "ranking_filter", "using": "m_spend", "bottom": 5}
    assert items[0]["_derived_basis"] == "title", "the human's title asked for this, not the generator"


def test_an_explicit_n_in_the_title_wins_over_the_default():
    items = rescued([_promised("Top 10 Merchants by Spend")], DATE_IDS, {"label/merchant.NAME": 40})
    assert next(iter(items[0]["query"]["filter_by"].values()))["top"] == 10


def test_a_title_asking_for_more_rows_than_exist_is_not_rescued():
    assert rescued([_promised("Top 10 Merchants by Spend")], DATE_IDS, {"label/merchant.NAME": 7}) == []


def test_a_promised_ranking_on_an_unrankable_shape_is_not_rescued():
    error = PromisedRanking(
        "promises a ranking",
        convert(
            viz(
                "local:line",
                [
                    {"localIdentifier": "measures", "items": [measure("m", "spend")]},
                    {"localIdentifier": "trend", "items": [attribute("a", "process_date.month")]},
                ],
            ),
            DATE_IDS,
        ),
        "top",
        5,
    )
    assert rescued([error], DATE_IDS, {}) == []


def test_rescued_items_are_spent_before_anything_the_generator_invents():
    # A base unrelated to the rescued one, so ordering is what is under test here and
    # not the dedup that would otherwise collapse two identical rankings.
    specs = [convert(_bar("revenue", "region.NAME"), DATE_IDS)]
    promised = [_promised("Top Merchants by Spend")]

    picked = pick_derived(specs, DATE_IDS, 1, counts={}, promised=promised)
    assert [p["_derived_basis"] for p in picked] == ["title"]

    picked = pick_derived(specs, DATE_IDS, 3, counts={}, promised=promised)
    assert [p["_derived_basis"] for p in picked] == ["title", "shape", "shape"]


def test_element_counts_cover_the_rescue_candidates_too():
    promised = [_promised("Top Merchants by Spend")]
    assert derived_candidates([], DATE_IDS, promised) == {"label/merchant.NAME"}


def test_a_bottom_sort_is_ascending():
    out = derive(convert(_bar("spend", "merchant.NAME"), DATE_IDS), "sort_by", 3, DATE_IDS, direction="bottom")
    assert out["sort_by"] == [{"field": "m_spend", "direction": "ASC"}]


def test_an_unknown_direction_is_a_programming_error():
    base = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    with pytest.raises(ValueError, match="direction"):
        derive(base, "ranking_filter", 3, DATE_IDS, direction="middle")


def test_a_rescued_item_is_scorable_and_says_the_title_asked_for_it():
    items = rescued([_promised("Top 5 Merchants by Spend")], DATE_IDS, {"label/merchant.NAME": 40})
    envelope = build(items[0], "What are the top 5 Merchants by Spend?", "d", set())

    assert _validation_errors(envelope) is None
    assert envelope["derived_basis"] == "title"
    assert langfuse_payload([envelope], "d", "ws", "o")["items"][0]["metadata"]["derived_basis"] == "title"


def test_a_bottom_ranking_is_briefed_as_bottom():
    items = rescued([_promised("Merchants With the Lowest Spend")], DATE_IDS, {"label/merchant.NAME": 40})
    assert "bottom 5 by Spend Amount" in describe(items[0], DISPLAY)
    assert "the bottom 5 Merchant Name" in _rules_for(items[0], DISPLAY)


def test_two_insights_with_one_definition_do_not_become_two_items():
    # loop has "Products by Most Items Sold" and "Products Driving the Highest Number of
    # Repeat Purchases" over the same metric and dimension. Both promise a ranking, and
    # deriving from each produced the identical question twice.
    promised = [_promised("Products by Most Items Sold"), _promised("Products With the Highest Spend")]
    picked = pick_derived([], DATE_IDS, 5, counts={"label/merchant.NAME": 40}, promised=promised)

    assert len(picked) == 1
    assert len({spec_signature(spec) for spec in picked}) == 1


def test_dedup_compares_what_is_asked_not_how_it_is_titled():
    base = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    same = derive(base, "ranking_filter", 5, DATE_IDS)
    renamed = derive({**base, "title": "Something Else", "id": "v_other"}, "ranking_filter", 5, DATE_IDS)
    assert spec_signature(same) == spec_signature(renamed)

    other_n = derive(base, "ranking_filter", 3, DATE_IDS)
    other_end = derive(base, "ranking_filter", 5, DATE_IDS, direction="bottom")
    assert len({spec_signature(s) for s in (same, other_n, other_end)}) == 3


def test_a_rescue_and_an_invented_ranking_that_agree_yield_one_item():
    # `pick_derived` spends rescues first, so the surviving item is the grounded one.
    base = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    picked = pick_derived(
        [base],
        DATE_IDS,
        5,
        counts={"label/merchant.NAME": 40},
        promised=[_promised("Top 5 Merchants by Spend")],
    )
    ranked = [spec for spec in picked if spec["_derived_kind"] == "ranking_filter"]
    assert [spec["_derived_basis"] for spec in ranked] == ["title"]


# --- items that cannot name what they mean ------------------------------------


def test_a_question_asking_for_one_number_must_ask_to_see_it():
    # A bare "What is the Upsell Ratio?" reads as a request for a definition, and the
    # agent answers in prose: seven of loop's headline items failed with no chart built.
    spec = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]), DATE_IDS)
    rules = _rules_for(spec, DISPLAY)
    assert "AS A CHART" in rules
    assert "as a single number" in rules
    assert "Never a bare 'What is <metric>?'" in rules
    assert "Do not name the chart type" not in rules, "a single number needs its form named"


def test_a_broken_down_question_is_not_told_to_name_a_chart_form():
    assert "AS A CHART" not in _rules_for(convert(spend_by_merchant(), DATE_IDS), DISPLAY)


def test_titles_carried_by_more_than_one_object_are_ambiguous():
    names = {
        "label/product_details.LINE_ITEM_TITLE": "Product Title",
        "label/EXT__RETURNED_ITEMS.PRODUCT_TITLE": "Product Title",
        "label/merchant.NAME": "Merchant Name",
        "metric/spend": "Spend Amount",
    }
    assert ambiguous_titles(names) == {"product title"}


def test_the_same_object_listed_twice_is_not_ambiguous():
    assert ambiguous_titles({"label/a": "Product Title"}) == set()


def test_an_item_naming_an_ambiguous_dimension_is_reported():
    spec = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    names = {**DISPLAY, "label/other_dataset.NAME": "Merchant Name"}
    assert ambiguous_fields(spec, names) == ["Merchant Name"]
    assert ambiguous_fields(spec, DISPLAY) == []


def test_an_ambiguous_metric_name_counts_too():
    spec = convert(_bar("spend", "merchant.NAME"), DATE_IDS)
    names = {**DISPLAY, "metric/spend_v2": "Spend Amount"}
    assert ambiguous_fields(spec, names) == ["Spend Amount"]


# --- date granularities -------------------------------------------------------


@pytest.mark.parametrize("spelling", ["monthOfYear", "month_of_year", "MONTH_OF_YEAR"])
def test_every_spelling_of_a_granularity_resolves(spelling):
    # The API returns label ids camelCase; the declarative LDM lists the enum member.
    # A lookup under one spelling must not miss the other and fall back to a de-slugged
    # id ("Order Created At - Monthofyear").
    phrase = granularity_phrase(f"label/ORDER_CREATED_AT.{spelling}", {"dataset/ORDER_CREATED_AT": "Order Created At"})
    assert phrase == "Order Created At, by month of the year (January to December), combining every year"


def test_a_sequential_granularity_rules_out_its_cyclical_twin():
    phrase = granularity_phrase("label/ORDER_CREATED_AT.month", {"dataset/ORDER_CREATED_AT": "Order Created At"})
    assert "one point per calendar month over time" in phrase
    assert "not month-of-year" in phrase


def test_a_plain_label_has_no_granularity_phrase():
    assert granularity_phrase("label/product_details.LINE_ITEM_TITLE", DISPLAY) is None
    assert granularity_phrase("metric/spend", DISPLAY) is None


def test_display_names_cover_both_spellings_of_every_granularity():
    names = build_display_names(
        {},
        {
            "dateInstances": [
                {"id": "ORDER_CREATED_AT", "title": "Order Created At", "granularities": ["MONTH_OF_YEAR"]}
            ]
        },
    )
    assert names["label/ORDER_CREATED_AT.monthOfYear"] == "Order Created At - Month of Year"
    assert names["label/ORDER_CREATED_AT.month_of_year"] == "Order Created At - Month of Year"


def _monthly(metric="spend", granularity="month"):
    return viz(
        "local:line",
        [
            {"localIdentifier": "measures", "items": [measure("m", metric)]},
            {"localIdentifier": "trend", "items": [attribute("a", f"process_date.{granularity}")]},
        ],
    )


def test_a_date_breakdown_is_briefed_by_what_it_does():
    spec = convert(_monthly(), DATE_IDS)
    brief = describe(spec, DISPLAY)
    assert "broken down by: Process Date, by month, one point per calendar month over time" in brief
    assert "Process Date - Month" not in brief, "a label id in prose is not what an analyst says"


def test_a_date_breakdown_is_not_asked_for_verbatim():
    rules = _rules_for(convert(_monthly(), DATE_IDS), DISPLAY)
    assert "natural words" in rules
    assert "never as a label name" in rules
    assert "naming each verbatim" not in rules


def test_a_plain_dimension_is_still_asked_for_verbatim():
    rules = _rules_for(convert(spend_by_merchant(), DATE_IDS), DISPLAY)
    assert "broken down by Merchant Name, naming each verbatim" in rules
    assert "natural words" not in rules


def test_a_question_saying_by_month_still_names_the_dimension():
    spec = convert(_monthly(), DATE_IDS)
    assert contradictions("Can you show me Spend Amount by month for Process Date?", spec, DISPLAY) == []


def test_a_ranking_word_inside_a_field_name_is_not_a_claim():
    # loop's date dataset is called "Most Recent Label Created At". A question naming it
    # verbatim -- which the rules require -- was dropped for "using ranking word 'Most'".
    spec = convert(
        viz(
            "local:line",
            [
                {"localIdentifier": "measures", "items": [measure("m", "total_labels")]},
                {"localIdentifier": "trend", "items": [attribute("a", "most_recent_label_created_at.month")]},
            ],
        ),
        {"most_recent_label_created_at"},
    )
    names = {
        "metric/total_labels": "Total Labels",
        "dataset/most_recent_label_created_at": "Most Recent Label Created At",
        "label/most_recent_label_created_at.month": "Most Recent Label Created At - Month",
    }
    question = "Can you show me Total Labels by month for Most Recent Label Created At?"
    assert contradictions(question, spec, names) == []


def test_a_real_ranking_claim_is_still_caught_around_the_names():
    spec = convert(spend_by_merchant(), DATE_IDS)
    problems = contradictions("Show me the top 5 Merchant Name values by Spend Amount", spec, DISPLAY)
    assert any("ranking word" in p for p in problems)


def test_a_filter_word_inside_a_field_name_is_not_a_claim():
    spec = convert(spend_by_merchant(), DATE_IDS)
    names = {**DISPLAY, "label/merchant.NAME": "Merchant Name Excluding Test Accounts"}
    assert contradictions("Show me Spend Amount by Merchant Name Excluding Test Accounts", spec, names) == []


def test_granularity_aliases_are_one_object_not_a_collision():
    names = build_display_names(
        {},
        {"dateInstances": [{"id": "RETURN_AT", "title": "Return At", "granularities": ["MONTH", "MONTH_OF_YEAR"]}]},
    )
    # Each granularity is registered under several spellings; the aliases must fold.
    assert ambiguous_titles(names) == set()


# --- the generate() pipeline --------------------------------------------------


def _snapshot(*vizs, granularities=("MONTH",)):
    return {
        "workspace_id": "ws",
        "analytics": {
            "visualizationObjects": list(vizs),
            "metrics": [{"id": "spend", "title": "Spend Amount"}],
        },
        "date_instance_ids": ["process_date"],
        "display_names": {
            "metric/spend": "Spend Amount",
            "metric/revenue": "Revenue Amount",
            "label/merchant.NAME": "Merchant Name",
            "label/region.NAME": "Region Name",
            "dataset/process_date": "Process Date",
        },
        "label_cardinality": {"label/merchant.NAME": 40, "label/region.NAME": 40},
    }


def _args(tmp_path, **kw):
    base = {
        "workspace": "ws",
        "dataset_name": "d",
        "out": str(tmp_path / "out"),
        "dashboard": [],
        "snapshot_in": None,
        "snapshot_out": None,
        "langfuse_out": None,
        "id_prefix": "",
        "no_phrase": True,
        "phrase_model": "gpt-4o",
        "no_viz_type": False,
        "min_questions": 1,
        "min_shapes": 1,
        "min_filtered": 0,
        "enrich_ranked": 0,
        "skip_ambiguous": False,
        "dry_run": False,
    }
    return SimpleNamespace(**{**base, **kw})


def _snapshot_file(tmp_path, snapshot):
    path = tmp_path / "snap.json"
    path.write_text(json.dumps(snapshot))
    return str(path)


def test_generate_writes_a_validated_item_per_insight(tmp_path):
    snapshot = _snapshot(_bar("spend", "merchant.NAME"), _bar("revenue", "region.NAME"))
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, snapshot))

    assert generate(args) == 0

    written = sorted(p.name for p in (tmp_path / "out").glob("*.json"))
    assert len(written) == 2
    for path in (tmp_path / "out").glob("*.json"):
        assert _validation_errors(json.loads(path.read_text())) is None


def test_generate_fails_the_run_when_too_few_insights_survive(tmp_path):
    # The gate exists so a thin workspace fails loudly instead of quietly shipping a
    # dataset too small to mean anything.
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, _snapshot(_bar("spend", "merchant.NAME"))))
    args.min_questions = 15

    assert generate(args) == 1
    assert list((tmp_path / "out").glob("*.json")), "the items are still written; only the exit code fails"


def test_generate_skips_hidden_insights(tmp_path):
    # Hidden objects are invisible to the assistant's catalog search, so a question about
    # one is unwinnable rather than merely hard.
    hidden = _bar("spend", "merchant.NAME")
    hidden["isHidden"] = True
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, _snapshot(hidden, _bar("revenue", "region.NAME"))))

    assert generate(args) == 0
    assert len(list((tmp_path / "out").glob("*.json"))) == 1


def test_generate_dry_run_writes_nothing(tmp_path):
    args = _args(
        tmp_path, snapshot_in=_snapshot_file(tmp_path, _snapshot(_bar("spend", "merchant.NAME"))), dry_run=True
    )

    assert generate(args) == 0
    assert not (tmp_path / "out").exists()


def test_generate_exports_a_langfuse_dataset_with_prefixed_ids(tmp_path):
    args = _args(
        tmp_path,
        snapshot_in=_snapshot_file(tmp_path, _snapshot(_bar("spend", "merchant.NAME"))),
        langfuse_out=str(tmp_path / "lf.json"),
        id_prefix="lr-",
    )
    assert generate(args) == 0

    payload = json.loads((tmp_path / "lf.json").read_text())
    assert payload["workspace"] == "ws"
    assert all(item["id"].startswith("lr-") for item in payload["items"])


def test_generate_derives_ranked_items_and_records_their_provenance(tmp_path):
    args = _args(
        tmp_path,
        snapshot_in=_snapshot_file(tmp_path, _snapshot(_bar("spend", "merchant.NAME"))),
        enrich_ranked=2,
    )
    assert generate(args) == 0

    items = [json.loads(p.read_text()) for p in (tmp_path / "out").glob("*.json")]
    derived = [i for i in items if i.get("derived_from")]
    assert len(derived) == 2
    assert {i["derived_kind"] for i in derived} == {"ranking_filter", "sort_by"}


def test_generate_can_drop_the_items_that_name_something_ambiguous(tmp_path):
    snapshot = _snapshot(_bar("spend", "merchant.NAME"), _bar("revenue", "region.NAME"))
    snapshot["display_names"]["label/other.NAME"] = "Merchant Name"  # a second "Merchant Name"
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, snapshot), skip_ambiguous=True)

    assert generate(args) == 0
    kept = [json.loads(p.read_text())["question"] for p in (tmp_path / "out").glob("*.json")]
    assert len(kept) == 1, "the item naming the duplicated label is dropped"


def test_generate_restricts_to_the_requested_dashboard(tmp_path):
    keep, drop = _bar("spend", "merchant.NAME"), _bar("revenue", "region.NAME")
    keep["id"], drop["id"] = "v_keep", "v_drop"
    snapshot = _snapshot(keep, drop)
    snapshot["analytics"]["analyticalDashboards"] = [
        {"id": "dash", "content": {"layout": [{"type": "insight", "insight": {"identifier": {"id": "v_keep"}}}]}}
    ]
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, snapshot), dashboard=["dash"])

    assert generate(args) == 0
    assert len(list((tmp_path / "out").glob("*.json"))) == 1


def test_generate_reports_an_unknown_dashboard_instead_of_generating_everything(tmp_path):
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, _snapshot(_bar("spend", "merchant.NAME"))))
    args.dashboard = ["nope"]

    assert generate(args) == 1
    assert not (tmp_path / "out").exists()


def test_generate_saves_the_fetched_snapshot_for_replay(tmp_path):
    class _Sdk:
        pass

    calls = {}

    def fake_fetch(sdk, workspace_id):
        calls["workspace"] = workspace_id
        return _snapshot(_bar("spend", "merchant.NAME"))

    args = _args(tmp_path, snapshot_out=str(tmp_path / "snap-out.json"))
    with patch.object(from_insights_mod, "fetch_snapshot", fake_fetch):
        assert generate(args, sdk_factory=_Sdk) == 0

    assert calls["workspace"] == "ws"
    assert json.loads((tmp_path / "snap-out.json").read_text())["workspace_id"] == "ws"


def test_generate_without_a_snapshot_or_an_sdk_says_which_is_missing(tmp_path):
    with pytest.raises(ValueError, match="snapshot-in"):
        generate(_args(tmp_path))


def test_generate_blanks_every_expected_chart_type_on_request(tmp_path):
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, _snapshot(_bar("spend", "merchant.NAME"))))
    args.no_viz_type = True
    assert generate(args) == 0

    items = [json.loads(p.read_text()) for p in (tmp_path / "out").glob("*.json")]
    assert all(i["expected_output"]["visualization"]["type"] == "" for i in items)


# --- the phrasing step --------------------------------------------------------


def _reply(text):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=text))])


def _fake_openai(*replies):
    """An OpenAI stub returning `replies` in order, recording the prompts it received."""
    sent = []

    class _Completions:
        def create(self, model, messages):
            sent.append(messages)
            return replies[min(len(sent) - 1, len(replies) - 1)]

    class _Client:
        chat = SimpleNamespace(completions=_Completions())

    return _Client, sent


def _phrase(specs, *replies):
    client_cls, sent = _fake_openai(*replies)
    with (
        patch("openai.OpenAI", client_cls),
        patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}),
    ):
        return from_insights_mod.phrase(specs, "gpt-4o", DISPLAY), sent


def test_phrase_returns_a_question_the_spec_agrees_with():
    spec = convert(spend_by_merchant(), DATE_IDS)
    (questions, sent) = _phrase([spec], _reply('"Show me Spend Amount by Merchant Name"'))

    assert questions == ["Show me Spend Amount by Merchant Name"], "surrounding quotes are stripped"
    assert len(sent) == 1, "a clean question is not re-asked"


def test_phrase_feeds_a_contradiction_back_once_and_keeps_the_rewrite():
    spec = convert(spend_by_merchant(), DATE_IDS)
    (questions, sent) = _phrase(
        [spec],
        _reply("Show me the top 5 Merchant Name by Spend Amount"),  # ranking the spec lacks
        _reply("Show me Spend Amount by Merchant Name"),
    )

    assert questions == ["Show me Spend Amount by Merchant Name"]
    assert len(sent) == 2
    assert "ranking word" in sent[1][-1]["content"], "the specific contradiction is quoted back"


def test_phrase_drops_an_item_the_writer_keeps_contradicting():
    # Shipping a question its own expected_output disagrees with is worse than shipping
    # fewer questions, so the second failure drops the item.
    spec = convert(spend_by_merchant(), DATE_IDS)
    (questions, sent) = _phrase([spec], _reply("Show me the top 5 Merchant Name by Spend Amount"))

    assert questions == [None]
    assert len(sent) == 2, "one retry, then give up"


def test_phrase_treats_a_refusal_with_no_text_as_a_failed_attempt():
    # `message.content` is None for a refusal; .strip() on it used to crash the run.
    spec = convert(spend_by_merchant(), DATE_IDS)
    (questions, _) = _phrase([spec], _reply(None))
    assert questions == [None]


def test_phrase_requires_the_api_key_rather_than_failing_per_item():
    spec = convert(spend_by_merchant(), DATE_IDS)
    client_cls, _ = _fake_openai(_reply("x"))
    with (
        patch("openai.OpenAI", client_cls),
        patch.dict("os.environ", {}, clear=True),
        pytest.raises(OSError, match="OPENAI_API_KEY"),
    ):
        from_insights_mod.phrase([spec], "gpt-4o", DISPLAY)


def test_generate_uses_the_phrasing_step_when_it_is_not_disabled(tmp_path):
    args = _args(tmp_path, snapshot_in=_snapshot_file(tmp_path, _snapshot(_bar("spend", "merchant.NAME"))))
    args.no_phrase = False
    client_cls, sent = _fake_openai(_reply("Show me Spend Amount by Merchant Name"))

    with patch("openai.OpenAI", client_cls), patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
        assert generate(args) == 0

    assert sent, "the LLM was asked"
    written = [json.loads(p.read_text()) for p in (tmp_path / "out").glob("*.json")]
    assert written[0]["question"] == "Show me Spend Amount by Merchant Name"
