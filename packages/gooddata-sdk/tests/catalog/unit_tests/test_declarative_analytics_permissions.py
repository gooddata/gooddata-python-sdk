# (C) 2026 GoodData Corporation
"""Unit test: metric and visualization object permissions survive the declarative round trip."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from gooddata_sdk.catalog.identifier import CatalogAssigneeIdentifier
from gooddata_sdk.catalog.permission.declarative_model.permission import (
    CatalogDeclarativeMetricPermissionsForAssignee,
    CatalogDeclarativeMetricPermissionsForAssigneeRule,
    CatalogDeclarativeVisualizationObjectPermissionsForAssignee,
    CatalogDeclarativeVisualizationObjectPermissionsForAssigneeRule,
)
from gooddata_sdk.catalog.rule import CatalogAssigneeRule
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    EMPTY_FOLDER_KEEP_FILE,
    LAYOUT_ANALYTICS_MODEL_DIR,
    LAYOUT_METRIC_EXTENSIONS_DIR,
    LAYOUT_VISUALIZATION_OBJECT_EXTENSIONS_DIR,
    CatalogDeclarativeAnalyticsLayer,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import CatalogDeclarativeWorkspaceModel

_METRIC: dict[str, Any] = {"id": "restricted_metric", "title": "Restricted", "content": {"maql": "SELECT 1"}}
_VISUALIZATION_OBJECT: dict[str, Any] = {"id": "restricted_insight", "title": "Restricted", "content": {"buckets": []}}

_FOR_USER: dict[str, Any] = {"name": "VIEW", "assignee": {"id": "demo2", "type": "user"}}
_FOR_GROUP: dict[str, Any] = {"name": "EDIT", "assignee": {"id": "demoGroup", "type": "userGroup"}}
_FOR_RULE: dict[str, Any] = {"name": "SHARE", "assigneeRule": {"type": "allWorkspaceUsers"}}
_PERMISSIONS: list[dict[str, Any]] = [_FOR_USER, _FOR_GROUP, _FOR_RULE]

_OBJECTS = pytest.mark.parametrize(
    ("layer_key", "obj", "assignee_class", "rule_class"),
    [
        (
            "metrics",
            _METRIC,
            CatalogDeclarativeMetricPermissionsForAssignee,
            CatalogDeclarativeMetricPermissionsForAssigneeRule,
        ),
        (
            "visualizationObjects",
            _VISUALIZATION_OBJECT,
            CatalogDeclarativeVisualizationObjectPermissionsForAssignee,
            CatalogDeclarativeVisualizationObjectPermissionsForAssigneeRule,
        ),
    ],
    ids=["metric", "visualization-object"],
)
_EXTENSIONS = pytest.mark.parametrize(
    ("layer_key", "folder"),
    [
        ("metricExtensions", LAYOUT_METRIC_EXTENSIONS_DIR),
        ("visualizationObjectExtensions", LAYOUT_VISUALIZATION_OBJECT_EXTENSIONS_DIR),
    ],
    ids=["metric", "visualization-object"],
)


def _objects(layer: CatalogDeclarativeAnalyticsLayer, layer_key: str) -> list[Any]:
    return layer.metrics if layer_key == "metrics" else layer.visualization_objects


def _extensions(layer: CatalogDeclarativeAnalyticsLayer, layer_key: str) -> list[Any] | None:
    return layer.metric_extensions if layer_key == "metricExtensions" else layer.visualization_object_extensions


@_OBJECTS
def test_permissions_survive_round_trip(
    tmp_path: Path, layer_key: str, obj: dict[str, Any], assignee_class: type, rule_class: type
) -> None:
    declared = {**obj, "permissions": _PERMISSIONS}
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: [declared]})

    permissions = _objects(layer, layer_key)[0].permissions
    assert [type(permission) for permission in permissions] == [assignee_class, assignee_class, rule_class]

    layer.store_to_disk(tmp_path)
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert reloaded == layer
    assert reloaded.to_dict(camel_case=True)[layer_key] == [declared]
    assert reloaded.to_api().to_dict(camel_case=True)[layer_key] == [declared]


@_OBJECTS
@pytest.mark.parametrize(
    ("extra", "expected"),
    [({}, None), ({"permissions": None}, None), ({"permissions": []}, [])],
    ids=["absent", "null", "empty"],
)
def test_absent_permissions_stay_absent_and_empty_stay_empty(
    tmp_path: Path,
    layer_key: str,
    obj: dict[str, Any],
    assignee_class: type,
    rule_class: type,
    extra: dict[str, Any],
    expected: list[Any] | None,
) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: [{**obj, **extra}]})

    layer.store_to_disk(tmp_path)
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert _objects(reloaded, layer_key)[0].permissions == expected
    sent = reloaded.to_api().to_dict(camel_case=True)[layer_key][0]
    assert sent == ({**obj, "permissions": []} if expected == [] else obj)


@_OBJECTS
def test_permissions_reach_the_workspace_model_payload(
    layer_key: str, obj: dict[str, Any], assignee_class: type, rule_class: type
) -> None:
    declared = {**obj, "permissions": _PERMISSIONS}
    model = CatalogDeclarativeWorkspaceModel.from_dict({"analytics": {layer_key: [declared]}})

    assert model.to_api().to_dict(camel_case=True)["analytics"][layer_key] == [declared]


@_OBJECTS
def test_unknown_permission_name_is_rejected(
    layer_key: str, obj: dict[str, Any], assignee_class: type, rule_class: type
) -> None:
    with pytest.raises(ValueError, match="Allowed values for attribute name"):
        assignee_class(name="MANAGE", assignee=CatalogAssigneeIdentifier(id="demo2", type="user"))
    with pytest.raises(ValueError, match="Allowed values for attribute name"):
        rule_class(name="MANAGE", assignee_rule=CatalogAssigneeRule(type="allWorkspaceUsers"))


@_EXTENSIONS
def test_extensions_survive_round_trip(tmp_path: Path, layer_key: str, folder: str) -> None:
    declared = [{"id": "open", "permissions": []}, {"id": "restricted", "permissions": _PERMISSIONS}]
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: declared})

    layer.store_to_disk(tmp_path)
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert reloaded == layer
    assert reloaded.to_api().to_dict(camel_case=True)[layer_key] == declared


@_EXTENSIONS
@pytest.mark.parametrize("declared", [None, []], ids=["absent", "empty"])
def test_absent_extensions_stay_absent_and_empty_stay_empty(
    tmp_path: Path, layer_key: str, folder: str, declared: list[Any] | None
) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({} if declared is None else {layer_key: declared})
    assert layer.to_api().to_dict(camel_case=True).get(layer_key) == declared

    layer.store_to_disk(tmp_path)
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert _extensions(reloaded, layer_key) == declared
    assert reloaded.to_api().to_dict(camel_case=True).get(layer_key) == declared


@_EXTENSIONS
def test_empty_extension_list_is_stored_as_a_folder_git_keeps(tmp_path: Path, layer_key: str, folder: str) -> None:
    CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: []}).store_to_disk(tmp_path)

    extensions_folder = tmp_path / LAYOUT_ANALYTICS_MODEL_DIR / folder
    assert [path.name for path in extensions_folder.iterdir()] == [EMPTY_FOLDER_KEEP_FILE]


@_EXTENSIONS
def test_absent_extension_list_has_no_folder(tmp_path: Path, layer_key: str, folder: str) -> None:
    CatalogDeclarativeAnalyticsLayer.from_dict({}).store_to_disk(tmp_path)

    assert not (tmp_path / LAYOUT_ANALYTICS_MODEL_DIR / folder).exists()


@_EXTENSIONS
def test_keep_file_is_dropped_once_the_list_has_extensions(tmp_path: Path, layer_key: str, folder: str) -> None:
    CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: []}).store_to_disk(tmp_path)
    CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: [{"id": "kept", "permissions": [_FOR_RULE]}]}).store_to_disk(
        tmp_path
    )

    extensions_folder = tmp_path / LAYOUT_ANALYTICS_MODEL_DIR / folder
    assert [path.name for path in extensions_folder.iterdir()] == ["kept.yaml"]


@_EXTENSIONS
@pytest.mark.parametrize(
    "declared",
    [None, [], [{"id": "kept", "permissions": [_FOR_RULE]}]],
    ids=["absent", "empty", "other-extension"],
)
def test_store_drops_extension_files_of_an_earlier_store(
    tmp_path: Path, layer_key: str, folder: str, declared: list[dict[str, Any]] | None
) -> None:
    stale = [{"id": "stale", "permissions": _PERMISSIONS}]
    CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: stale}).store_to_disk(tmp_path)

    CatalogDeclarativeAnalyticsLayer.from_dict({} if declared is None else {layer_key: declared}).store_to_disk(
        tmp_path
    )
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert reloaded.to_api().to_dict(camel_case=True).get(layer_key) == declared
