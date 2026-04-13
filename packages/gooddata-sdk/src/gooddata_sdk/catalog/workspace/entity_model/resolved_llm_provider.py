# (C) 2026 GoodData Corporation
from __future__ import annotations

import attrs

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogResolvedLlmModel(Base):
    """Represents a single model available from a resolved LLM provider."""

    id: str
    family: str

    @staticmethod
    def client_class() -> type:
        from gooddata_api_client.model.llm_model import LlmModel

        return LlmModel


@attrs.define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """The resolved LLM provider configuration for a workspace."""

    id: str
    title: str
    models: list[CatalogResolvedLlmModel] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type:
        from gooddata_api_client.model.resolved_llm_provider import ResolvedLlmProvider

        return ResolvedLlmProvider

    @classmethod
    def from_dict(cls, data: dict) -> CatalogResolvedLlmProvider:  # type: ignore[override]
        models = [CatalogResolvedLlmModel(id=m["id"], family=m["family"]) for m in data.get("models", [])]
        return cls(
            id=data["id"],
            title=data["title"],
            models=models,
        )
