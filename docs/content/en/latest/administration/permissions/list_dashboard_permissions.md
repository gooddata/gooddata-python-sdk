---
title: "list_dashboard_permissions"
linkTitle: "list_dashboard_permissions"
weight: 16
no_list: true
superheading: "catalog_permission."
---



``list_dashboard_permissions(workspace_id: str, dashboard_id: str) -> CatalogDashboardPermissions``

Provide list of users and user groups with granted dashboard permissions for particular dashboard

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="workspace_id" p_type="str" >}}
Workspace identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="dashboard_id" p_type="str" >}}
Dashboard identification string. e.g. "campaign"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}

{{< parameter p_type="CatalogDashboardPermissions" >}}
Object containing users and user groups and granted dashboard permissions and any permission rules in effect.
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# list all dashboard permissions
permissions = list_dashboard_permissions(workspace_id="demo",dashboard_id="sales")
```
