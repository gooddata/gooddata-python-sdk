# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic alert-skill evaluation runner."""

from __future__ import annotations

import dataclasses
import json
import os
import re
import string
import time
from dataclasses import dataclass, field
from typing import Any

import httpx
from gooddata_sdk import GoodDataSdk

from gooddata_eval.core.agentic._catalog import AnomalyDetectionGranularity, CatalogMetricAlert
from gooddata_eval.core.agentic._failed_runs import build_failed_runs
from gooddata_eval.core.agentic._failure_message import failed_checks_from
from gooddata_eval.core.agentic._gate import (
    DEFAULT_GATE,
    EvalGate,
    gate_passed,
    log_gate_scores,
    stamp_gate_metadata,
)
from gooddata_eval.core.agentic._outcome import (
    agentic_detail,
    agentic_success,
    chat_failure_exit,
    failure_message_head,
    label_runs,
    log_eval_error_score,
    raise_agentic_failure,
)
from gooddata_eval.core.agentic._trace_linker import (
    RunIdentity,
    RunTraceContext,
    SubmitTraceLink,
    open_item_trace,
    run_trace_link_inline,
    submit_trace_scoring,
    utc_now,
)
from gooddata_eval.core.agentic.metric_skill import _delete_metric, _extract_created_metric_ids
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatClient, ChatError
from gooddata_eval.core.config import ReasoningEffort
from gooddata_eval.core.langfuse.item_scope import item_scope
from gooddata_eval.core.models import (
    AgenticAssertionError,
    AgenticEvalOutcome,
    ChatResult,
    LoopExit,
    ReasoningStepEvent,
    ToolCallEvent,
    shift_and_index_events,
    timeline_detail,
)

try:
    from openai import OpenAI as _OpenAI
except ImportError:
    _OpenAI: Any = None

_DEFAULT_K = 1
_DEFAULT_MAX_ITERATIONS = 6

_TRIGGER_DISPLAY_TO_API = {"Every time": "ALWAYS", "One time": "ONCE"}
_ALWAYS_TRIGGER_VALUES = {"Every time", "ALWAYS", "not specified"}
_RELATIVE_OPERATORS = ("INCREASES_BY", "DECREASES_BY", "CHANGES_BY")

# Fixture spelling of each period-comparison property -> the create_metric_alert argument.
_COMPARISON_ARGS = {
    "kind": "comparison_kind",
    "periods_ago": "comparison_periods_ago",
    "date_dataset_id": "comparison_date_dataset_id",
    "date_attribute_id": "comparison_date_attribute_id",
    "arithmetic_operator": "arithmetic_operator",
    "compare_metric_id": "compare_metric_id",
}
# Compared verbatim: object ids are case-sensitive, unlike the enum-valued properties.
_COMPARISON_ID_ARGS = ("comparison_date_dataset_id", "comparison_date_attribute_id", "compare_metric_id")
# What create_metric_alert applies when the argument is left out, per its own contract. A
# metric-to-metric comparison has no periods, so periods_ago defaults only for a period kind.
_COMPARISON_ARG_DEFAULTS: dict[str, object] = {"comparison_periods_ago": 1, "arithmetic_operator": "DIFFERENCE"}
_PERIOD_COMPARISON_KINDS = ("PREVIOUS_PERIOD", "SAME_PERIOD_PRIOR_YEAR")
_NO_COMPARISON_MARKERS = ("none", "no comparison")

# AlertEvaluation checks, in report order. Every run is scored on the first group; the second only
# when the item states the matching expectation.
_ALERT_CHECKS = (
    "alert_created",
    "operator_correct",
    "threshold_correct",
    "trigger_correct",
    "filters_correct",
    "metric_correct",
    "recipients_correct",
    "attributes_correct",
    "granularity_correct",
)
_CONDITIONAL_ALERT_CHECKS = (
    "comparison_correct",
    "title_correct",
    "dashboard_correct",
    "alert_sensitivity_correct",
    "alert_trigger_interval_correct",
    "alert_date_dataset_correct",
    "alert_initial_filters_correct",
    "alert_initial_recipients_correct",
)
# Fields `check_first_proposal` may name; each one is scored on the first proposal as well.
_FIRST_PROPOSAL_FIELDS = ("filters", "recipients")
# Labels of the `any_of` combinations in the simulated user's rule 9; an item lists at most this many.
_COMBINATION_LABELS = string.ascii_uppercase
# The only CatalogMetricAlert fields `any_of` options may differ in. Rule 9 states them per
# combination and rules 1 and 5 defer to it; rules 1-8 state every other field once.
_ANY_OF_FIELDS = ("threshold", "threshold_from", "threshold_to", "filters")
# The only check of an item that expects no alert; it replaces every other check.
_NO_ALERT_CHECK = "alert_not_proposed"
# Score names published only by an item that states the matching expectation (gdc-nas combo_report).
ALERT_CONDITIONAL_SCORES = (*_CONDITIONAL_ALERT_CHECKS, _NO_ALERT_CHECK)

_SENSITIVITIES = ("LOW", "MEDIUM", "HIGH")
# What create_metric_alert applies to an ANOMALY alert when `sensitivity` is left out, per its own contract.
_DEFAULT_SENSITIVITY = "MEDIUM"
_TRIGGER_INTERVALS = ("DAY", "WEEK", "MONTH", "QUARTER", "YEAR")
# The tool whose call is the agent proposing an alert, whether or not the call succeeded.
_PROPOSAL_TOOL = "prepare_metric_alert_proposal"
# The metric skill's write tool. The alert prompt lets the agent offer a metric the workspace lacks.
_CREATE_METRIC_TOOL = "create_metric"
# A no-alert item asserts nothing about an alert, so stating any of these is a fixture mistake.
_ALERT_ONLY_KEYS = (
    "operator",
    "threshold",
    "threshold_from",
    "threshold_to",
    "filters",
    "time window/filters",
    "time_window",
    "attributes",
    "granularity",
    "detection granularity",
    "comparison",
    "title",
    "dashboard",
    "dashboard_id",
    "sensitivity",
    "trigger_interval",
    "trigger interval",
    "date_dataset_id",
    "date dataset",
    "check_first_proposal",
    "check first proposal",
)
# A no-alert run stops after this many agent turns: the simulated user only declines. Measured on
# 2026-11-25 with the cap at the default budget of 6 (6 runs, a churn-rate and a website-traffic
# request, gpt-5.6-luna): every agent answered in turn 1, confirmed it would not create the alert
# in turn 2, and spent turns 3-6 on pleasantries without a tool call. Three turns cover that with
# one to spare.
_NO_ALERT_MAX_ITERATIONS = 3

# Expected-recipient spellings that mean the owner of the API token.
_CURRENT_USER_RECIPIENT = "me"
_CURRENT_USER_MARKERS = {"me", "myself", "current user", "current_user"}

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


def _recipient_list(value: object, *, split_bare: bool) -> list[str]:
    """A recipient argument as a list, decoded the way gen-ai does before calling the server.

    The tool schema declares both recipient fields ``anyOf: [array of string, string, null]``,
    and some models send the list JSON-encoded as a string (``'["admin"]'``). Empty or
    ``"null"`` means none; any other string that is not a JSON list of strings is a bare
    value -- one user id, or with ``split_bare`` a comma/semicolon-separated email list
    (gen-ai forwards a bare string as one entry; the split is this checker's own leniency).
    A non-string list entry is kept as its ``str()`` so it compares unequal instead of raising.
    """
    if isinstance(value, list):
        return [str(item) for item in value]
    if not isinstance(value, str) or value.strip() in ("", "null"):
        return []
    try:
        parsed = json.loads(value)
    except ValueError:
        parsed = None
    if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
        return parsed
    return (_parse_recipients(value) or []) if split_bare else [value]


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
    return _to_number(expected.threshold) == _to_number(actual_args.get("threshold"))


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


def _filters_match(exp_filters: list | str | None, act_filters: list) -> bool:
    """``None`` asserts nothing, ``[]`` asserts no filter, a list must match entry by entry."""
    if exp_filters is None:
        return True
    if not exp_filters:
        return not act_filters
    if not act_filters:
        return False
    return _deep_subset(exp_filters, act_filters)


def _check_filters(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    act_filters = actual_args.get("filters", actual_args.get("attribute_filters")) or []
    return _filters_match(expected.filters, act_filters)


def _attribute_label_ids(items: list, *, side: str) -> list[str]:
    """Canonicalise group-by entries to bare label ids, whatever spelling they arrive in.

    The two sides of the comparison speak different vocabularies for the same grouping.
    Fixtures author the AAC tool-input form, ``{"using": "label/x"}``; ``create_metric_alert``
    receives the resolved AFM form, ``{"localIdentifier": "a0", "label": {"identifier":
    {"id": "x", "type": "label"}}}``, forwarded verbatim from ``prepare_metric_alert_proposal``.
    Identity is therefore the only thing they can be compared on.

    A shape not listed here, or a URI prefix other than ``label/``, raises: ``label/x`` and
    ``attribute/x`` are different objects, and an unknown spelling must fail loudly rather
    than quietly compare unequal.
    """
    if not isinstance(items, list):
        raise ValueError(f"Unrecognised {side} group-by attributes, expected a list: {items!r}")
    ids: list[str] = []
    for item in items:
        raw: object = None
        if isinstance(item, str):
            raw = item
        elif isinstance(item, dict):
            label = item.get("label")
            identifier = item.get("identifier")
            if isinstance(item.get("using"), str):
                raw = item["using"]
            elif isinstance(label, dict) and isinstance(label.get("identifier"), dict):
                raw = label["identifier"].get("id")
            elif isinstance(identifier, dict):
                raw = identifier.get("id")
        if not isinstance(raw, str) or not raw:
            raise ValueError(f"Unrecognised {side} group-by attribute entry: {item!r}")
        prefix, slash, rest = raw.partition("/")
        if not slash:
            ids.append(raw)
        elif prefix == "label" and rest:
            ids.append(rest)
        else:
            raise ValueError(f"Unrecognised {side} group-by attribute reference: {raw!r}")
    return ids


def _check_attributes(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    """Compare group-by identity only.

    Per-entry properties — ``showAllValues``, the converter-assigned ``localIdentifier`` —
    are deliberately not asserted, and the comparison is a multiset so entry order does not
    matter.
    """
    exp_attributes = expected.attributes
    if exp_attributes is None:
        return True
    act_attributes = actual_args.get("attributes")
    if act_attributes is None:
        # Arguments are raw `json.loads` output, where an unset nullable argument arrives as
        # null rather than absent. Both spellings of "no grouping" have to land on [], which
        # is why this is not `actual_args.get("attributes", [])`.
        act_attributes = []
    elif not isinstance(act_attributes, list):
        # An argument that is not a list of groupings is the agent answering wrongly, so it
        # scores False. Raising instead would make the runner record an ERROR, and errored
        # items are excluded from the failure count — a malformed answer must not rank above
        # a merely wrong one. An unreadable *entry* still raises, in `_attribute_label_ids`:
        # entries are typed at the tool boundary, so the plausible cause there is the wire
        # format moving, which has to be unmissable.
        return False
    if not exp_attributes:
        return not act_attributes
    exp_ids = sorted(_attribute_label_ids(exp_attributes, side="expected"))
    act_ids = sorted(_attribute_label_ids(act_attributes, side="actual"))
    return exp_ids == act_ids


def _check_granularity(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    """Compare the ANOMALY detection interval when the fixture states one.

    ``None`` means unasserted, mirroring ``attributes``: only the ANOMALY items carry a
    ``Granularity``, and every other item must stay unaffected. The expectation is already
    canonical by the time it lands here; the tool argument is a raw string, so only that
    side needs folding.
    """
    if expected.granularity is None:
        return True
    actual = actual_args.get("granularity")
    if not actual:
        return False
    return str(actual).strip().upper() == expected.granularity.value


def _canonical_comparison_value(arg: str, value: object) -> str | int | float | None:
    """Fold one comparison value so fixture and tool-argument spellings compare equal."""
    if value is None or str(value).strip() == "":
        return None
    if arg == "comparison_periods_ago":
        return _to_number(value)
    if arg in _COMPARISON_ID_ARGS:
        return str(value).strip()
    return str(value).strip().upper()


def _check_comparison(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    """Compare only the comparison properties the fixture states.

    ``None`` means unasserted. A stated ``comparison_kind`` of ``None`` asserts the alert has
    no comparison at all. ``comparison_kind`` is read as ``create_metric_alert`` resolves it:
    left out next to a ``compare_metric_id`` it is METRIC. Any other argument the agent left out
    on an alert that does compare counts as the value ``create_metric_alert`` applies for it, so
    omitting ``comparison_periods_ago`` matches 1 on a period comparison; a METRIC comparison has
    no periods, and with no comparison there is nothing to default.
    The comparison period itself (DAY, MONTH, ...) is not checked here: it is the granularity
    of the comparison date filter, which ``filters`` asserts.
    """
    if expected.comparison is None:
        return True
    kind = actual_args.get("comparison_kind") or ("METRIC" if actual_args.get("compare_metric_id") else None)
    for arg, exp_value in expected.comparison.items():
        act_raw = kind if arg == "comparison_kind" else actual_args.get(arg)
        defaults_apply = arg != "comparison_periods_ago" or str(kind).upper() in _PERIOD_COMPARISON_KINDS
        if act_raw is None and kind is not None and defaults_apply:
            act_raw = _COMPARISON_ARG_DEFAULTS.get(arg)
        # Only the fixture side of an object id is trimmed: a padded id is a different id.
        actual = act_raw if arg in _COMPARISON_ID_ARGS else _canonical_comparison_value(arg, act_raw)
        if actual != exp_value:
            return False
    return True


def _check_title(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    """Exact match on the alert name when the fixture states one.

    Only the fixture side is trimmed: a name saved with padding is not the name the user asked for.

    An omitted ``title`` fails: ``create_metric_alert`` then saves an auto-generated name, even
    when ``automation_id`` carries a slug of the requested one.
    """
    if expected.title is None:
        return True
    actual = actual_args.get("title")
    return isinstance(actual, str) and actual == expected.title


def _check_dashboard(expected: CatalogMetricAlert, actual_args: dict) -> bool:
    """Compare the bound dashboard id when the fixture states one; the actual id verbatim."""
    if expected.dashboard_id is None:
        return True
    actual = actual_args.get("dashboard_id")
    return isinstance(actual, str) and actual == expected.dashboard_id


def _check_enum_arg(expected_value: str | None, actual_args: dict, arg: str, default: str | None = None) -> bool | None:
    """Case-folded compare of an enum-valued argument; ``None`` when the fixture states no value.

    ``default`` is the value ``create_metric_alert`` applies when the argument is left out, so an
    omitted argument is compared as that value.
    """
    if expected_value is None:
        return None
    actual = actual_args.get(arg)
    if actual is None:
        actual = default
    return isinstance(actual, str) and actual.strip().upper() == expected_value


def _check_trigger_interval(expected: CatalogMetricAlert, actual_args: dict) -> bool | None:
    """The stated interval, on an alert that fires once per interval; ``None`` when unasserted.

    The tool applies ``trigger_interval`` only to ONCE_PER_INTERVAL and defaults the trigger to
    ALWAYS. ``_check_trigger`` skips ANOMALY alerts, so an anomaly alert sent without that trigger
    would otherwise score an interval it never uses.
    """
    if expected.trigger_interval is None:
        return None
    actual_trigger = actual_args.get("trigger") or actual_args.get("triggerMode") or "ALWAYS"
    if _TRIGGER_DISPLAY_TO_API.get(actual_trigger, actual_trigger) != "ONCE_PER_INTERVAL":
        return False
    return _check_enum_arg(expected.trigger_interval, actual_args, "trigger_interval")


def _check_date_dataset(expected: CatalogMetricAlert, actual_args: dict) -> bool | None:
    """The ANOMALY detection dataset, compared verbatim; ``None`` when unasserted."""
    if expected.date_dataset_id is None:
        return None
    return actual_args.get("date_dataset_id") == expected.date_dataset_id


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
    matching user, no permission, network error) are logged and return an
    empty set: the caller treats that the same as "this delivery path doesn't
    match", which is correct -- it doesn't mean the alert itself failed.
    """
    if not emails:
        return set()
    try:
        # RSQL quoted-string escaping: backslash first, then the enclosing quote char,
        # or an email like o'hara@example.com breaks the filter into invalid RSQL.
        escaped = [email.replace("\\", "\\\\").replace("'", "\\'") for email in emails]
        quoted = ",".join(f"'{email}'" for email in escaped)
        resp = sdk._client.entities_api.get_all_entities_users(filter=f"email=in=({quoted})")
        ids = {u.id for u in (resp.data or [])}
    except Exception as exc:
        print(f"[RECIPIENTS] Looking up users by {len(emails)} recipient email(s) failed: {exc}")
        return set()
    if not ids:
        print(
            f"[RECIPIENTS] No user has any of the {len(emails)} recipient email(s); internal recipients cannot match."
        )
    return ids


_AUTOMATION_PAGE_SIZE = 500


def _automation_ids(host: str, token: str, workspace_id: str) -> set[str] | None:
    """Ids of every automation of the workspace, page by page, or None when they cannot all be listed.

    A partial list would make an automation that existed before the run look new to the cleanup,
    so any failure, including a page that adds nothing, returns None.
    """
    ids: set[str] = set()
    page = 0
    try:
        while True:
            resp = httpx.get(
                f"{host.rstrip('/')}/api/v1/entities/workspaces/{workspace_id}/automations",
                params={"size": _AUTOMATION_PAGE_SIZE, "page": page},
                headers={"Authorization": f"Bearer {token}"},
                timeout=30.0,
            )
            resp.raise_for_status()
            body = resp.json()
            # A body without a `data` list is not an empty workspace: read as one, it would make
            # an alert that existed before the run look new to the cleanup.
            data = body.get("data") if isinstance(body, dict) else None
            if not isinstance(data, list):
                raise ValueError(f"page {page} has no data list")
            page_ids = {item.get("id") for item in data if isinstance(item, dict)}
            if len(page_ids) != len(data) or not all(isinstance(i, str) and i for i in page_ids):
                raise ValueError(f"page {page} lists an automation without an id")
            if len(data) < _AUTOMATION_PAGE_SIZE:
                return ids | page_ids
            if page_ids <= ids:
                raise ValueError(f"page {page} repeats automations already listed")
            ids |= page_ids
            page += 1
    except Exception as exc:
        print(f"[CLEANUP] Listing automations failed: {exc}")
        return None


def _parsed_arguments(tc: ToolCallEvent) -> dict:
    """A tool call's arguments, or ``{}`` when they are not a JSON object."""
    args = tc.parsed_arguments()
    return args if isinstance(args, dict) else {}


def _named_automation_ids(tool_call_events: list[ToolCallEvent]) -> set[str]:
    """``automation_id`` values the agent passed to the proposal and create tools.

    A create call can succeed on the server while its event is missing from the turn the
    harness reads, so the id the agent named is the only handle left for cleanup.
    """
    names = (_PROPOSAL_TOOL, "create_metric_alert")
    # Filtered before the set: a rejected call may carry an unhashable value such as a list, and
    # this runs in the cleanup, where an error would drop the run and the other named ids.
    ids = (_parsed_arguments(tc).get("automation_id") for tc in tool_call_events if tc.function_name in names)
    return {i for i in ids if isinstance(i, str) and i}


def _resolve_current_user_id(host: str, token: str) -> str | None:
    """Id of the user that owns ``token``, or None if the profile cannot be read.

    The current user is matched by id, not email: that user may have no email at all.
    """
    try:
        resp = httpx.get(
            f"{host.rstrip('/')}/api/v1/profile",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0,
        )
        resp.raise_for_status()
        user_id = resp.json().get("userId")
    except Exception as exc:
        print(f"[RECIPIENTS] Resolving the current user failed: {exc}")
        return None
    return user_id if isinstance(user_id, str) and user_id else None


def _split_current_user(recipients: list[str]) -> tuple[bool, list[str]]:
    """Whether ``recipients`` names the current user, and the email recipients besides it."""
    emails = [r for r in recipients if r != _CURRENT_USER_RECIPIENT]
    return len(emails) != len(recipients), emails


def _check_recipients(
    expected: CatalogMetricAlert,
    actual_args: dict,
    sdk: GoodDataSdk | None = None,
    current_user_id: str | None = None,
) -> bool:
    if not expected.recipients:
        return True
    act_recip = _recipient_list(actual_args.get("recipients", actual_args.get("external_recipients")), split_bare=True)
    act_internal = _recipient_list(actual_args.get("internal_recipients"), split_bare=False)
    wants_current_user, expected_emails = _split_current_user(expected.recipients)
    if wants_current_user:
        if current_user_id is None or current_user_id not in act_internal:
            return False
        other_internal = set(act_internal) - {current_user_id}
        external = set(act_recip)
        if external - set(expected_emails):
            return False
        # An email not sent externally must arrive as its user's id (workspace-restricted channel).
        unmatched = [e for e in expected_emails if e not in external]
        if not unmatched:
            return not other_internal
        if sdk is None or not other_internal:
            return False
        # One lookup per email: a bulk lookup returns only the users that exist, hiding a missing one.
        ids_per_email = [_resolve_internal_recipient_ids(sdk, [email]) for email in unmatched]
        return all(ids_per_email) and other_internal == set().union(*ids_per_email)
    if set(expected_emails) == set(act_recip):
        return True
    if sdk is not None and act_internal:
        internal_recipient_ids = _resolve_internal_recipient_ids(sdk, expected_emails)
        if internal_recipient_ids & set(act_internal):
            return True
    return False


def generate_simulated_alert_response(
    agent_message: str,
    expected: CatalogMetricAlert,
    conversation_history: list,
    question: str = "",
    current_user_id: str | None = None,
) -> str:
    """Stateful sim-user reply for alert-skill conversation (gpt-4o).

    ``question`` is the fixture's original request. The sim-user is first called with an empty
    history — the opening question went straight to the agent, never to the sim-user — so
    without it rule 5's "the filters your original request implies" refers to text the model
    cannot see. Optional (defaults to "") to keep the signature backwards compatible.

    ``current_user_id`` lets the sim-user recognise itself as the recipient of a "me" alert.
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
    if not expected.expect_alert:
        return _ask_simulated_user(
            openai_client, _no_alert_sim_user_prompt(question), conversation_history, agent_message
        )

    metric = expected.metric_id or "not specified"
    # Rule 9 lists the values of the `any_of` combinations; rule 1 points there instead of
    # stating the item's own value, which no combination may share.
    in_rule_9 = "one of the combinations in rule 9"
    operator = expected.operator
    # BETWEEN / NOT_BETWEEN carry their value in threshold_from/threshold_to, so `threshold` is
    # None for them. Rule 3 asks the sim-user to verify the threshold, and reporting "not
    # specified" made it demand the agent delete both bounds of a BETWEEN condition — an
    # impossible request that burned every iteration without the alert ever being created.
    threshold: str | float | int
    if any(_states_threshold(a) for a in expected.alternatives):
        threshold = in_rule_9
    elif expected.operator in ("BETWEEN", "NOT_BETWEEN") and (
        expected.threshold_from is not None or expected.threshold_to is not None
    ):
        threshold = f"between {expected.threshold_from} and {expected.threshold_to}"
    elif expected.threshold is not None:
        threshold = expected.threshold
    else:
        threshold = "not specified"
    wants_current_user, emails = _split_current_user(expected.recipients)
    recipient_names = list(emails)
    if wants_current_user:
        user_id_note = f", user id {current_user_id}" if current_user_id else ""
        recipient_names.insert(0, f"me (yourself, the current user{user_id_note})")
    recipients = ", ".join(recipient_names) if recipient_names else "not specified"
    if wants_current_user and not emails:
        # An email given here would make the agent send the alert to it instead of the current user.
        recipients_rule = (
            "4. The alert is for you yourself. Never give an email address and never ask for one to "
            "be added. A proposal whose recipient is you — shown as 'You', the current user or your "
            "own user id — has the correct recipient.\n"
        )
    elif wants_current_user:
        recipients_rule = (
            f"4. Proactively state the email recipients in your first reply: {', '.join(emails)}, "
            "and say the alert should also go to you yourself. A recipient shown as 'You', the "
            "current user or your own user id is you.\n"
        )
    else:
        recipients_rule = (
            "4. Proactively include your email recipient in your first reply. "
            "   Do not wait for the agent to ask — state it alongside the metric and condition answers.\n"
        )
    trigger = expected.trigger
    alternative_filters = any(a.filters is not None for a in expected.alternatives)
    # The combinations' filters replace the item's own, so rule 1 must not state those as well.
    filters = None if alternative_filters else expected.filters

    # "not specified" is the normalizer's stand-in for an absent trigger, which the product
    # persists as its ALWAYS default and `_check_trigger` asserts as ALWAYS. Both the cadence to
    # ask for (rule 6) and the goal text (rule 1) use the resolved value: reporting the raw
    # placeholder made rule 3 treat the trigger as unconstrained, so the sim-user would confirm a
    # ONCE/ONCE_PER_INTERVAL proposal that the assertion then failed.
    trigger_key = "ALWAYS" if trigger in _ALWAYS_TRIGGER_VALUES else trigger
    trigger_request = _TRIGGER_INSTRUCTIONS.get(trigger_key, f"set the trigger to {trigger}")
    if expected.trigger_interval:
        trigger_request += f", with a trigger interval of {expected.trigger_interval}"

    # Three branches, matching the three states of `expected.filters`. `[]` and `None` must not
    # share one: telling the sim-user "you want NO filters" on an unstated expectation makes it
    # refuse filters the request genuinely implies (e.g. "orders from the United States"), which
    # quietly turns that fixture into a weaker test rather than a failing one.
    if alternative_filters:
        filters_rule = (
            "5. The filters you want depend on the combination in rule 9 you accept. Refuse any filter "
            "that is not part of that combination. A combination that names no filters wants only the "
            "filters your original request implies: do not invent a date window it never asked for.\n"
        )
    elif filters:
        filters_rule = (
            f"5. Your alert needs exactly these filters and NOTHING else: {filters}. "
            "If the agent offers, proposes or asks about any further date/time window, "
            "evaluation period or granularity, refuse it and repeat that these are the only "
            "filters you want.\n"
        )
    elif filters == []:
        filters_rule = (
            "5. Your alert must have NO filters and NO date/time window on the metric — it evaluates "
            "over all time. If the agent asks which time period each check should cover, or offers a "
            "choice such as 'last Day / Week / Month', do NOT pick one: reply that you want no date "
            "filter at all, all time.\n"
        )
    else:
        filters_rule = (
            "5. Ask only for the filters your original request implies — do not invent an evaluation "
            "period or date window that was not requested. If the agent offers a choice "
            "such as 'last Day / Week / Month' that your request never mentioned, say you do not want "
            "a date window.\n"
        )

    if operator == "ANOMALY":
        # The fallback keeps the conversation alive when the fixture names no interval -- an
        # anomaly alert cannot be created without one. It is deliberately NOT mirrored into
        # `expected.granularity`: `_check_granularity` asserts only what the fixture stated,
        # and scoring an item against an interval it never asked for is the defect this rule
        # exists to undo.
        granularity = (expected.granularity or AnomalyDetectionGranularity.DAY).value
        period_rule = (
            "7. This is an ANOMALY alert. Anomaly detection REQUIRES a time granularity, and that "
            f"granularity is NOT a date filter. State it in your first reply and repeat it whenever "
            f"asked: use {granularity} granularity. Rule 5 constrains filters on the metric only — it "
            "never applies to this detection interval, so never refuse to give one."
            + (f" Use {expected.sensitivity} sensitivity." if expected.sensitivity else "")
            + (f" Detect on the date dataset {expected.date_dataset_id}." if expected.date_dataset_id else "")
            + "\n"
        )
    elif operator in _RELATIVE_OPERATORS:
        # The item names no comparison date or period; delegating is an answer the agent accepts,
        # refusing loops until the turn budget runs out.
        period_rule = (
            "7. This is a comparison alert: keep the comparison your original request describes. The "
            "agent may need a comparison date and a period length (day, week, month, quarter or "
            "year), and those are NOT a date filter. Rule 5 constrains filters on the metric only — "
            "it never applies to the comparison. If the agent asks which date or which period the "
            "comparison should use, do not refuse and do not name one yourself: hand the choice back, "
            "for example 'Pick whichever date and period fit best.' A proposal's filters may list one "
            "relative date filter for that comparison date: it is the comparison period, not a time "
            "window, so never refuse it.\n"
        )
    else:
        period_rule = (
            "7. Do not invent an evaluation period, a granularity or an 'evaluate each run on a X "
            "basis' instruction your goal never asked for.\n"
        )

    original_request = f'Your original request to the agent was: "{question}"\n' if question else ""
    if expected.setup_turns:
        earlier = " / ".join(f'"{turn}"' for turn in expected.setup_turns)
        original_request = f"Earlier in this conversation you asked: {earlier}.\n" + original_request

    # The agent may offer several metrics and describe one as ignoring filters or counting all
    # time. That reads like rule 5's "no filters ... all time", which made the simulated user
    # pick it. The pick follows the goal's metric whatever its description says, matched by id
    # or by title, and repeats the option as the agent wrote it, so the reply adds no reference
    # the agent did not offer. A fixture names a bare metric id: `_check_metric` compares it as
    # written.
    metric_choice_rule = (
        f"   If the agent offers several metrics to choose from, choose the option for your goal metric "
        f"({expected.metric_id}; the agent may show it by this id or only by its title) and repeat that option "
        "as the agent wrote it. How the agent describes a metric, for example as ignoring filters or counting all "
        "time, never changes which metric you want: rule 5 is about filters on the alert.\n"
        if expected.metric_id
        else ""
    )

    # Only a stated title is enforced: an unstated one is the agent's to choose, and telling the
    # sim-user nothing keeps it from objecting to a generated name.
    title_rule = (
        f'8. The alert must be named exactly "{expected.title}". If a summary or proposal shows a '
        "different name, do NOT confirm: state that exact name and ask the agent to use it.\n"
        if expected.title
        else ""
    )

    system_prompt = (
        "You are a user requesting creation of an alert for a metric from an AI agent. "
        "Respond naturally but always steer toward the exact values you were given.\n"
        + original_request
        + "Rules you MUST follow:\n"
        f"1. Your goal: metric={metric}, operator={operator}, threshold={threshold}, "
        f"recipients={recipients}, trigger={trigger_key}"
        + (f", filters={filters}" if filters else "")
        + (f", sensitivity={expected.sensitivity}" if expected.sensitivity else "")
        + (f", trigger interval={expected.trigger_interval}" if expected.trigger_interval else "")
        + (f", date dataset={expected.date_dataset_id}" if expected.date_dataset_id else "")
        + ".\n"
        + metric_choice_rule
        + "2. Never revert or change a decision that was already confirmed in a previous turn.\n"
        "3. If the agent shows a final summary, an alert proposal or asks for confirmation, check "
        "   ALL of these against your goal: recipients, trigger (how often you are alerted), "
        "   filters / time window, threshold and operator. If ANY of them differs — for example the "
        "   summary says 'once per day/week/month' but your goal is every time, or it lists a date "
        "   filter you never asked for — do NOT confirm: name the wrong field, state the correct "
        "   value and ask the agent to fix it. Say 'Yes, please proceed to create the alert.' ONLY "
        "   when every one of those fields matches your goal.\n"
        "   A field your goal reports as 'not specified' is one you have NO expectation about: "
        "   accept whatever the agent chose for it and never ask for it to be removed.\n"
        + recipients_rule
        + filters_rule
        + f"6. Proactively state how often you want to be alerted in your first reply: {trigger_request}. "
        "   Repeat it if the agent proposes a different cadence.\n"
        + period_rule
        + title_rule
        + _alternatives_rule(expected)
        + "Reply concisely and directly."
    )

    return _ask_simulated_user(openai_client, system_prompt, conversation_history, agent_message)


def _states_threshold(option: CatalogMetricAlert) -> bool:
    return option.threshold is not None or option.threshold_from is not None or option.threshold_to is not None


def _alternatives_rule(expected: CatalogMetricAlert) -> str:
    """Rule 9: the combinations an `any_of` item accepts, by their threshold and filters.

    Options differ in nothing else (``_ANY_OF_FIELDS``), so rules 1-8 state every other field.
    """
    if not expected.alternatives:
        return ""
    combinations: list[str] = []
    for letter, option in zip(_COMBINATION_LABELS, expected.alternatives, strict=False):
        parts: list[str] = []
        if option.threshold is not None:
            parts.append(f"threshold={option.threshold}")
        if option.threshold_from is not None or option.threshold_to is not None:
            parts.append(f"threshold=between {option.threshold_from} and {option.threshold_to}")
        if option.filters is not None:
            parts.append(f"filters={json.dumps(option.filters)}" if option.filters else "filters=no filter at all")
        # Never empty: options differ only in threshold and filters, and never repeat one another.
        combinations.append(f"{letter}) " + ", ".join(parts))
    return (
        "9. Your goal can be met by any ONE of these combinations: "
        + " | ".join(combinations)
        + ". A value a combination names replaces the value rules 1-8 give for that field. "
        "Accept a proposal only when it matches one combination in full. If it mixes fields of "
        "different combinations or matches none, do NOT confirm: ask for the combination closest to "
        "what the agent proposed. Never name a value yourself unless the agent asks for one.\n"
    )


def _ask_simulated_user(openai_client: Any, system_prompt: str, conversation_history: list, agent_message: str) -> str:
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


def _no_alert_sim_user_prompt(question: str) -> str:
    """The simulated user of an item whose request names nothing the workspace can monitor.

    It never accepts a substitute: the check is whether the agent proposes one anyway.
    """
    return (
        "You are a user who asked an AI agent to create an alert.\n"
        f'Your original request to the agent was: "{question}"\n'
        "The workspace may not have what you asked for. Rules you MUST follow:\n"
        "1. You want an alert only on exactly what you asked for. Never accept a different or similar metric, "
        "never ask the agent to create a new metric, and never confirm an alert proposal.\n"
        "2. If the agent offers alternatives or asks which one to use, decline them all and say you only wanted "
        "what you asked for.\n"
        "3. If the agent says it cannot create the alert, accept that and end politely.\n"
        "Reply concisely and directly."
    )


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
    attributes_correct: bool = True
    granularity_correct: bool = True
    # ``None``: the item states no such expectation, so the check is neither scored nor gated.
    comparison_correct: bool | None = None
    title_correct: bool | None = None
    dashboard_correct: bool | None = None
    alert_sensitivity_correct: bool | None = None
    alert_trigger_interval_correct: bool | None = None
    alert_date_dataset_correct: bool | None = None
    # Scored on the first proposal, before the simulated user could correct it.
    alert_initial_filters_correct: bool | None = None
    alert_initial_recipients_correct: bool | None = None
    # Set only for an item that expects no alert; then it is the run's one check.
    alert_not_proposed: bool | None = None

    def checks(self) -> dict[str, bool]:
        """Every check that ran, by name; strict_pass requires all of them.

        The conditional checks are left out when unasserted, so an item that names no title does
        not report a ``title_correct`` it was never scored on, and a refusal on it is not counted
        as a title failure.
        """
        if self.alert_not_proposed is not None:
            return {_NO_ALERT_CHECK: self.alert_not_proposed}
        ran: dict[str, bool] = {name: getattr(self, name) for name in _ALERT_CHECKS}
        for name in _CONDITIONAL_ALERT_CHECKS:
            value = getattr(self, name)
            if value is not None:
                ran[name] = value
        return ran

    @property
    def strict_pass(self) -> bool:
        return all(self.checks().values())


@dataclass
class AlertRunResult:
    """Outcome of one K-run conversation for alert creation."""

    conversation_id: str
    alert_id: str | None
    eval: AlertEvaluation
    actual_alert_arguments: dict
    total_turns: int = 0
    total_steps: int = 0
    reasoning_steps: list[str] = field(default_factory=list)
    response_id: str | None = None
    tool_call_events: list[ToolCallEvent] = field(default_factory=list)
    reasoning_step_events: list[ReasoningStepEvent] = field(default_factory=list)
    # Why the simulated-user loop stopped, and how many turns it took. Without these a run
    # that ran out of turns is indistinguishable from one that refused: both land on
    # alert_created=False, and every downstream check is `alert_created and ...`, so both
    # also report operator/threshold/metric/recipients as False.
    exit_reason: LoopExit = LoopExit.BUDGET_EXHAUSTED
    turns_used: int = 0
    # This run's own wall time, across all its turns -- mirrors the single-shot
    # path's best_run_latency_s (see core/runner.py's _run_one_item).
    run_latency_s: float = 0.0


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


_NO_GROUPING_MARKERS = ("none", "no grouping")


def _normalize_expected_attributes(expected: dict) -> list | None:
    """
    * ``Attributes`` list        -> that list (exact expectation)
    * "None" / "no grouping"     -> ``[]``   (stated: no group-by; extras fail)
    * absent, or other prose     -> ``None`` (unstated; grouping not asserted)

    A date narrows an alert as a group-by as well as a filter, and a group-by makes it fire
    per period value instead of on the latest one — so ``[]`` has to be expressible separately
    from "absent", exactly as it is for ``filters``.

    The simulated user is told nothing about groupings, so a non-empty expectation requires the
    item's own question to request that grouping; ``[]`` needs no such support, because the
    simulated user does not invent a grouping and the check verifies it did not.
    """
    attributes = _case_insensitive_get(expected, "attributes")
    if isinstance(attributes, list):
        # Validated here so a malformed fixture fails before the run spends an API call.
        _attribute_label_ids(attributes, side="expected")
        return attributes
    if attributes is None:
        return None
    if isinstance(attributes, str):
        return [] if any(kw in attributes.lower() for kw in _NO_GROUPING_MARKERS) else None
    raise ValueError(f"Attributes expectation must be a list or a display string, got {type(attributes).__name__}")


def _normalize_expected_comparison(expected: dict) -> dict[str, str | int | float | None] | None:
    """
    * ``Comparison`` object       -> its stated properties, keyed by tool-argument name
    * "None" / "no comparison"    -> ``{"comparison_kind": None}`` (stated: no comparison)
    * absent, empty, or prose     -> ``None`` (unstated; comparison not asserted)

    Each property of the object is asserted only when it carries a value, so an item can pin
    the comparison kind without also pinning the date dataset the agent may pick.
    """
    comparison = _case_insensitive_get(expected, "comparison")
    if comparison is None:
        return None
    if isinstance(comparison, str):
        return {"comparison_kind": None} if any(kw in comparison.lower() for kw in _NO_COMPARISON_MARKERS) else None
    if not isinstance(comparison, dict):
        raise ValueError(f"Comparison expectation must be an object or a display string, got {comparison!r}")
    stated: dict[str, str | int | float | None] = {}
    for key, value in comparison.items():
        name = str(key).strip().lower()
        arg = _COMPARISON_ARGS.get(name) or (name if name in _COMPARISON_ARGS.values() else None)
        if arg is None:
            # Validated here so a misspelled property fails before the run spends an API call.
            raise ValueError(f"Unrecognised comparison property {key!r}; expected one of {sorted(_COMPARISON_ARGS)}")
        if arg in _COMPARISON_ID_ARGS and value is not None and not isinstance(value, str):
            # str() would turn ["net_sales_goal"] into an id no tool argument can ever equal.
            raise ValueError(f"Comparison {key} must be an object id string, got {value!r}")
        canonical = _canonical_comparison_value(arg, value)
        if canonical is None and arg == "comparison_periods_ago" and str(value or "").strip():
            raise ValueError(f"Comparison periods_ago must be a number, got {value!r}")
        if canonical is not None:
            stated[arg] = canonical
    return stated or None


def _normalize_expected_text(expected: dict, *keys: str) -> str | None:
    """A stated string expectation, or ``None`` when absent or blank (unasserted)."""
    value = _case_insensitive_get(expected, *keys)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{keys[0]} expectation must be a string, got {value!r}")
    return value.strip() or None


def _normalize_expected_dashboard(expected: dict) -> str | None:
    """
    * ``dashboard_id``            -> that id
    * ``Dashboard`` "Title (id)"  -> the id in the trailing parentheses, as ``Metric`` is read
    * absent / empty              -> ``None`` (unstated; binding not asserted)

    A ``Dashboard`` without a trailing ``(id)`` raises: a title alone can never equal the
    ``dashboard_id`` the tool receives, so the item would fail on every run.
    """
    dashboard_id = _normalize_expected_text(expected, "dashboard_id")
    if dashboard_id is not None:
        return dashboard_id
    display = _normalize_expected_text(expected, "dashboard")
    if display is None:
        return None
    parsed = _parse_metric_id(display)
    if parsed is None:
        raise ValueError(f'Dashboard expectation must be "Title (id)", got {display!r}; use dashboard_id for a bare id')
    return parsed


def _normalize_expected_enum(expected: dict, allowed: tuple[str, ...], *keys: str) -> str | None:
    """A stated enum value, upper-cased; raises on a value outside ``allowed`` so a typo never reads green."""
    value = _normalize_expected_text(expected, *keys)
    if value is None:
        return None
    canonical = value.upper()
    if canonical not in allowed:
        raise ValueError(f"{keys[0]} expectation must be one of {list(allowed)}, got {value!r}")
    return canonical


def _normalize_expect_alert(expected: dict) -> bool:
    """``Expect alert: false`` marks an item whose request must end without any alert."""
    value = _case_insensitive_get(expected, "expect_alert", "expect alert")
    if value is None:
        return True
    if not isinstance(value, bool):
        raise ValueError(f"expect_alert must be true or false, got {value!r}")
    if not value:
        stated = sorted(k for k in expected if str(k).strip().lower() in _ALERT_ONLY_KEYS)
        if stated:
            raise ValueError(f"expect_alert: false states no alert, but the item also states {stated}")
    return value


def _normalize_setup_turns(expected: dict) -> tuple[str, ...]:
    """Messages sent before the question; each one a non-empty string."""
    turns = _case_insensitive_get(expected, "setup_turns", "setup turns")
    if turns is None:
        return ()
    if not isinstance(turns, list) or not all(isinstance(t, str) and t.strip() for t in turns):
        raise ValueError(f"setup_turns must be a list of non-empty strings, got {turns!r}")
    return tuple(turns)


def _normalize_check_first_proposal(
    expected: dict, *, filters_stated: bool, recipients_stated: bool
) -> tuple[str, ...]:
    """Fields also scored on the first proposal; each must be one the item states."""
    value = _case_insensitive_get(expected, *_CHECK_FIRST_PROPOSAL_KEYS)
    if value is None:
        return ()
    if not isinstance(value, list) or not value or any(field not in _FIRST_PROPOSAL_FIELDS for field in value):
        raise ValueError(
            f"check_first_proposal must be a non-empty list of {list(_FIRST_PROPOSAL_FIELDS)}, got {value!r}"
        )
    if "filters" in value and not filters_stated:
        raise ValueError("check_first_proposal names filters, but the item states no filter expectation")
    if "recipients" in value and not recipients_stated:
        raise ValueError("check_first_proposal names recipients, but the item states no recipients")
    return tuple(dict.fromkeys(value))


_ANY_OF_KEYS = ("any_of", "any of")
_CHECK_FIRST_PROPOSAL_KEYS = ("check_first_proposal", "check first proposal")
# Keys that describe the item, not one possible alert, so an `any_of` option may not state them.
_ITEM_LEVEL_KEYS = (
    *_ANY_OF_KEYS,
    *_CHECK_FIRST_PROPOSAL_KEYS,
    "setup_turns",
    "setup turns",
    "expect_alert",
    "expect alert",
)
# Spellings of the filter expectation; an option stating one replaces all of them.
_FILTER_KEYS = ("filters", "time window/filters", "time_window")
# Every group of spellings the normalizer reads as one field; an option stating one spelling
# replaces the whole group, or the item's other spelling would be read instead of the option's.
_KEY_SPELLINGS = (
    _FILTER_KEYS,
    ("recipients", "recipient(s)"),
    ("metric_id", "metric"),
    ("dashboard_id", "dashboard"),
    ("granularity", "detection granularity"),
    ("trigger_interval", "trigger interval"),
    ("date_dataset_id", "date dataset"),
)


def _merge_option(base: dict, option: dict) -> dict:
    """``base`` with ``option``'s keys replacing the same keys, compared case-insensitively."""
    replaced = {str(k).strip().lower() for k in option}
    for spellings in _KEY_SPELLINGS:
        if replaced & set(spellings):
            replaced |= set(spellings)
    return {**{k: v for k, v in base.items() if str(k).strip().lower() not in replaced}, **option}


def _normalize_expected_output(expected: dict) -> CatalogMetricAlert:
    """Parse expected_output into CatalogMetricAlert; ``any_of`` lists complete alternatives.

    Each ``any_of`` option replaces some fields of the item (``Threshold``, ``Filters``, ...) and
    keeps the rest, so fields that must agree (a threshold and the period it is measured over)
    are matched together, never one from each option.
    """
    options = _case_insensitive_get(expected, *_ANY_OF_KEYS)
    if options is None:
        return _normalize_single_expectation(expected)
    if not isinstance(options, list) or len(options) < 2 or not all(isinstance(o, dict) and o for o in options):
        raise ValueError(f"any_of must list at least two non-empty objects, got {options!r}")
    if len(options) > len(_COMBINATION_LABELS):
        raise ValueError(f"any_of lists {len(options)} options; the simulated user is told at most 26")
    for option in options:
        item_level = sorted(k for k in option if str(k).strip().lower() in _ITEM_LEVEL_KEYS)
        if item_level:
            raise ValueError(f"an any_of option may not state {item_level}; state them once for the item")
    base = {k: v for k, v in expected.items() if str(k).strip().lower() not in _ANY_OF_KEYS}
    if _normalize_expect_alert(base) is False:
        raise ValueError("expect_alert: false states no alert, so it cannot list alternatives")
    alternatives = tuple(_normalize_single_expectation(_merge_option(base, option)) for option in options)
    _validate_alternatives(alternatives)
    # The item is what the options share, not the base parsed on its own: the base alone may be
    # incomplete (a trigger interval whose trigger only the options give), and a value every
    # option replaces is no longer the goal. A field the options disagree on keeps its default;
    # rule 9 states it per combination.
    shared = {
        f.name: getattr(alternatives[0], f.name)
        for f in dataclasses.fields(CatalogMetricAlert)
        if all(getattr(a, f.name) == getattr(alternatives[0], f.name) for a in alternatives[1:])
    }
    return dataclasses.replace(CatalogMetricAlert(**shared), alternatives=alternatives)


def _validate_alternatives(alternatives: tuple[CatalogMetricAlert, ...]) -> None:
    """Reject `any_of` options the simulated user could not tell apart or that would accept anything."""
    exempt = (*_ANY_OF_FIELDS, "alternatives")
    differing = sorted(
        f.name
        for f in dataclasses.fields(CatalogMetricAlert)
        if f.name not in exempt and any(getattr(a, f.name) != getattr(alternatives[0], f.name) for a in alternatives)
    )
    if differing:
        # Rules 1-8 state each other field once; the simulated user never sees a proposal's
        # group-by at all. A field that differs would be asked for one way and scored another.
        raise ValueError(f"any_of options may differ only in threshold and filters, not in {differing}")
    for name, states in (("Threshold", _states_threshold), ("Filters", lambda a: a.filters is not None)):
        if len({states(a) for a in alternatives}) > 1:
            # An option without it inherits an unstated base and accepts any value: the mix any_of blocks.
            raise ValueError(f"every any_of option must state {name}, or none may (Filters: [] means no filter)")
    for i, option in enumerate(alternatives):
        # A misspelled key ("Thresold") is ignored, which often leaves two options the same.
        if option in alternatives[:i]:
            raise ValueError(f"any_of option {i + 1} repeats an earlier one; is one of its keys misspelled?")


def _normalize_single_expectation(expected: dict) -> CatalogMetricAlert:
    """Parse one expectation, accepting display-format or internal-format keys."""
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
    recipients = [_CURRENT_USER_RECIPIENT if str(r).strip().lower() in _CURRENT_USER_MARKERS else r for r in recipients]

    filters = _normalize_expected_filters(expected)
    attributes = _normalize_expected_attributes(expected)

    granularity = AnomalyDetectionGranularity.parse(
        _case_insensitive_get(expected, "granularity", "detection granularity")
    )
    comparison = _normalize_expected_comparison(expected)
    title = _normalize_expected_text(expected, "title")
    dashboard_id = _normalize_expected_dashboard(expected)
    expect_alert = _normalize_expect_alert(expected)
    sensitivity = _normalize_expected_enum(expected, _SENSITIVITIES, "sensitivity")
    trigger_interval = _normalize_expected_enum(expected, _TRIGGER_INTERVALS, "trigger_interval", "trigger interval")
    date_dataset_id = _normalize_expected_text(expected, "date_dataset_id", "date dataset")
    setup_turns = _normalize_setup_turns(expected)
    check_first_proposal = _normalize_check_first_proposal(
        expected, filters_stated=filters is not None, recipients_stated=bool(recipients)
    )
    if trigger_interval is not None and trigger != "ONCE_PER_INTERVAL":
        raise ValueError(f"trigger_interval applies only to the ONCE_PER_INTERVAL trigger, got trigger {trigger!r}")
    # Both are ANOMALY arguments. On any other operator the agent sends neither, so a stated
    # MEDIUM would always match the default and only raise the quality score.
    if (sensitivity is not None or date_dataset_id is not None) and operator != "ANOMALY":
        raise ValueError(f"sensitivity and date_dataset_id apply only to the ANOMALY operator, got {operator!r}")

    return CatalogMetricAlert(
        operator=operator,
        threshold=threshold,
        threshold_from=threshold_from,
        threshold_to=threshold_to,
        trigger=trigger,
        metric_id=metric_id,
        recipients=recipients,
        filters=filters,
        attributes=attributes,
        granularity=granularity,
        comparison=comparison,
        title=title,
        dashboard_id=dashboard_id,
        expect_alert=expect_alert,
        sensitivity=sensitivity,
        trigger_interval=trigger_interval,
        date_dataset_id=date_dataset_id,
        setup_turns=setup_turns,
        check_first_proposal=check_first_proposal,
    )


def _alert_call_failed(result: dict | None) -> bool:
    """Whether a ``create_metric_alert`` result reports an error, so the call created nothing.

    An MCP error carries ``isError``. gen-ai's tool registry reports rejected arguments and a
    failed execution as ``{"success": false, "error": ...}`` instead, with no ``isError``.
    """
    if not isinstance(result, dict):
        return False
    data = result.get("data")
    payloads = [result, data] if isinstance(data, dict) else [result]
    return any(p.get("isError") or p.get("success") is False for p in payloads)


def _created_alert_id(result: dict | None) -> str | None:
    """Server-assigned id of the automation a call created: it lives in the result, not the arguments."""
    if not isinstance(result, dict):
        return None
    data = result.get("data")
    alert_id = result.get("id") or (data.get("id") if isinstance(data, dict) else None)
    return alert_id if isinstance(alert_id, str) and alert_id else None


@dataclass
class _AlertCalls:
    """Every ``create_metric_alert`` call of a turn, read for scoring and for cleanup."""

    called: bool = False
    """The agent called the tool at least once."""
    created: bool = False
    """At least one call did not report an error."""
    created_ids: list[str] = field(default_factory=list)
    """Ids of every alert the calls created; each one is deleted after the run."""
    args: dict = field(default_factory=dict)
    """Arguments of the first call that did not fail, else of the last call."""
    alert_id: str | None = None
    """Id of the alert the call in ``args`` created, None when that call failed or its result has no id."""


def _extract_alert_calls(tool_call_events: list[ToolCallEvent]) -> _AlertCalls:
    """Read every ``create_metric_alert`` call of a turn.

    The agent may retry after an error. A call that failed created nothing, so the run is scored
    on the first call that did not fail, and the id of every alert a call created is collected so
    that alert is deleted after the run.
    """
    calls = _AlertCalls()
    for tc in tool_call_events:
        if tc.function_name != "create_metric_alert":
            continue
        calls.called = True
        args = tc.parsed_arguments() or {}
        result = tc.parsed_result()
        if _alert_call_failed(result):
            if not calls.created:
                calls.args = args
            continue
        alert_id = _created_alert_id(result)
        if alert_id is not None:
            calls.created_ids.append(alert_id)
        if not calls.created:
            calls.created = True
            calls.args, calls.alert_id = args, alert_id
    return calls


def render_alert_proposal(proposal: dict) -> str:
    """Render an alert-proposal part as the text the simulated user reacts to.

    The alert skill's confirmation step deliberately emits no text part (GDAI-2032) — the
    prompt and the CTA live only in the proposal payload, which the frontend renders as a
    widget. Dumping the payload (rather than prose) keeps recipients, condition, trigger,
    filters and dashboard visible so the simulated user can still verify them against its
    goal, and does not need updating whenever ``AlertProposal`` grows a field.
    """
    cta = proposal.get("cta") or "Should I create this alert?"
    summary = {k: v for k, v in proposal.items() if k != "cta"}
    alert = dict(summary.get("alert") or {})
    # `execution` is the only place a proposal carries its filters, which rule 3 of the simulated
    # user checks. Hoisting them keeps them visible. The rest stays out: the measures
    # repeat `condition`, and the simulated user is told nothing about group-bys, so a date
    # group-by would only read as a time window rule 5 tells it to refuse.
    execution = alert.pop("execution", None)
    if isinstance(execution, dict):
        alert["filters"] = execution.get("filters") or []
    if "alert" in summary:
        # Key off presence, not truthiness: an alert whose only key was `execution` must
        # still be replaced, otherwise the original (execution-bearing) dict survives.
        summary["alert"] = alert
    return f"{cta}\n\nAlert proposal:\n{json.dumps(summary, indent=2, sort_keys=True)}"


def render_turn_for_simulated_user(chat_result: ChatResult) -> str:
    """Render the whole agent turn the simulated user answers: prose, every other part, and the last proposal.

    A ``clarifyingQuestions`` part carries the options the agent asks the user to pick from, so the
    simulated user cannot answer a question whose options it never reads.
    """
    chunks = [render_answer_text(chat_result)]
    if chat_result.alert_proposals:
        chunks.append(render_alert_proposal(chat_result.alert_proposals[-1]))
    return "\n\n".join(chunk for chunk in chunks if chunk)


def _first_proposal(turns: list[list[ToolCallEvent]]) -> tuple[dict, dict] | None:
    """Arguments and result of the first proposal the user was shown, or None when none succeeded.

    ``turns`` holds the tool calls of each scored turn, in order. The user sees only the last
    proposal of a turn, so a proposal the agent replaced within the same turn is not the answer.

    The result carries the proposal's filters in the AFM form ``create_metric_alert`` receives
    (``afm_filters``, empty when left out), the same form the expectation is written in.
    """
    for events in turns:
        shown: tuple[dict, dict] | None = None
        for tc in events:
            if tc.function_name != _PROPOSAL_TOOL:
                continue
            result = tc.parsed_result()
            # gen-ai's result always names the stored proposal; its filters default to none.
            if isinstance(result, dict) and result.get("success") is not False and result.get("alert_proposal_ref"):
                shown = _parsed_arguments(tc), result
        if shown is not None:
            return shown
    return None


def _proposal_recipient_args(proposal_args: dict) -> dict:
    """A proposal's recipient list as the ``create_metric_alert`` arguments `_check_recipients` reads.

    The list may arrive JSON-encoded as a string, as the create tool's recipient lists do.
    """
    raw = proposal_args.get("recipients")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except ValueError:
            raw = None
    recipients = [r for r in raw if isinstance(r, dict)] if isinstance(raw, list) else []
    return {
        "internal_recipients": [r["id"] for r in recipients if r.get("id")],
        "external_recipients": [r["email"] for r in recipients if not r.get("id") and r.get("email")],
    }


def _evaluate_first_proposal(
    expected: CatalogMetricAlert,
    turns: list[list[ToolCallEvent]],
    sdk: GoodDataSdk,
    current_user_id: str | None,
) -> tuple[bool | None, bool | None]:
    """(filters, recipients) of the first proposal; ``None`` for a field the item does not name.

    The final alert can be right only because the simulated user corrected the first proposal.
    These checks keep that first answer visible.
    """
    if not expected.check_first_proposal:
        return None, None
    proposal = _first_proposal(turns)
    filters_ok: bool | None = None
    recipients_ok: bool | None = None
    if "filters" in expected.check_first_proposal:
        filters_ok = proposal is not None and _check_filters(
            expected, {"filters": proposal[1].get("afm_filters") or []}
        )
    if "recipients" in expected.check_first_proposal:
        recipients_ok = proposal is not None and _check_recipients(
            expected, _proposal_recipient_args(proposal[0]), sdk=sdk, current_user_id=current_user_id
        )
    return filters_ok, recipients_ok


def _evaluate_alert(
    expected: CatalogMetricAlert,
    actual_args: dict,
    alert_created: bool,
    sdk: GoodDataSdk,
    current_user_id: str | None,
    proposal_turns: list[list[ToolCallEvent]] | None = None,
) -> AlertEvaluation:
    """Score the created alert's arguments; a conditional check is ``None`` when the item states no value.

    ``proposal_turns`` holds the tool calls of each scored turn, read for the first-proposal checks.
    """

    if expected.alternatives:
        # The option the run comes closest to; a full match on any option passes.
        evaluations = [
            _evaluate_alert(option, actual_args, alert_created, sdk, current_user_id, proposal_turns)
            for option in expected.alternatives
        ]
        return max(evaluations, key=lambda ev: (ev.strict_pass, sum(ev.checks().values())))

    def conditional(check: bool | None) -> bool | None:
        return None if check is None else alert_created and check

    initial_filters, initial_recipients = _evaluate_first_proposal(expected, proposal_turns or [], sdk, current_user_id)
    return AlertEvaluation(
        alert_created=alert_created,
        operator_correct=alert_created and expected.operator == actual_args.get("operator"),
        threshold_correct=alert_created and _check_threshold(expected, actual_args),
        trigger_correct=alert_created and _check_trigger(expected, actual_args),
        filters_correct=alert_created and _check_filters(expected, actual_args),
        metric_correct=alert_created and _check_metric(expected, actual_args),
        recipients_correct=alert_created
        and _check_recipients(expected, actual_args, sdk=sdk, current_user_id=current_user_id),
        attributes_correct=alert_created and _check_attributes(expected, actual_args),
        granularity_correct=alert_created and _check_granularity(expected, actual_args),
        comparison_correct=None
        if expected.comparison is None
        else alert_created and _check_comparison(expected, actual_args),
        title_correct=None if expected.title is None else alert_created and _check_title(expected, actual_args),
        dashboard_correct=None
        if expected.dashboard_id is None
        else alert_created and _check_dashboard(expected, actual_args),
        alert_sensitivity_correct=conditional(
            _check_enum_arg(expected.sensitivity, actual_args, "sensitivity", default=_DEFAULT_SENSITIVITY)
        ),
        alert_trigger_interval_correct=conditional(_check_trigger_interval(expected, actual_args)),
        alert_date_dataset_correct=conditional(_check_date_dataset(expected, actual_args)),
        alert_initial_filters_correct=initial_filters,
        alert_initial_recipients_correct=initial_recipients,
    )


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
    user_context: dict | None = None,
) -> AgenticAlertSummary:
    """Run the alert-skill agentic evaluation K times and return a summary."""
    if max_iterations < 1:
        # With no turn the agent never gets the question, and a no-alert item would pass unasked.
        raise ValueError(f"max_iterations must be at least 1, got {max_iterations}")
    expected = _normalize_expected_output(expected_output)
    current_user_id: str | None = None
    # A no-alert item scores no recipients, so it needs no current user. `any_of` options share theirs.
    if expected.expect_alert and _CURRENT_USER_RECIPIENT in expected.recipients:
        current_user_id = _resolve_current_user_id(host, token)
        if current_user_id is None:
            # A harness fault: report it as an item error, not as the agent's recipient mistake.
            raise RuntimeError("Cannot score a current-user alert: the token owner's user id could not be resolved")
    run_results: list[AlertRunResult] = []
    client = ChatClient(
        host=host,
        token=token,
        workspace_id=workspace_id,
        reasoning_effort=reasoning_effort,
        agent_id=agent_id,
        user_context=user_context,
    )
    sdk = GoodDataSdk.create(host, token)

    def _run_once(conv_id: str) -> AlertRunResult:
        alert_ids_to_delete: list[str] = []
        # A metric the agent created stays in the shared workspace, and the item's next run would find it.
        metric_ids_to_delete: list[str] = []

        def _track_writes(events: list[ToolCallEvent]) -> _AlertCalls:
            """The turn's alert calls; records every alert and metric it created for cleanup."""
            calls = _extract_alert_calls(events)
            alert_ids_to_delete.extend(calls.created_ids)
            metric_ids_to_delete.extend(_extract_created_metric_ids(events))
            return calls

        # Taken before the run, so cleanup by a named id never touches an alert the run did not create.
        existing_ids = _automation_ids(host, token, workspace_id)
        all_tool_call_events: list[ToolCallEvent] = []
        # Tool calls of each question and follow-up turn; setup turns are not scored.
        scored_turns: list[list[ToolCallEvent]] = []
        # Events of turns that broke mid-stream: not part of the run's record, but they can name an alert.
        partial_events: list[ToolCallEvent] = []
        run_started = time.monotonic()
        try:
            alert_id: str | None = None
            actual_args: dict = {}
            alert_created = False
            reasoning_steps: list[str] = []
            response_id: str | None = None
            all_reasoning_step_events: list[ReasoningStepEvent] = []
            turn_offset = 0.0  # each turn's call_ts/ts restarts near 0 -- shift by prior turns' wall time
            tool_index_offset = 0
            reasoning_index_offset = 0
            # conversation_history stores prior turns for GPT-4o context.
            # Roles follow GPT-4o's perspective: "assistant"=agent text, "user"=sim-user reply.
            conversation_history: list = []
            current_question = question
            turns = 0
            steps = 0

            # Defaults to BUDGET_EXHAUSTED: every other exit sets it explicitly, so a loop
            # that simply runs out of range() is correctly labelled without a trailing else.
            exit_reason = LoopExit.BUDGET_EXHAUSTED
            turns_used = 0
            no_alert = not expected.expect_alert
            # A no-alert run ends when the agent proposes anything; the simulated user only declines.
            iterations = min(max_iterations, _NO_ALERT_MAX_ITERATIONS) if no_alert else max_iterations
            proposed = False
            # Whether the agent wrote anything in a scored turn; a no-alert run may end quiet after declining.
            answered = False
            run_started = time.monotonic()
            # Setup turns set the scene (a chart to alert on) and are not scored. A failed one
            # ends the run as the agent's failure, like a failed question turn.
            for number, turn in enumerate(expected.setup_turns, start=1):
                try:
                    setup = client.send_message(conv_id, turn)
                except ChatError as exc:
                    print(f"[CHAT] setup turn {number} failed for conversation {conv_id}: {exc}")
                    # A broken stream can still have created an alert server-side.
                    partial = exc.partial_result
                    if partial is not None:
                        reasoning_steps.extend(partial.reasoning_steps or [])
                        response_id = partial.response_id or response_id
                        _track_writes(partial.tool_call_events or [])
                        partial_events.extend(partial.tool_call_events or [])
                    exit_reason = chat_failure_exit(exc)
                    iterations = 0
                    break
                steps += setup.reasoning_step_count
                reasoning_steps.extend(setup.reasoning_steps or [])
                turn_offset, tool_index_offset, reasoning_index_offset = shift_and_index_events(
                    setup,
                    turn_offset=turn_offset,
                    tool_index_offset=tool_index_offset,
                    reasoning_index_offset=reasoning_index_offset,
                )
                all_tool_call_events.extend(setup.tool_call_events or [])
                all_reasoning_step_events.extend(setup.reasoning_step_events or [])
                _track_writes(setup.tool_call_events or [])
                conversation_history.append({"role": "user", "content": turn})
                conversation_history.append({"role": "assistant", "content": render_answer_text(setup)})
            for _iteration in range(iterations):
                turns_used = _iteration + 1
                try:
                    chat_result = client.send_message(conv_id, current_question)
                except ChatError as exc:
                    # Without this the exception escapes run_agentic_alert_skill entirely,
                    # discarding every K-run already completed along with any exit_reason.
                    print(f"[CHAT] send_message failed for conversation {conv_id}: {exc}")
                    # The stream can break AFTER create_metric_alert already succeeded
                    # server-side. That id only ever reached alert_ids_to_delete from the
                    # normal path below, so breaking here left the alert in the workspace for
                    # the `finally` cleanup to miss -- a real object leaking out of a failed
                    # run, not a reporting gap.
                    partial = exc.partial_result
                    if partial is not None:
                        reasoning_steps.extend(partial.reasoning_steps or [])
                        response_id = partial.response_id or response_id
                        _track_writes(partial.tool_call_events or [])
                        partial_events.extend(partial.tool_call_events or [])
                    exit_reason = chat_failure_exit(exc)
                    break
                # `turns_used` counts attempts (set above, so a failed send still shows the
                # loop reached this iteration); `turns`/`steps` count completed work, so they
                # advance only once send_message has actually returned.
                turns += 1
                steps += chat_result.reasoning_step_count
                reasoning_steps.extend(chat_result.reasoning_steps or [])
                response_id = chat_result.response_id or response_id
                turn_offset, tool_index_offset, reasoning_index_offset = shift_and_index_events(
                    chat_result,
                    turn_offset=turn_offset,
                    tool_index_offset=tool_index_offset,
                    reasoning_index_offset=reasoning_index_offset,
                )
                all_tool_call_events.extend(chat_result.tool_call_events or [])
                scored_turns.append(list(chat_result.tool_call_events or []))
                all_reasoning_step_events.extend(chat_result.reasoning_step_events or [])
                calls = _track_writes(chat_result.tool_call_events or [])
                tools_called = {tc.function_name for tc in chat_result.tool_call_events or []}
                substitute = _PROPOSAL_TOOL in tools_called or _CREATE_METRIC_TOOL in tools_called
                if no_alert and (calls.called or substitute or chat_result.alert_proposals):
                    # Nothing in the request can be monitored, so any proposal is a substitute the
                    # user never agreed to. A proposal call the tool rejected leaves no proposal
                    # part, but the agent still tried to propose one. A metric the agent creates
                    # is a substitute too: the simulated user never asks for one.
                    proposed = True
                    actual_args = calls.args
                    exit_reason = LoopExit.SUCCESS
                    break
                if calls.created:
                    alert_id, actual_args = calls.alert_id, calls.args
                    alert_created = True
                    exit_reason = LoopExit.SUCCESS
                    break
                if calls.called:
                    # Every call reported an error, so nothing was created. Scoring their arguments
                    # would pass a run whose creation failed, and ending here would label it a
                    # success. The agent gets the next turn to recover, as with a user, and the
                    # failed arguments are kept for triage.
                    actual_args = calls.args
                response_text = render_turn_for_simulated_user(chat_result)
                # Stop if the agent gave a completely empty response (stuck), or wrote nothing after
                # every create call failed: the rendered turn holds no tool results, so the simulated
                # user would be asked to answer an empty message.
                if not response_text and (calls.called or not chat_result.tool_call_events):
                    exit_reason = LoopExit.AGENT_SILENT
                    break
                answered = answered or bool(response_text)
                # Stop before generating a follow-up for the last iteration
                if _iteration >= iterations - 1:
                    break
                # Recorded rather than raised, matching metric_skill and kda_skill. Letting it
                # propagate did keep a harness fault from being scored as a content failure,
                # but it also discarded the K-runs already completed -- and SIMULATED_USER_FAILED
                # achieves the same separation while keeping them, since reporting reads the
                # exit reason to classify the run as an error rather than an agent failure.
                try:
                    follow_up = generate_simulated_alert_response(
                        response_text,
                        expected,
                        conversation_history,
                        question=question,
                        current_user_id=current_user_id,
                    )
                except Exception as exc:  # noqa: BLE001 -- harness-side fault; end only this run
                    print(f"[SIM-USER] Simulated reply failed for conversation {conv_id}: {exc}")
                    exit_reason = LoopExit.SIMULATED_USER_FAILED
                    break
                # Record this exchange so the next call has full history
                conversation_history.append({"role": "assistant", "content": response_text})
                conversation_history.append({"role": "user", "content": follow_up})
                current_question = follow_up

            if no_alert:
                # Only a run that spent its whole budget without a proposal shows the agent
                # declining. A run cut short by a chat failure or a failed simulated user never
                # gave the agent the turns to propose one. An agent that declined and then had
                # nothing to add to the user's "OK, thanks" ends silent, and that is a decline
                # too; one silent from its first turn never answered the request.
                declined = not proposed and (
                    exit_reason == LoopExit.BUDGET_EXHAUSTED or (exit_reason == LoopExit.AGENT_SILENT and answered)
                )
                ev = AlertEvaluation(
                    alert_created=False,
                    operator_correct=False,
                    threshold_correct=False,
                    trigger_correct=False,
                    filters_correct=False,
                    metric_correct=False,
                    recipients_correct=False,
                    alert_not_proposed=declined,
                )
            else:
                ev = _evaluate_alert(expected, actual_args, alert_created, sdk, current_user_id, scored_turns)
            return AlertRunResult(
                conversation_id=conv_id,
                alert_id=alert_id,
                eval=ev,
                actual_alert_arguments=actual_args,
                total_turns=turns,
                total_steps=steps,
                reasoning_steps=reasoning_steps,
                response_id=response_id,
                tool_call_events=all_tool_call_events,
                reasoning_step_events=all_reasoning_step_events,
                exit_reason=exit_reason,
                turns_used=turns_used,
                run_latency_s=time.monotonic() - run_started,
            )
        finally:
            for created_id in dict.fromkeys(alert_ids_to_delete):
                _delete_alert(sdk, workspace_id, created_id)
            unseen = _named_automation_ids(all_tool_call_events + partial_events) - set(alert_ids_to_delete)
            if unseen and existing_ids is not None:
                now = _automation_ids(host, token, workspace_id) or set()
                for leaked_id in sorted((unseen & now) - existing_ids):
                    print(f"[CLEANUP] Deleting alert {leaked_id}: created, but its create call was not in the turn")
                    _delete_alert(sdk, workspace_id, leaked_id)
            # After the alerts: an alert on a created metric would keep that metric in use.
            for metric_id in dict.fromkeys(metric_ids_to_delete):
                _delete_metric(sdk, workspace_id, metric_id)

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
    # A passing run first: with `any_of`, a failing run scored against a larger option can have
    # more true checks than a passing one.
    best = max(
        run_results,
        key=lambda r: (r.eval.strict_pass, sum(r.eval.checks().values())),
    )
    return AgenticAlertSummary(
        run_results=run_results,
        pass_at_k=pass_at_k,
        pass_power_k=pass_power_k,
        best=best,
    )


class AlertSkillAssertionError(AgenticAssertionError):
    """Raised when an alert-skill evaluation fails."""


def _run_detail(run: AlertRunResult) -> dict:
    """The diagnostic fields for ONE run, shared by the best run and every failing one.

    Extracted so a failing run is described by exactly the same keys as the winning run --
    for this kind that means the full per-field check breakdown and the arguments the run sent.
    """
    return {
        **run.eval.checks(),
        "actual_alert_arguments": run.actual_alert_arguments,
        # Why the loop stopped. alert_created=False alone cannot tell a refusal from a run
        # that hit max_iterations while still on track -- see LoopExit. Per-run rather than
        # best-only: on a failing run it is the first thing worth reading.
        "exit_reason": run.exit_reason.value,
        "turns_used": run.turns_used,
        **timeline_detail(run.tool_call_events, run.reasoning_step_events),
    }


def _failed_checks(run: AlertRunResult) -> list[dict]:
    """The checks this run failed, by name. The arguments the run sent are in its detail.

    Every other check reads False when no alert was created, so then only that one is named.
    """
    return failed_checks_from(run.eval.checks(), prerequisite="alert_created")


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
    submit_trace_link: SubmitTraceLink = run_trace_link_inline,
    user_context: dict | None = None,
    gate: EvalGate = DEFAULT_GATE,
) -> AgenticEvalOutcome:
    """Run alert-skill evaluation, log to Langfuse, and raise AlertSkillAssertionError on failure.

    Returns the best run's outcome (reasoning_steps, conversation_id, response_id) as an
    AgenticEvalOutcome on success; on failure the same three values are attached to the
    raised exception as
    ``.reasoning_steps``/``.conversation_id``/``.response_id`` (mirrors the
    `conversation_id`-on-exception idiom in `ChatClient.ask()`) so callers can retrieve them
    either way.
    """
    identity = RunIdentity(
        host,
        token,
        workspace_id,
        dataset_name,
        run_timestamp,
        model_version_override,
        run_metadata_extra,
        reasoning_effort,
    )
    langfuse, window_start, scope = open_item_trace(langfuse, identity, dataset_item_id, suffix_runs=k > 1)
    with item_scope(scope):
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
            user_context=user_context,
        )

    # Before the Langfuse scores, so an ERROR run gets its marker beside its usual scores.
    run_labels = label_runs(summary.run_results, passed=lambda r: r.eval.strict_pass)

    if langfuse is not None and dataset_item_id:
        # Pinned on the calling thread: a deferred poll must not widen its query window.
        window_end = utc_now()

        def _write_scores(ctx: RunTraceContext) -> None:
            stamp_gate_metadata(ctx.run_metadata, k=len(summary.run_results), gate=gate)

            for run_idx, run in enumerate(summary.run_results):
                pt = ctx.trace(run.conversation_id)
                strict_checks = run.eval.checks()
                with ctx.observe(pt, run_idx, conversation_id=run.conversation_id, output=strict_checks) as tid:
                    if (run_error := run_labels.error_label(run_idx)) is not None:
                        log_eval_error_score(ctx, tid, run_error)
                    for score_name, value in strict_checks.items():
                        ctx.score(tid, name=score_name, value=float(value), data_type="BOOLEAN")
                    ctx.score(tid, name="turns", value=run.total_turns, data_type="NUMERIC")
                    ctx.score(tid, name="steps", value=run.total_steps, data_type="NUMERIC")
                    log_gate_scores(ctx, tid, gate=gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k)
                    ctx.quality(
                        tid,
                        strict_checks=strict_checks,
                        latency_sec=pt.latency if pt else None,
                        cost_usd=pt.total_cost if pt else None,
                    )

        # Before the pass@K raise: a failing item's scores are the ones worth having.
        submit_trace_scoring(
            submit_trace_link,
            identity,
            langfuse=langfuse,
            dataset_item_id=dataset_item_id,
            conversation_ids=[r.conversation_id for r in summary.run_results],
            window_start=window_start,
            window_end=window_end,
            suffix_runs=k > 1,
            write_scores=_write_scores,
            scope=scope,
            item_input=question,
        )

    runs_passed = sum(1 for r in summary.run_results if r.eval.strict_pass)
    runs_effective = len(summary.run_results)

    best = summary.best
    ev = best.eval
    # The checks that ran, not a fixed field list: quality_score is the share of true booleans
    # here, so a no-alert item must not carry the alert checks it was never scored on, and a
    # stated conditional check must count.
    detail = agentic_detail(
        best.tool_call_events,
        best.reasoning_step_events,
        **ev.checks(),
        actual_alert_arguments=best.actual_alert_arguments,
        # Why the loop stopped. alert_created=False alone cannot tell a refusal from a run
        # that hit max_iterations while still on track -- see LoopExit.
        exit_reason=best.exit_reason.value,
        turns_used=best.turns_used,
        max_iterations=max_iterations,
    )
    # Same predicate runs_passed is taken over, so an item's failed_runs and its counts
    # cannot disagree about which runs failed.
    failed_runs = build_failed_runs(
        summary.run_results,
        labels=run_labels,
        detail=_run_detail,
        failed_checks=_failed_checks,
    )

    if not gate_passed(gate, pass_at_k=summary.pass_at_k, pass_power_k=summary.pass_power_k):
        gate_note = failure_message_head(gate, run_labels, runs_passed, failed_runs)
        raise_agentic_failure(
            AlertSkillAssertionError,
            f"Alert skill assertion failed. {gate_note} strict_pass={ev.strict_pass}. "
            f"Checks: {ev.checks()}. "
            f"Actual args: {best.actual_alert_arguments}",
            harness_error=run_labels.harness_error_record,
            shadow=run_labels.shadow(gate),
            reasoning_steps=best.reasoning_steps,
            conversation_id=best.conversation_id,
            response_id=best.response_id,
            detail=detail,
            runs_passed=runs_passed,
            runs_effective=runs_effective,
            failed_runs=failed_runs,
            run_latencies_s=[r.run_latency_s for r in summary.run_results],
            best_run_latency_s=best.run_latency_s,
        )
    return agentic_success(
        shadow=run_labels.shadow(gate),
        reasoning_steps=best.reasoning_steps,
        conversation_id=best.conversation_id,
        response_id=best.response_id,
        detail=detail,
        runs_passed=runs_passed,
        runs_effective=runs_effective,
        failed_runs=failed_runs,
        run_latencies_s=[r.run_latency_s for r in summary.run_results],
        best_run_latency_s=best.run_latency_s,
    )
