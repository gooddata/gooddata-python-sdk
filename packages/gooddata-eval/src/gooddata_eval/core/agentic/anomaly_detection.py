# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic anomaly-detection skill evaluation runner.

The skill is a single tool over a chart the agent builds first:

    create_adhoc_visualization(...)                     a measure over a time dimension
    execute_anomaly_detection(visualization_ref, max_points)

Its parameters say nothing about *what* to look for -- there is no threshold, no
sensitivity, no expected anomaly -- so unlike forecasting and what-if, the tool call itself
carries almost no assertable intent. What is assertable is the chart the detection ran on:
the measure and the time granularity are the whole of the question "did it look at the
right series", and getting either wrong makes the result meaningless however well the
detection itself performed.

Granularity is resolved in the tool's own order -- field tokens first, then a relative date
filter's granularity -- so the evaluation reads the chart the way the service does. It
differs in one respect, deliberately: see ``_granularity_from``.

The count of flagged points is reported but never asserted: whether a real series contains
anomalies is a property of the data, not of the agent, and a fixture that demanded some
would start failing the day the warehouse refreshed.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from typing import Any

from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_trace_window,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
    shift_and_index_events,
)

_log = logging.getLogger(__name__)

_DEFAULT_K = 1
# Observed live, the agent completes this in one turn (search, build, detect). The budget
# is disambiguation headroom for questions that name an ambiguous measure.
_DEFAULT_MAX_ITERATIONS = 4

# The granularities the detection tool recognises, keyed by the tokens it looks for. Copied
# from gen-ai's own token map -- note "date" maps to DAY there, which is what makes a label
# like process_date.month ambiguous (see _granularity_from).
_TOKEN_TO_GRANULARITY = {
    "day": "DAY",
    "date": "DAY",
    "week": "WEEK",
    "month": "MONTH",
    "quarter": "QUARTER",
    "year": "YEAR",
}


def _build_clarification_prompt(agent_message: str, expected_output: dict) -> str:
    """The simulated-user reply, mentioning only the hints the fixture actually supplies."""
    hints: list[str] = []
    metric = expected_output.get("metric")
    if metric:
        hints.append(f"the measure to analyse is {metric}")
    granularity = expected_output.get("granularity")
    if granularity:
        hints.append(f"the time granularity is {granularity}")
    period = expected_output.get("period")
    if period:
        hints.append(f"the period to cover is {period}")
    reference = "; ".join(hints)
    return (
        f"You are simulating a user in a conversation with a BI assistant that detects anomalies "
        f"in a metric over time. The assistant asked: '{agent_message}'. "
        + (f"For reference, {reference}. " if reference else "")
        + "Reply briefly as the user, answering whichever of those the assistant actually asked about."
    )


def generate_simulated_anomaly_response(agent_message: str, expected_output: dict) -> str:
    """Generate a user reply to keep the anomaly conversation going (gpt-4o-mini).

    Always OpenAI regardless of the workspace's own model: harness plumbing, not the system
    under test.
    """
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError("openai package is required for generate_simulated_anomaly_response") from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise OSError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": _build_clarification_prompt(agent_message, expected_output)}],
        max_tokens=150,
        temperature=0,
        timeout=30,
    )
    return response.choices[0].message.content or "Please proceed with the most complete option."


def _extract_anomaly_calls(tool_call_events: list[ToolCallEvent]) -> tuple[dict | None, dict | None]:
    """Return (visualization_args, execute_result) for the LAST create/execute pair.

    A new chart clears any earlier detection result: that result described the chart it
    followed. Taking the last of each independently would score a fresh series against a
    detection that never ran on it.
    """
    viz_args: dict | None = None
    execute_result: dict | None = None
    for tc in tool_call_events:
        if tc.function_name == "create_adhoc_visualization":
            args = tc.parsed_arguments() or {}
            viz = args.get("visualization")
            viz_args = viz if isinstance(viz, dict) else args
            execute_result = None
        elif tc.function_name == "execute_anomaly_detection" and tc.result:
            execute_result = tc.parsed_result()
    return viz_args, execute_result


def _granularity_from(value: str) -> str | None:
    """The granularity a field reference names, taking the LAST recognised token.

    Deliberately not the service's own rule. gen-ai tokenizes the same string into a *set*
    and returns the first match it happens to iterate, so ``label/process_date.month``
    yields MONTH or DAY depending on hash order -- ``date`` and ``month`` both map. Taking
    the last token instead reads the suffix, which is what a dotted label means, and is
    deterministic. The divergence only shows up on references that name two granularities,
    where the service's answer is not stable anyway.
    """
    parts = [part for part in re.split(r"[^a-zA-Z0-9]+", value.lower()) if part]
    for part in reversed(parts):
        if part in _TOKEN_TO_GRANULARITY:
            return _TOKEN_TO_GRANULARITY[part]
    return None


def _metric_uris(viz_args: dict | None) -> set[str]:
    """The metric URIs the chart measures, resolved through its field aliases.

    Reads raw tool-call arguments rather than a parsed CreatedVisualization, so a field may
    be a bare URI string as well as an object.
    """
    query = (viz_args or {}).get("query")
    fields = query.get("fields") if isinstance(query, dict) else None
    if not isinstance(fields, dict):
        return set()
    uris: set[str] = set()
    for alias in (viz_args or {}).get("metrics") or list(fields):
        name = alias.get("field") if isinstance(alias, dict) else alias
        field_def = fields.get(name)
        if isinstance(field_def, dict) and field_def.get("using"):
            uris.add(str(field_def["using"]))
        elif isinstance(field_def, str):
            uris.add(field_def)
    return {u for u in uris if u.startswith(("metric/", "fact/"))}


def _inferred_granularity(viz_args: dict | None) -> str | None:
    """The granularity the detection tool would read off this chart.

    Follows gen-ai's own resolution ORDER -- field ``using``/``title`` tokens first, then a
    relative date filter's ``granularity`` -- so a chart scored here as monthly is the one
    the service analysed monthly. Within a single reference it differs on purpose; see
    ``_granularity_from``.
    """
    query = (viz_args or {}).get("query")
    if not isinstance(query, dict):
        return None

    fields = query.get("fields")
    if isinstance(fields, dict):
        for field_def in fields.values():
            if isinstance(field_def, dict):
                reference = f"{field_def.get('using') or ''} {field_def.get('title') or ''}"
            elif isinstance(field_def, str):
                reference = field_def
            else:
                continue
            granularity = _granularity_from(reference)
            if granularity is not None:
                return granularity

    filter_by = query.get("filter_by")
    if isinstance(filter_by, dict):
        for filter_def in filter_by.values():
            if not isinstance(filter_def, dict) or filter_def.get("type") != "date_filter":
                continue
            granularity = _granularity_from(str(filter_def.get("granularity", "")))
            if granularity is not None:
                return granularity
    return None


def _point_count(execute_result: dict | None) -> int | None:
    data = (execute_result or {}).get("data")
    if not isinstance(data, dict):
        return None
    count = data.get("point_count")
    return count if isinstance(count, int) else None


@dataclass
class AnomalyEvaluation:
    """Scores for a single anomaly-detection run.

    ``triggered``/``executed``/``success``/``turn_completed`` are the shared process checks.
    ``metric_correct`` and ``granularity_correct`` ask whether the detection ran on the
    right series at all; each is True when the fixture did not pin it, and ``asserted``
    records which ones it did.
    """

    triggered: bool
    executed: bool
    success: bool
    turn_completed: bool
    metric_correct: bool
    granularity_correct: bool
    asserted: list[str] = field(default_factory=list)
    disambiguated: bool = False

    @property
    def strict_pass(self) -> bool:
        return all(
            [
                self.triggered,
                self.executed,
                self.success,
                self.turn_completed,
                self.metric_correct,
                self.granularity_correct,
            ]
        )


@dataclass
class AnomalyRunResult:
    """Outcome of one run (one conversation, up to max_iterations messages)."""

    conversation_id: str
    evaluation: AnomalyEvaluation
    actual_visualization: dict | None
    actual_execute_result: dict | None
    turn_wall_clock_sec: float | None = None
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)


@dataclass
class AgenticAnomalySummary:
    """Aggregated outcome of K runs for one anomaly-detection item."""

    run_results: list[AnomalyRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: AnomalyRunResult


def _evaluate_run(
    viz_args: dict | None,
    execute_result: dict | None,
    expected_output: dict,
    turn_completed: bool,
    disambiguated: bool = False,
) -> AnomalyEvaluation:
    triggered = execute_result is not None or viz_args is not None
    executed = execute_result is not None
    success = executed and execute_result.get("success") is True
    asserted: list[str] = []

    expected_metric = expected_output.get("metric")
    if not expected_metric:
        metric_correct = True
    else:
        asserted.append("metric")
        wanted = {expected_metric} if isinstance(expected_metric, str) else set(expected_metric)
        metric_correct = bool(_metric_uris(viz_args) & wanted)

    expected_granularity = expected_output.get("granularity")
    if not expected_granularity:
        granularity_correct = True
    else:
        asserted.append("granularity")
        granularity_correct = _inferred_granularity(viz_args) == str(expected_granularity).upper()

    return AnomalyEvaluation(
        triggered=triggered,
        executed=executed,
        success=success,
        turn_completed=turn_completed,
        metric_correct=metric_correct,
        granularity_correct=granularity_correct,
        asserted=asserted,
        disambiguated=disambiguated,
    )


def run_agentic_anomaly_detection(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
) -> AgenticAnomalySummary:
    """Run the anomaly-detection agentic evaluation K times and return a summary.

    A run ends when execute_anomaly_detection returns. Short of that it keeps sending
    simulated replies up to ``max_iterations``, without classifying whether the agent's
    text was a question: missing a genuine one hard-fails the run, while answering a final
    answer costs one harmless extra turn.
    """
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")
    run_results: list[AnomalyRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )

    def _run_once(conv_id: str) -> AnomalyRunResult:
        viz_args: dict | None = None
        execute_result: dict | None = None
        turn_wall_clock_sec: float | None = None
        turn_completed = False
        disambiguated = False
        current_question = question
        reasoning_steps: list[str] = []
        response_id: str | None = None
        all_tool_call_events: list[ToolCallEvent] = []
        all_reasoning_step_events: list[ReasoningStepEvent] = []
        turn_offset = 0.0  # each turn's call_ts/ts restarts near 0 -- shift by prior turns' wall time
        tool_index_offset = 0
        reasoning_index_offset = 0

        def _accumulate(result: ChatResult) -> None:
            nonlocal turn_offset, tool_index_offset, reasoning_index_offset
            turn_offset, tool_index_offset, reasoning_index_offset = shift_and_index_events(
                result,
                turn_offset=turn_offset,
                tool_index_offset=tool_index_offset,
                reasoning_index_offset=reasoning_index_offset,
            )
            all_tool_call_events.extend(result.tool_call_events or [])
            all_reasoning_step_events.extend(result.reasoning_step_events or [])

        for iteration in range(max_iterations):
            try:
                chat_result = client.send_message(conv_id, current_question)
            except Exception as exc:  # noqa: BLE001 -- end this run, not the whole item
                _log.warning("Anomaly send_message failed for conversation %s: %s", conv_id, exc)
                partial = getattr(exc, "partial_result", None)
                if partial is not None:
                    reasoning_steps.extend(partial.reasoning_steps or [])
                    response_id = partial.response_id or response_id
                    _accumulate(partial)
                    viz_args, execute_result = _extract_anomaly_calls(partial.tool_call_events or [])
                turn_completed = False
                break
            reasoning_steps.extend(chat_result.reasoning_steps or [])
            response_id = chat_result.response_id or response_id
            _accumulate(chat_result)
            viz_args, execute_result = _extract_anomaly_calls(chat_result.tool_call_events or [])
            response_text = render_answer_text(chat_result)
            turn_completed = chat_result.stream_ended and bool(response_text)
            if execute_result is not None:
                # The turn that ran the detection, not an earlier disambiguation turn.
                turn_wall_clock_sec = chat_result.turn_wall_clock_sec
                break
            if not response_text:
                break
            if iteration >= max_iterations - 1:
                break
            try:
                current_question = generate_simulated_anomaly_response(response_text, expected_output)
                disambiguated = True
            except Exception as exc:  # noqa: BLE001 -- harness-side fault; end only this run
                _log.warning("Simulated anomaly user reply failed for conversation %s: %s", conv_id, exc)
                break

        return AnomalyRunResult(
            conversation_id=conv_id,
            evaluation=_evaluate_run(viz_args, execute_result, expected_output, turn_completed, disambiguated),
            actual_visualization=viz_args,
            actual_execute_result=execute_result,
            turn_wall_clock_sec=turn_wall_clock_sec,
            reasoning_steps=reasoning_steps,
            response_id=response_id,
            tool_call_events=all_tool_call_events,
            reasoning_step_events=all_reasoning_step_events,
        )

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(_run_once(conv_id_0))
        finally:
            if initial_conversation_id is None:  # only delete conversations we created
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(_run_once(conv_id))
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    pass_at_k = any(r.evaluation.strict_pass for r in run_results)
    pass_power_k = all(r.evaluation.strict_pass for r in run_results)
    best = max(
        run_results,
        key=lambda r: sum(
            [
                r.evaluation.triggered,
                r.evaluation.executed,
                r.evaluation.success,
                r.evaluation.turn_completed,
                r.evaluation.metric_correct,
                r.evaluation.granularity_correct,
            ]
        ),
    )
    return AgenticAnomalySummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class AnomalyDetectionAssertionError(AgenticAssertionError):
    """Raised when an anomaly-detection evaluation fails."""


def _detail(best: AnomalyRunResult) -> dict[str, Any]:
    ev = best.evaluation
    return {
        "triggered": ev.triggered,
        "executed": ev.executed,
        "success": ev.success,
        "turn_completed": ev.turn_completed,
        "metric_correct": ev.metric_correct,
        "granularity_correct": ev.granularity_correct,
        # Which content checks the fixture pinned -- without it a run that verified nothing
        # reads the same as one where everything matched.
        "asserted": ev.asserted,
        "disambiguated": ev.disambiguated,
        "actual_metrics": sorted(_metric_uris(best.actual_visualization)),
        "actual_granularity": _inferred_granularity(best.actual_visualization),
        # Reported, never asserted: whether a real series contains anomalies is a property
        # of the data, so a fixture demanding some would fail on the next warehouse refresh.
        "anomaly_point_count": _point_count(best.actual_execute_result),
        "actual_execute_result": best.actual_execute_result,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
    }


def evaluate_agentic_anomaly_detection(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "anomaly_detection",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
) -> AgenticEvalOutcome:
    """Run anomaly-detection evaluation, log to Langfuse, and raise on failure."""
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_anomaly_detection(
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
                ev = run.evaluation
                strict_checks = {
                    "anomaly_triggered": ev.triggered,
                    "anomaly_executed": ev.executed,
                    "anomaly_success": ev.success,
                    "anomaly_turn_completed": ev.turn_completed,
                    "anomaly_metric_correct": ev.metric_correct,
                    "anomaly_granularity_correct": ev.granularity_correct,
                }
                with ctx.observe(pt, run_idx) as tid:
                    for score_name, value in strict_checks.items():
                        ctx.score(tid, name=score_name, value=float(value), data_type="BOOLEAN")
                    ctx.quality(
                        tid,
                        strict_checks=strict_checks,
                        latency_sec=run.turn_wall_clock_sec,
                        cost_usd=pt.total_cost if pt and ev.triggered else None,
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

    best = summary.best
    ev = best.evaluation
    detail = _detail(best)
    runs_passed = sum(1 for r in summary.run_results if r.evaluation.strict_pass)

    if not summary.pass_at_k:
        message = (
            f"Anomaly detection assertion failed. strict_pass={ev.strict_pass} "
            f"(triggered={ev.triggered}, executed={ev.executed}, success={ev.success}, "
            f"turn_completed={ev.turn_completed}, metric_correct={ev.metric_correct}, "
            f"granularity_correct={ev.granularity_correct}). "
            f"Analysed {detail['actual_metrics']} at {detail['actual_granularity']}. "
            f"Actual execute result: {best.actual_execute_result}."
        )
        exc = AnomalyDetectionAssertionError(message)
        exc.reasoning_steps = best.reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = best.response_id
        exc.detail = detail
        exc.runs_passed = runs_passed
        exc.runs_effective = len(summary.run_results)
        raise exc

    return AgenticEvalOutcome(
        runs_passed=runs_passed,
        runs_effective=len(summary.run_results),
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
    )
