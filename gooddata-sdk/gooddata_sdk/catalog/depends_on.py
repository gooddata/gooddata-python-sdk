# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import List, Optional, Type

import attr

from gooddata_api_client.model.depends_on import DependsOn
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependsOn(Base):
    label: str
    values: List[str]
    complement_filter: Optional[bool] = None

    @staticmethod
    def client_class() -> Type[DependsOn]:
        return DependsOn
