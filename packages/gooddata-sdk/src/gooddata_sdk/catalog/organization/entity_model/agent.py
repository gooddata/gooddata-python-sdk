# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs
from gooddata_api_client.model.json_api_agent_in import JsonApiAgentIn
from gooddata_api_client.model.json_api_agent_in_attributes import JsonApiAgentInAttributes
from gooddata_api_client.model.json_api_agent_in_document import JsonApiAgentInDocument
from gooddata_api_client.model.json_api_agent_patch_document import JsonApiAgentPatchDocument

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.utils import safeget


@attrs.define(kw_only=True)
class CatalogAgentAttributes(Base):
    """Attributes of an AI agent entity."""

    title: str | None = None
    description: str | None = None
    ai_knowledge: bool | None = None
    available_to_all: bool | None = None
    custom_skills: list[str] | None = None
    enabled: bool | None = None
    personality: str | None = None
    skills_mode: str | None = None

    @staticmethod
    def client_class() -> type[JsonApiAgentInAttributes]:
        return JsonApiAgentInAttributes


@attrs.define(kw_only=True)
class CatalogAgent(Base):
    """Represents an AI agent entity with its configuration."""

    id: str
    attributes: CatalogAgentAttributes | None = None

    @staticmethod
    def client_class() -> type[JsonApiAgentIn]:
        return JsonApiAgentIn

    @classmethod
    def init(
        cls,
        id: str,
        title: str | None = None,
        description: str | None = None,
        ai_knowledge: bool | None = None,
        available_to_all: bool | None = None,
        custom_skills: list[str] | None = None,
        enabled: bool | None = None,
        personality: str | None = None,
        skills_mode: str | None = None,
    ) -> CatalogAgent:
        """Convenience factory for building a CatalogAgent."""
        return cls(
            id=id,
            attributes=CatalogAgentAttributes(
                title=title,
                description=description,
                ai_knowledge=ai_knowledge,
                available_to_all=available_to_all,
                custom_skills=custom_skills,
                enabled=enabled,
                personality=personality,
                skills_mode=skills_mode,
            ),
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogAgent:
        ea = entity.get("attributes") or {}
        return cls(
            id=entity["id"],
            attributes=CatalogAgentAttributes(
                title=safeget(ea, ["title"]),
                description=safeget(ea, ["description"]),
                ai_knowledge=safeget(ea, ["ai_knowledge"]),
                available_to_all=safeget(ea, ["available_to_all"]),
                custom_skills=safeget(ea, ["custom_skills"]),
                enabled=safeget(ea, ["enabled"]),
                personality=safeget(ea, ["personality"]),
                skills_mode=safeget(ea, ["skills_mode"]),
            ),
        )


@attrs.define(kw_only=True)
class CatalogAgentDocument(Base):
    """Wraps CatalogAgent for POST (create) requests."""

    data: CatalogAgent

    @staticmethod
    def client_class() -> type[JsonApiAgentInDocument]:
        return JsonApiAgentInDocument


@attrs.define(kw_only=True)
class CatalogAgentPatchDocument(Base):
    """Wraps CatalogAgent for PATCH requests."""

    data: CatalogAgent

    @staticmethod
    def client_class() -> type[JsonApiAgentPatchDocument]:
        return JsonApiAgentPatchDocument
