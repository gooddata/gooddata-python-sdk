# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic conversation evaluation runner (multi-turn, multi-skill).

Two modes decide what a pass means:

- ``legacy``: a turn passes when the expected skill is active and an output of the
  expected type appears. The simulated user is primed with the turn's expected output.
- ``context``: a turn additionally has to match its expected output given everything the
  conversation established, must not ask for information the conversation already holds
  (graded by a binary judge), and must not stall. The simulated user answers from the
  fixture's set answers and the conversation only, never from the expected output.

Both modes compute every score, so a dataset can run in ``legacy`` while the ``context``
scores are collected alongside it; the mode only picks which verdict raises.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import date
from typing import ClassVar, Literal

from gooddata_sdk import GoodDataSdk
from pydantic import BaseModel, Field, ValidationError

from gooddata_eval.core.agentic._conversation_context import (
    CONFIRMATION_REPLY,
    NUDGE_MESSAGE,
    ClarificationJudge,
    TranscriptEntry,
    classify_reply,
    clip,
    judge_prompt,
    render_transcript,
    reply_from_facts,
    reply_restating,
    summarize_visualizations,
)
from gooddata_eval.core.agentic._gate import log_gate_scores
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.agentic.alert_skill import _delete_alert, render_alert_proposal
from gooddata_eval.core.agentic.metric_skill import _delete_metric, _extract_metric_result
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError, TurnIncompleteError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._deep_subset import deep_subset
from gooddata_eval.core.evaluators._maql import normalize_maql
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    CreatedVisualization,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    shift_and_index_events,
    timeline_detail,
)
from gooddata_eval.core.scoring import (
    check_filters,
    check_viz_type,
    get_dimension_uri_set,
    get_metric_uri_set,
    normalized_filters,
    resolve_alias_to_uri,
)

_REF_PATTERN = re.compile(r"\$ref:([\w_]+)\.([\w_]+)")

_DEFAULT_MAX_CLARIFICATION_TURNS = 7

ConversationMode = Literal["legacy", "context"]
CONVERSATION_MODE_ENV_VAR = "GD_EVAL_CONVERSATION_MODE"


def resolve_conversation_mode(mode: str | None = None) -> ConversationMode:
    """The explicit mode, else ``GD_EVAL_CONVERSATION_MODE``, else ``legacy``."""
    raw = (mode or os.environ.get(CONVERSATION_MODE_ENV_VAR, "") or "legacy").strip().lower()
    if raw not in ("legacy", "context"):
        raise ValueError(f"conversation mode must be 'legacy' or 'context', got {raw!r}")
    return "context" if raw == "context" else "legacy"


class TurnDefinition(BaseModel):
    """Definition of a single turn in a multi-turn conversation evaluation.

    ``depends_on`` names the earlier turns this one cannot be answered without. It does not
    change how the turn is graded; it selects which turns ``context_kept_rate`` is computed
    over. ``set_answers`` are what the user replies, in order, when the assistant asks a
    legitimate question on this turn -- the only knowledge the context-mode simulated user
    has beyond the conversation itself.
    """

    turn_id: str
    message: str
    expected_skill: str
    expected_output_type: Literal["visualization", "tool_call", "metric"] = "visualization"
    expected_tool_name: str | None = None
    expected_output: dict | None = None
    expected_output_alternatives: list[dict] = Field(default_factory=list)
    expected_tool_args: dict | None = None
    depends_on: list[str] = Field(default_factory=list)
    set_answers: list[str] = Field(default_factory=list)


class ConversationFixture(BaseModel):
    """A complete multi-turn conversation test fixture."""

    id: str
    dataset_name: str = "conversation"
    expected_skills: list[str]
    turns: list[TurnDefinition]


ReplyRecordKind = Literal["confirmation", "question", "no_action", "turn_incomplete"]


class ClarificationRecord(BaseModel):
    """One assistant reply that did not deliver the turn's output, and what the user said back."""

    kind: ReplyRecordKind
    agent_message: str
    lost_context: bool | None = None
    reasoning: str = ""
    judge_error: str | None = None
    judge_input: str = ""
    reply: str = ""


class TurnResult(BaseModel):
    """Evaluation result for a single conversation turn.

    The two skill fields measure DIFFERENT SCOPES, so a turn can legitimately report
    ``skill_routing=True`` with an empty ``activated_skills``:

    - ``activated_skills`` -- what THIS turn's own ``set_skills`` call declared. Empty
      whenever the agent reused an already-active skill without re-declaring it.
    - ``active_skills`` -- what was actually active DURING this turn: the last declared
      set, carried over on turns that declare nothing. This is the set ``skill_routing``
      is judged against, so a report never has to infer it.
    - ``skill_routing`` -- whether ``expected_skill`` appears in ``active_skills``.

    ``skill_routing=True`` with ``activated_skills=[]`` is the reused-skill case, not a
    scoring bug -- ``active_skills`` shows where the credit came from.

    ``skill_success`` is the legacy verdict. ``context_success`` also requires the output to
    match the expected one (when the fixture states it), no clarification the judge found
    to be lost context, and no stall.
    """

    turn_id: str
    expected_skill: str
    skill_routing: bool
    output_present: bool
    no_error: bool
    activated_skills: list[str]
    # Sorted for stable output: the source is a set, whose iteration order is not.
    active_skills: list[str] = Field(default_factory=list)
    clarification_turns_used: int = 0
    output_correct: bool | None = None
    # Why this turn's clarification loop stopped -- see LoopExit. output_present=False alone
    # cannot separate a turn that ran out of clarification budget from one where the agent
    # went silent, and skill_success folds both into the same failure.
    exit_reason: LoopExit = LoopExit.BUDGET_EXHAUSTED
    mismatches: list[str] = Field(default_factory=list)
    clarifications: list[ClarificationRecord] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)

    @property
    def skill_success(self) -> bool:
        return self.skill_routing and self.output_present and self.no_error

    @property
    def lost_context(self) -> bool:
        return any(c.lost_context is True for c in self.clarifications)

    @property
    def stalled(self) -> bool:
        return any(c.kind in ("no_action", "turn_incomplete") for c in self.clarifications)

    @property
    def context_success(self) -> bool:
        return self.skill_success and self.output_correct is not False and not self.lost_context and not self.stalled

    def failure_reasons(self) -> list[str]:
        """Why ``context_success`` is False, in reading order; empty when it is True."""
        reasons: list[str] = []
        if not self.no_error:
            reasons.append("turn could not run")
        elif not self.output_present:
            reasons.append("no output of the expected type")
        elif not self.skill_routing:
            reasons.append(f"skill {self.expected_skill!r} not active")
        if self.output_correct is False:
            reasons.extend(self.mismatches or ["output does not match the expected output"])
        if self.lost_context:
            reasons.append("asked for information the conversation already established")
        if self.stalled:
            reasons.append("ended a reply without the expected output and without asking anything")
        return reasons

    # Reported per turn in detail["turns"]. A name listed here that no longer exists on the
    # model raises rather than silently emitting a stale key, which a hand-written dict
    # literal of the same fields would not -- and model_dump deep-copies activated_skills,
    # so a caller mutating the returned dict cannot reach back into this TurnResult.
    _DETAIL_FIELDS: ClassVar[set[str]] = {
        "turn_id",
        "expected_skill",
        "skill_routing",
        "output_present",
        "output_correct",
        "activated_skills",
        # What skill_routing was judged against -- without it, a turn showing
        # skill_routing=True and activated_skills=[] looks like a scoring bug.
        "active_skills",
        # Why the clarification loop ended on this turn, and how much of the budget it
        # took to get there -- exit_reason alone cannot be related to the limit without it.
        "exit_reason",
        "clarification_turns_used",
        "mismatches",
        "clarifications",
        "depends_on",
    }

    def detail(self) -> dict:
        """The subset of this result reported in detail["turns"] for one conversation turn."""
        out = self.model_dump(include=self._DETAIL_FIELDS)
        out["context_success"] = self.context_success
        out["failure_reasons"] = self.failure_reasons()
        return out


def _resolve_refs(
    expected_output: dict | None,
    turn_outputs: dict[str, dict],
) -> dict | None:
    """Resolve $ref:turn_id.field placeholders from prior turn outputs.

    Works on the JSON-serialised form so nested values (e.g. URI strings) are
    also resolved.  Raises ValueError when a referenced turn or field is absent.
    """
    if not expected_output:
        return expected_output

    raw = json.dumps(expected_output)
    if "$ref:" not in raw:
        return expected_output

    def _replace(match: re.Match) -> str:  # type: ignore[type-arg]
        turn_id, field = match.group(1), match.group(2)
        if turn_id not in turn_outputs:
            raise ValueError(
                f"Cannot resolve '$ref:{turn_id}.{field}': "
                f"turn '{turn_id}' has no captured output. "
                f"Available turns: {list(turn_outputs)}"
            )
        if field not in turn_outputs[turn_id]:
            raise ValueError(
                f"Cannot resolve '$ref:{turn_id}.{field}': "
                f"field '{field}' not found in turn '{turn_id}' output. "
                f"Available fields: {list(turn_outputs[turn_id])}"
            )
        return str(turn_outputs[turn_id][field])

    resolved_raw = _REF_PATTERN.sub(_replace, raw)
    return json.loads(resolved_raw)


def _set_skills_declarations(tool_call_events: list[ToolCallEvent]) -> list[list[str]]:
    """Every set_skills declaration in these events, in call order.

    `skill_names` is the key the tool declares; `skills` is a legacy spelling kept as a
    fallback. A call carrying neither is treated as declaring an empty list, which is what
    the platform would do with one.
    """
    declarations: list[list[str]] = []
    for tc in tool_call_events:
        if tc.function_name != "set_skills":
            continue
        args = tc.parsed_arguments() or {}
        names = args.get("skill_names")
        if names is None:
            names = args.get("skills")
        declarations.append(list(names or []))
    return declarations


def _final_skill_declaration(tool_call_events: list[ToolCallEvent]) -> list[str] | None:
    """The skill list from the LAST set_skills call, or None when there was no call.

    set_skills replaces the active set, so when a turn issues several calls -- which it can,
    since these events span every clarification sub-turn within one logical turn -- only the
    final one describes the resulting state. Merging them would credit a skill that an
    earlier call declared and a later one dropped.

    An empty list is a real declaration: it deactivates everything. That has to stay
    distinguishable from ``None`` ("no call at all"), which leaves the previous turn's set
    untouched -- hence the Optional rather than just an empty list for both.

    This answers "what is active NOW". For "was this skill ever exercised" -- what
    full_skill_coverage asks -- use every declaration, not just the last one.
    """
    declarations = _set_skills_declarations(tool_call_events)
    return declarations[-1] if declarations else None


def _check_output_present(turn: TurnDefinition, chat_result: ChatResult) -> bool:
    otype = turn.expected_output_type
    if otype == "visualization":
        return bool(
            chat_result.created_visualizations
            and getattr(chat_result.created_visualizations, "objects", chat_result.created_visualizations)
        )
    if otype == "metric":
        return _extract_metric_result(chat_result.tool_call_events or []) is not None
    if otype == "tool_call":
        expected_tool = turn.expected_tool_name
        if not expected_tool:
            return bool(chat_result.tool_call_events)
        return any(tc.function_name == expected_tool for tc in (chat_result.tool_call_events or []))
    return False


def _expected_viz(expected: dict) -> CreatedVisualization | None:
    """The chart an expected output describes, or None when it names no fields to compare.

    Fixtures wrap the chart as ``{"visualization": {...}}``; a bare chart is accepted too.
    ``type`` may be empty, which means "any chart type".
    """
    body = expected.get("visualization", expected)
    if not isinstance(body, dict):
        return None
    query = body.get("query")
    if not isinstance(query, dict) or not query.get("fields"):
        return None
    try:
        return CreatedVisualization.model_validate({**body, "type": body.get("type") or ""})
    except ValidationError:
        return None


def _flat_viz_check(candidates: list[dict], chat_result: ChatResult) -> tuple[bool | None, list[str]]:
    """The flat ``{"metrics": [uri, ...], "dimensions": [uri, ...]}`` form: the listed URIs
    must all be in one of the charts. ``(None, [])`` when no candidate lists any."""
    flat = [c for c in candidates if isinstance(c.get("metrics"), list) or isinstance(c.get("dimensions"), list)]
    if not flat:
        return None, []
    objects = getattr(chat_result.created_visualizations, "objects", None) or []
    for cand in flat:
        want_m, want_d = set(cand.get("metrics") or []), set(cand.get("dimensions") or [])
        for act in objects:
            if want_m <= get_metric_uri_set(act) and want_d <= get_dimension_uri_set(act):
                return True, []
    return False, [f"expected {flat[0].get('metrics') or []} / {flat[0].get('dimensions') or []} in the chart"]


def _sort_signature(viz: CreatedVisualization) -> set[tuple[str, str, str]]:
    """(sort type, sorted-by URI, direction) for each sort entry."""
    out: set[tuple[str, str, str]] = set()
    for entry in viz.query.sort_by:
        stype = str(entry.get("type") or "")
        direction = str(entry.get("direction") or "").upper()
        aliases = entry.get("metrics") if stype == "metric_sort" else [entry.get("by")]
        for alias in aliases or []:
            if isinstance(alias, str):
                out.add((stype, resolve_alias_to_uri(alias, viz.query.fields), direction))
    return out


def _clamp_future_dates(viz: CreatedVisualization, today: date) -> CreatedVisualization:
    """A copy whose absolute date filters end no later than ``today``.

    Nothing is recorded after today, so "2025 and 2026 so far" as 2025-01-01..2026-12-31 and as
    2025-01-01..<today> select the same data. Comparing the raw end dates would fail an answer
    that states the period more precisely than the fixture does.
    """
    filters = {}
    for key, f in viz.query.filter_by.items():
        to = f.get("to") if isinstance(f, dict) and f.get("type") == "date_filter" else None
        if isinstance(to, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", to) and to > today.isoformat():
            f = {**f, "to": today.isoformat()}
        filters[key] = f
    return viz.model_copy(update={"query": viz.query.model_copy(update={"filter_by": filters})})


def _viz_mismatches(
    expected: CreatedVisualization, actual: CreatedVisualization, today: date | None = None
) -> list[str]:
    """Every way ``actual`` differs from ``expected``; empty when they match.

    Metrics and dimensions compare as sets of URIs, so bucket order and local ids do not
    matter. Filters compare per category and always: a chart with a filter nobody asked for
    fails as surely as one missing a filter. Type and sort compare only when the expected
    chart states them.
    """
    today = today or date.today()
    expected, actual = _clamp_future_dates(expected, today), _clamp_future_dates(actual, today)
    out: list[str] = []
    exp_m, act_m = get_metric_uri_set(expected), get_metric_uri_set(actual)
    if exp_m != act_m:
        out.append(f"metrics: expected {sorted(exp_m)}, got {sorted(act_m)}")
    exp_d, act_d = get_dimension_uri_set(expected), get_dimension_uri_set(actual)
    if exp_d != act_d:
        out.append(f"dimensions: expected {sorted(exp_d)}, got {sorted(act_d)}")
    if not check_viz_type(expected, actual):
        out.append(f"type: expected {expected.type!r}, got {actual.type!r}")
    scores = check_filters(expected, actual, today)
    exp_f, act_f = normalized_filters(expected, today), normalized_filters(actual, today)
    for category, ok in (("date", scores.date_ok), ("ranking", scores.ranking_ok), ("attribute", scores.attribute_ok)):
        if not ok:
            out.append(f"{category} filters: expected {exp_f[category]}, got {act_f[category]}")
    if expected.query.sort_by:
        exp_s, act_s = _sort_signature(expected), _sort_signature(actual)
        # An expected entry without a direction matches either direction.
        if not all(any(a[:2] == e[:2] and (not e[2] or a[2] == e[2]) for a in act_s) for e in exp_s):
            out.append(f"sort: expected {sorted(exp_s)}, got {sorted(act_s)}")
    return out


# `IN ("x")` with one value is `= "x"`: both spellings appear in agent output for the same filter.
_SINGLE_IN_RE = re.compile(r'(?<!\bnot)(?<!\bnot )\s*\bin\(("(?:[^"\\]|\\.)*")\)')


def _canonical_maql(maql: str) -> str:
    return _SINGLE_IN_RE.sub(r"=\1", normalize_maql(maql))


def _tool_calls_named(tool_call_events: list[ToolCallEvent], name: str | None) -> list[ToolCallEvent]:
    return [tc for tc in tool_call_events if name is None or tc.function_name == name]


def _check_output_correct(
    turn: TurnDefinition, chat_result: ChatResult, turn_tool_calls: list[ToolCallEvent] | None = None
) -> tuple[bool | None, list[str]]:
    """Whether the turn's output matches its expected output, and how it differs if not.

    Returns ``(None, [])`` when the fixture states nothing to compare. The expected output
    and each of ``expected_output_alternatives`` are candidates; matching any one is a pass.
    ``turn_tool_calls`` are every tool call of the turn, across its clarification rounds --
    the tool whose arguments are checked may have run before the final reply.
    """
    tool_calls = turn_tool_calls if turn_tool_calls is not None else (chat_result.tool_call_events or [])
    candidates = [c for c in [turn.expected_output, *turn.expected_output_alternatives] if c]
    otype = turn.expected_output_type

    if otype == "visualization":
        expected_vizzes = [v for v in (_expected_viz(c) for c in candidates) if v is not None]
        if not expected_vizzes:
            return _flat_viz_check(candidates, chat_result)
        objects = getattr(chat_result.created_visualizations, "objects", None) or []
        if not objects:
            return False, ["no visualization to compare"]
        best: list[str] | None = None
        for exp in expected_vizzes:
            for act in objects:
                diff = _viz_mismatches(exp, act)
                if not diff:
                    return True, []
                if best is None or len(diff) < len(best):
                    best = diff
        return False, best or []

    if otype == "metric":
        maqls: list[str] = [m for m in (c.get("maql") for c in candidates) if isinstance(m, str) and m]
        if not maqls:
            return None, []
        metric_result = _extract_metric_result(tool_calls)
        if not metric_result:
            return False, ["no created metric to compare"]
        actual = _canonical_maql(metric_result.get("maql", ""))
        if any(_canonical_maql(m) == actual for m in maqls):
            return True, []
        return False, [f"maql: expected {maqls[0]!r}, got {metric_result.get('maql', '')!r}"]

    if otype == "tool_call":
        if not turn.expected_tool_args:
            return None, []
        calls = _tool_calls_named(tool_calls, turn.expected_tool_name)
        args = [tc.parsed_arguments() or {} for tc in calls]
        if any(deep_subset(turn.expected_tool_args, a) for a in args):
            return True, []
        got = args[-1] if args else None
        return False, [f"tool arguments: expected subset {turn.expected_tool_args}, got {got}"]

    return None, []


def _get_sim_user_response(agent_message: str, turn: TurnDefinition, expected_output: dict | None) -> str:
    """Generate a simulated user reply to an agent clarification question."""
    otype = turn.expected_output_type
    if otype == "visualization" and expected_output:
        try:
            from gooddata_eval.core.agentic.visualization import generate_simulated_response  # noqa: PLC0415
            from gooddata_eval.core.models import CreatedVisualization  # noqa: PLC0415

            exp_viz = CreatedVisualization.model_validate(expected_output.get("visualization", expected_output))
            return generate_simulated_response(agent_message, exp_viz)
        except Exception:
            pass
    elif otype == "metric" and expected_output:
        try:
            from gooddata_eval.core.agentic.metric_skill import (  # noqa: PLC0415
                generate_simulated_response,
            )

            # A conversation turn only ever carries one expected_output (no multi-candidate
            # list like agent_metric_skill's fixtures) -- wrap it as a single-item list to
            # match generate_simulated_response's signature.
            return generate_simulated_response(agent_message, [expected_output], turn.message)
        except Exception as exc:
            print(f"[SIM-USER] metric branch failed for turn {turn.turn_id}: {exc}")

    # Generic fallback for other skill types or when expected_output is absent
    import os  # noqa: PLC0415

    try:
        from openai import OpenAI  # noqa: PLC0415

        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a business user interacting with a data analytics chatbot. "
                            "The chatbot may ask clarifying questions before completing your request. "
                            "Answer naturally and concisely to help it accomplish your original goal. "
                            "Do not mention technical terms like tools, skills, or APIs."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f'Your original request was: "{turn.message}"\n'
                            f'\nThe chatbot asked: "{agent_message}"\n\n'
                            f"Answer the clarification question naturally and helpfully to accomplish your goal. "
                            f"Keep your response concise, as a real user would."
                        ),
                    },
                ],
                temperature=0,
            )
            content = response.choices[0].message.content
            return content.strip() if content else "Please proceed with sensible defaults."
    except Exception:
        pass
    return "Please proceed with sensible defaults."


@dataclass
class ConversationResult:
    """Outcome of a multi-turn, multi-skill conversation evaluation.

    ``conversation_success`` is the legacy verdict, ``context_success`` the context one; see
    the module docstring. ``context_kept_rate`` is the share of context-dependent turns
    (those with ``depends_on``, else every turn after the first) that passed in context
    terms, and ``turns_before_first_break`` how many turns passed before the first one that
    did not.
    """

    conversation_id: str
    turn_results: list[TurnResult]
    full_skill_coverage: bool
    conversation_success: bool
    total_clarification_turns: int
    # The configured per-turn clarification budget, so a reader can tell a turn that used
    # its whole allowance from one that stopped early. Every other agentic kind reports its
    # limit in detail; without this, conversation is the exception to that contract.
    max_clarification_turns: int = _DEFAULT_MAX_CLARIFICATION_TURNS
    total_steps: int = 0
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    context_success: bool = False
    context_kept_rate: float | None = None
    turns_before_first_break: int = 0
    lost_context_clarifications: int = 0
    stalled_turns: int = 0
    mode: ConversationMode = "legacy"
    judge_model: str | None = None


def _metric_creations(tool_call_events: list[ToolCallEvent]) -> list[tuple[str, bool]]:
    """(metric_id, created_new) for every successful create_metric call.

    ``create_metric`` is an upsert: on an existing id it replaces that metric and reports
    ``created_new: false``. A result without the flag counts as a creation.
    """
    out: list[tuple[str, bool]] = []
    for tc in tool_call_events:
        if tc.function_name != "create_metric" or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        data = result_data.get("data", result_data)
        if not isinstance(data, dict) or data.get("isError"):
            continue
        metric_id = data.get("metric_id")
        if metric_id:
            out.append((metric_id, data.get("created_new") is not False))
    return out


def _created_alert_ids(tool_call_events: list[ToolCallEvent]) -> list[str]:
    """Ids of the alerts (automations) ``create_metric_alert`` calls created."""
    ids: list[str] = []
    for tc in tool_call_events:
        if tc.function_name != "create_metric_alert" or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        nested = result_data.get("data")
        alert_id = result_data.get("id") or (nested.get("id") if isinstance(nested, dict) else None)
        if isinstance(alert_id, str) and alert_id and alert_id not in ids:
            ids.append(alert_id)
    return ids


class _WorkspaceObjects:
    """What a conversation wrote to the workspace, for cleanup once it ends.

    Deferred to the end because a later turn may ``$ref`` a metric an earlier turn created.
    A metric the agent updated in place (``created_new: false``) existed before the
    conversation, so it is reported rather than deleted.
    """

    def __init__(self) -> None:
        self.metrics: list[str] = []
        self.updated_metrics: list[str] = []
        self.alerts: list[str] = []

    def record(self, tool_call_events: list[ToolCallEvent]) -> None:
        for metric_id, created_new in _metric_creations(tool_call_events):
            if created_new:
                if metric_id not in self.metrics and metric_id not in self.updated_metrics:
                    self.metrics.append(metric_id)
            elif metric_id not in self.metrics and metric_id not in self.updated_metrics:
                self.updated_metrics.append(metric_id)
        for alert_id in _created_alert_ids(tool_call_events):
            if alert_id not in self.alerts:
                self.alerts.append(alert_id)

    def delete(self, sdk: GoodDataSdk, workspace_id: str) -> None:
        for alert_id in self.alerts:
            _delete_alert(sdk, workspace_id, alert_id)
        for metric_id in self.metrics:
            _delete_metric(sdk, workspace_id, metric_id)
        for metric_id in self.updated_metrics:
            print(f"[CLEANUP] Metric {metric_id} existed before the conversation and was updated in place; kept.")


def _context_summary(
    turn_results: list[TurnResult], fixture: ConversationFixture
) -> tuple[bool, float | None, int, int, int]:
    """(context_success, context_kept_rate, turns_before_first_break, lost_context, stalled)."""
    context_success = bool(turn_results) and all(tr.context_success for tr in turn_results)
    labelled = {t.turn_id for t in fixture.turns if t.depends_on}
    dependent = [tr for tr in turn_results if tr.turn_id in labelled] if labelled else turn_results[1:]
    rate = (sum(tr.context_success for tr in dependent) / len(dependent)) if dependent else None
    before_break = len(turn_results)
    for i, tr in enumerate(turn_results):
        if not tr.context_success:
            before_break = i
            break
    lost = sum(1 for tr in turn_results for c in tr.clarifications if c.lost_context is True)
    stalled = sum(1 for tr in turn_results if tr.stalled)
    return context_success, rate, before_break, lost, stalled


def run_agentic_conversation(
    host: str,
    token: str,
    workspace_id: str,
    fixture: ConversationFixture,
    max_clarification_turns: int = _DEFAULT_MAX_CLARIFICATION_TURNS,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    mode: ConversationMode | None = None,
    clarification_judge: ClarificationJudge | None = None,
    fresh_conversation_per_turn: bool = False,
) -> ConversationResult:
    """Run a multi-turn, multi-skill conversation evaluation (no K-runs).

    A single conversation is used for all turns in the fixture.  Each turn may
    trigger up to *max_clarification_turns* additional rounds of simulated-user
    replies before the agent produces the expected output.

    ``fresh_conversation_per_turn`` sends every turn into a new conversation instead, so the
    agent sees no history. It is the no-memory baseline a context score is calibrated
    against: context-dependent turns are expected to fail there.
    """
    resolved_mode = resolve_conversation_mode(mode)
    if fresh_conversation_per_turn and initial_conversation_id is not None:
        raise ValueError("fresh_conversation_per_turn needs conversations this run creates itself")
    judge = clarification_judge if clarification_judge is not None else ClarificationJudge()
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    sdk = GoodDataSdk.create(host, token)
    turn_results: list[TurnResult] = []
    turn_outputs: dict[str, dict] = {}
    total_clarification_turns = 0
    total_steps = 0
    conversation_id: str = ""
    owns_conversation = False
    created = _WorkspaceObjects()
    reasoning_steps: list[str] = []
    response_id: str | None = None
    conversation_tool_call_events: list[ToolCallEvent] = []
    conversation_reasoning_step_events: list[ReasoningStepEvent] = []
    transcript: list[TranscriptEntry] = []
    # The skills active right now, mirroring the platform's own state machine: set_skills
    # REPLACES the active set rather than adding to it -- verified against the gen-ai
    # service's skill registry, and stated in the tool's own description. So a turn that
    # issues no set_skills call inherits the previous turn's set unchanged, while a turn
    # that does issue one drops whatever it left out. Tracking this as a running UNION
    # would credit a skill a later call had already switched off.
    active_skills: set[str] = set()
    # Every skill declared at any point, for full_skill_coverage. This asks a DIFFERENT
    # question from active_skills -- "did the conversation ever exercise this skill" rather
    # than "is it active now" -- so replace semantics do not apply: a skill switched on and
    # later switched off was still exercised. Deriving coverage from the per-turn final
    # declaration instead would drop any skill a turn declared and then replaced within
    # itself (across its clarification sub-turns), a false FAIL on a genuine activation.
    ever_declared_skills: set[str] = set()
    # Every send_message() call (across every logical turn AND every clarification
    # sub-turn within it) restarts call_ts/ts near 0 -- these run across the whole
    # conversation, not reset per logical turn, so every one of those calls shifts them.
    turn_offset = 0.0
    tool_index_offset = 0
    reasoning_index_offset = 0

    try:
        if initial_conversation_id is not None:
            conversation_id = initial_conversation_id
        else:
            conversation_id = client.create_conversation()
            owns_conversation = True

        for turn_index, turn in enumerate(fixture.turns):
            if fresh_conversation_per_turn and turn_index > 0:
                client.delete_conversation(conversation_id)
                conversation_id = client.create_conversation()
                transcript = []
                active_skills = set()
            try:
                resolved_expected = _resolve_refs(turn.expected_output, turn_outputs)
                resolved_alternatives = [
                    _resolve_refs(a, turn_outputs) or {} for a in turn.expected_output_alternatives
                ]
                resolved_tool_args = _resolve_refs(turn.expected_tool_args, turn_outputs)
            except ValueError as exc:
                print(f"[SKIP] turn '{turn.turn_id}': {exc}")
                turn_results.append(
                    TurnResult(
                        turn_id=turn.turn_id,
                        expected_skill=turn.expected_skill,
                        skill_routing=False,
                        output_present=False,
                        no_error=False,
                        activated_skills=[],
                        # The turn never ran, so it declared nothing -- but a set carried over
                        # from an earlier turn is still active, and reporting [] here would
                        # read as "nothing was active", which is a different claim.
                        active_skills=sorted(active_skills),
                        output_correct=False,
                        # This turn's loop never ran at all -- a $ref pointing at an earlier
                        # turn's output could not be resolved. Labelling it BUDGET_EXHAUSTED
                        # (the field default) would claim it ran out of clarification turns.
                        exit_reason=LoopExit.NOT_RUN,
                        mismatches=[str(exc)],
                        depends_on=list(turn.depends_on),
                    )
                )
                continue
            resolved_turn = turn.model_copy(
                update={
                    "expected_output": resolved_expected,
                    "expected_output_alternatives": resolved_alternatives,
                    "expected_tool_args": resolved_tool_args,
                }
            )

            clarification_turns = 0
            all_tool_calls: list[ToolCallEvent] = []
            current_message = turn.message
            final_result: ChatResult | None = None
            records: list[ClarificationRecord] = []
            answers_left = list(turn.set_answers)

            # Defaults to BUDGET_EXHAUSTED: every other exit assigns explicitly, so a loop
            # that simply runs out of range() is labelled correctly with no trailing else.
            turn_exit = LoopExit.BUDGET_EXHAUSTED
            for _iter in range(max_clarification_turns + 1):
                transcript.append(TranscriptEntry("user", current_message))
                incomplete = False
                try:
                    chat_result = client.send_message(conversation_id, current_message)
                except TurnIncompleteError as exc:
                    chat_result = exc.partial_result or ChatResult()
                    incomplete = True
                except ChatError as exc:
                    # Recorded rather than raised so the turns already completed keep their
                    # results, and so this turn is distinguishable from one where the agent
                    # simply failed to produce output. no_error below reads this back.
                    print(f"[CHAT] send_message failed for conversation {conversation_id}: {exc}")
                    partial = exc.partial_result
                    if partial is not None:
                        # The stream can die after create_metric ran server-side; keep what
                        # the accumulator saw so the cleanup still knows what to delete.
                        created.record(partial.tool_call_events or [])
                        final_result = partial
                        all_tool_calls.extend(partial.tool_call_events or [])
                        conversation_tool_call_events.extend(partial.tool_call_events or [])
                        conversation_reasoning_step_events.extend(partial.reasoning_step_events or [])
                        reasoning_steps.extend(partial.reasoning_steps or [])
                        response_id = partial.response_id or response_id
                    turn_exit = LoopExit.CHAT_ERROR
                    break
                final_result = chat_result
                total_steps += chat_result.reasoning_step_count
                turn_offset, tool_index_offset, reasoning_index_offset = shift_and_index_events(
                    chat_result,
                    turn_offset=turn_offset,
                    tool_index_offset=tool_index_offset,
                    reasoning_index_offset=reasoning_index_offset,
                )
                all_tool_calls.extend(chat_result.tool_call_events or [])
                created.record(chat_result.tool_call_events or [])
                conversation_tool_call_events.extend(chat_result.tool_call_events or [])
                conversation_reasoning_step_events.extend(chat_result.reasoning_step_events or [])
                reasoning_steps.extend(chat_result.reasoning_steps or [])
                response_id = chat_result.response_id or response_id

                response_text = (chat_result.text_response or "").strip()
                if not response_text and chat_result.alert_proposals:
                    response_text = render_alert_proposal(chat_result.alert_proposals[-1])
                if not response_text:
                    response_text = render_answer_text(chat_result)
                transcript.append(
                    TranscriptEntry(
                        "assistant", " ".join(p for p in (response_text, summarize_visualizations(chat_result)) if p)
                    )
                )

                if _check_output_present(resolved_turn, chat_result):
                    if incomplete:
                        records.append(ClarificationRecord(kind="turn_incomplete", agent_message=clip(response_text)))
                    turn_exit = LoopExit.SUCCESS
                    break

                # `incomplete` is excluded deliberately: a turn the server cut short is a
                # known stall with its own nudge path below, not an agent that said nothing.
                if not incomplete and not response_text and not chat_result.tool_call_events:
                    turn_exit = LoopExit.AGENT_SILENT
                    break

                kind: ReplyRecordKind = "turn_incomplete" if incomplete else classify_reply(chat_result, response_text)
                if (
                    resolved_mode == "legacy"
                    and not incomplete
                    and not response_text
                    and not chat_result.tool_call_events
                ):
                    records.append(ClarificationRecord(kind="no_action", agent_message=""))
                    break
                record = ClarificationRecord(kind=kind, agent_message=clip(response_text))
                if kind == "question":
                    # transcript ends [..., user: current_message, assistant: this reply].
                    history, latest = render_transcript(transcript[:-2]), current_message
                    record.judge_input = judge_prompt(history, latest, response_text)
                    verdict = judge.judge(history, latest, response_text)
                    record.lost_context = verdict.lost_context
                    record.reasoning = verdict.reasoning
                    record.judge_error = verdict.error
                # A second stall in the same turn ends it: one push is what a user gives.
                second_stall = (
                    resolved_mode == "context"
                    and kind in ("no_action", "turn_incomplete")
                    and any(r.kind in ("no_action", "turn_incomplete") for r in records)
                )
                if clarification_turns >= max_clarification_turns or second_stall:
                    records.append(record)
                    break

                if resolved_mode == "legacy":
                    reply = _get_sim_user_response(response_text, resolved_turn, resolved_expected)
                elif kind == "confirmation":
                    reply = CONFIRMATION_REPLY
                elif kind in ("no_action", "turn_incomplete"):
                    reply = NUDGE_MESSAGE
                elif record.lost_context is True and not any(r.lost_context is True for r in records):
                    # Once per turn, so a judge mistake cannot loop the user on restating.
                    reply = reply_restating(render_transcript(transcript[:-1]), response_text)
                elif answers_left:
                    reply = answers_left.pop(0)
                else:
                    reply = reply_from_facts(render_transcript(transcript[:-1]), response_text, turn.set_answers)
                record.reply = clip(reply)
                records.append(record)

                clarification_turns += 1
                total_clarification_turns += 1
                current_message = reply

            # `declared` is what THIS turn's final set_skills call asked for (None when it
            # made no call); `active_skills` is what is actually active during the turn. No
            # call carries the previous set over; a call replaces it outright, including
            # when it declares an empty list. See active_skills' declaration above.
            declarations = _set_skills_declarations(all_tool_calls)
            for declaration in declarations:
                ever_declared_skills.update(declaration)
            declared = declarations[-1] if declarations else None
            if declared is not None:
                active_skills = set(declared)
            skill_routing = turn.expected_skill in active_skills
            output_present = _check_output_present(resolved_turn, final_result) if final_result else False
            output_correct: bool | None = None
            mismatches: list[str] = []
            if final_result and output_present:
                output_correct, mismatches = _check_output_correct(resolved_turn, final_result, all_tool_calls)

            # Capture metric output for $ref resolution in subsequent turns.
            if final_result and turn.expected_output_type == "metric":
                metric_data = _extract_metric_result(all_tool_calls)
                if metric_data:
                    turn_outputs[turn.turn_id] = metric_data

            turn_results.append(
                TurnResult(
                    turn_id=turn.turn_id,
                    expected_skill=turn.expected_skill,
                    skill_routing=skill_routing,
                    output_present=output_present,
                    # A chat fault used to escape the whole run, so reaching here did mean no
                    # error. Now that it is caught and recorded, this has to read it back --
                    # otherwise a turn whose chat call failed reports no_error=True.
                    no_error=turn_exit is not LoopExit.CHAT_ERROR,
                    activated_skills=declared or [],
                    active_skills=sorted(active_skills),
                    clarification_turns_used=clarification_turns,
                    output_correct=output_correct,
                    exit_reason=turn_exit,
                    mismatches=mismatches,
                    clarifications=records,
                    depends_on=list(turn.depends_on),
                )
            )

    finally:
        if owns_conversation and conversation_id:
            client.delete_conversation(conversation_id)
        created.delete(sdk, workspace_id)
        client.close()

    # Not derived from TurnResult.activated_skills: that field carries only each turn's FINAL
    # declaration, so a skill replaced within its own turn is absent from it despite having
    # been activated. See ever_declared_skills' declaration above.
    full_skill_coverage = set(fixture.expected_skills).issubset(ever_declared_skills)
    conversation_success = all(tr.skill_success for tr in turn_results)
    context_success, kept_rate, before_break, lost, stalled = _context_summary(turn_results, fixture)
    judged = any(c.kind == "question" for tr in turn_results for c in tr.clarifications)

    return ConversationResult(
        conversation_id=conversation_id,
        turn_results=turn_results,
        full_skill_coverage=full_skill_coverage,
        conversation_success=conversation_success,
        total_clarification_turns=total_clarification_turns,
        max_clarification_turns=max_clarification_turns,
        total_steps=total_steps,
        reasoning_steps=reasoning_steps,
        response_id=response_id,
        tool_call_events=conversation_tool_call_events,
        reasoning_step_events=conversation_reasoning_step_events,
        context_success=context_success,
        context_kept_rate=kept_rate,
        turns_before_first_break=before_break,
        lost_context_clarifications=lost,
        stalled_turns=stalled,
        mode=resolved_mode,
        judge_model=judge.model_name if judged else None,
    )


def _conversation_detail(result: ConversationResult) -> dict:
    return {
        "mode": result.mode,
        "full_skill_coverage": result.full_skill_coverage,
        "conversation_success": result.conversation_success,
        "context_success": result.context_success,
        "context_kept_rate": result.context_kept_rate,
        "turns_before_first_break": result.turns_before_first_break,
        "lost_context_clarifications": result.lost_context_clarifications,
        "stalled_turns": result.stalled_turns,
        "total_clarification_turns": result.total_clarification_turns,
        "max_clarification_turns": result.max_clarification_turns,
        "judge_model": result.judge_model,
        "turns": [tr.detail() for tr in result.turn_results],
        **timeline_detail(result.tool_call_events, result.reasoning_step_events),
    }


class ConversationAssertionError(AgenticAssertionError):
    """Raised when a conversation evaluation fails."""


def evaluate_agentic_conversation(
    host: str,
    token: str,
    workspace_id: str,
    fixture: ConversationFixture,
    max_clarification_turns: int = _DEFAULT_MAX_CLARIFICATION_TURNS,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "conversation",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    mode: ConversationMode | None = None,
    clarification_judge: ClarificationJudge | None = None,
) -> AgenticEvalOutcome:
    """Run conversation evaluation, log to Langfuse, and raise on failure.

    ``mode`` (default: ``GD_EVAL_CONVERSATION_MODE``, else ``legacy``) picks which verdict
    raises; both are always scored. Returns the conversation's outcome (reasoning_steps,
    conversation_id, response_id) as an AgenticEvalOutcome on success; on failure the same
    three values are attached to the raised exception as
    ``.reasoning_steps``/``.conversation_id``/``.response_id`` (mirrors the
    `conversation_id`-on-exception idiom in `ChatClient.ask()`) so callers can retrieve them
    either way.
    """
    resolved_mode = resolve_conversation_mode(mode)
    langfuse, window_start = open_trace_window(langfuse)
    result = run_agentic_conversation(
        host=host,
        token=token,
        workspace_id=workspace_id,
        fixture=fixture,
        max_clarification_turns=max_clarification_turns,
        initial_conversation_id=initial_conversation_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        mode=resolved_mode,
        clarification_judge=clarification_judge,
    )
    passed = result.context_success if resolved_mode == "context" else result.conversation_success

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()
        # Resolved here, not inside the task: deferring it would make the queued task hold
        # the whole fixture until the drain.
        ds_name = dataset_name or fixture.dataset_name
        failed_turns = {tr.turn_id: tr.failure_reasons() for tr in result.turn_results if not tr.context_success}

        def _write_scores(ctx: RunTraceContext) -> None:

            pt = ctx.trace(result.conversation_id)
            with ctx.observe(
                pt,
                0,
                conversation_id=result.conversation_id,
                output={
                    "mode": result.mode,
                    "conversation_success": result.conversation_success,
                    "context_success": result.context_success,
                    "full_skill_coverage": result.full_skill_coverage,
                    "failed_turns": failed_turns,
                },
            ) as tid:
                ctx.score(
                    tid,
                    name="conversation_success",
                    value=float(result.conversation_success),
                    data_type="BOOLEAN",
                )
                ctx.score(
                    tid,
                    name="context_success",
                    value=float(result.context_success),
                    data_type="BOOLEAN",
                )
                ctx.score(
                    tid,
                    name="full_skill_coverage",
                    value=float(result.full_skill_coverage),
                    data_type="BOOLEAN",
                )
                if result.context_kept_rate is not None:
                    ctx.score(tid, name="context_kept_rate", value=result.context_kept_rate, data_type="NUMERIC")
                ctx.score(
                    tid, name="turns_before_first_break", value=result.turns_before_first_break, data_type="NUMERIC"
                )
                ctx.score(
                    tid,
                    name="lost_context_clarifications",
                    value=result.lost_context_clarifications,
                    data_type="NUMERIC",
                )
                ctx.score(tid, name="stalled_turns", value=result.stalled_turns, data_type="NUMERIC")
                # One turn per fixture turn, plus every simulated-user round the agent triggered.
                # The clarification count alone hides how much of the conversation the fixture
                # asked for, so the comparison needs the total.
                ctx.score(
                    tid,
                    name="turns",
                    value=len(result.turn_results) + result.total_clarification_turns,
                    data_type="NUMERIC",
                )
                ctx.score(tid, name="steps", value=result.total_steps, data_type="NUMERIC")
                ctx.score(
                    tid,
                    name="clarification_turns",
                    value=result.total_clarification_turns,
                    data_type="NUMERIC",
                )
                # Reports read gate_passed first; it must be the verdict this run raised on.
                log_gate_scores(ctx, tid, gate=None, pass_at_k=passed, pass_power_k=passed)
                for tr in result.turn_results:
                    ctx.score(
                        tid,
                        name=f"turn_{tr.turn_id}_skill_success",
                        value=float(tr.skill_success),
                        data_type="BOOLEAN",
                    )
                strict_checks = {
                    "conversation_success": result.conversation_success,
                    "full_skill_coverage": result.full_skill_coverage,
                }
                if resolved_mode == "context":
                    strict_checks["context_success"] = result.context_success
                ctx.quality(
                    tid,
                    strict_checks=strict_checks,
                    latency_sec=pt.latency if pt else None,
                    cost_usd=pt.total_cost if pt else None,
                )

        # Before the pass@K raise: a failing item's scores are the ones worth having.
        submit_trace_scoring(
            submit_trace_link,
            RunIdentity(
                host,
                token,
                workspace_id,
                ds_name,
                run_timestamp,
                model_version_override,
                run_metadata_extra,
                reasoning_effort,
            ),
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=[result.conversation_id],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=False,
            write_scores=_write_scores,
            item_input=fixture.turns[0].message if fixture.turns else fixture.id,
        )

    detail = _conversation_detail(result)

    if not passed:
        if resolved_mode == "context":
            failed = {tr.turn_id: tr.failure_reasons() for tr in result.turn_results if not tr.context_success}
            message = f"Conversation assertion failed (context). Failed turns: {failed}"
        else:
            legacy_failed = [tr.turn_id for tr in result.turn_results if not tr.skill_success]
            message = (
                f"Conversation assertion failed. "
                f"full_skill_coverage={result.full_skill_coverage}. "
                f"Failed turns: {legacy_failed}"
            )
        exc = ConversationAssertionError(message)
        exc.reasoning_steps = result.reasoning_steps
        exc.conversation_id = result.conversation_id
        exc.response_id = result.response_id
        exc.detail = detail
        # This kind takes no k and drives its fixture exactly once, whatever --runs asks
        # for. Saying so explicitly stops the report claiming K runs that never happened.
        exc.runs_passed = 0
        exc.runs_effective = 1
        raise exc
    return AgenticEvalOutcome(
        reasoning_steps=result.reasoning_steps,
        conversation_id=result.conversation_id,
        response_id=result.response_id,
        detail=detail,
        runs_passed=1,
        runs_effective=1,
    )
