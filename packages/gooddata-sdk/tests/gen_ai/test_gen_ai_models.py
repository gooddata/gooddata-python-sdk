# (C) 2024 GoodData Corporation
"""Unit tests for gen-ai catalog model classes."""

from __future__ import annotations

import pytest

from gooddata_sdk.catalog.workspace.gen_ai.conversation import (
    CatalogConversation,
    CatalogConversationFeedback,
    CatalogConversationItem,
    CatalogConversationTurnResponse,
    CatalogGenAiAllowedRelationshipType,
    CatalogSendMessageOptions,
    CatalogSendMessageSearchOptions,
)


class TestCatalogConversation:
    def test_from_api_dict_all_fields(self):
        data = {
            "conversationId": "conv-1",
            "workspaceId": "ws-1",
            "organizationId": "org-1",
            "userId": "user-1",
            "createdAt": "2024-01-01T00:00:00Z",
            "lastActivityAt": "2024-01-02T00:00:00Z",
        }
        obj = CatalogConversation.from_api_dict(data)
        assert obj.conversation_id == "conv-1"
        assert obj.workspace_id == "ws-1"
        assert obj.organization_id == "org-1"
        assert obj.user_id == "user-1"
        assert obj.created_at == "2024-01-01T00:00:00Z"
        assert obj.last_activity_at == "2024-01-02T00:00:00Z"


class TestCatalogConversationFeedback:
    def test_from_api_dict_positive_no_text(self):
        data = {"type": "POSITIVE"}
        obj = CatalogConversationFeedback.from_api_dict(data)
        assert obj.type == "POSITIVE"
        assert obj.text is None

    def test_from_api_dict_negative_with_text(self):
        data = {"type": "NEGATIVE", "text": "Not helpful"}
        obj = CatalogConversationFeedback.from_api_dict(data)
        assert obj.type == "NEGATIVE"
        assert obj.text == "Not helpful"

    def test_as_api_dict_without_text(self):
        obj = CatalogConversationFeedback(type="POSITIVE")
        d = obj.as_api_dict()
        assert d == {"type": "POSITIVE"}
        assert "text" not in d

    def test_as_api_dict_with_text(self):
        obj = CatalogConversationFeedback(type="NEGATIVE", text="some comment")
        d = obj.as_api_dict()
        assert d == {"type": "NEGATIVE", "text": "some comment"}


class TestCatalogConversationTurnResponse:
    def test_from_api_dict_without_feedback(self):
        data = {
            "responseId": "resp-1",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:01:00Z",
        }
        obj = CatalogConversationTurnResponse.from_api_dict(data)
        assert obj.response_id == "resp-1"
        assert obj.created_at == "2024-01-01T00:00:00Z"
        assert obj.updated_at == "2024-01-01T00:01:00Z"
        assert obj.feedback is None

    def test_from_api_dict_with_feedback(self):
        data = {
            "responseId": "resp-2",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:01:00Z",
            "feedback": {"type": "POSITIVE", "text": "Great!"},
        }
        obj = CatalogConversationTurnResponse.from_api_dict(data)
        assert obj.feedback is not None
        assert obj.feedback.type == "POSITIVE"
        assert obj.feedback.text == "Great!"

    def test_from_api_dict_with_null_feedback(self):
        data = {
            "responseId": "resp-3",
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:01:00Z",
            "feedback": None,
        }
        obj = CatalogConversationTurnResponse.from_api_dict(data)
        assert obj.feedback is None


class TestCatalogConversationItem:
    def test_from_api_dict_required_fields(self):
        data = {
            "itemId": "item-1",
            "conversationId": "conv-1",
            "itemIndex": 0,
            "createdAt": "2024-01-01T00:00:00Z",
            "role": "user",
            "content": {"type": "text", "text": "Hello"},
        }
        obj = CatalogConversationItem.from_api_dict(data)
        assert obj.item_id == "item-1"
        assert obj.conversation_id == "conv-1"
        assert obj.item_index == 0
        assert obj.role == "user"
        assert obj.content.type == "text"
        assert obj.response_id is None
        assert obj.reply_to is None
        assert obj.task_id is None

    def test_from_api_dict_optional_fields(self):
        data = {
            "itemId": "item-2",
            "conversationId": "conv-1",
            "itemIndex": 1,
            "createdAt": "2024-01-01T00:00:00Z",
            "role": "assistant",
            "content": {"type": "text", "text": "Hi there"},
            "responseId": "resp-1",
            "replyTo": "item-1",
            "taskId": "task-1",
        }
        obj = CatalogConversationItem.from_api_dict(data)
        assert obj.response_id == "resp-1"
        assert obj.reply_to == "item-1"
        assert obj.task_id == "task-1"


class TestCatalogGenAiAllowedRelationshipType:
    def test_as_api_dict_without_allow_orphans(self):
        obj = CatalogGenAiAllowedRelationshipType(source_type="dataset", target_type="metric")
        d = obj.as_api_dict()
        assert d == {"sourceType": "dataset", "targetType": "metric"}
        assert "allowOrphans" not in d

    def test_as_api_dict_with_allow_orphans(self):
        obj = CatalogGenAiAllowedRelationshipType(source_type="dataset", target_type="metric", allow_orphans=False)
        d = obj.as_api_dict()
        assert d == {"sourceType": "dataset", "targetType": "metric", "allowOrphans": False}

    def test_from_api_dict(self):
        data = {"sourceType": "dataset", "targetType": "fact", "allowOrphans": True}
        obj = CatalogGenAiAllowedRelationshipType.from_api_dict(data)
        assert obj.source_type == "dataset"
        assert obj.target_type == "fact"
        assert obj.allow_orphans is True


class TestCatalogSendMessageSearchOptions:
    def test_as_api_dict_empty(self):
        obj = CatalogSendMessageSearchOptions()
        assert obj.as_api_dict() == {}

    def test_as_api_dict_with_object_types(self):
        obj = CatalogSendMessageSearchOptions(object_types=["metric", "dataset"])
        d = obj.as_api_dict()
        assert d == {"objectTypes": ["metric", "dataset"]}

    def test_as_api_dict_with_search_limit(self):
        obj = CatalogSendMessageSearchOptions(search_limit=10)
        d = obj.as_api_dict()
        assert d == {"searchLimit": 10}

    def test_as_api_dict_with_allowed_relationship_types(self):
        art = CatalogGenAiAllowedRelationshipType(source_type="dataset", target_type="metric")
        obj = CatalogSendMessageSearchOptions(allowed_relationship_types=[art])
        d = obj.as_api_dict()
        assert "allowedRelationshipTypes" in d
        assert d["allowedRelationshipTypes"] == [{"sourceType": "dataset", "targetType": "metric"}]

    def test_from_api_dict_empty(self):
        obj = CatalogSendMessageSearchOptions.from_api_dict({})
        assert obj.object_types is None
        assert obj.search_limit is None
        assert obj.allowed_relationship_types is None

    def test_from_api_dict_full(self):
        data = {
            "objectTypes": ["fact", "label"],
            "searchLimit": 25,
            "allowedRelationshipTypes": [{"sourceType": "dataset", "targetType": "fact"}],
        }
        obj = CatalogSendMessageSearchOptions.from_api_dict(data)
        assert obj.object_types == ["fact", "label"]
        assert obj.search_limit == 25
        assert obj.allowed_relationship_types is not None
        assert len(obj.allowed_relationship_types) == 1
        assert obj.allowed_relationship_types[0].source_type == "dataset"


class TestCatalogSendMessageOptions:
    def test_as_api_dict_no_search(self):
        obj = CatalogSendMessageOptions()
        assert obj.as_api_dict() == {}

    def test_as_api_dict_with_search(self):
        search = CatalogSendMessageSearchOptions(object_types=["metric"])
        obj = CatalogSendMessageOptions(search=search)
        d = obj.as_api_dict()
        assert d == {"search": {"objectTypes": ["metric"]}}

    def test_from_api_dict_no_search(self):
        obj = CatalogSendMessageOptions.from_api_dict({})
        assert obj.search is None

    def test_from_api_dict_with_search(self):
        data = {"search": {"objectTypes": ["dashboard"], "searchLimit": 5}}
        obj = CatalogSendMessageOptions.from_api_dict(data)
        assert obj.search is not None
        assert obj.search.object_types == ["dashboard"]
        assert obj.search.search_limit == 5
