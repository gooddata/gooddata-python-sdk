# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any

import attrs


@attrs.define(kw_only=True)
class ConversationFeedback:
    """Represents feedback for a conversation turn response.

    Corresponds to ``FeedbackDto`` in the gen-ai OpenAPI spec.
    """

    type: str
    """Feedback type. One of ``'POSITIVE'`` or ``'NEGATIVE'``."""

    text: str | None = None
    """Optional free-form feedback comment."""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> ConversationFeedback:
        return cls(
            type=data["type"],
            text=data.get("text"),
        )

    def to_api_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"type": self.type}
        if self.text is not None:
            result["text"] = self.text
        return result


@attrs.define(kw_only=True)
class ConversationTurnResponse:
    """Represents a single conversation turn response.

    Corresponds to ``ConversationTurnResponseDto`` in the gen-ai OpenAPI spec.
    """

    response_id: str
    created_at: str
    updated_at: str
    feedback: ConversationFeedback | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> ConversationTurnResponse:
        feedback_data = data.get("feedback")
        return cls(
            response_id=data["responseId"],
            created_at=data["createdAt"],
            updated_at=data["updatedAt"],
            feedback=ConversationFeedback.from_api(feedback_data) if feedback_data is not None else None,
        )


@attrs.define(kw_only=True)
class ConversationResponseList:
    """Represents a list of conversation turn responses.

    Corresponds to ``ConversationResponseListDto`` in the gen-ai OpenAPI spec.
    """

    responses: list[ConversationTurnResponse] = attrs.field(factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> ConversationResponseList:
        return cls(
            responses=[ConversationTurnResponse.from_api(r) for r in data.get("responses", [])],
        )
