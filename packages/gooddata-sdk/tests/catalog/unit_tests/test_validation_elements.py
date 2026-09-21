# (C) 2026 GoodData Corporation
"""Attribute filter values against the data they filter on.

The only check in the package that asks a question about the data rather than the layout,
so most of these tests are about what it declines to ask: elements given by reference, the
NULL element, and empty lists are all left alone rather than guessed at.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.validation.elements import (
    check_filter_element_values,
    collect_filter_values,
)
from gooddata_sdk.catalog.validation.model import Severity


def _positive(label: str, *values: Any) -> dict[str, Any]:
    return {
        "positiveAttributeFilter": {
            "displayForm": {"identifier": {"id": label, "type": "label"}},
            "in": {"values": list(values)},
        }
    }


def _negative(label: str, *values: Any) -> dict[str, Any]:
    return {
        "negativeAttributeFilter": {
            "displayForm": {"identifier": {"id": label, "type": "label"}},
            "notIn": {"values": list(values)},
        }
    }


def _content(*filters: dict[str, Any]) -> dict[str, Any]:
    return {"version": "2", "visualizationUrl": "local:column", "buckets": [], "filters": list(filters)}


def _model(**collections: list[dict[str, Any]]) -> CatalogDeclarativeAnalytics:
    return CatalogDeclarativeAnalytics.from_dict({"analytics": collections}, camel_case=True)


def _viz(object_id: str, *filters: dict[str, Any]) -> dict[str, Any]:
    return {"id": object_id, "title": object_id, "content": _content(*filters)}


class _FakeContent:
    """Stands in for the elements API, recording what it was asked."""

    def __init__(self, existing: dict[str, list[str]], *, fail: set[str] | None = None):
        self._existing = existing
        self._fail = fail or set()
        self.calls: list[tuple[str, str, tuple[str, ...]]] = []

    def get_label_elements(self, workspace_id, label_id, exact_filter=None, limit=None, **_):
        self.calls.append((workspace_id, label_id, tuple(exact_filter or ())))
        if label_id in self._fail:
            raise RuntimeError("no such label")
        return [v for v in (exact_filter or []) if v in self._existing.get(label_id, [])]


class _FakeSdk:
    def __init__(self, content: _FakeContent):
        self.catalog_workspace_content = content


class TestCollecting:
    def test_a_positive_filter_is_collected_with_its_label_and_values(self):
        [found] = collect_filter_values(_content(_positive("region", "EMEA", "APAC")), object_id="v1")
        assert (found.label_id, found.values, found.object_id) == ("region", ("EMEA", "APAC"), "v1")
        assert found.location == "content.filters[0].positiveAttributeFilter.in.values"

    def test_a_negative_filter_is_collected_too(self):
        """Which list it is decides what the filter does with the values, not whether they
        have to exist."""
        [found] = collect_filter_values(_content(_negative("region", "EMEA")), object_id="v1")
        assert found.values == ("EMEA",)
        assert found.location.endswith("negativeAttributeFilter.notIn.values")

    def test_elements_given_by_reference_are_skipped(self):
        """`uris` names primary-label values rather than the titles this resolves, and the
        empty form occurs constantly in stored content."""
        content = _content(
            {"negativeAttributeFilter": {"displayForm": {"identifier": {"id": "r"}}, "notIn": {"uris": []}}}
        )
        assert collect_filter_values(content, object_id="v1") == []

    def test_the_null_element_is_not_a_value_to_look_up(self):
        assert collect_filter_values(_content(_positive("region", None)), object_id="v1") == []

    def test_nulls_are_dropped_but_real_values_beside_them_are_kept(self):
        [found] = collect_filter_values(_content(_positive("region", None, "EMEA")), object_id="v1")
        assert found.values == ("EMEA",)

    def test_an_empty_list_asks_nothing(self):
        assert collect_filter_values(_content(_positive("region")), object_id="v1") == []

    def test_repeated_values_are_asked_once_but_keep_their_order(self):
        [found] = collect_filter_values(_content(_positive("r", "B", "A", "B")), object_id="v1")
        assert found.values == ("B", "A")

    def test_filters_are_found_wherever_they_are_nested(self):
        """Dashboards carry them inside widgets and filter contexts, not in a `filters` list."""
        nested = {"layout": {"sections": [{"items": [{"widget": {"filters": [_positive("region", "EMEA")]}}]}]}}
        [found] = collect_filter_values(nested, object_id="d1")
        assert found.label_id == "region"
        assert "widget" in found.location


class TestCheckingAgainstData:
    def test_a_value_the_data_holds_is_not_reported(self):
        content = _FakeContent({"region": ["EMEA", "APAC"]})
        findings, resolution = check_filter_element_values(
            _FakeSdk(content), "ws", _model(visualizationObjects=[_viz("v1", _positive("region", "EMEA"))])
        )
        assert findings == []
        assert (resolution.labels_queried, resolution.values_checked) == (1, 1)

    def test_a_value_the_data_does_not_hold_is_a_warning(self):
        """Not an error: an overnight load can make this finding disappear without anything
        being edited, so it must not fail a build the way a structural fault does."""
        content = _FakeContent({"region": ["EMEA"]})
        findings, _ = check_filter_element_values(
            _FakeSdk(content), "ws", _model(visualizationObjects=[_viz("v1", _positive("region", "ATLANTIS"))])
        )
        assert [f.code for f in findings] == ["filter_value_not_in_data"]
        assert findings[0].severity is Severity.WARNING
        assert findings[0].object_id == "v1"
        assert "ATLANTIS" in findings[0].message

    def test_only_the_missing_values_are_named(self):
        content = _FakeContent({"region": ["EMEA"]})
        findings, _ = check_filter_element_values(
            _FakeSdk(content),
            "ws",
            _model(visualizationObjects=[_viz("v1", _positive("region", "EMEA", "ATLANTIS"))]),
        )
        assert "ATLANTIS" in findings[0].message
        assert "EMEA" not in findings[0].message

    def test_one_query_serves_every_object_using_the_same_label(self):
        """Twenty charts pinned to the same region cost one SELECT DISTINCT, not twenty."""
        content = _FakeContent({"region": ["EMEA"]})
        model = _model(
            visualizationObjects=[
                _viz("v1", _positive("region", "EMEA")),
                _viz("v2", _positive("region", "EMEA")),
                _viz("v3", _negative("region", "EMEA")),
            ]
        )
        check_filter_element_values(_FakeSdk(content), "ws", model)
        assert len(content.calls) == 1

    def test_each_object_is_reported_separately_even_though_one_query_served_them(self):
        content = _FakeContent({"region": []})
        model = _model(
            visualizationObjects=[_viz("v1", _positive("region", "GONE")), _viz("v2", _positive("region", "GONE"))]
        )
        findings, _ = check_filter_element_values(_FakeSdk(content), "ws", model)
        assert sorted(f.object_id for f in findings) == ["v1", "v2"]

    def test_a_label_that_cannot_be_queried_reports_nothing(self):
        """A missing label is the reference check's finding, not this one's. Reporting it
        here as well would say the same thing twice in different words, and reporting its
        values as missing would be wrong -- nothing was actually answered."""
        content = _FakeContent({}, fail={"region"})
        findings, resolution = check_filter_element_values(
            _FakeSdk(content), "ws", _model(visualizationObjects=[_viz("v1", _positive("region", "EMEA"))])
        )
        assert findings == []
        assert resolution.labels_queried == 0

    def test_a_label_whose_data_is_empty_is_a_finding_not_a_failure(self):
        """The difference from the test above: the server answered, and its answer was no."""
        content = _FakeContent({"region": []})
        findings, resolution = check_filter_element_values(
            _FakeSdk(content), "ws", _model(visualizationObjects=[_viz("v1", _positive("region", "EMEA"))])
        )
        assert [f.code for f in findings] == ["filter_value_not_in_data"]
        assert resolution.labels_queried == 1

    def test_the_query_carries_an_explicit_limit_so_nothing_looks_missing_from_paging(self):
        content = _FakeContent({"region": ["A", "B", "C"]})
        model = _model(visualizationObjects=[_viz("v1", _positive("region", "A", "B", "C"))])
        findings, _ = check_filter_element_values(_FakeSdk(content), "ws", model)
        assert findings == []
        assert content.calls[0][2] == ("A", "B", "C")

    def test_a_filter_naming_more_values_than_one_request_allows_is_split(self):
        values = [f"v{i}" for i in range(1200)]
        content = _FakeContent({"region": values})
        model = _model(visualizationObjects=[_viz("v1", _positive("region", *values))])
        findings, resolution = check_filter_element_values(_FakeSdk(content), "ws", model)
        assert findings == []
        assert len(content.calls) == 3
        assert resolution.values_checked == 1200

    def test_dashboards_and_filter_contexts_are_checked_too(self):
        """Filter contexts are where a dashboard's own filters live, and they are the most
        likely thing to be pinned to a value that later disappears."""
        content = _FakeContent({"region": []})
        model = _model(
            analyticalDashboards=[{"id": "d1", "title": "d", "content": _content(_positive("region", "GONE"))}],
            filterContexts=[{"id": "fc1", "title": "fc", "content": _content(_positive("region", "GONE"))}],
        )
        findings, _ = check_filter_element_values(_FakeSdk(content), "ws", model)
        assert sorted(f.object_id for f in findings) == ["d1", "fc1"]

    def test_an_empty_model_asks_nothing(self):
        content = _FakeContent({})
        findings, resolution = check_filter_element_values(
            _FakeSdk(content), "ws", CatalogDeclarativeAnalytics(analytics=None)
        )
        assert findings == []
        assert content.calls == []
        assert resolution.labels_queried == 0

    def test_a_layout_with_no_attribute_filters_queries_nothing(self):
        """The cost of this check is the queries it makes, so making none when there is
        nothing to ask is the property worth pinning."""
        content = _FakeContent({})
        check_filter_element_values(_FakeSdk(content), "ws", _model(visualizationObjects=[_viz("v1")]))
        assert content.calls == []
