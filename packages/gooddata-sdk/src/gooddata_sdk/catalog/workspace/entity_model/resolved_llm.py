# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, Union

import attrs

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogResolvedLlmModelItem(Base):
    """A model entry returned as part of a resolved LLM provider."""

    id: str
    family: str

    @staticmethod
    def client_class() -> Any:
        from gooddata_api_client.model.llm_model import LlmModel

        return LlmModel

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlmModelItem:
        return cls(id=entity["id"], family=entity["family"])


@attrs.define(kw_only=True)
class CatalogResolvedLlmEndpoint(Base):
    """Resolved LLM configuration backed by an LLM endpoint."""

    id: str
    title: str

    @staticmethod
    def client_class() -> Any:
        from gooddata_api_client.model.resolved_llm_endpoint import ResolvedLlmEndpoint

        return ResolvedLlmEndpoint

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlmEndpoint:
        return cls(id=entity["id"], title=entity["title"])


@attrs.define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """Resolved LLM configuration backed by an LLM provider."""

    id: str
    title: str
    models: list[CatalogResolvedLlmModelItem] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> Any:
        from gooddata_api_client.model.resolved_llm_provider import ResolvedLlmProvider

        return ResolvedLlmProvider

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlmProvider:
        models = [CatalogResolvedLlmModelItem.from_api(m) for m in entity.get("models", [])]
        return cls(id=entity["id"], title=entity["title"], models=models)


CatalogResolvedLlmData = Union[CatalogResolvedLlmEndpoint, CatalogResolvedLlmProvider]


@attrs.define(kw_only=True)
class CatalogResolvedLlms(Base):
    """Container for the active LLM configuration resolved for a given workspace.

    The ``data`` field is ``None`` when no LLM is configured for the workspace.
    Otherwise it is either a :class:`CatalogResolvedLlmEndpoint` (when the
    workspace uses an LLM endpoint) or a :class:`CatalogResolvedLlmProvider`
    (when the workspace uses an LLM provider with associated models).
    """

    data: CatalogResolvedLlmData | None = None

    @staticmethod
    def client_class() -> Any:
        from gooddata_api_client.model.resolved_llms import ResolvedLlms

        return ResolvedLlms

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlms:
        raw_data = entity.get("data")
        if raw_data is None:
            return cls(data=None)
        # Distinguish endpoint from provider by the presence of the "models" key.
        if "models" in raw_data:
            return cls(data=CatalogResolvedLlmProvider.from_api(raw_data))
        return cls(data=CatalogResolvedLlmEndpoint.from_api(raw_data))
