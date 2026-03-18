# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from attr import define


@define(kw_only=True)
class CatalogResolvedLlmModel:
    """A resolved LLM model with id and family."""

    id: str
    family: str


@define(kw_only=True)
class CatalogResolvedLlm:
    """Base resolved LLM with id and title."""

    id: str
    title: str


@define(kw_only=True)
class CatalogResolvedLlmProvider:
    """A resolved LLM provider with associated models."""

    id: str
    title: str
    models: list[CatalogResolvedLlmModel]

    @classmethod
    def from_api_model(cls, obj: Any) -> CatalogResolvedLlmProvider:
        raw_models = getattr(obj, "models", None) or []
        models = [CatalogResolvedLlmModel(id=m.id, family=m.family) for m in raw_models]
        return cls(id=obj.id, title=obj.title, models=models)


@define(kw_only=True)
class CatalogResolvedLlms:
    """Wrapper for the resolved LLMs response."""

    data: CatalogResolvedLlmProvider | None = None

    @classmethod
    def from_api_model(cls, obj: Any) -> CatalogResolvedLlms:
        raw_data = getattr(obj, "data", None)
        if raw_data is None:
            return cls(data=None)
        # Discriminate by presence of models field — provider has models, endpoint does not
        if getattr(raw_data, "models", None) is not None:
            return cls(data=CatalogResolvedLlmProvider.from_api_model(raw_data))
        return cls(data=None)
