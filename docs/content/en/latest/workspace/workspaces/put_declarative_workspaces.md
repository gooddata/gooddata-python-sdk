---
title: "put_declarative_workspaces"
linkTitle: "put_declarative_workspaces"
weight: 60
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.put_declarative_workspaces" >}}

## Example

```python
# Load declarative workspaces
declarative_workspaces = sdk.catalog_workspace.get_declarative_workspaces()

# Do changes
# ...

# Set the layout and hierachy
sdk.catalog_workspace.put_declarative_workspaces(declarative_workspaces)
```
