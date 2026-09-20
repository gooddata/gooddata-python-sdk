# (C) 2026 GoodData Corporation
"""Checks that need the whole layout rather than one object.

Two kinds of reference run through an analytics model, and they resolve against different
things:

* **catalog references** -- metrics, labels, datasets, attributes, facts. These live in the
  workspace, so they can only be checked against a server (see
  :mod:`gooddata_sdk.catalog.validation.references`).
* **layout references** -- a dashboard naming the visualization it renders, or the filter
  context it uses. These name objects the layout itself carries, so they are answerable
  from the files alone.

The second kind is where a migration usually breaks: dashboards get exported and a filter
context does not, or a visualization is dropped from the set while the dashboard that
renders it is kept. The deploy succeeds -- the API validates none of this -- and the
dashboard is broken when someone opens it.

Also here: duplicate ids, and cycles in metric definitions, both of which are properties of
the set rather than of any one object.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from gooddata_sdk.catalog.validation.maql import extract_maql_references, referenced_metric_ids
from gooddata_sdk.catalog.validation.model import Finding, Severity
from gooddata_sdk.catalog.validation.properties import extract_properties_references
from gooddata_sdk.catalog.validation.references import CatalogReference, extract_catalog_references

if TYPE_CHECKING:
    from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
        CatalogDeclarativeAnalytics,
    )

# Reference types that name an object the layout itself defines. Everything else an
# identifier node can name belongs to the workspace catalog and is resolved elsewhere.
LAYOUT_REFERENCE_TYPES = ("visualizationObject", "filterContext", "analyticalDashboard", "dashboardPlugin")

# Which collection on the analytics layer holds each layout reference type. Explicit rather
# than derived from the name, because the two do not follow one rule -- the objects behind
# "visualizationObject" live in `visualization_objects`.
_COLLECTION_BY_TYPE = {
    "visualizationObject": "visualization_objects",
    "filterContext": "filter_contexts",
    "analyticalDashboard": "analytical_dashboards",
    "dashboardPlugin": "dashboard_plugins",
}

# Every collection whose objects carry an id, for the duplicate check. Metrics and
# visualizations are the ones that actually collide in practice, but an id clash is a
# deploy-time surprise wherever it happens.
_ID_BEARING_COLLECTIONS = (
    "analytical_dashboards",
    "attribute_hierarchies",
    "dashboard_plugins",
    "export_definitions",
    "filter_contexts",
    "memory_items",
    "metrics",
    "parameters",
    "visualization_objects",
)


def _collection(model: CatalogDeclarativeAnalytics, name: str) -> list[Any]:
    if model.analytics is None:
        return []
    return list(getattr(model.analytics, name, []) or [])


def layout_object_ids(model: CatalogDeclarativeAnalytics) -> set[str]:
    """``type/id`` of every object the layout defines that something else can point at."""
    ids: set[str] = set()
    for reference_type, collection in _COLLECTION_BY_TYPE.items():
        ids.update(f"{reference_type}/{obj.id}" for obj in _collection(model, collection))
    return ids


def object_references(model: CatalogDeclarativeAnalytics) -> list[tuple[str, CatalogReference]]:
    """Every reference every object in the layout makes, as ``(object_id, reference)``.

    Visualizations and dashboards carry theirs as ``identifier`` nodes and are walked;
    metrics carry theirs inside a MAQL string and are read with the MAQL reader. Filter
    contexts are walked too -- they name the labels they filter on.

    A geo chart also names labels in ``properties.controls`` as bare strings, which the
    walk cannot see, so those are collected separately. Being gathered here rather than at
    either call site is what makes them resolve on both paths -- against a workspace and
    against the layout's own logical model -- instead of only the one that was remembered.
    """
    found: list[tuple[str, CatalogReference]] = []

    for collection, path in (
        ("visualization_objects", "content"),
        ("analytical_dashboards", "content"),
        ("filter_contexts", "content"),
    ):
        for obj in _collection(model, collection):
            found.extend((obj.id, reference) for reference in extract_catalog_references(obj.content, path=path))

    for visualization in _collection(model, "visualization_objects"):
        found.extend(
            (visualization.id, reference)
            for reference in extract_properties_references(visualization.content, path="content")
        )

    for metric in _collection(model, "metrics"):
        maql = (metric.content or {}).get("maql")
        found.extend((metric.id, reference) for reference in extract_maql_references(maql))

    return found


def check_duplicate_ids(model: CatalogDeclarativeAnalytics) -> list[Finding]:
    """Ids repeated within a collection.

    The layout stores one file per object named by its id, so two objects sharing one id
    cannot both survive a round trip through disk: the second silently overwrites the first
    and the layout that gets deployed is missing an object nobody removed.
    """
    findings: list[Finding] = []
    for collection in _ID_BEARING_COLLECTIONS:
        seen: set[str] = set()
        for obj in _collection(model, collection):
            if obj.id in seen:
                findings.append(
                    Finding(
                        severity=Severity.ERROR,
                        code="duplicate_id",
                        message=f"{collection} contains more than one object with id {obj.id!r}",
                        object_id=obj.id,
                        location=collection,
                    )
                )
            seen.add(obj.id)
    return findings


def check_layout_references(model: CatalogDeclarativeAnalytics) -> list[Finding]:
    """Layout references that name an object the layout does not carry.

    Reported as a warning, not an error, and the distinction is the point: the layout is
    not always the whole picture. A child workspace's layout holds only what the child
    owns, so a dashboard there can legitimately render a visualization inherited from the
    parent. What this finds is "not in these files" -- which is worth saying, because it is
    the shape of a half-exported migration -- but only the target workspace can settle
    whether it is actually missing.
    """
    defined = layout_object_ids(model)
    findings: list[Finding] = []
    for object_id, reference in object_references(model):
        if reference.type not in LAYOUT_REFERENCE_TYPES:
            continue
        if reference.obj_id not in defined:
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    code="layout_reference_not_in_layout",
                    message=(
                        f"{reference.obj_id} is referenced but no object in this layout defines it; "
                        f"it must already exist in the target workspace, or be inherited"
                    ),
                    object_id=object_id,
                    location=reference.location,
                )
            )
    return findings


def check_metric_cycles(model: CatalogDeclarativeAnalytics) -> list[Finding]:
    """Metrics that depend on themselves, directly or through other metrics.

    A cycle cannot be executed, and it is invisible in any single metric: each one on its
    own looks ordinary. Only edges between metrics defined in this layout are followed --
    a reference to a metric that lives elsewhere is not a cycle this layout can resolve, and
    following it would need the whole workspace.
    """
    metrics = {metric.id: (metric.content or {}).get("maql") for metric in _collection(model, "metrics")}
    edges = {metric_id: referenced_metric_ids(maql) & metrics.keys() for metric_id, maql in metrics.items()}

    findings: list[Finding] = []
    reported: set[frozenset[str]] = set()
    # Iterative depth-first search with an explicit stack: a recursive walk would hit
    # Python's recursion limit on a deep metric chain, which several thousand metrics can
    # produce, and a RecursionError in the middle of a layout says nothing useful.
    for start in edges:
        stack: list[tuple[str, list[str]]] = [(start, [start])]
        on_path = {start}
        while stack:
            node, path = stack.pop()
            for neighbour in sorted(edges.get(node, ())):
                if neighbour == start:
                    cycle = frozenset(path)
                    if cycle not in reported:
                        reported.add(cycle)
                        findings.append(
                            Finding(
                                severity=Severity.ERROR,
                                code="metric_cycle",
                                message=f"metric definitions form a cycle: {' -> '.join([*path, start])}",
                                object_id=start,
                                location="content.maql",
                            )
                        )
                elif neighbour not in on_path:
                    on_path.add(neighbour)
                    stack.append((neighbour, [*path, neighbour]))
    return findings


def validate_layout(model: CatalogDeclarativeAnalytics) -> list[Finding]:
    """Every whole-layout check, for a model that needs no server to answer them."""
    return check_duplicate_ids(model) + check_layout_references(model) + check_metric_cycles(model)
