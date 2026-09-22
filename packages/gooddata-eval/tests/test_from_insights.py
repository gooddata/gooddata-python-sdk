# (C) 2026 GoodData Corporation
import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from gooddata_eval.core.dataset import from_insights as from_insights_mod
from gooddata_eval.core.dataset.from_insights import (
    Unsupported,
    _rules_for,
    _validation_errors,
    aliases,
    ambiguous_fields,
    ambiguous_titles,
    build,
    build_display_names,
    contradictions,
    convert,
    describe,
    display_name,
    generate,
    granularity_phrase,
    insight_ids_on,
    langfuse_payload,
    list_ids,
    mint_id,
    resolve_type,
)
from gooddata_eval.core.dataset.local import load_local_dataset
from gooddata_eval.core.scoring import (
    check_filters,
    get_metric_uri_set,
    resolve_alias_to_uri,
    validate_cross_references,
)

DATE_IDS = {"process_date"}


def uris(spec, *buckets):
    """Resolved URIs of the given buckets; aliases are the platform's local ids and carry no meaning."""
    return sorted(resolve_alias_to_uri(a, spec.query.fields) for b in buckets for a in aliases(getattr(spec, b)))


def viz(url, buckets, filters=(), sorts=(), **kw):
    content = {"visualizationUrl": url, "buckets": buckets, "filters": list(filters), "sorts": list(sorts)}
    if "properties" in kw:
        content["properties"] = kw.pop("properties")
    return {"id": "v_x", "title": kw.pop("title", "X"), "content": content, **kw}


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


def test_relative_date_granularity_is_normalized():
    spec = convert(
        viz(
            "local:headline",
            [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
            filters=[
                {
                    "relativeDateFilter": {
                        "dataSet": {"identifier": {"id": "process_date", "type": "dataset"}},
                        "granularity": "GDC.time.quarter",
                        "from": -1,
                        "to": -1,
                    }
                }
            ],
        ),
    )
    assert spec.query.filter_by["f0"] == {
        "type": "date_filter",
        "using": "dataset/process_date",
        "granularity": "QUARTER",
        "from": -1,
        "to": -1,
    }


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("GDC.time.month_in_year", "MONTH_OF_YEAR"), ("GDC.time.date", "DAY"), ("GDC.time.week_us", "WEEK")],
)
def test_cyclical_and_aliased_granularities_map_to_the_platform_enum(raw, expected):
    """Stripping the prefix and upper-casing gives MONTH_IN_YEAR/DATE, which score zero."""
    spec = convert(
        viz(
            "local:headline",
            [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
            filters=[
                {
                    "relativeDateFilter": {
                        "dataSet": {"identifier": {"id": "process_date", "type": "dataset"}},
                        "granularity": raw,
                        "from": -1,
                        "to": -1,
                    }
                }
            ],
        ),
    )
    assert spec.query.filter_by["f0"]["granularity"] == expected


def test_an_unknown_granularity_is_skipped_not_guessed():
    with pytest.raises(Unsupported, match="fortnight"):
        convert(
            viz(
                "local:headline",
                [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
                filters=[
                    {
                        "relativeDateFilter": {
                            "dataSet": {"identifier": {"id": "process_date", "type": "dataset"}},
                            "granularity": "GDC.time.fortnight",
                            "from": -1,
                            "to": -1,
                        }
                    }
                ],
            ),
        )


def test_fact_measure_carries_its_aggregation():
    spec = convert(
        viz(
            "local:headline",
            [{"localIdentifier": "measures", "items": [measure("m", "amount", "fact", aggregation="sum")]}],
        ),
    )
    field = spec.query.fields["m"]
    assert (field.using, field.aggregation) == ("fact/amount", "SUM")


@pytest.mark.parametrize(
    "bad,reason",
    [
        (
            {
                "measure": {
                    "localIdentifier": "m",
                    "definition": {"arithmeticMeasure": {"operator": "SUM", "measureIdentifiers": ["x", "y"]}},
                }
            },
            "cannot compare",
        ),
        (
            {
                "measure": {
                    "localIdentifier": "m",
                    "definition": {
                        "measureDefinition": {
                            "item": {"identifier": {"type": "metric", "id": "x"}},
                            "filters": [
                                {
                                    "positiveAttributeFilter": {
                                        "displayForm": {"identifier": {"id": "r.NAME", "type": "label"}},
                                        "in": {"values": ["EU"]},
                                    }
                                }
                            ],
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
        convert(viz("local:headline", [{"localIdentifier": "measures", "items": [bad]}]))


def test_uri_form_attribute_filter_is_skipped_rather_than_guessed():
    with pytest.raises(Unsupported, match="not given by value"):
        convert(
            viz(
                "local:bar",
                [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
                filters=[
                    {
                        "positiveAttributeFilter": {
                            "displayForm": {"identifier": {"id": "region", "type": "label"}},
                            "in": {"uris": ["/obj/1?id=2"]},
                        }
                    }
                ],
            ),
        )


def test_a_pushpin_maps_size_and_colour_to_metrics():
    """Real bucket set from a pushpin insight: no `measures` bucket, the metrics are here."""
    spec = convert(
        viz(
            "local:pushpin",
            [
                {"localIdentifier": "size", "items": [measure("s", "orders")]},
                {"localIdentifier": "color", "items": [measure("c", "spend")]},
                {"localIdentifier": "segment", "items": [attribute("a", "country.NAME")]},
            ],
            properties={"controls": {"latitude": "geo.lat", "longitude": "geo.lon"}},
        ),
    )
    assert uris(spec, "metrics") == ["metric/orders", "metric/spend"]
    assert uris(spec, "segment_by") == ["label/country.NAME"]


def test_a_bubbles_size_measure_is_kept_in_its_own_bucket():
    """AAC puts bubble size beside the dimensions (`segment_by`/`size_by`), not with x and y."""
    spec = convert(
        viz(
            "local:bubble",
            [
                {"localIdentifier": "measures", "items": [measure("m", "price")]},
                {"localIdentifier": "secondary_measures", "items": [measure("s", "volume")]},
                {"localIdentifier": "tertiary_measures", "items": [measure("t", "profit")]},
                {"localIdentifier": "view", "items": [attribute("a", "brand.NAME")]},
            ],
        ),
    )
    assert uris(spec, "metrics") == ["metric/price", "metric/volume"]
    assert uris(spec, "segment_by") == ["metric/profit"]


def test_a_sankeys_two_ends_are_dimensions():
    spec = convert(
        viz(
            "local:sankey",
            [
                {"localIdentifier": "measures", "items": [measure("m", "orders")]},
                {"localIdentifier": "attribute_from", "items": [attribute("a", "customer.NAME")]},
                {"localIdentifier": "attribute_to", "items": [attribute("b", "product.NAME")]},
            ],
        ),
    )
    assert uris(spec, "metrics") == ["metric/orders"]
    assert uris(spec, "view_by", "segment_by") == ["label/customer.NAME", "label/product.NAME"]


def test_a_maps_location_bucket_is_skipped_not_broken_down_by():
    """`city_pushpin_latitude` is a rendering label, not a breakdown anyone asks for."""
    with pytest.raises(Unsupported, match="unknown bucket 'location'"):
        convert(
            viz(
                "local:pushpin",
                [
                    {"localIdentifier": "measures", "items": [measure("m", "orders")]},
                    {"localIdentifier": "location", "items": [attribute("a", "geo.city_pushpin_latitude")]},
                ],
            ),
        )


def test_a_count_over_an_attribute_is_a_metric_the_scorer_can_compare():
    """`COUNT(attribute/x)` is an ad-hoc metric, unlike a repeater's bare label column."""
    spec = convert(
        viz(
            "local:headline",
            [
                {
                    "localIdentifier": "measures",
                    "items": [
                        {
                            "measure": {
                                "localIdentifier": "m",
                                "definition": {
                                    "measureDefinition": {
                                        "item": {"identifier": {"type": "attribute", "id": "visit_id"}},
                                        "aggregation": "count",
                                    }
                                },
                            }
                        }
                    ],
                }
            ],
        ),
    )
    assert uris(spec, "metrics") == ["attribute/visit_id"]
    assert spec.query.fields["m"].aggregation == "COUNT"


def test_treemap_is_mapped_not_dropped():
    spec = convert(viz("local:treemap", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]))
    assert spec.type == "treemap_chart"


def test_unmapped_viz_url_fails_loudly():
    with pytest.raises(Unsupported, match="no spec for visualizationUrl"):
        convert(viz("local:brandnew", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]))


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
                        "dataSet": {"identifier": {"id": "process_date", "type": "dataset"}},
                        "from": "2025-01-01",
                        "to": "2025-12-31",
                    }
                },
                {
                    "rankingFilter": {
                        "measure": {"localIdentifier": "m"},
                        "attributes": [{"localIdentifier": "a"}],
                        "operator": "TOP",
                        "value": 5,
                    }
                },
            ]
        ),
    )
    brief = describe(spec, DISPLAY)
    assert "date range 2025-01-01 to 2025-12-31 on Process Date" in brief
    assert "top 5 by Spend Amount, ranked within Merchant Name" in brief
    assert "{" not in brief


def test_contradictions_flag_ranking_and_filter_language_the_spec_lacks():
    plain = convert(spend_by_merchant())
    assert contradictions("Which merchants drove the most spend?", plain)
    assert contradictions("Show spend by merchant for last quarter", plain)
    assert contradictions("How does spend break down across merchants?", plain) == []

    ranked = convert(
        spend_by_merchant(
            filters=[{"rankingFilter": {"measure": {"localIdentifier": "m"}, "operator": "TOP", "value": 5}}]
        ),
    )
    assert contradictions("What are the top 5 merchants by spend?", ranked) == []


def test_type_is_kept_only_when_the_question_names_the_chart_form():
    spec = convert(spend_by_merchant())
    assert resolve_type(spec, "Show me spend by merchant as a bar chart") == "bar_chart"
    assert resolve_type(spec, "Which merchants did we spend the most with?") == ""


def test_build_blanks_type_for_a_question_that_names_no_chart_form():

    spec = convert(spend_by_merchant())
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
    headline = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]))
    assert contradictions("Can you show me Spend Amount by Spend Amount?", headline, DISPLAY)
    assert contradictions("Can you show me Spend Amount broken down by Spend Amount?", headline, DISPLAY)
    assert contradictions("Can you show me Spend Amount?", headline, DISPLAY) == []


def test_unsubstituted_placeholder_is_a_hard_error():
    headline = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]))
    for bad in (
        "Can you show me Spend Amount by breakdown dimension?",
        "Can you show me Spend Amount by {dimension}?",
        "Can you show me Spend Amount by <split dimension>?",
    ):
        assert contradictions(bad, headline, DISPLAY), bad


def test_breakdown_promised_but_not_expected():
    headline = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]))
    assert contradictions("Can you show me Spend Amount by Merchant Name?", headline, DISPLAY)
    # Explicit negation is legitimate phrasing, not a contradiction.
    for ok in (
        "Can you show me Spend Amount with no breakdown?",
        "Can you show me Spend Amount without breaking it down by any dimension?",
    ):
        assert contradictions(ok, headline, DISPLAY) == [], ok


def test_breakdown_expected_but_not_asked_is_the_same_severity():
    spec = convert(spend_by_merchant())
    assert contradictions("Can you show me Spend Amount?", spec, DISPLAY)
    assert contradictions("Can you show me Spend Amount by Merchant Name?", spec, DISPLAY) == []
    # Plurals and reordering still count as naming the dimension.
    assert contradictions("How does Spend Amount break down across merchants?", spec, DISPLAY) == []


def test_ranking_phrasing_without_a_dimension_is_not_a_false_breakdown():
    ranked = convert(
        viz(
            "local:headline",
            [{"localIdentifier": "measures", "items": [measure("m", "spend")]}],
            filters=[{"rankingFilter": {"measure": {"localIdentifier": "m"}, "operator": "TOP", "value": 5}}],
        ),
    )
    assert contradictions("What is the top 5 by Spend Amount?", ranked, DISPLAY) == []


def test_every_reported_malformed_question_is_caught():
    """The 7 real failures from the gpt-5.4 run over the Loop workspace."""
    headline = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]))
    names = {"metric/spend": "Variant Exchange Ratio"}
    for bad in (
        "Can you show me Variant Exchange Ratio broken down by Variant Exchange Ratio?",
        "Can you show me the Variant Exchange Ratio by Variant Exchange Ratio?",
        "Can you show me Variant Exchange Ratio by breakdown dimension?",
    ):
        assert contradictions(bad, headline, names), bad
    assert contradictions("Can you show me Variant Exchange Ratio?", headline, names) == []


# --- AD's "All" filters and the singular ranking form -----------------------


def test_dropped_noop_filter_does_not_leave_a_gap_in_filter_keys():
    spec = convert(
        spend_by_merchant(
            filters=[
                {
                    "negativeAttributeFilter": {
                        "displayForm": {"identifier": {"id": "x", "type": "label"}},
                        "notIn": {"values": []},
                    }
                },
                {
                    "positiveAttributeFilter": {
                        "displayForm": {"identifier": {"id": "region", "type": "label"}},
                        "in": {"values": ["EMEA"]},
                    }
                },
            ]
        ),
    )
    assert list(spec.query.filter_by) == ["f0"]


def test_uri_form_attribute_filter_is_still_skipped():
    """The guard the empty-values case was wrongly sharing: uris can't become literals."""
    with pytest.raises(Unsupported, match="not given by value"):
        convert(
            spend_by_merchant(
                filters=[
                    {
                        "negativeAttributeFilter": {
                            "displayForm": {"identifier": {"id": "x", "type": "label"}},
                            "notIn": {"uris": ["/obj/1"]},
                        }
                    }
                ]
            ),
        )


def _bar(metric_id, label_id, **kw):
    return viz(
        "local:bar",
        [
            {"localIdentifier": "measures", "items": [measure("m", metric_id)]},
            {"localIdentifier": "view", "items": [attribute("a", label_id)]},
        ],
        **kw,
    )


def test_a_ranking_over_two_dimensions_names_neither_as_the_ranked_one():
    """No `attribute` means the filter ranks (state, city) pairs, not states within cities."""
    spec = convert(
        viz(
            "local:bar",
            [
                {"localIdentifier": "measures", "items": [measure("m", "orders")]},
                {"localIdentifier": "view", "items": [attribute("a", "state.NAME")]},
                {"localIdentifier": "stack", "items": [attribute("b", "city.NAME")]},
            ],
            filters=[{"rankingFilter": {"measure": {"localIdentifier": "m"}, "operator": "TOP", "value": 5}}],
        ),
    )
    rules = _rules_for(spec, {})
    assert "top 5 rows of" not in rules, "that shorthand asserts a single-dimension scope the filter lacks"
    assert "broken down by" in rules


def test_a_ranking_within_an_attribute_still_asks_for_the_breakdown():
    # `ranked within <attribute>` ranks inside each group, so the breakdown is real and
    # the question has to name it.
    spec = convert(spend_by_merchant())
    spec.query.filter_by["f0"] = {
        "type": "ranking_filter",
        "using": "m_spend",
        "attribute": "d_merchant_name",
        "top": 3,
    }
    assert "- Say the question is broken down by" in _rules_for(spec, DISPLAY)


def test_a_question_asking_for_one_number_must_ask_to_see_it():
    # A bare "What is the Upsell Ratio?" reads as a request for a definition, and the
    # agent answers in prose: seven of loop's headline items failed with no chart built.
    spec = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "spend")]}]))
    rules = _rules_for(spec, DISPLAY)
    assert "AS A CHART" in rules
    assert "as a single number" in rules
    assert "Never a bare 'What is <metric>?'" in rules
    assert "Do not name the chart type" not in rules, "a single number needs its form named"


def test_a_broken_down_question_is_not_told_to_name_a_chart_form():
    assert "AS A CHART" not in _rules_for(convert(spend_by_merchant()), DISPLAY)


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
    spec = convert(_bar("spend", "merchant.NAME"))
    names = {**DISPLAY, "label/other_dataset.NAME": "Merchant Name"}
    assert ambiguous_fields(spec, names) == ["Merchant Name"]
    assert ambiguous_fields(spec, DISPLAY) == []


def test_an_ambiguous_metric_name_counts_too():
    spec = convert(_bar("spend", "merchant.NAME"))
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
    spec = convert(_monthly())
    brief = describe(spec, DISPLAY)
    assert "broken down by: Process Date, by month, one point per calendar month over time" in brief
    assert "Process Date - Month" not in brief, "a label id in prose is not what an analyst says"


def test_a_date_breakdown_is_not_asked_for_verbatim():
    rules = _rules_for(convert(_monthly()), DISPLAY)
    assert "natural words" in rules
    assert "never as a label name" in rules
    assert "naming each verbatim" not in rules


def test_a_plain_dimension_is_still_asked_for_verbatim():
    rules = _rules_for(convert(spend_by_merchant()), DISPLAY)
    assert "broken down by Merchant Name, naming each verbatim" in rules
    assert "natural words" not in rules


def test_a_question_saying_by_month_still_names_the_dimension():
    spec = convert(_monthly())
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
    )
    names = {
        "metric/total_labels": "Total Labels",
        "dataset/most_recent_label_created_at": "Most Recent Label Created At",
        "label/most_recent_label_created_at.month": "Most Recent Label Created At - Month",
    }
    question = "Can you show me Total Labels by month for Most Recent Label Created At?"
    assert contradictions(question, spec, names) == []


def test_a_real_ranking_claim_is_still_caught_around_the_names():
    spec = convert(spend_by_merchant())
    problems = contradictions("Show me the top 5 Merchant Name values by Spend Amount", spec, DISPLAY)
    assert any("ranking word" in p for p in problems)


def test_a_filter_word_inside_a_field_name_is_not_a_claim():
    spec = convert(spend_by_merchant())
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
        "min_filtered": 0,
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
    spec = convert(spend_by_merchant())
    (questions, sent) = _phrase([spec], _reply('"Show me Spend Amount by Merchant Name"'))

    assert questions == ["Show me Spend Amount by Merchant Name"], "surrounding quotes are stripped"
    assert len(sent) == 1, "a clean question is not re-asked"


def test_phrase_feeds_a_contradiction_back_once_and_keeps_the_rewrite():
    spec = convert(spend_by_merchant())
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
    spec = convert(spend_by_merchant())
    (questions, sent) = _phrase([spec], _reply("Show me the top 5 Merchant Name by Spend Amount"))

    assert questions == [None]
    assert len(sent) == 2, "one retry, then give up"


def test_phrase_treats_a_refusal_with_no_text_as_a_failed_attempt():
    # `message.content` is None for a refusal; .strip() on it used to crash the run.
    spec = convert(spend_by_merchant())
    (questions, _) = _phrase([spec], _reply(None))
    assert questions == [None]


def test_phrase_requires_the_api_key_rather_than_failing_per_item():
    spec = convert(spend_by_merchant())
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


def test_headline_converts_to_scorable_single_metric_spec():
    spec = convert(viz("local:headline", [{"localIdentifier": "measures", "items": [measure("m", "gross_revenue")]}]))
    assert spec.type == "headline_chart"
    # The alias is arbitrary; what must survive is the URI gd-eval scores on.
    assert get_metric_uri_set(spec) == {"metric/gross_revenue"}


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
                        "dataSet": {"identifier": {"id": "process_date", "type": "dataset"}},
                        "from": "2025-01-01",
                        "to": "2025-12-31",
                    }
                },
                {
                    "positiveAttributeFilter": {
                        "displayForm": {"identifier": {"id": "region", "type": "label"}},
                        "in": {"values": ["EMEA"]},
                    }
                },
                {
                    "rankingFilter": {
                        "measure": {"localIdentifier": "m"},
                        "attributes": [{"localIdentifier": "a"}],
                        "operator": "TOP",
                        "value": 5,
                    }
                },
            ],
        ),
    )
    # Ranking-filter aliases must resolve to metric/ and label/ URIs or gd-eval rejects them.
    assert validate_cross_references(spec) == (True, [])
    assert check_filters(spec, spec).all_ok


def test_a_real_sort_or_ranking_legitimises_a_ranking_title():
    sorted_spec = convert(
        spend_by_merchant(
            title="Merchants, Most Spend First",
            sorts=[{"attributeSortItem": {"attributeIdentifier": "a", "direction": "asc"}}],
        ),
    )
    assert sorted_spec.query.sort_by == [{"type": "attribute_sort", "by": "a", "direction": "ASC"}]


@pytest.mark.parametrize(
    "noop",
    [
        {
            "negativeAttributeFilter": {
                "displayForm": {"identifier": {"id": "product_name", "type": "label"}},
                "notIn": {"values": []},
            }
        },
        {
            "positiveAttributeFilter": {
                "displayForm": {"identifier": {"id": "product_name", "type": "label"}},
                "in": {"values": []},
            }
        },
        {
            "relativeDateFilter": {
                "dataSet": {"identifier": {"id": "process_date", "type": "dataset"}},
                "granularity": "GDC.time.month",
            }
        },
    ],
)
def test_all_selection_filters_are_dropped_not_fatal(noop):
    """AD writes an unset filter as an empty exclusion or an all-time window.

    It restricts nothing, so it must not appear in the spec -- and must not cost the
    insight, which is otherwise perfectly expressible.
    """
    spec = convert(spend_by_merchant(filters=[noop]))
    assert spec.query.filter_by == {}
