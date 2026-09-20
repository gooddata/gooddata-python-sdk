# (C) 2026 GoodData Corporation
"""Checks that need the whole layout: layout references, duplicate ids, metric cycles."""

from __future__ import annotations

from typing import Any

from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.validation.layout import (
    check_duplicate_ids,
    check_layout_references,
    check_metric_cycles,
    layout_object_ids,
    object_references,
    validate_layout,
)


def _viz(object_id: str) -> dict[str, Any]:
    return {
        "id": object_id,
        "title": object_id,
        "content": {
            "version": "2",
            "visualizationUrl": "local:column",
            "buckets": [
                {
                    "localIdentifier": "measures",
                    "items": [
                        {
                            "measure": {
                                "localIdentifier": "m1",
                                "definition": {
                                    "measureDefinition": {"item": {"identifier": {"id": "rev", "type": "metric"}}}
                                },
                            }
                        }
                    ],
                }
            ],
            "filters": [],
            "sorts": [],
        },
    }


def _dashboard(object_id: str, *, insights: tuple[str, ...] = (), filter_context: str | None = None) -> dict[str, Any]:
    """A dashboard shaped like a real one: widgets carry the insight reference, and the
    filter context hangs off the layout rather than off a widget."""
    content: dict[str, Any] = {
        "version": "2",
        "tabs": [
            {
                "sections": [
                    {
                        "items": [
                            {"widget": {"insight": {"identifier": {"id": insight, "type": "visualizationObject"}}}}
                            for insight in insights
                        ]
                    }
                ]
            }
        ],
    }
    if filter_context is not None:
        content["filterContextRef"] = {"identifier": {"id": filter_context, "type": "filterContext"}}
    return {"id": object_id, "title": object_id, "content": content}


def _metric(object_id: str, maql: str) -> dict[str, Any]:
    return {"id": object_id, "title": object_id, "content": {"maql": maql}}


def _model(**collections: list[dict[str, Any]]) -> CatalogDeclarativeAnalytics:
    return CatalogDeclarativeAnalytics.from_dict({"analytics": collections}, camel_case=True)


def _codes(findings: list[Any]) -> list[str]:
    return [f.code for f in findings]


class TestReferenceCollection:
    def test_references_are_gathered_from_every_kind_that_has_them(self):
        model = _model(
            visualizationObjects=[_viz("v1")],
            analyticalDashboards=[_dashboard("d1", insights=("v1",), filter_context="fc1")],
            metrics=[_metric("m1", "SELECT {fact/amount}")],
        )
        by_type = {reference.type for _, reference in object_references(model)}
        assert {"visualizationObject", "filterContext", "fact"} <= by_type

    def test_a_metrics_references_come_out_of_its_maql(self):
        """Metrics keep theirs in a string, so the identifier walk alone would find none."""
        model = _model(metrics=[_metric("m1", "SELECT {metric/other} / {fact/amount}")])
        assert {(r.type, r.id) for _, r in object_references(model)} == {("metric", "other"), ("fact", "amount")}

    def test_layout_object_ids_are_typed(self):
        model = _model(visualizationObjects=[_viz("v1")], filterContexts=[{"id": "fc1", "title": "fc1", "content": {}}])
        assert layout_object_ids(model) == {"visualizationObject/v1", "filterContext/fc1"}

    def test_an_empty_model_yields_nothing(self):
        assert object_references(CatalogDeclarativeAnalytics(analytics=None)) == []
        assert layout_object_ids(CatalogDeclarativeAnalytics(analytics=None)) == set()

    def test_a_geo_charts_position_labels_are_collected_here(self):
        """They live in `properties.controls` as plain strings, so the identifier walk goes
        past them. Collecting them at this one point is what makes them resolve on both
        paths -- against a workspace and against the layout's own logical model -- rather
        than on whichever call site was remembered."""
        geo = {
            "id": "g1",
            "title": "g1",
            "content": {
                "version": "2",
                "visualizationUrl": "local:pushpin",
                "buckets": [
                    {
                        "localIdentifier": "location",
                        "items": [
                            {
                                "attribute": {
                                    "localIdentifier": "loc",
                                    "displayForm": {"identifier": {"id": "city", "type": "label"}},
                                }
                            }
                        ],
                    }
                ],
                "properties": {"controls": {"latitude": "city.lat", "longitude": "city.lon"}},
            },
        }
        found = {
            (object_id, reference.obj_id)
            for object_id, reference in object_references(_model(visualizationObjects=[geo]))
        }
        assert ("g1", "label/city.lat") in found
        assert ("g1", "label/city.lon") in found
        assert ("g1", "label/city") in found


class TestLayoutReferences:
    def test_a_dashboard_whose_visualization_is_present_is_quiet(self):
        model = _model(visualizationObjects=[_viz("v1")], analyticalDashboards=[_dashboard("d1", insights=("v1",))])
        assert check_layout_references(model) == []

    def test_a_dashboard_kept_without_its_visualization_is_reported(self):
        """The half-exported migration: dashboards come across, the objects they render do
        not, and the deploy succeeds because the API validates none of it."""
        model = _model(analyticalDashboards=[_dashboard("d1", insights=("gone",))])
        findings = check_layout_references(model)
        assert _codes(findings) == ["layout_reference_not_in_layout"]
        assert findings[0].object_id == "d1"
        assert "visualizationObject/gone" in findings[0].message

    def test_a_missing_filter_context_is_reported(self):
        model = _model(analyticalDashboards=[_dashboard("d1", filter_context="fc-gone")])
        assert _codes(check_layout_references(model)) == ["layout_reference_not_in_layout"]

    def test_it_is_a_warning_because_the_layout_may_not_be_the_whole_picture(self):
        """A child workspace's layout holds only what the child owns, so a dashboard there
        can legitimately render a visualization inherited from its parent. Only the target
        workspace can settle it, so this cannot be an error."""
        model = _model(analyticalDashboards=[_dashboard("d1", insights=("inherited",))])
        assert check_layout_references(model)[0].severity.value == "warning"

    def test_a_drill_to_a_missing_insight_is_reported(self):
        """Drill targets are not a special case: they carry the same identifier node as the
        widget's own insight, so the tree walk already finds them. This test exists so a
        future refactor that narrows the walk to known positions cannot quietly lose them --
        a drill to a deleted insight is a dead end nobody notices until someone clicks it.
        """
        drilling = {
            "id": "d1",
            "title": "d1",
            "content": {
                "version": "2",
                "tabs": [
                    {
                        "sections": [
                            {
                                "items": [
                                    {
                                        "widget": {
                                            "insight": {"identifier": {"id": "v1", "type": "visualizationObject"}},
                                            "drills": [
                                                {
                                                    "type": "drillToInsight",
                                                    "target": {
                                                        "identifier": {"id": "gone", "type": "visualizationObject"}
                                                    },
                                                }
                                            ],
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ],
            },
        }
        model = _model(visualizationObjects=[_viz("v1")], analyticalDashboards=[drilling])
        findings = check_layout_references(model)
        assert _codes(findings) == ["layout_reference_not_in_layout"]
        assert "visualizationObject/gone" in findings[0].message
        assert findings[0].location.endswith("drills[0].target.identifier")

    def test_catalog_references_are_left_to_the_workspace_check(self):
        """A metric or label is not a layout object; reporting it here would fire on every
        healthy layout, since a layout never contains the catalog."""
        model = _model(metrics=[_metric("m1", "SELECT {fact/amount} + {metric/elsewhere}")])
        assert check_layout_references(model) == []


class TestDuplicateIds:
    def test_two_objects_sharing_an_id_are_reported(self):
        """One file per object named by its id: the second silently overwrites the first on
        the way to disk, and the layout deployed is missing an object nobody deleted."""
        model = _model(metrics=[_metric("m1", "SELECT 1"), _metric("m1", "SELECT 2")])
        findings = check_duplicate_ids(model)
        assert _codes(findings) == ["duplicate_id"]
        assert findings[0].object_id == "m1"

    def test_the_same_id_in_different_collections_is_fine(self):
        """Ids are unique per kind, not globally -- a metric and a visualization may share
        one, and they land in different folders."""
        model = _model(metrics=[_metric("shared", "SELECT 1")], visualizationObjects=[_viz("shared")])
        assert check_duplicate_ids(model) == []

    def test_distinct_ids_are_quiet(self):
        model = _model(metrics=[_metric("a", "SELECT 1"), _metric("b", "SELECT 2")])
        assert check_duplicate_ids(model) == []


class TestMetricCycles:
    def test_a_two_metric_cycle_is_reported(self):
        model = _model(metrics=[_metric("a", "SELECT {metric/b}"), _metric("b", "SELECT {metric/a}")])
        findings = check_metric_cycles(model)
        assert _codes(findings) == ["metric_cycle"]
        assert "a -> b -> a" in findings[0].message or "b -> a -> b" in findings[0].message

    def test_a_metric_referring_to_itself_is_a_cycle(self):
        model = _model(metrics=[_metric("s", "SELECT {metric/s} + 1")])
        assert _codes(check_metric_cycles(model)) == ["metric_cycle"]

    def test_a_longer_chain_is_found(self):
        model = _model(
            metrics=[
                _metric("a", "SELECT {metric/b}"),
                _metric("b", "SELECT {metric/c}"),
                _metric("c", "SELECT {metric/a}"),
            ]
        )
        assert _codes(check_metric_cycles(model)) == ["metric_cycle"]

    def test_a_cycle_is_reported_once_not_once_per_participant(self):
        model = _model(metrics=[_metric("a", "SELECT {metric/b}"), _metric("b", "SELECT {metric/a}")])
        assert len(check_metric_cycles(model)) == 1

    def test_a_deep_acyclic_chain_is_quiet_and_does_not_recurse(self):
        """Thousands of metrics can form a long chain; a recursive walk would raise
        RecursionError somewhere in the middle and say nothing useful."""
        chain = [_metric(f"m{i}", f"SELECT {{metric/m{i + 1}}}") for i in range(2000)]
        chain.append(_metric("m2000", "SELECT 1"))
        assert check_metric_cycles(_model(metrics=chain)) == []

    def test_a_reference_to_a_metric_outside_the_layout_is_not_a_cycle(self):
        model = _model(metrics=[_metric("a", "SELECT {metric/lives_in_the_workspace}")])
        assert check_metric_cycles(model) == []

    def test_a_diamond_is_not_a_cycle(self):
        model = _model(
            metrics=[
                _metric("top", "SELECT {metric/left} + {metric/right}"),
                _metric("left", "SELECT {metric/base}"),
                _metric("right", "SELECT {metric/base}"),
                _metric("base", "SELECT 1"),
            ]
        )
        assert check_metric_cycles(model) == []


class TestValidateLayout:
    def test_every_check_runs(self):
        model = _model(
            metrics=[
                _metric("a", "SELECT {metric/b}"),
                _metric("b", "SELECT {metric/a}"),
                _metric("dup", "SELECT 1"),
                _metric("dup", "SELECT 2"),
            ],
            analyticalDashboards=[_dashboard("d1", insights=("gone",))],
        )
        assert set(_codes(validate_layout(model))) == {"duplicate_id", "layout_reference_not_in_layout", "metric_cycle"}

    def test_a_duplicate_id_shadows_the_earlier_definition_for_cycle_detection(self):
        """Two metrics sharing an id cannot both exist after a round trip through disk, so
        the cycle walk sees only the last one -- exactly what deploying the layout would
        leave behind. The duplicate itself is reported separately."""
        model = _model(
            metrics=[_metric("a", "SELECT {metric/b}"), _metric("b", "SELECT {metric/a}"), _metric("a", "SELECT 1")]
        )
        assert _codes(check_metric_cycles(model)) == []
        assert _codes(check_duplicate_ids(model)) == ["duplicate_id"]

    def test_a_healthy_layout_is_quiet(self):
        model = _model(
            visualizationObjects=[_viz("v1")],
            analyticalDashboards=[_dashboard("d1", insights=("v1",))],
            metrics=[_metric("m1", "SELECT {fact/amount}")],
        )
        assert validate_layout(model) == []
