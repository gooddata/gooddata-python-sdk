# (C) 2026 GoodData Corporation
"""Resolving the catalog objects a visualization points at."""

from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.validation.references import (
    CatalogReference,
    extract_catalog_references,
    resolve_references,
)


def _measure(local_id: str, metric_id: str) -> dict[str, Any]:
    return {
        "measure": {
            "localIdentifier": local_id,
            "definition": {"measureDefinition": {"item": {"identifier": {"id": metric_id, "type": "metric"}}}},
        }
    }


def _content(metric_id: str = "revenue", label_id: str = "label.region") -> dict[str, Any]:
    return {
        "version": "2",
        "visualizationUrl": "local:column",
        "buckets": [
            {"localIdentifier": "measures", "items": [_measure("m1", metric_id)]},
            {
                "localIdentifier": "view",
                "items": [
                    {
                        "attribute": {
                            "localIdentifier": "a1",
                            "displayForm": {"identifier": {"id": label_id, "type": "label"}},
                        }
                    }
                ],
            },
        ],
        "filters": [],
        "sorts": [],
    }


class TestExtraction:
    def test_every_identifier_node_is_found_with_its_path(self):
        refs = extract_catalog_references(_content())
        assert {(r.type, r.id) for r in refs} == {("metric", "revenue"), ("label", "label.region")}
        assert refs[0].location.startswith("content.buckets[0].items[0].measure")

    def test_identifiers_are_found_wherever_they_appear(self):
        """The walk is deliberately not a list of known positions: the format keeps gaining
        new places to put one (layers, parameters, conditional formatting)."""
        refs = extract_catalog_references(
            {"something": {"brand": {"new": {"identifier": {"id": "x", "type": "metric"}}}}}
        )
        assert [(r.type, r.id) for r in refs] == [("metric", "x")]

    def test_a_date_filter_dataset_is_a_reference(self):
        content = {
            "filters": [
                {
                    "absoluteDateFilter": {
                        "dataSet": {"identifier": {"id": "dt", "type": "dataset"}},
                        "from": "a",
                        "to": "b",
                    }
                }
            ]
        }
        assert [(r.type, r.id) for r in extract_catalog_references(content)] == [("dataset", "dt")]

    def test_a_malformed_identifier_is_ignored_rather_than_reported(self):
        assert extract_catalog_references({"identifier": {"id": 7}}) == []
        assert extract_catalog_references({"identifier": "not-an-object"}) == []

    def test_obj_id_is_the_type_slash_id_form_the_catalog_uses(self):
        assert CatalogReference(type="metric", id="rev", location="x").obj_id == "metric/rev"


class TestResolution:
    def test_everything_present_resolves(self):
        findings, resolution = resolve_references(
            extract_catalog_references(_content()),
            effective_ids={"metric/revenue", "label/label.region"},
        )
        assert findings == []
        assert resolution.resolved_count == 2
        assert resolution.unresolved == []

    def test_a_missing_object_is_an_error_naming_where_it_was_used(self):
        findings, resolution = resolve_references(
            extract_catalog_references(_content(metric_id="ghost")),
            effective_ids={"label/label.region"},
            object_id="v1",
        )
        assert [f.code for f in findings] == ["unresolved_reference"]
        assert findings[0].object_id == "v1"
        assert "metric/ghost" in findings[0].message
        assert findings[0].location.endswith(".identifier")
        assert [r.obj_id for r in resolution.unresolved] == ["metric/ghost"]

    def test_inherited_objects_resolve_because_the_effective_catalog_includes_them(self):
        """The case that makes or breaks this in a parent/child hierarchy: a child owns
        almost nothing, so resolving against its own objects would fail everything."""
        findings, resolution = resolve_references(
            extract_catalog_references(_content()),
            effective_ids={"metric/revenue", "label/label.region"},  # all from the parent
        )
        assert findings == []
        assert resolution.resolved_count == 2

    def test_reference_types_the_sdk_does_not_model_are_skipped(self):
        """The walk is broad on purpose. An unfamiliar type far more likely means the format
        grew than that the content is broken, so it is not reported as missing."""
        findings, resolution = resolve_references(
            extract_catalog_references({"identifier": {"id": "x", "type": "somethingNew"}}),
            effective_ids=set(),
        )
        assert findings == []
        assert resolution.resolved_count == 0

    def test_the_summary_states_both_counts(self):
        _, resolution = resolve_references(
            extract_catalog_references(_content(metric_id="ghost")),
            effective_ids={"label/label.region"},
        )
        assert resolution.summary() == "1 reference(s) resolved, 1 unresolved"
