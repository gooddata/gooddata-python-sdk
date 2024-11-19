---
title: "store_declarative_analytics_model"
linkTitle: "store_declarative_analytics_model"
weight: 130
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.store_declarative_analytics_model" >}}

## Example

```python
# Store the analytics model to disk
sdk.catalog_workspace_content.store_declarative_analytics_model(
        workspace_id="123",
        layout_root_path=Path.cwd()
)
```
