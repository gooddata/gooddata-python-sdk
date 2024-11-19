---
title: "load_declarative_workspaces"
linkTitle: "load_declarative_workspaces"
weight: 80
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.load_declarative_workspaces" >}}

## Example

```python
# Load declarative workspaces
declarative_workspaces = sdk.catalog_workspace.load_declarative_workspaces(
    layout_root_path=Path.cwd()
)
```
