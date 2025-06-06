---
title: "manage_user_group_permissions"
linkTitle: "manage_user_group_permissions"
weight: 10
no_list: true
superheading: "catalog_user."
---



``manage_user_group_permissions(user_group_id: str, api_token_id: str) -> None``

Set permission assignments for a user.

{{% parameters-block title="Parameters"%}}
{{< parameter p_name="user_group_id" p_type="string" >}}
User group identification string. e.g. "demo.users"
{{< /parameter >}}
{{< parameter p_name="permission_assignments" p_type="CatalogPermissionAssignments" >}}
Object containing permission assignments for workspaces and data sources.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
permissions = CatalogPermissionAssignments(workspaces=[CatalogWorkspacePermissionAssignment(id='demo_west',
                                                                                            permissions=['VIEW',
                                                                                                         'CREATE_AUTOMATION',
                                                                                                         'EXPORT_PDF',
                                                                                                         'CREATE_FILTER_VIEW'],
                                                                                            hierarchy_permissions=[],
                                                                                            name='Demo West')],
                                           data_sources=[])
sdk.catalog_user.manage_user_group_permissions("demo.users", permissions)
```
