---
title: "delete_workspace"
linkTitle: "delete_workspace"
weight: 30
superheading: "catalog_workspace."
---

<!-- TODO -->

``delete_workspace(workspace_id: str)``

Delete a workspace with all its content - logical model and analytics model.

## Example

```python
# Delete workspace
sdk.catalog_workspace.delete_workspace(workspace_id="test_demo")
```
