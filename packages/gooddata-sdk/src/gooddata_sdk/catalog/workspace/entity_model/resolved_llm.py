# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.llm_model import LlmModel
from gooddata_api_client.model.resolved_llm_provider import ResolvedLlmProvider
from gooddata_api_client.model.resolved_llms import ResolvedLlms

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogResolvedLlmModel(Base):
    """A single LLM model associated with a resolved LLM provider."""

    id: str
    family: str

    @staticmethod
    def client_class() -> type[LlmModel]:
        return LlmModel


@attrs.define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """Resolved LLM provider for a workspace.

    Represents either a ResolvedLlmProvider (when ENABLE_LLM_ENDPOINT_REPLACEMENT
    feature flag is enabled) or a ResolvedLlmEndpoint (legacy fallback).
    When the legacy endpoint is returned, models will be an empty list.
    """

    id: str
    title: str
    models: list[CatalogResolvedLlmModel] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type[ResolvedLlmProvider]:
        return ResolvedLlmProvider

    @classmethod
    def from_api(cls, entity: Any) -> CatalogResolvedLlmProvider:
        raw_models = getattr(entity, "models", None) or []
        models = [CatalogResolvedLlmModel(id=m.id, family=m.family) for m in raw_models]
        return cls(
            id=entity.id,
            title=entity.title,
            models=models,
        )


@attrs.define(kw_only=True)
class CatalogResolvedLlms(Base):
    """Response from the resolveLlmProviders workspace action endpoint.

    Contains the active LLM configuration for a given workspace.
    The data field is present when an active LLM configuration exists.
    """

    data: CatalogResolvedLlmProvider | None = None

    @staticmethod
    def client_class() -> type[ResolvedLlms]:
        return ResolvedLlms

    @classmethod
    def from_api(cls, entity: Any) -> CatalogResolvedLlms:
        raw_data = getattr(entity, "data", None)
        if raw_data is None:
            return cls(data=None)
        return cls(data=CatalogResolvedLlmProvider.from_api(raw_data))
