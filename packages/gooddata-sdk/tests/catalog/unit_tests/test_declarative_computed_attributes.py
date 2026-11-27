# (C) 2026 GoodData Corporation
"""Unit test: analytics-layer ``computed_attributes`` survive the declarative round-trip.

The declarative round-trip is the whole point of CA support in the SDK - it is what
gives analytics-as-code parity with the backend layout API (CQ-2799 / CQ-2800). A
computed attribute that goes into ``analytics_model/computed_attributes/`` must come
back out unchanged, including the nested ``content`` ({maql, format, metricType}).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from gooddata_sdk import (
    CatalogComputedAttribute,
    CatalogComputedAttributeDocument,
    CatalogComputedAttributePostDocument,
    CatalogDeclarativeAnalytics,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)
from gooddata_sdk.compute.model.attribute import Attribute
from gooddata_sdk.compute.model.base import ObjId

_COMPUTED_ATTRIBUTE = {
    "id": "sales-band",
    "title": "Sales Band",
    "description": "Bucketed sales.",
    "content": {"maql": "SELECT 1", "format": "#,##0", "metricType": "UNSPECIFIED"},
    "dataType": "STRING",
    "tags": ["Sales"],
}
_LAYOUT = {"analytics": {"computedAttributes": [_COMPUTED_ATTRIBUTE]}}


def test_declarative_computed_attributes_survive_round_trip() -> None:
    analytics = CatalogDeclarativeAnalytics.from_dict(_LAYOUT)

    computed_attributes = analytics.analytics.computed_attributes
    assert len(computed_attributes) == 1
    assert computed_attributes[0].id == "sales-band"
    assert computed_attributes[0].title == "Sales Band"
    assert computed_attributes[0].data_type == "STRING"
    # The nested content is typed, not a bare dict.
    assert computed_attributes[0].content.maql == "SELECT 1"
    assert computed_attributes[0].content.format == "#,##0"
    assert computed_attributes[0].content.metric_type == "UNSPECIFIED"

    round_tripped = analytics.to_api().to_dict(camel_case=True)
    assert round_tripped["analytics"]["computedAttributes"] == [_COMPUTED_ATTRIBUTE]


def test_declarative_computed_attributes_survive_disk_round_trip(tmp_path: Path) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({"computedAttributes": [_COMPUTED_ATTRIBUTE]})

    layer.store_to_disk(tmp_path)
    assert (tmp_path / "analytics_model" / "computed_attributes" / "sales-band.yaml").exists()

    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)
    assert reloaded.computed_attributes == layer.computed_attributes
    assert reloaded.to_dict(camel_case=True)["computedAttributes"] == [_COMPUTED_ATTRIBUTE]


def _computed_attribute(**kwargs: object) -> CatalogComputedAttribute:
    return CatalogComputedAttribute.init(maql="SELECT 1", title="Sales Band", format="#,##0", **kwargs)  # type: ignore[arg-type]


_EXPECTED_ATTRIBUTES = {"title": "Sales Band", "content": {"maql": "SELECT 1", "format": "#,##0"}}


def test_computed_attribute_entity_serializes_to_json_api_document() -> None:
    """The PUT (update) endpoint takes the `In` document, which requires the id."""
    document = CatalogComputedAttributeDocument(data=_computed_attribute(computed_attribute_id="sales-band"))

    assert document.to_api().to_dict(camel_case=True) == {
        "data": {"id": "sales-band", "type": "computedAttribute", "attributes": _EXPECTED_ATTRIBUTES}
    }


def test_computed_attribute_post_document_carries_the_optional_id_body() -> None:
    """The POST (create) endpoint takes its own document, whose id is optional.

    Regression test: the create call was originally wired to the `In` document, copied
    from the filter-view template. Computed attributes have a separate POST schema, so
    that raised a TypeError from the generated client before it ever reached the backend.
    """
    with_id = CatalogComputedAttributePostDocument(data=_computed_attribute(computed_attribute_id="sales-band"))
    assert with_id.to_api().to_dict(camel_case=True) == {
        "data": {"id": "sales-band", "type": "computedAttribute", "attributes": _EXPECTED_ATTRIBUTES}
    }

    # No id - the backend generates one, so the key must be absent rather than null.
    without_id = CatalogComputedAttributePostDocument(data=_computed_attribute())
    assert without_id.to_api().to_dict(camel_case=True) == {
        "data": {"type": "computedAttribute", "attributes": _EXPECTED_ATTRIBUTES}
    }


def test_computed_attribute_without_id_cannot_be_updated() -> None:
    with pytest.raises(ValueError, match="id is required for an update"):
        CatalogComputedAttributeDocument(data=_computed_attribute()).to_api()


def _label_slot(label: str | ObjId) -> dict[str, dict[str, str]]:
    return Attribute(local_id="a", label=label).as_api_model().to_dict(camel_case=True)["label"]


def test_computed_attribute_can_slice_an_execution() -> None:
    """A computed attribute is referenced through the label slot of an AFM attribute."""
    assert _label_slot(ObjId("sales-band", "computedAttribute")) == {
        "identifier": {"id": "sales-band", "type": "computedAttribute"}
    }

    # Plain labels keep working - the type is no longer defaulted by the generated client.
    assert _label_slot("region") == {"identifier": {"id": "region", "type": "label"}}
    assert _label_slot(ObjId("region", "label")) == {"identifier": {"id": "region", "type": "label"}}


@pytest.mark.parametrize("obj_id_type", ["attribute", "dataset", "fact", "metric"])
def test_non_computed_attribute_obj_id_still_slices_by_label(obj_id_type: str) -> None:
    """An ObjId of any other type keeps going to the API as a label.

    Regression test: `AfmObjectIdentifierLabelIdentifier.type` used to be defaulted by the
    generated client, so the ObjId type was ignored and every type reached the API as a
    label. Once the enum gained "computedAttribute" the type became required, and forwarding
    it verbatim raised ApiValueError for external callers that pass some other type -- a
    visualization ref carries whatever type it was stored with (see utils.ref_extract).
    """
    assert _label_slot(ObjId("region", obj_id_type)) == {"identifier": {"id": "region", "type": "label"}}
