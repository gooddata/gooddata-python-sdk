# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic general-question evaluation runner."""

from __future__ import annotations

from dataclasses import dataclass

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.evaluators._llm_judge import LLMJudge

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


@dataclass
class AgenticGeneralQuestionSummary:
    """Aggregated outcome of K runs for a general question evaluation."""

    run_results: list[GeneralQuestionResult]
    pass_at_k: bool
    pass_power_k: bool
    best: GeneralQuestionResult


def run_agentic_general_question(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: str,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
) -> AgenticGeneralQuestionSummary:
    """Run the general-question agentic evaluation K times and return a summary."""
    run_results: list[GeneralQuestionResult] = []
    client = ChatClient(host=host, token=token, workspace_id=workspace_id)
    judge = LLMJudge(_GENERAL_QUESTION_EVALUATION_STEPS, model="gpt-4o")

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            chat_result = client.send_message(conv_id_0, question)
            actual_output = (chat_result.text_response or "").strip()
            passed, reasoning = judge.score(
                input=question, expected_output=expected_output, actual_output=actual_output
            )
            llm_judge_score = 1.0 if passed else 0.0
            run_results.append(
                GeneralQuestionResult(
                    conversation_id=conv_id_0,
                    actual_output=actual_output,
                    passed=passed,
                    llm_judge_score=llm_judge_score,
                    reasoning=reasoning,
                )
            )
        finally:
            if initial_conversation_id is None:
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                chat_result = client.send_message(conv_id, question)
                actual_output = (chat_result.text_response or "").strip()
                passed, reasoning = judge.score(
                    input=question, expected_output=expected_output, actual_output=actual_output
                )
                llm_judge_score = 1.0 if passed else 0.0
                run_results.append(
                    GeneralQuestionResult(
                        conversation_id=conv_id,
                        actual_output=actual_output,
                        passed=passed,
                        llm_judge_score=llm_judge_score,
                        reasoning=reasoning,
                    )
                )
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    pass_at_k = any(r.passed for r in run_results)
    pass_power_k = all(r.passed for r in run_results)
    best = max(run_results, key=lambda r: r.llm_judge_score)
    return AgenticGeneralQuestionSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class GeneralQuestionAssertionError(AssertionError):
    """Raised when a general-question evaluation fails."""

    __tracebackhide__ = True


def evaluate_agentic_general_question(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: str,
    k: int = _DEFAULT_K,
    initial_conversation_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "general_question",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
) -> None:
    """Run general-question evaluation, log to Langfuse, and raise on failure."""
    from datetime import datetime as _dt, timezone as _tz  # noqa: PLC0415
    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    if langfuse is None:
        langfuse = try_make_langfuse_client()
    window_start = _dt.now(_tz.utc)
    summary = run_agentic_general_question(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_output=expected_output,
        k=k,
        initial_conversation_id=initial_conversation_id,
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
        )
        traces_by_conv = find_traces_per_conversation(
            langfuse,
            [r.conversation_id for r in summary.run_results],
            window_start,
        )
        suffix_needed = len(summary.run_results) > 1
        for run_idx, run in enumerate(summary.run_results):
            pt = traces_by_conv.get(run.conversation_id)
            run_name = f"{run_name_base}_run{run_idx}" if suffix_needed else run_name_base
            with observe(langfuse, pt.id if pt else None, dataset_item_id, run_name, run_metadata) as tid:
                score_safe(langfuse, tid, name="general_question_pass", value=float(run.passed), data_type="BOOLEAN")
                score_safe(langfuse, tid, name="llm_judge_score", value=run.llm_judge_score, data_type="NUMERIC")
                log_quality_and_value_scores(
                    langfuse,
                    tid,
                    strict_checks={"general_question_pass": run.passed},
                    latency_sec=pt.latency if pt else None,
                    cost_usd=pt.total_cost if pt else None,
                )

    if not summary.pass_at_k:
        best = summary.best
        raise GeneralQuestionAssertionError(
            f"General question assertion failed. passed={best.passed}. Reasoning: {best.reasoning}"
        )
