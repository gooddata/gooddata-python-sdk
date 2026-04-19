# (C) 2026 GoodData Corporation
from __future__ import annotations

import pytest
from gooddata_sdk.compute.model.ai_chat import ConversationFeedback, ConversationResponseList, ConversationTurnResponse


class TestConversationFeedback:
    def test_from_api_positive(self) -> None:
        data = {"type": "POSITIVE"}
        feedback = ConversationFeedback.from_api(data)
        assert feedback.type == "POSITIVE"
        assert feedback.text is None

    def test_from_api_negative_with_text(self) -> None:
        data = {"type": "NEGATIVE", "text": "The answer was wrong"}
        feedback = ConversationFeedback.from_api(data)
        assert feedback.type == "NEGATIVE"
        assert feedback.text == "The answer was wrong"

    def test_to_api_dict_without_text(self) -> None:
        feedback = ConversationFeedback(type="POSITIVE")
        result = feedback.to_api_dict()
        assert result == {"type": "POSITIVE"}
        assert "text" not in result

    def test_to_api_dict_with_text(self) -> None:
        feedback = ConversationFeedback(type="NEGATIVE", text="Not helpful")
        result = feedback.to_api_dict()
        assert result == {"type": "NEGATIVE", "text": "Not helpful"}

    @pytest.mark.parametrize("feedback_type", ["POSITIVE", "NEGATIVE"])
    def test_roundtrip(self, feedback_type: str) -> None:
        original = ConversationFeedback(type=feedback_type, text="some comment")
        restored = ConversationFeedback.from_api(original.to_api_dict())
        assert restored.type == original.type
        assert restored.text == original.text


class TestConversationTurnResponse:
    def test_from_api_without_feedback(self) -> None:
        data = {
            "responseId": "resp-123",
            "createdAt": "2026-01-01T00:00:00Z",
            "updatedAt": "2026-01-01T00:01:00Z",
        }
        turn = ConversationTurnResponse.from_api(data)
        assert turn.response_id == "resp-123"
        assert turn.created_at == "2026-01-01T00:00:00Z"
        assert turn.updated_at == "2026-01-01T00:01:00Z"
        assert turn.feedback is None

    def test_from_api_with_feedback(self) -> None:
        data = {
            "responseId": "resp-456",
            "createdAt": "2026-02-01T10:00:00Z",
            "updatedAt": "2026-02-01T10:05:00Z",
            "feedback": {"type": "POSITIVE", "text": "Great answer!"},
        }
        turn = ConversationTurnResponse.from_api(data)
        assert turn.response_id == "resp-456"
        assert turn.feedback is not None
        assert turn.feedback.type == "POSITIVE"
        assert turn.feedback.text == "Great answer!"

    def test_from_api_with_null_feedback(self) -> None:
        data = {
            "responseId": "resp-789",
            "createdAt": "2026-03-01T08:00:00Z",
            "updatedAt": "2026-03-01T08:00:30Z",
            "feedback": None,
        }
        turn = ConversationTurnResponse.from_api(data)
        assert turn.feedback is None


class TestConversationResponseList:
    def test_from_api_empty(self) -> None:
        data: dict = {"responses": []}
        result = ConversationResponseList.from_api(data)
        assert result.responses == []

    def test_from_api_with_responses(self) -> None:
        data = {
            "responses": [
                {
                    "responseId": "r1",
                    "createdAt": "2026-01-01T00:00:00Z",
                    "updatedAt": "2026-01-01T00:01:00Z",
                },
                {
                    "responseId": "r2",
                    "createdAt": "2026-01-02T00:00:00Z",
                    "updatedAt": "2026-01-02T00:02:00Z",
                    "feedback": {"type": "NEGATIVE"},
                },
            ]
        }
        result = ConversationResponseList.from_api(data)
        assert len(result.responses) == 2
        assert result.responses[0].response_id == "r1"
        assert result.responses[0].feedback is None
        assert result.responses[1].response_id == "r2"
        assert result.responses[1].feedback is not None
        assert result.responses[1].feedback.type == "NEGATIVE"

    def test_from_api_missing_responses_key(self) -> None:
        # 'responses' key might be missing; default to empty list
        result = ConversationResponseList.from_api({})
        assert result.responses == []
