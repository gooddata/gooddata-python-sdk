# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import List, Optional, Type

import attr
from gooddata_api_client.model.json_api_jwk_in import JsonApiJwkIn
from gooddata_api_client.model.json_api_jwk_in_attributes import JsonApiJwkInAttributes
from gooddata_api_client.model.json_api_jwk_in_attributes_content import JsonApiJwkInAttributesContent
from gooddata_api_client.model.json_api_jwk_in_document import JsonApiJwkInDocument

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogJwkDocument(Base):
    data: CatalogJwk

    @staticmethod
    def client_class() -> Type[JsonApiJwkInDocument]:
        return JsonApiJwkInDocument


@attr.s(auto_attribs=True, kw_only=True)
class CatalogJwk(Base):
    id: str
    attributes: Optional[CatalogJwkAttributes] = None

    @staticmethod
    def client_class() -> Type[JsonApiJwkIn]:
        return JsonApiJwkIn

    @classmethod
    def init(
        cls,
        jwk_id: str,
        rsa_spec: Optional[CatalogRsaSpecification] = None,
    ) -> CatalogJwk:
        return cls(id=jwk_id, attributes=CatalogJwkAttributes(content=rsa_spec))


@attr.s(auto_attribs=True, kw_only=True)
class CatalogJwkAttributes(Base):
    content: Optional[CatalogRsaSpecification] = None

    @staticmethod
    def client_class() -> Type[JsonApiJwkInAttributes]:
        return JsonApiJwkInAttributes


@attr.s(auto_attribs=True, kw_only=True)
class CatalogRsaSpecification(Base):
    alg: str
    e: str
    kid: str
    kty: str
    n: str
    use: str
    x5c: List[str]
    x5t: str

    @staticmethod
    def client_class() -> Type[JsonApiJwkInAttributesContent]:
        return JsonApiJwkInAttributesContent
