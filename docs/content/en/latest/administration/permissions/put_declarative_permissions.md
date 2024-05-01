---
title: "put_declarative_permissions"
linkTitle: "put_declarative_permissions"
weight: 20
no_list: true
superheading: "catalog_permission."
---



``put_declarative_permissions(workspace_id: str, declarative_workspace_permissions: CatalogDeclarativeWorkspacePermissions)``

Sets the permissions for the workspace.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="declarative_workspace_permissions" p_type="CatalogDeclarativeWorkspacePermissions" >}}
Object Containing Workspace Permissions.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
permissions=[CatalogDeclarativeSingleWorkspacePermission(name="ANALYZE", assignee=CatalogAssigneeIdentifier(id="demo", type="user"))]
hierarchy_permissions=[CatalogDeclarativeWorkspaceHierarchyPermission(name="ANALYZE", assignee=CatalogAssigneeIdentifier(id="adminGroup", type="userGroup"))]
declarative_permissions = CatalogDeclarativeWorkspacePermissions(permissions=permissions, hierarchy_permissions=hierarchy_permissions)

# Update permissions on the server with your changes
sdk.catalog_permission.put_declarative_permissions(workspace_id=workspace_id,
                                                    declarative_workspace_permissions=declarative_permissions)
```
