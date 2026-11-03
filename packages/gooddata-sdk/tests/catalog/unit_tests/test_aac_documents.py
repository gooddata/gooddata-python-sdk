# (C) 2026 GoodData Corporation
from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from gooddata_sdk.catalog.workspace.aac import load_aac_workspace_from_disk, store_aac_workspace_to_disk
from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import CatalogDeclarativeWorkspaceModel
from gooddata_sdk.utils import read_layout_from_file

_FIXTURES_DIR = Path(__file__).parent / "aac_tests"

_AUTHOR = {
    "createdBy": {"id": "admin", "type": "user"},
    "createdAt": "2026-11-02 10:00",
    "modifiedBy": {"id": "admin", "type": "user"},
    "modifiedAt": "2026-11-02 11:00",
}
_TEXT = {"type": "text", "id": "t1", "markdown": "Hello"}
_PAGES = [{"id": "p1", "kind": "content", "layout": {"type": "row", "children": [_TEXT]}}]
_DOCUMENT = {
    "id": "doc_1",
    "title": "Doc 1",
    "description": "Monthly",
    "tags": ["finance"],
    "version": "2",
    "period": {"type": "relative", "granularity": "GDC.time.month", "from": -1, "to": 0},
    "content": {"locale": "en-US", "pages": _PAGES, "futureField": {"nested": [1, {"deep": True}]}},
    **_AUTHOR,
}
_DOCUMENT_TEMPLATE = {
    "id": "tpl_1",
    "title": "Tpl 1",
    "description": "Base",
    "tags": ["finance"],
    "version": "2",
    "content": {"locale": "en-US", "pages": _PAGES},
}
_PAGE_TEMPLATE = {
    "id": "pt_1",
    "title": "Page 1",
    "description": "Cover",
    "tags": ["finance"],
    "version": "2",
    "content": {"layout": _TEXT},
}
_METRIC = {"id": "m1", "title": "Metric 1", "content": {"format": "#,##0", "maql": "SELECT 1"}}
_LAYOUT_KEYS = ("documents", "documentTemplates", "pageTemplates")


def _model(analytics: dict[str, Any]) -> CatalogDeclarativeWorkspaceModel:
    return CatalogDeclarativeWorkspaceModel.from_dict({"analytics": analytics})


def _publisher_model() -> CatalogDeclarativeWorkspaceModel:
    return _model(
        {"documents": [_DOCUMENT], "documentTemplates": [_DOCUMENT_TEMPLATE], "pageTemplates": [_PAGE_TEMPLATE]}
    )


def _reloaded_analytics(tmp_path: Path) -> dict[str, Any]:
    return load_aac_workspace_from_disk(tmp_path).to_dict(camel_case=True).get("analytics", {})


def test_store_writes_one_file_per_object(tmp_path: Path) -> None:
    store_aac_workspace_to_disk(_publisher_model(), tmp_path)
    common_keys = {"type", "id", "version", "title", "description", "tags", "content"}

    for path, aac_type, keys in (
        (tmp_path / "documents" / "doc_1.yaml", "document", common_keys | {"period"}),
        (tmp_path / "documentTemplates" / "tpl_1.yaml", "document_template", common_keys),
        (tmp_path / "pageTemplates" / "pt_1.yaml", "page_template", common_keys),
    ):
        assert path.is_file()
        aac = read_layout_from_file(path)
        assert aac["type"] == aac_type
        assert aac["version"] == "2"
        assert set(aac) == keys


def test_objects_round_trip_through_aac(tmp_path: Path) -> None:
    store_aac_workspace_to_disk(_publisher_model(), tmp_path)

    analytics = _reloaded_analytics(tmp_path)

    document_without_author = {key: value for key, value in _DOCUMENT.items() if key not in _AUTHOR}
    assert {key: analytics.get(key) for key in _LAYOUT_KEYS} == {
        "documents": [document_without_author],
        "documentTemplates": [_DOCUMENT_TEMPLATE],
        "pageTemplates": [_PAGE_TEMPLATE],
    }


def test_absolute_period_round_trips(tmp_path: Path) -> None:
    document = {**_DOCUMENT, "period": {"type": "absolute", "from": "2026-01-01", "to": "2026-01-31"}}
    store_aac_workspace_to_disk(_model({"documents": [document]}), tmp_path)

    period = _reloaded_analytics(tmp_path)["documents"][0]["period"]

    assert {key: period[key] for key in ("type", "from", "to")} == {
        "type": "absolute",
        "from": date(2026, 1, 1),
        "to": date(2026, 1, 31),
    }


def test_load_fixture_folders_beside_visualisations(tmp_path: Path) -> None:
    for subdir in ("datasets", "metrics", "visualisations", "documents", "documentTemplates", "pageTemplates"):
        shutil.copytree(_FIXTURES_DIR / subdir, tmp_path / subdir)

    model_dict = load_aac_workspace_from_disk(tmp_path).to_dict(camel_case=True)
    ldm = model_dict.get("ldm", {})
    analytics = model_dict.get("analytics", {})

    assert [obj["id"] for obj in analytics.get("documents", [])] == ["doc_1"]
    assert [obj["id"] for obj in analytics.get("documentTemplates", [])] == ["tpl_1"]
    assert [obj["id"] for obj in analytics.get("pageTemplates", [])] == ["pt_1"]
    assert len(ldm.get("datasets", [])) == 2
    assert len(analytics.get("metrics", [])) == 1
    assert len(analytics.get("visualizationObjects", [])) == 2


def test_workspace_without_documents_stores_as_today(tmp_path: Path) -> None:
    store_aac_workspace_to_disk(_model({"metrics": [_METRIC]}), tmp_path)

    for subdir in _LAYOUT_KEYS:
        assert not (tmp_path / subdir).exists()
    assert (tmp_path / "metrics" / "m1.yaml").is_file()

    analytics = _reloaded_analytics(tmp_path)
    for key in _LAYOUT_KEYS:
        assert not analytics.get(key)
    assert [metric["id"] for metric in analytics["metrics"]] == ["m1"]


@pytest.mark.parametrize(
    ("layout_key", "obj", "aac_type"),
    [
        ("documents", _DOCUMENT, "document"),
        ("documentTemplates", _DOCUMENT_TEMPLATE, "document_template"),
        ("pageTemplates", _PAGE_TEMPLATE, "page_template"),
    ],
)
def test_store_refuses_non_v2_object(tmp_path: Path, layout_key: str, obj: dict[str, Any], aac_type: str) -> None:
    model = _model({"metrics": [_METRIC], layout_key: [{**obj, "version": "1"}]})
    obj_id = obj["id"]

    with pytest.raises(ValueError, match=rf'{aac_type} "{obj_id}" \(version "1"\)'):
        store_aac_workspace_to_disk(model, tmp_path)

    assert list(tmp_path.rglob("*.yaml")) == []


def test_store_names_refused_template(tmp_path: Path) -> None:
    model = _model({"documentTemplates": [{**_DOCUMENT_TEMPLATE, "content": {"locale": "en-US"}}]})

    with pytest.raises(ValueError, match=r'document_template "tpl_1" \(version "2"\)'):
        store_aac_workspace_to_disk(model, tmp_path)


def test_load_refuses_non_v2_file(tmp_path: Path) -> None:
    fixture = (_FIXTURES_DIR / "documents" / "doc_1.yaml").read_text(encoding="utf-8")
    (tmp_path / "documents").mkdir()
    (tmp_path / "documents" / "doc_1.yaml").write_text(
        fixture.replace('version: "2"', 'version: "1"'), encoding="utf-8"
    )

    with pytest.raises(ValueError, match=r'document "doc_1" \(version "1"\)'):
        load_aac_workspace_from_disk(tmp_path)
