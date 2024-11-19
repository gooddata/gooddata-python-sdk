---
title: "load_analytics_model_from_disk"
linkTitle: "load_analytics_model_from_disk"
weight: 132
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.load_analytics_model_from_disk" >}}

## Example

```python
# Get Analytics model from disk
declarative_analytics = sdk.catalog_workspace_content.load_analytics_model_from_disk(
    path=Path.cwd()
)
```
