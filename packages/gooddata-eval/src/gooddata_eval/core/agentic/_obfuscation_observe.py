# (C) 2026 GoodData Corporation. All rights reserved.
"""Record-only observations for the agentic_obfuscation kind's multi-turn items.

Some multi-turn behaviour has no agreed expectation yet -- whether an alert still reaches the
email the user typed once history is masked, or a filter still holds its value on the next
turn. An item lists what to look at under ``expected_output.observe``; this module reports
it and never decides a verdict. It also deletes what the chat created (an alert, a scheduled
export, a metric), so a persistent workspace can run the dataset again and again.

``observe`` keys:
  automation_match  substring identifying the automation this item makes (a metric id, a
                    dashboard id); the recipients it ended up with are reported
  metric_title      title of the metric this item makes; its MAQL is reported
  stream_markers    strings to look for in the last turn's streamed text and visualizations
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import httpx

_ENTITIES = "application/vnd.gooddata.api+json"
_PAGE_SIZE = 500
_MAX_PAGES = 20


class WorkspaceEntities:
    """Just enough of the workspace entities API to list and delete what a chat created."""

    def __init__(self, http: httpx.Client, host: str, workspace_id: str) -> None:
        self._http = http
        self._base = f"{host.rstrip('/')}/api/v1/entities/workspaces/{workspace_id}"

    def list(self, entity: str) -> dict[str, dict[str, Any]]:
        """Every entity of the kind, all pages: a created one missed here is never cleaned up."""
        found: dict[str, dict[str, Any]] = {}
        for page in range(_MAX_PAGES):
            resp = self._http.get(
                f"{self._base}/{entity}", params={"size": _PAGE_SIZE, "page": page}, headers={"Accept": _ENTITIES}
            )
            resp.raise_for_status()
            data = resp.json().get("data", [])
            found.update((item["id"], item) for item in data)
            if len(data) < _PAGE_SIZE:
                return found
        raise httpx.HTTPError(f"{entity}: more than {_MAX_PAGES * _PAGE_SIZE} entities, listing stopped")

    def delete(self, entity: str, entity_id: str) -> None:
        resp = self._http.delete(f"{self._base}/{entity}/{entity_id}", headers={"Accept": _ENTITIES})
        # Already gone -- the agent, or the kind's own cleanup, removed it first.
        if resp.status_code != 404:
            resp.raise_for_status()


def snapshot(entities: WorkspaceEntities, spec: dict[str, Any]) -> dict[str, set[str]]:
    """Ids that existed before the item ran, for the entities its ``observe`` spec watches."""
    taken: dict[str, set[str]] = {}
    if spec.get("automation_match"):
        taken["automations"] = set(entities.list("automations"))
    if spec.get("metric_title"):
        taken["metrics"] = set(entities.list("metrics"))
    return taken


def _recipients(automation: dict[str, Any]) -> str:
    attributes = automation.get("attributes") or {}
    external = [r.get("email") for r in attributes.get("externalRecipients") or []]
    internal = [r.get("id") for r in ((automation.get("relationships") or {}).get("recipients") or {}).get("data", [])]
    return f"external={external} internal={internal}"


def observe_and_clean(
    entities: WorkspaceEntities, spec: dict[str, Any], before: dict[str, set[str]], last_stream: str
) -> list[str]:
    """Report what the item's ``observe`` spec asks about, then delete what the chat created.

    Runs from a ``finally``: a failed list or delete becomes a note, so it can neither replace
    the item's verdict nor stop the rest of the cleanup.
    """
    notes: list[str] = []
    _observe_step("automations", _observe_automations, entities, spec, before, notes)
    _observe_step("metrics", _observe_metrics, entities, spec, before, notes)
    notes.extend(
        f"OBSERVED last turn stream {'contains' if marker in last_stream else 'lacks'} {marker!r}"
        for marker in spec.get("stream_markers") or []
    )
    return notes


def _observe_step(
    name: str,
    step: Callable[[WorkspaceEntities, dict[str, Any], dict[str, set[str]], list[str]], None],
    entities: WorkspaceEntities,
    spec: dict[str, Any],
    before: dict[str, set[str]],
    notes: list[str],
) -> None:
    try:
        step(entities, spec, before, notes)
    except httpx.HTTPError as exc:
        notes.append(f"OBSERVED cleanup failed ({name}): {exc}")


def _delete(entities: WorkspaceEntities, entity: str, entity_id: str, notes: list[str]) -> None:
    try:
        entities.delete(entity, entity_id)
    except httpx.HTTPError as exc:
        notes.append(f"OBSERVED could not delete {entity} {entity_id}: {exc}")


def _observe_automations(
    entities: WorkspaceEntities, spec: dict[str, Any], before: dict[str, set[str]], notes: list[str]
) -> None:
    match = spec.get("automation_match")
    if match:
        created = {i: a for i, a in entities.list("automations").items() if i not in before["automations"]}
        mine = {i: a for i, a in created.items() if match in json.dumps(a)}
        if not mine:
            notes.append(f"OBSERVED no automation matching {match!r} was created")
        for automation_id, automation in mine.items():
            notes.append(f"OBSERVED automation {automation_id} created with {_recipients(automation)}")
            _delete(entities, "automations", automation_id, notes)


def _observe_metrics(
    entities: WorkspaceEntities, spec: dict[str, Any], before: dict[str, set[str]], notes: list[str]
) -> None:
    title = spec.get("metric_title")
    if title:
        created = {i: m for i, m in entities.list("metrics").items() if i not in before["metrics"]}
        mine = {i: m for i, m in created.items() if (m.get("attributes") or {}).get("title") == title}
        if not mine:
            notes.append(f"OBSERVED no metric titled {title!r} was created")
        for metric_id, metric in mine.items():
            maql = ((metric.get("attributes") or {}).get("content") or {}).get("maql")
            notes.append(f"OBSERVED metric {metric_id} created, maql={maql!r}")
            _delete(entities, "metrics", metric_id, notes)
