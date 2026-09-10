# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic forecasting-skill evaluation runner.

Unlike kda_skill, this is not limited to "the process ran". The forecasting skill refuses to
execute unless the visualization it points at carries an AAC forecast config, and that config
is where the user's request lands:

    config.forecast_enabled     must be true or execute_forecast returns an error
    config.forecast_period      how many periods ahead -- "next 3 months" is 3
    config.forecast_confidence  confidence level, 0.95 by default
    config.forecast_seasonal    whether seasonality is modelled

So a fixture can state what it asked for and have it checked exactly, with no judge: the
period the agent chose is a number in the tool call it made. The measure it forecast is
checkable the same way, off the visualization's own fields.
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
# The agent routinely asks which measure to forecast before it builds anything (observed
# live: "your data has two different Spend metrics"), so the budget covers a couple of
# disambiguation rounds plus slack, matching kda_skill's reasoning.
_DEFAULT_MAX_ITERATIONS = 4


def _build_clarification_prompt(agent_message: str, expected_output: dict) -> str:
    """The simulated-user reply, mentioning only the hints the fixture actually supplies.

    An absent hint is dropped from the prompt entirely rather than asserted as a literal
    "None", which would answer a question the agent never asked with a wrong value.
    """
    hints: list[str] = []
    metric = expected_output.get("metric")
    if metric:
        hints.append(f"the measure to forecast is {metric}")
    period = expected_output.get("forecast_period")
    if period is not None:
        hints.append(f"the forecast horizon is {period} periods ahead")
    granularity = expected_output.get("granularity")
    if granularity:
        hints.append(f"the time granularity is {granularity}")
    reference = "; ".join(hints)
    return (
        f"You are simulating a user in a conversation with a BI assistant that forecasts metric "
        f"values. The assistant asked: '{agent_message}'. "
        + (f"For reference, {reference}. " if reference else "")
        + "Reply briefly as the user, answering whichever of those the assistant actually asked about."
    )


def generate_simulated_forecast_response(agent_message: str, expected_output: dict) -> str:
    """Generate a user reply to keep the forecasting conversation going (gpt-4o-mini).

    Always OpenAI regardless of the workspace's own model: this is harness plumbing, not the
    system under test.
    """
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError("openai package is required for generate_simulated_forecast_response") from exc

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


def _extract_forecast_calls(
    tool_call_events: list[ToolCallEvent],
) -> tuple[dict | None, dict | None]:
    """Return (visualization_args, execute_result) for the LAST create/execute pair.

    A new create_adhoc_visualization clears any earlier execute result: that result belongs
    to the visualization it followed, not to this one. Picking the last of each
    independently would pair a fresh chart with a stale forecast.
    """
    viz_args: dict | None = None
    execute_result: dict | None = None
    for tc in tool_call_events:
        if tc.function_name == "create_adhoc_visualization":
            args = tc.parsed_arguments() or {}
            viz = args.get("visualization")
            viz_args = viz if isinstance(viz, dict) else args
            execute_result = None
        elif tc.function_name == "execute_forecast" and tc.result:
            execute_result = tc.parsed_result()
    return viz_args, execute_result


def _forecast_config(viz_args: dict | None) -> dict:
    config = (viz_args or {}).get("config")
    return config if isinstance(config, dict) else {}


def _metric_uris(viz_args: dict | None) -> set[str]:
    """The metric URIs the visualization measures, resolved through its field aliases.

    Deliberately not core.scoring.get_metric_uri_set: that takes a parsed
    CreatedVisualization, while this reads the raw tool-call arguments, where a field may be
    a bare URI string rather than an object.
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


@dataclass
class ForecastEvaluation:
    """Scores for a single forecasting run.

    ``triggered``/``executed``/``success``/``turn_completed`` are the process checks every
    skill kind shares. ``forecast_enabled``, ``period_correct`` and ``metric_correct`` are
    content checks, and each is True when the fixture did not ask for it -- an unstated
    expectation must not fail a run, and must not silently pass one either, which is why
    ``asserted`` records which of them the fixture actually pinned.
    """

    triggered: bool
    executed: bool
    success: bool
    turn_completed: bool
    forecast_enabled: bool
    period_correct: bool
    metric_correct: bool
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
                self.forecast_enabled,
                self.period_correct,
                self.metric_correct,
            ]
        )


@dataclass
class ForecastRunResult:
    """Outcome of one run (one conversation, up to max_iterations messages)."""

    conversation_id: str
    evaluation: ForecastEvaluation
    actual_visualization: dict | None
    actual_execute_result: dict | None
    turn_wall_clock_sec: float | None = None
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)


@dataclass
class AgenticForecastSummary:
    """Aggregated outcome of K runs for one forecasting item."""

    run_results: list[ForecastRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: ForecastRunResult


def _evaluate_run(
    viz_args: dict | None,
    execute_result: dict | None,
    expected_output: dict,
    turn_completed: bool,
    disambiguated: bool = False,
) -> ForecastEvaluation:
    triggered = execute_result is not None or viz_args is not None
    executed = execute_result is not None
    success = executed and execute_result.get("success") is True

    config = _forecast_config(viz_args)
    # None is "not set", which the tool treats as disabled -- only an explicit true enables it.
    forecast_enabled = config.get("forecast_enabled") is True

    asserted: list[str] = []
    expected_period = expected_output.get("forecast_period")
    if expected_period is None:
        period_correct = True
    else:
        asserted.append("forecast_period")
        actual_period = config.get("forecast_period")
        period_correct = isinstance(actual_period, int | float) and float(actual_period) == float(expected_period)

    expected_metric = expected_output.get("metric")
    if not expected_metric:
        metric_correct = True
    else:
        asserted.append("metric")
        wanted = {expected_metric} if isinstance(expected_metric, str) else set(expected_metric)
        metric_correct = bool(_metric_uris(viz_args) & wanted)

    return ForecastEvaluation(
        triggered=triggered,
        executed=executed,
        success=success,
        turn_completed=turn_completed,
        forecast_enabled=forecast_enabled,
        period_correct=period_correct,
        metric_correct=metric_correct,
        asserted=asserted,
        disambiguated=disambiguated,
    )


def run_agentic_forecasting(
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
) -> AgenticForecastSummary:
    """Run the forecasting agentic evaluation K times and return a summary.

    A run ends as soon as execute_forecast returns, which is the goal signal. Short of that
    it keeps sending simulated replies up to ``max_iterations``, with no attempt to classify
    whether the agent's text was really a question: missing a genuine clarifying question
    hard-fails the run, while answering a final answer costs one harmless extra turn.
    """
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")
    run_results: list[ForecastRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )

    def _run_once(conv_id: str) -> ForecastRunResult:
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
                _log.warning("Forecast send_message failed for conversation %s: %s", conv_id, exc)
                partial = getattr(exc, "partial_result", None)
                if partial is not None:
                    reasoning_steps.extend(partial.reasoning_steps or [])
                    response_id = partial.response_id or response_id
                    _accumulate(partial)
                    viz_args, execute_result = _extract_forecast_calls(partial.tool_call_events or [])
                turn_completed = False
                break
            reasoning_steps.extend(chat_result.reasoning_steps or [])
            response_id = chat_result.response_id or response_id
            _accumulate(chat_result)
            viz_args, execute_result = _extract_forecast_calls(chat_result.tool_call_events or [])
            response_text = render_answer_text(chat_result)
            turn_completed = chat_result.stream_ended and bool(response_text)
            if execute_result is not None:
                # The turn that actually forecast, not an earlier disambiguation turn.
                turn_wall_clock_sec = chat_result.turn_wall_clock_sec
                break
            if not response_text:
                break
            if iteration >= max_iterations - 1:
                break
            try:
                current_question = generate_simulated_forecast_response(response_text, expected_output)
                disambiguated = True
            except Exception as exc:  # noqa: BLE001 -- harness-side fault; end only this run
                _log.warning("Simulated forecast user reply failed for conversation %s: %s", conv_id, exc)
                break

        return ForecastRunResult(
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
                r.evaluation.forecast_enabled,
                r.evaluation.period_correct,
                r.evaluation.metric_correct,
            ]
        ),
    )
    return AgenticForecastSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class ForecastingAssertionError(AgenticAssertionError):
    """Raised when a forecasting evaluation fails."""


def _detail(best: ForecastRunResult) -> dict[str, Any]:
    ev = best.evaluation
    return {
        "triggered": ev.triggered,
        "executed": ev.executed,
        "success": ev.success,
        "turn_completed": ev.turn_completed,
        "forecast_enabled": ev.forecast_enabled,
        "period_correct": ev.period_correct,
        "metric_correct": ev.metric_correct,
        # Which content checks the fixture pinned. Without it a run where nothing was
        # asserted is indistinguishable in the report from one where everything matched.
        "asserted": ev.asserted,
        "disambiguated": ev.disambiguated,
        "actual_forecast_config": _forecast_config(best.actual_visualization),
        "actual_metrics": sorted(_metric_uris(best.actual_visualization)),
        "actual_execute_result": best.actual_execute_result,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
    }


def evaluate_agentic_forecasting(
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
    dataset_name: str = "forecasting",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
) -> AgenticEvalOutcome:
    """Run forecasting evaluation, log to Langfuse, and raise ForecastingAssertionError on failure."""
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_forecasting(
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
                    "forecast_triggered": ev.triggered,
                    "forecast_executed": ev.executed,
                    "forecast_success": ev.success,
                    "forecast_turn_completed": ev.turn_completed,
                    "forecast_enabled": ev.forecast_enabled,
                    "forecast_period_correct": ev.period_correct,
                    "forecast_metric_correct": ev.metric_correct,
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
            f"Forecasting assertion failed. strict_pass={ev.strict_pass} "
            f"(triggered={ev.triggered}, executed={ev.executed}, success={ev.success}, "
            f"turn_completed={ev.turn_completed}, forecast_enabled={ev.forecast_enabled}, "
            f"period_correct={ev.period_correct}, metric_correct={ev.metric_correct}). "
            f"Actual forecast config: {detail['actual_forecast_config']}. "
            f"Actual execute result: {best.actual_execute_result}."
        )
        exc = ForecastingAssertionError(message)
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
