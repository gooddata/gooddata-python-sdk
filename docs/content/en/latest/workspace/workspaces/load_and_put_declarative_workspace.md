---
title: "load_and_put_declarative_workspace"
linkTitle: "load_and_put_declarative_work..."
weight: 130
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.load_and_put_declarative_workspace" >}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put on server the stored layout
sdk.catalog_workspace.load_and_put_declarative_workspace(
    workspace_id="demo",
    layout_root_path=Path.cwd()
)
```

Or by two separate calls:

```python
# Load a declarative workspace
declarative_workspaces = sdk.catalog_workspace.load_declarative_workspace(
    workspace_id="demo",
    layout_root_path=Path.cwd()
)
# Set the layout
sdk.catalog_workspace.put_declarative_workspace(
    workspace_id="demo",
    workspace=declarative_workspaces
)
```

The result is identical.
