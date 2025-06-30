---
title: "load_and_put_declarative_analytics_model"
linkTitle: "load_and_put_declarative_analyt..."
weight: 150
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.load_and_put_declarative_analytics_model" >}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put on server the stored layout
sdk.catalog_workspace_content.load_and_put_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```

Or by two separate calls:

```python
# Get analytics layout
declarative_analytics = sdk.catalog_workspace_content.load_declarative_analytics_model(
    workspace_id="123",
    layout_root_path=Path.cwd()
)

# Put analytics model object back to the server:
sdk.catalog_workspace_content.put_declarative_analytics_model(
    workspace_id="123",
    analytics_model=declarative_analytics
)
```

The result is identical.
