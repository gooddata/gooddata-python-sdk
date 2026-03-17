# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

from attr import define

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.organization.entity_model.llm_provider import CatalogLlmProviderModel
from gooddata_sdk.utils import safeget


@define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """Resolved LLM provider for a workspace."""

    id: str
    title: str | None = None
    models: list[CatalogLlmProviderModel] | None = None

    @staticmethod
    def client_class() -> type:
        raise NotImplementedError()

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogResolvedLlmProvider:
        raw_models = safeget(data, ["models"]) or []
        models = [
            CatalogLlmProviderModel(
                id=safeget(m, ["id"]) or "",
                family=safeget(m, ["family"]) or "",
            )
            for m in raw_models
        ]
        return cls(
            id=safeget(data, ["id"]) or "",
            title=safeget(data, ["title"]),
            models=models if models else None,
        )


@define(kw_only=True)
class CatalogResolvedLlmEndpoint(Base):
    """Resolved LLM endpoint for a workspace (deprecated legacy type)."""

    id: str
    title: str | None = None

    @staticmethod
    def client_class() -> type:
        raise NotImplementedError()

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogResolvedLlmEndpoint:
        return cls(
            id=safeget(data, ["id"]) or "",
            title=safeget(data, ["title"]),
        )


@define(kw_only=True)
class CatalogResolvedLlms(Base):
    """Container for resolved LLM configuration of a workspace."""

    data: list[CatalogResolvedLlmProvider | CatalogResolvedLlmEndpoint] | None = None

    @staticmethod
    def client_class() -> type:
        raise NotImplementedError()

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CatalogResolvedLlms:
        raw_data = safeget(data, ["data"])
        if raw_data is None:
            return cls(data=None)
        items: list[CatalogResolvedLlmProvider | CatalogResolvedLlmEndpoint] = []
        for item in raw_data if isinstance(raw_data, list) else [raw_data]:
            # Dispatch: providers have "models" field; endpoints do not
            if safeget(item, ["models"]) is not None:
                items.append(CatalogResolvedLlmProvider.from_api(item))
            else:
                items.append(CatalogResolvedLlmEndpoint.from_api(item))
        return cls(data=items if items else None)
