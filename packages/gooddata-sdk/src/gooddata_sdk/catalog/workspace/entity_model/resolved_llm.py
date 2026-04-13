# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@attrs.define(kw_only=True)
class CatalogResolvedLlmModel(Base):
    """Represents a single LLM model returned by the resolveLlmProviders endpoint."""

    id: str
    family: str

    @staticmethod
    def client_class() -> type:
        return NotImplemented


@attrs.define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """Represents the resolved LLM provider configuration for a workspace."""

    id: str
    title: str
    models: list[CatalogResolvedLlmModel] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> type:
        return NotImplemented

    @classmethod
    def from_api(cls, data: Any) -> CatalogResolvedLlmProvider:
        raw_models = safeget(data, ["models"]) or []
        models = [
            CatalogResolvedLlmModel(
                id=safeget(m, ["id"]) or m["id"],
                family=safeget(m, ["family"]) or m["family"],
            )
            for m in raw_models
        ]
        return cls(
            id=data["id"],
            title=data["title"],
            models=models,
        )


@attrs.define(kw_only=True)
class CatalogResolvedLlms(Base):
    """Wraps the response from the resolveLlmProviders endpoint.

    Contains the active LLM configuration for a workspace, or None if none is configured.
    """

    data: CatalogResolvedLlmProvider | None = None

    @staticmethod
    def client_class() -> type:
        return NotImplemented

    @classmethod
    def from_api(cls, response: Any) -> CatalogResolvedLlms:
        raw_data = safeget(response, ["data"])
        if raw_data is None:
            return cls(data=None)
        provider = CatalogResolvedLlmProvider.from_api(raw_data)
        return cls(data=provider)
