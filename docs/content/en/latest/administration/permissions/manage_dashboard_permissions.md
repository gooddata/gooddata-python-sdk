---
title: "manage_dashboard_permissions"
linkTitle: "manage_dashboard_permissions"
weight: 15
no_list: true
superheading: "catalog_permission."
---

{{< api-ref "sdk.CatalogPermissionService.manage_dashboard_permissions" >}}

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
