# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic general-question evaluation runner."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

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
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError, LLMJudge, score_run
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ReasoningStepEvent,
    ToolCallEvent,
    build_latency_breakdown,
)
from gooddata_eval.core.timing import PhaseTimings, log_timer, sum_timings

_DEFAULT_K = 1

_GENERAL_QUESTION_EVALUATION_STEPS: list[str] = [
    (
        "Read the EXPECTED OUTPUT carefully. It describes what a correct response to the INPUT should convey — "
        "this may include specific facts, figures, key concepts, or analytical conclusions. "
        "Use it as the ground truth for evaluation."
    ),
    (
        "Check that the ACTUAL OUTPUT genuinely attempts to answer the question. "
        "Return FAIL (0) if the chatbot refuses, says it cannot answer, or deflects a legitimate analytical question."
    ),
    (
        "Check whether the key facts, figures, or concepts described in the EXPECTED OUTPUT "
        "are present and correctly represented in the ACTUAL OUTPUT. "
        "Exact wording is not required — focus on conceptual and factual alignment. "
        "Return FAIL (0) if important information from the EXPECTED OUTPUT is missing or contradicted."
    ),
    (
        "Do not penalize the chatbot for providing additional relevant context, richer explanations, "
        "or different but equivalent phrasing. "
        "Focus only on whether the core answer aligns with the EXPECTED OUTPUT."
    ),
    (
        "If the ACTUAL OUTPUT is empty, null, or contains only an error message unrelated to the question, "
        "return FAIL (0)."
    ),
    (
        "Return PASS (1) if the chatbot's response is factually and conceptually aligned with the EXPECTED OUTPUT. "
        "Return FAIL (0) otherwise."
    ),
]


@dataclass
class GeneralQuestionResult:
    """Outcome of one K-run conversation for a general question."""

    conversation_id: str
    actual_output: str
    passed: bool
    llm_judge_score: float
    reasoning: str
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    timings: PhaseTimings = field(default_factory=PhaseTimings)
    # Set when the judge returned something unreadable for THIS run. Such a run is
    # excluded from pass@K and from Langfuse scoring rather than counted as a failure:
    # scoring it 0 would publish a verdict the judge never gave.
    judge_error: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)


@dataclass
class AgenticGeneralQuestionSummary:
    """Aggregated outcome of K runs for a general question evaluation."""

    run_results: list[GeneralQuestionResult]
    pass_at_k: bool
    pass_power_k: bool
    best: GeneralQuestionResult

    @property
    def scored_run_results(self) -> list[GeneralQuestionResult]:
        """The runs the judge actually graded -- the only ones pass@K may consider."""
        return [r for r in self.run_results if r.judge_error is None]

    @property
    def judge_errors(self) -> list[str]:
        """One message per run the judge could not grade."""
        return [r.judge_error for r in self.run_results if r.judge_error is not None]


def _run_single_general_question(
    client: ChatClient,
    judge: LLMJudge,
    conversation_id: str,
    question: str,
    expected_output: str,
    user_context: dict | None = None,
) -> GeneralQuestionResult:
    item_started = time.monotonic()
    agent_started = time.monotonic()
    chat_result = client.send_message(conversation_id, question, user_context=user_context)
    actual_output = (chat_result.text_response or "").strip()
    agent_elapsed = time.monotonic() - agent_started
    log_timer(
        f"[timer] general_question {conversation_id} GoodData response complete after "
        f"{agent_elapsed:.2f}s; waiting for {judge.model} judge"
    )

    judge_started = time.monotonic()
    verdict = score_run(judge, input=question, expected_output=expected_output, actual_output=actual_output)
    judge_elapsed = time.monotonic() - judge_started
    total_elapsed = time.monotonic() - item_started
    log_timer(
        f"[timer] general_question {conversation_id} {judge.model} judge complete after "
        f"{judge_elapsed:.2f}s; item total {total_elapsed:.2f}s"
    )
    return GeneralQuestionResult(
        conversation_id=conversation_id,
        actual_output=actual_output,
        passed=verdict.passed,
        llm_judge_score=1.0 if verdict.passed else 0.0,
        reasoning=verdict.reasoning,
        reasoning_steps=list(chat_result.reasoning_steps or []),
        response_id=chat_result.response_id,
        # Derived from the elapsed values the [timer] lines above already computed, so
        # recording them adds no extra clock reads. Recorded on the unscored path too: the
        # agent still answered, and that measurement is the one worth keeping.
        timings=PhaseTimings(agent_s=agent_elapsed, judge_s=judge_elapsed),
        judge_error=verdict.error,
        tool_call_events=list(chat_result.tool_call_events or []),
        reasoning_step_events=list(chat_result.reasoning_step_events or []),
    )


def run_agentic_general_question(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: str,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    agent_id: str | None = None,
    user_context: dict | None = None,
) -> AgenticGeneralQuestionSummary:
    """Run the general-question agentic evaluation K times and return a summary."""
    run_results: list[GeneralQuestionResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    judge = LLMJudge(_GENERAL_QUESTION_EVALUATION_STEPS)

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(
                _run_single_general_question(client, judge, conv_id_0, question, expected_output, user_context)
            )
        finally:
            if initial_conversation_id is None:
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(
                    _run_single_general_question(client, judge, conv_id, question, expected_output, user_context)
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    # The two aggregates treat an ungraded run differently, on purpose. pass@K asks "did
    # any run pass", which an ungraded run cannot change, so it is excluded. pass^K claims
    # every run passed, which one ungraded run leaves unverified, so it is False. With
    # nothing graded at all there is no verdict either way and this raises.
    scored = [r for r in run_results if r.judge_error is None]
    pass_at_k = any(r.passed for r in scored)
    pass_power_k = len(scored) == len(run_results) and bool(scored) and all(r.passed for r in scored)
    best = max(scored or run_results, key=lambda r: r.llm_judge_score)
    return AgenticGeneralQuestionSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class GeneralQuestionAssertionError(AgenticAssertionError):
    """Raised when a general-question evaluation fails."""


def evaluate_agentic_general_question(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: str,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    agent_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "general_question",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    user_context: dict | None = None,
) -> AgenticEvalOutcome:
    """Run general-question evaluation, log to Langfuse, and raise GeneralQuestionAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as ``.reasoning_steps``/``.conversation_id``/``.response_id``.
    """
    langfuse, window_start = open_trace_window(langfuse)
    summary = run_agentic_general_question(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_output=expected_output,
        k=k,
        initial_conversation_id=initial_conversation_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=user_context,
    )

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:

            for run_idx, run in enumerate(summary.run_results):
                if run.judge_error is not None:
                    # No verdict for this run: float(run.passed) would write a 0 the judge
                    # never returned.
                    continue
                pt = ctx.trace(run.conversation_id)
                with ctx.observe(pt, run_idx) as tid:
                    ctx.score(tid, name="general_question_pass", value=float(run.passed), data_type="BOOLEAN")
                    ctx.score(tid, name="llm_judge_score", value=run.llm_judge_score, data_type="NUMERIC")
                    ctx.quality(
                        tid,
                        strict_checks={"general_question_pass": run.passed},
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
            # Ungraded runs are skipped above, so polling for their traces would only spend
            # the item's shared retry budget on scores that never get written.
            conversation_ids=[r.conversation_id for r in summary.scored_run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=len(summary.run_results) > 1,
            write_scores=_write_scores,
        )

    item_timings = sum_timings([r.timings for r in summary.run_results])
    unscored = summary.judge_errors

    if not summary.scored_run_results:
        # Not one run produced a readable verdict, so this item has no result -- an error,
        # not K failures. Raised after the trace link is queued so whatever the agent did
        # is still linked, and carrying the timings so the runner can report what the item
        # cost before it became unevaluable.
        exc = JudgeResponseError(
            f"judge returned no readable verdict for any of the {len(summary.run_results)} run(s): "
            + " | ".join(unscored)
        )
        exc.timings = item_timings
        raise exc

    runs_passed = sum(1 for r in summary.scored_run_results if r.passed)
    runs_effective = len(summary.run_results)

    best = summary.best
    detail = {
        "judge_passed": best.passed,
        "judge_reasoning": best.reasoning,
        "actual_output": best.actual_output,
        "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
        # Only present when it happened, so the usual JSON shape is unchanged. A
        # pass@K computed over fewer runs than --runs asked for is a weaker result and
        # the report has to say so.
        **({"unscored_runs": len(unscored), "judge_errors": unscored} if unscored else {}),
    }

    if not summary.pass_at_k:
        exc = GeneralQuestionAssertionError(
            f"General question assertion failed. passed={best.passed}. Reasoning: {best.reasoning}"
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
