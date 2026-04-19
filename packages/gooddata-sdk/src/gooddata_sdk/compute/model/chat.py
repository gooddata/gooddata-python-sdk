# (C) 2026 GoodData Corporation
from __future__ import annotations

import attrs
from gooddata_api_client.model.tool_call_event_result import (
    ToolCallEventResult as ApiToolCallEventResult,
)

from gooddata_sdk.catalog.base import Base


@attrs.define(kw_only=True)
class ToolCallEventResult(Base):
    """Represents a tool call event emitted during the agentic loop.

    Only present in :class:`~gooddata_api_client.model.chat_result.ChatResult`
    when the ``GEN_AI_YIELD_TOOL_CALL_EVENTS`` feature flag is enabled on the
    GoodData backend.
    """

    function_arguments: str
    """JSON-encoded arguments passed to the tool function."""

    function_name: str
    """Name of the tool function that was called."""

    result: str
    """Result returned by the tool function."""

    @staticmethod
    def client_class() -> type[ApiToolCallEventResult]:
        return ApiToolCallEventResult
