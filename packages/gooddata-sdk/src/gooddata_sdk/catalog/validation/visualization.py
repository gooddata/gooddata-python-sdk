# (C) 2026 GoodData Corporation
"""Offline checks on a visualization's ``content``.

Nothing here needs a workspace, a catalog or a network call: every check is answerable
from the object itself. That is deliberate -- it is what lets the same code run in CI on a
pull request that touches one YAML file, with no credentials.

The checks are limited to what stays true as the visualization format grows. Which chart
types and bucket names exist is owned elsewhere and changes without notice, so those are
warnings; a reference that resolves to nothing is broken under any future format, so that
is an error. See :class:`gooddata_sdk.catalog.validation.model.Severity`.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk.catalog.validation.model import Finding, Severity

# The platform stores content as a free-form JSON object capped by length. The cap comes
# from LARGE_CONTENT_LENGTH in the metadata model, and is the real one: the declarative
# OpenAPI schema advertises 15000 for this field because it reuses a generic "JsonNode"
# schema, which understates it by more than an order of magnitude. Validating against that
# smaller number would reject content the platform stores happily.
MAX_CONTENT_LENGTH = 250_000

# Only version 2 of the content format is currently understood by the platform. A missing
# version is an error (it is a required field), but an *unknown* version is only a warning:
# a version 3 would mean this SDK is behind, not that the content is wrong.
SUPPORTED_CONTENT_VERSION = "2"

_REQUIRED_KEYS = ("buckets", "visualizationUrl", "version")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def defined_local_ids(content: dict[str, Any]) -> set[str]:
    """Local identifiers that the buckets *define* -- the ones sorts and filters may point at.

    Only bucket items define them. An attribute filter also carries a ``localIdentifier``,
    but that names the filter itself rather than referring to a bucket item, so collecting
    it here would let a sort "resolve" to a filter and hide a real dangling reference.
    """
    local_ids: set[str] = set()
    for bucket in _as_list(content.get("buckets")):
        for item in _as_list(_as_dict(bucket).get("items")):
            for kind in ("measure", "attribute"):
                local_id = _as_dict(_as_dict(item).get(kind)).get("localIdentifier")
                if isinstance(local_id, str):
                    local_ids.add(local_id)
    return local_ids


def referenced_local_ids(content: dict[str, Any]) -> list[tuple[str, str]]:
    """Every reference to a bucket item's local identifier, as ``(local_id, location)``.

    Enumerated by shape rather than by searching for any ``localIdentifier`` key anywhere,
    because several of those keys *declare* an identifier instead of referring to one --
    bucket items and attribute filters both do. Treating a declaration as a reference would
    report an object as broken precisely because it is well-formed.
    """
    refs: list[tuple[str, str]] = []

    for index, sort in enumerate(_as_list(content.get("sorts"))):
        sort = _as_dict(sort)
        attribute_sort = _as_dict(sort.get("attributeSortItem"))
        identifier = attribute_sort.get("attributeIdentifier")
        if isinstance(identifier, str):
            refs.append((identifier, f"content.sorts[{index}].attributeSortItem.attributeIdentifier"))
        measure_sort = _as_dict(sort.get("measureSortItem"))
        for locator_index, locator in enumerate(_as_list(measure_sort.get("locators"))):
            measure_locator = _as_dict(_as_dict(locator).get("measureLocatorItem"))
            identifier = measure_locator.get("measureIdentifier")
            if isinstance(identifier, str):
                refs.append(
                    (
                        identifier,
                        f"content.sorts[{index}].measureSortItem.locators[{locator_index}]"
                        ".measureLocatorItem.measureIdentifier",
                    )
                )

    for index, filter_ in enumerate(_as_list(content.get("filters"))):
        for filter_name in ("rankingFilter", "measureValueFilter"):
            body = _as_dict(_as_dict(filter_).get(filter_name))
            if not body:
                continue
            measure_local_id = _as_dict(body.get("measure")).get("localIdentifier")
            if isinstance(measure_local_id, str):
                refs.append((measure_local_id, f"content.filters[{index}].{filter_name}.measure.localIdentifier"))
            for dim_index, dimension in enumerate(_as_list(body.get("dimensionality"))):
                dim_local_id = _as_dict(dimension).get("localIdentifier")
                if isinstance(dim_local_id, str):
                    refs.append(
                        (
                            dim_local_id,
                            f"content.filters[{index}].{filter_name}.dimensionality[{dim_index}].localIdentifier",
                        )
                    )

    return refs


def validate_content(
    content: Any,
    *,
    object_id: str | None = None,
    known_visualization_urls: frozenset[str] | None = None,
    known_bucket_names: frozenset[str] | None = None,
) -> list[Finding]:
    """Check one visualization ``content`` blob and return what is wrong with it.

    Args:
        content: the visualization content, as stored.
        object_id: id reported alongside each finding.
        known_visualization_urls: recognised ``visualizationUrl`` values. When None, the
            chart type is not checked at all -- an empty set would report every object.
        known_bucket_names: recognised bucket ``localIdentifier`` values, same convention.

    Returns:
        Findings, unsorted. An empty list means nothing was found -- not that the
        visualization renders.
    """
    findings: list[Finding] = []

    def error(code: str, message: str, location: str | None = None) -> None:
        findings.append(
            Finding(severity=Severity.ERROR, code=code, message=message, object_id=object_id, location=location)
        )

    def warning(code: str, message: str, location: str | None = None) -> None:
        findings.append(
            Finding(severity=Severity.WARNING, code=code, message=message, object_id=object_id, location=location)
        )

    if not isinstance(content, dict):
        error("content_not_an_object", f"content must be a JSON object, got {type(content).__name__}", "content")
        return findings

    for key in _REQUIRED_KEYS:
        if content.get(key) is None:
            error("missing_required_key", f"content is missing the required key '{key}'", f"content.{key}")

    version = content.get("version")
    if version is not None and version != SUPPORTED_CONTENT_VERSION:
        warning(
            "unknown_content_version",
            f"content version {version!r} is not the supported version "
            f"{SUPPORTED_CONTENT_VERSION!r}; this SDK may be older than the platform",
            "content.version",
        )

    buckets = content.get("buckets")
    if buckets is not None and not isinstance(buckets, list):
        error("buckets_not_a_list", f"content.buckets must be a list, got {type(buckets).__name__}", "content.buckets")

    if known_bucket_names is not None:
        for index, bucket in enumerate(_as_list(buckets)):
            name = _as_dict(bucket).get("localIdentifier")
            if isinstance(name, str) and name not in known_bucket_names:
                warning(
                    "unknown_bucket_name",
                    f"bucket local identifier {name!r} is not one this SDK knows",
                    f"content.buckets[{index}].localIdentifier",
                )

    visualization_url = content.get("visualizationUrl")
    if (
        known_visualization_urls is not None
        and isinstance(visualization_url, str)
        and visualization_url not in known_visualization_urls
    ):
        warning(
            "unknown_visualization_url",
            f"visualizationUrl {visualization_url!r} is not one this SDK knows",
            "content.visualizationUrl",
        )

    # Resolution is skipped when there are no usable buckets to resolve against: with the
    # buckets missing, every single reference dangles, and burying the one real finding
    # ("buckets is missing") under a cascade of consequences of it helps nobody.
    if isinstance(buckets, list):
        defined = defined_local_ids(content)
        for local_id, location in referenced_local_ids(content):
            if local_id not in defined:
                error(
                    "dangling_local_id",
                    f"local identifier {local_id!r} is referenced but no bucket item defines it",
                    location,
                )

    return findings


def validate_content_length(content_json: str, *, object_id: str | None = None) -> list[Finding]:
    """Check the serialised content against the platform's length cap.

    Kept apart from :func:`validate_content` because it is the only check that depends on
    how the content is serialised rather than on what it says, and the caller is the one
    holding the bytes that will actually be sent.
    """
    if len(content_json) <= MAX_CONTENT_LENGTH:
        return []
    return [
        Finding(
            severity=Severity.ERROR,
            code="content_too_long",
            message=f"serialised content is {len(content_json)} characters, over the {MAX_CONTENT_LENGTH} limit",
            object_id=object_id,
            location="content",
        )
    ]
