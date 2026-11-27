# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

from gooddata_sdk.catalog.workspace.aac import load_aac_workspace_from_disk, store_aac_workspace_to_disk
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import CatalogDeclarativeWorkspaceModel
from gooddata_sdk.utils import read_layout_from_file

_STRING = {
    "id": "scenario",
    "title": "Scenario",
    "description": "Planning scenario",
    "tags": ["planning"],
    "content": {"type": "STRING", "defaultValue": "Actual"},
}
_NUMBER = {
    "id": "discount_rate",
    "title": "Discount rate",
    "description": "",
    "tags": [],
    "content": {"type": "NUMBER", "defaultValue": 0.5},
}
_PERIOD = {
    "id": "last_13_months",
    "title": "Last 13 months",
    "description": "",
    "tags": [],
    "content": {"type": "DATE_RANGE", "defaultValue": {"granularity": "MONTH", "from": "2024-11", "to": "2025-11"}},
}
_OPEN_PERIOD = {
    "id": "since_2024",
    "title": "Since 2024",
    "description": "",
    "tags": [],
    "content": {"type": "DATE_RANGE", "defaultValue": {"granularity": "YEAR", "from": "2024"}},
}
_CODE_PARAMETERS = [_STRING, _NUMBER, _PERIOD, _OPEN_PERIOD]


def _model(parameters: list[dict[str, Any]]) -> CatalogDeclarativeWorkspaceModel:
    return CatalogDeclarativeWorkspaceModel.from_dict({"analytics": {"parameters": parameters}})


def _parameters(model: CatalogDeclarativeWorkspaceModel) -> list[dict[str, Any]]:
    return model.to_dict(camel_case=True).get("analytics", {}).get("parameters", [])


def test_parameters_round_trip_through_aac(tmp_path: Path) -> None:
    store_aac_workspace_to_disk(_model(_CODE_PARAMETERS), tmp_path)

    for parameter in _CODE_PARAMETERS:
        stored = read_layout_from_file(tmp_path / "parameters" / f"{parameter['id']}.yaml")
        assert stored["type"] == "parameter"
        assert stored["definition"]["type"] == parameter["content"]["type"]
    loaded = sorted(_parameters(load_aac_workspace_from_disk(tmp_path)), key=lambda p: p["id"])
    assert loaded == sorted(_CODE_PARAMETERS, key=lambda p: p["id"])
