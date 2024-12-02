---
title: "create_or_update"
linkTitle: "create_or_update"
weight: 10
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.create_or_update" >}}

## Example

```python
# Create workspace
sdk.catalog_workspace.create_or_update(
    CatalogWorkspace(
        workspace_id="123",
        name="Test demo",
        parent_id="demo"
    )
)
```
