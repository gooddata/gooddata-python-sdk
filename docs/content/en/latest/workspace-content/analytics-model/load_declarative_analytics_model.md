---
title: "load_declarative_analytics_model"
linkTitle: "load_declarative_analytics_model"
weight: 140
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.load_declarative_analytics_model" >}}

## Example

```python
# Get analytics layout
declarative_analytics = sdk.catalog_workspace_content.load_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
