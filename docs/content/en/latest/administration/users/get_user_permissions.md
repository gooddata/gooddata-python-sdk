---
title: "get_user_permissions"
linkTitle: "get_user_permissions"
weight: 10
no_list: true
superheading: "catalog_user."
---



``get_user_permissions(user_id: str) -> CatalogPermissionAssignments``

Get permission assignments for a user.

{{% parameters-block title="Parameters"%}}
{{< parameter p_name="user_id" p_type="string" >}}
User identification string. e.g. "admin"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogPermissionAssignments" >}}
Object containing permission assignments for workspaces and data sources.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_user.get_user_permissions("demo.user")
"""
CatalogPermissionAssignments(workspaces=[CatalogWorkspacePermissionAssignment(id='demo_west',
                                                                              permissions=['VIEW', 'CREATE_AUTOMATION',
                                                                                           'EXPORT_PDF',
                                                                                           'CREATE_FILTER_VIEW'],
                                                                              hierarchy_permissions=[],
                                                                              name='Demo West')], data_sources=[])
"""
```
