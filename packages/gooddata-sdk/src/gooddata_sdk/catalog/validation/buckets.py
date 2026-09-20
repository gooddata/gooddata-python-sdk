# (C) 2026 GoodData Corporation
"""Which buckets belong to which chart type.

Bucket names are not interchangeable between chart types, and putting items in the wrong
one is the classic hand-authoring failure: a line chart's dimension bucket is ``trend``
while a column chart's is ``view``, so a line chart carrying a ``view`` bucket stores
without complaint and draws nothing. Neither the required-key checks nor the local
identifier resolution can see it -- the content is perfectly well-formed, it is just not
what a line chart is.

Three things keep this from becoming the source of false alarms it could easily be.

**Every entry names buckets the platform is known to read.** The table is derived from the
converter that turns stored content into an execution -- the code that decides, per chart
type, which bucket each dimension comes out of. A bucket that converter never looks up on
that type contributes nothing to the execution, which is the property being reported.

**Findings are warnings.** Bucket vocabularies gain members, and a chart type can learn a
new bucket long before this table hears about it.

**Only unexpected buckets are reported, never missing ones.** A chart with no dimension
bucket is a legitimate work in progress; a chart with a bucket its type has no meaning for
is a mistake.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.validation.model import Finding, Severity

# Every bucket name the platform's execution converter recognises.
#
# A bucket called anything else is read by nothing: the converter looks buckets up by name,
# so an unrecognised name is not an extension point, it is a bucket that will be skipped.
# Reported as a warning all the same, because this vocabulary does grow.
BUCKET_NAMES: frozenset[str] = frozenset(
    {
        "measures",
        "secondary_measures",
        "tertiary_measures",
        "attribute",
        "attribute_from",
        "attribute_to",
        "attributes",
        "view",
        "stack",
        "trend",
        "segment",
        "columns",
        "location",
        "longitude",
        "latitude",
        "size",
        "color",
        "tooltipText",
    }
)

# Chart types the execution converter can convert, by their bare name.
#
# The canonical stored form is ``local:<name>``, but the bare name occurs in real stored
# content too -- ``table`` alongside ``local:table`` -- so both spellings are accepted.
VISUALIZATION_NAMES: frozenset[str] = frozenset(
    {
        "table",
        "pie",
        "donut",
        "funnel",
        "waterfall",
        "pyramid",
        "treemap",
        "line",
        "area",
        "bar",
        "column",
        "bullet",
        "combo",
        "combo2",
        "headline",
        "scatter",
        "heatmap",
        "bubble",
        "sankey",
        "dependencywheel",
        "geo",
        "pushpin",
        "choropleth",
        "xirr",
        "repeater",
        "radar",
        "mekko",
    }
)

#: Both accepted spellings of every convertible chart type.
VISUALIZATION_URLS: frozenset[str] = frozenset(VISUALIZATION_NAMES) | frozenset(
    f"local:{name}" for name in VISUALIZATION_NAMES
)

# Measure buckets are allowed on every chart type that has a rule at all, because the
# converter collects measures by walking *all* buckets rather than by name. Only the
# attribute buckets are looked up per type, so only those can be wrong.
_MEASURE_BUCKETS = frozenset({"measures", "secondary_measures", "tertiary_measures"})

# Chart type -> the attribute buckets the converter reads for that type.
#
# Three types are deliberately absent. ``treemap`` and the ``geo`` family read attributes
# from every bucket without naming any, so there is no wrong bucket to report; ``geo``
# keeps an entry below only because its bucket set is separately established from stored
# content. Anything not listed here is not checked at all -- no entry means no opinion,
# which is the difference between "this SDK has no rule" and "this is wrong".
_ATTRIBUTE_BUCKETS_BY_NAME: dict[str, frozenset[str]] = {
    "table": frozenset({"attribute", "columns"}),
    "pie": frozenset({"view"}),
    "donut": frozenset({"view"}),
    "funnel": frozenset({"view"}),
    "waterfall": frozenset({"view"}),
    "pyramid": frozenset({"view"}),
    "line": frozenset({"trend", "segment"}),
    "radar": frozenset({"trend", "segment"}),
    "area": frozenset({"view", "stack"}),
    "bar": frozenset({"view", "stack"}),
    "column": frozenset({"view", "stack"}),
    "mekko": frozenset({"view", "stack"}),
    "bullet": frozenset({"view"}),
    "combo": frozenset({"view"}),
    "combo2": frozenset({"view"}),
    "headline": frozenset(),
    "scatter": frozenset({"attribute", "segment"}),
    "heatmap": frozenset({"view", "stack"}),
    "bubble": frozenset({"view"}),
    "sankey": frozenset({"attribute_from", "attribute_to"}),
    "dependencywheel": frozenset({"attribute_from", "attribute_to"}),
    "repeater": frozenset({"attribute", "columns", "view"}),
    "xirr": frozenset({"attribute"}),
    # The geo family is the one entry not derived from the converter's per-type lookups
    # (it reads every bucket): these names come from stored content, and from the virtual
    # buckets the converter builds out of `properties.controls` for latitude, longitude
    # and tooltipText.
    "geo": frozenset({"location", "size", "color", "segment", "tooltipText", "latitude", "longitude"}),
    "pushpin": frozenset({"location", "size", "color", "segment", "tooltipText", "latitude", "longitude"}),
    "choropleth": frozenset({"location", "size", "color", "segment", "tooltipText", "latitude", "longitude"}),
}

#: visualizationUrl -> the bucket local identifiers that type uses, in both spellings.
BUCKETS_BY_VISUALIZATION: dict[str, frozenset[str]] = {
    url: attribute_buckets | _MEASURE_BUCKETS
    for name, attribute_buckets in _ATTRIBUTE_BUCKETS_BY_NAME.items()
    for url in (name, f"local:{name}")
}


def check_buckets_for_visualization_type(
    content: Any,
    *,
    object_id: str | None = None,
    rules: dict[str, frozenset[str]] | None = None,
) -> list[Finding]:
    """Report buckets that the visualization's own chart type has no use for.

    Args:
        content: the visualization content, as stored.
        object_id: reported on each finding.
        rules: ``visualizationUrl`` to its bucket names. Defaults to
            :data:`BUCKETS_BY_VISUALIZATION`; pass your own to cover chart types this SDK
            has no entry for, or to correct one. A type absent from the mapping is not
            checked.

    Returns:
        One warning per unexpected bucket, or nothing when the chart type has no rule.
    """
    if not isinstance(content, dict):
        return []
    table = BUCKETS_BY_VISUALIZATION if rules is None else rules
    allowed = table.get(content.get("visualizationUrl"))
    if allowed is None:
        return []

    buckets = content.get("buckets")
    if not isinstance(buckets, list):
        return []

    findings: list[Finding] = []
    for index, bucket in enumerate(buckets):
        if not isinstance(bucket, dict):
            continue
        name = bucket.get("localIdentifier")
        if not isinstance(name, str) or name in allowed:
            continue
        # An empty bucket of the wrong name carries nothing and breaks nothing; reporting it
        # would flag the placeholder buckets the UI leaves behind on a half-built chart.
        if not (bucket.get("items") or []):
            continue
        findings.append(
            Finding(
                severity=Severity.WARNING,
                code="unexpected_bucket_for_visualization_type",
                message=(
                    f"bucket {name!r} is not one {content['visualizationUrl']!r} uses "
                    f"({', '.join(sorted(allowed))}); its items will not be rendered"
                ),
                object_id=object_id,
                location=f"content.buckets[{index}].localIdentifier",
            )
        )
    return findings
