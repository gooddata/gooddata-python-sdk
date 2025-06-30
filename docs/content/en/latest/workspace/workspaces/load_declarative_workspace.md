---
title: "load_declarative_workspace"
linkTitle: "load_declarative_workspace"
weight: 120
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.load_declarative_workspace" >}}

## Example

```python
# Load a declarative workspace
declarative_workspace = sdk.catalog_workspace.load_declarative_workspace(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
