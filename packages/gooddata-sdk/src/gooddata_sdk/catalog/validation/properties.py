# (C) 2026 GoodData Corporation
"""Checks on ``content.properties`` -- the part of a visualization nothing else looks at.

``properties`` carries the rendering configuration: axes, legends, colours, totals, the
comparison on a headline, the latitude and longitude of a geo chart. It is the least
constrained part of the content and the easiest to get wrong by hand, and until now
validation ignored it entirely.

**The guiding constraint is that almost all of it must be left alone.** Stored content
carries ``controls`` keys the platform models nowhere -- ``legend``, ``xaxis``,
``dataLabels``, ``colorMapping``, ``dualAxis``, ``grid`` and more -- because the renderer
owns that vocabulary and the backend simply ignores what it does not recognise. Reporting
an unknown key would flag ordinary, working charts. So there is no "unknown key" check
here and there should never be one: what is checked is only the handful of fields the
platform itself reads, where a wrong value provably changes what happens.

Those fields are worth checking precisely because nothing else can see them:

* **Geo position fields.** ``controls.latitude``, ``controls.longitude`` and
  ``controls.tooltipText`` hold *label identifiers*, from which the platform builds the
  buckets those values are read out of. They are catalog references living in a plain
  string, so the reference walk -- which looks for ``identifier`` nodes -- goes straight
  past them. A geo chart whose latitude label was renamed loses the field silently.
* **Local identifier references.** ``controls.secondary_xaxis.measures`` and the keys of
  ``controls.inlineVisualizations`` name measures by their bucket local identifier, the
  same way a sort does.
* **Enumerated values.** ``measureGroupDimension`` decides whether a table is transposed,
  and a value the platform does not recognise is not a different layout, it is one that
  fails to parse.

Severity: everything here is a warning, deliberately. The geo references are the exception
and they are not raised here at all -- they are handed to the ordinary reference resolver
in :mod:`gooddata_sdk.catalog.validation.references`, which reports an unresolved one as
an error like any other. The rest stay warnings until they have been run against stored
content at the scale the other checks were, because a check that has not met real data is
a hypothesis.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.validation.buckets import VISUALIZATION_NAMES
from gooddata_sdk.catalog.validation.model import Finding, Severity
from gooddata_sdk.catalog.validation.references import CatalogReference

# Chart types for which the geo position controls mean anything. On every other type the
# platform never reads them, so a stale value there is inert and reporting it would be a
# false alarm.
_GEO_VISUALIZATIONS = frozenset({"geo", "pushpin", "choropleth"}) & VISUALIZATION_NAMES
_GEO_URLS = frozenset(_GEO_VISUALIZATIONS) | frozenset(f"local:{name}" for name in _GEO_VISUALIZATIONS)

# controls key -> the bucket the platform builds from it. All three name a label.
_GEO_POSITION_CONTROLS = ("latitude", "longitude", "tooltipText")

# Values the platform accepts, by the controls key that carries them. A value outside the
# set is not a variant the renderer falls back from -- it is one the platform cannot
# deserialise -- but the sets themselves grow, so these are warnings.
_ENUMERATED_CONTROLS: dict[str, frozenset[str]] = {
    "measureGroupDimension": frozenset({"rows", "columns"}),
    "grandTotalsPosition": frozenset({"pinnedBottom", "pinnedTop", "bottom", "top"}),
}

# Values accepted for `controls.comparison.calculationType`, which selects the arithmetic
# the platform generates for a headline's comparison measure.
_CALCULATION_TYPES = frozenset({"change", "ratio", "difference", "change_difference"})

# Values accepted for the `type` of each entry in `controls.inlineVisualizations`.
_INLINE_VISUALIZATION_TYPES = frozenset({"metric", "line", "column"})


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _controls(content: Any) -> dict[str, Any]:
    return _as_dict(_as_dict(_as_dict(content).get("properties")).get("controls"))


def _has_location_attribute(content: dict[str, Any]) -> bool:
    """Whether a ``location`` bucket holds an attribute.

    The platform builds the latitude, longitude and tooltipText buckets *out of* the
    location attribute -- it copies its alias and, for latitude, its local identifier. With
    no location attribute it builds nothing, and the position controls are never read, so
    their values cannot be wrong.
    """
    for bucket in content.get("buckets") or []:
        if _as_dict(bucket).get("localIdentifier") != "location":
            continue
        for item in _as_dict(bucket).get("items") or []:
            if _as_dict(item).get("attribute") is not None:
                return True
    return False


def extract_properties_references(content: Any, *, path: str = "content") -> list[CatalogReference]:
    """Catalog references hiding in ``properties.controls`` as plain strings.

    Only the geo position controls qualify, and only on a geo chart that has a location
    attribute for the platform to build the derived buckets from. Outside that, the values
    are never read and a reference extracted from them would be a reference to something
    that does not have to exist.

    Args:
        content: the visualization content, as stored.
        path: prefix for the reported location, matching the reference walk's convention.

    Returns:
        One reference per populated geo position control.
    """
    content = _as_dict(content)
    if content.get("visualizationUrl") not in _GEO_URLS or not _has_location_attribute(content):
        return []

    controls = _controls(content)
    references: list[CatalogReference] = []
    for key in _GEO_POSITION_CONTROLS:
        value = controls.get(key)
        if isinstance(value, str) and value:
            references.append(CatalogReference(type="label", id=value, location=f"{path}.properties.controls.{key}"))
    return references


def check_properties(
    content: Any,
    *,
    defined_local_ids: set[str],
    object_id: str | None = None,
) -> list[Finding]:
    """Check the parts of ``properties`` the platform itself reads.

    Args:
        content: the visualization content, as stored.
        defined_local_ids: local identifiers the buckets define, for the controls that
            refer to a measure by one.
        object_id: reported on each finding.

    Returns:
        Warnings. Catalog references are not reported here -- see
        :func:`extract_properties_references`.
    """
    content = _as_dict(content)
    properties = content.get("properties")
    findings: list[Finding] = []

    def warning(code: str, message: str, location: str) -> None:
        findings.append(
            Finding(severity=Severity.WARNING, code=code, message=message, object_id=object_id, location=location)
        )

    if properties is None:
        return findings
    if not isinstance(properties, dict):
        warning(
            "properties_not_an_object",
            f"content.properties must be a JSON object, got {type(properties).__name__}",
            "content.properties",
        )
        return findings

    controls = properties.get("controls")
    if controls is not None and not isinstance(controls, dict):
        warning(
            "controls_not_an_object",
            f"content.properties.controls must be a JSON object, got {type(controls).__name__}",
            "content.properties.controls",
        )
        return findings
    controls = _as_dict(controls)

    for key, allowed in _ENUMERATED_CONTROLS.items():
        value = controls.get(key)
        if value is not None and value not in allowed:
            warning(
                "unknown_control_value",
                f"{key} is {value!r}, which is not one of {', '.join(sorted(allowed))}",
                f"content.properties.controls.{key}",
            )

    calculation_type = _as_dict(controls.get("comparison")).get("calculationType")
    if calculation_type is not None and calculation_type not in _CALCULATION_TYPES:
        warning(
            "unknown_control_value",
            f"comparison.calculationType is {calculation_type!r}, which is not one of "
            f"{', '.join(sorted(_CALCULATION_TYPES))}",
            "content.properties.controls.comparison.calculationType",
        )

    # Each key names a measure in a bucket; the value says how that measure is drawn. A key
    # matching no measure configures nothing.
    for local_id, inline in _as_dict(controls.get("inlineVisualizations")).items():
        location = f"content.properties.controls.inlineVisualizations.{local_id}"
        if local_id not in defined_local_ids:
            warning(
                "dangling_local_id_in_properties",
                f"inlineVisualizations configures {local_id!r}, but no bucket item defines it",
                location,
            )
        inline_type = _as_dict(inline).get("type")
        if inline_type is not None and inline_type not in _INLINE_VISUALIZATION_TYPES:
            warning(
                "unknown_control_value",
                f"inlineVisualizations type is {inline_type!r}, which is not one of "
                f"{', '.join(sorted(_INLINE_VISUALIZATION_TYPES))}",
                f"{location}.type",
            )

    for index, local_id in enumerate(_as_dict(controls.get("secondary_xaxis")).get("measures") or []):
        if isinstance(local_id, str) and local_id not in defined_local_ids:
            warning(
                "dangling_local_id_in_properties",
                f"secondary_xaxis puts {local_id!r} on the secondary axis, but no bucket item defines it",
                f"content.properties.controls.secondary_xaxis.measures[{index}]",
            )

    return findings
