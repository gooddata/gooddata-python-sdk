---
title: "load_declarative_workspace_data_filters"
linkTitle: "load_declarative_workspace_data_..."
weight: 170
superheading: "catalog_workspace."
---

<!-- TODO -->

``load_declarative_workspace_data_filters(layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeWorkspaceDataFilters*.

Load declarative workspaces layout, which was stored using [store_declarative_workspace_data_filters](../store_declarative_workspace_data_filters).

## Example

```Python
# Load the workspace data filters
declarative_workspace_filters = sdk.catalog_workspace.load_declarative_workspace_data_filters(
    layout_root_path=Path.cwd()
)
```
