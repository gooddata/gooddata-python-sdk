---
title: "store_declarative_workspace"
linkTitle: "store_declarative_workspace"
weight: 115
superheading: "catalog_workspace."
---



`store_declarative_workspace(workspace_id: str, layout_root_path: Path = Path.cwd())`

Stores the workspace layout in a directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── workspaces
                    └── workspace_a
                            ├── analytics_model
                            │   ├── analytical_dashboards
                            │   │       └── analytical_dashboard.yaml
                            │   ├── dashboard_plugins
                            │   │       └── dashboard_plugin.yaml
                            │   ├── filter_contexts
                            │   │       └── filter_context.yaml
                            │   ├── metrics
                            │   │       └── metric.yaml
                            │   └── visualization_objects
                            │           └── visualization_object.yaml
                            └── ldm
                                ├── datasets
                                │       └── dataset.yaml
                                └── date_instances
                                        └── date_instance.yaml

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
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
# Store workspace layout
sdk.catalog_workspace.store_declarative_workspace(workspace_id="123",layout_root_path=Path.cwd())
```
