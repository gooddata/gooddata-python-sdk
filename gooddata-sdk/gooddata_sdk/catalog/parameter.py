# (C) 2022 GoodData Corporation
from typing import Type

import attr

from gooddata_api_client.model.parameter import Parameter
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogParameter(Base):
    name: str
    value: str

    @staticmethod
    def client_class() -> Type[Parameter]:
        return Parameter
