# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic metric-skill evaluation runner."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any

from gooddata_sdk import GoodDataSdk

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.models import ToolCallEvent

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI: Any = None

_DEFAULT_K = 1
_DEFAULT_MAX_ITERATIONS = 7

_IFNULL_RE = re.compile(r"IFNULL\s*\([^,]+,\s*0\)", re.IGNORECASE)
_SELECT_WRAP_RE = re.compile(r"^\s*\(\s*SELECT\s*\{([^}]+)\}\s*\)\s*$", re.IGNORECASE)
_INNER_SELECT_RE = re.compile(r"\(\s*SELECT\s*\{([^}]+)\}\s*\)", re.IGNORECASE)


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


def _normalize_maql(maql: str) -> str:
    """Semantic normalisation: strip whitespace, unwrap IFNULL/SELECT wrappers."""
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
    return m.strip()


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


def generate_simulated_response(agent_message: str, expected_output: dict) -> str:
    """Generate a user reply to keep the metric-skill conversation going (gpt-4o-mini)."""
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError("openai package is required for generate_simulated_response") from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise OSError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)
    expected_maql = expected_output.get("maql", "")
    prompt = (
        f"You are simulating a user in a conversation with a BI assistant that creates metrics. "
        f"The assistant said: '{agent_message}'. "
        f"The user originally asked to create a metric with MAQL: {expected_maql}. "
        f"Reply briefly as the user, providing any clarification the assistant needs."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
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


@dataclass
class AgenticMetricSummary:
    """Aggregated outcome of K runs for metric creation."""

    run_results: list[MetricRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: MetricRunResult


def _extract_metric_result(tool_call_events: list[ToolCallEvent]) -> dict | None:
    for tc in tool_call_events:
        if tc.function_name == "create_metric" and tc.result:
            result_data = tc.parsed_result()
            if result_data is not None:
                return result_data.get("data", result_data)
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


def _is_asking_clarification(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return "?" in t or "could you" in t or "please provide" in t or "clarif" in t


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
    primary_expected = expected_outputs[0] if expected_outputs else {}
    metric_result: dict | None = None
    metric_id_to_delete: str | None = None
    turns = 0
    current_question = question

    try:
        for _iteration in range(max_iterations):
            turns += 1
            chat_result = client.send_message(conversation_id, current_question)
            candidate = _extract_metric_result(chat_result.tool_call_events or [])
            if candidate is not None:
                metric_result = candidate
                metric_id_to_delete = candidate.get("metric_id")
                break
            response_text = (chat_result.text_response or "").strip()
            if _is_asking_clarification(response_text):
                current_question = generate_simulated_response(response_text, primary_expected)
            else:
                break

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
        )
    finally:
        if metric_id_to_delete:
            _delete_metric(sdk, workspace_id, metric_id_to_delete)


def run_agentic_metric_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict | list,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
) -> AgenticMetricSummary:
    """Run the metric-skill agentic evaluation K times and return a summary.

    ``expected_output`` may be a single candidate dict or a list of candidate dicts.
    The run passes when the actual MAQL matches any candidate after normalisation.
    """
    expected_outputs: list[dict] = expected_output if isinstance(expected_output, list) else [expected_output]
    run_results: list[MetricRunResult] = []
    client = ChatClient(host=host, token=token, workspace_id=workspace_id)
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


class MetricSkillAssertionError(AssertionError):
    """Raised when a metric-skill evaluation fails."""

    __tracebackhide__ = True


def evaluate_agentic_metric_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict | list,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "metric_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
) -> None:
    """Run metric-skill evaluation, log to Langfuse, and raise MetricSkillAssertionError on failure."""
    from datetime import datetime as _dt  # noqa: PLC0415
    from datetime import timezone as _tz  # noqa: PLC0415

    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    if langfuse is None:
        langfuse = try_make_langfuse_client()
    window_start = _dt.now(_tz.utc)
    summary = run_agentic_metric_skill(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_output=expected_output,
        k=k,
        max_iterations=max_iterations,
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
            run_metadata_extra,
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
                score_safe(langfuse, tid, name="metric_created", value=float(run.metric_created), data_type="BOOLEAN")
                score_safe(langfuse, tid, name="maql_correct", value=float(run.maql_correct), data_type="BOOLEAN")
                log_quality_and_value_scores(
                    langfuse,
                    tid,
                    strict_checks={"metric_created": run.metric_created, "maql_correct": run.maql_correct},
                    latency_sec=pt.latency if pt else None,
                    cost_usd=pt.total_cost if pt else None,
                )

    if not summary.pass_at_k:
        best = summary.best
        expected_outputs_list: list[dict] = expected_output if isinstance(expected_output, list) else [expected_output]
        candidates_str = "; ".join(repr(c.get("maql", "")) for c in expected_outputs_list)
        raise MetricSkillAssertionError(
            f"Metric skill assertion failed. "
            f"metric_created={best.metric_created}, maql_correct={best.maql_correct}. "
            f"Expected MAQL (candidates): {candidates_str}. "
            f"Actual MAQL: {best.actual_maql}."
        )
