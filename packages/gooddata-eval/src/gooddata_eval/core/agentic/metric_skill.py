# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic metric-skill evaluation runner."""

from __future__ import annotations

import os
import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import httpx
from gooddata_api_client.exceptions import NotFoundException
from gooddata_sdk import GoodDataSdk

from gooddata_eval.core.agentic._clarification import read_first_reply
from gooddata_eval.core.agentic._conversation_context import asks_in_text
from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._failure_message import FailedCheck, failed_check_records
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._metric_expectation import (
    MetricExpectation,
    field_mismatches,
    first_proposed_maql,
    missing_mentions,
    parse_expectation,
    substitute_placeholders,
    update_mismatches,
)
from gooddata_eval.core.agentic._metric_workspace import MetricWorkspace, WorkspaceReadError, last_suggestions
from gooddata_eval.core.agentic._outcome import (
    CHAT_FAILURE_EXITS,
    agentic_detail,
    agentic_success,
    chat_failure_exit,
    failure_message_head,
    label_runs,
    log_eval_error_score,
    raise_agentic_failure,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_item_trace,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.evaluators._llm_judge import JudgeVerdict, LLMJudge, score_run
from gooddata_eval.core.evaluators._maql import normalize_maql
from gooddata_eval.core.langfuse.item_scope import item_scope
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    shift_and_index_events,
    timeline_detail,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer, run_latency_s, sum_timings

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI: Any = None


def _judge_provider_errors() -> tuple[type[BaseException], ...]:
    """The failures of a judge request at the provider (timeout, outage, rate limit): they leave a run unscored."""
    transport: tuple[type[BaseException], ...] = (httpx.HTTPError, TimeoutError, ConnectionError)
    try:
        from openai import OpenAIError  # noqa: PLC0415
    except ImportError:
        return transport
    return (OpenAIError, *transport)


_DEFAULT_K = 1
_DEFAULT_MAX_ITERATIONS = 7
# Seconds to wait before each check that a deleted metric stayed deleted, so the checks fall
# 3, 6 and 12 seconds after the delete; see _delete_metric.
_DELETE_RECHECK_DELAYS_S: tuple[float, ...] = (3.0, 3.0, 6.0)

# Every check score an options-shape item can publish, beside metric_created and maql_correct. Each is published only
# for an item that opts into it; metric_scored only when the snapshot or the restore failed. A check the harness could
# not read reads False with a "harness:" reason; a run left without a verdict by it is labelled ERROR.
# metric_first_proposal_correct is a diagnostic and never gates.
METRIC_CONDITIONAL_SCORES = (
    "metric_not_created",
    "metric_reuse_named",
    "metric_no_overwrite",
    "metric_clarified",
    "metric_confirmed_first",
    "metric_rubric",
    "metric_fields_correct",
    "metric_updated",
    "metric_all_created",
    "metric_none_deleted",
    "metric_executes",
    "metric_suggestions",
    "metric_scored",
)
METRIC_DIAGNOSTIC_SCORES = ("metric_first_proposal_correct",)

_RUBRIC_STEPS = [
    "EXPECTED OUTPUT states the criteria the assistant's behaviour must meet.",
    "ACTUAL OUTPUT holds every assistant reply of the conversation, in order.",
    "Pass only when every reply meets every criterion. Fail when any reply breaks one.",
]


def _best_maql_match(actual_maql: str, expected_outputs: list[dict]) -> tuple[bool, str]:
    """Try actual MAQL against every candidate; return (matched, best_expected_maql).

    First match wins. First candidate is used for error reporting when none match.
    """
    normalized_actual = normalize_maql(actual_maql)
    for candidate in expected_outputs:
        expected_maql = candidate.get("maql", "")
        if normalized_actual == normalize_maql(expected_maql):
            return True, expected_maql
    return False, expected_outputs[0].get("maql", "") if expected_outputs else ""


class SimulatedResponseError(RuntimeError):
    """The simulated user could not reply: openai missing, no API key, or the provider failed.

    Carries every expected setup/provider failure so callers can end the run without
    swallowing programming errors raised from the same call.
    """


# Separate from evaluators._maql._PROTECTED_RE on purpose: this one only feeds a same-turn
# LLM-prompt hint (see _no_where_clause_hint), never the scoring comparator, so it can afford
# to consume \X escape sequences inside quoted literals without risking maql_correct semantics.
_HINT_PROTECTED_RE = re.compile(r"\{[^}]*\}|\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'")


def _no_where_clause_hint(expected_maqls: list[str]) -> str:
    """Deterministic nudge for when NONE of the accepted candidate MAQLs has a WHERE clause.

    Without this, whether to add a filter is left entirely to the simulating LLM's judgment
    of what the original request "implies" -- the same fuzzy reasoning that caused it to
    inject an unrequested filter in the first place (QA-29094). Checks every candidate, not
    just the first: _best_maql_match accepts any of them, so hinting off just candidate 0
    would risk steering the agent away from a filtered candidate the scorer would still have
    accepted (the mirror-image of the original bug). Strips {type/id} identifiers and quoted
    literals first so a "where" substring inside one of those -- e.g.
    `{metric/somewhere_sales}`, or a literal value containing the word -- doesn't get
    mistaken for a real WHERE clause.
    """
    for maql in expected_maqls:
        outside_protected = _HINT_PROTECTED_RE.sub(" ", maql)
        if re.search(r"\bWHERE\b", outside_protected, re.IGNORECASE):
            return ""
    return (
        " This metric needs no filter. If the assistant asks about excluding or filtering "
        "anything, say no filter is needed."
    )


def generate_simulated_response(agent_message: str, expected_outputs: list[dict], original_question: str) -> str:
    """Generate a user reply to keep the metric-skill conversation going (gpt-4o-mini).

    ``expected_outputs`` is the fixture's full candidate list (as accepted by
    ``_best_maql_match``), not just the first one -- the ground-truth MAQL woven into the
    prompt still comes from candidate 0, but the no-filter hint checks all of them (see
    ``_no_where_clause_hint``).

    Raises:
        SimulatedResponseError: openai is not installed, OPENAI_API_KEY is unset, or the
            provider call failed.
    """
    try:
        from openai import OpenAI, OpenAIError  # noqa: PLC0415
    except ImportError as exc:
        raise SimulatedResponseError("openai package is required for generate_simulated_response") from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SimulatedResponseError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)
    expected_maql = expected_outputs[0].get("maql", "") if expected_outputs else ""
    expected_maqls = [eo.get("maql", "") for eo in expected_outputs]
    prompt = (
        f"You are simulating a user in a conversation with a BI assistant that creates metrics. "
        f"The user's original request was: '{original_question}'. "
        f"The assistant said: '{agent_message}'. "
        f"The user's ground-truth intended metric is exactly this MAQL: {expected_maql}. "
        f"Reply as the user. If the assistant is asking a clarifying question rather than proposing "
        f"a metric, answer that question directly using the ground-truth MAQL -- quote field/label "
        f"identifiers verbatim -- instead of merely agreeing. "
        f"If the assistant's proposal already satisfies the ORIGINAL REQUEST above, agree and confirm "
        f"-- do not introduce new requirements the original request never mentioned. "
        f"Only if the assistant's proposal is missing something the original request actually implies "
        f"(e.g. a filter/clause from the ground-truth MAQL that is a reasonable reading of the original "
        f"request), point it out and add it yourself, quoting field/label identifiers verbatim from the "
        f"ground-truth MAQL."
        f"{_no_where_clause_hint(expected_maqls)}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0,
        )
    except OpenAIError as exc:
        raise SimulatedResponseError(f"simulated user reply failed: {exc}") from exc
    return response.choices[0].message.content or "Please proceed."


@dataclass
class MetricRunResult:
    """Outcome of one K-run conversation for metric creation."""

    conversation_id: str
    metric_result: dict | None
    metric_created: bool
    actual_maql: str
    maql_correct: bool
    total_turns: int
    total_steps: int = 0
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    # Why the simulated-user loop stopped. metric_created=False alone cannot separate a run
    # that ran out of turns, one where the agent went silent, and one where the harness's
    # own simulated user failed -- see LoopExit.
    exit_reason: LoopExit = LoopExit.BUDGET_EXHAUSTED
    turns_used: int = 0
    timings: PhaseTimings = field(default_factory=PhaseTimings)
    # This run's own wall time, from just before its first chat call to the end of its scoring.
    run_latency_s: float = 0.0
    # The gating checks of an options-shape item, by score name; empty for the original shape.
    checks: dict[str, bool] = field(default_factory=dict)
    diagnostics: dict[str, bool] = field(default_factory=dict)
    # Why each failed check failed, by score name.
    check_details: dict[str, Any] = field(default_factory=dict)
    # Set when the harness could not score a check (workspace unreadable, judge failed, snapshot or restore failed):
    # the run never passes, and it is labelled ERROR unless a graded check already failed it.
    harness_error: str | None = None
    # The checks the harness could not read; every other check was graded on what the agent did.
    unscored: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Every gating check passed and the harness scored the run fully.

        The original shape gates on the created metric and its MAQL. A harness error (a check the harness could not
        read, a restore that failed) makes the run unscored: it never passes, and its checks stay for diagnosis.
        An options-shape run whose chat failed does not pass either: the loop sends a turn only while the item
        still needs one (a scripted reply, a missing metric), so checks that held on the cut-off conversation prove
        nothing. Its label is the FAIL of that exit.
        """
        if self.harness_error:
            return False
        if self.checks:
            return self.exit_reason not in CHAT_FAILURE_EXITS and all(self.checks.values())
        return self.metric_created and self.maql_correct


@dataclass
class AgenticMetricSummary:
    """Aggregated outcome of K runs for metric creation."""

    run_results: list[MetricRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: MetricRunResult


def _extract_metric_result(tool_call_events: list[ToolCallEvent]) -> dict | None:
    """Result payload of the create_metric tool call.

    Prefers the most recent successful call in this turn -- when the agent retries
    after a validation error, the earlier failed attempt must not shadow it. Shared
    with ``conversation.py``, which imports this instead of keeping its own copy.
    """
    writes = _successful_writes(tool_call_events)
    return writes[-1] if writes else None


def _extract_created_metric_ids(tool_call_events: list[ToolCallEvent]) -> list[str]:
    """Ids of every metric created by ``create_metric`` calls (a turn may create more than one).

    Used for cleanup so no created metric leaks — unlike ``_extract_metric_result``, which
    returns only the first result for MAQL evaluation. ``create_metric`` is an upsert: a result
    with ``created_new: false`` replaced a metric that existed before, so it is not listed.
    """
    metric_ids: list[str] = []
    for tc in tool_call_events:
        if tc.function_name != "create_metric" or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            # A result that is not an object names no metric; it must not stop the ids of the other calls.
            continue
        data = result_data.get("data", result_data)
        if not isinstance(data, dict) or data.get("created_new") is False:
            continue
        metric_id = data.get("metric_id")
        if metric_id and metric_id not in metric_ids:
            metric_ids.append(metric_id)
    return metric_ids


def _successful_writes(tool_call_events: list[ToolCallEvent]) -> list[dict]:
    """The payload of every successful ``create_metric`` call, in call order; updates included."""
    out: list[dict] = []
    for tc in tool_call_events:
        if tc.function_name != "create_metric" or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        payload = result_data.get("data", result_data)
        if isinstance(payload, dict) and payload and not payload.get("isError"):
            out.append(payload)
    return out


class MetricMatchUndecided(RuntimeError):
    """The assignment search ran out of steps before it could tell whether every expected metric was written."""


# Steps of the assignment search. A real item ends in a few dozen; only many written metrics sharing one formula
# come near, and their factorial count of assignments must not stall the item.
_MATCH_SEARCH_STEPS = 10_000


def _match_expected_metrics(expected: tuple[tuple[str, ...], ...], writes: list[dict]) -> list[str | None]:
    """For each expected metric in order, the id of a written metric whose MAQL matches it, or None.

    Each id is judged by its latest write, since a rewrite replaces the earlier formula, and each id fills one
    entry. Every assignment is tried, so a candidate that two entries both accept cannot starve the other; the
    first complete assignment wins, else the one that matches the most entries.

    Raises:
        MetricMatchUndecided: The search used ``_MATCH_SEARCH_STEPS`` steps without a complete assignment, so
            whether one exists is unknown.
    """
    latest: dict[str, str] = {}
    for write in writes:
        if write.get("metric_id"):
            latest[write["metric_id"]] = normalize_maql(write.get("maql") or "")
    best: list[str | None] = [None] * len(expected)
    steps = 0

    def _search(assigned: list[str | None]) -> bool:
        nonlocal best, steps
        steps += 1
        if steps > _MATCH_SEARCH_STEPS:
            raise MetricMatchUndecided(
                f"no verdict after {_MATCH_SEARCH_STEPS} assignments of {len(latest)} written metrics "
                f"to {len(expected)} expected ones"
            )
        if len(assigned) == len(expected):
            if sum(a is not None for a in assigned) > sum(b is not None for b in best):
                best = list(assigned)
            return None not in assigned
        candidates = expected[len(assigned)]
        for metric_id, maql in latest.items():
            matches = metric_id not in assigned and any(
                maql == normalize_maql(substitute_placeholders(c, assigned)) for c in candidates
            )
            if matches and _search([*assigned, metric_id]):
                return True
        return _search([*assigned, None])

    _search([])
    return best


def _delete_metric(sdk: GoodDataSdk, workspace_id: str, metric_id: str) -> None:
    """Delete a metric created during evaluation.

    Eval runs share a persistent workspace, so a metric left behind is picked up by
    a later test — the agent reuses it (returning ``SELECT {id}`` instead of full
    MAQL) and the assertion fails. Deleting the created metric on the way out keeps
    the workspace clean for the next run. Best-effort: failures are logged, not raised.
    Mirrors ``alert_skill._delete_alert``.

    A delete does not stay done on its own. ``create_metric`` reads the whole analytics
    model and writes it back, so a concurrent test whose read preceded this delete
    restores the metric when its write lands. The metric is therefore checked again after
    each of ``_DELETE_RECHECK_DELAYS_S`` and deleted again while it is still there.
    """
    if not _try_delete_metric(sdk, workspace_id, metric_id):
        return
    for delay in _DELETE_RECHECK_DELAYS_S:
        time.sleep(delay)
        if not _metric_exists(sdk, workspace_id, metric_id):
            return
        print(f"[CLEANUP] Metric {metric_id} is back or could not be checked; deleting again")
        if not _try_delete_metric(sdk, workspace_id, metric_id):
            return
    if _DELETE_RECHECK_DELAYS_S:
        # Every check found it back, so the last delete is unverified: say so rather than
        # report a clean workspace. The post-run reset is what removes it for good.
        print(
            f"[CLEANUP] Metric {metric_id} was back or unchecked at all {len(_DELETE_RECHECK_DELAYS_S)} checks; "
            "the last delete is not verified and the metric may remain"
        )


def _try_delete_metric(sdk: GoodDataSdk, workspace_id: str, metric_id: str) -> bool:
    """Delete the metric; True when it is gone afterwards, a 404 included."""
    try:
        sdk._client.entities_api.delete_entity_metrics(workspace_id, metric_id)
    except NotFoundException:
        return True
    except Exception as exc:
        print(f"[CLEANUP] Failed to delete metric {metric_id}: {exc}")
        return False
    return True


def _metric_exists(sdk: GoodDataSdk, workspace_id: str, metric_id: str) -> bool:
    """Whether the metric may still be in the workspace. Only a 404 reads as absent; any other
    lookup failure reads as present, so the caller deletes again rather than leave a restored
    metric behind. The recheck delays bound how often that happens."""
    try:
        sdk._client.entities_api.get_entity_metrics(workspace_id, metric_id)
    except NotFoundException:
        return False
    except Exception as exc:
        print(f"[CLEANUP] Could not check metric {metric_id}: {exc}")
    return True


def _stop_after_write(spec: MetricExpectation, replies_left: int, writes: list[dict]) -> bool:
    """Whether a turn that wrote a metric ends the run.

    The original shape stops at the first metric, as before. An item that scripts further replies after a write
    (``run_all_replies``), or expects several metrics, keeps going while replies are left and metrics are missing.
    """
    if spec.legacy or spec.expect_no_create:
        return True
    if spec.run_all_replies and replies_left:
        return False
    if spec.expected_metrics:
        try:
            return None not in _match_expected_metrics(spec.expected_metrics, writes) or replies_left == 0
        except MetricMatchUndecided:
            return True  # No later turn can make the match decidable; the score reports it.
    return True


def _judge_rubric(judge: LLMJudge, rubric: str, transcript: list[tuple[str, str]]) -> JudgeVerdict:
    """Grade the whole conversation, user and assistant turns in order, against the rubric."""
    conversation = "\n\n".join(f"{role}: {text}" for role, text in transcript)
    first_user = next((text for role, text in transcript if role == "User"), "")
    return score_run(judge, input=first_user, expected_output=rubric, actual_output=conversation)


def _score_options_run(
    spec: MetricExpectation,
    workspace: MetricWorkspace,
    *,
    conversation_id: str,
    transcript: list[tuple[str, str]],
    texts: list[str],
    first_turn: ChatResult | None,
    first_write_call_turn: int | None,
    writes: list[dict],
    metric_result: dict | None,
    before: dict[str, dict],
    judge: LLMJudge | None,
    answered: bool = True,
) -> tuple[dict[str, bool], dict[str, bool], dict[str, Any], str | None, list[str]]:
    """The gating checks, diagnostics, failure reasons, harness error and unscored check names of one run.

    A check the harness could not evaluate (the workspace or the conversation was unreadable, the judge gave no
    verdict) reads False, is named unscored and sets the harness error; the other checks are still evaluated.
    """
    checks: dict[str, bool] = {}
    diagnostics: dict[str, bool] = {}
    details: dict[str, Any] = {}
    harness_errors: list[str] = []
    unscored: list[str] = []

    def _check(name: str, ok: bool, why: Any = None) -> None:
        checks[name] = ok
        if not ok and why:
            details[name] = why

    def _harness(name: str, reason: str) -> None:
        _check(name, False, f"harness: {reason}")
        harness_errors.append(f"{name}: {reason}")
        unscored.append(name)

    def _read(name: str, check: Callable[[], None]) -> None:
        """Run one check that reads the workspace: a read failure leaves that check unscored, and only it."""
        try:
            check()
        except WorkspaceReadError as exc:
            _harness(name, str(exc))

    target_id = (metric_result or {}).get("metric_id")
    if spec.candidates:
        actual = (metric_result or {}).get("maql", "")
        _check("metric_created", metric_result is not None)
        _check(
            "maql_correct",
            metric_result is not None and _best_maql_match(actual, spec.candidates)[0],
            {"expected": [c["maql"] for c in spec.candidates], "actual": actual},
        )
    if spec.expect_no_create:
        # A run whose chat failed before any complete answer proves no refusal.
        _check(
            "metric_not_created",
            answered and not writes,
            {"written": [w.get("metric_id") for w in writes]} if answered else "the agent never completed an answer",
        )
        if spec.expected_mentions:
            missing = missing_mentions(spec.expected_mentions, texts)
            _check("metric_reuse_named", not missing, {"missing": missing})
    if spec.expect_no_overwrite:
        # A metric is overwritten only when it existed before the run; editing one the run created is not.
        overwritten = list(dict.fromkeys(w.get("metric_id") for w in writes if w.get("metric_id") in before))
        _check("metric_no_overwrite", not overwritten, {"overwritten": overwritten})
    if spec.expect_clarification:
        asked = (
            first_turn is not None
            and read_first_reply(first_turn, asked_in_text=asks_in_text(first_turn, texts[0] if texts else "")).asked
        )
        _check(
            "metric_clarified",
            asked and first_write_call_turn != 1,
            {"asked": asked, "write_turn": first_write_call_turn},
        )
    if spec.confirmation_turn is not None:
        ok = first_write_call_turn is None or first_write_call_turn >= spec.confirmation_turn
        _check(
            "metric_confirmed_first",
            ok,
            {"first_create_metric_turn": first_write_call_turn, "allowed_from": spec.confirmation_turn},
        )
    if spec.rubric and judge is not None:
        try:
            verdict = _judge_rubric(judge, spec.rubric, transcript)
        except _judge_provider_errors() as exc:
            verdict = JudgeVerdict(passed=False, reasoning="", error=f"{type(exc).__name__}: {exc}")
        if verdict.error is not None:
            _harness("metric_rubric", f"judge gave no verdict: {verdict.error}")
        else:
            _check("metric_rubric", verdict.passed, verdict.reasoning)
    if spec.expected_fields is not None:
        fields = spec.expected_fields

        def _fields() -> None:
            # The metric the agent wrote, never the id the item names: a pre-existing metric of that id could pass.
            if target_id is None:
                _check("metric_fields_correct", False, "no metric was written")
            else:
                mismatches = field_mismatches(fields, target_id, workspace.get_metric(target_id))
                _check("metric_fields_correct", not mismatches, mismatches)

        _read("metric_fields_correct", _fields)
    if spec.expected_update is not None:
        update = spec.expected_update

        def _update() -> None:
            mismatches = update_mismatches(update, before.get(update.metric_id), workspace.get_metric(update.metric_id))
            _check("metric_updated", not mismatches, mismatches)

        _read("metric_updated", _update)
    if spec.expect_no_deletion:

        def _no_deletion() -> None:
            gone = [m for m in spec.expect_no_deletion if workspace.get_metric(m) is None]
            _check("metric_none_deleted", not gone, {"missing": gone})

        _read("metric_none_deleted", _no_deletion)
    if spec.expect_executes:

        def _executes() -> None:
            reason = workspace.execute_metric(target_id) if target_id else "no metric was written"
            _check("metric_executes", reason is None, reason)

        _read("metric_executes", _executes)
    if spec.expect_suggestions:

        def _suggestions() -> None:
            # QA accepts a turn without suggestions; when there are some, the first must name the new metric.
            suggestions = last_suggestions(workspace.conversation_items(conversation_id))
            actions = (suggestions or {}).get("actions")
            if actions is None:
                actions = []  # Only an absent list means no actions; any other value is checked below.
            if not isinstance(actions, list) or not all(isinstance(a, dict) for a in actions):
                raise WorkspaceReadError(f"conversation {conversation_id}: unreadable suggestion actions {actions!r}")
            if not actions or target_id is None:
                _check("metric_suggestions", True)
            else:
                first = f"{actions[0].get('query', '')} {actions[0].get('label', '')}".casefold()
                title = str((metric_result or {}).get("title") or "").casefold()
                named = (bool(title) and title in first) or f"{{metric/{target_id}}}".casefold() in first
                _check("metric_suggestions", named, {"first_action": actions[0], "metric": target_id})

        _read("metric_suggestions", _suggestions)
    if spec.expected_metrics:
        try:
            matched = _match_expected_metrics(spec.expected_metrics, writes)
        except MetricMatchUndecided as exc:
            _harness("metric_all_created", str(exc))
        else:
            _check(
                "metric_all_created",
                None not in matched,
                {"matched": matched, "written": [(w.get("metric_id"), w.get("maql")) for w in writes]},
            )
    if spec.score_first_proposal:
        # An agent that wrote without showing a formula first proposed the MAQL of its first write, not its last.
        proposed = first_proposed_maql(texts) or (writes[0].get("maql") if writes else None)
        diagnostics["metric_first_proposal_correct"] = (
            bool(proposed) and _best_maql_match(proposed or "", spec.candidates)[0]
        )
        if not diagnostics["metric_first_proposal_correct"]:
            details["metric_first_proposal_correct"] = {"proposed": proposed}
    return checks, diagnostics, details, ("; ".join(harness_errors) or None), unscored


def _restore_workspace(
    workspace: MetricWorkspace, before: dict[str, dict], writes: list[dict], guarded: tuple[str, ...]
) -> list[str]:
    """Put back every pre-existing metric the run wrote over, and every guarded metric it removed.

    Returns the ids it could not put back. Guarded metrics go first: one the run wrote over and then removed is
    recreated with its original attributes, so the overwrite restore, which updates a metric that exists, skips it.
    """
    failed: list[str] = []
    recreated: set[str] = set()
    for metric_id in guarded:
        if metric_id not in before:
            continue
        try:
            gone = workspace.get_metric(metric_id) is None
        except WorkspaceReadError as exc:
            print(f"[CLEANUP] Could not check metric {metric_id}: {exc}")
            failed.append(metric_id)
            continue
        if not gone:
            continue
        if workspace.restore_metric(metric_id, before[metric_id], exists=False):
            recreated.add(metric_id)
        else:
            failed.append(metric_id)
    failed.extend(
        metric_id
        for metric_id in dict.fromkeys(w.get("metric_id") for w in writes)
        if metric_id in before
        and metric_id not in recreated
        and not workspace.restore_metric(metric_id, before[metric_id], exists=True)
    )
    return list(dict.fromkeys(failed))


def _execute_single_metric_run(
    client: ChatClient,
    sdk: GoodDataSdk,
    workspace_id: str,
    conversation_id: str,
    question: str,
    expected_outputs: list[dict],
    max_iterations: int,
    *,
    spec: MetricExpectation | None = None,
    workspace: MetricWorkspace | None = None,
    judge: LLMJudge | None = None,
) -> MetricRunResult:
    """Drive one full multi-turn metric-skill conversation and evaluate the result.

    Any metric the agent creates during this run is deleted on the way out (see
    ``_delete_metric``) so it cannot leak into — and be reused by — a later test
    sharing the workspace. An options-shape item also gets back every metric the run
    wrote over, from a snapshot taken before its first turn; without that snapshot the
    agent is not driven at all, since nothing it overwrote could be put back.
    """
    spec = spec or MetricExpectation(candidates=expected_outputs)
    before: dict[str, dict] = {}
    if workspace is not None:
        try:
            if workspace.unrestored:
                # A snapshot now would record an earlier run's leftover as the original.
                raise WorkspaceReadError(f"an earlier run could not put back {workspace.unrestored}")
            before = workspace.list_metrics()
        except WorkspaceReadError as exc:
            print(f"[SNAPSHOT] Could not read the workspace metrics before the run: {exc}")
            return MetricRunResult(
                conversation_id=conversation_id,
                metric_result=None,
                metric_created=False,
                actual_maql="",
                maql_correct=False,
                total_turns=0,
                exit_reason=LoopExit.NOT_RUN,
                checks={"metric_scored": False},
                check_details={"metric_scored": f"harness: snapshot: {exc}"},
                harness_error=f"snapshot: {exc}",
                unscored=["metric_scored"],
            )
    metric_result: dict | None = None
    created_metric_ids: list[str] = []
    turns = 0
    steps = 0
    current_question = question
    reasoning_steps: list[str] = []
    response_id: str | None = None
    all_tool_call_events: list[ToolCallEvent] = []
    all_reasoning_step_events: list[ReasoningStepEvent] = []
    timings = PhaseTimings()
    turn_offset = 0.0  # each turn's call_ts/ts restarts near 0 -- shift by prior turns' wall time
    tool_index_offset = 0
    reasoning_index_offset = 0
    replies = list(spec.user_replies)
    transcript: list[tuple[str, str]] = [("User", question)]
    texts: list[str] = []
    first_turn: ChatResult | None = None
    first_write_call_turn: int | None = None
    writes: list[dict] = []
    answered_turns = 0
    result: MetricRunResult | None = None

    def _record_turn(result: ChatResult, events: list[ToolCallEvent]) -> str:
        """Note the turn's writes and text for the options-shape checks; returns the rendered text."""
        nonlocal first_turn, first_write_call_turn
        writes.extend(_successful_writes(events))
        if first_write_call_turn is None and any(tc.function_name == "create_metric" for tc in events):
            first_write_call_turn = turns
        if first_turn is None:
            first_turn = result
        text = render_answer_text(result)
        texts.append(text)
        transcript.append(("Assistant", text))
        return text

    try:
        # Defaults to BUDGET_EXHAUSTED: every other exit assigns explicitly, so a loop that
        # simply runs out of range() is labelled correctly with no trailing else.
        exit_reason = LoopExit.BUDGET_EXHAUSTED
        run_started = time.monotonic()
        for _iteration in range(max_iterations):
            turns += 1
            agent_started = time.monotonic()
            try:
                chat_result = client.send_message(conversation_id, current_question)
            except ChatError as exc:
                # Without this the exception escapes run_agentic_metric_skill entirely,
                # discarding every K-run already completed along with any exit_reason. A
                # GoodData-side fault, so recorded like the simulated-user one below.
                timings.agent_s += time.monotonic() - agent_started
                print(f"[CHAT] send_message failed for conversation {conversation_id}: {exc}")
                # The stream can break AFTER create_metric already succeeded server-side.
                # Those ids only ever reached created_metric_ids from the normal path below,
                # so breaking here left the metric in the workspace for the `finally` cleanup
                # to miss -- a real object leaking out of a failed run, not a reporting gap.
                partial = exc.partial_result
                if partial is not None:
                    reasoning_steps.extend(partial.reasoning_steps or [])
                    response_id = partial.response_id or response_id
                    for metric_id in _extract_created_metric_ids(partial.tool_call_events or []):
                        if metric_id not in created_metric_ids:
                            created_metric_ids.append(metric_id)
                    _record_turn(partial, partial.tool_call_events or [])
                exit_reason = chat_failure_exit(exc)
                break
            agent_elapsed = time.monotonic() - agent_started
            timings.agent_s += agent_elapsed
            reasoning_steps.extend(chat_result.reasoning_steps or [])
            response_id = chat_result.response_id or response_id
            turn_offset, tool_index_offset, reasoning_index_offset = shift_and_index_events(
                chat_result,
                turn_offset=turn_offset,
                tool_index_offset=tool_index_offset,
                reasoning_index_offset=reasoning_index_offset,
            )
            turn_events = chat_result.tool_call_events or []
            all_tool_call_events.extend(turn_events)
            all_reasoning_step_events.extend(chat_result.reasoning_step_events or [])
            steps += chat_result.reasoning_step_count
            for metric_id in _extract_created_metric_ids(turn_events):
                if metric_id not in created_metric_ids:
                    created_metric_ids.append(metric_id)
            response_text = _record_turn(chat_result, turn_events)
            if response_text.strip():
                # Only a turn with text is an answer: a silent one proves no refusal.
                answered_turns += 1
            candidate = _extract_metric_result(turn_events)
            if candidate is not None:
                metric_result = candidate
                if _stop_after_write(spec, len(replies), writes):
                    log_timer(
                        f"[timer] metric_skill {conversation_id} GoodData turn {turns} complete after "
                        f"{agent_elapsed:.2f}s; metric result received"
                    )
                    exit_reason = LoopExit.SUCCESS
                    break
            if not response_text and not turn_events:
                exit_reason = LoopExit.AGENT_SILENT
                break
            if _iteration >= max_iterations - 1:
                break
            if replies:
                current_question = replies.pop(0)
                transcript.append(("User", current_question))
                continue
            if not spec.legacy and (
                not spec.candidates or spec.expect_no_create or spec.run_all_replies or spec.expected_metrics
            ):
                # The scripted replies are spent and the item hands the rest to no one: it has no MAQL for the
                # simulated user, or it scripts the whole conversation (run_all_replies, several metrics).
                exit_reason = LoopExit.STOPPED_EARLY
                break
            log_timer(
                f"[timer] metric_skill {conversation_id} GoodData turn {turns} complete after "
                f"{agent_elapsed:.2f}s; waiting for gpt-4o-mini simulated user"
            )
            simulated_started = time.monotonic()
            try:
                current_question = generate_simulated_response(response_text, spec.candidates, question)
            except SimulatedResponseError as exc:
                simulated_elapsed = time.monotonic() - simulated_started
                timings.simulated_user_s += simulated_elapsed
                print(f"[SIM-USER] Simulated reply failed for conversation {conversation_id}: {exc}")
                log_timer(
                    f"[timer] metric_skill {conversation_id} gpt-4o-mini simulated user failed after "
                    f"{simulated_elapsed:.2f}s"
                )
                # A harness-side fault, not an agent one. Recorded so reporting can treat it
                # as an error instead of scoring the agent down for it.
                exit_reason = LoopExit.SIMULATED_USER_FAILED
                break
            simulated_elapsed = time.monotonic() - simulated_started
            timings.simulated_user_s += simulated_elapsed
            transcript.append(("User", current_question))
            log_timer(
                f"[timer] metric_skill {conversation_id} gpt-4o-mini simulated user complete after "
                f"{simulated_elapsed:.2f}s"
            )

        actual_maql = (metric_result or {}).get("maql", "")
        metric_created = metric_result is not None
        maql_correct, _ = _best_maql_match(actual_maql, spec.candidates) if metric_created else (False, "")
        checks: dict[str, bool] = {}
        diagnostics: dict[str, bool] = {}
        check_details: dict[str, Any] = {}
        harness_error: str | None = None
        unscored: list[str] = []
        if workspace is not None:
            checks, diagnostics, check_details, harness_error, unscored = _score_options_run(
                spec,
                workspace,
                conversation_id=conversation_id,
                transcript=transcript,
                texts=texts,
                first_turn=first_turn,
                first_write_call_turn=first_write_call_turn,
                writes=writes,
                metric_result=metric_result,
                before=before,
                judge=judge,
                answered=answered_turns > 0,
            )
        result = MetricRunResult(
            conversation_id=conversation_id,
            metric_result=metric_result,
            metric_created=metric_created,
            actual_maql=actual_maql,
            maql_correct=maql_correct,
            total_turns=turns,
            total_steps=steps,
            reasoning_steps=reasoning_steps,
            response_id=response_id,
            tool_call_events=all_tool_call_events,
            reasoning_step_events=all_reasoning_step_events,
            timings=timings,
            exit_reason=exit_reason,
            turns_used=turns,
            run_latency_s=time.monotonic() - run_started,
            checks=checks,
            diagnostics=diagnostics,
            check_details=check_details,
            harness_error=harness_error,
            unscored=unscored,
        )
        return result
    finally:
        for metric_id in created_metric_ids:
            _delete_metric(sdk, workspace_id, metric_id)
        if workspace is not None:
            unrestored = _restore_workspace(workspace, before, writes, spec.expect_no_deletion)
            if unrestored:
                # Later runs of the item are skipped rather than scored against a changed workspace.
                workspace.unrestored.extend(unrestored)
                if result is not None:
                    # Unscored like a check the harness could not read: metric_scored reads False with the reason.
                    note = f"restore failed for {unrestored}"
                    result.harness_error = f"{result.harness_error}; {note}" if result.harness_error else note
                    result.checks["metric_scored"] = False
                    result.unscored.append("metric_scored")
                    prior = result.check_details.get("metric_scored")
                    result.check_details["metric_scored"] = f"{prior}; harness: {note}" if prior else f"harness: {note}"


def run_agentic_metric_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict | list,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    user_context: dict | None = None,
) -> AgenticMetricSummary:
    """Run the metric-skill agentic evaluation K times and return a summary.

    ``expected_output`` is a single candidate dict, a list of candidate dicts, or the options shape of
    ``_metric_expectation``. With candidates, a run passes when the actual MAQL matches any of them
    after normalisation; the options shape adds the checks it names.

    Raises:
        ValueError: The options shape is malformed. Raised before any request.
        ImportError, OSError: The item has a rubric and the LLM judge cannot be built (the llm-judge extra
            or OPENAI_API_KEY is missing). Raised before any request.
    """
    spec = parse_expectation(expected_output)
    expected_outputs = spec.candidates
    # Built before the first request, as general_question does: a missing judge is a setup error to
    # report at once, not something to find after every run's conversation.
    judge = LLMJudge(_RUBRIC_STEPS) if spec.rubric else None
    run_results: list[MetricRunResult] = []
    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=user_context,
    )
    sdk = GoodDataSdk.create(host, token)
    workspace = MetricWorkspace(host, token, workspace_id, sdk) if spec.needs_workspace else None

    def _run(conversation_id: str) -> MetricRunResult:
        return _execute_single_metric_run(
            client,
            sdk,
            workspace_id,
            conversation_id,
            question,
            expected_outputs,
            max_iterations,
            spec=spec,
            workspace=workspace,
            judge=judge,
        )

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(_run(conv_id_0))
        finally:
            if initial_conversation_id is None:  # only delete conversations we created
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(_run(conv_id))
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()
        if workspace is not None:
            workspace.close()

    pass_at_k = any(r.passed for r in run_results)
    pass_power_k = all(r.passed for r in run_results)
    # A graded run describes the item better than an unscored one, whatever their check counts.
    best = max(
        run_results,
        key=lambda r: (r.passed, r.harness_error is None, sum(r.checks.values()), r.maql_correct, r.metric_created),
    )
    return AgenticMetricSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class MetricSkillAssertionError(AgenticAssertionError):
    """Raised when a metric-skill evaluation fails."""


def _harness_error_of(run: MetricRunResult) -> str | None:
    """The harness error, for the run's label, only when it is what left the run without a verdict.

    A run that failed a check the harness did grade, or whose chat failed on a turn it still needed, is a FAIL
    whatever the unscored checks would have said (see ``classify_run``).
    """
    if not run.harness_error or run.exit_reason in CHAT_FAILURE_EXITS:
        return None
    graded = [ok for name, ok in run.checks.items() if name not in run.unscored]
    return run.harness_error if all(graded) else None


def _quality_checks(run: MetricRunResult) -> dict[str, bool]:
    """The checks a run's quality score counts.

    An unscored run (``harness_error``) counts as ``metric_scored`` False alone: its other checks are observations
    the harness could not complete, and an ERROR run must not report the quality of a graded one.
    """
    if run.harness_error:
        return {"metric_scored": False}
    return run.checks or {"metric_created": run.metric_created, "maql_correct": run.maql_correct}


def _verdict_fields(run: MetricRunResult) -> dict[str, Any]:
    """A run's checks as top-level booleans of its detail, which the report's quality score counts.

    The original shape keeps ``metric_created`` and ``maql_correct``. An options-shape item puts its own checks there
    instead, so an item without candidates is not scored on a MAQL it never asked for; the failure reasons and the
    diagnostics sit beside them as dicts, which the quality score does not count. An unscored run keeps its checks
    for diagnosis under ``unscored_checks``, also a dict (see ``_quality_checks``).
    """
    if not run.checks:
        return _quality_checks(run)
    return {
        **_quality_checks(run),
        **({"unscored_checks": run.checks} if run.harness_error else {}),
        "check_details": run.check_details,
        **({"diagnostics": run.diagnostics} if run.diagnostics else {}),
        **({"harness_error": run.harness_error} if run.harness_error else {}),
    }


def evaluate_agentic_metric_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict | list,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "metric_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    user_context: dict | None = None,
    gate: EvalGate = DEFAULT_GATE,
) -> AgenticEvalOutcome:
    """Run metric-skill evaluation, log to Langfuse, and raise MetricSkillAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as
    ``.reasoning_steps``/``.conversation_id``/``.response_id`` (mirrors the
    `conversation_id`-on-exception idiom in `ChatClient.ask()`) so callers can retrieve them
    either way.
    """
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
    langfuse, window_start, scope = open_item_trace(langfuse, identity, dataset_item_id, suffix_runs=k > 1)
    with item_scope(scope):
        summary = run_agentic_metric_skill(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=question,
            expected_output=expected_output,
            k=k,
            max_iterations=max_iterations,
            initial_conversation_id=initial_conversation_id,
            reasoning_effort=reasoning_effort,
            agent_id=agent_id,
            user_context=user_context,
        )

    # Before the Langfuse scores, so an ERROR run gets its marker beside its usual scores.
    run_labels = label_runs(summary.run_results, passed=lambda r: r.passed, judge_error=_harness_error_of)

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)

            for run_idx, run in enumerate(summary.run_results):
                pt = ctx.trace(run.conversation_id)
                strict = run.checks or {"metric_created": run.metric_created, "maql_correct": run.maql_correct}
                with ctx.observe(
                    pt,
                    run_idx,
                    conversation_id=run.conversation_id,
                    output=strict,
                ) as tid:
                    if (run_error := run_labels.error_label(run_idx)) is not None:
                        log_eval_error_score(ctx, tid, run_error)
                    for name, ok in {**strict, **run.diagnostics}.items():
                        ctx.score(tid, name=name, value=float(ok), data_type="BOOLEAN")
                    ctx.score(tid, name="turns", value=run.total_turns, data_type="NUMERIC")
                    ctx.score(tid, name="steps", value=run.total_steps, data_type="NUMERIC")
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)
                    ctx.quality(
                        tid,
                        strict_checks=_quality_checks(run),
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        # Before the pass@K raise: a failing item's scores are the ones worth having.
        submit_trace_scoring(
            submit_trace_link,
            identity,
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=[r.conversation_id for r in summary.run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=k > 1,
            write_scores=_write_scores,
            scope=scope,
            item_input=question,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])

    runs_passed = sum(1 for r in summary.run_results if r.passed)
    runs_effective = len(summary.run_results)
    run_latencies_s = [r.run_latency_s for r in summary.run_results]

    best = summary.best
    expected_outputs_list: list[dict] = parse_expectation(expected_output).candidates

    def _run_detail(run: MetricRunResult) -> dict:
        """The diagnostic fields for ONE run, shared by the best run and every failing one.

        Extracted so a failing run is described by exactly the same keys as the winning run --
        for this kind that means the MAQL the run actually produced, which is the whole diagnosis.
        """
        return {
            **_verdict_fields(run),
            "expected_maql_candidates": [c.get("maql", "") for c in expected_outputs_list],
            "actual_maql": run.actual_maql,
            # Why the loop stopped. metric_created=False alone cannot tell a refusal from a
            # run that hit max_iterations while still on track -- see LoopExit.
            "exit_reason": run.exit_reason.value,
            "turns_used": run.turns_used,
            **timeline_detail(run.tool_call_events, run.reasoning_step_events),
        }

    def _failed_checks(run: MetricRunResult) -> list[dict]:
        """The checks this run failed; the MAQL pair is the whole diagnosis for this kind.

        With no metric, ``maql_correct`` reads False only because there is no MAQL to compare,
        so ``metric_created`` alone is named.
        """
        checks: list[FailedCheck] = []
        if run.checks:
            for name, ok in run.checks.items():
                if not ok and not (name == "maql_correct" and not run.metric_created):
                    checks.append(FailedCheck(name, expected=True, actual=run.check_details.get(name, False)))
            return failed_check_records(checks)
        if not run.metric_created:
            checks.append(FailedCheck("metric_created", expected=True, actual=False))
        elif not run.maql_correct:
            checks.append(
                FailedCheck(
                    "maql_correct",
                    expected=[c.get("maql", "") for c in expected_outputs_list],
                    actual=run.actual_maql,
                )
            )
        return failed_check_records(checks)

    detail = agentic_detail(
        best.tool_call_events,
        best.reasoning_step_events,
        **_verdict_fields(best),
        expected_maql_candidates=[c.get("maql", "") for c in expected_outputs_list],
        actual_maql=best.actual_maql,
        # Why the loop stopped. metric_created=False alone cannot tell a refusal from a run
        # that hit max_iterations while still on track -- see LoopExit.
        exit_reason=best.exit_reason.value,
        turns_used=best.turns_used,
        max_iterations=max_iterations,
    )
    # Same predicate runs_passed is taken over, so an item's failed_runs and its counts
    # cannot disagree about which runs failed.
    failed_runs = build_failed_runs(
        summary.run_results,
        labels=run_labels,
        detail=_run_detail,
        failed_checks=_failed_checks,
    )

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        gate_note = failure_message_head(gate, run_labels, runs_passed, failed_runs)
        candidates_str = "; ".join(repr(c.get("maql", "")) for c in expected_outputs_list)
        failing = [name for name, ok in best.checks.items() if not ok]
        checks_str = f" Failed checks: {', '.join(failing)}; details: {best.check_details}." if failing else ""
        raise_agentic_failure(
            MetricSkillAssertionError,
            f"Metric skill assertion failed. {gate_note} "
            f"metric_created={best.metric_created}, maql_correct={best.maql_correct}. "
            f"Expected MAQL (candidates): {candidates_str}. "
            f"Actual MAQL: {best.actual_maql}.{checks_str}",
            harness_error=run_labels.harness_error_record,
            shadow=run_labels.shadow(gate),
            reasoning_steps=best.reasoning_steps,
            conversation_id=best.conversation_id,
            response_id=best.response_id,
            detail=detail,
            runs_passed=runs_passed,
            runs_effective=runs_effective,
            best_run_latency_s=run_latency_s(best.timings),
            timings=item_timings,
            failed_runs=failed_runs,
            run_latencies_s=run_latencies_s,
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
        best_run_latency_s=run_latency_s(best.timings),
        timings=item_timings,
    )
