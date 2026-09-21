# (C) 2026 GoodData Corporation
"""Whether the values an attribute filter names still exist in the data.

Every other check in this package asks whether the layout is *well formed*. This one asks
whether it is still *true*, which is a different kind of question and the reason it is kept
apart: a filter pinned to ``in: {values: ["EMEA"]}`` is perfectly valid content, and the
day that region is renamed the chart it filters quietly returns nothing. Nobody gets an
error. The dashboard just goes empty, which is the failure people notice last and diagnose
slowest.

**This is the only check that reads data rather than metadata.** Resolving a label element
means a ``SELECT DISTINCT`` against the customer's warehouse, so it costs money and time
that none of the other checks do, and it is therefore opt-in twice over: it needs a
workspace, and it needs asking for by name. Nothing calls it implicitly.

Three things keep the cost and the false-alarm rate down:

* **One query per label, not per value.** ``exact_filter`` asks the server which of a given
  list exist, so a filter naming forty values on a million-row label costs the same single
  call as one naming a single value.
* **Findings are warnings.** A value absent today may be loaded tomorrow: this reports the
  state of the data at the moment it was asked, not a property of the layout. An overnight
  load makes a finding here disappear without anything being edited, which is precisely why
  it must not fail a build the way a structural error does.
* **Only value-based filters are checked.** The format also allows elements by *reference*
  (``uris``), which name primary-label values rather than the text this can resolve, and a
  ``null`` value means the NULL element rather than a value to look up. Both are skipped
  rather than guessed at.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from attrs import define, field

from gooddata_sdk.catalog.validation.model import Finding, Severity

if TYPE_CHECKING:
    from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
        CatalogDeclarativeAnalytics,
    )
    from gooddata_sdk.sdk import GoodDataSdk

# The two filter shapes that name their elements by value. `in` and `notIn` hold the same
# kind of list; which one it is decides only what the filter *does* with them, not whether
# the values have to exist.
_VALUE_FILTERS = {"positiveAttributeFilter": "in", "negativeAttributeFilter": "notIn"}

# The elements API takes the values to look for as a query parameter, so a filter naming
# hundreds of them is split rather than sent as one unbounded request.
_BATCH = 500


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


@define(kw_only=True, frozen=True)
class FilterValues:
    """One attribute filter's label and the values it pins, with where it was found."""

    label_id: str
    values: tuple[str, ...]
    object_id: str
    location: str


@define(kw_only=True)
class ElementResolution:
    """What checking the filters against the data found.

    ``labels_queried`` is reported because zero findings has two very different meanings
    here -- every value resolved, or nothing was asked -- and only this number tells them
    apart.
    """

    labels_queried: int = 0
    values_checked: int = 0
    missing: list[Finding] = field(factory=list)


def collect_filter_values(content: Any, *, object_id: str, path: str = "content") -> list[FilterValues]:
    """Every attribute filter in an object that pins its elements by value.

    Walks the whole tree rather than reading known positions, because the same filter shape
    occurs in a visualization's ``filters``, in a dashboard's filter context, and nested
    inside a dashboard's widgets, and enumerating those would need updating each time the
    format gains a place to put one.

    Skipped, deliberately: elements given by ``uris`` (they name primary-label values, not
    the titles this resolves), ``null`` entries (the NULL element is not a value to look
    up), and empty lists (a negative filter with no elements is a no-op, and a positive one
    with none is already reported as an incomplete filter).
    """
    found: list[FilterValues] = []

    def walk(node: Any, node_path: str) -> None:
        if isinstance(node, dict):
            for filter_name, values_key in _VALUE_FILTERS.items():
                body = _as_dict(node.get(filter_name))
                if not body:
                    continue
                label_id = _as_dict(_as_dict(body.get("displayForm")).get("identifier")).get("id")
                raw = _as_dict(body.get(values_key)).get("values")
                if not isinstance(label_id, str) or not isinstance(raw, list):
                    continue
                # dict.fromkeys rather than a set: the order a filter lists its values in is
                # the order a reader will look for them in the finding.
                values = tuple(dict.fromkeys(v for v in raw if isinstance(v, str)))
                if values:
                    found.append(
                        FilterValues(
                            label_id=label_id,
                            values=values,
                            object_id=object_id,
                            location=f"{node_path}.{filter_name}.{values_key}.values",
                        )
                    )
            for key, value in node.items():
                walk(value, f"{node_path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{node_path}[{index}]")

    walk(content, path)
    return found


def _existing_values(sdk: GoodDataSdk, workspace_id: str, label_id: str, values: tuple[str, ...]) -> set[str] | None:
    """Which of ``values`` the data actually holds, or None when the question could not be put.

    None rather than an empty set on failure, and the difference matters: an empty set means
    the server answered that none of them exist, which is a finding, while None means it did
    not answer, which is not. A label that is missing altogether raises here and is reported
    by the reference check instead -- this one has nothing useful to add about it.
    """
    existing: set[str] = set()
    for start in range(0, len(values), _BATCH):
        batch = list(values[start : start + _BATCH])
        try:
            found = sdk.catalog_workspace_content.get_label_elements(
                workspace_id,
                label_id,
                exact_filter=batch,
                # Without an explicit limit the server pages at its own default, and a
                # filter naming more values than that would look partly missing.
                limit=len(batch),
            )
        except Exception:  # noqa: BLE001 - any failure here means "unknown", never "missing"
            return None
        existing.update(found)
    return existing


def check_filter_element_values(
    sdk: GoodDataSdk,
    workspace_id: str,
    model: CatalogDeclarativeAnalytics,
) -> tuple[list[Finding], ElementResolution]:
    """Check every value-based attribute filter in a layout against the workspace's data.

    Args:
        sdk: connected SDK. This issues one element query per distinct label, each of which
            runs a ``SELECT DISTINCT`` against the data source.
        workspace_id: the workspace whose data the values are resolved against. Values live
            in the data, not the catalog, so a filter valid in one workspace can be empty in
            another that shares its model.
        model: the layout to check.

    Returns:
        Warnings for values the data does not hold, and the counts behind them.

    Filters are grouped by label before anything is asked, so twenty visualizations pinned
    to the same region cost one query rather than twenty.
    """
    analytics = model.analytics
    resolution = ElementResolution()
    if analytics is None:
        return [], resolution

    collected: list[FilterValues] = []
    for collection in ("visualization_objects", "analytical_dashboards", "filter_contexts"):
        for obj in getattr(analytics, collection, None) or []:
            collected.extend(collect_filter_values(obj.content, object_id=obj.id))

    by_label: dict[str, list[FilterValues]] = {}
    for entry in collected:
        by_label.setdefault(entry.label_id, []).append(entry)

    findings: list[Finding] = []
    for label_id, entries in sorted(by_label.items()):
        wanted = tuple(dict.fromkeys(value for entry in entries for value in entry.values))
        existing = _existing_values(sdk, workspace_id, label_id, wanted)
        if existing is None:
            continue
        resolution.labels_queried += 1
        resolution.values_checked += len(wanted)

        for entry in entries:
            missing = [value for value in entry.values if value not in existing]
            if not missing:
                continue
            findings.append(
                Finding(
                    severity=Severity.WARNING,
                    code="filter_value_not_in_data",
                    message=(
                        f"{label_id} has no value {', '.join(repr(v) for v in missing)} in {workspace_id}; "
                        f"this filter will match nothing on {'them' if len(missing) > 1 else 'it'}"
                    ),
                    object_id=entry.object_id,
                    location=entry.location,
                )
            )

    resolution.missing = findings
    return findings, resolution
