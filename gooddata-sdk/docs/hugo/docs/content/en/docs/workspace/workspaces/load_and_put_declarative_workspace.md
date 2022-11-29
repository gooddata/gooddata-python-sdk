---
title: "load_and_put_declarative_workspace"
linkTitle: "load_and_put_declarative_work..."
weight: 130
superheading: "catalog_workspace."
---

<!-- TODO -->

``load_and_put_declarative_workspace(workspace_id: str, layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_workspace](../load_declarative_workspace) and [put_declarative_workspace](../put_declarative_workspace) methods to load and
set layouts stored using [store_declarative_workspace](../store_declarative_workspace).

## Example

The load and put can be done two ways.

Either by one call:

```Python
# Load and put on server the stored layout
sdk.catalog_workspaces.load_and_put_declarative_workspaces(
    layout_root_path=Path.cwd()
)
```

Or by two separate calls:

```Python
# Load a declarative workspace
declarative_workspaces = sdk.catalog_workspace.load_declarative_workspaces(
    layout_root_path=Path.cwd()
)
# Set the layout
sdk.catalog_workspace.put_declarative_workspaces(
    workspace=declarative_workspaces
)
```

The result is identical.
