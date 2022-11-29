---
title: "put_declarative_permissions"
linkTitle: "put_declarative_permissions"
weight: 20
no_list: true
superheading: "catalog_permission."
---

<!-- TODO -->

``put_declarative_permissions(workspace_id: str, declarative_workspace_permissions: CatalogDeclarativeWorkspacePermissions)``

Set effective permissions for the workspace.

## Example

```python
# Update permissions on the server with your changes
sdk.catalog_permission.put_declarative_permissions(workspace_id=workspace_id,
                                                    declarative_workspace_permissions=declarative_permissions)
```
