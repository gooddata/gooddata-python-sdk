# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from attr import define

from gooddata_sdk.catalog.organization.entity_model.llm_provider import CatalogLlmProviderModel
from gooddata_sdk.utils import safeget


@define(kw_only=True)
class CatalogResolvedLlm:
    """Resolved LLM base — carries id and title shared by both providers and endpoints."""

    id: str
    title: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogResolvedLlm:
        return cls(
            id=data["id"],
            title=safeget(data, ["title"]),
        )


@define(kw_only=True)
class CatalogResolvedLlmProvider(CatalogResolvedLlm):
    """Resolved LLM provider — extends CatalogResolvedLlm with available models."""

    models: list[CatalogLlmProviderModel] = []

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogResolvedLlmProvider:
        raw_models = safeget(data, ["models"]) or []
        models = [
            CatalogLlmProviderModel(
                id=safeget(m, ["id"]),
                family=safeget(m, ["family"]),
            )
            for m in raw_models
        ]
        return cls(
            id=data["id"],
            title=safeget(data, ["title"]),
            models=models,
        )


@define(kw_only=True)
class CatalogResolvedLlms:
    """Wrapper for a list of resolved LLMs returned by the resolveLlmProviders endpoint."""

    data: list[CatalogResolvedLlm] | None = None

    @classmethod
    def from_api(cls, raw: dict[str, Any]) -> CatalogResolvedLlms:
        raw_data = safeget(raw, ["data"])
        if raw_data is None:
            return cls(data=None)
        items: list[CatalogResolvedLlm] = []
        for item in raw_data:
            item_type = safeget(item, ["type"])
            if item_type == "LLM_PROVIDER" or safeget(item, ["models"]) is not None:
                items.append(CatalogResolvedLlmProvider.from_api(item))
            else:
                items.append(CatalogResolvedLlm.from_api(item))
        return cls(data=items)
