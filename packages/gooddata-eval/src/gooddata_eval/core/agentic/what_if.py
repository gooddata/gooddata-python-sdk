# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic what-if-analysis skill evaluation runner.

The skill builds a scenario spec and executes it:

    create_what_if_scenario(visualization_ref, scenarios[], include_baseline)
    execute_what_if_scenario(scenario_ref)  ->  one result per scenario, plus the baseline

Each scenario carries adjustments of the form ``{metric_id, metric_type, scenario_maql}``,
where ``scenario_maql`` is the adjusted expression -- a 10% uplift on a revenue metric
defined as ``SELECT SUM({fact/price} * {fact/quantity})`` becomes
``SELECT SUM({fact/price} * 1.10 * {fact/quantity})``.

That makes this the most checkable of the analysis skills: the adjustment is MAQL, and
MAQL already has a comparator here (``evaluators._maql.normalize_maql``, used by
metric_skill), so "did it apply the right adjustment" is answerable without a judge. What
the adjustment produced is not checked -- that is the platform's arithmetic, not the
agent's -- only that the agent asked for the right thing and the execution succeeded.
"""

from __future__ import annotations

import logging
import os
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
from gooddata_eval.core.evaluators._maql import normalize_maql
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
# The agent asks which measure to adjust before building anything (observed live: "I need
# to confirm which 'Spend' calculation you want to adjust"), so the budget covers a couple
# of disambiguation rounds plus slack.
_DEFAULT_MAX_ITERATIONS = 4


def _build_clarification_prompt(agent_message: str, expected_output: dict) -> str:
    """The simulated-user reply, mentioning only the hints the fixture actually supplies."""
    hints: list[str] = []
    metric = expected_output.get("metric_id")
    if metric:
        hints.append(f"the measure to adjust is '{metric}'")
    change = expected_output.get("change")
    if change:
        hints.append(f"the adjustment is {change}")
    period = expected_output.get("period")
    if period:
        hints.append(f"the time period is {period}")
    reference = "; ".join(hints)
    return (
        f"You are simulating a user in a conversation with a BI assistant that runs what-if "
        f"scenario analysis. The assistant asked: '{agent_message}'. "
        + (f"For reference, {reference}. " if reference else "")
        + "Reply briefly as the user, answering whichever of those the assistant actually asked about."
    )


def generate_simulated_what_if_response(agent_message: str, expected_output: dict) -> str:
    """Generate a user reply to keep the what-if conversation going (gpt-4o-mini).

    Always OpenAI regardless of the workspace's own model: harness plumbing, not the system
    under test.
    """
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError("openai package is required for generate_simulated_what_if_response") from exc

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


def _extract_what_if_calls(tool_call_events: list[ToolCallEvent]) -> tuple[dict | None, dict | None]:
    """Return (create_args, execute_result) for the LAST create/execute pair.

    A new create_what_if_scenario clears any earlier execute result: that result belongs to
    the spec it followed. Picking the last of each independently would score a fresh
    scenario against a stale execution.
    """
    create_args: dict | None = None
    execute_result: dict | None = None
    for tc in tool_call_events:
        if tc.function_name == "create_what_if_scenario":
            create_args = tc.parsed_arguments()
            execute_result = None
        elif tc.function_name == "execute_what_if_scenario" and tc.result:
            execute_result = tc.parsed_result()
    return create_args, execute_result


def _adjustments(create_args: dict | None) -> list[dict]:
    """Every adjustment across every scenario, flattened.

    Scenario grouping does not matter to the checks below -- a fixture asserts that the
    right measure was adjusted the right way, not which scenario label it landed under.
    """
    scenarios = (create_args or {}).get("scenarios")
    if not isinstance(scenarios, list):
        return []
    out: list[dict] = []
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            continue
        out.extend(a for a in scenario.get("adjustments") or [] if isinstance(a, dict))
    return out


def _maql_matches(actual_maql: str, expected: str | list[str]) -> bool:
    """Whether the adjustment matches any accepted expression, compared as MAQL.

    Uses metric_skill's normalizer, so whitespace and casing differences do not decide a
    verdict. A list is a candidate set: several expressions can be equally correct
    adjustments (``* 1.1`` and ``* 1.10``, or a rewrite that reaches the same value).
    """
    candidates = [expected] if isinstance(expected, str) else list(expected)
    normalized = normalize_maql(actual_maql)
    return any(normalized == normalize_maql(c) for c in candidates)


@dataclass
class WhatIfEvaluation:
    """Scores for a single what-if run.

    ``triggered``/``executed``/``success``/``turn_completed`` are the shared process checks.
    ``metric_correct``, ``maql_correct``, ``scenario_count_correct`` and ``baseline_correct``
    are content checks, each True when the fixture did not pin it; ``asserted`` records
    which ones it did, so a run that verified nothing is not reported as a full pass.
    """

    triggered: bool
    executed: bool
    success: bool
    turn_completed: bool
    metric_correct: bool
    maql_correct: bool
    scenario_count_correct: bool
    baseline_correct: bool
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
                self.maql_correct,
                self.scenario_count_correct,
                self.baseline_correct,
            ]
        )


@dataclass
class WhatIfRunResult:
    """Outcome of one run (one conversation, up to max_iterations messages)."""

    conversation_id: str
    evaluation: WhatIfEvaluation
    actual_create_args: dict | None
    actual_execute_result: dict | None
    turn_wall_clock_sec: float | None = None
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)


@dataclass
class AgenticWhatIfSummary:
    """Aggregated outcome of K runs for one what-if item."""

    run_results: list[WhatIfRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: WhatIfRunResult


def _evaluate_run(
    create_args: dict | None,
    execute_result: dict | None,
    expected_output: dict,
    turn_completed: bool,
    disambiguated: bool = False,
) -> WhatIfEvaluation:
    triggered = create_args is not None
    executed = execute_result is not None
    success = executed and execute_result.get("success") is True
    adjustments = _adjustments(create_args)
    asserted: list[str] = []

    expected_metric = expected_output.get("metric_id")
    if not expected_metric:
        metric_correct = True
    else:
        asserted.append("metric_id")
        wanted = {expected_metric} if isinstance(expected_metric, str) else set(expected_metric)
        metric_correct = any(a.get("metric_id") in wanted for a in adjustments)

    expected_maql = expected_output.get("scenario_maql")
    if not expected_maql:
        maql_correct = True
    else:
        asserted.append("scenario_maql")
        maql_correct = any(
            isinstance(a.get("scenario_maql"), str) and _maql_matches(a["scenario_maql"], expected_maql)
            for a in adjustments
        )

    expected_scenarios = expected_output.get("scenarios")
    if expected_scenarios is None:
        scenario_count_correct = True
    else:
        asserted.append("scenarios")
        actual = (create_args or {}).get("scenarios")
        scenario_count_correct = isinstance(actual, list) and len(actual) == expected_scenarios

    expected_baseline = expected_output.get("include_baseline")
    if expected_baseline is None:
        baseline_correct = True
    else:
        asserted.append("include_baseline")
        # The tool defaults include_baseline to true, so an absent argument means true --
        # `.get(..., True)` would be wrong only if the agent sent an explicit null, which
        # the `is None` fallback below also treats as the default.
        actual_baseline = (create_args or {}).get("include_baseline")
        baseline_correct = (True if actual_baseline is None else bool(actual_baseline)) == bool(expected_baseline)

    return WhatIfEvaluation(
        triggered=triggered,
        executed=executed,
        success=success,
        turn_completed=turn_completed,
        metric_correct=metric_correct,
        maql_correct=maql_correct,
        scenario_count_correct=scenario_count_correct,
        baseline_correct=baseline_correct,
        asserted=asserted,
        disambiguated=disambiguated,
    )


def run_agentic_what_if(
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
) -> AgenticWhatIfSummary:
    """Run the what-if agentic evaluation K times and return a summary.

    A run ends when execute_what_if_scenario returns. Short of that it keeps sending
    simulated replies up to ``max_iterations``, without trying to classify whether the
    agent's text was a question: missing a genuine one hard-fails the run, while answering
    a final answer costs one harmless extra turn.
    """
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")
    run_results: list[WhatIfRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )

    def _run_once(conv_id: str) -> WhatIfRunResult:
        create_args: dict | None = None
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
                _log.warning("What-if send_message failed for conversation %s: %s", conv_id, exc)
                partial = getattr(exc, "partial_result", None)
                if partial is not None:
                    reasoning_steps.extend(partial.reasoning_steps or [])
                    response_id = partial.response_id or response_id
                    _accumulate(partial)
                    create_args, execute_result = _extract_what_if_calls(partial.tool_call_events or [])
                turn_completed = False
                break
            reasoning_steps.extend(chat_result.reasoning_steps or [])
            response_id = chat_result.response_id or response_id
            _accumulate(chat_result)
            create_args, execute_result = _extract_what_if_calls(chat_result.tool_call_events or [])
            response_text = render_answer_text(chat_result)
            turn_completed = chat_result.stream_ended and bool(response_text)
            if execute_result is not None:
                # The turn that ran the scenario, not an earlier disambiguation turn.
                turn_wall_clock_sec = chat_result.turn_wall_clock_sec
                break
            if not response_text:
                break
            if iteration >= max_iterations - 1:
                break
            try:
                current_question = generate_simulated_what_if_response(response_text, expected_output)
                disambiguated = True
            except Exception as exc:  # noqa: BLE001 -- harness-side fault; end only this run
                _log.warning("Simulated what-if user reply failed for conversation %s: %s", conv_id, exc)
                break

        return WhatIfRunResult(
            conversation_id=conv_id,
            evaluation=_evaluate_run(create_args, execute_result, expected_output, turn_completed, disambiguated),
            actual_create_args=create_args,
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
                r.evaluation.maql_correct,
                r.evaluation.scenario_count_correct,
                r.evaluation.baseline_correct,
            ]
        ),
    )
    return AgenticWhatIfSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class WhatIfAssertionError(AgenticAssertionError):
    """Raised when a what-if evaluation fails."""


def _detail(best: WhatIfRunResult) -> dict[str, Any]:
    ev = best.evaluation
    adjustments = _adjustments(best.actual_create_args)
    return {
        "triggered": ev.triggered,
        "executed": ev.executed,
        "success": ev.success,
        "turn_completed": ev.turn_completed,
        "metric_correct": ev.metric_correct,
        "maql_correct": ev.maql_correct,
        "scenario_count_correct": ev.scenario_count_correct,
        "baseline_correct": ev.baseline_correct,
        # Which content checks the fixture pinned -- without it a run that verified nothing
        # reads the same as one where everything matched.
        "asserted": ev.asserted,
        "disambiguated": ev.disambiguated,
        "actual_adjustments": adjustments,
        "actual_scenario_labels": [
            s.get("label") for s in ((best.actual_create_args or {}).get("scenarios") or []) if isinstance(s, dict)
        ],
        "actual_execute_result": best.actual_execute_result,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
    }


def evaluate_agentic_what_if(
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
    dataset_name: str = "what_if_analysis",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
) -> AgenticEvalOutcome:
    """Run what-if evaluation, log to Langfuse, and raise WhatIfAssertionError on failure."""
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_what_if(
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
                    "what_if_triggered": ev.triggered,
                    "what_if_executed": ev.executed,
                    "what_if_success": ev.success,
                    "what_if_turn_completed": ev.turn_completed,
                    "what_if_metric_correct": ev.metric_correct,
                    "what_if_maql_correct": ev.maql_correct,
                    "what_if_scenario_count_correct": ev.scenario_count_correct,
                    "what_if_baseline_correct": ev.baseline_correct,
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
            f"What-if assertion failed. strict_pass={ev.strict_pass} "
            f"(triggered={ev.triggered}, executed={ev.executed}, success={ev.success}, "
            f"turn_completed={ev.turn_completed}, metric_correct={ev.metric_correct}, "
            f"maql_correct={ev.maql_correct}, scenario_count_correct={ev.scenario_count_correct}, "
            f"baseline_correct={ev.baseline_correct}). "
            f"Actual adjustments: {detail['actual_adjustments']}. "
            f"Actual execute result: {best.actual_execute_result}."
        )
        exc = WhatIfAssertionError(message)
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
