---
title: "list_workspaces"
linkTitle: "list_workspaces"
weight: 40
superheading: "catalog_workspace."
---

<!-- TODO -->

``list_workspaces()``

Returns *List[CatalogWorkspace]*.

Get a list of all existing workspaces.

## Example

```python
# List workspaces
workspaces = sdk.catalog_workspace.list_workspaces()

print(workspaces)
# [
#   CatalogWorkspace(id=demo, name=Demo),
#   CatalogWorkspace(id=demo_west, name=Demo West),
#   CatalogWorkspace(id=demo_west_california, name=Demo West California)
# ]
```
