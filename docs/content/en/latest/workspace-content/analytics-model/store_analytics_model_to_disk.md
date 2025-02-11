---
title: "store_analytics_model_to_disk"
linkTitle: "store_analytics_model_to_disk"
weight: 131
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.store_analytics_model_to_disk" >}}

## Example

```python
# Store the analytics model to disk
sdk.catalog_workspace_content.store_analytics_model_to_disk(
        workspace_id="123",
        path=Path.cwd()
)
```
