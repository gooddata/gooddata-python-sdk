# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic conversation evaluation runner (multi-turn, multi-skill)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.models import ChatResult, ToolCallEvent
from gooddata_eval.core.scoring import (
    check_filters,
    check_viz_type,
    get_dimension_uri_set,
    get_metric_uri_set,
)

_REF_PATTERN = re.compile(r"\$ref:([\w_]+)\.([\w_]+)")

_DASHBOARD_SUMMARY_EVALUATION_STEPS: list[str] = [
    (
        "Read the EXPECTED OUTPUT carefully. It describes which analytical insights a correct "
        "dashboard summary should cover across all the dashboard's visualizations."
    ),
    (
        "Check that the ACTUAL OUTPUT provides a genuine business-level summary — not just a "
        "list of chart titles or axis labels."
    ),
    (
        "Check that the key insights described in the EXPECTED OUTPUT are present and "
        "correctly represented in the ACTUAL OUTPUT. Exact wording is not required."
    ),
    (
        "Return FAIL (0) if the response refuses to summarize, produces only chart mechanics, "
        "or misses the key insights listed in the EXPECTED OUTPUT."
    ),
    (
        "Return PASS (1) if the summary is factually aligned with the EXPECTED OUTPUT criteria "
        "and provides genuine analytical insight about the dashboard's data."
    ),
]

_VIZ_SUMMARY_EVALUATION_STEPS: list[str] = [
    (
        "Read the EXPECTED OUTPUT carefully. It describes which analytical insights a correct "
        "summary should cover (e.g. top performers, trends, comparisons, outliers)."
    ),
    (
        "Check that the ACTUAL OUTPUT provides a genuine business-level summary — not just a "
        "description of chart mechanics, axis labels, or metadata."
    ),
    (
        "Check that the key insights described in the EXPECTED OUTPUT are present and "
        "correctly represented in the ACTUAL OUTPUT. Exact wording is not required."
    ),
    (
        "Return FAIL (0) if the response refuses to summarize, produces only chart mechanics, "
        "or misses the key insights listed in the EXPECTED OUTPUT."
    ),
    (
        "Return PASS (1) if the summary is factually aligned with the EXPECTED OUTPUT criteria "
        "and provides genuine analytical insight about the data."
    ),
]


class TurnDefinition(BaseModel):
    """Definition of a single turn in a multi-turn conversation evaluation."""

    turn_id: str
    message: str
    expected_skill: str
    expected_output_type: Literal["visualization", "tool_call", "metric", "alert", "visualization_summary", "search", "dashboard_summary", "key_driver_analysis", "what_if_analysis", "anomaly_detection", "clustering", "forecasting"] = "visualization"
    expected_tool_name: str | None = None
    expected_output: dict | None = None


class ConversationFixture(BaseModel):
    """A complete multi-turn conversation test fixture."""

    id: str
    dataset_name: str = "conversation"
    expected_skills: list[str]
    turns: list[TurnDefinition]
    workspace_id: str | None = None
    category: str | None = None


class TurnResult(BaseModel):
    """Evaluation result for a single conversation turn."""

    turn_id: str
    turn_index: int = 0
    expected_skill: str
    skill_routing: bool
    output_present: bool
    no_error: bool
    activated_skills: list[str]
    all_tool_calls: list[str] = []
    text_response: str | None = None
    clarification_turns_used: int = 0
    output_correct: bool | None = None

    @property
    def skill_success(self) -> bool:
        # Turn 0 must explicitly route via set_skills (strict).
        # Follow-up turns: if the expected output is present the model is
        # implicitly carrying the skill from the prior turn — consistent with
        # how ToolSandbox and COMPASS evaluate stateful multi-turn conversations.
        if self.turn_index == 0:
            return self.skill_routing and self.output_present and self.no_error
        return self.output_present and self.no_error


def _resolve_refs(
    expected_output: dict | None,
    turn_outputs: dict[str, dict],
) -> dict | None:
    """Resolve $ref:turn_id.field placeholders from prior turn outputs.

    Works on the JSON-serialised form so nested values (e.g. URI strings) are
    also resolved.  Raises ValueError when a referenced turn or field is absent.
    """
    if not expected_output:
        return expected_output

    raw = json.dumps(expected_output)
    if "$ref:" not in raw:
        return expected_output

    def _replace(match: re.Match) -> str:  # type: ignore[type-arg]
        turn_id, field = match.group(1), match.group(2)
        if turn_id not in turn_outputs:
            raise ValueError(
                f"Cannot resolve '$ref:{turn_id}.{field}': "
                f"turn '{turn_id}' has no captured output. "
                f"Available turns: {list(turn_outputs)}"
            )
        if field not in turn_outputs[turn_id]:
            raise ValueError(
                f"Cannot resolve '$ref:{turn_id}.{field}': "
                f"field '{field}' not found in turn '{turn_id}' output. "
                f"Available fields: {list(turn_outputs[turn_id])}"
            )
        return str(turn_outputs[turn_id][field])

    resolved_raw = _REF_PATTERN.sub(_replace, raw)
    return json.loads(resolved_raw)


def _activated_skills(tool_call_events: list[ToolCallEvent]) -> list[str]:
    """Collect all skill names passed to set_skills across all tool call events."""
    skills: list[str] = []
    for tc in tool_call_events:
        if tc.function_name != "set_skills":
            continue
        args = tc.parsed_arguments() or {}
        skills.extend(args.get("skill_names", []))
    return list(set(skills))


def _check_viz_skill_activated(chat_result: ChatResult, config_flag: str) -> bool:
    """Return True if create_adhoc_visualization was called with the given config flag set to True."""
    for tc in chat_result.tool_call_events or []:
        if tc.function_name != "create_adhoc_visualization":
            continue
        args = tc.parsed_arguments() or {}
        config = (args.get("visualization") or {}).get("config") or {}
        if config.get(config_flag):
            return True
    return False


def _check_viz_skill_metric(chat_result: ChatResult, config_flag: str, exp_metric: str) -> bool:
    """Return True if the visualization with config_flag=True used the expected metric."""
    for tc in chat_result.tool_call_events or []:
        if tc.function_name != "create_adhoc_visualization":
            continue
        args = tc.parsed_arguments() or {}
        viz = args.get("visualization") or {}
        if not (viz.get("config") or {}).get(config_flag):
            continue
        fields = (viz.get("query") or {}).get("fields") or {}
        for field_def in fields.values():
            if not isinstance(field_def, dict):
                continue
            using = field_def.get("using", "")
            metric_id = using.split("/", 1)[-1] if "/" in using else using
            if metric_id == exp_metric:
                return True
    return False


def _check_output_present(turn: TurnDefinition, chat_result: ChatResult) -> bool:
    otype = turn.expected_output_type
    if otype == "visualization":
        return bool(
            chat_result.created_visualizations
            and getattr(chat_result.created_visualizations, "objects", chat_result.created_visualizations)
        )
    if otype == "metric":
        return any(tc.function_name == "create_metric" for tc in (chat_result.tool_call_events or []))
    if otype == "alert":
        return any(tc.function_name == "create_metric_alert" for tc in (chat_result.tool_call_events or []))
    if otype == "visualization_summary":
        return bool(chat_result.text_response and chat_result.text_response.strip())
    if otype == "dashboard_summary":
        return bool(chat_result.text_response and chat_result.text_response.strip())
    if otype == "search":
        return any(tc.function_name == "search_objects" for tc in (chat_result.tool_call_events or []))
    if otype == "key_driver_analysis":
        return any(tc.function_name == "create_key_driver_analysis" for tc in (chat_result.tool_call_events or []))
    if otype == "what_if_analysis":
        return any(tc.function_name == "create_what_if_scenario" for tc in (chat_result.tool_call_events or []))
    if otype == "anomaly_detection":
        return _check_viz_skill_activated(chat_result, "anomaly_detection_enabled")
    if otype == "clustering":
        return _check_viz_skill_activated(chat_result, "clustering_enabled")
    if otype == "forecasting":
        return _check_viz_skill_activated(chat_result, "forecast_enabled")
    if otype == "tool_call":
        expected_tool = turn.expected_tool_name
        if not expected_tool:
            return bool(chat_result.tool_call_events)
        return any(tc.function_name == expected_tool for tc in (chat_result.tool_call_events or []))
    return False


def _extract_metric_from_turn(tool_call_events: list[ToolCallEvent]) -> dict | None:
    """Extract the result payload from the create_metric tool call, if present."""
    for tc in tool_call_events:
        if tc.function_name != "create_metric":
            continue
        if not tc.result:
            continue
        result_data = tc.parsed_result()
        if result_data is not None:
            return result_data.get("data", result_data)
    return None


def _check_output_correct(turn: TurnDefinition, chat_result: ChatResult) -> bool | None:
    """Check output correctness against expected_output when defined.

    Returns None when expected_output is absent (presence check only).
    """
    from gooddata_eval.core.agentic.metric_skill import _normalize_maql  # noqa: PLC0415

    otype = turn.expected_output_type
    expected = turn.expected_output
    if not expected:
        return None

    if otype == "visualization":
        from gooddata_eval.core.models import CreatedVisualization  # noqa: PLC0415

        vizzes = chat_result.created_visualizations
        if not vizzes:
            return False
        objects = getattr(vizzes, "objects", None)
        if not objects:
            return False
        viz = objects[0]
        results: list[bool] = []
        if "viz_type" in expected or "type" in expected:
            try:
                exp_viz = CreatedVisualization.model_validate(expected.get("visualization", expected))
                results.append(check_viz_type(exp_viz, viz))
            except Exception:
                pass
        if expected.get("metrics"):
            actual_uris = get_metric_uri_set(viz)
            results.append(all(m in actual_uris for m in expected["metrics"]))
        if expected.get("dimensions"):
            actual_uris = get_dimension_uri_set(viz)
            results.append(all(d in actual_uris for d in expected["dimensions"]))
        if "filters" in expected:
            try:
                exp_viz = CreatedVisualization.model_validate(expected.get("visualization", expected))
                results.append(check_filters(exp_viz, viz).all_ok)
            except Exception:
                pass
        return all(results) if results else None

    if otype == "metric":
        metric_result = _extract_metric_from_turn(chat_result.tool_call_events or [])
        if not metric_result:
            return False
        return _normalize_maql(metric_result.get("maql", "")) == _normalize_maql(expected.get("maql", ""))

    if otype == "alert":
        from gooddata_eval.core.agentic.alert_skill import (  # noqa: PLC0415
            _check_filters,
            _check_metric,
            _check_threshold,
            _check_trigger,
            _extract_alert_call,
            _normalize_expected_output,
        )

        _, actual_args, tool_called = _extract_alert_call(chat_result.tool_call_events or [])
        if not tool_called:
            return False
        exp_alert = _normalize_expected_output(expected)
        return all(
            [
                exp_alert.operator == actual_args.get("operator"),
                _check_threshold(exp_alert, actual_args),
                _check_trigger(exp_alert, actual_args),
                _check_filters(exp_alert, actual_args),
                _check_metric(exp_alert, actual_args),
            ]
        )

    if otype == "visualization_summary":
        rubric = expected.get("rubric") if isinstance(expected, dict) else None
        if not rubric:
            return None
        actual_text = (chat_result.text_response or "").strip()
        if not actual_text:
            return False
        from gooddata_eval.core.evaluators._llm_judge import LLMJudge  # noqa: PLC0415

        judge = LLMJudge(_VIZ_SUMMARY_EVALUATION_STEPS)
        passed, _ = judge.score(
            input=turn.message,
            expected_output=rubric,
            actual_output=actual_text,
        )
        return passed

    if otype == "dashboard_summary":
        rubric = expected.get("rubric") if isinstance(expected, dict) else None
        if not rubric:
            return None
        actual_text = (chat_result.text_response or "").strip()
        if not actual_text:
            return False
        from gooddata_eval.core.evaluators._llm_judge import LLMJudge  # noqa: PLC0415

        judge = LLMJudge(_DASHBOARD_SUMMARY_EVALUATION_STEPS)
        passed, _ = judge.score(
            input=turn.message,
            expected_output=rubric,
            actual_output=actual_text,
        )
        return passed

    if otype == "search":
        matching = [tc for tc in (chat_result.tool_call_events or []) if tc.function_name == "search_objects"]
        if not matching:
            return False
        exp_keywords = sorted(expected.get("keywords") or [])
        exp_types = sorted(expected.get("object_types") or [])
        return any(
            sorted((tc.parsed_arguments() or {}).get("keywords") or []) == exp_keywords
            and sorted((tc.parsed_arguments() or {}).get("object_types") or []) == exp_types
            for tc in matching
        )

    if otype == "key_driver_analysis":
        exp_metric = expected.get("metric_id")
        if not exp_metric:
            return None
        for tc in chat_result.tool_call_events or []:
            if tc.function_name != "create_key_driver_analysis":
                continue
            args = tc.parsed_arguments() or {}
            measure = args.get("measure") or {}
            if isinstance(measure, dict) and measure.get("id") == exp_metric:
                return True
        return False

    if otype == "what_if_analysis":
        exp_metric = expected.get("metric_id")
        if not exp_metric:
            return None
        for tc in chat_result.tool_call_events or []:
            if tc.function_name != "create_what_if_scenario":
                continue
            args = tc.parsed_arguments() or {}
            for scenario in args.get("scenarios") or []:
                for adj in (scenario.get("adjustments") or []):
                    if adj.get("metric_id") == exp_metric:
                        return True
        return False

    if otype in {"anomaly_detection", "clustering", "forecasting"}:
        exp_metric = expected.get("metric_id")
        if not exp_metric:
            return None
        config_flag = {
            "anomaly_detection": "anomaly_detection_enabled",
            "clustering": "clustering_enabled",
            "forecasting": "forecast_enabled",
        }[otype]
        return _check_viz_skill_metric(chat_result, config_flag, exp_metric)

    return None


def _is_asking_clarification(text: str) -> bool:
    """Return True when the agent response contains a question (awaiting user input).

    We only reach this check when no expected output was produced, so any "?"
    in the text reliably signals the model needs user guidance rather than
    being a rhetorical flourish inside an otherwise complete answer.
    """
    return bool(text) and "?" in text


def _get_sim_user_response(agent_message: str, turn: TurnDefinition, expected_output: dict | None) -> str:
    """Generate a simulated user reply to an agent clarification question."""
    otype = turn.expected_output_type
    if otype == "visualization" and expected_output:
        try:
            from gooddata_eval.core.agentic.visualization import generate_simulated_response  # noqa: PLC0415
            from gooddata_eval.core.models import CreatedVisualization  # noqa: PLC0415

            exp_viz = CreatedVisualization.model_validate(expected_output.get("visualization", expected_output))
            return generate_simulated_response(agent_message, exp_viz)
        except Exception:
            pass
    elif otype == "metric" and expected_output:
        try:
            from gooddata_eval.core.agentic.metric_skill import (  # noqa: PLC0415
                generate_simulated_response,
            )

            return generate_simulated_response(agent_message, expected_output)
        except Exception:
            pass
    elif otype in {"anomaly_detection", "clustering", "forecasting"}:
        metric_id = (expected_output or {}).get("metric_id")
        if not metric_id:
            m = re.search(r"\{metric/([^}]+)\}", agent_message)
            if m:
                metric_id = m.group(1)
        if metric_id:
            return f"Use {{metric/{metric_id}}}. Please proceed with that metric."
    elif otype in {"key_driver_analysis", "what_if_analysis"}:
        metric_id = (expected_output or {}).get("metric_id")
        date_attr = (expected_output or {}).get("date_attribute_id")
        if not metric_id:
            m = re.search(r"\{metric/([^}]+)\}", agent_message)
            if m:
                metric_id = m.group(1)
        parts = []
        if metric_id:
            parts.append(f"Use {{metric/{metric_id}}}.")
        if date_attr:
            parts.append(f"Use {{date_attribute/{date_attr}}} as the date dimension.")
            if date_attr.endswith(".year"):
                parts.append("Use 2025 as the analyzed year (comparing to 2024).")
        parts.append("Please proceed and complete the analysis without asking further questions.")
        return " ".join(parts)

    # Generic fallback: when expected_output is absent we cannot know which option
    # is correct, so instruct the agent to self-select the best match and proceed.
    # A vague "natural" reply here only prolongs clarification loops.
    return (
        "Please pick whichever option best matches my original request and proceed. "
        "Do not ask for further clarification."
    )


@dataclass
class ConversationResult:
    """Outcome of a multi-turn, multi-skill conversation evaluation."""

    conversation_id: str
    turn_results: list[TurnResult]
    full_skill_coverage: bool
    conversation_success: bool
    total_clarification_turns: int


def run_agentic_conversation(
    host: str,
    token: str,
    workspace_id: str,
    fixture: ConversationFixture,
    max_clarification_turns: int = 20,
    initial_conversation_id: str | None = None,
) -> ConversationResult:
    """Run a multi-turn, multi-skill conversation evaluation (no K-runs).

    A single conversation is used for all turns in the fixture.  Each turn may
    trigger up to *max_clarification_turns* additional rounds of simulated-user
    replies before the agent produces the expected output.
    """
    client = ChatClient(host=host, token=token, workspace_id=workspace_id)
    turn_results: list[TurnResult] = []
    turn_outputs: dict[str, dict] = {}
    total_clarification_turns = 0
    conversation_id: str = ""
    owns_conversation = False

    try:
        if initial_conversation_id is not None:
            conversation_id = initial_conversation_id
        else:
            conversation_id = client.create_conversation()
            owns_conversation = True

        for turn_index, turn in enumerate(fixture.turns):
            # Resolve $ref placeholders using outputs captured from prior turns.
            resolved_expected = _resolve_refs(turn.expected_output, turn_outputs)
            resolved_turn = turn.model_copy(update={"expected_output": resolved_expected})

            clarification_turns = 0
            all_tool_calls: list[ToolCallEvent] = []
            current_message = turn.message
            final_result: ChatResult | None = None

            for _iter in range(max_clarification_turns + 1):
                chat_result = client.send_message(conversation_id, current_message)
                final_result = chat_result
                all_tool_calls.extend(chat_result.tool_call_events or [])

                if _check_output_present(resolved_turn, chat_result):
                    break

                response_text = (chat_result.text_response or "").strip()
                if clarification_turns >= max_clarification_turns:
                    break
                clarification_turns += 1
                total_clarification_turns += 1
                if _is_asking_clarification(response_text):
                    current_message = _get_sim_user_response(response_text, resolved_turn, resolved_expected)
                else:
                    # Model produced no expected output and asked no question —
                    # nudge it to continue rather than stopping prematurely.
                    current_message = "Please proceed and complete the task."

            activated = _activated_skills(all_tool_calls)
            all_tool_call_names = [tc.function_name for tc in all_tool_calls]
            skill_routing = turn.expected_skill in activated if activated else False
            output_present = _check_output_present(resolved_turn, final_result) if final_result else False
            output_correct = (
                _check_output_correct(resolved_turn, final_result) if (final_result and output_present) else None
            )
            final_text = (final_result.text_response or "").strip() if final_result else None

            # Capture metric output for $ref resolution in subsequent turns.
            if final_result and turn.expected_output_type == "metric":
                metric_data = _extract_metric_from_turn(all_tool_calls)
                if metric_data:
                    turn_outputs[turn.turn_id] = metric_data

            turn_results.append(
                TurnResult(
                    turn_id=turn.turn_id,
                    turn_index=turn_index,
                    expected_skill=turn.expected_skill,
                    skill_routing=skill_routing,
                    output_present=output_present,
                    no_error=True,  # SDK raises on errors; reaching here means no critical error.
                    activated_skills=activated,
                    all_tool_calls=all_tool_call_names,
                    text_response=final_text,
                    clarification_turns_used=clarification_turns,
                    output_correct=output_correct,
                )
            )

    finally:
        if owns_conversation and conversation_id:
            client.delete_conversation(conversation_id)
        client.close()

    activated_all = {skill for tr in turn_results for skill in tr.activated_skills}
    full_skill_coverage = set(fixture.expected_skills).issubset(activated_all)
    conversation_success = all(tr.skill_success for tr in turn_results)

    return ConversationResult(
        conversation_id=conversation_id,
        turn_results=turn_results,
        full_skill_coverage=full_skill_coverage,
        conversation_success=conversation_success,
        total_clarification_turns=total_clarification_turns,
    )


class ConversationAssertionError(AssertionError):
    """Raised when a conversation evaluation fails."""

    __tracebackhide__ = True


def evaluate_agentic_conversation(
    host: str,
    token: str,
    workspace_id: str,
    fixture: ConversationFixture,
    max_clarification_turns: int = 20,
    initial_conversation_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "conversation",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
) -> None:
    """Run conversation evaluation, log to Langfuse, and raise on failure."""
    from datetime import datetime as _dt, timezone as _tz  # noqa: PLC0415
    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    if langfuse is None:
        langfuse = try_make_langfuse_client()
    window_start = _dt.now(_tz.utc)
    result = run_agentic_conversation(
        host=host,
        token=token,
        workspace_id=workspace_id,
        fixture=fixture,
        max_clarification_turns=max_clarification_turns,
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
            dataset_name or fixture.dataset_name,
            run_timestamp,
            model_version_override,
        )
        traces_by_conv = find_traces_per_conversation(
            langfuse,
            [result.conversation_id],
            window_start,
        )
        pt = traces_by_conv.get(result.conversation_id)
        with observe(langfuse, pt.id if pt else None, dataset_item_id, run_name_base, run_metadata) as tid:
            score_safe(
                langfuse,
                tid,
                name="conversation_success",
                value=float(result.conversation_success),
                data_type="BOOLEAN",
            )
            score_safe(
                langfuse, tid, name="full_skill_coverage", value=float(result.full_skill_coverage), data_type="BOOLEAN"
            )
            for tr in result.turn_results:
                score_safe(
                    langfuse,
                    tid,
                    name=f"turn_{tr.turn_id}_skill_success",
                    value=float(tr.skill_success),
                    data_type="BOOLEAN",
                )
            log_quality_and_value_scores(
                langfuse,
                tid,
                strict_checks={
                    "conversation_success": result.conversation_success,
                    "full_skill_coverage": result.full_skill_coverage,
                },
                latency_sec=pt.latency if pt else None,
                cost_usd=pt.total_cost if pt else None,
            )

    if not result.conversation_success:
        failed_turns = [tr for tr in result.turn_results if not tr.skill_success]
        raise ConversationAssertionError(
            f"Conversation assertion failed. "
            f"full_skill_coverage={result.full_skill_coverage}. "
            f"Failed turns: {[t.turn_id for t in failed_turns]}"
        )
