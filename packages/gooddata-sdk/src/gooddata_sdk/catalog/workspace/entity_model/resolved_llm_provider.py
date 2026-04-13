# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.resolved_llm_provider import ResolvedLlmProvider
from gooddata_api_client.model.resolved_llms import ResolvedLlms

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@attrs.define(kw_only=True)
class CatalogResolvedLlmModel(Base):
    """A single LLM model available from a resolved LLM provider."""

    id: str
    family: str | None = None

    @staticmethod
    def client_class() -> type:
        from gooddata_api_client.model.llm_model import LlmModel

        return LlmModel

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogResolvedLlmModel:
        return cls(
            id=data["id"],
            family=data.get("family"),
        )


@attrs.define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """Resolved LLM provider configuration for a workspace."""

    id: str
    title: str
    models: list[CatalogResolvedLlmModel] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[ResolvedLlmProvider]:
        return ResolvedLlmProvider

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogResolvedLlmProvider:
        models = [CatalogResolvedLlmModel.from_api(m) for m in (data.get("models") or [])]
        return cls(
            id=data["id"],
            title=data["title"],
            models=models,
        )


@attrs.define(kw_only=True)
class CatalogResolvedLlms(Base):
    """Container for resolved LLM configuration for a workspace.

    Wraps the response from the resolveLlmProviders endpoint.
    The ``data`` field holds the active LLM provider, or ``None`` if
    no provider is configured for the workspace.
    """

    data: CatalogResolvedLlmProvider | None = None

    @staticmethod
    def client_class() -> type[ResolvedLlms]:
        return ResolvedLlms

    @classmethod
    def from_api(cls, response: Any) -> CatalogResolvedLlms:
        response_dict = response.to_dict() if hasattr(response, "to_dict") else response
        data_dict = safeget(response_dict, ["data"])
        if data_dict is None:
            return cls(data=None)
        return cls(data=CatalogResolvedLlmProvider.from_api(data_dict))
