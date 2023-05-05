---
title: "store_analytics_model_to_disk"
linkTitle: "store_analytics_model_to_disk"
weight: 131
superheading: "catalog_workspace_content."
---

``store_analytics_model_to_disk(workspace_id: str, path: Path = Path.cwd())``

Stores analytics model for a given workspace in directory hierarchy.This method does not tie the declarative analytics model to the workspace and organization, thus it is recommended for migration between workspaces. If you want to backup analytics model between workspaces or organizations, use [store_analytics_model_to_disk](../store_analytics_model_to_disk/).

The directory structure below shows the output for the path set to `Path("analytics_model_location")`.

    analytics_model_location
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
{{< parameter p_name="path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Store the analytics model to disk
sdk.catalog_workspace_content.store_analytics_model_to_disk(
        workspace_id="123",
        path=Path.cwd()
)
```
