# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Type

import attr
from gooddata_api_client.model.filter_by import FilterBy

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogFilterBy(Base):
    label_type: str

    @staticmethod
    def client_class() -> Type[FilterBy]:
        return FilterBy
