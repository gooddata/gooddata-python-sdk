# (C) 2026 GoodData Corporation
"""Reading catalog references out of MAQL.

The expressions here are shaped from real stored metrics: ``BY ALL OTHER``, ``FOR
PREVIOUS``, ``WHERE`` with a quoted element value, and date-attribute ids carrying a
granularity suffix. Nothing here asserts anything about what the MAQL *means* -- only
which objects it names.
"""

from __future__ import annotations

from gooddata_sdk.catalog.validation.maql import extract_maql_references, referenced_metric_ids


def _pairs(maql: str) -> list[tuple[str, str]]:
    return [(r.type, r.id) for r in extract_maql_references(maql)]


class TestExtraction:
    def test_a_simple_ratio_names_both_metrics(self):
        assert _pairs("SELECT {metric/orders} / {metric/sessions}") == [
            ("metric", "orders"),
            ("metric", "sessions"),
        ]

    def test_facts_labels_and_datasets_are_all_found(self):
        maql = "SELECT AVG({fact/amount}) BY ALL OTHER EXCEPT {dataset/dim_calendar}, {label/region}"
        assert set(_pairs(maql)) == {("fact", "amount"), ("dataset", "dim_calendar"), ("label", "region")}

    def test_a_date_attribute_keeps_its_granularity_suffix(self):
        """``process_date.year`` is one object id, not an id and a field: splitting on the
        dot would look for an object that does not exist."""
        assert _pairs("SELECT {metric/x} FOR PREVIOUS({label/process_date.year})") == [
            ("metric", "x"),
            ("label", "process_date.year"),
        ]

    def test_ids_with_hyphens_and_underscores_survive(self):
        assert _pairs("SELECT {metric/approval_rate_-_card_not_present_-_cuta}") == [
            ("metric", "approval_rate_-_card_not_present_-_cuta")
        ]

    def test_repeated_references_are_all_reported(self):
        """A self-ratio names the same metric twice; deduplicating would under-report what
        the expression actually depends on."""
        assert _pairs("SELECT {metric/x} / (SELECT {metric/x} BY ALL OTHER)") == [
            ("metric", "x"),
            ("metric", "x"),
        ]

    def test_the_location_carries_the_offset_so_repeats_are_distinguishable(self):
        refs = extract_maql_references("SELECT {metric/x} / {metric/x}")
        assert refs[0].location != refs[1].location
        assert all(r.location.startswith("content.maql@") for r in refs)

    def test_an_expression_with_no_references_yields_none(self):
        assert extract_maql_references("SELECT 1") == []

    def test_empty_and_non_string_input_is_tolerated(self):
        """Metric content is free-form too: a missing or oddly-typed maql must not raise
        in the middle of validating a layout."""
        assert extract_maql_references("") == []
        assert extract_maql_references(None) == []  # type: ignore[arg-type]
        assert extract_maql_references(42) == []  # type: ignore[arg-type]


class TestQuotedValues:
    def test_a_quoted_element_value_is_not_mistaken_for_a_reference(self):
        maql = 'SELECT COUNT({label/status}) WHERE {label/status} = "{not/a/reference}"'
        assert _pairs(maql) == [("label", "status"), ("label", "status")]

    def test_an_ordinary_quoted_value_changes_nothing(self):
        maql = 'SELECT COUNT({label/pan}) WHERE {label/is_active} = "1" AND {label/is_mdes} = "1"'
        assert _pairs(maql) == [("label", "pan"), ("label", "is_active"), ("label", "is_mdes")]

    def test_offsets_still_point_at_the_original_text(self):
        """Literals are blanked rather than removed, so a reported offset indexes the
        string the user actually has."""
        maql = 'SELECT {metric/a} WHERE {label/x} = "yyyy" AND {label/z} = 1'
        refs = extract_maql_references(maql)
        for ref in refs:
            offset = int(ref.location.split("@")[1])
            assert maql[offset:].startswith("{" + ref.type + "/" + ref.id + "}")


class TestMetricDependencies:
    def test_only_metric_edges_are_returned(self):
        """Cycle detection is a metric-to-metric question; a fact cannot take part in one."""
        maql = "SELECT {metric/a} + {fact/b} + {label/c} - {metric/d}"
        assert referenced_metric_ids(maql) == {"a", "d"}

    def test_a_self_reference_is_visible(self):
        assert referenced_metric_ids("SELECT {metric/self} + 1") == {"self"}

    def test_no_metric_references_gives_an_empty_set(self):
        assert referenced_metric_ids("SELECT SUM({fact/x})") == set()
