---
title: "put_declarative_permissions"
linkTitle: "put_declarative_permissions"
weight: 20
no_list: true
superheading: "catalog_permission."
---

{{< api-ref "sdk.CatalogPermissionService.put_declarative_permissions" >}}

## Example

```python
permissions=[CatalogDeclarativeSingleWorkspacePermission(name="ANALYZE", assignee=CatalogAssigneeIdentifier(id="demo", type="user"))]
hierarchy_permissions=[CatalogDeclarativeWorkspaceHierarchyPermission(name="ANALYZE", assignee=CatalogAssigneeIdentifier(id="adminGroup", type="userGroup"))]
declarative_permissions = CatalogDeclarativeWorkspacePermissions(permissions=permissions, hierarchy_permissions=hierarchy_permissions)

# Update permissions on the server with your changes
sdk.catalog_permission.put_declarative_permissions(workspace_id=workspace_id,
                                                    declarative_workspace_permissions=declarative_permissions)
```
