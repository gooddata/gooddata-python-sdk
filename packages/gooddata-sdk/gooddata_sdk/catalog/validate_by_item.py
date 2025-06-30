# (C) 2023 GoodData Corporation
from __future__ import annotations

import builtins

import attr
from gooddata_api_client.model.validate_by_item import ValidateByItem

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogValidateByItem(Base):
    id: str
    type: str

    @staticmethod
    def client_class() -> builtins.type[ValidateByItem]:
        return ValidateByItem
