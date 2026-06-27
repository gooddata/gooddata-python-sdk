# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic alert-skill evaluation runner."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

from typing import Any

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.agentic._catalog import CatalogMetricAlert

from gooddata_eval.core.models import ToolCallEvent

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI: Any = None

_DEFAULT_K = 1
_DEFAULT_MAX_ITERATIONS = 6

_TRIGGER_DISPLAY_TO_API = {"Every time": "ALWAYS", "One time": "ONCE"}
_ALWAYS_TRIGGER_VALUES = {"Every time", "ALWAYS", "not specified"}


def _to_number(value: object) -> float | int | None:
    """Convert string/number to int or float, None on failure."""
    if value is None:
        return None
    try:
        f = float(str(value))
        return int(f) if f == int(f) else f
    except (ValueError, TypeError):
        return None


def _parse_metric_id(metric_display: str | None) -> str | None:
    if not metric_display:
        return None
    m = re.search(r"\(([^)]+)\)\s*$", metric_display)
    return m.group(1).strip() if m else None


def _parse_recipients(recipients_str: str | None) -> list[str] | None:
    if not recipients_str:
        return None
    return [r.strip() for r in recipients_str.replace(";", ",").split(",") if r.strip()]


def _deep_subset(expected: object, actual: object) -> bool:
    """Return True if expected is a recursive subset of actual."""
    if isinstance(expected, dict) and isinstance(actual, dict):
        exp_d: dict[Any, Any] = expected  # type: ignore[assignment]
        act_d: dict[Any, Any] = actual  # type: ignore[assignment]
        return all(k in act_d and _deep_subset(v, act_d[k]) for k, v in exp_d.items())
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return False
        return all(_deep_subset(e, a) for e, a in zip(expected, actual))
    return expected == actual


def _check_threshold(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    if expected.operator in ("BETWEEN", "NOT_BETWEEN"):
        exp_from = _to_number(expected.threshold_from)
        exp_to = _to_number(expected.threshold_to)
        act_from = _to_number(actual_args.get("from_value", actual_args.get("fromValue")))
        act_to = _to_number(actual_args.get("to_value", actual_args.get("toValue")))
        return exp_from == act_from and exp_to == act_to
    exp_thr = _to_number(expected.threshold)
    act_thr = _to_number(actual_args.get("threshold"))
    return exp_thr == act_thr


def _check_trigger(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    exp_trigger = expected.trigger
    act_trigger = actual_args.get("trigger", actual_args.get("triggerMode", "ALWAYS"))
    if exp_trigger in _ALWAYS_TRIGGER_VALUES:
        return act_trigger in {"ALWAYS", "Every time"}
    exp_api = _TRIGGER_DISPLAY_TO_API.get(exp_trigger, exp_trigger)
    act_api = _TRIGGER_DISPLAY_TO_API.get(act_trigger, act_trigger)
    return exp_api == act_api


def _check_filters(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    exp_filters = expected.filters
    act_filters = actual_args.get("filters", actual_args.get("attribute_filters"))
    if not exp_filters:
        return True
    if not act_filters:
        return False
    return _deep_subset(exp_filters, act_filters)


def _check_metric(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    if not expected.metric_id:
        return True
    act_metric_raw = actual_args.get("metric_id", actual_args.get("metricId", ""))
    act_metric = _parse_metric_id(str(act_metric_raw)) or str(act_metric_raw)
    return expected.metric_id == act_metric


def _check_recipients(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    if not expected.recipients:
        return True
    act_recip_raw = actual_args.get("recipients", actual_args.get("external_recipients"))
    if isinstance(act_recip_raw, str):
        # external_recipients is JSON-encoded (e.g. '["email@example.com"]')
        try:
            parsed = json.loads(act_recip_raw)
            act_recip = parsed if isinstance(parsed, list) else _parse_recipients(act_recip_raw)
        except (json.JSONDecodeError, ValueError):
            act_recip = _parse_recipients(act_recip_raw)
    elif isinstance(act_recip_raw, list):
        act_recip = act_recip_raw
    else:
        act_recip = []
    return set(expected.recipients) == set(act_recip or [])


def generate_simulated_alert_response(
    agent_message: str,
    expected: CatalogMetricAlert,
    conversation_history: list,
) -> str:
    """Stateful sim-user reply for alert-skill conversation (gpt-4o)."""
    if _OpenAI is None:
        raise RuntimeError(
            "openai package is required for generate_simulated_alert_response. "
            "Install the [llm-judge] extra: pip install 'gooddata-eval[llm-judge]'"
        )
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise OSError("OPENAI_API_KEY environment variable is not set")

    openai_client = _OpenAI(api_key=api_key)

    metric = expected.metric_id or "not specified"
    operator = expected.operator
    threshold = expected.threshold if expected.threshold is not None else "not specified"
    recipients = ", ".join(expected.recipients) if expected.recipients else "not specified"
    trigger = expected.trigger
    filters = expected.filters

    trigger_line = (
        f"5. Proactively tell the agent the trigger is '{trigger}' in your first reply.\n"
        if trigger not in _ALWAYS_TRIGGER_VALUES
        else ""
    )
    system_prompt = (
        "You are a user requesting creation of an alert for a metric from an AI agent. "
        "Respond naturally but always steer toward the exact values you were given.\n"
        "Rules you MUST follow:\n"
        f"1. Your goal: metric={metric}, operator={operator}, threshold={threshold}, "
        f"recipients={recipients}, trigger={trigger}" + (f", filters={filters}" if filters else "") + ".\n"
        "2. Never revert or change a decision that was already confirmed in a previous turn.\n"
        "3. If the agent shows a final summary and asks for confirmation, verify that the "
        "   recipients match your goal. If they differ, correct them. "
        "   Once recipients are correct, say 'Yes, please proceed to create the alert.'\n"
        "4. Proactively include your email recipient in your first reply. "
        "   Do not wait for the agent to ask — state it alongside the metric and condition answers.\n"
        + trigger_line
        + "Reply concisely and directly."
    )

    messages: list = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append(
        {"role": "user", "content": f'The agent asked: "{agent_message}"\n\nRespond concisely and directly.'}
    )
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content or ""


def _delete_alert(client: ChatClient, workspace_id: str, alert_id: str) -> None:
    host = str(client._base).split("/api/")[0]
    url = f"{host}/api/v1/entities/workspaces/{workspace_id}/automations/{alert_id}"
    try:
        client._client.delete(url, headers=client._auth)
    except Exception as exc:
        print(f"[CLEANUP] Failed to delete alert {alert_id}: {exc}")


@dataclass
class AlertEvaluation:
    """Evaluation scores for a single alert creation run."""

    alert_created: bool
    operator_correct: bool
    threshold_correct: bool
    trigger_correct: bool
    filters_correct: bool
    metric_correct: bool
    recipients_correct: bool

    @property
    def strict_pass(self) -> bool:
        return all(
            [
                self.alert_created,
                self.operator_correct,
                self.threshold_correct,
                self.trigger_correct,
                self.filters_correct,
                self.metric_correct,
                self.recipients_correct,
            ]
        )


@dataclass
class AlertRunResult:
    """Outcome of one K-run conversation for alert creation."""

    conversation_id: str
    alert_id: str | None
    eval: AlertEvaluation
    actual_alert_arguments: dict


@dataclass
class AgenticAlertSummary:
    """Aggregated outcome of K runs for alert creation."""

    run_results: list[AlertRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: AlertRunResult


def _normalize_expected_output(expected: dict) -> CatalogMetricAlert:
    """Parse expected_output dict into CatalogMetricAlert, accepting display-format or internal-format keys."""
    operator = expected.get("operator") or expected.get("Operator") or "GREATER_THAN"
    threshold = expected.get("threshold") or expected.get("Threshold")
    threshold_from = expected.get("threshold_from")
    threshold_to = expected.get("threshold_to")
    trigger = expected.get("trigger") or expected.get("Trigger") or "not specified"

    metric_id = expected.get("metric_id")
    if not metric_id and "Metric" in expected:
        m = re.search(r"\(([^)]+)\)\s*$", str(expected["Metric"]))
        if m:
            metric_id = m.group(1).strip()

    raw_recip = expected.get("recipients") or expected.get("Recipient(s)") or []
    if isinstance(raw_recip, str):
        recipients = [r.strip() for r in raw_recip.replace(";", ",").split(",") if r.strip()]
    else:
        recipients = list(raw_recip)

    filters = expected.get("filters") or expected.get("Time window/Filters")
    if isinstance(filters, str) and any(kw in filters for kw in ("None", "All time")):
        filters = None

    return CatalogMetricAlert(
        operator=operator,
        threshold=threshold,
        threshold_from=threshold_from,
        threshold_to=threshold_to,
        trigger=trigger,
        metric_id=metric_id,
        recipients=recipients,
        filters=filters,
    )


def _extract_alert_call(tool_call_events: list[ToolCallEvent]) -> tuple[str | None, dict, bool]:
    """Return (alert_id, args, tool_called). tool_called=True whenever create_metric_alert appears."""
    for tc in tool_call_events:
        if tc.function_name == "create_metric_alert":
            args = tc.parsed_arguments() or {}
            alert_id: str | None = None
            if tc.result:
                try:
                    result_data = json.loads(tc.result)
                    alert_id = result_data.get("id") or (result_data.get("data") or {}).get("id")
                except Exception:
                    pass
            return alert_id, args, True
    return None, {}, False


def _is_asking_clarification(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return "?" in t or "could you" in t or "please" in t or "clarif" in t


def run_agentic_alert_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
) -> AgenticAlertSummary:
    """Run the alert-skill agentic evaluation K times and return a summary."""
    expected = _normalize_expected_output(expected_output)
    run_results: list[AlertRunResult] = []
    client = ChatClient(host=host, token=token, workspace_id=workspace_id)

    def _run_once(conv_id: str) -> AlertRunResult:
        alert_id_to_delete: str | None = None
        try:
            alert_id: str | None = None
            actual_args: dict = {}
            tool_called = False
            # conversation_history stores prior turns for GPT-4o context.
            # Roles follow GPT-4o's perspective: "assistant"=agent text, "user"=sim-user reply.
            conversation_history: list = []
            current_question = question

            for _iteration in range(max_iterations):
                chat_result = client.send_message(conv_id, current_question)
                alert_id, actual_args, tool_called = _extract_alert_call(chat_result.tool_call_events or [])
                if tool_called:
                    alert_id_to_delete = alert_id
                    break
                response_text = (chat_result.text_response or "").strip()
                # Stop if agent gave a completely empty response (stuck)
                if not response_text and not chat_result.tool_call_events:
                    break
                # Stop before generating a follow-up for the last iteration
                if _iteration >= max_iterations - 1:
                    break
                follow_up = generate_simulated_alert_response(response_text, expected, conversation_history)
                # Record this exchange so the next call has full history
                conversation_history.append({"role": "assistant", "content": response_text})
                conversation_history.append({"role": "user", "content": follow_up})
                current_question = follow_up

            ev = AlertEvaluation(
                alert_created=tool_called,
                operator_correct=tool_called and expected.operator == actual_args.get("operator"),
                threshold_correct=tool_called and _check_threshold(expected, actual_args),
                trigger_correct=tool_called and _check_trigger(expected, actual_args),
                filters_correct=tool_called and _check_filters(expected, actual_args),
                metric_correct=tool_called and _check_metric(expected, actual_args),
                recipients_correct=tool_called and _check_recipients(expected, actual_args),
            )
            return AlertRunResult(
                conversation_id=conv_id,
                alert_id=alert_id,
                eval=ev,
                actual_alert_arguments=actual_args,
            )
        finally:
            if alert_id_to_delete:
                _delete_alert(client, workspace_id, alert_id_to_delete)

    try:
        conv_id_0 = initial_conversation_id if initial_conversation_id is not None else client.create_conversation()
        try:
            run_results.append(_run_once(conv_id_0))
        finally:
            if initial_conversation_id is None:
                client.delete_conversation(conv_id_0)

        for _ in range(1, k):
            conv_id = client.create_conversation()
            try:
                run_results.append(_run_once(conv_id))
            finally:
                client.delete_conversation(conv_id)
    finally:
        client.close()

    pass_at_k = any(r.eval.strict_pass for r in run_results)
    pass_power_k = all(r.eval.strict_pass for r in run_results)
    best = max(
        run_results,
        key=lambda r: sum(
            [
                r.eval.alert_created,
                r.eval.operator_correct,
                r.eval.threshold_correct,
                r.eval.trigger_correct,
                r.eval.filters_correct,
                r.eval.metric_correct,
                r.eval.recipients_correct,
            ]
        ),
    )
    return AgenticAlertSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class AlertSkillAssertionError(AssertionError):
    """Raised when an alert-skill evaluation fails."""

    __tracebackhide__ = True


def evaluate_agentic_alert_skill(
    host: str,
    token: str,
    workspace_id: str,
    question: str,
    expected_output: dict,
    k: int = _DEFAULT_K,
    max_iterations: int = _DEFAULT_MAX_ITERATIONS,
    initial_conversation_id: str | None = None,
    langfuse: object | None = None,
    dataset_item_id: str = "",
    dataset_name: str = "alert_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
) -> None:
    """Run alert-skill evaluation, log to Langfuse, and raise AlertSkillAssertionError on failure."""
    from datetime import datetime as _dt, timezone as _tz  # noqa: PLC0415
    from gooddata_eval.core.agentic._langfuse import try_make_langfuse_client  # noqa: PLC0415

    if langfuse is None:
        langfuse = try_make_langfuse_client()
    window_start = _dt.now(_tz.utc)
    summary = run_agentic_alert_skill(
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
            ev = run.eval
            strict_checks = {
                "alert_created": ev.alert_created,
                "operator_correct": ev.operator_correct,
                "threshold_correct": ev.threshold_correct,
                "trigger_correct": ev.trigger_correct,
                "filters_correct": ev.filters_correct,
                "metric_correct": ev.metric_correct,
                "recipients_correct": ev.recipients_correct,
            }
            with observe(langfuse, pt.id if pt else None, dataset_item_id, run_name, run_metadata) as tid:
                for score_name, value in strict_checks.items():
                    score_safe(langfuse, tid, name=score_name, value=float(value), data_type="BOOLEAN")
                log_quality_and_value_scores(
                    langfuse,
                    tid,
                    strict_checks=strict_checks,
                    latency_sec=pt.latency if pt else None,
                    cost_usd=pt.total_cost if pt else None,
                )

    if not summary.pass_at_k:
        best = summary.best
        ev = best.eval
        raise AlertSkillAssertionError(
            f"Alert skill assertion failed. strict_pass={ev.strict_pass}. "
            f"alert_created={ev.alert_created}, operator_correct={ev.operator_correct}, "
            f"threshold_correct={ev.threshold_correct}, trigger_correct={ev.trigger_correct}, "
            f"filters_correct={ev.filters_correct}, metric_correct={ev.metric_correct}, "
            f"recipients_correct={ev.recipients_correct}. "
            f"Actual args: {best.actual_alert_arguments}"
        )
