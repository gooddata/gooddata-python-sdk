# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic metric-skill evaluation runner."""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass, field
from typing import Any

from gooddata_sdk import GoodDataSdk

from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer, sum_timings

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI: Any = None

_DEFAULT_K = 1
_DEFAULT_MAX_ITERATIONS = 7

_IFNULL_RE = re.compile(r"IFNULL\s*\([^,]+,\s*0\)", re.IGNORECASE)
_SELECT_WRAP_RE = re.compile(r"^\s*\(\s*SELECT\s*\{([^}]+)\}\s*\)\s*$", re.IGNORECASE)
_INNER_SELECT_RE = re.compile(r"\(\s*SELECT\s*\{([^}]+)\}\s*\)", re.IGNORECASE)
# Matches whichever comes first: a {type/id} identifier reference or a quoted string
# literal -- both are case-sensitive data and must survive casefolding untouched.
# Everything else in MAQL (keywords, operators, numbers, punctuation) carries no
# case-sensitive meaning, per the MAQL reference (SELECT/BY/WHERE/FOR PREVIOUS/etc.
# are case-insensitive; only {..} identifiers and quoted literal values are not).
# Feeds _normalize_maql, the scoring comparator (_best_maql_match) -- do not widen this
# to handle \X escapes without confirming MAQL literals actually support backslash
# escaping (unconfirmed; see PR #1760 review). A wrong guess here silently changes
# maql_correct for the whole eval dataset, not just a hint. _no_where_clause_hint()
# below has its own, separately-scoped regex for that reason.
_PROTECTED_RE = re.compile(r"\{[^}]*\}|\"[^\"]*\"|'[^']*'")


def _strip_outer_parens(s: str) -> str:
    """Strip one balanced layer of outer () if they wrap the entire expression."""
    if not (s.startswith("(") and s.endswith(")")):
        return s
    depth = 0
    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and i < len(s) - 1:
                return s  # Closing paren found before end — not a simple outer wrapper
    return s[1:-1].strip()


def _casefold_outside_protected(s: str) -> str:
    """Lowercase MAQL keywords/operators while preserving case-sensitive {type/id}
    identifiers and quoted string literal values (e.g. WHERE {label/x} = "Active")."""
    parts = []
    last = 0
    for m in _PROTECTED_RE.finditer(s):
        parts.append(s[last : m.start()].lower())
        parts.append(m.group(0))
        last = m.end()
    parts.append(s[last:].lower())
    return "".join(parts)


def _normalize_maql(maql: str) -> str:
    """Semantic normalisation: strip whitespace, unwrap IFNULL/SELECT wrappers, casefold keywords."""
    if not maql:
        return ""
    m = maql.strip()
    m = _IFNULL_RE.sub(
        lambda mo: _strip_outer_parens(mo.group(0).split(",")[0].strip()[len("IFNULL(") :].strip()),
        m,
    )
    m = _SELECT_WRAP_RE.sub(r"{\1}", m)
    m = _INNER_SELECT_RE.sub(r"{\1}", m)
    m = re.sub(r"\{\s+", "{", m)
    m = re.sub(r"\s+\}", "}", m)
    m = re.sub(r"\s+", " ", m)
    return _casefold_outside_protected(m.strip())


def _best_maql_match(actual_maql: str, expected_outputs: list[dict]) -> tuple[bool, str]:
    """Try actual MAQL against every candidate; return (matched, best_expected_maql).

    First match wins. First candidate is used for error reporting when none match.
    """
    normalized_actual = _normalize_maql(actual_maql)
    for candidate in expected_outputs:
        expected_maql = candidate.get("maql", "")
        if normalized_actual == _normalize_maql(expected_maql):
            return True, expected_maql
    return False, expected_outputs[0].get("maql", "") if expected_outputs else ""


class SimulatedResponseError(RuntimeError):
    """The simulated user could not reply: openai missing, no API key, or the provider failed.

    Carries every expected setup/provider failure so callers can end the run without
    swallowing programming errors raised from the same call.
    """


# Separate from _PROTECTED_RE on purpose: this one only feeds a same-turn LLM-prompt hint
# (see _no_where_clause_hint), never the scoring comparator, so it can afford to consume
# \X escape sequences inside quoted literals without risking maql_correct semantics.
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
    total_turns: float
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    timings: PhaseTimings = field(default_factory=PhaseTimings)


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
    for tc in reversed(tool_call_events):
        if tc.function_name != "create_metric" or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not isinstance(result_data, dict):
            continue
        payload = result_data.get("data", result_data)
        if not isinstance(payload, dict) or not payload or payload.get("isError"):
            continue
        return payload
    return None


def _extract_created_metric_ids(tool_call_events: list[ToolCallEvent]) -> list[str]:
    """Ids of every metric created by ``create_metric`` calls (a turn may create more than one).

    Used for cleanup so no created metric leaks — unlike ``_extract_metric_result``, which
    returns only the first result for MAQL evaluation. Shared with conversation evaluation.
    """
    metric_ids: list[str] = []
    for tc in tool_call_events:
        if tc.function_name != "create_metric" or not tc.result:
            continue
        result_data = tc.parsed_result()
        if not result_data:
            continue
        data = result_data.get("data", result_data)
        metric_id = data.get("metric_id") if isinstance(data, dict) else None
        if metric_id and metric_id not in metric_ids:
            metric_ids.append(metric_id)
    return metric_ids


def _delete_metric(sdk: GoodDataSdk, workspace_id: str, metric_id: str) -> None:
    """Delete a metric created during evaluation.

    Eval runs share a persistent workspace, so a metric left behind is picked up by
    a later test — the agent reuses it (returning ``SELECT {id}`` instead of full
    MAQL) and the assertion fails. Deleting the created metric on the way out keeps
    the workspace clean for the next run. Best-effort: failures are logged, not raised.
    Mirrors ``alert_skill._delete_alert``.
    """
    try:
        sdk._client.entities_api.delete_entity_metrics(workspace_id, metric_id)
    except Exception as exc:
        print(f"[CLEANUP] Failed to delete metric {metric_id}: {exc}")


def _execute_single_metric_run(
    client: ChatClient,
    sdk: GoodDataSdk,
    workspace_id: str,
    conversation_id: str,
    question: str,
    expected_outputs: list[dict],
    max_iterations: int,
) -> MetricRunResult:
    """Drive one full multi-turn metric-skill conversation and evaluate the result.

    Any metric the agent creates during this run is deleted on the way out (see
    ``_delete_metric``) so it cannot leak into — and be reused by — a later test
    sharing the workspace.
    """
    metric_result: dict | None = None
    created_metric_ids: list[str] = []
    turns = 0
    current_question = question
    reasoning_steps: list[str] = []
    response_id: str | None = None
    all_tool_call_events: list[ToolCallEvent] = []
    all_reasoning_step_events: list[ReasoningStepEvent] = []
    timings = PhaseTimings()
    turn_offset = 0.0  # each turn's call_ts/ts restarts near 0 -- shift by prior turns' wall time
    tool_index_offset = 0
    reasoning_index_offset = 0

    try:
        for _iteration in range(max_iterations):
            turns += 1
            agent_started = time.monotonic()
            chat_result = client.send_message(conversation_id, current_question)
            agent_elapsed = time.monotonic() - agent_started
            timings.agent_s += agent_elapsed
            reasoning_steps.extend(chat_result.reasoning_steps or [])
            response_id = chat_result.response_id or response_id
            for tc in chat_result.tool_call_events or []:
                if tc.call_ts is not None:
                    tc.call_ts += turn_offset
                if tc.result_ts is not None:
                    tc.result_ts += turn_offset
                if tc.index is not None:
                    tc.index += tool_index_offset
            for rs in chat_result.reasoning_step_events or []:
                rs.ts += turn_offset
                rs.index += reasoning_index_offset
            all_tool_call_events.extend(chat_result.tool_call_events or [])
            all_reasoning_step_events.extend(chat_result.reasoning_step_events or [])
            tool_index_offset += len(chat_result.tool_call_events or [])
            reasoning_index_offset += len(chat_result.reasoning_step_events or [])
            turn_offset += chat_result.turn_wall_clock_sec or 0.0
            for metric_id in _extract_created_metric_ids(chat_result.tool_call_events or []):
                if metric_id not in created_metric_ids:
                    created_metric_ids.append(metric_id)
            candidate = _extract_metric_result(chat_result.tool_call_events or [])
            if candidate is not None:
                log_timer(
                    f"[timer] metric_skill {conversation_id} GoodData turn {turns} complete after "
                    f"{agent_elapsed:.2f}s; metric result received"
                )
                metric_result = candidate
                break
            response_text = (chat_result.text_response or "").strip()
            if not response_text and not chat_result.tool_call_events:
                break
            if _iteration >= max_iterations - 1:
                break
            log_timer(
                f"[timer] metric_skill {conversation_id} GoodData turn {turns} complete after "
                f"{agent_elapsed:.2f}s; waiting for gpt-4o-mini simulated user"
            )
            simulated_started = time.monotonic()
            try:
                current_question = generate_simulated_response(response_text, expected_outputs, question)
            except SimulatedResponseError as exc:
                simulated_elapsed = time.monotonic() - simulated_started
                timings.simulated_user_s += simulated_elapsed
                print(f"[SIM-USER] Simulated reply failed for conversation {conversation_id}: {exc}")
                log_timer(
                    f"[timer] metric_skill {conversation_id} gpt-4o-mini simulated user failed after "
                    f"{simulated_elapsed:.2f}s"
                )
                break
            simulated_elapsed = time.monotonic() - simulated_started
            timings.simulated_user_s += simulated_elapsed
            log_timer(
                f"[timer] metric_skill {conversation_id} gpt-4o-mini simulated user complete after "
                f"{simulated_elapsed:.2f}s"
            )

        actual_maql = (metric_result or {}).get("maql", "")
        metric_created = metric_result is not None
        maql_correct, _ = _best_maql_match(actual_maql, expected_outputs) if metric_created else (False, "")
        return MetricRunResult(
            conversation_id=conversation_id,
            metric_result=metric_result,
            metric_created=metric_created,
            actual_maql=actual_maql,
            maql_correct=maql_correct,
            total_turns=float(turns),
            reasoning_steps=reasoning_steps,
            response_id=response_id,
            tool_call_events=all_tool_call_events,
            reasoning_step_events=all_reasoning_step_events,
            timings=timings,
        )
    finally:
        for metric_id in created_metric_ids:
            _delete_metric(sdk, workspace_id, metric_id)


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
) -> AgenticMetricSummary:
    """Run the metric-skill agentic evaluation K times and return a summary.

    ``expected_output`` may be a single candidate dict or a list of candidate dicts.
    The run passes when the actual MAQL matches any candidate after normalisation.
    """
    expected_outputs: list[dict] = expected_output if isinstance(expected_output, list) else [expected_output]
    run_results: list[MetricRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    sdk = GoodDataSdk.create(host, token)

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(
                _execute_single_metric_run(
                    client, sdk, workspace_id, conv_id_0, question, expected_outputs, max_iterations
                )
            )
        finally:
            if initial_conversation_id is None:  # only delete conversations we created
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(
                    _execute_single_metric_run(
                        client, sdk, workspace_id, conv_id, question, expected_outputs, max_iterations
                    )
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    pass_at_k = any(r.metric_created and r.maql_correct for r in run_results)
    pass_power_k = all(r.metric_created and r.maql_correct for r in run_results)
    best = max(run_results, key=lambda r: (r.maql_correct, r.metric_created))
    return AgenticMetricSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class MetricSkillAssertionError(AgenticAssertionError):
    """Raised when a metric-skill evaluation fails."""


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
) -> AgenticEvalOutcome:
    """Run metric-skill evaluation, log to Langfuse, and raise MetricSkillAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as
    ``.reasoning_steps``/``.conversation_id``/``.response_id`` (mirrors the
    `conversation_id`-on-exception idiom in `ChatClient.ask()`) so callers can retrieve them
    either way.
    """
    langfuse, window_start = open_trace_window(langfuse)
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
    )

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:

            for run_idx, run in enumerate(summary.run_results):
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(pt, run_idx) as tid:
                    ctx.score(tid, name="metric_created", value=float(run.metric_created), data_type="BOOLEAN")
                    ctx.score(tid, name="maql_correct", value=float(run.maql_correct), data_type="BOOLEAN")
                    ctx.quality(
                        tid,
                        strict_checks={"metric_created": run.metric_created, "maql_correct": run.maql_correct},
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
                dataset_name,
                run_timestamp,
                model_version_override,
                run_metadata_extra,
                reasoning_effort,
            ),
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=[r.conversation_id for r in summary.run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(summary.run_results) > 1,
            write_scores=_write_scores,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])

    runs_passed = sum(1 for r in summary.run_results if r.metric_created and r.maql_correct)
    runs_effective = len(summary.run_results)

    best = summary.best
    expected_outputs_list: list[dict] = expected_output if isinstance(expected_output, list) else [expected_output]
    detail = {
        "metric_created": best.metric_created,
        "maql_correct": best.maql_correct,
        "expected_maql_candidates": [c.get("maql", "") for c in expected_outputs_list],
        "actual_maql": best.actual_maql,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
    }

    if not summary.pass_at_k:
        candidates_str = "; ".join(repr(c.get("maql", "")) for c in expected_outputs_list)
        exc = MetricSkillAssertionError(
            f"Metric skill assertion failed. "
            f"metric_created={best.metric_created}, maql_correct={best.maql_correct}. "
            f"Expected MAQL (candidates): {candidates_str}. "
            f"Actual MAQL: {best.actual_maql}."
        )
        exc.reasoning_steps = best.reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = best.response_id
        exc.timings = item_timings
        exc.detail = detail
        exc.runs_passed = runs_passed
        exc.runs_effective = runs_effective
        raise exc
    return AgenticEvalOutcome(
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        timings=item_timings,
    )
