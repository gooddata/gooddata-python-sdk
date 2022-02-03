# (C) 2022 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.catalog.entity import CatalogEntity


class CatalogDataSource(CatalogEntity):
    @property
    def name(self) -> str:
        return self._e["name"]

    @property
    def data_source_type(self) -> str:
        return self._e["type"]

    @property
    def url(self) -> str:
        return self._e["url"]

    @property
    def username(self) -> str:
        return self._e["username"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
