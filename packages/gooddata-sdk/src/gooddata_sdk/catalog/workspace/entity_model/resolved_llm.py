# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogResolvedLlmModel(Base):
    """Represents a single LLM model available in the resolved LLM configuration."""

    id: str
    family: str | None = None

    @staticmethod
    def client_class() -> Any:
        return NotImplemented

    @classmethod
    def from_api(cls, data: Any) -> CatalogResolvedLlmModel:
        family = None
        try:
            family = data["family"]
        except (KeyError, TypeError):
            pass
        return cls(
            id=data["id"],
            family=family,
        )


@attrs.define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """Represents a resolved LLM provider configuration for a workspace.

    Returned by the resolveLlmProviders endpoint. When the ENABLE_LLM_ENDPOINT_REPLACEMENT
    feature flag is enabled, contains LLM provider information with associated models.
    Otherwise, falls back to the legacy LLM endpoint representation.
    """

    id: str
    title: str | None = None
    models: list[CatalogResolvedLlmModel] = attrs.field(factory=list)

    @staticmethod
    def client_class() -> Any:
        return NotImplemented

    @classmethod
    def from_api(cls, data: Any) -> CatalogResolvedLlmProvider:
        raw_models = None
        try:
            raw_models = data["models"]
        except (KeyError, TypeError):
            pass
        models = [CatalogResolvedLlmModel.from_api(m) for m in raw_models] if raw_models is not None else []
        title = None
        try:
            title = data["title"]
        except (KeyError, TypeError):
            pass
        return cls(
            id=data["id"],
            title=title,
            models=models,
        )


@attrs.define(kw_only=True)
class CatalogResolvedLlms(Base):
    """Represents the resolved LLM configuration for a workspace.

    Returned by the resolveLlmProviders endpoint. The data field contains the active
    LLM configuration, or None if no LLM is configured for the workspace.
    """

    data: CatalogResolvedLlmProvider | None = None

    @staticmethod
    def client_class() -> Any:
        return NotImplemented

    @classmethod
    def from_api(cls, response: Any) -> CatalogResolvedLlms:
        data_raw = None
        try:
            data_raw = response["data"]
        except (KeyError, TypeError):
            pass
        if data_raw is None:
            return cls(data=None)
        return cls(data=CatalogResolvedLlmProvider.from_api(data_raw))
