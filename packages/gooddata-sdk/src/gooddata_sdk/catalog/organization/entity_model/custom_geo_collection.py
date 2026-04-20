# (C) 2026 GoodData Corporation
from __future__ import annotations

from attrs import define
from gooddata_api_client.model.json_api_custom_geo_collection_in import JsonApiCustomGeoCollectionIn
from gooddata_api_client.model.json_api_custom_geo_collection_in_attributes import (
    JsonApiCustomGeoCollectionInAttributes,
)
from gooddata_api_client.model.json_api_custom_geo_collection_in_document import JsonApiCustomGeoCollectionInDocument

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogCustomGeoCollectionDocument(Base):
    data: CatalogCustomGeoCollection

    @staticmethod
    def client_class() -> type[JsonApiCustomGeoCollectionInDocument]:
        return JsonApiCustomGeoCollectionInDocument


@define(kw_only=True)
class CatalogCustomGeoCollection(Base):
    id: str
    attributes: CatalogCustomGeoCollectionAttributes | None = None

    @staticmethod
    def client_class() -> type[JsonApiCustomGeoCollectionIn]:
        return JsonApiCustomGeoCollectionIn

    @classmethod
    def init(
        cls,
        collection_id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> CatalogCustomGeoCollection:
        return cls(
            id=collection_id,
            attributes=CatalogCustomGeoCollectionAttributes(name=name, description=description),
        )


@define(kw_only=True)
class CatalogCustomGeoCollectionAttributes(Base):
    description: str | None = None
    name: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiCustomGeoCollectionInAttributes]:
        return JsonApiCustomGeoCollectionInAttributes
