# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic alert-skill evaluation runner."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

from gooddata_sdk import GoodDataSdk

from gooddata_eval.core.agentic._catalog import CatalogMetricAlert
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.models import AgenticEvalOutcome, ReasoningStepEvent, ToolCallEvent, build_latency_breakdown

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI: Any = None

_DEFAULT_K = 1
_DEFAULT_MAX_ITERATIONS = 6

_TRIGGER_DISPLAY_TO_API = {"Every time": "ALWAYS", "One time": "ONCE"}
_ALWAYS_TRIGGER_VALUES = {"Every time", "ALWAYS", "not specified"}

_TRIGGER_INSTRUCTIONS = {
    "ALWAYS": (
        "alert me EVERY TIME the condition is met — not once per day, week or month, and not only the first time"
    ),
    "ONCE": "alert me ONLY THE FIRST TIME the condition is met, then stop",
}


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
    if expected.operator == "ANOMALY":
        return True
    exp_trigger = expected.trigger
    # A missing OR explicit-null trigger means "unset" -> the product persists the
    # default ALWAYS ("Every time"). `.get(k, default)` only returns the default when
    # the key is ABSENT, but create_metric_alert serialises unset params as
    # `trigger: null`, so chain with `or` to also cover the present-but-None case.
    act_trigger = actual_args.get("trigger") or actual_args.get("triggerMode") or "ALWAYS"
    if exp_trigger in _ALWAYS_TRIGGER_VALUES:
        return act_trigger in {"ALWAYS", "Every time"}
    act_api = _TRIGGER_DISPLAY_TO_API.get(act_trigger, act_trigger)
    return exp_trigger == act_api


def _check_filters(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    exp_filters = expected.filters
    act_filters = actual_args.get("filters", actual_args.get("attribute_filters")) or []
    if exp_filters is None:
        return True
    if not exp_filters:
        return not act_filters
    if not act_filters:
        return False
    return _deep_subset(exp_filters, act_filters)


def _check_metric(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    if not expected.metric_id:
        return True
    act_metric_raw = actual_args.get("metric_id", actual_args.get("metricId", ""))
    act_metric = _parse_metric_id(str(act_metric_raw)) or str(act_metric_raw)
    return expected.metric_id == act_metric


def _resolve_internal_recipient_ids(sdk: GoodDataSdk, emails: list[str]) -> set[str]:
    """Best-effort map of expected recipient emails to internal GoodData user ids.

    Some notification channels are workspace-restricted to internal users --
    `create_metric_alert` then addresses the alert by internal user id
    (`internal_recipients`), never by email, so an expected email has to be
    resolved before it can be compared against that field. Failures (no
    matching user, no permission, network error) are swallowed: the caller
    treats an empty result the same as "this delivery path doesn't match",
    which is correct -- it doesn't mean the alert itself failed.
    """
    if not emails:
        return set()
    try:
        # RSQL quoted-string escaping: backslash first, then the enclosing quote char,
        # or an email like o'hara@example.com breaks the filter into invalid RSQL.
        escaped = [email.replace("\\", "\\\\").replace("'", "\\'") for email in emails]
        quoted = ",".join(f"'{email}'" for email in escaped)
        resp = sdk._client.entities_api.get_all_entities_users(filter=f"email=in=({quoted})")
        return {u.id for u in (resp.data or [])}
    except Exception:
        return set()


def _check_recipients(expected: CatalogMetricAlert, actual_args: dict, sdk: GoodDataSdk | None = None) -> bool:
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
    if set(expected.recipients) == set(act_recip or []):
        return True
    act_internal_raw = actual_args.get("internal_recipients")
    # internal_recipients is declared `anyOf: [array of string, string, null]` in the
    # create_metric_alert tool schema -- a single id as a bare string is schema-legal,
    # not a malformed call, so it needs the same string/list normalization already
    # applied to recipients/external_recipients above.
    if isinstance(act_internal_raw, str):
        act_internal = [act_internal_raw]
    elif isinstance(act_internal_raw, list):
        act_internal = act_internal_raw
    else:
        act_internal = []
    if sdk is not None and act_internal:
        internal_recipient_ids = _resolve_internal_recipient_ids(sdk, expected.recipients)
        if internal_recipient_ids & set(act_internal):
            return True
    return False


def generate_simulated_alert_response(
    agent_message: str,
    expected: CatalogMetricAlert,
    conversation_history: list,
    question: str = "",
) -> str:
    """Stateful sim-user reply for alert-skill conversation (gpt-4o).

    ``question`` is the fixture's original request. The sim-user is first called with an empty
    history — the opening question went straight to the agent, never to the sim-user — so
    without it rule 5's "the filters your original request implies" refers to text the model
    cannot see. Optional (defaults to "") to keep the signature backwards compatible.
    """
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
    # BETWEEN / NOT_BETWEEN carry their value in threshold_from/threshold_to, so `threshold` is
    # None for them. Rule 3 asks the sim-user to verify the threshold, and reporting "not
    # specified" made it demand the agent delete both bounds of a BETWEEN condition — an
    # impossible request that burned every iteration without the alert ever being created.
    threshold: str | float | int
    if expected.operator in ("BETWEEN", "NOT_BETWEEN") and (
        expected.threshold_from is not None or expected.threshold_to is not None
    ):
        threshold = f"between {expected.threshold_from} and {expected.threshold_to}"
    elif expected.threshold is not None:
        threshold = expected.threshold
    else:
        threshold = "not specified"
    recipients = ", ".join(expected.recipients) if expected.recipients else "not specified"
    trigger = expected.trigger
    filters = expected.filters

    # "not specified" is the normalizer's stand-in for an absent trigger, which the product
    # persists as its ALWAYS default and `_check_trigger` asserts as ALWAYS. Both the cadence to
    # ask for (rule 6) and the goal text (rule 1) use the resolved value: reporting the raw
    # placeholder made rule 3 treat the trigger as unconstrained, so the sim-user would confirm a
    # ONCE/ONCE_PER_INTERVAL proposal that the assertion then failed.
    trigger_key = "ALWAYS" if trigger in _ALWAYS_TRIGGER_VALUES else trigger
    trigger_request = _TRIGGER_INSTRUCTIONS.get(trigger_key, f"set the trigger to {trigger}")

    # Three branches, matching the three states of `expected.filters`. `[]` and `None` must not
    # share one: telling the sim-user "you want NO filters" on an unstated expectation makes it
    # refuse filters the request genuinely implies (e.g. "orders from the United States"), which
    # quietly turns that fixture into a weaker test rather than a failing one.
    if filters:
        filters_rule = (
            f"5. Your alert needs exactly these filters and NOTHING else: {filters}. "
            "If the agent offers, proposes or asks about any further date/time window, "
            "evaluation period or granularity, refuse it and repeat that these are the only "
            "filters you want.\n"
        )
    elif filters == []:
        filters_rule = (
            "5. Your alert must have NO filters and NO date/time window — it evaluates over all time. "
            "If the agent asks which time period each check should cover, or offers a choice such as "
            "'last Day / Week / Month', do NOT pick one: reply that you want no date filter at all, "
            "all time. Never invent a period, a granularity or an 'evaluate each run on a X basis' "
            "instruction the goal did not ask for.\n"
        )
    else:
        filters_rule = (
            "5. Ask only for the filters your original request implies — do not invent an evaluation "
            "period, granularity or date window that was not requested. If the agent offers a choice "
            "such as 'last Day / Week / Month' that your request never mentioned, say you do not want "
            "a date window.\n"
        )

    original_request = f'Your original request to the agent was: "{question}"\n' if question else ""

    system_prompt = (
        "You are a user requesting creation of an alert for a metric from an AI agent. "
        "Respond naturally but always steer toward the exact values you were given.\n"
        + original_request
        + "Rules you MUST follow:\n"
        f"1. Your goal: metric={metric}, operator={operator}, threshold={threshold}, "
        f"recipients={recipients}, trigger={trigger_key}" + (f", filters={filters}" if filters else "") + ".\n"
        "2. Never revert or change a decision that was already confirmed in a previous turn.\n"
        "3. If the agent shows a final summary, an alert proposal or asks for confirmation, check "
        "   ALL of these against your goal: recipients, trigger (how often you are alerted), "
        "   filters / time window, threshold and operator. If ANY of them differs — for example the "
        "   summary says 'once per day/week/month' but your goal is every time, or it lists a date "
        "   filter you never asked for — do NOT confirm: name the wrong field, state the correct "
        "   value and ask the agent to fix it. Say 'Yes, please proceed to create the alert.' ONLY "
        "   when every one of those fields matches your goal.\n"
        "   A field your goal reports as 'not specified' is one you have NO expectation about: "
        "   accept whatever the agent chose for it and never ask for it to be removed.\n"
        "4. Proactively include your email recipient in your first reply. "
        "   Do not wait for the agent to ask — state it alongside the metric and condition answers.\n"
        + filters_rule
        + f"6. Proactively state how often you want to be alerted in your first reply: {trigger_request}. "
        "   Repeat it if the agent proposes a different cadence.\n"
        "Reply concisely and directly."
    )

    messages: list = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append(
        {"role": "user", "content": f'The agent asked: "{agent_message}"\n\nRespond concisely and directly.'}
    )
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content or ""


def _delete_alert(sdk: GoodDataSdk, workspace_id: str, alert_id: str) -> None:
    """Best-effort delete of an alert (automation) created during evaluation.

    Uses the GoodData SDK entities API rather than reimplementing the REST call.
    Failures are logged, not raised.
    """
    try:
        sdk._client.entities_api.delete_entity_automations(workspace_id, alert_id)
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
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)


@dataclass
class AgenticAlertSummary:
    """Aggregated outcome of K runs for alert creation."""

    run_results: list[AlertRunResult]
    pass_at_k: bool
    pass_power_k: bool
    best: AlertRunResult


def _case_insensitive_get(d: dict, *keys: str) -> Any:
    """Look up a value by key, preferring an exact match then a case-insensitive one."""
    for k in keys:
        if k in d:
            return d[k]
    lowered = {str(k).lower(): v for k, v in d.items()}
    for k in keys:
        if k.lower() in lowered:
            return lowered[k.lower()]
    return None


_NO_FILTER_MARKERS = ("none", "all time")


def _normalize_expected_filters(expected: dict) -> list | str | None:
    """
    * ``Filters`` list           -> that list (exact expectation)
    * "None (All time)" in either -> ``[]``   (stated: no filters; extras fail)
    * anything else / absent      -> ``None`` (unstated; filters not asserted)
    """
    filters = _case_insensitive_get(expected, "filters")
    if isinstance(filters, list):
        return filters
    time_window = _case_insensitive_get(expected, "time window/filters", "time_window")
    for candidate in (filters, time_window):
        if isinstance(candidate, str) and any(kw in candidate.lower() for kw in _NO_FILTER_MARKERS):
            return []
    # Prose that is not a no-filter marker ("Product Category = X") describes a filter without
    # encoding it, so it cannot be compared: returning it made `_check_filters` fall through to
    # `_deep_subset(str, list)`, which can never match. `None` is what the contract above
    # promises — the sim-user derives such filters from the original request instead.
    return None


def _normalize_expected_output(expected: dict) -> CatalogMetricAlert:
    """Parse expected_output dict into CatalogMetricAlert, accepting display-format or internal-format keys."""
    operator = _case_insensitive_get(expected, "operator") or "GREATER_THAN"
    threshold = _case_insensitive_get(expected, "threshold")
    threshold_from = _case_insensitive_get(expected, "threshold_from")
    threshold_to = _case_insensitive_get(expected, "threshold_to")

    trigger = _case_insensitive_get(expected, "trigger") or "not specified"
    trigger = _TRIGGER_DISPLAY_TO_API.get(trigger, trigger)

    metric_id = _case_insensitive_get(expected, "metric_id")
    if not metric_id:
        metric_disp = _case_insensitive_get(expected, "metric")
        if metric_disp:
            m = re.search(r"\(([^)]+)\)\s*$", str(metric_disp))
            metric_id = m.group(1).strip() if m else None

    raw_recip = _case_insensitive_get(expected, "recipients", "recipient(s)") or []
    if isinstance(raw_recip, str):
        recipients = [r.strip() for r in raw_recip.replace(";", ",").split(",") if r.strip()]
    else:
        recipients = list(raw_recip)

    filters = _normalize_expected_filters(expected)

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


def render_alert_proposal(proposal: dict) -> str:
    """Render an alert-proposal part as the text the simulated user reacts to.

    The alert skill's confirmation step deliberately emits no text part (GDAI-2032) — the
    prompt and the CTA live only in the proposal payload, which the frontend renders as a
    widget. Dumping the payload (rather than prose) keeps recipients, condition, trigger and
    dashboard visible so the simulated user can still verify them against its goal, and does
    not need updating whenever ``AlertProposal`` grows a field.
    """
    cta = proposal.get("cta") or "Should I create this alert?"
    summary = {k: v for k, v in proposal.items() if k != "cta"}
    alert = dict(summary.get("alert") or {})
    # The AFM execution block is opaque wire dicts — noise that would crowd out the fields
    # the simulated user actually has to check.
    alert.pop("execution", None)
    if "alert" in summary:
        # Key off presence, not truthiness: an alert whose only key was `execution` must
        # still be replaced, otherwise the original (execution-bearing) dict survives.
        summary["alert"] = alert
    return f"{cta}\n\nAlert proposal:\n{json.dumps(summary, indent=2, sort_keys=True)}"


def run_agentic_alert_skill(
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
) -> AgenticAlertSummary:
    """Run the alert-skill agentic evaluation K times and return a summary."""
    expected = _normalize_expected_output(expected_output)
    run_results: list[AlertRunResult] = []
    client = ChatClient(
        host=host, token=token, workspace_id=workspace_id, reasoning_effort=reasoning_effort, agent_id=agent_id
    )
    sdk = GoodDataSdk.create(host, token)

    def _run_once(conv_id: str) -> AlertRunResult:
        alert_id_to_delete: str | None = None
        try:
            alert_id: str | None = None
            actual_args: dict = {}
            tool_called = False
            reasoning_steps: list[str] = []
            response_id: str | None = None
            all_tool_call_events: list[ToolCallEvent] = []
            all_reasoning_step_events: list[ReasoningStepEvent] = []
            turn_offset = 0.0  # each turn's call_ts/ts restarts near 0 -- shift by prior turns' wall time
            tool_index_offset = 0
            reasoning_index_offset = 0
            # conversation_history stores prior turns for GPT-4o context.
            # Roles follow GPT-4o's perspective: "assistant"=agent text, "user"=sim-user reply.
            conversation_history: list = []
            current_question = question

            for _iteration in range(max_iterations):
                chat_result = client.send_message(conv_id, current_question)
                reasoning_steps.extend(chat_result.reasoning_steps or [])
                response_id = chat_result.response_id or response_id
                for tc in chat_result.tool_call_events or []:
                    if tc.call_ts is not None:
                        tc.call_ts += turn_offset
                    if tc.result_ts is not None:
                        tc.result_ts += turn_offset
                    if tc.index is not None:
                        tc.index += tool_index_offset
                for rs in chat_result.reasoning_step_events or []:
                    rs.ts += turn_offset
                    rs.index += reasoning_index_offset
                all_tool_call_events.extend(chat_result.tool_call_events or [])
                all_reasoning_step_events.extend(chat_result.reasoning_step_events or [])
                tool_index_offset += len(chat_result.tool_call_events or [])
                reasoning_index_offset += len(chat_result.reasoning_step_events or [])
                turn_offset += chat_result.turn_wall_clock_sec or 0.0
                alert_id, actual_args, tool_called = _extract_alert_call(chat_result.tool_call_events or [])
                if tool_called:
                    alert_id_to_delete = alert_id
                    break
                response_text = (chat_result.text_response or "").strip()
                if not response_text and chat_result.alert_proposals:
                    response_text = render_alert_proposal(chat_result.alert_proposals[-1])
                # Stop if agent gave a completely empty response (stuck)
                if not response_text and not chat_result.tool_call_events:
                    break
                # Stop before generating a follow-up for the last iteration
                if _iteration >= max_iterations - 1:
                    break
                follow_up = generate_simulated_alert_response(
                    response_text, expected, conversation_history, question=question
                )
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
                recipients_correct=tool_called and _check_recipients(expected, actual_args, sdk=sdk),
            )
            return AlertRunResult(
                conversation_id=conv_id,
                alert_id=alert_id,
                eval=ev,
                actual_alert_arguments=actual_args,
                reasoning_steps=reasoning_steps,
                response_id=response_id,
                tool_call_events=all_tool_call_events,
                reasoning_step_events=all_reasoning_step_events,
            )
        finally:
            if alert_id_to_delete:
                _delete_alert(sdk, workspace_id, alert_id_to_delete)

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
    reasoning_steps: list[str]
    conversation_id: str
    response_id: str | None
    detail: dict


def evaluate_agentic_alert_skill(
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
    dataset_name: str = "alert_skill",
    run_timestamp: str | None = None,
    model_version_override: str | None = None,
    run_metadata_extra: dict | None = None,
    reasoning_effort: ReasoningEffort | None = None,
) -> AgenticEvalOutcome:
    """Run alert-skill evaluation, log to Langfuse, and raise AlertSkillAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as
    ``.reasoning_steps``/``.conversation_id``/``.response_id`` (mirrors the
    `conversation_id`-on-exception idiom in `ChatClient.ask()`) so callers can retrieve them
    either way.
    """
    from datetime import datetime as _dt  # noqa: PLC0415
    from datetime import timezone as _tz  # noqa: PLC0415

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
        exc = AlertSkillAssertionError(
            f"Alert skill assertion failed. strict_pass={ev.strict_pass}. "
            f"alert_created={ev.alert_created}, operator_correct={ev.operator_correct}, "
            f"threshold_correct={ev.threshold_correct}, trigger_correct={ev.trigger_correct}, "
            f"filters_correct={ev.filters_correct}, metric_correct={ev.metric_correct}, "
            f"recipients_correct={ev.recipients_correct}. "
            f"Actual args: {best.actual_alert_arguments}"
        )
        exc.reasoning_steps = best.reasoning_steps
        exc.conversation_id = best.conversation_id
        exc.response_id = best.response_id
        exc.detail = {
            "alert_created": ev.alert_created,
            "operator_correct": ev.operator_correct,
            "threshold_correct": ev.threshold_correct,
            "trigger_correct": ev.trigger_correct,
            "filters_correct": ev.filters_correct,
            "metric_correct": ev.metric_correct,
            "recipients_correct": ev.recipients_correct,
            "actual_alert_arguments": best.actual_alert_arguments,
            "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
        }
        raise exc
    best = summary.best
    ev = best.eval
    return AgenticEvalOutcome(
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail={
            "alert_created": ev.alert_created,
            "operator_correct": ev.operator_correct,
            "threshold_correct": ev.threshold_correct,
            "trigger_correct": ev.trigger_correct,
            "filters_correct": ev.filters_correct,
            "metric_correct": ev.metric_correct,
            "recipients_correct": ev.recipients_correct,
            "actual_alert_arguments": best.actual_alert_arguments,
            "latency_breakdown": build_latency_breakdown(best.tool_call_events, best.reasoning_step_events),
        },
    )
