---
title: "load_analytics_model_from_disk"
linkTitle: "load_analytics_model_from_disk"
weight: 132
superheading: "catalog_workspace_content."
---

``load_analytics_model_from_disk(path: Path = Path.cwd())``

Returns *CatalogDeclarativeAnalytics*.

The method is used to load analytics model stored to disk using method [store_analytics_model_to_disk](../store_analytics_model_to_disk).

## Example

```Python
#Retrieve Analytics model from disk
declarative_analytics = sdk.catalog_workspace_content.load_analytics_model_from_disk(
    path=Path.cwd()
)
```
