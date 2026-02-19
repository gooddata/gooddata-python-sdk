# (C) 2026 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any

import attr
from gooddata_api_client.model.json_api_custom_geo_collection_in import JsonApiCustomGeoCollectionIn
from gooddata_api_client.model.json_api_custom_geo_collection_in_attributes import (
    JsonApiCustomGeoCollectionInAttributes,
)
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True, kw_only=True)
class CatalogCustomGeoCollectionDocument(Base):
    data: CatalogCustomGeoCollection

    @staticmethod
    def client_class() -> builtins.type[JsonApiCustomGeoCollectionInDocument]:
        return JsonApiCustomGeoCollectionInDocument


@attr.s(auto_attribs=True, kw_only=True)
class CatalogCustomGeoCollection(Base):
    id: str
    name: str | None = None
    description: str | None = None

    @staticmethod
    def client_class() -> builtins.type[JsonApiCustomGeoCollectionIn]:
        return JsonApiCustomGeoCollectionIn

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogCustomGeoCollection:
        ea = entity.get("attributes") or {}
        return cls(
            id=entity["id"],
            name=safeget(ea, ["name"]),
            description=safeget(ea, ["description"]),
        )

    def to_api(self) -> JsonApiCustomGeoCollectionIn:
        kwargs: dict[str, Any] = {}
        if self.name is not None or self.description is not None:
            attrs: dict[str, Any] = {}
            if self.name is not None:
                attrs["name"] = self.name
            if self.description is not None:
                attrs["description"] = self.description
            kwargs["attributes"] = JsonApiCustomGeoCollectionInAttributes(**attrs)
        return JsonApiCustomGeoCollectionIn(
            id=self.id,
            type="customGeoCollection",
            **kwargs,
        )
