---
title: "create_or_update"
linkTitle: "create_or_update"
weight: 10
superheading: "catalog_workspace."
---

<!-- TODO -->

``create_or_update(workspace: CatalogWorkspace)``

Create a new workspace or overwrite an existing workspace with the same id.

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
