# (C) 2026 GoodData Corporation
"""Validating a declarative model against a workspace.

The SDK is faked rather than recorded: what these tests are about is which *set* the
references are resolved against, and a fake makes the parent/child distinction the whole
point of the test instead of an artefact of a fixture.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.validation.service import ValidationService


class _FakeObjId:
    def __init__(self, value: str) -> None:
        self._value = value

    def __str__(self) -> str:
        return self._value


class _FakeEntity:
    def __init__(self, obj_id: str) -> None:
        self.obj_id = _FakeObjId(obj_id)


class _FakeCatalog:
    """Stands in for CatalogWorkspaceContent, which exposes each kind as a flat property."""

    def __init__(self, obj_ids: set[str]) -> None:
        by_type: dict[str, list[_FakeEntity]] = {"dataset": [], "metric": [], "attribute": [], "label": [], "fact": []}
        for obj_id in obj_ids:
            by_type[obj_id.split("/", 1)[0]].append(_FakeEntity(obj_id))
        self.datasets = by_type["dataset"]
        self.metrics = by_type["metric"]
        self.attributes = by_type["attribute"]
        self.labels = by_type["label"]
        self.facts = by_type["fact"]


class _FakeSdk:
    """Serves one effective catalog per workspace id, and records what was asked for."""

    def __init__(self, catalogs: dict[str, set[str]]) -> None:
        self._catalogs = catalogs
        self.requested: list[str] = []
        outer = self

        class _Content:
            def get_full_catalog(self, workspace_id: str, inject_valid_objects_func: bool = True) -> _FakeCatalog:
                outer.requested.append(workspace_id)
                return _FakeCatalog(outer._catalogs[workspace_id])

        self.catalog_workspace_content = _Content()


def _model(*metric_ids: str) -> CatalogDeclarativeAnalytics:
    def viz(index: int, metric_id: str) -> dict[str, Any]:
        return {
            "id": f"v{index}",
            "title": f"v{index}",
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
                                        "measureDefinition": {
                                            "item": {"identifier": {"id": metric_id, "type": "metric"}}
                                        }
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

    return CatalogDeclarativeAnalytics.from_dict(
        {"analytics": {"visualizationObjects": [viz(i, m) for i, m in enumerate(metric_ids)]}},
        camel_case=True,
    )


class TestValidateAgainstWorkspace:
    def test_a_model_whose_references_all_exist_passes(self):
        service = ValidationService(_FakeSdk({"ws": {"metric/a", "metric/b"}}))
        result = service.validate_analytics_model("ws", _model("a", "b"))
        assert result.ok
        assert result.objects_checked == 2
        assert result.resolution.resolved_count == 2

    def test_a_reference_the_workspace_cannot_see_is_an_error(self):
        service = ValidationService(_FakeSdk({"ws": {"metric/a"}}))
        result = service.validate_analytics_model("ws", _model("a", "missing"))
        assert not result.ok
        assert [f.object_id for f in result.report.errors] == ["v1"]
        assert result.resolution.resolved_count == 1

    def test_the_same_model_can_pass_for_one_workspace_and_fail_for_another(self):
        """Validity is a property of (object, target), not of the object -- which is why a
        layout has to be checked against where it is going, not where it came from."""
        service = ValidationService(_FakeSdk({"parent": {"metric/a"}, "sibling": set()}))
        model = _model("a")
        assert service.validate_analytics_model("parent", model).ok
        assert not service.validate_analytics_model("sibling", model).ok

    def test_a_child_that_owns_nothing_still_validates_through_inheritance(self):
        """The child's effective catalog carries the parent's objects, so content that owns
        none of what it names is correct and must not be reported."""
        service = ValidationService(_FakeSdk({"child": {"metric/from_parent"}}))
        assert service.validate_analytics_model("child", _model("from_parent")).ok

    def test_structural_findings_are_reported_alongside_reference_ones(self):
        model = _model("a")
        del model.analytics.visualization_objects[0].content["version"]
        result = ValidationService(_FakeSdk({"ws": {"metric/a"}})).validate_analytics_model("ws", model)
        assert sorted(f.code for f in result.report.errors) == ["missing_required_key"]

    def test_the_catalog_is_fetched_once_per_call(self):
        """One request per validation, not one per object -- a layout can hold thousands."""
        sdk = _FakeSdk({"ws": {"metric/a", "metric/b", "metric/c"}})
        ValidationService(sdk).validate_analytics_model("ws", _model("a", "b", "c"))
        assert sdk.requested == ["ws"]

    def test_an_empty_model_reports_nothing_checked(self):
        result = ValidationService(_FakeSdk({"ws": set()})).validate_analytics_model(
            "ws", CatalogDeclarativeAnalytics(analytics=None)
        )
        assert result.ok
        assert result.objects_checked == 0

    def test_a_single_visualization_can_be_validated_on_its_own(self):
        model = _model("a")
        service = ValidationService(_FakeSdk({"ws": {"metric/a"}}))
        assert service.validate_visualization("ws", model.analytics.visualization_objects[0]).ok

    def test_the_summary_says_inheritance_was_taken_into_account(self):
        """A clean report is otherwise indistinguishable from one that checked nothing."""
        result = ValidationService(_FakeSdk({"ws": {"metric/a"}})).validate_analytics_model("ws", _model("a"))
        assert "effective catalog (inherited objects included)" in result.format()
        assert "1 reference(s) resolved, 0 unresolved" in result.format()
