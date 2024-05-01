---
title: "get_metrics_catalog"
linkTitle: "get_metrics_catalog"
weight: 30
superheading: "catalog_workspace_content."
---



``get_metrics_catalog(workspace_id: str)``

Gets all metrics for a workspace.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="list[CatalogMetric]" >}}
List of all metrics in a given workspace.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get all metrics
metrics = sdk.catalog_workspace_content.get_metrics_catalog(workspace_id="123")
```
