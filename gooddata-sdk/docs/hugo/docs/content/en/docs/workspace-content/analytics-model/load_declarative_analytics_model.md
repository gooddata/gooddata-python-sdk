---
title: "load_declarative_analytics_model"
linkTitle: "load_declarative_analytics_model"
weight: 140
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``load_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeAnalytics*.

Load declarative analytics layout, which was stored using [store_declarative_analytics_model](../store_declarative_analytics_model).

## Example

```Python
# Retrieve analytics layout
declarative_analytics = sdk.catalog_workspace_content.load_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
