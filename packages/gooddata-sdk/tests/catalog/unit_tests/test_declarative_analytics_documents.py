# (C) 2026 GoodData Corporation
"""Unit test: Publisher documents survive the declarative analytics round-trip.

The analytics layer carries ``documents``, ``documentTemplates`` and
``pageTemplates``. Whatever goes in through ``from_dict`` must come back out of
``to_api()`` unchanged, including content keys the SDK does not model.
"""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from cattrs import structure
from gooddata_sdk import (
    CatalogAbsolutePublisherDocumentPeriod,
    CatalogDeclarativeAnalytics,
    CatalogDeclarativePublisherDocument,
    CatalogDeclarativePublisherDocumentPageTemplate,
    CatalogDeclarativePublisherDocumentTemplate,
    CatalogPublisherDocumentPeriod,
    CatalogRelativePublisherDocumentPeriod,
    CatalogUserIdentifier,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)
from gooddata_sdk.utils import write_layout_to_file

_AUTHOR = {
    "createdBy": {"id": "admin", "type": "user"},
    "createdAt": "2026-11-02 10:00",
    "modifiedBy": {"id": "admin", "type": "user"},
    "modifiedAt": "2026-11-02 11:00",
}
_TEXT = {"type": "text", "id": "t1", "markdown": "Hello"}
_DOCUMENT = {
    "id": "doc_1",
    "title": "Doc 1",
    "version": "1",
    "period": {"type": "relative", "granularity": "GDC.time.month", "from": -1, "to": 0},
    "content": {
        "locale": "en-US",
        "pages": [{"id": "p1", "kind": "content", "layout": {"type": "row", "children": [_TEXT]}}],
        "futureField": {"nested": [1, {"deep": True}]},
    },
    **_AUTHOR,
}
_DOCUMENT_TEMPLATE = {"id": "tpl_1", "title": "Tpl 1", "version": "1", "content": {"locale": "en-US"}}
_PAGE_TEMPLATE = {"id": "pt_1", "title": "Page 1", "version": "1", "content": {"layout": _TEXT}}
_LAYER = {"documents": [_DOCUMENT], "documentTemplates": [_DOCUMENT_TEMPLATE], "pageTemplates": [_PAGE_TEMPLATE]}
_METRIC = {"id": "bmk_w_fraud_charged_back", "title": "BMK", "content": {"format": "#,##0", "maql": "SELECT 1"}}
_DOCUMENT_FOLDERS = ("documents", "document_templates", "page_templates")
_ABSOLUTE_PERIOD = {"type": "absolute", "granularity": "GDC.time.date", "from": "2026-01-01", "to": "2026-01-31"}
_RELATIVE_PERIOD = {"type": "relative", "granularity": "GDC.time.month", "from": -1, "to": 0}
# The generated client holds an absolute period's dates as `datetime.date`, so its `to_dict` writes them so.
_PERIODS = pytest.mark.parametrize(
    ("period", "typed_period", "client_period"),
    [
        (
            _ABSOLUTE_PERIOD,
            CatalogAbsolutePublisherDocumentPeriod(from_="2026-01-01", to="2026-01-31", granularity="GDC.time.date"),
            {**_ABSOLUTE_PERIOD, "from": date(2026, 1, 1), "to": date(2026, 1, 31)},
        ),
        (
            _RELATIVE_PERIOD,
            CatalogRelativePublisherDocumentPeriod(from_=-1, to=0, granularity="GDC.time.month"),
            _RELATIVE_PERIOD,
        ),
    ],
    ids=["absolute", "relative"],
)


def _round_trip(layer: CatalogDeclarativeAnalyticsLayer) -> dict[str, Any]:
    return layer.to_api().to_dict(camel_case=True)


def test_documents_survive_api_round_trip() -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict(_LAYER)

    round_tripped = _round_trip(layer)

    assert {key: round_tripped[key] for key in _LAYER} == _LAYER


def test_document_author_fields_are_typed() -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict(_LAYER)

    document = layer.documents[0]

    assert isinstance(document, CatalogDeclarativePublisherDocument)
    assert document.created_by == CatalogUserIdentifier(id="admin", type="user")
    assert document.created_at == "2026-11-02 10:00"
    assert document.modified_by == CatalogUserIdentifier(id="admin", type="user")
    assert document.modified_at == "2026-11-02 11:00"


@pytest.mark.parametrize(
    ("layer_key", "attribute", "item_class", "item"),
    [
        ("documentTemplates", "document_templates", CatalogDeclarativePublisherDocumentTemplate, _DOCUMENT_TEMPLATE),
        ("pageTemplates", "page_templates", CatalogDeclarativePublisherDocumentPageTemplate, _PAGE_TEMPLATE),
    ],
    ids=["document_template", "page_template"],
)
def test_templates_have_no_author_attributes(
    layer_key: str, attribute: str, item_class: type, item: dict[str, Any]
) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({layer_key: [item]})

    template = getattr(layer, attribute)[0]

    assert isinstance(template, item_class)
    assert not hasattr(template, "created_by")
    round_tripped = _round_trip(layer)[layer_key]
    assert round_tripped == [item]
    assert not set(_AUTHOR) & set(round_tripped[0])


def test_document_without_author_fields() -> None:
    document = {key: value for key, value in _DOCUMENT.items() if key not in _AUTHOR}
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({"documents": [document]})

    loaded = layer.documents[0]

    assert loaded.created_by is None
    assert loaded.created_at is None
    assert loaded.modified_by is None
    assert loaded.modified_at is None
    round_tripped = _round_trip(layer)["documents"]
    assert round_tripped == [document]
    assert not set(_AUTHOR) & set(round_tripped[0])


def test_empty_layer_has_empty_document_lists() -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({})

    assert layer.documents == []
    assert layer.document_templates == []
    assert layer.page_templates == []
    round_tripped = _round_trip(layer)
    assert round_tripped["documents"] == []
    assert round_tripped["documentTemplates"] == []
    assert round_tripped["pageTemplates"] == []


@pytest.mark.parametrize("sort", [True, False], ids=["sorted", "unsorted"])
def test_documents_survive_disk_round_trip(tmp_path: Path, sort: bool) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict(_LAYER)

    layer.store_to_disk(tmp_path, sort=sort)

    analytics_model_folder = tmp_path / "analytics_model"
    assert (analytics_model_folder / "documents" / "doc_1.yaml").is_file()
    assert (analytics_model_folder / "document_templates" / "tpl_1.yaml").is_file()
    assert (analytics_model_folder / "page_templates" / "pt_1.yaml").is_file()
    round_tripped = _round_trip(CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path))
    assert {key: round_tripped[key] for key in _LAYER} == _LAYER


def test_load_without_document_folders(tmp_path: Path) -> None:
    CatalogDeclarativeAnalyticsLayer.from_dict({"metrics": [_METRIC]}).store_to_disk(tmp_path)
    for folder in _DOCUMENT_FOLDERS:
        shutil.rmtree(tmp_path / "analytics_model" / folder, ignore_errors=True)

    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert reloaded.documents == []
    assert reloaded.document_templates == []
    assert reloaded.page_templates == []
    assert _round_trip(reloaded)["metrics"] == [_METRIC]


def _document_with(period: dict[str, Any]) -> dict[str, Any]:
    return {**{key: value for key, value in _DOCUMENT.items() if key not in _AUTHOR}, "period": period}


@_PERIODS
def test_period_read_is_typed(
    period: dict[str, Any], typed_period: CatalogPublisherDocumentPeriod, client_period: dict[str, Any]
) -> None:
    document = CatalogDeclarativePublisherDocument.from_dict(_document_with(period))

    assert document.period == typed_period


@_PERIODS
def test_period_to_dict_writes_api_names(
    period: dict[str, Any], typed_period: CatalogPublisherDocumentPeriod, client_period: dict[str, Any]
) -> None:
    document = CatalogDeclarativePublisherDocument.from_dict(_document_with(period))

    assert document.to_dict()["period"] == client_period


@_PERIODS
def test_hand_built_document_equals_read_document(
    period: dict[str, Any], typed_period: CatalogPublisherDocumentPeriod, client_period: dict[str, Any]
) -> None:
    hand_built = CatalogDeclarativePublisherDocument(
        id=_DOCUMENT["id"],
        title=_DOCUMENT["title"],
        version=_DOCUMENT["version"],
        content=_DOCUMENT["content"],
        period=typed_period,
    )

    read_back = CatalogDeclarativePublisherDocument.from_dict(hand_built.to_dict())

    assert read_back == hand_built


@_PERIODS
def test_nested_period_read_is_typed(
    period: dict[str, Any], typed_period: CatalogPublisherDocumentPeriod, client_period: dict[str, Any]
) -> None:
    analytics = CatalogDeclarativeAnalytics.from_dict({"analytics": {"documents": [_document_with(period)]}})

    assert analytics.analytics is not None
    assert analytics.analytics.documents[0].period == typed_period


@_PERIODS
def test_nested_period_write_uses_api_names(
    period: dict[str, Any], typed_period: CatalogPublisherDocumentPeriod, client_period: dict[str, Any]
) -> None:
    document = CatalogDeclarativePublisherDocument(
        id=_DOCUMENT["id"],
        title=_DOCUMENT["title"],
        version=_DOCUMENT["version"],
        content=_DOCUMENT["content"],
        period=typed_period,
    )
    analytics = CatalogDeclarativeAnalytics(analytics=CatalogDeclarativeAnalyticsLayer(documents=[document]))

    written = analytics.to_api().to_dict(camel_case=True)["analytics"]["documents"][0]["period"]

    assert "from_" not in written
    assert written == client_period


def test_unknown_period_type_raises() -> None:
    with pytest.raises(ValueError, match="rolling"):
        structure({"type": "rolling", "from": -1, "to": 0}, CatalogPublisherDocumentPeriod)


def test_load_document_yaml_without_author_fields(tmp_path: Path) -> None:
    document = {key: value for key, value in _DOCUMENT.items() if key not in _AUTHOR}
    documents_folder = tmp_path / "analytics_model" / "documents"
    documents_folder.mkdir(parents=True)
    write_layout_to_file(documents_folder / "doc_1.yaml", document)

    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert len(reloaded.documents) == 1
    loaded = reloaded.documents[0]
    assert loaded.created_by is None
    assert loaded.created_at is None
    assert loaded.modified_by is None
    assert loaded.modified_at is None
