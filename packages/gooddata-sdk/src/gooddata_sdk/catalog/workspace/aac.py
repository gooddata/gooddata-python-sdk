# (C) 2026 GoodData Corporation
from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any, Literal

from gooddata_code_convertors import (
    declarative_attribute_hierarchy_to_yaml,
    declarative_dashboard_to_yaml,
    declarative_dataset_to_yaml,
    declarative_date_instance_to_yaml,
    declarative_metric_to_yaml,
    declarative_plugin_to_yaml,
    declarative_visualisation_to_yaml,
    yaml_attribute_hierarchy_to_declarative,
    yaml_dashboard_to_declarative,
    yaml_dataset_to_declarative,
    yaml_date_dataset_to_declarative,
    yaml_metric_to_declarative,
    yaml_plugin_to_declarative,
    yaml_visualisation_to_declarative,
)

from gooddata_sdk.catalog.workspace.declarative_model.workspace.workspace import CatalogDeclarativeWorkspaceModel
from gooddata_sdk.utils import read_layout_from_file

_AAC_DEPRECATION_MSG = (
    "AAC analytics model support is deprecated and will be removed in a future version. "
    "The AAC analytics model API endpoints have been removed from the GoodData platform. "
    "Use the declarative workspace model API directly instead."
)

# AAC types that map to visualization objects (all go through yaml_visualisation_to_declarative)
_VISUALIZATION_TYPES = frozenset(
    {
        "bar_chart",
        "column_chart",
        "line_chart",
        "area_chart",
        "pie_chart",
        "donut_chart",
        "scatter_chart",
        "bubble_chart",
        "heatmap_chart",
        "treemap_chart",
        "bullet_chart",
        "funnel_chart",
        "pyramid_chart",
        "waterfall_chart",
        "sankey_chart",
        "dependency_wheel_chart",
        "combo_chart",
        "headline_chart",
        "geo_chart",
        "geo_area_chart",
        "repeater_chart",
        "table",
    }
)

# All known AAC type values
_ALL_AAC_TYPES = (
    frozenset({"dataset", "date", "metric", "dashboard", "plugin", "attribute_hierarchy"}) | _VISUALIZATION_TYPES
)

# Types that are "dataset-like" for the entities array
_DATASET_TYPES = frozenset({"dataset", "date"})


# ---------------------------------------------------------------------------
# Entities list builder (needed for cross-reference resolution)
# ---------------------------------------------------------------------------


def _build_entities(aac_objects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build the entities array expected by convertor functions.

    Some convertor functions (dataset, visualization, dashboard) need access to
    all objects for cross-reference resolution (e.g., dataset references).
    """
    return [
        {
            "id": obj["id"],
            "type": obj["type"],
            "path": f"{obj['id']}.yaml",
            "data": obj,
        }
        for obj in aac_objects
    ]


# ---------------------------------------------------------------------------
# Individual object conversions: AAC dict → Declarative dict
# ---------------------------------------------------------------------------


def aac_dataset_to_declarative(
    aac: dict[str, Any],
    entities: list[dict[str, Any]] | None = None,
    data_source_id: str | None = None,
) -> dict[str, Any]:
    """Convert an AAC dataset dict to declarative format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Args:
        aac: The AAC dataset dict (parsed YAML).
        entities: Optional list of all AAC objects for cross-reference resolution.
        data_source_id: Optional data source ID for table-based datasets.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    ent = entities if entities is not None else _build_entities([aac])
    args: list[Any] = [ent, aac]
    if data_source_id is not None:
        args.append(data_source_id)
    return yaml_dataset_to_declarative(*args)


def aac_date_dataset_to_declarative(aac: dict[str, Any]) -> dict[str, Any]:
    """Convert an AAC date dataset dict to declarative format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return yaml_date_dataset_to_declarative(aac)


def aac_metric_to_declarative(aac: dict[str, Any]) -> dict[str, Any]:
    """Convert an AAC metric dict to declarative format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return yaml_metric_to_declarative(aac)


def aac_visualization_to_declarative(
    aac: dict[str, Any],
    entities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Convert an AAC visualization dict to declarative format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Args:
        aac: The AAC visualization dict (parsed YAML).
        entities: Optional list of all AAC objects for cross-reference resolution.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    ent = entities if entities is not None else _build_entities([aac])
    return yaml_visualisation_to_declarative(ent, aac)


def aac_dashboard_to_declarative(
    aac: dict[str, Any],
    entities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Convert an AAC dashboard dict to declarative format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Args:
        aac: The AAC dashboard dict (parsed YAML).
        entities: Optional list of all AAC objects for cross-reference resolution.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    ent = entities if entities is not None else _build_entities([aac])
    return yaml_dashboard_to_declarative(ent, aac)


def aac_plugin_to_declarative(aac: dict[str, Any]) -> dict[str, Any]:
    """Convert an AAC plugin dict to declarative format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return yaml_plugin_to_declarative(aac)


def aac_attribute_hierarchy_to_declarative(aac: dict[str, Any]) -> dict[str, Any]:
    """Convert an AAC attribute hierarchy dict to declarative format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return yaml_attribute_hierarchy_to_declarative(aac)


# ---------------------------------------------------------------------------
# Individual object conversions: Declarative dict → AAC dict
# Returns {"json": dict, "content": str}
# ---------------------------------------------------------------------------


def declarative_dataset_to_aac(
    declarative: dict[str, Any],
    profile: dict[str, Any] | None = None,
    tables_map: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Convert a declarative dataset dict to AAC format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Args:
        declarative: The declarative dataset dict.
        profile: Optional profile dict with host, token, workspace_id, data_source.
        tables_map: Optional mapping of data source ID to list of table definitions.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    p = profile if profile is not None else {}
    t = tables_map if tables_map is not None else {}
    return declarative_dataset_to_yaml(declarative, p, t)


def declarative_date_instance_to_aac(declarative: dict[str, Any]) -> dict[str, Any]:
    """Convert a declarative date instance dict to AAC format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return declarative_date_instance_to_yaml(declarative)


def declarative_metric_to_aac(declarative: dict[str, Any]) -> dict[str, Any]:
    """Convert a declarative metric dict to AAC format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return declarative_metric_to_yaml(declarative)


def declarative_visualization_to_aac(
    declarative: dict[str, Any],
    entities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Convert a declarative visualization dict to AAC format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Args:
        declarative: The declarative visualization dict.
        entities: Optional entities list for cross-reference resolution.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    ent = entities if entities is not None else []
    return declarative_visualisation_to_yaml(ent, declarative)


def declarative_dashboard_to_aac(
    declarative: dict[str, Any],
    entities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Convert a declarative dashboard dict to AAC format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Args:
        declarative: The declarative dashboard dict.
        entities: Optional entities list for cross-reference resolution.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    ent = entities if entities is not None else []
    return declarative_dashboard_to_yaml(ent, declarative)


def declarative_plugin_to_aac(declarative: dict[str, Any]) -> dict[str, Any]:
    """Convert a declarative plugin dict to AAC format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return declarative_plugin_to_yaml(declarative)


def declarative_attribute_hierarchy_to_aac(declarative: dict[str, Any]) -> dict[str, Any]:
    """Convert a declarative attribute hierarchy dict to AAC format.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    return declarative_attribute_hierarchy_to_yaml(declarative)


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------


def detect_yaml_format(path: Path) -> Literal["aac", "declarative"]:
    """Detect whether a directory contains AAC or declarative YAMLs.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    AAC files have a top-level 'type' field (dataset, metric, line_chart, etc.)
    and live as flat files or in typed subdirectories (datasets/, metrics/, etc.).

    Declarative files follow a nested folder structure with
    workspaces/<id>/ldm/ and workspaces/<id>/analytics_model/.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    # Check for declarative structure markers
    if (path / "workspaces").is_dir() or (path / "ldm").is_dir() or (path / "analytics_model").is_dir():
        return "declarative"

    # Check for AAC markers: typed subdirectories
    aac_subdirs = {"datasets", "metrics", "visualisations", "dashboards", "plugins", "attributeHierarchies"}
    for subdir in aac_subdirs:
        if (path / subdir).is_dir():
            return "aac"

    # Check YAML files for top-level 'type' field
    for yaml_file in path.glob("*.yaml"):
        content = read_layout_from_file(yaml_file)
        if isinstance(content, dict) and content.get("type") in _ALL_AAC_TYPES:
            return "aac"
        break  # Only check the first file

    return "declarative"


# ---------------------------------------------------------------------------
# Workspace-level: load AAC from disk → CatalogDeclarativeWorkspaceModel
# ---------------------------------------------------------------------------


def _collect_aac_yaml_files(source_dir: Path) -> list[Path]:
    """Collect all AAC YAML files from source_dir (flat and typed subdirs)."""
    files: list[Path] = []

    # Flat YAML files in source_dir root
    files.extend(sorted(source_dir.glob("*.yaml")))
    files.extend(sorted(source_dir.glob("*.yml")))

    # Typed subdirectories used by gd CLI
    for subdir in sorted(source_dir.iterdir()):
        if subdir.is_dir() and subdir.name not in {
            "data_sources",
            "users",
            "user_groups",
            "workspaces_data_filters",
            "workspaces",
        }:
            files.extend(sorted(subdir.rglob("*.yaml")))
            files.extend(sorted(subdir.rglob("*.yml")))

    return files


def load_aac_workspace_from_disk(
    source_dir: Path,
    data_source_id: str | None = None,
) -> CatalogDeclarativeWorkspaceModel:
    """Load AAC YAML files from source_dir and return a declarative workspace model.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Reads all .yaml/.yml files, detects object type from the 'type' field,
    converts each to declarative format, and assembles into a
    CatalogDeclarativeWorkspaceModel.

    Args:
        source_dir: Path to directory containing AAC YAML files.
        data_source_id: Optional data source ID for table-based datasets.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    # First pass: read all AAC objects and build entities list
    aac_objects: list[dict[str, Any]] = []
    for yaml_file in _collect_aac_yaml_files(source_dir):
        content = read_layout_from_file(yaml_file)
        if isinstance(content, dict) and "type" in content:
            aac_objects.append(content)

    entities = _build_entities(aac_objects)

    # Second pass: convert each object
    datasets: list[dict[str, Any]] = []
    date_instances: list[dict[str, Any]] = []
    metrics: list[dict[str, Any]] = []
    visualization_objects: list[dict[str, Any]] = []
    analytical_dashboards: list[dict[str, Any]] = []
    dashboard_plugins: list[dict[str, Any]] = []
    attribute_hierarchies: list[dict[str, Any]] = []

    for aac in aac_objects:
        aac_type = aac.get("type")

        match aac_type:
            case "dataset":
                datasets.append(aac_dataset_to_declarative(aac, entities, data_source_id))
            case "date":
                date_instances.append(aac_date_dataset_to_declarative(aac))
            case "metric":
                metrics.append(aac_metric_to_declarative(aac))
            case "dashboard":
                result = aac_dashboard_to_declarative(aac, entities)
                # Dashboard convertor may return dashboard + filterContext
                if isinstance(result, dict) and "dashboard" in result:
                    analytical_dashboards.append(result["dashboard"])
                else:
                    analytical_dashboards.append(result)
            case "plugin":
                dashboard_plugins.append(aac_plugin_to_declarative(aac))
            case "attribute_hierarchy":
                attribute_hierarchies.append(aac_attribute_hierarchy_to_declarative(aac))
            case vis_type if vis_type in _VISUALIZATION_TYPES:
                visualization_objects.append(aac_visualization_to_declarative(aac, entities))

    workspace_model_dict: dict[str, Any] = {}

    ldm: dict[str, Any] = {}
    if datasets:
        ldm["datasets"] = datasets
    if date_instances:
        ldm["dateInstances"] = date_instances
    if ldm:
        workspace_model_dict["ldm"] = ldm

    analytics: dict[str, Any] = {}
    if metrics:
        analytics["metrics"] = metrics
    if visualization_objects:
        analytics["visualizationObjects"] = visualization_objects
    if analytical_dashboards:
        analytics["analyticalDashboards"] = analytical_dashboards
    if dashboard_plugins:
        analytics["dashboardPlugins"] = dashboard_plugins
    if attribute_hierarchies:
        analytics["attributeHierarchyObjects"] = attribute_hierarchies
    if analytics:
        workspace_model_dict["analytics"] = analytics

    return CatalogDeclarativeWorkspaceModel.from_dict(workspace_model_dict)


# ---------------------------------------------------------------------------
# Workspace-level: CatalogDeclarativeWorkspaceModel → AAC files on disk
# ---------------------------------------------------------------------------


def _write_aac_file(source_dir: Path, subdir: str, obj_id: str, content: str) -> None:
    """Write a single AAC YAML file to disk."""
    target_dir = source_dir / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"{obj_id}.yaml"
    target_file.write_text(content, encoding="utf-8")


def store_aac_workspace_to_disk(model: CatalogDeclarativeWorkspaceModel, source_dir: Path) -> None:
    """Convert a declarative workspace model to AAC YAML files and write to disk.

    .. deprecated::
        AAC analytics model support is deprecated. Use the declarative workspace model API directly.

    Creates typed subdirectories (datasets/, metrics/, visualisations/, dashboards/,
    plugins/, attributeHierarchies/) under source_dir.
    """
    warnings.warn(_AAC_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    source_dir.mkdir(parents=True, exist_ok=True)
    model_dict = model.to_dict(camel_case=True)

    ldm = model_dict.get("ldm", {})
    analytics = model_dict.get("analytics", {})

    for dataset in ldm.get("datasets", []):
        result = declarative_dataset_to_aac(dataset)
        _write_aac_file(source_dir, "datasets", dataset["id"], result["content"])

    for date_instance in ldm.get("dateInstances", []):
        result = declarative_date_instance_to_aac(date_instance)
        _write_aac_file(source_dir, "datasets", date_instance["id"], result["content"])

    for metric in analytics.get("metrics", []):
        result = declarative_metric_to_aac(metric)
        _write_aac_file(source_dir, "metrics", metric["id"], result["content"])

    for vis in analytics.get("visualizationObjects", []):
        result = declarative_visualization_to_aac(vis)
        _write_aac_file(source_dir, "visualisations", vis["id"], result["content"])

    for dashboard in analytics.get("analyticalDashboards", []):
        result = declarative_dashboard_to_aac(dashboard)
        _write_aac_file(source_dir, "dashboards", dashboard["id"], result["content"])

    for plugin in analytics.get("dashboardPlugins", []):
        result = declarative_plugin_to_aac(plugin)
        _write_aac_file(source_dir, "plugins", plugin["id"], result["content"])

    for hierarchy in analytics.get("attributeHierarchyObjects", []):
        result = declarative_attribute_hierarchy_to_aac(hierarchy)
        _write_aac_file(source_dir, "attributeHierarchies", hierarchy["id"], result["content"])
