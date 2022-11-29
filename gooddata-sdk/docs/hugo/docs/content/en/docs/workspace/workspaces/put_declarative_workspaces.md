---
title: "put_declarative_workspaces"
linkTitle: "put_declarative_workspaces"
weight: 60
superheading: "catalog_workspace."
---

<!-- TODO -->

``put_declarative_workspaces(workspace: CatalogDeclarativeWorkspaces)``

Set layout of all workspaces and their hierarchy.

## Example

```Python
# Load declarative workspaces
declarative_workspaces = sdk.catalog_workspace.get_declarative_workspaces()

# Do changes
# ...

#Set the layout and hierachy
sdk.catalog_workspace.put_declarative_workspaces(workspace=declarative_workspaces)
```
