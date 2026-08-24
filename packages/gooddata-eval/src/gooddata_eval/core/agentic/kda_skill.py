# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic KDA (Key Driver Analysis)-skill evaluation runner."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import AgenticEvalOutcome, ToolCallEvent

_log = logging.getLogger(__name__)

_DEFAULT_K = 1
# Disambiguation safety net only (create+execute always run together in the same turn) --
# 3 real questions' worth (metric, period, +1 slack) since a simulated reply is now sent on
# every non-final turn (see run_agentic_kda_skill), not just ones classified as a question.
_DEFAULT_MAX_ITERATIONS = 4


def _build_period_hint(expected_output: dict) -> str | None:
    """Build a period hint from whichever of expected_output's Date Attribute/Analyzed
    Period/Reference Period are present -- a question about only one of them (e.g. "which
    date dimension?") must still get an answerable hint, not None just because the other
    two are absent.
    """
    date_attr = expected_output.get("Date Attribute")
    analyzed = expected_output.get("Analyzed Period")
    reference_period = expected_output.get("Reference Period")
    if not (date_attr or analyzed or reference_period):
        return None
    parts = []
    if date_attr:
        parts.append(date_attr)
    if analyzed and reference_period:
        parts.append(f"comparing {analyzed} to {reference_period}")
    elif analyzed:
        parts.append(f"period {analyzed}")
    elif reference_period:
        parts.append(f"compared to {reference_period}")
    return ", ".join(parts)


def _build_clarification_prompt(
    agent_message: str, measure_candidates: dict | list[dict] | None, period_hint: str | None
) -> str:
    """Build the simulated-user prompt, referencing only whatever candidates/period-hint
    are actually usable -- an empty/None candidate must drop the "acceptable metric/fact"
    clause entirely rather than assert a literal "None" as if it were a real option.
    """
    candidates = [
        c for c in (measure_candidates if isinstance(measure_candidates, list) else [measure_candidates]) if c
    ]
    reference = ""
    if candidates:
        candidate_desc = "; or ".join(
            f"{c.get('type')} '{c.get('id')}'" + (f" (aggregation {c['aggregation']})" if c.get("aggregation") else "")
            for c in candidates
        )
        reference = f"an acceptable metric/fact is {candidate_desc}"
    if period_hint:
        reference = (
            f"{reference}; the intended time period is {period_hint}"
            if reference
            else f"the intended time period is {period_hint}"
        )
    return (
        f"You are simulating a user in a conversation with a BI assistant that runs key driver "
        f"analysis. The assistant asked: '{agent_message}'. "
        + (f"For reference, {reference}. " if reference else "")
        + "Reply briefly as the user, answering whichever of those the assistant actually asked about."
    )


def generate_simulated_kda_response(
    agent_message: str,
    measure_candidates: dict | list[dict] | None,
    period_hint: str | None = None,
) -> str:
    """Generate a user reply to keep the KDA-skill conversation going (gpt-4o-mini).

    Called on any turn that didn't trigger KDA, whatever the agent's response actually
    said -- most often a clarifying question about the measure, the period, or both, so
    both are given as reference and the reply answers whichever was actually asked.
    Scope only needs KDA to trigger, not the resulting measure/period to be exactly
    right. Always OpenAI regardless of the combo's own provider -- this is
    test-harness plumbing, not the system under test.
    """
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError("openai package is required for generate_simulated_kda_response") from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise OSError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)
    prompt = _build_clarification_prompt(agent_message, measure_candidates, period_hint)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0,
        timeout=30,
    )
    return response.choices[0].message.content or "Please proceed with either option."


def _extract_kda_calls(tool_call_events: list[ToolCallEvent]) -> tuple[dict | None, dict | None]:
    """Return (create_args, execute_result) for the LAST create/execute pair in this turn's
    tool calls -- not the last create and last execute picked independently. A new create
    call clears any earlier execute_result -- it belongs to the create it followed, not to
    this one.
    """
    create_args: dict | None = None
    execute_result: dict | None = None
    for tc in tool_call_events:
        if tc.function_name == "create_key_driver_analysis":
            create_args = tc.parsed_arguments()
            execute_result = None
        elif tc.function_name == "execute_key_driver_analysis" and tc.result:
            execute_result = tc.parsed_result()
    return create_args, execute_result


@dataclass
class KdaEvaluation:
    """Evaluation scores for a single KDA-skill run.

    Scope: asserts only that the KDA process runs to completion -- the tool chain
    triggers, executes successfully, and the chat turn ends cleanly with a non-empty
    response (``turn_completed`` requires both gen-ai's stream-ended signal and a
    non-empty ``text_response`` -- a stream that ends cleanly but delivers nothing to the
    user isn't a completed turn either).
    """

    triggered: bool
    executed: bool
    success: bool
    turn_completed: bool
    disambiguated: bool = False

    @property
    def strict_pass(self) -> bool:
        return all([self.triggered, self.executed, self.success, self.turn_completed])


@dataclass
class KdaRunResult:
    """Outcome of one run (one conversation, up to max_iterations messages) for a KDA case."""

    conversation_id: str
    evaluation: KdaEvaluation
    actual_create_args: dict | None
    actual_execute_result: dict | None
    # Wall-clock time of the turn that called create (None if create never happened) --
    # not any earlier disambiguation turn. See run_agentic_kda_skill's _run_once.
    turn_wall_clock_sec: float | None = None
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None


@dataclass
class AgenticKdaSummary:
    """Aggregated outcome of K runs for a KDA case."""

    run_results: list[KdaRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: KdaRunResult


def _evaluate_run(
    create_args: dict | None,
    execute_result: dict | None,
    turn_completed: bool,
    disambiguated: bool = False,
) -> KdaEvaluation:
    triggered = create_args is not None
    executed = execute_result is not None
    success = executed and execute_result.get("success") is True
    return KdaEvaluation(
        triggered=triggered,
        executed=executed,
        success=success,
        turn_completed=turn_completed,
        disambiguated=disambiguated,
    )


def run_agentic_kda_skill(
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
) -> AgenticKdaSummary:
    """Run the KDA-skill agentic evaluation K times and return a summary.

    Each run is normally one message, one turn -- create and execute are always called
    together in the same turn (the skill's own system prompt: "NO confirmation needed").
    A run only extends past turn 1, up to ``max_iterations``, when the agent's response
    has no create call and isn't empty; a simulated user reply is then always sent, with
    no attempt to classify whether the text was actually asking for input (matching
    visualization.py/alert_skill.py's own break conditions) -- missing a genuine
    clarifying question hard-fails the run, while sending one after an unrecognized final
    answer only costs one harmless extra turn, so the asymmetry favors never guessing.
    """
    if k < 1:
        # k=0 or negative would otherwise silently run once, indistinguishable from k=1.
        raise ValueError(f"k must be >= 1, got {k}")
    run_results: list[KdaRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )

    def _run_once(conv_id: str) -> KdaRunResult:
        create_args: dict | None = None
        execute_result: dict | None = None
        turn_wall_clock_sec: float | None = None
        turn_completed = False
        disambiguated = False
        current_question = question
        reasoning_steps: list[str] = []
        response_id: str | None = None

        for iteration in range(max_iterations):
            try:
                chat_result = client.send_message(conv_id, current_question)
            except Exception as exc:  # noqa: BLE001 -- end this run, not the whole assertion
                _log.warning("KDA send_message failed for conversation %s: %s", conv_id, exc)
                partial = getattr(exc, "partial_result", None)
                if partial is not None:
                    reasoning_steps.extend(partial.reasoning_steps or [])
                    response_id = partial.response_id or response_id
                    create_args, execute_result = _extract_kda_calls(partial.tool_call_events or [])
                    if create_args is not None:
                        turn_wall_clock_sec = partial.turn_wall_clock_sec
                turn_completed = False
                break
            reasoning_steps.extend(chat_result.reasoning_steps or [])
            response_id = chat_result.response_id or response_id
            create_args, execute_result = _extract_kda_calls(chat_result.tool_call_events or [])
            response_text = (chat_result.text_response or "").strip()
            turn_completed = chat_result.stream_ended and bool(response_text)
            if create_args is not None:
                # This turn's own time -- the turn that called create, not any earlier
                # disambiguation turn or the simulated-reply generation. create and execute
                # are always called together in the same turn (or not at all), so this is
                # final either way -- execute_result may still be None (e.g. the skill's
                # execute tool isn't available at all when data-sharing is off for the org).
                turn_wall_clock_sec = chat_result.turn_wall_clock_sec
                break
            if not response_text:
                break
            if iteration >= max_iterations - 1:
                break
            # No text classification -- matches visualization.py/alert_skill.py: break only on
            # the goal signal (create_args set) or an empty response, otherwise always send a
            # simulated reply. A false positive (agent had already given a final answer) costs
            # one harmless extra turn; a false negative (missing a genuine clarifying question)
            # would hard-fail the run, so the asymmetry favors never trying to tell them apart.
            measure_candidates = expected_output.get("Measure") if isinstance(expected_output, dict) else None
            period_hint = _build_period_hint(expected_output) if isinstance(expected_output, dict) else None
            try:
                current_question = generate_simulated_kda_response(response_text, measure_candidates, period_hint)
                disambiguated = True
            except Exception as exc:  # noqa: BLE001 -- safety net, not the assertion; end only this run
                _log.warning("Simulated KDA user reply failed for conversation %s: %s", conv_id, exc)
                break

        ev = _evaluate_run(create_args, execute_result, turn_completed, disambiguated)
        return KdaRunResult(
            conversation_id=conv_id,
            evaluation=ev,
            actual_create_args=create_args,
            actual_execute_result=execute_result,
            turn_wall_clock_sec=turn_wall_clock_sec,
            reasoning_steps=reasoning_steps,
            response_id=response_id,
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
            [r.evaluation.triggered, r.evaluation.executed, r.evaluation.success, r.evaluation.turn_completed]
        ),
    )
    return AgenticKdaSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class KdaSkillAssertionError(AssertionError):
    """Raised when a KDA-skill evaluation fails."""

    __tracebackhide__ = True
    reasoning_steps: list[str]
    conversation_id: str
    response_id: str | None
    detail: dict


def evaluate_agentic_kda_skill(
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
    dataset_name: str = "kda_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
) -> AgenticEvalOutcome:
    """Run KDA-skill evaluation, log to Langfuse, and raise KdaSkillAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as ``.reasoning_steps``/``.conversation_id``/``.response_id``.
    """
    from datetime import datetime as _dt  # noqa: PLC0415
    from datetime import timezone as _tz  # noqa: PLC0415

    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    if langfuse is None:
        langfuse = try_make_langfuse_client()
    window_start = _dt.now(_tz.utc)
    summary = run_agentic_kda_skill(
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
        from gooddata_eval.core.agentic._langfuse import (  # noqa: PLC0415
            build_run_context,
            find_traces_per_conversation,
            log_quality_and_value_scores,
            observe,
            score_safe,
        )

        run_name_base, run_metadata = build_run_context(
            host,
            token,
            workspace_id,
            dataset_name,
            run_timestamp,
            model_version_override,
            run_metadata_extra,
            reasoning_effort,
        )
        # No custom selector -- same default (max-latency) as every other skill; harmless
        # here since latency comes from run.turn_wall_clock_sec below, not this trace.
        traces_by_conv = find_traces_per_conversation(
            langfuse,
            [r.conversation_id for r in summary.run_results],
            window_start,
        )
        suffix_needed = len(summary.run_results) > 1
        for run_idx, run in enumerate(summary.run_results):
            pt = traces_by_conv.get(run.conversation_id)
            run_name = f"{run_name_base}_run{run_idx}" if suffix_needed else run_name_base
            ev = run.evaluation
            # Gates strict_pass -- current scope is completion only (see KdaEvaluation docstring).
            strict_checks = {
                "kda_triggered": ev.triggered,
                "kda_executed": ev.executed,
                "kda_success": ev.success,
                "kda_turn_completed": ev.turn_completed,
            }
            # Not pt.latency: pt can be any trace of the conversation, not necessarily the KDA turn.
            turn_wall_clock_sec = run.turn_wall_clock_sec
            _log.info("[kda-report] %s: strict_pass=%s latency_sec=%s", run_name, ev.strict_pass, turn_wall_clock_sec)
            with observe(langfuse, pt.id if pt else None, dataset_item_id, run_name, run_metadata) as tid:
                for score_name, value in strict_checks.items():
                    score_safe(langfuse, tid, name=score_name, value=float(value), data_type="BOOLEAN")
                score_safe(langfuse, tid, name="kda_disambiguated", value=float(ev.disambiguated), data_type="BOOLEAN")
                if turn_wall_clock_sec is not None:
                    # combo_report.py reads this score directly -- no trace re-resolution needed.
                    score_safe(
                        langfuse, tid, name="kda_turn_wall_clock_sec", value=turn_wall_clock_sec, data_type="NUMERIC"
                    )
                log_quality_and_value_scores(
                    langfuse,
                    tid,
                    strict_checks=strict_checks,
                    latency_sec=turn_wall_clock_sec,
                    cost_usd=pt.total_cost if pt and ev.triggered else None,
                )

    if not summary.pass_at_k:
        best = summary.best
        ev = best.evaluation
        message = (
            f"KDA skill assertion failed. strict_pass={ev.strict_pass} "
            f"(triggered={ev.triggered}, executed={ev.executed}, "
            f"success={ev.success}, turn_completed={ev.turn_completed}). "
            f"Actual create args: {best.actual_create_args}. "
            f"Actual execute result: {best.actual_execute_result}."
        )
        exc = KdaSkillAssertionError(message)
        exc.reasoning_steps = best.reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = best.response_id
        exc.detail = {
            "triggered": ev.triggered,
            "executed": ev.executed,
            "success": ev.success,
            "turn_completed": ev.turn_completed,
            "disambiguated": ev.disambiguated,
            "actual_create_args": best.actual_create_args,
            "actual_execute_result": best.actual_execute_result,
        }
        raise exc
    best = summary.best
    ev = best.evaluation
    return AgenticEvalOutcome(
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail={
            "triggered": ev.triggered,
            "executed": ev.executed,
            "success": ev.success,
            "turn_completed": ev.turn_completed,
            "disambiguated": ev.disambiguated,
            "actual_create_args": best.actual_create_args,
            "actual_execute_result": best.actual_execute_result,
        },
    )
