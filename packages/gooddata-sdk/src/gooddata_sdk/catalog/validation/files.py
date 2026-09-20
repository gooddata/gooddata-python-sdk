# (C) 2026 GoodData Corporation
"""Checks on the layout as it sits on disk, before it is loaded into a model.

Loading throws away everything about the files themselves -- which file an object came
from, and whether two of them disagreed. Some failures live only there, and the layout's
one-file-per-object convention is what makes them possible: an object is written to
``<id>.yaml``, so a file whose name and ``id`` disagree round-trips into a different file
than it came from, and the one it replaces disappears.

These run before and independently of everything else, because a layout that cannot be
read faithfully makes every later finding unreliable.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from gooddata_sdk.catalog.validation.model import Finding, Severity

# The object folders a layout writes under analytics_model/. Listed rather than globbed so
# that a folder the SDK does not know about is left alone instead of being read as an
# object collection.
_OBJECT_DIRS = (
    "analytical_dashboards",
    "analytical_dashboard_extensions",
    "attribute_hierarchy_objects",
    "dashboard_plugins",
    "export_definitions",
    "filter_contexts",
    "memory_items",
    "metrics",
    "parameters",
    "visualization_objects",
)


def _load(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        loaded = yaml.safe_load(path.read_text())
    except (yaml.YAMLError, UnicodeDecodeError, OSError) as exc:
        return None, str(exc).splitlines()[0]
    if not isinstance(loaded, dict):
        return None, f"expected a mapping, got {type(loaded).__name__}"
    return loaded, None


def check_layout_files(analytics_model_dir: Path) -> list[Finding]:
    """Read every object file and report what only the filesystem can show.

    Three things:

    * a file that does not parse, or does not hold a mapping -- reported rather than raised,
      so one bad file does not hide the state of the rest of the layout;
    * a file whose name does not match the ``id`` inside it. The layout writes
      ``<id>.yaml``, so on the next round trip this object lands in a different file and
      whatever legitimately owns that name is overwritten;
    * two files in one folder declaring the same ``id`` -- the same collision, already
      realised.

    The model-level duplicate check cannot see any of this: by the time objects are loaded,
    a name clash has already resolved itself silently.
    """
    findings: list[Finding] = []
    if not analytics_model_dir.is_dir():
        return findings

    for dir_name in _OBJECT_DIRS:
        directory = analytics_model_dir / dir_name
        if not directory.is_dir():
            continue

        ids_seen: dict[str, str] = {}
        for path in sorted(directory.glob("*.yaml")):
            location = f"{dir_name}/{path.name}"
            loaded, error = _load(path)
            if loaded is None:
                findings.append(
                    Finding(
                        severity=Severity.ERROR,
                        code="unreadable_file",
                        message=f"{location} could not be read as a layout object: {error}",
                        location=location,
                    )
                )
                continue

            object_id = loaded.get("id")
            if not isinstance(object_id, str) or not object_id:
                findings.append(
                    Finding(
                        severity=Severity.ERROR,
                        code="missing_id",
                        message=f"{location} has no 'id'",
                        location=location,
                    )
                )
                continue

            if object_id != path.stem:
                findings.append(
                    Finding(
                        severity=Severity.ERROR,
                        code="filename_id_mismatch",
                        message=(
                            f"{location} declares id {object_id!r}; the layout writes one file per "
                            f"object named by its id, so this object would be written to "
                            f"{object_id}.yaml and overwrite whatever owns that name"
                        ),
                        object_id=object_id,
                        location=location,
                    )
                )

            if object_id in ids_seen:
                findings.append(
                    Finding(
                        severity=Severity.ERROR,
                        code="duplicate_id_in_files",
                        message=f"{location} and {ids_seen[object_id]} both declare id {object_id!r}",
                        object_id=object_id,
                        location=location,
                    )
                )
            else:
                ids_seen[object_id] = location

    return findings
