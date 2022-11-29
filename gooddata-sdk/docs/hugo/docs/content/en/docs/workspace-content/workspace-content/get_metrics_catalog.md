---
title: "get_metrics_catalog"
linkTitle: "get_metrics_catalog"
weight: 30
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``get_metrics_catalog(workspace_id: str)``

Returns *list[CatalogMetric]*

Retrieve all metrics for a workspace.

## Example

```Python
# Get all metrics
metrics = sdk.catalog_workspace_content.get_metrics_catalog(workspace_id="123")
```
