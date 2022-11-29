---
title: "load_declarative_workspaces"
linkTitle: "load_declarative_workspaces"
weight: 80
superheading: "catalog_workspace."
---

<!-- TODO -->

``load_declarative_workspaces(layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeWorkspaces*.

Load declarative workspaces layout, which was stored using [store_declarative_workspaces](../store_declarative_workspaces).

## Example

```Python
# Load declarative workspaces
declarative_workspaces = sdk.catalog_workspace.load_declarative_workspaces(
    layout_root_path=Path.cwd()
)
```
