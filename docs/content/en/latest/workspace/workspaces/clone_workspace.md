---
title: "clone_workspace"
linkTitle: "clone_workspace"
weight: 21
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.clone_workspace" >}}

## Example

```python
# Clones complete workspace content - LDM, ADM, permissions.
sdk.catalog_workspace.clone_workspace(
        source_workspace_id="123",
        target_workspace_id="xyz",
        target_workspace_name="Demo"
)
```
