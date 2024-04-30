---
title: "store_declarative_workspaces"
linkTitle: "store_declarative_workspaces"
weight: 70
superheading: "catalog_workspace."
---



``store_declarative_workspaces(layout_root_path: Path = Path.cwd())``

Stores declarative workspaces in a given path, as folder hierarchy.

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

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Store workspace layout and hierarchy
sdk.catalog_workspace.store_declarative_workspaces(layout_root_path=Path.cwd())
```
