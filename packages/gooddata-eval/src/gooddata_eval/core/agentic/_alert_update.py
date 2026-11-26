# (C) 2026 GoodData Corporation. All rights reserved.
"""Update mode of the agentic alert-skill evaluation: the agent changes an alert that exists before the question.

An item in this mode states the alert to set up and the change its question asks for. Each run creates the
alert through the API, asks the question, and compares the stored alert before and after. The asked fields
must hold the new values, and every other field must be unchanged. ``update_metric_alert`` keeps every field
it is not given, so its arguments cannot show a field the update lost on the way. Only the stored alert can.
"""

from __future__ import annotations

import copy
import json
import math
import uuid
from dataclasses import dataclass
from typing import Any, ClassVar

import httpx

# Score names, in report order. An update item publishes these and none of the creation checks.
UPDATE_CHECKS = ("alert_update_called", "alert_update_correct", "alert_update_preserved", "alert_not_recreated")
# Tools that change an existing alert: the condition and settings, and the paused/active state.
UPDATE_TOOLS = ("update_metric_alert", "update_alert_state")

_MODE_UPDATE = "update"
_PAGE_SIZE = 250
# Keys under which an AFM attribute filter lists the elements it selects (`in`/`notIn`).
_ELEMENT_KEYS = ("values", "uris")
# Every setup alert's id starts with this, so a run deletes only alerts an earlier run left.
SETUP_ID_PREFIX = "eval-update-"
_ITEM_KEYS = ("mode", "setup_alert", "expected_change")

_ALERT = ("attributes", "alert")
# Server bookkeeping that every write changes, and the text gen-ai generates from the condition when it
# creates the alert. A correct update may rewrite that text, so it is not compared.
_IGNORED_PATHS = (
    ("attributes", "createdAt"),
    ("attributes", "modifiedAt"),
    ("attributes", "description"),
    ("relationships", "createdBy"),
    ("relationships", "modifiedBy"),
    ("relationships", "automationResults"),
)

_COMPARISON_OPERATORS = (
    "GREATER_THAN",
    "GREATER_THAN_OR_EQUAL_TO",
    "LESS_THAN",
    "LESS_THAN_OR_EQUAL_TO",
    "EQUAL_TO",
    "NOT_EQUAL_TO",
)
_RELATIVE_OPERATORS = ("INCREASES_BY", "DECREASES_BY", "CHANGES_BY")
_TRIGGERS = ("ALWAYS", "ONCE", "ONCE_PER_INTERVAL")
_TRIGGER_DISPLAY = {"EVERY TIME": "ALWAYS", "ONE TIME": "ONCE"}
_TRIGGER_INTERVALS = ("DAY", "WEEK", "MONTH", "QUARTER", "YEAR")
_SENSITIVITIES = ("LOW", "MEDIUM", "HIGH")
_GRANULARITIES = ("HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR")
_STATES = ("ACTIVE", "PAUSED")
_CONDITION_KINDS = ("comparison", "relative", "anomaly", "range")
_ENUMS: dict[str, tuple[str, ...]] = {
    "trigger": _TRIGGERS,
    "trigger_interval": _TRIGGER_INTERVALS,
    "sensitivity": _SENSITIVITIES,
    "granularity": _GRANULARITIES,
    "state": _STATES,
}
# The condition kinds each change applies to; a change missing here applies to every kind.
_KINDS_OF_CHANGE = {
    "threshold": ("comparison", "relative"),
    "operator": ("comparison", "relative"),
    "sensitivity": ("anomaly",),
    "granularity": ("anomaly",),
}
_CHANGE_ALIASES = {"dashboard": "dashboard_id", "interval": "trigger_interval", "name": "title"}
_CHANGES = ("threshold", "operator", "trigger", "trigger_interval", "sensitivity", "granularity", "title", "state")
_CHANGES_WITH_SHAPE = ("filters", "dashboard_id")


@dataclass(frozen=True)
class AlertUpdateExpectation:
    """The alert a run sets up and the change its question asks for."""

    setup_alert: dict[str, Any]
    """The automation entity to create: ``attributes`` and optional ``relationships``, as the API returns them."""
    expected_change: dict[str, Any]
    """New value per changed field, by canonical name (``threshold``, ``trigger``, ``filters``, ...)."""

    @property
    def title(self) -> str:
        return self.setup_alert["attributes"]["title"]

    @property
    def condition_kind(self) -> str:
        return condition_kind(self.setup_alert)


@dataclass
class AlertUpdateEvaluation:
    """Scores of one update run."""

    alert_update_called: bool
    """An update tool call on the setup alert succeeded."""
    alert_update_correct: bool
    """The stored alert holds every value the item expects to change."""
    alert_update_preserved: bool
    """No other field of the stored alert changed."""
    alert_not_recreated: bool
    """The setup alert still exists and the agent created no alert."""

    # The check every other one depends on: without an update call, the others read False.
    prerequisite: ClassVar[str] = "alert_update_called"

    def checks(self) -> dict[str, bool]:
        return {name: getattr(self, name) for name in UPDATE_CHECKS}

    @property
    def strict_pass(self) -> bool:
        return all(self.checks().values())


def _canonical(key: object) -> str:
    return str(key).strip().lower().replace(" ", "_")


def _get(d: dict, *keys: str) -> Any:
    """A value by any of ``keys``, case-insensitively; spaces and underscores are interchangeable."""
    by_name = {_canonical(k): v for k, v in d.items()}
    for key in keys:
        if key in by_name:
            return by_name[key]
    return None


def condition_kind(entity: dict) -> str:
    """``comparison``, ``relative``, ``anomaly`` or ``range``: the one key of the alert condition."""
    condition = ((entity.get("attributes") or {}).get("alert") or {}).get("condition")
    bodies = {k: v for k, v in condition.items() if v is not None} if isinstance(condition, dict) else {}
    if len(bodies) != 1:
        raise ValueError(f"setup_alert must have exactly one alert condition, got {list(bodies)}")
    [(kind, body)] = bodies.items()
    if kind not in _CONDITION_KINDS:
        raise ValueError(f"setup_alert condition must be one of {list(_CONDITION_KINDS)}, got {kind!r}")
    if not isinstance(body, dict):
        raise ValueError(f"setup_alert condition {kind} must be an object, got {body!r}")
    return kind


def _normalize_setup_alert(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"setup_alert must be an automation entity object, got {value!r}")
    unknown = sorted(set(value) - {"attributes", "relationships", "id", "type"})
    if unknown:
        raise ValueError(f"setup_alert takes only attributes and relationships, got {unknown}")
    attributes = value.get("attributes")
    if not isinstance(attributes, dict) or not isinstance(attributes.get("alert"), dict):
        raise ValueError("setup_alert.attributes.alert is required")
    title = attributes.get("title")
    if not isinstance(title, str) or not title.strip():
        # The agent finds the alert by its title, and each run deletes alerts with the same title first.
        raise ValueError("setup_alert.attributes.title is required: it identifies the alert to the agent")
    relationships = value.get("relationships")
    relationships = {} if relationships is None else relationships
    if not isinstance(relationships, dict):
        raise ValueError(f"setup_alert.relationships must be an object, got {relationships!r}")
    entity = {"attributes": copy.deepcopy(attributes), "relationships": copy.deepcopy(relationships)}
    for section, key in _IGNORED_PATHS:
        if key != "description":
            entity[section].pop(key, None)
    condition_kind(entity)
    return entity


def _finite(value: float) -> bool:
    """Whether the scorer can compare ``value`` as a float: not NaN, not infinite, not too large."""
    try:
        return math.isfinite(float(value))
    except OverflowError:
        return False


def _normalize_change(key: str, value: object, kind: str) -> object:
    kinds = _KINDS_OF_CHANGE.get(key)
    if kinds is not None and kind not in kinds:
        raise ValueError(
            f"expected_change.{key} applies only to {' and '.join(kinds)} alerts, the setup alert is {kind}"
        )
    if key == "threshold":
        if isinstance(value, bool) or not isinstance(value, int | float) or not _finite(value):
            raise ValueError(f"expected_change.threshold must be a finite number, got {value!r}")
        return value
    if key == "operator":
        operators = _COMPARISON_OPERATORS if kind == "comparison" else _RELATIVE_OPERATORS
        canonical = str(value).strip().upper()
        if canonical not in operators:
            raise ValueError(f"expected_change.operator must be one of {list(operators)}, got {value!r}")
        return canonical
    if key in _ENUMS:
        canonical = str(value).strip().upper()
        canonical = _TRIGGER_DISPLAY.get(canonical, canonical) if key == "trigger" else canonical
        if canonical not in _ENUMS[key]:
            raise ValueError(f"expected_change.{key} must be one of {list(_ENUMS[key])}, got {value!r}")
        return canonical
    if key == "filters":
        # An empty object would fit any stored filter; `[]` (no filter at all) stays valid.
        if not isinstance(value, list) or not all(isinstance(f, dict) and f for f in value):
            raise ValueError(f"expected_change.filters must be a list of non-empty filter objects, got {value!r}")
        return value
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"expected_change.{key} must be a non-empty string, got {value!r}")
    return value


def update_expectation(expected: dict) -> AlertUpdateExpectation | None:
    """The update expectation of an item in update mode; None only when ``expected`` has no ``mode`` key.

    Raises on a malformed item, so a typo never reads green: a ``mode`` other than ``update`` (null
    included), an unknown key, a change the setup alert cannot take, or a trigger interval without the
    ONCE_PER_INTERVAL trigger.
    """
    # Only an item without the key is a creation item: `mode: null` next to update keys is a typo.
    if "mode" not in {_canonical(k) for k in expected}:
        return None
    mode = _get(expected, "mode")
    if not isinstance(mode, str) or mode.strip().lower() != _MODE_UPDATE:
        raise ValueError(f"mode must be {_MODE_UPDATE!r}, got {mode!r}")
    unknown = sorted(k for k in expected if _canonical(k) not in _ITEM_KEYS)
    if unknown:
        # A creation key next to update mode would be ignored, and the item would read green without it.
        raise ValueError(f"an update item takes only {list(_ITEM_KEYS)}, got also {unknown}")
    setup = _normalize_setup_alert(_get(expected, "setup_alert"))
    kind = condition_kind(setup)
    raw_change = _get(expected, "expected_change")
    if not isinstance(raw_change, dict) or not raw_change:
        raise ValueError(f"expected_change must name at least one field, got {raw_change!r}")
    change: dict[str, Any] = {}
    for raw_key, value in raw_change.items():
        key = _CHANGE_ALIASES.get(_canonical(raw_key), _canonical(raw_key))
        if key not in _CHANGES + _CHANGES_WITH_SHAPE:
            raise ValueError(
                f"expected_change.{raw_key} is not a field update mode checks; use one of "
                f"{list(_CHANGES + _CHANGES_WITH_SHAPE)}"
            )
        if key in change:
            raise ValueError(f"expected_change names {key} twice, the second time as {raw_key!r}")
        change[key] = _normalize_change(key, value, kind)
    if "trigger_interval" in change:
        trigger = change.get("trigger", (setup["attributes"]["alert"].get("trigger") or "").upper())
        if trigger != "ONCE_PER_INTERVAL":
            raise ValueError(f"expected_change.trigger_interval needs the ONCE_PER_INTERVAL trigger, got {trigger!r}")
    return AlertUpdateExpectation(setup_alert=setup, expected_change=change)


def setup_entity(expectation: AlertUpdateExpectation, *, current_user_id: str, channel_id: str | None) -> dict:
    """The entity a run creates: the item's setup alert, sent to the current user over the org's channel.

    An item states neither, so that it runs in any organization: the token owner differs per environment,
    and so do the notification channel ids.
    """
    entity = copy.deepcopy(expectation.setup_alert)
    relationships = entity["relationships"]
    relationships.setdefault("recipients", {"data": [{"id": current_user_id, "type": "user"}]})
    if "notificationChannel" not in relationships and channel_id is not None:
        relationships["notificationChannel"] = {"data": {"id": channel_id, "type": "notificationChannel"}}
    return entity


def needs_channel(expectation: AlertUpdateExpectation) -> bool:
    return "notificationChannel" not in expectation.setup_alert["relationships"]


def _owned_paths(key: str, kind: str, *, keeps_interval: bool = False) -> tuple[tuple[str, ...], ...]:
    """The stored paths a change of ``key`` may rewrite; a difference under any other path is a lost field.

    ``keeps_interval``: the trigger stays ONCE_PER_INTERVAL, so a trigger change must leave the interval as it is.
    """
    condition = (*_ALERT, "condition", kind)
    owned: dict[str, tuple[tuple[str, ...], ...]] = {
        "threshold": ((*condition, "right", "value"),) if kind == "comparison" else ((*condition, "threshold"),),
        "operator": ((*condition, "operator"),),
        # Leaving ONCE_PER_INTERVAL clears the interval, and entering it sets one.
        "trigger": ((*_ALERT, "trigger"),) if keeps_interval else ((*_ALERT, "trigger"), (*_ALERT, "interval")),
        "trigger_interval": ((*_ALERT, "interval"),),
        "sensitivity": ((*condition, "sensitivity"),),
        "granularity": ((*condition, "granularity"),),
        "title": (("attributes", "title"),),
        "state": (("attributes", "state"),),
        # The filter list, the dashboard dialog's record of which filters it shows and hides, and the labels
        # they use. The rest of the metadata, such as the widget the alert was set on, is not the change's.
        "filters": (
            (*_ALERT, "execution", "filters"),
            ("attributes", "metadata", "filters"),
            ("attributes", "metadata", "visibleFilters"),
            ("relationships", "labels"),
        ),
        "dashboard_id": (("relationships", "analyticalDashboard"),),
    }
    return owned[key]


def _at(entity: dict, path: tuple[str, ...]) -> Any:
    node: Any = entity
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def _stored_value(entity: dict, key: str, kind: str) -> Any:
    if key == "dashboard_id":
        return _at(entity, ("relationships", "analyticalDashboard", "data", "id"))
    if key == "threshold" and kind == "relative":
        return _at(entity, (*_ALERT, "condition", kind, "threshold", "value"))
    return _at(entity, _owned_paths(key, kind)[0])


def _contains(expected: object, actual: object) -> bool:
    """Whether ``expected`` is a recursive subset of ``actual``: a filter may carry ids the item omits."""
    if isinstance(expected, dict) and isinstance(actual, dict):
        return all(k in actual and _contains_value(k, v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list) and isinstance(actual, list):
        return len(expected) == len(actual) and all(_contains(e, a) for e, a in zip(expected, actual))
    return expected == actual


def _same_filters(expected: list, actual: object) -> bool:
    """The same filters in any order; each stored filter may add a localIdentifier and defaults.

    One expected filter can fit several stored ones, so every pairing is tried, not the first fit.
    """
    if not isinstance(actual, list) or len(actual) != len(expected):
        return False
    fits = [[i for i, got in enumerate(actual) if _contains(want, got)] for want in expected]
    owner: dict[int, int] = {}
    return all(_assign(fits, want, owner, set()) for want in range(len(fits)))


def _assign(fits: list[list[int]], want: int, owner: dict[int, int], visited: set[int]) -> bool:
    """Give expected filter ``want`` a stored filter, moving earlier owners along an augmenting path."""
    for got in fits[want]:
        if got in visited:
            continue
        visited.add(got)
        if got not in owner or _assign(fits, owner[got], owner, visited):
            owner[got] = want
            return True
    return False


def _change_applied(key: str, expected: Any, stored: Any) -> bool:
    if key == "threshold":
        return (
            isinstance(stored, int | float)
            and not isinstance(stored, bool)
            and math.isclose(float(stored), float(expected), rel_tol=1e-9, abs_tol=1e-12)
        )
    if key == "filters":
        return _same_filters(expected, stored)
    return stored == expected


def _ignored(path: tuple[str, ...], owned: list[tuple[str, ...]]) -> bool:
    return any(path[: len(prefix)] == prefix for prefix in [*_IGNORED_PATHS, *owned])


def _contains_value(key: str, expected: object, actual: object) -> bool:
    # The elements an attribute filter selects are a set: the agent may list them in another order.
    if key in _ELEMENT_KEYS and isinstance(expected, list) and isinstance(actual, list):
        return sorted(map(json.dumps, expected)) == sorted(map(json.dumps, actual))
    return _contains(expected, actual)


def _differences(before: object, after: object, path: tuple[str, ...], out: list[dict]) -> None:
    # An object that appears or disappears is compared field by field, so an owned child such as
    # metadata.visibleFilters can be added to an alert that had no metadata.
    if isinstance(before, dict) and after is None:
        after = {}
    elif before is None and isinstance(after, dict):
        before = {}
    if isinstance(before, dict) and isinstance(after, dict):
        for key in sorted(set(before) | set(after)):
            _differences(before.get(key), after.get(key), (*path, key), out)
    elif before != after:
        # A missing key and a null read the same: the API omits some nulls on one write and not another.
        out.append({"path": ".".join(path), "before": before, "after": after})


def unexpected_changes(expectation: AlertUpdateExpectation, before: dict, after: dict) -> list[dict]:
    """Every stored field that changed although the item did not ask for it, as ``{path, before, after}``."""
    kind = condition_kind(before)
    change = expectation.expected_change
    keeps_interval = change.get("trigger") == _at(before, (*_ALERT, "trigger")) == "ONCE_PER_INTERVAL"
    owned = [path for key in change for path in _owned_paths(key, kind, keeps_interval=keeps_interval)]
    diffs: list[dict] = []
    _differences(before, after, (), diffs)
    return [d for d in diffs if not _ignored(tuple(d["path"].split(".")), owned)]


def evaluate_update(
    expectation: AlertUpdateExpectation,
    *,
    before: dict,
    after: dict | None,
    update_called: bool,
    alert_created: bool,
) -> tuple[AlertUpdateEvaluation, list[dict]]:
    """Score one run from the stored alert before the question and after it; also returns the unexpected changes.

    ``after`` is None when the alert no longer exists: the agent deleted it, or deleted and recreated it.
    """
    if after is None:
        evaluation = AlertUpdateEvaluation(
            alert_update_called=update_called,
            alert_update_correct=False,
            alert_update_preserved=False,
            alert_not_recreated=False,
        )
        return evaluation, []
    kind = condition_kind(before)
    applied = all(
        _change_applied(key, value, _stored_value(after, key, kind))
        for key, value in expectation.expected_change.items()
    )
    changes = unexpected_changes(expectation, before, after)
    evaluation = AlertUpdateEvaluation(
        alert_update_called=update_called,
        alert_update_correct=update_called and applied,
        alert_update_preserved=update_called and not changes,
        alert_not_recreated=not alert_created,
    )
    return evaluation, changes


def targets_alert(args: dict, alert_id: str) -> bool:
    """Whether an update call names ``alert_id``: ``automation_id``, or ``automation_ids``.

    ``automation_ids`` is a list, one id, or a list encoded as a JSON string, which the tool also accepts.
    """
    if args.get("automation_id") == alert_id:
        return True
    ids = args.get("automation_ids")
    if isinstance(ids, str) and ids.strip().startswith("["):
        try:
            ids = json.loads(ids)
        except json.JSONDecodeError:
            return False
    return ids == alert_id or (isinstance(ids, list) and alert_id in ids)


def update_sim_user_prompt(question: str, title: str) -> str:
    """The simulated user of an update item: it confirms the requested change and nothing else."""
    return (
        "You are a user who asked an AI agent to change one of your existing alerts.\n"
        f'Your request was: "{question}"\n'
        f'The alert is the one titled "{title}".\n'
        "Rules you MUST follow:\n"
        "1. Your goal is exactly the change in your request. Never ask for any other change.\n"
        "2. If the agent asks you to confirm that change, or shows a summary or proposal of it, confirm: "
        "'Yes, please apply that change.'\n"
        f'3. If the agent asks which alert you mean, it is the one titled "{title}".\n'
        "4. If the agent proposes to change anything else, to create a new alert or to delete this one, "
        "decline and repeat your request.\n"
        "5. If the agent asks about a setting your request does not mention, tell it to keep the current value.\n"
        "Reply concisely and directly."
    )


class AutomationApi:
    """The workspace automation entities one update run creates, reads and deletes."""

    def __init__(
        self, host: str, token: str, workspace_id: str, *, transport: httpx.BaseTransport | None = None
    ) -> None:
        self._host = host.rstrip("/")
        self._automations = f"{self._host}/api/v1/entities/workspaces/{workspace_id}/automations"
        self._client = httpx.Client(
            timeout=60.0,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/vnd.gooddata.api+json"},
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def create(self, entity: dict) -> str:
        alert_id = f"{SETUP_ID_PREFIX}{uuid.uuid4().hex[:12]}"
        body = {"data": {"id": alert_id, "type": "automation", **entity}}
        try:
            self._client.post(self._automations, json=body).raise_for_status()
        except Exception:
            # The server may have stored the alert before the request failed, and the run never gets its id.
            self.delete(alert_id)
            raise
        return alert_id

    def get(self, alert_id: str) -> dict | None:
        """The stored alert as ``attributes`` + ``relationships``; None when it does not exist."""
        resp = self._client.get(f"{self._automations}/{alert_id}", params={"include": "ALL"})
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = _envelope(resp).get("data")
        if not isinstance(data, dict):
            raise ValueError(f"Automation {alert_id} response has no data object")
        attributes, relationships = data.get("attributes"), data.get("relationships") or {}
        if not isinstance(attributes, dict) or not isinstance(relationships, dict):
            raise ValueError(f"Automation {alert_id} response has no attributes object or a malformed relationships")
        return {"attributes": attributes, "relationships": relationships}

    def ids_titled(self, title: str) -> list[str]:
        ids: list[str] = []
        page = 0
        while True:
            resp = self._client.get(self._automations, params={"page": page, "size": _PAGE_SIZE})
            resp.raise_for_status()
            data = _entries(resp, "automations")
            ids += [a["id"] for a in data if (a.get("attributes") or {}).get("title") == title]
            if len(data) < _PAGE_SIZE:
                return ids
            page += 1

    def delete(self, alert_id: str, *, strict: bool = False) -> None:
        """Delete an alert; a missing one counts as deleted.

        Best effort unless ``strict``: a failure is logged, not raised, so a cleanup never hides the run's own
        error. ``strict`` raises instead, for a deletion the run cannot go on without.
        """
        try:
            resp = self._client.delete(f"{self._automations}/{alert_id}")
            if resp.status_code != 404:
                resp.raise_for_status()
        except Exception as exc:
            if strict:
                raise
            print(f"[CLEANUP] Failed to delete alert {alert_id}: {exc}")

    def first_channel_id(self) -> str | None:
        """The organization's notification channel with the lowest id, None when it has none."""
        ids: list[str] = []
        page = 0
        while True:
            resp = self._client.get(
                f"{self._host}/api/v1/entities/notificationChannels", params={"page": page, "size": _PAGE_SIZE}
            )
            resp.raise_for_status()
            data = _entries(resp, "notification channels")
            ids += [c["id"] for c in data]
            if len(data) < _PAGE_SIZE:
                return min(ids) if ids else None
            page += 1


def _envelope(resp: httpx.Response) -> dict:
    body = resp.json()
    if not isinstance(body, dict):
        raise ValueError(f"{resp.request.url} returned {type(body).__name__}, expected a JSON object")
    return body


def _entries(resp: httpx.Response, what: str) -> list[dict]:
    """The ``data`` list of a listing; every entry an object with a string id."""
    data = _envelope(resp).get("data")
    if not isinstance(data, list) or not all(isinstance(e, dict) and isinstance(e.get("id"), str) for e in data):
        raise ValueError(f"The {what} listing has no data list of objects with an id")
    return data
