---
title: "load_and_put_declarative_workspace_data_filters"
linkTitle: "load_and_put_declarative_worksp..."
weight: 180
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.load_and_put_declarative_workspace_data_filters" >}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put on server the stored layout
sdk.catalog_workspace.load_and_put_declarative_workspace_data_filters(layout_root_path=Path.cwd())
```

Or by two separate calls:

```python
# Load the workspace data filters
workspace_filters = sdk.catalog_workspace.load_declarative_workspace_data_filters(
    layout_root_path=Path.cwd()
)

# Puth the filters back on server
sdk.catalog_workspace.put_declarative_workspace_data_filters(
    workspace_data_filters= workspace_filters
)
```

The result is identical.
