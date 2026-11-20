# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic agent-switcher evaluation: one conversation, switched between agents mid-way.

Each run replays the item's turns on a new conversation created with ``agent_id``. A turn
with ``switch_to`` calls ``switchAgent`` before its message is sent. Per-turn checks come
from the item:

- ``must_include`` / ``must_not_include``: LLM judge criteria, graded against the
  transcript so far (earlier answers labelled with the agent that gave them).
- ``skills_used`` / ``skills_not_used``: skills whose tools the turn ran, read from the
  stored items: ``skillsInUse`` of the turn's ``toolCall`` items. A skill carried over from
  an earlier turn counts once one of its tools runs; a requested skill whose tools never
  ran does not.
- ``alert_metric``: the primary measure of the turn's alert proposal is that metric.
- ``visualization``: the turn's created chart uses these metrics and attributes.

The skills checks and two run checks are read from the stored items after the last turn:

- ``agent_stamped``: every assistant item of a turn carries the agent active at that turn.
- ``switch_marker``: one system marker per real switch, carrying the new agent, before the
  turn it was made for. A switch to the agent already bound is a no-op and has no marker.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._failure_message import FailedCheck, failed_check_records
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._outcome import (
    agentic_detail,
    agentic_success,
    attach_labels,
    chat_failure_exit,
    failure_message_head,
    label_runs,
    mark_unscored_run,
    raise_agentic_failure,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    conversations_to_link,
    open_item_trace,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ADHOC_VIZ_ID, ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError, LLMJudge
from gooddata_eval.core.evaluators._rubric import Criterion, grade_rubric
from gooddata_eval.core.langfuse.item_scope import item_scope
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    AgentSwitcherInput,
    AgentSwitcherTurn,
    AgentSwitcherVisualization,
    ChatResult,
    DatasetItem,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
    shift_and_index_events,
)
from gooddata_eval.core.scoring import get_dimension_uri_set, get_metric_uri_set
from gooddata_eval.core.timing import PhaseTimings, sum_timings

_TEST_KIND = "agentic_agent_switcher"
_DEFAULT_K = 1
# Per earlier answer in the judge transcript; the turn under grading is never cut.
_TRANSCRIPT_ANSWER_CHARS = 2000

_CONTEXT_STEP = (
    "The INPUT is a conversation between a user and an analytics assistant, ending with the user's "
    "LATEST MESSAGE. Each earlier answer is labelled with the agent that gave it; the conversation may "
    "have been switched from one agent to another. Use the conversation only to resolve what the "
    "criterion refers to (for example 'the plan the user gave earlier'). Grade the ACTUAL OUTPUT, the "
    "answer to the latest message, not the earlier answers."
)

_POSITIVE_STEPS = [
    _CONTEXT_STEP,
    "Read the EXPECTED OUTPUT: one criterion the answer must satisfy.",
    "Score 1 if the actual output clearly satisfies the criterion.",
    "Score 0 if the criterion is missing, contradicted, or only partially addressed.",
]

# A presence question, inverted in code -- see the same split in evaluators/takeaway.py.
_VIOLATION_STEPS = [
    _CONTEXT_STEP,
    "Read the CHARACTERISTIC described in EXPECTED OUTPUT, including any exceptions it states.",
    "Score 1 if the actual output clearly exhibits the described characteristic.",
    "Score 0 if it does not exhibit it.",
]


class AgentSwitcherAssertionError(AgenticAssertionError):
    """Raised when an agent-switcher evaluation fails its gate."""


@dataclass
class TurnRecord:
    """What one turn sent, which agent answered, and how its checks went."""

    turn: int
    message: str
    agent_id: str
    switch_to: str | None = None
    answer: str = ""
    answering_agents: list[str] = field(default_factory=list)
    # Skills whose tools ran in the turn (`skillsInUse` of its toolCall items).
    skills: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)
    reasons: dict[str, str] = field(default_factory=dict)

    def as_record(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "message": self.message,
            "switch_to": self.switch_to,
            "agent_id": self.agent_id,
            "answering_agents": self.answering_agents,
            "answer": self.answer,
            "skills": self.skills,
            "checks": self.checks,
            "reasons": self.reasons,
        }


@dataclass
class AgentSwitcherRunResult:
    """One replay of the item's turns on its own conversation."""

    conversation_id: str
    turns: list[TurnRecord] = field(default_factory=list)
    # Every check that ran, by name: per turn `turn<N>_<check>`, per run `agent_stamped`, `switch_marker`.
    checks: dict[str, bool] = field(default_factory=dict)
    failed: list[FailedCheck] = field(default_factory=list)
    # A switch, chat or items call that failed; the run stopped there.
    error: str | None = None
    # Set only when every graded check passed and a judge criterion went ungraded.
    judge_error: str | None = None
    exit_reason: LoopExit = LoopExit.SUCCESS
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    timings: PhaseTimings = field(default_factory=PhaseTimings)
    run_latency_s: float = 0.0

    @property
    def passed(self) -> bool:
        return self.error is None and self.judge_error is None and all(self.checks.values())

    def fail(self, check: FailedCheck) -> None:
        self.checks[check.name] = False
        self.failed.append(check)


@dataclass
class AgenticAgentSwitcherSummary:
    """Aggregated outcome of K runs."""

    run_results: list[AgentSwitcherRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: AgentSwitcherRunResult

    @property
    def scored_run_results(self) -> list[AgentSwitcherRunResult]:
        return [r for r in self.run_results if r.judge_error is None]

    @property
    def judge_errors(self) -> list[str]:
        return [r.judge_error for r in self.run_results if r.judge_error is not None]


@dataclass
class _Judges:
    positive: LLMJudge
    violation: LLMJudge


def _strip_type(ref: str) -> str:
    """`metric/revenue` -> `revenue`; a bare id stays as it is."""
    return ref.split("/", 1)[1] if "/" in ref else ref


def _primary_metric_id(proposal: Any) -> str | None:
    """Metric id of an alert proposal's primary measure.

    - primary = first of `alert.execution.measures` (gen-ai puts the alerted metric first);
    - a second measure is only the comparison side, so it is not read.
    """
    alert = proposal.get("alert") if isinstance(proposal, dict) else None
    execution = alert.get("execution") if isinstance(alert, dict) else None
    measures = execution.get("measures") if isinstance(execution, dict) else None
    if not isinstance(measures, list) or not measures:
        return None
    node: Any = measures[0]
    for key in ("definition", "measure", "item", "identifier", "id"):
        node = node.get(key) if isinstance(node, dict) else None
    return node if isinstance(node, str) else None


def _proposal_metric_ids(chat_result: ChatResult) -> list[str]:
    """Primary metric id of each of the turn's alert proposals."""
    return [i for i in (_primary_metric_id(p) for p in chat_result.alert_proposals) if i is not None]


def _render_turn(chat_result: ChatResult) -> str:
    """The answer text, plus one line naming the last alert proposal (no payload dump)."""
    chunks = [render_answer_text(chat_result)]
    if chat_result.alert_proposals:
        proposal = chat_result.alert_proposals[-1]
        cta = proposal.get("cta") if isinstance(proposal, dict) else None
        metric = _primary_metric_id(proposal)
        chunks.append(f"[Alert proposal: {cta or 'no prompt'}; metric {metric or 'unknown'}]")
    return "\n\n".join(chunk for chunk in chunks if chunk)


def _visualization_problem(expected: AgentSwitcherVisualization, chat_result: ChatResult) -> str | None:
    """None when a created chart uses every expected metric and attribute, else what was created."""
    objects = chat_result.created_visualizations.objects if chat_result.created_visualizations else []
    # ADHOC_VIZ_ID: tool args of a call that produced no chart part, so not a created chart
    objects = [viz for viz in objects if viz.id != ADHOC_VIZ_ID]
    if not objects:
        return "no visualization was created"
    # Metrics keep their type: a bare id means `metric/<id>`, so a fact of that id never matches.
    want_metrics = {m if "/" in m else f"metric/{m}" for m in expected.metrics}
    want_attributes = {_strip_type(a) for a in expected.attributes}
    seen: list[dict[str, list[str]]] = []
    for viz in objects:
        metrics = get_metric_uri_set(viz)
        attributes = {_strip_type(u) for u in get_dimension_uri_set(viz)}
        if want_metrics <= metrics and want_attributes <= attributes:
            return None
        seen.append({"metrics": sorted(metrics), "attributes": sorted(attributes)})
    return f"created {seen}"


def _set_check(
    record: TurnRecord, run: AgentSwitcherRunResult, name: str, ok: bool, expected: Any, actual: Any
) -> None:
    """Record one per-turn check on the turn and, as `turn<N>_<name>`, on the run."""
    record.checks[name] = ok
    full = f"turn{record.turn}_{name}"
    if ok:
        run.checks[full] = True
    else:
        run.fail(FailedCheck(full, expected=expected, actual=actual))


def _turn_code_checks(
    record: TurnRecord, run: AgentSwitcherRunResult, turn: AgentSwitcherTurn, result: ChatResult
) -> None:
    """The turn's checks read from its chat result."""
    checks = turn.checks
    if checks.alert_metric is not None:
        ids = _proposal_metric_ids(result)
        ok = _strip_type(checks.alert_metric) in {_strip_type(i) for i in ids}
        _set_check(record, run, "alert_metric", ok, checks.alert_metric, ids)
    if checks.visualization is not None:
        problem = _visualization_problem(checks.visualization, result)
        _set_check(record, run, "visualization", problem is None, checks.visualization.model_dump(), problem)


def _skills_checks(
    record: TurnRecord, run: AgentSwitcherRunResult, turn: AgentSwitcherTurn, unreadable: str | None
) -> None:
    """`skills_used` / `skills_not_used` against `record.skills`; both fail when the items were unreadable."""
    checks = turn.checks
    if checks.skills_used:
        ok = unreadable is None and set(checks.skills_used) <= set(record.skills)
        _set_check(record, run, "skills_used", ok, checks.skills_used, unreadable or record.skills)
    if checks.skills_not_used:
        used = sorted(set(checks.skills_not_used) & set(record.skills))
        ok = unreadable is None and not used
        _set_check(record, run, "skills_not_used", ok, f"none of {checks.skills_not_used}", unreadable or used)


def _skills_in_use(item: dict[str, Any]) -> list[str]:
    """`skillsInUse[].name` of a toolCall item; empty for any other item."""
    content = item.get("content")
    if item.get("role") != "assistant" or not isinstance(content, dict) or content.get("type") != "toolCall":
        return []
    refs = item.get("skillsInUse")
    names = (ref.get("name") for ref in refs if isinstance(ref, dict)) if isinstance(refs, list) else ()
    return [n for n in names if isinstance(n, str)]


def _switch_error(turn: int, agent_id: str, exc: Exception) -> str:
    head = f"switchAgent to {agent_id!r} before turn {turn} failed"
    if not isinstance(exc, httpx.HTTPStatusError):
        return f"{head}: {type(exc).__name__}: {exc}"
    status = exc.response.status_code
    if status == 404:
        return f"{head} with 404: the agent-switching feature flag may be off, or the agent is unknown"
    if status == 403:
        return f"{head} with 403: no access to the agent"
    return f"{head} with {status}: {exc.response.text[:200]}"


def _check_items(
    run: AgentSwitcherRunResult,
    spec: AgentSwitcherInput,
    items: list[dict[str, Any]],
    expected_markers: list[tuple[int, str]],
) -> None:
    """Skills checks, `agent_stamped` and `switch_marker` from the stored items.

    - a user item opens a turn; the turn runs up to the next user item;
    - a switch marker (`trigger` `agent_switched`) counts by the user items before it, so the
      marker for the switch before turn N comes after N-1 user items;
    - fills each turn's answering agents and used skills.
    """
    user_items = 0
    answering: dict[int, list[str]] = {}
    skills: dict[int, list[str]] = {}
    markers: list[tuple[int, str]] = []
    for item in items:
        role = item.get("role")
        if role == "user":
            user_items += 1
        elif role == "assistant":
            answering.setdefault(user_items, []).append(str(item.get("agentId")))
            turn_skills = skills.setdefault(user_items, [])
            turn_skills.extend(n for n in _skills_in_use(item) if n not in turn_skills)
        elif role == "system" and item.get("trigger") == "agent_switched":
            markers.append((user_items, str(item.get("agentId") or item.get("newAgentId"))))

    for record, turn in zip(run.turns, spec.turns, strict=False):
        record.skills = skills.get(record.turn, [])
        _skills_checks(record, run, turn, unreadable=None)

    stamping: list[str] = []
    if user_items != len(run.turns):
        stamping.append(f"{user_items} user item(s) for {len(run.turns)} turn(s)")
    if answering.get(0):
        stamping.append(f"assistant item(s) before the first user item: {answering[0]}")
    for record in run.turns:
        agents = answering.get(record.turn, [])
        record.answering_agents = list(dict.fromkeys(agents))
        if not agents:
            stamping.append(f"turn {record.turn}: no assistant item")
        elif record.answering_agents != [record.agent_id]:
            stamping.append(f"turn {record.turn}: {record.answering_agents}, active {record.agent_id!r}")
    if stamping:
        expected = "every assistant item stamped with the active agent"
        run.fail(FailedCheck("agent_stamped", expected=expected, actual=stamping))
    else:
        run.checks["agent_stamped"] = True

    if markers == expected_markers:
        run.checks["switch_marker"] = True
    else:
        run.fail(
            FailedCheck(
                "switch_marker",
                expected=[{"after_user_items": n, "agent_id": a} for n, a in expected_markers],
                actual=[{"after_user_items": n, "agent_id": a} for n, a in markers],
            )
        )


def _transcript(turns: list[TurnRecord], current: TurnRecord) -> str:
    """The conversation before `current`, then its message, for the judge's INPUT."""
    lines = ["CONVERSATION BEFORE:"] if turns else ["CONVERSATION BEFORE: (none)"]
    for record in turns:
        agent = ", ".join(record.answering_agents) or record.agent_id
        answer = " ".join(record.answer.split())
        if len(answer) > _TRANSCRIPT_ANSWER_CHARS:
            answer = answer[: _TRANSCRIPT_ANSWER_CHARS - 1] + "…"
        lines.append(f"USER: {record.message}")
        lines.append(f"ASSISTANT (agent {agent}): {answer}")
    current_agent = ", ".join(current.answering_agents) or current.agent_id
    lines.append(f"LATEST MESSAGE: {current.message}")
    lines.append(f"ANSWERED BY: agent {current_agent}")
    return "\n".join(lines)


def _judge_turns(run: AgentSwitcherRunResult, spec: AgentSwitcherInput, judges: _Judges) -> None:
    """Grade every turn's criteria; an ungraded criterion leaves the run's verdict open."""
    ungraded: list[str] = []
    for index, (record, turn) in enumerate(zip(run.turns, spec.turns, strict=True)):
        if not turn.checks.judged:
            continue
        must_include: list[Criterion] = [(f"include_{i}", c) for i, c in enumerate(turn.checks.must_include)]
        must_not_include: list[Criterion] = [(f"exclude_{i}", c) for i, c in enumerate(turn.checks.must_not_include)]
        detail: dict[str, Any] = {}
        try:
            grade_rubric(
                judges.positive,
                judges.violation,
                question=_transcript(run.turns[:index], record),
                actual=record.answer,
                must_include=must_include,
                must_not_include=must_not_include,
                rubric=[],
                detail=detail,
            )
        except Exception as exc:
            # A judge request failure (timeout, provider error): the turn's criteria not yet
            # graded stay ungraded, as for an unreadable verdict; the other runs still count.
            for key, _ in [*must_include, *must_not_include]:
                if key not in detail:
                    detail[f"{key}_reason"] = f"UNGRADED: {type(exc).__name__}: {exc}"
        for key, criterion in [*must_include, *must_not_include]:
            reason = str(detail.get(f"{key}_reason", ""))
            record.reasons[key] = reason
            if key not in detail:
                ungraded.append(f"turn {record.turn} {key}: {reason}")
                continue
            ok = detail[key] is True
            record.checks[key] = ok
            name = f"turn{record.turn}_{key}"
            if ok:
                run.checks[name] = True
            else:
                run.fail(FailedCheck(name, part="judge", expected=criterion, actual=reason))
    if ungraded and all(run.checks.values()):
        run.judge_error = " | ".join(ungraded)


def _run_once(
    client: ChatClient, spec: AgentSwitcherInput, judges: _Judges | None, conversation_id: str
) -> AgentSwitcherRunResult:
    started = time.monotonic()
    run = AgentSwitcherRunResult(conversation_id=conversation_id)
    active = spec.agent_id
    # (user items before the marker, new agent) for every switch that changes the agent.
    expected_markers: list[tuple[int, str]] = []
    agent_s = 0.0
    offsets = (0.0, 0, 0)

    for number, turn in enumerate(spec.turns, start=1):
        if turn.switch_to is not None:
            try:
                conversation = client.switch_agent(conversation_id, turn.switch_to)
            # ValueError: a 200 whose body is not JSON
            except (httpx.HTTPError, ValueError) as exc:
                run.error = _switch_error(number, turn.switch_to, exc)
                run.exit_reason = LoopExit.CHAT_ERROR
                run.fail(FailedCheck(f"turn{number}_switched", expected=turn.switch_to, actual=run.error))
                break
            bound = conversation.get("agentId") if isinstance(conversation, dict) else None
            if bound != turn.switch_to:
                run.error = f"switchAgent before turn {number} answered agentId {bound!r}, asked for {turn.switch_to!r}"
                run.exit_reason = LoopExit.CHAT_ERROR
                run.fail(FailedCheck(f"turn{number}_switched", expected=turn.switch_to, actual=bound))
                break
            if turn.switch_to != active:
                expected_markers.append((number - 1, turn.switch_to))
            active = turn.switch_to

        record = TurnRecord(turn=number, message=turn.message, agent_id=active, switch_to=turn.switch_to)
        sent = time.monotonic()
        try:
            result = client.send_message(conversation_id, turn.message)
        # httpx.HTTPError: a status or transport error that outlasted the retries
        except (ChatError, httpx.HTTPError) as exc:
            agent_s += time.monotonic() - sent
            partial = exc.partial_result if isinstance(exc, ChatError) else None
            if partial is not None:
                run.reasoning_steps.extend(partial.reasoning_steps or [])
                run.response_id = partial.response_id or run.response_id
            run.error = f"turn {number}: {type(exc).__name__}: {exc}"
            run.exit_reason = chat_failure_exit(exc)
            run.fail(FailedCheck(f"turn{number}_answered", actual=run.error))
            run.turns.append(record)
            break
        agent_s += time.monotonic() - sent
        record.answer = _render_turn(result)
        run.reasoning_steps.extend(result.reasoning_steps or [])
        run.response_id = result.response_id or run.response_id
        offsets = shift_and_index_events(
            result, turn_offset=offsets[0], tool_index_offset=offsets[1], reasoning_index_offset=offsets[2]
        )
        run.tool_call_events.extend(result.tool_call_events or [])
        run.reasoning_step_events.extend(result.reasoning_step_events or [])
        run.turns.append(record)
        _turn_code_checks(record, run, turn, result)

    judge_s = 0.0
    if run.error is None:
        try:
            items = client.list_items(conversation_id)
        except (httpx.HTTPError, ValueError) as exc:
            run.error = f"reading the conversation items failed: {type(exc).__name__}: {exc}"
            run.exit_reason = LoopExit.CHAT_ERROR
            run.fail(FailedCheck("items_read", actual=run.error))
            for record, turn in zip(run.turns, spec.turns, strict=False):
                _skills_checks(record, run, turn, unreadable="items unreadable")
        else:
            _check_items(run, spec, items, expected_markers)
            if judges is not None:
                judged = time.monotonic()
                _judge_turns(run, spec, judges)
                judge_s = time.monotonic() - judged

    run.timings = PhaseTimings(agent_s=agent_s, judge_s=judge_s)
    run.run_latency_s = time.monotonic() - started
    return run


def run_agentic_agent_switcher(
    host: str,
    token: str,
    workspace_id: str,
    spec: AgentSwitcherInput,
    k: int = _DEFAULT_K,
    reasoning_effort: ReasoningEffort | None = None,
    user_context: dict | None = None,
) -> AgenticAgentSwitcherSummary:
    """Replay the item K times, each run on a conversation of its own, and return a summary.

    Raises:
        ValueError: ``k`` is below 1.
    """
    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")
    # Built before any request: a missing judge key fails the item, not its runs.
    judges = (
        _Judges(LLMJudge(_POSITIVE_STEPS), LLMJudge(_VIOLATION_STEPS))
        if any(t.checks.judged for t in spec.turns)
        else None
    )
    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=spec.agent_id,
        user_context=user_context,
    )
    run_results: list[AgentSwitcherRunResult] = []
    try:
        for _ in range(k):
            conversation_id = client.create_conversation()
            try:
                run_results.append(_run_once(client, spec, judges, conversation_id))
            finally:
                client.delete_conversation(conversation_id)
    finally:
        client.close()

    # As general_question: pass@K ignores ungraded runs, pass^K is not met by one.
    scored = [r for r in run_results if r.judge_error is None]
    pass_at_k = any(r.passed for r in scored)
    pass_power_k = len(scored) == len(run_results) and all(r.passed for r in scored)
    best = max(scored or run_results, key=lambda r: (r.passed, sum(r.checks.values())))
    return AgenticAgentSwitcherSummary(run_results, pass_at_k, pass_power_k, best)


def _kind_fields(run: AgentSwitcherRunResult) -> dict[str, Any]:
    return {
        **run.checks,
        "turns": [t.as_record() for t in run.turns],
        **({"error": run.error} if run.error is not None else {}),
    }


def _run_detail(run: AgentSwitcherRunResult) -> dict[str, Any]:
    return {
        **_kind_fields(run),
        "latency_breakdown": build_latency_breakdown(run.tool_call_events, run.reasoning_step_events),
    }


def _failed_checks(run: AgentSwitcherRunResult) -> list[dict]:
    return failed_check_records(run.failed)


def _attach_diagnostics(
    error: AgenticAssertionError | JudgeResponseError,
    best: AgentSwitcherRunResult,
    detail: dict,
    failed_runs: list[dict],
    runs_passed: int,
    runs_effective: int,
    run_latencies_s: list[float],
) -> None:
    error.reasoning_steps = best.reasoning_steps
    error.conversation_id = best.conversation_id
    error.response_id = best.response_id
    error.detail = detail
    error.runs_passed = runs_passed
    error.runs_effective = runs_effective
    error.failed_runs = failed_runs
    error.run_latencies_s = run_latencies_s
    error.best_run_latency_s = best.run_latency_s


def _dataset_item(dataset_item: DatasetItem | dict, dataset_name: str) -> tuple[DatasetItem, AgentSwitcherInput]:
    if isinstance(dataset_item, DatasetItem):
        item = dataset_item
    else:
        item = DatasetItem.model_validate(
            {"id": "", "test_kind": _TEST_KIND, "expected_output": {}, **dataset_item, "dataset_name": dataset_name}
        )
    if item.agent_switcher_input is None:
        raise ValueError(f"{_TEST_KIND} item '{item.id}' is missing required 'agent_switcher_input'.")
    return item, item.agent_switcher_input


def evaluate_agentic_agent_switcher(
    host: str,
    token: str,
    workspace_id: str,
    dataset_item: DatasetItem | dict,
    k: int = _DEFAULT_K,
    langfuse: object | None = None,
    dataset_item_id: str | None = None,
    dataset_name: str = "agent_switcher",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    gate: EvalGate = DEFAULT_GATE,
) -> AgenticEvalOutcome:
    """Run the agent-switcher evaluation K times, log to Langfuse, and raise on a failed gate.

    Args:
        host: GoodData host URL.
        token: API token.
        workspace_id: Workspace the conversations run in.
        dataset_item: The item as stored, carrying `agent_switcher_input` and optionally `user_context`.
        k: Runs per item; each creates its own conversation.
        langfuse: Langfuse client; built from the LANGFUSE_* environment when None.
        dataset_item_id: Langfuse item id; the item's own `id` when None.
        dataset_name: Langfuse dataset name; prefixes the experiment run name.
        run_timestamp: Shared run timestamp for the run name.
        model_version_override: Model-version tag for the run.
        run_metadata_extra: Extra experiment-run metadata.
        reasoning_effort: Sent on every message.
        submit_trace_link: How the Langfuse block is run; inline by default.
        gate: `any` (pass@K) or `power` (pass^K).

    Raises:
        AgentSwitcherAssertionError: the gate did not pass.
        JudgeResponseError: the judge returned no readable verdict for any run.
        ValueError: the item has no valid `agent_switcher_input`, raised before any request.
    """
    item, spec = _dataset_item(dataset_item, dataset_name)
    item_id = item.id if dataset_item_id is None else dataset_item_id
    identity = RunIdentity(
        host,
        token,
        workspace_id,
        dataset_name,
        run_timestamp,
        model_version_override,
        run_metadata_extra,
        reasoning_effort,
    )
    langfuse, window_start, scope = open_item_trace(langfuse, identity, item_id, suffix_runs=k > 1)
    with item_scope(scope):
        summary = run_agentic_agent_switcher(
            host=host,
            token=token,
            workspace_id=workspace_id,
            spec=spec,
            k=k,
            reasoning_effort=reasoning_effort,
            user_context=item.user_context,
        )

    run_labels = label_runs(summary.run_results, passed=lambda r: r.passed)

    if langfuse is not None and item_id:
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)
            for run_idx, run in enumerate(summary.run_results):
                if run.judge_error is not None:
                    mark_unscored_run(ctx, run_idx, run.conversation_id, run_labels.error_label(run_idx))
                    continue
                pt = ctx.trace(run.conversation_id)
                turn_checks = [ok for name, ok in run.checks.items() if name.startswith("turn")]
                with ctx.observe(
                    pt, run_idx, conversation_id=run.conversation_id, output={"agent_switcher_pass": run.passed}
                ) as tid:
                    ctx.score(tid, name="agent_switcher_pass", value=float(run.passed), data_type="BOOLEAN")
                    for name in ("agent_stamped", "switch_marker"):
                        if name in run.checks:
                            ctx.score(tid, name=name, value=float(run.checks[name]), data_type="BOOLEAN")
                    if turn_checks:
                        ctx.score(tid, name="turn_checks_pass", value=float(all(turn_checks)), data_type="BOOLEAN")
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)
                    ctx.quality(
                        tid,
                        strict_checks=run.checks,
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        submit_trace_scoring(
            submit_trace_link,
            identity,
            langfuse=langfuse,
            dataset_item_id=item_id,
            conversation_ids=conversations_to_link(
                [r.conversation_id for r in summary.scored_run_results],
                [r.conversation_id for r in summary.run_results if r.judge_error is not None],
            ),
            window_start=window_start,
            window_end=window_end,
            suffix_runs=k > 1,
            write_scores=_write_scores,
            scope=scope,
            item_input=item.question,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])
    unscored = summary.judge_errors
    runs_passed = sum(1 for r in summary.scored_run_results if r.passed)
    runs_effective = len(summary.run_results)
    run_latencies_s = [r.run_latency_s for r in summary.run_results]
    best = summary.best
    detail = agentic_detail(
        best.tool_call_events,
        best.reasoning_step_events,
        **_kind_fields(best),
        **({"unscored_runs": len(unscored), "judge_errors": unscored} if unscored else {}),
    )
    failed_runs = build_failed_runs(
        summary.run_results, labels=run_labels, detail=_run_detail, failed_checks=_failed_checks
    )

    if not summary.scored_run_results:
        error = JudgeResponseError(
            f"judge returned no readable verdict for any of the {len(summary.run_results)} run(s): "
            + " | ".join(unscored)
        )
        _attach_diagnostics(error, best, detail, failed_runs, runs_passed, runs_effective, run_latencies_s)
        error.timings = item_timings
        attach_labels(error, run_labels, gate)
        raise error

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        head = failure_message_head(gate, run_labels, runs_passed, failed_runs, len(unscored))
        raise_agentic_failure(
            AgentSwitcherAssertionError,
            f"Agent switcher assertion failed. {head}" + (f" Best run error: {best.error}" if best.error else ""),
            harness_error=run_labels.harness_error_record,
            shadow=run_labels.shadow(gate),
            reasoning_steps=best.reasoning_steps,
            conversation_id=best.conversation_id,
            response_id=best.response_id,
            detail=detail,
            runs_passed=runs_passed,
            runs_effective=runs_effective,
            failed_runs=failed_runs,
            run_latencies_s=run_latencies_s,
            best_run_latency_s=best.run_latency_s,
            timings=item_timings,
        )
    return agentic_success(
        shadow=run_labels.shadow(gate),
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        failed_runs=failed_runs,
        run_latencies_s=run_latencies_s,
        best_run_latency_s=best.run_latency_s,
        timings=item_timings,
    )
