---
title: "load_and_put_declarative_workspaces"
linkTitle: "load_and_put_declarative_work..."
weight: 90
superheading: "catalog_workspace."
---

<!-- TODO -->

``load_and_put_declarative_workspaces(layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_workspaces](../load_declarative_workspaces) and [put_declarative_workspaces](../put_declarative_workspaces) methods to load and
set layouts stored using [store_declarative_workspaces](../store_declarative_workspaces).

## Example

The load and put can be done two ways.

Either by one call:

```Python
# Load and put on server the stored layout
sdk.catalog_workspace.load_and_put_declarative_workspaces(
    layout_root_path=Path.cwd()
)
```

Or by two separate calls:

```Python
# Load a declarative workspace
declarative_workspace = sdk.catalog_workspace.load_declarative_workspace(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
# Set the layout
sdk.catalog_workspace.put_declarative_workspace(
    workspace_id="123",
    workspace=declarative_workspace
    )
```

The result is identical.
