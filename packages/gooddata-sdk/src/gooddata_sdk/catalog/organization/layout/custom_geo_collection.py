# (C) 2026 GoodData Corporation
from __future__ import annotations

from attrs import define
from gooddata_api_client.model.declarative_custom_geo_collection import DeclarativeCustomGeoCollection

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogDeclarativeCustomGeoCollection(Base):
    id: str
    description: str | None = None
    name: str | None = None

    @staticmethod
    def client_class() -> type[DeclarativeCustomGeoCollection]:
        return DeclarativeCustomGeoCollection
