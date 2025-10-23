# (C) 2023 GoodData Corporation
from __future__ import annotations

from typing import Union

import attr
from gooddata_api_client.model.absolute_date_filter import AbsoluteDateFilter as AbsoluteDateFilterAPI
from gooddata_api_client.model.elements_request_depends_on_inner import ElementsRequestDependsOnInner
from gooddata_api_client.model.relative_date_filter import RelativeDateFilter as RelativeDateFilterAPI

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.compute.model.filter import AbsoluteDateFilter, RelativeDateFilter


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependsOn(Base):
    label: str
    values: list[str]
    complement_filter: bool = False

    @staticmethod
    def client_class() -> type[ElementsRequestDependsOnInner]:
        return ElementsRequestDependsOnInner


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependsOnDateFilter:
    date_filter: Union[AbsoluteDateFilter, RelativeDateFilter]

    def to_api(self) -> type[ElementsRequestDependsOnInner]:
        return CatalogDependsOnDateFilterItem(date_filter=self.date_filter.as_api_model()).to_api()


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDependsOnDateFilterItem(Base):
    date_filter: Union[AbsoluteDateFilterAPI, RelativeDateFilterAPI]

    @staticmethod
    def client_class() -> type[ElementsRequestDependsOnInner]:
        return ElementsRequestDependsOnInner
