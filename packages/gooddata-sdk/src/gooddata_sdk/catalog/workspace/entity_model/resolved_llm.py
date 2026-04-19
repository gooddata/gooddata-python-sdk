# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, Union

import attrs

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class CatalogResolvedLlmModel(Base):
    """An LLM model available for a resolved LLM provider."""

    id: str
    family: str

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlmModel:
        return cls(id=entity["id"], family=entity["family"])


@attrs.define(kw_only=True)
class CatalogResolvedLlmEndpoint(Base):
    """Legacy resolved LLM endpoint returned when ENABLE_LLM_ENDPOINT_REPLACEMENT is disabled."""

    id: str
    title: str

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlmEndpoint:
        return cls(id=entity["id"], title=entity["title"])


@attrs.define(kw_only=True)
class CatalogResolvedLlmProvider(Base):
    """Resolved LLM provider with associated models, returned when ENABLE_LLM_ENDPOINT_REPLACEMENT is enabled."""

    id: str
    title: str
    models: list[CatalogResolvedLlmModel] = attrs.field(factory=list)

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlmProvider:
        return cls(
            id=entity["id"],
            title=entity["title"],
            models=[CatalogResolvedLlmModel.from_api(m) for m in entity.get("models", [])],
        )


CatalogResolvedLlmsData = Union[CatalogResolvedLlmEndpoint, CatalogResolvedLlmProvider]


def _resolved_llms_data_from_api(data: dict[str, Any]) -> CatalogResolvedLlmsData:
    """Distinguish between endpoint and provider based on presence of the 'models' field."""
    if "models" in data:
        return CatalogResolvedLlmProvider.from_api(data)
    return CatalogResolvedLlmEndpoint.from_api(data)


@attrs.define(kw_only=True)
class CatalogResolvedLlms(Base):
    """The resolved LLM configuration for a workspace.

    The ``data`` field is either a :class:`CatalogResolvedLlmProvider` (when
    the ``ENABLE_LLM_ENDPOINT_REPLACEMENT`` feature flag is enabled) or a
    :class:`CatalogResolvedLlmEndpoint` (legacy fallback), or ``None`` if no
    LLM is configured for the workspace.
    """

    data: CatalogResolvedLlmsData | None = None

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogResolvedLlms:
        raw_data = entity.get("data")
        if raw_data is None:
            return cls(data=None)
        return cls(data=_resolved_llms_data_from_api(raw_data))
