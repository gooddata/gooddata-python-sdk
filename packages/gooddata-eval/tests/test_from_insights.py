# (C) 2026 GoodData Corporation
import json

import pytest
from gooddata_eval.core.dataset.from_insights import (
    Unsupported,
    _rules_for,
    _validation_errors,
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
    insight_ids_on,
    langfuse_payload,
    list_ids,
    mint_id,
    pick_derived,
    rankable,
    resolve_type,
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
