# (C) 2026 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any, Optional

import attr
from gooddata_api_client.model.declarative_custom_geo_collection import DeclarativeCustomGeoCollection

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeCustomGeoCollection(Base):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None

    @staticmethod
    def client_class() -> builtins.type[DeclarativeCustomGeoCollection]:
        return DeclarativeCustomGeoCollection

    @classmethod
    def from_api(cls, api_model: Any) -> CatalogDeclarativeCustomGeoCollection:
        return cls(
            id=api_model["id"],
            name=safeget(api_model, ["name"]),
            description=safeget(api_model, ["description"]),
        )

    def to_api(self) -> DeclarativeCustomGeoCollection:
        kwargs: dict[str, Any] = {}
        if self.name is not None:
            kwargs["name"] = self.name
        if self.description is not None:
            kwargs["description"] = self.description
        return DeclarativeCustomGeoCollection(id=self.id, **kwargs)
