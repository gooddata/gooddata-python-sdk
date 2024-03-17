# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import List, Type

import attr
from gooddata_api_client.model.elements_request_depends_on_inner import ElementsRequestDependsOnInner

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependsOn(Base):
    label: str
    values: List[str]
    complement_filter: bool = False

    @staticmethod
    def client_class() -> Type[ElementsRequestDependsOnInner]:
        return ElementsRequestDependsOnInner
