---
title: "store_declarative_workspaces"
linkTitle: "store_declarative_workspaces"
weight: 70
superheading: "catalog_workspace."
---

<!-- TODO -->

``store_declarative_workspaces(layout_root_path: Path = Path.cwd())``

Store workspaces layouts in directory hierarchy.

    gooddata_layouts
    └── organization_id
            ├── workspaces
            │       ├── workspace_a
            │       │       ├── analytics_model
            │       │       │   ├── analytical_dashboards
            │       │       │   │       └── analytical_dashboard.yaml
            │       │       │   ├── dashboard_plugins
            │       │       │   │       └── dashboard_plugin.yaml
            │       │       │   ├── filter_contexts
            │       │       │   │       └── filter_context.yaml
            │       │       │   ├── metrics
            │       │       │   │       └── metric.yaml
            │       │       │   └── visualization_objects
            │       │       │           └── visualization_object.yaml
            │       │       ├── ldm
            │       │       │   ├── datasets
            │       │       │   │       └── dataset.yaml
            │       │       │   └── date_instances
            │       │       │           └── date_instance.yaml
            │       │       └── workspace_a.yaml
            │       └── workspace_b
            │               └── ...
            │
            └── workspaces_data_filters
                    ├── filter_1.yaml
                    └── filter_2.yaml

## Example

```Python
# Store workspace layout and hierarchy
sdk.catalog_workspace.store_declarative_workspaces(layout_root_path=Path.cwd())
```
