---
title: "get_declarative_permissions"
linkTitle: "get_declarative_permissions"
weight: 10
no_list: true
superheading: "catalog_permission."
---

<!-- TODO -->

``get_declarative_permissions(workspace_id: str)``

Returns *CatalogDeclarativeWorkspacePermissions*.

Retrieve current set of permissions of the workspace in a declarative form.

## Example

```python
# Get permissions in declarative from
declarative_permissions = sdk.catalog_permission.get_declarative_permissions(workspace_id=workspace_id)
```
