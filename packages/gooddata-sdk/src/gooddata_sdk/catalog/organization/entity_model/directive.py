# (C) 2023 GoodData Corporation
from __future__ import annotations

import attr
from gooddata_api_client.model.json_api_csp_directive_in import JsonApiCspDirectiveIn
from gooddata_api_client.model.json_api_csp_directive_in_attributes import JsonApiCspDirectiveInAttributes

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogCspDirective(Base):
    id: str
    attributes: CatalogCspDirectiveAttributes

    @classmethod
    def init(cls, directive_id: str, sources: list[str]) -> CatalogCspDirective:
        return cls(id=directive_id, attributes=CatalogCspDirectiveAttributes(sources=sources))

    @staticmethod
    def client_class() -> type[JsonApiCspDirectiveIn]:
        return JsonApiCspDirectiveIn


@attr.s(auto_attribs=True, kw_only=True)
class CatalogCspDirectiveAttributes(Base):
    sources: list[str]

    @staticmethod
    def client_class() -> type[JsonApiCspDirectiveInAttributes]:
        return JsonApiCspDirectiveInAttributes
