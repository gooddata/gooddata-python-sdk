---
title: "manage_dashboard_permissions"
linkTitle: "manage_dashboard_permissions"
weight: 15
no_list: true
superheading: "catalog_permission."
---



``manage_dashboard_permissions(workspace_id: str, dashboard_id: str, permissions_for_assignee: List[Union[CatalogPermissionsForAssigneeIdentifier, CatalogPermissionsForAssigneeRule]] ) -> None``

Provide managing dashboard permissions for user and user groups.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="workspace_id" p_type="str" >}}
Workspace identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="dashboard_id" p_type="str" >}}
Dashboard identification string. e.g. "campaign"
{{< /parameter >}}
{{< parameter p_name="permissions_for_assignee" p_type="List[Union[CatalogPermissionsForAssigneeIdentifier, CatalogPermissionsForAssigneeRule]]" >}}
Object containing list of users, user groups, or rules and desired dashboard permissions. Set empty list permissions for user/user group means remove dashboard permissions.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
manage_dashboard_permissions(
    workspace_id="demo",
    dashboard_id="sales",
    permissions_for_assignee=[
        CatalogPermissionsForAssigneeIdentifier(
            assignee_identifier=CatalogAssigneeIdentifier(id="demoGroup", type="userGroup"),
            permissions=["EDIT"],
        ),
        CatalogPermissionsForAssigneeRule(
            assignee_rule=CatalogAssigneeRule(type="allWorkspaceUsers"),
            permissions=["VIEW"],
        ),
    ],
)
```
