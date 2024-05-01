---
title: "store_declarative_analytics_model"
linkTitle: "store_declarative_analytics_model"
weight: 130
superheading: "catalog_workspace_content."
---



``store_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

Stores declarative analytics model for a given workspace in directory hierarchy. This method ties the declarative analytics model to the workspace and organization, thus it is recommended for backups. If you want to move declarative analytics model between workspaces or organizations, use [store_analytics_model_to_disk](../store_analytics_model_to_disk/).

Store declarative analytics model layout in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── workspaces
                    └── workspace_id
                            └── analytics_model
                                    ├── analytical_dashboards
                                    │       └── analytical_dashboard.yaml
                                    ├── dashboard_plugins
                                    │       └── dashboard_plugin.yaml
                                    ├── filter_contexts
                                    │       └── filter_context.yaml
                                    ├── metrics
                                    │       └── metric.yaml
                                    └── visualization_objects
                                            └── visualization_object.yaml

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="str" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Store the analytics model to disk
sdk.catalog_workspace_content.store_declarative_analytics_model(
        workspace_id="123",
        layout_root_path=Path.cwd()
)
```
