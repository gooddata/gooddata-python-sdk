# (C) 2022 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.catalog.entity import CatalogEntity


class CatalogWorkspace(CatalogEntity):
    @property
    def name(self) -> str:
        return self._e["name"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, title={self.name})"
