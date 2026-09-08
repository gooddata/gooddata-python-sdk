# (C) 2026 GoodData Corporation
import json

import pytest
from gooddata_eval.core.dataset.from_insights import (
    Unsupported,
    _validation_errors,
    build,
    build_display_names,
    contradictions,
    convert,
    describe,
    display_name,
    insight_ids_on,
    langfuse_payload,
    list_ids,
    mint_id,
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
