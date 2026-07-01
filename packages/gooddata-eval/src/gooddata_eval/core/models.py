# (C) 2026 GoodData Corporation
"""Pydantic models for the eval dataset envelope and the agent's AAC output.

Ported from gdc-nas tavern-e2e app/llm_as_judge/schemas/chat.py.
"""

import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AacQueryField(BaseModel):
    model_config = ConfigDict(extra="allow")

    using: str
    title: str | None = None
    aggregation: str | None = None


class AacBucketRef(BaseModel):
    model_config = ConfigDict(extra="allow")

    field: str


class AacQuery(BaseModel):
    fields: dict[str, AacQueryField | str]
    filter_by: dict[str, dict] = Field(default_factory=dict)

    @field_validator("filter_by", mode="before")
    @classmethod
    def _coerce_filter_by(cls, v: object) -> object:
        return v if v is not None else {}


class CreatedVisualization(BaseModel):
    """Visualization in the AAC format (agent output and dataset expected output)."""

    model_config = ConfigDict(extra="ignore")

    id: str
    title: str | None = None
    type: str
    query: AacQuery
    metrics: list[AacBucketRef | str] = Field(default_factory=list)
    view_by: list[AacBucketRef | str] = Field(default_factory=list)
    segment_by: list[AacBucketRef | str] = Field(default_factory=list)
    rows: list[AacBucketRef | str] = Field(default_factory=list)
    columns: list[AacBucketRef | str] = Field(default_factory=list)
    config: dict | None = None

    @field_validator("metrics", "view_by", "segment_by", "rows", "columns", mode="before")
    @classmethod
    def _coerce_list_fields(cls, v: object) -> object:
        return v if v is not None else []


class CreatedVisualizations(BaseModel):
    model_config = ConfigDict(extra="ignore")

    objects: list[CreatedVisualization] = Field(default_factory=list)
    reasoning: str = ""


class ToolCallEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    function_name: str = Field(alias="functionName")
    function_arguments: str = Field(alias="functionArguments")
    result: str | None = None

    def parsed_arguments(self) -> dict[str, Any]:
        try:
            return json.loads(self.function_arguments) if self.function_arguments else {}
        except json.JSONDecodeError:
            return {}

    def parsed_result(self) -> dict[str, Any] | None:
        if not self.result:
            return None
        try:
            return json.loads(self.result)
        except json.JSONDecodeError:
            return None


class ChatResult(BaseModel):
    """Subset of the agent chat response needed for Phase 1 evaluation."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    text_response: str | None = Field(default=None, alias="textResponse")
    created_visualizations: CreatedVisualizations | None = Field(default=None, alias="createdVisualizations")
    tool_call_events: list[ToolCallEvent] = Field(default_factory=list, alias="toolCallEvents")
    reasoning_step_count: int = Field(default=0, alias="reasoningStepCount")
    conversation_id: str | None = Field(default=None, alias="conversationId")
    response_id: str | None = Field(default=None, alias="responseId")


class SummaryInput(BaseModel):
    """Structured input for the `dashboard_summary` test kind.

    Maps onto the dedicated summary endpoint's request body
    (`POST /api/v1/ai/workspaces/{ws}/summary`). Authored in snake_case in the
    dataset; the SummaryClient maps it to the endpoint's camelCase fields.
    """

    model_config = ConfigDict(extra="ignore")

    dashboard_id: str
    visualizations: list[str] | None = None
    filter_context: list[dict] | None = None
    tab_id: str | None = None
    format_hint: str | None = None


class DatasetItem(BaseModel):
    """Common dataset envelope. `expected_output` stays raw; each evaluator parses its own shape."""

    model_config = ConfigDict(extra="ignore")

    id: str
    dataset_name: str
    test_kind: str
    question: str
    expected_output: Any
    # Only used by the `dashboard_summary` test kind; ignored by all others.
    summary_input: SummaryInput | None = None
