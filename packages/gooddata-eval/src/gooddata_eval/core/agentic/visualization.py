# (C) 2026 GoodData Corporation
"""Full agentic visualization evaluation loop — multi-turn, K-runs, simulated user.

Ported from gdc-nas tavern-e2e app/vis_agentic.py.
Langfuse logging and VisAssertionError remain in the Tavern shim.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.evaluators.visualization import (
    EvaluationResult,
    _check_visualization_skill_activated,
    _evaluate_against_candidates,
)
from gooddata_eval.core.models import CreatedVisualization, ToolCallEvent
from gooddata_eval.core.scoring import get_dimension_uri_set, get_metric_uri_set, uri_to_display_name

_DEFAULT_K = 2
_DEFAULT_MAX_ITERATIONS = 4


@dataclass
class RunResult:
    """Outcome of one K-run conversation."""

    conversation_id: str
    actual_output: CreatedVisualization | None
    eval_result: EvaluationResult
    best_expected: CreatedVisualization
    total_turns: float
    total_steps: float


@dataclass
class AgenticRunSummary:
    """Aggregated outcome of all K runs for one dataset item."""

    run_results: list[RunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: RunResult


def generate_simulated_response(agent_message: str, expected_output: CreatedVisualization) -> str:
    """Generate a simulated user reply to an agent clarification question.

    Uses OpenAI gpt-5.2 to produce a realistic reply that guides the agent
    toward the expected visualization without revealing the answer directly.
    Requires the [llm-judge] extra: pip install gooddata-eval[llm-judge]
    """
    try:
        from openai import OpenAI  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError(
            "openai is required for multi-turn agentic evaluation. "
            "Install the [llm-judge] extra: pip install 'gooddata-eval[llm-judge]'"
        ) from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise OSError("OPENAI_API_KEY environment variable is required for multi-turn agentic evaluation.")
    client = OpenAI(api_key=api_key)

    metric_uris = sorted(get_metric_uri_set(expected_output))
    dim_uris = sorted(get_dimension_uri_set(expected_output))
    viz_type_str = expected_output.type or "not specified"
    metrics_str = ", ".join(uri_to_display_name(u) for u in metric_uris) or "not specified"
    dimensions_str = ", ".join(uri_to_display_name(u) for u in dim_uris) or "not specified"

    filter_parts: list[str] = []
    for filter_dict in expected_output.query.filter_by.values():
        ft = filter_dict.get("type", "")
        if ft == "date_filter":
            granularity = filter_dict.get("granularity", "")
            from_val = filter_dict.get("from", "")
            to_val = filter_dict.get("to", "")
            filter_parts.append(
                f"date filter: {granularity} from {from_val} to {to_val}"
                if granularity
                else f"date filter: {from_val} to {to_val}"
            )
        elif ft == "ranking_filter":
            n = filter_dict.get("top") or filter_dict.get("bottom")
            direction = "top" if "top" in filter_dict else "bottom"
            filter_parts.append(f"{direction} {n}")
        elif ft == "attribute_filter":
            state = filter_dict.get("state", {})
            include = state.get("include")
            exclude = state.get("exclude")
            field_uri = filter_dict.get("using", "")
            field_name = uri_to_display_name(field_uri)
            if include is not None:
                filter_parts.append(f"{field_name} include {include}")
            elif exclude is not None:
                filter_parts.append(f"{field_name} exclude {exclude}")
    filters_str = ", ".join(filter_parts) or "not specified"

    has_date_filter = any(f.get("type") == "date_filter" for f in expected_output.query.filter_by.values())
    has_attribute_filter = any(f.get("type") == "attribute_filter" for f in expected_output.query.filter_by.values())
    no_filter_hints: list[str] = []
    if not has_date_filter:
        no_filter_hints.append(
            "If the agent asks about a time period or date filter, say you want all-time data with no date filter."
        )
    if not has_attribute_filter:
        no_filter_hints.append(
            "If the agent asks about filtering by any attribute (e.g. order status, category, region), "
            "say you do not need any attribute filter — show data for all values."
        )
    no_filter_hint = (" " + " ".join(no_filter_hints)) if no_filter_hints else ""

    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a user requesting data visualization from an AI agent. "
                    "The agent may ask clarifying questions to better understand your request. "
                    "Respond naturally and helpfully to their questions."
                ),
            },
            {
                "role": "user",
                "content": (
                    f'The agent asked: "{agent_message}"\n\n'
                    f"Your goal is to get a visualization with:\n"
                    f"- Metrics: {metrics_str}\n"
                    f"- Dimensions: {dimensions_str}\n"
                    f"- Filters: {filters_str}\n"
                    f"- Visualization type: {viz_type_str}\n\n"
                    f"Respond naturally to the agent's question. Be helpful and answer what they're asking about.\n"
                    f"If the agent asks specifically about items from your goal (like which metrics or dimensions "
                    f"you want), you should mention them. Keep your response concise and natural, as a real user would."
                    f"{no_filter_hint}"
                ),
            },
        ],
        temperature=0.5,
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


def _execute_single_run(
    client: ChatClient,
    conversation_id: str,
    question: str,
    expected_outputs: list[CreatedVisualization],
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
) -> RunResult:
    """Drive one full multi-turn conversation and evaluate the result."""
    total_turns = 0.0
    total_steps = 0.0
    all_tool_call_events: list[ToolCallEvent] = []
    simulated_response_guide = expected_outputs[0]  # primary candidate guides the simulated user

    current_result = client.send_message(conversation_id, question)

    for iteration in range(max_iterations):
        total_turns += 1.0
        total_steps += float(current_result.reasoning_step_count)
        all_tool_call_events.extend(current_result.tool_call_events)

        viz_produced = bool(current_result.created_visualizations and current_result.created_visualizations.objects)
        if viz_produced:
            break
        if not current_result.text_response:
            break
        if iteration >= max_iterations - 1:
            break

        follow_up = generate_simulated_response(current_result.text_response, simulated_response_guide)
        current_result = client.send_message(conversation_id, follow_up)

    skill_activated = _check_visualization_skill_activated(all_tool_call_events)
    actual_output: CreatedVisualization | None = None
    if current_result.created_visualizations and current_result.created_visualizations.objects:
        actual_output = current_result.created_visualizations.objects[0]

    eval_result, best_expected = _evaluate_against_candidates(expected_outputs, actual_output, skill_activated)

    return RunResult(
        conversation_id=conversation_id,
        actual_output=actual_output,
        eval_result=eval_result,
        best_expected=best_expected,
        total_turns=total_turns,
        total_steps=total_steps,
    )


def run_agentic_visualization(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_outputs: list[CreatedVisualization],
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
) -> AgenticRunSummary:
    """Run K independent conversations and return evaluation results.

    If initial_conversation_id is provided, Run 0 reuses that conversation
    (e.g. one created by a Tavern YAML POST). Subsequent runs always create
    fresh conversations. Caller-supplied conversations are not deleted; all
    conversations created by this function are deleted on completion.
    """
    client = ChatClient(host=host, token=token, workspace_id=workspace_id)
    run_results: list[RunResult] = []

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(_execute_single_run(client, conv_id_0, question, expected_outputs, max_iterations))
        finally:
            if initial_conversation_id is None:
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(_execute_single_run(client, conv_id, question, expected_outputs, max_iterations))
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    pass_at_k = any(r.eval_result.strict_pass for r in run_results)
    pass_power_k = all(r.eval_result.strict_pass for r in run_results)
    best = max(run_results, key=lambda r: (r.eval_result.strict_pass, r.eval_result.strict_checks_passed_count))

    return AgenticRunSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class VisualizationAssertionError(AssertionError):
    """Raised when a visualization evaluation fails."""

    __tracebackhide__ = True


def evaluate_agentic_visualization(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_outputs: list[CreatedVisualization],
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "visualization",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    record_output_path: str | None = None,
) -> None:
    """Run visualization evaluation, log to Langfuse, and raise VisualizationAssertionError on failure."""
    import json as _json  # noqa: PLC0415
    from datetime import datetime as _dt  # noqa: PLC0415
    from datetime import timezone as _tz  # noqa: PLC0415

    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    if langfuse is None:
        langfuse = try_make_langfuse_client()
    window_start = _dt.now(_tz.utc)
    summary = run_agentic_visualization(
        host=host,
        token=token,
        workspace_id=workspace_id,
        question=question,
        expected_outputs=expected_outputs,
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
        )
        K = len(summary.run_results)
        traces_by_conv = find_traces_per_conversation(
            langfuse,
            [r.conversation_id for r in summary.run_results],
            window_start,
        )
        for run_idx, run in enumerate(summary.run_results):
            pt = traces_by_conv.get(run.conversation_id)
            ev = run.eval_result
            with observe(
                langfuse, pt.id if pt else None, dataset_item_id, f"{run_name_base}_run{run_idx}", run_metadata
            ) as tid:
                score_safe(
                    langfuse, tid, name="assertion-cross-ref-valid", value=ev.cross_ref_valid, data_type="BOOLEAN"
                )
                score_safe(langfuse, tid, name="assertion-vis-metric", value=ev.metrics_correct, data_type="BOOLEAN")
                score_safe(
                    langfuse, tid, name="assertion-vis-dimensions", value=ev.dimensions_correct, data_type="BOOLEAN"
                )
                score_safe(langfuse, tid, name="assertion-vis-filters", value=ev.filters_correct, data_type="BOOLEAN")
                score_safe(langfuse, tid, name="assertion-vis-type", value=ev.viz_type_hard, data_type="BOOLEAN")
                score_safe(langfuse, tid, name="skill_selection", value=ev.skill_activated, data_type="BOOLEAN")
                score_safe(langfuse, tid, name=f"pass_at_{K}", value=summary.pass_at_k, data_type="BOOLEAN")
                score_safe(langfuse, tid, name=f"pass_power_{K}", value=summary.pass_power_k, data_type="BOOLEAN")
                score_safe(langfuse, tid, name="turns", value=run.total_turns, data_type="NUMERIC")
                score_safe(langfuse, tid, name="steps", value=run.total_steps, data_type="NUMERIC")
                log_quality_and_value_scores(
                    langfuse,
                    tid,
                    strict_checks={
                        "assertion-cross-ref-valid": ev.cross_ref_valid,
                        "assertion-vis-metric": ev.metrics_correct,
                        "assertion-vis-dimensions": ev.dimensions_correct,
                        "assertion-vis-filters": ev.filters_correct,
                        "assertion-vis-type": ev.viz_type_hard,
                    },
                    latency_sec=pt.latency if pt else None,
                    cost_usd=pt.total_cost if pt else None,
                )

    if record_output_path and summary.best.actual_output is not None:
        import json as _j  # noqa: PLC0415

        with open(record_output_path) as _f:
            _fixture = _j.load(_f)
        _fixture["actual_output"] = {"visualization": summary.best.actual_output.model_dump(exclude_none=True)}
        with open(record_output_path, "w") as _f:
            _j.dump(_fixture, _f, indent=2)

    if not summary.pass_at_k:
        best = summary.best
        ev = best.eval_result
        n = len(expected_outputs)
        candidate_note = f" (closest of {n} candidates)" if n > 1 else ""
        cross_ref_detail = (" → " + "; ".join(ev.cross_ref_errors)) if ev.cross_ref_errors else ""
        expected_dump = best.best_expected.model_dump(exclude_none=True)
        actual_dump = best.actual_output.model_dump(exclude_none=True) if best.actual_output else None
        raise VisualizationAssertionError(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Agentic Visualization Assertion Failed! (Critical Mode)\n"
            "------------------------------------------\n"
            f"Question:\n{question}\n"
            "------------------------------------------\n"
            f"Expected Output{candidate_note}:\n{_json.dumps(expected_dump, indent=2)}\n"
            "------------------------------------------\n"
            f"Actual Output:\n{_json.dumps(actual_dump, indent=2)}\n"
            "------------------------------------------\n"
            "Strict Check Summary:\n"
            f"  Visualization Created : {ev.visualization_created}\n"
            f"  Cross-Ref Valid       : {ev.cross_ref_valid}{cross_ref_detail}\n"
            f"  Metrics Correct       : {ev.metrics_correct}\n"
            f"    expected : {sorted(ev.expected_metric_uris)}\n"
            f"    actual   : {sorted(ev.actual_metric_uris)}\n"
            f"  Dimensions Correct    : {ev.dimensions_correct}\n"
            f"    expected : {sorted(ev.expected_dim_uris)}\n"
            f"    actual   : {sorted(ev.actual_dim_uris)}\n"
            f"  Filters Correct       : {ev.filters_correct}\n"
            f"    date      : {ev.filter_date_score}\n"
            f"    ranking   : {ev.filter_ranking_score}\n"
            f"    attribute : {ev.filter_attribute_score}\n"
            f"  Viz Type Hard         : {ev.viz_type_hard}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
