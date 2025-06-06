---
title: "get_user_group_permissions"
linkTitle: "get_user_group_permissions"
weight: 10
no_list: true
superheading: "catalog_user."
---



``get_user_group_permissions(user_group_id: str) -> CatalogPermissionAssignments``

Get permission assignments for a user group.

{{% parameters-block title="Parameters"%}}
{{< parameter p_name="user_group_id" p_type="string" >}}
User group identification string. e.g. "demo.users"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogPermissionAssignments" >}}
Object containing permission assignments for workspaces and data sources.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_user.get_user_group_permissions("demo.users")
"""
CatalogPermissionAssignments(workspaces=[CatalogWorkspacePermissionAssignment(id='demo_west',
                                                                              permissions=['VIEW', 'CREATE_AUTOMATION',
                                                                                           'EXPORT_PDF',
                                                                                           'CREATE_FILTER_VIEW'],
                                                                              hierarchy_permissions=[],
                                                                              name='Demo West')], data_sources=[])
"""
```
