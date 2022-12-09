---
title: "load_and_put_declarative_workspace_data_filters"
linkTitle: "load_and_put_declarative_worksp..."
weight: 180
superheading: "catalog_workspace."
---

<!-- TODO -->

``load_and_put_declarative_workspace_data_filters(layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_workspace_data_filters](../load_declarative_workspace_data_filters) and [put_declarative_workspace_data_filters](../put_declarative_workspace_data_filters) methods to load and set layouts stored using [store_declarative_workspace_data_filters](../store_declarative_workspace_data_filters).

## Example

The load and put can be done two ways.

Either by one call:

```Python
# Load and put on server the stored layout
sdk.catalog_workspace.load_and_put_declarative_workspace_data_filters(layout_root_path=Path.cwd())
```

Or by two separate calls:

```Python
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
