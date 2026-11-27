# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

from gooddata_sdk.catalog.workspace.aac import (
    _build_entities,
    aac_visualization_to_declarative,
    detect_yaml_format,
    load_aac_workspace_from_disk,
    store_aac_workspace_to_disk,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import CatalogDeclarativeWorkspaceModel
from gooddata_sdk.utils import read_layout_from_file

_COMPUTED_ATTRIBUTE = {
    "id": "order_size",
    "title": "Order size",
    "description": "Orders grouped by their size",
    "tags": ["Orders"],
    "content": {"maql": 'SELECT CASE WHEN {metric/revenue} > 100 THEN "Large" ELSE "Small" END', "format": "#,##0"},
    "dataType": "STRING",
    "isHidden": True,
}
# The AAC form of a visualization that slices by the computed attribute above.
_AAC_VISUALIZATION = {
    "id": "rating_by_order_size",
    "type": "table",
    "title": "Rating by order size",
    "query": {
        "fields": {
            "size": "computed_attribute/order_size",
            "sum_rating": {"title": "Sum of Rating", "aggregation": "SUM", "using": "fact/rating"},
        }
    },
    "metrics": [{"field": "sum_rating"}],
    "view_by": ["size"],
}


def _model(analytics: dict[str, Any]) -> CatalogDeclarativeWorkspaceModel:
    return CatalogDeclarativeWorkspaceModel.from_dict({"analytics": analytics})


def _reloaded_analytics(path: Path) -> dict[str, Any]:
    return load_aac_workspace_from_disk(path).to_dict(camel_case=True).get("analytics", {})


def _attribute_identifiers(visualization: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item["attribute"]["displayForm"]["identifier"]
        for bucket in visualization["content"]["buckets"]
        for item in bucket["items"]
        if "attribute" in item
    ]


def test_store_writes_computed_attribute_file(tmp_path: Path) -> None:
    store_aac_workspace_to_disk(_model({"computedAttributes": [_COMPUTED_ATTRIBUTE]}), tmp_path)

    aac = read_layout_from_file(tmp_path / "computedAttributes" / "order_size.yaml")

    assert aac["type"] == "computed_attribute"
    assert aac["id"] == "order_size"
    assert aac["maql"] == _COMPUTED_ATTRIBUTE["content"]["maql"]


def test_computed_attribute_round_trips_through_aac(tmp_path: Path) -> None:
    store_aac_workspace_to_disk(_model({"computedAttributes": [_COMPUTED_ATTRIBUTE]}), tmp_path)

    assert _reloaded_analytics(tmp_path)["computedAttributes"] == [_COMPUTED_ATTRIBUTE]


def test_visualization_reference_to_computed_attribute_round_trips(tmp_path: Path) -> None:
    aac_computed_attribute = {"type": "computed_attribute", "id": "order_size", "maql": "SELECT 1"}
    entities = _build_entities([aac_computed_attribute, _AAC_VISUALIZATION])
    visualization = aac_visualization_to_declarative(_AAC_VISUALIZATION, entities)
    assert _attribute_identifiers(visualization) == [{"id": "order_size", "type": "computedAttribute"}]

    store_aac_workspace_to_disk(
        _model({"computedAttributes": [_COMPUTED_ATTRIBUTE], "visualizationObjects": [visualization]}), tmp_path
    )
    analytics = _reloaded_analytics(tmp_path)

    assert [ca["id"] for ca in analytics["computedAttributes"]] == ["order_size"]
    [reloaded_visualization] = analytics["visualizationObjects"]
    assert _attribute_identifiers(reloaded_visualization) == [{"id": "order_size", "type": "computedAttribute"}]


def test_workspace_without_computed_attributes_has_no_folder_or_key(tmp_path: Path) -> None:
    store_aac_workspace_to_disk(
        _model({"metrics": [{"id": "m1", "title": "Metric 1", "content": {"maql": "SELECT 1"}}]}), tmp_path
    )

    assert not (tmp_path / "computedAttributes").exists()
    assert "computedAttributes" not in _reloaded_analytics(tmp_path)


def test_computed_attributes_folder_is_detected_as_aac(tmp_path: Path) -> None:
    (tmp_path / "computedAttributes").mkdir()

    assert detect_yaml_format(tmp_path) == "aac"
