---
title: "load_declarative_workspace"
linkTitle: "load_declarative_workspace"
weight: 120
superheading: "catalog_workspace."
---

<!-- TODO -->

``load_declarative_workspace(workspace_id: str, layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeWorkspaceModel*.

Load declarative workspaces layout, which was stored using [store_declarative_workspace](../store_declarative_workspace).

## Example

```Python
# Load a declarative workspace
declarative_workspace = sdk.catalog_workspace.load_declarative_workspace(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
