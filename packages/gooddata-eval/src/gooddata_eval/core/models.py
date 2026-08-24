# (C) 2026 GoodData Corporation
"""Pydantic models for the eval dataset envelope and the agent's AAC output.

Ported from gdc-nas tavern-e2e app/llm_as_judge/schemas/chat.py.
"""

import json
import re
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
    # Client-observed receipt time (seconds since the turn's first SSE line), not a
    # server-side execution measurement -- set by sse_client.py as the tool-call and
    # tool-result events stream in. None when the call never got a result (stalled turn).
    call_ts: float | None = None
    result_ts: float | None = None

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


class ReasoningStepEvent(BaseModel):
    """One reasoning step with its client-observed receipt time (see ToolCallEvent.call_ts).

    ``index`` is this step's 0-based position among reasoning steps in the turn -- the same
    position it occupies in ``ChatResult.reasoning_steps`` and, downstream, in the
    ``.reasoning.json`` sidecar's ``reasoning`` list. It's embedded in
    ``build_latency_breakdown``'s label precisely so the two files can be cross-referenced
    by an exact index instead of fuzzy-matching on title text (which is not unique -- the
    same title can recur, e.g. two distinct "Considering data analysis" steps).
    """

    summary: str
    ts: float
    index: int


# Reasoning summaries are full paragraphs, e.g. "**Identifying analytics needs**\n\nI'm
# analyzing..." -- using the whole thing as a latency_breakdown label would make every
# entry an unreadable wall of text. Same bolded-title convention this repo's own reasoning
# tooling already keys off of (see gdc-mic-ai-evaluation's generate_dashboard_summary.py).
_REASONING_TITLE_RE = re.compile(r"^\*\*(.+?)\*\*")
_REASONING_LABEL_MAX_LEN = 60


def _reasoning_label(step: "ReasoningStepEvent") -> str:
    m = _REASONING_TITLE_RE.match(step.summary.strip())
    title = m.group(1) if m else step.summary.strip().replace("\n", " ")
    if len(title) > _REASONING_LABEL_MAX_LEN:
        title = title[:_REASONING_LABEL_MAX_LEN] + "…"
    return f"{step.index}:{title}"


def build_latency_breakdown(
    tool_call_events: list[ToolCallEvent],
    reasoning_step_events: list[ReasoningStepEvent] | None = None,
) -> dict[str, float]:
    """Wall time attributed to each tool call and each reasoning step in the turn.

    Without ``reasoning_step_events``, this is just per-tool wall time (call receipt to
    result receipt) summed by name -- the gaps between tool calls (the model "thinking")
    are left unaccounted for.

    With them, every point in the turn -- a tool call starting, a tool call's result
    arriving, or a reasoning step being emitted -- is merged into one timeline and sorted.
    The gap between consecutive points is charged to whatever was "active" during it: a
    tool call while it's outstanding (call event to result event), or the most recently
    emitted reasoning step's own summary otherwise (its gap runs until the next point,
    whatever that turns out to be -- another reasoning step, or the next tool call
    starting). This accounts for effectively the whole turn, not just its tool-call
    portion; only the time before the first point and after the last (connection
    setup/teardown) is left out, since this function has no reference to the turn's total
    duration.

    Calls missing either timestamp (stalled, or from a chat backend that predates this
    capture) are skipped rather than counted as zero -- an absent entry means "unknown",
    not "instant".
    """
    points: list[tuple[float, str, str]] = []  # (ts, kind, label); kind: tool_start/tool_end/reasoning
    for tc in tool_call_events:
        if tc.call_ts is None or tc.result_ts is None:
            continue
        points.append((tc.call_ts, "tool_start", tc.function_name))
        points.append((tc.result_ts, "tool_end", tc.function_name))
    points.extend((rs.ts, "reasoning", _reasoning_label(rs)) for rs in reasoning_step_events or [])
    points.sort(key=lambda p: p[0])

    by_label: dict[str, float] = {}
    current_reasoning_label = "reasoning:(before first step)"
    for (ts, kind, label), (next_ts, _, _) in zip(points, points[1:]):
        gap = next_ts - ts
        if gap <= 0:
            continue
        if kind == "tool_start":
            key = f"tool:{label}"
        else:
            # A tool call resolving, or a reasoning step being emitted, both hand control
            # back to "whatever the model is doing until the next point" -- which is this
            # reasoning step once one has been seen, else the pre-first-step catch-all.
            key = f"reasoning:{label}" if kind == "reasoning" else current_reasoning_label
        by_label[key] = by_label.get(key, 0.0) + gap
        if kind == "reasoning":
            current_reasoning_label = f"reasoning:{label}"
    return {name: round(secs, 2) for name, secs in by_label.items()}


class ChatResult(BaseModel):
    """Subset of the agent chat response needed for Phase 1 evaluation."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    text_response: str | None = Field(default=None, alias="textResponse")
    created_visualizations: CreatedVisualizations | None = Field(default=None, alias="createdVisualizations")
    # Alert-proposal parts of the agent's multipart response. The alert skill's confirmation
    # step emits ONLY this part (no text part), so its `cta` is the only "the agent is asking
    # a question" signal the simulated-user loops can key off.
    alert_proposals: list[dict] = Field(default_factory=list, alias="alertProposals")
    tool_call_events: list[ToolCallEvent] = Field(default_factory=list, alias="toolCallEvents")
    reasoning_step_count: int = Field(default=0, alias="reasoningStepCount")
    reasoning_steps: list[str] = Field(default_factory=list, alias="reasoningSteps")
    reasoning_step_events: list[ReasoningStepEvent] = Field(default_factory=list, alias="reasoningStepEvents")
    conversation_id: str | None = Field(default=None, alias="conversationId")
    response_id: str | None = Field(default=None, alias="responseId")
    # True once gen-ai's response_ended event arrived.
    stream_ended: bool = False
    # Wall-clock seconds for the whole chat turn, timed by the client.
    turn_wall_clock_sec: float | None = None


class AgenticEvalOutcome(BaseModel):
    """Reasoning trace, trace-lookup IDs, and per-kind diagnostics from an evaluate_agentic_* call.

    ``detail`` mirrors the single-shot path's ``ItemEvaluation.detail`` -- a kind-specific
    dict of whatever diagnostic fields that evaluator already tracks internally (e.g.
    ``actual_maql`` for metric_skill, the full per-check breakdown for visualization). Both
    ``reasoning_steps``/etc. and ``detail`` are populated on success; on failure the same
    fields are attached directly to the raised ``*AssertionError`` instead.
    """

    reasoning_steps: list[str] = Field(default_factory=list)
    conversation_id: str | None = None
    response_id: str | None = None
    detail: dict = Field(default_factory=dict)


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
