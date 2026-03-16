# (C) 2024 GoodData Corporation
"""Catalog model classes for the gen-ai conversation HTTP API."""
from __future__ import annotations

from typing import Any

import attrs

# ObjectType values from the OpenAPI spec ObjectType enum
GenAiObjectType = str
"""Type alias for gen-ai ObjectType enum values.

Allowed values: 'unidentified', 'workspace', 'dataset', 'date', 'fact', 'metric',
'attribute', 'date_attribute', 'label', 'visualization', 'dashboard', 'filter_context'
"""

# FeedbackType values from the OpenAPI spec FeedbackDto.type enum
GenAiFeedbackType = str
"""Type alias for gen-ai feedback type enum values. Allowed values: 'POSITIVE', 'NEGATIVE'."""


@attrs.define(kw_only=True)
class CatalogGenAiAllowedRelationshipType:
    """Wraps AllowedRelationshipTypeDto — specifies allowed relationship traversal for search."""

    source_type: str
    target_type: str
    allow_orphans: bool | None = None

    def as_api_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "sourceType": self.source_type,
            "targetType": self.target_type,
        }
        if self.allow_orphans is not None:
            d["allowOrphans"] = self.allow_orphans
        return d

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogGenAiAllowedRelationshipType:
        return cls(
            source_type=data["sourceType"],
            target_type=data["targetType"],
            allow_orphans=data.get("allowOrphans"),
        )


@attrs.define(kw_only=True)
class CatalogSendMessageSearchOptions:
    """Wraps SendMessageSearchOptionsDto — controls vector search behaviour when sending a message."""

    object_types: list[GenAiObjectType] | None = None
    search_limit: int | None = None
    allowed_relationship_types: list[CatalogGenAiAllowedRelationshipType] | None = None

    def as_api_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.object_types is not None:
            d["objectTypes"] = list(self.object_types)
        if self.search_limit is not None:
            d["searchLimit"] = self.search_limit
        if self.allowed_relationship_types is not None:
            d["allowedRelationshipTypes"] = [r.as_api_dict() for r in self.allowed_relationship_types]
        return d

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogSendMessageSearchOptions:
        art_raw = data.get("allowedRelationshipTypes")
        art = [CatalogGenAiAllowedRelationshipType.from_api_dict(r) for r in art_raw] if art_raw else None
        return cls(
            object_types=data.get("objectTypes"),
            search_limit=data.get("searchLimit"),
            allowed_relationship_types=art,
        )


@attrs.define(kw_only=True)
class CatalogSendMessageOptions:
    """Wraps SendMessageOptionsDto — optional options for POST /conversations/{id}/messages."""

    search: CatalogSendMessageSearchOptions | None = None

    def as_api_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.search is not None:
            d["search"] = self.search.as_api_dict()
        return d

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogSendMessageOptions:
        search_raw = data.get("search")
        return cls(
            search=CatalogSendMessageSearchOptions.from_api_dict(search_raw) if search_raw else None,
        )


@attrs.define(kw_only=True)
class CatalogConversationFeedback:
    """Wraps FeedbackDto — user feedback attached to a conversation turn response."""

    type: GenAiFeedbackType
    text: str | None = None

    def as_api_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self.type}
        if self.text is not None:
            d["text"] = self.text
        return d

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogConversationFeedback:
        return cls(
            type=data["type"],
            text=data.get("text"),
        )


@attrs.define(kw_only=True)
class CatalogConversationTurnResponse:
    """Wraps ConversationTurnResponseDto — a conversation turn response, optionally with feedback."""

    response_id: str
    created_at: str
    updated_at: str
    feedback: CatalogConversationFeedback | None = None

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogConversationTurnResponse:
        feedback_raw = data.get("feedback")
        return cls(
            response_id=data["responseId"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"],
            feedback=CatalogConversationFeedback.from_api_dict(feedback_raw) if feedback_raw else None,
        )


@attrs.define(kw_only=True)
class CatalogConversationItemContent:
    """Wraps the content payload of a ConversationItemResponseDto (simplified view)."""

    type: str
    raw: dict[str, Any] = attrs.field(factory=dict)

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogConversationItemContent:
        return cls(
            type=data.get("type", ""),
            raw=dict(data),
        )


@attrs.define(kw_only=True)
class CatalogConversationItem:
    """Wraps ConversationItemResponseDto — an individual item within a conversation."""

    item_id: str
    conversation_id: str
    item_index: int
    created_at: str
    role: str
    content: CatalogConversationItemContent
    response_id: str | None = None
    reply_to: str | None = None
    task_id: str | None = None

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogConversationItem:
        return cls(
            item_id=data["itemId"],
            conversation_id=data["conversationId"],
            item_index=data["itemIndex"],
            created_at=data["createdAt"],
            role=data["role"],
            content=CatalogConversationItemContent.from_api_dict(data["content"]),
            response_id=data.get("responseId"),
            reply_to=data.get("replyTo"),
            task_id=data.get("taskId"),
        )


@attrs.define(kw_only=True)
class CatalogConversation:
    """Wraps ConversationResponseDto — a conversation within a workspace."""

    conversation_id: str
    workspace_id: str
    organization_id: str
    user_id: str
    created_at: str
    last_activity_at: str

    @classmethod
    def from_api_dict(cls, data: dict[str, Any]) -> CatalogConversation:
        return cls(
            conversation_id=data["conversationId"],
            workspace_id=data["workspaceId"],
            organization_id=data["organizationId"],
            user_id=data["userId"],
            created_at=data["createdAt"],
            last_activity_at=data["lastActivityAt"],
        )
