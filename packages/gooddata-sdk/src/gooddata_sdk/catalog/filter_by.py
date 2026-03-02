# (C) 2024 GoodData Corporation
from __future__ import annotations

from attrs import define
from gooddata_api_client.model.filter_by import FilterBy

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogFilterBy(Base):
    label_type: str | None

    @staticmethod
    def client_class() -> type[FilterBy]:
        return FilterBy
