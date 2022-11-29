---
title: "load_and_put_declarative_analytics_model"
linkTitle: "load_and_put_declarative_analyt..."
weight: 150
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``load_and_put_declarative_analytics_model(workspace_id: str, layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_analytics_model](../load_declarative_analytics_model) and [put_declarative_analytics_model](../put_declarative_analytics_model) methods to load and set layouts stored using [store_declarative_analytics_model](../store_declarative_analytics_model).

## Example

The load and put can be done two ways.

Either by one call:

```Python
# Load and put on server the stored layout
sdk.catalog_workspace.load_and_put_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```

Or by two separate calls:

```Python
# Retrieve analytics layout
declarative_analytics = sdk.catalog_workspace_content.load_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)

#Put analytics model object back to the server:
sdk.catalog_workspace_content.put_declarative_analytics_model(
    workspace_id="123",
    analytics_model=declarative_analytics
)
```

The result is identical.
