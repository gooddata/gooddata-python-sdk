---
title: "put_declarative_workspace"
linkTitle: "put_declarative_workspace"
weight: 110
superheading: "catalog_workspace."
---

<!-- TODO -->

``put_declarative_workspace(workspace_id: str, workspace: CatalogDeclarativeWorkspaceModel)``

Set a workspace layout.

## Example

```Python
# Get workspace
declarative_workspace = sdk.catalog_workspace.get_workspace(workspace_id="123")

# Do some changes
# ...

# Set the layout
sdk.catalog_workspace.put_declarative_workspace(
    workspace_id="123",
    workspace=declarative_workspace
)
```
