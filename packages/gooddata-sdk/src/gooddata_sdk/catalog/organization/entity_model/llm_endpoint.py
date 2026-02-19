# (C) 2024 GoodData Corporation
from __future__ import annotations

from typing import Any

from attr import define
from gooddata_api_client.model.json_api_llm_endpoint_in import JsonApiLlmEndpointIn
from gooddata_api_client.model.json_api_llm_endpoint_in_attributes import JsonApiLlmEndpointInAttributes
from gooddata_api_client.model.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.model.json_api_llm_endpoint_patch import JsonApiLlmEndpointPatch
from gooddata_api_client.model.json_api_llm_endpoint_patch_attributes import JsonApiLlmEndpointPatchAttributes
from gooddata_api_client.model.json_api_llm_endpoint_patch_document import JsonApiLlmEndpointPatchDocument

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@define(kw_only=True)
class CatalogLlmEndpointDocument(Base):
    data: CatalogLlmEndpoint

    @staticmethod
    def client_class() -> type[JsonApiLlmEndpointInDocument]:
        return JsonApiLlmEndpointInDocument


@define(kw_only=True)
class CatalogLlmEndpointPatchDocument(Base):
    data: CatalogLlmEndpointPatch

    @staticmethod
    def client_class() -> type[JsonApiLlmEndpointPatchDocument]:
        return JsonApiLlmEndpointPatchDocument


@define(kw_only=True)
class CatalogLlmEndpoint(Base):
    id: str
    attributes: CatalogLlmEndpointAttributes | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmEndpointIn]:
        return JsonApiLlmEndpointIn

    @classmethod
    def init(
        cls,
        id: str,
        title: str,
        token: str,
        provider: str | None = None,
        base_url: str | None = None,
        llm_organization: str | None = None,
        llm_model: str | None = None,
    ) -> CatalogLlmEndpoint:
        return cls(
            id=id,
            attributes=CatalogLlmEndpointAttributes(
                title=title,
                token=token,
                provider=provider,
                base_url=base_url,
                llm_organization=llm_organization,
                llm_model=llm_model,
            ),
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogLlmEndpoint:
        ea = entity["attributes"]
        attr = CatalogLlmEndpointAttributes(
            title=safeget(ea, ["title"]),
            token="",  # Token is not returned for security reasons
            provider=safeget(ea, ["provider"]),
            base_url=safeget(ea, ["baseUrl"]),
            llm_organization=safeget(ea, ["llmOrganization"]),
            llm_model=safeget(ea, ["llmModel"]),
        )
        return cls(
            id=entity["id"],
            attributes=attr,
        )


@define(kw_only=True)
class CatalogLlmEndpointPatch(Base):
    id: str
    attributes: CatalogLlmEndpointPatchAttributes | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmEndpointPatch]:
        return JsonApiLlmEndpointPatch

    @classmethod
    def init(
        cls,
        id: str,
        title: str | None = None,
        token: str | None = None,
        provider: str | None = None,
        base_url: str | None = None,
        llm_organization: str | None = None,
        llm_model: str | None = None,
    ) -> CatalogLlmEndpointPatch:
        return cls(
            id=id,
            attributes=CatalogLlmEndpointPatchAttributes(
                title=title,
                token=token,
                provider=provider,
                base_url=base_url,
                llm_organization=llm_organization,
                llm_model=llm_model,
            ),
        )


@define(kw_only=True)
class CatalogLlmEndpointAttributes(Base):
    title: str
    token: str
    provider: str | None = None
    base_url: str | None = None
    llm_organization: str | None = None
    llm_model: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmEndpointInAttributes]:
        return JsonApiLlmEndpointInAttributes


@define(kw_only=True)
class CatalogLlmEndpointPatchAttributes(Base):
    title: str | None = None
    token: str | None = None
    provider: str | None = None
    base_url: str | None = None
    llm_organization: str | None = None
    llm_model: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiLlmEndpointPatchAttributes]:
        return JsonApiLlmEndpointPatchAttributes
