---
title: "list_available_assignees"
linkTitle: "list_available_assignees"
weight: 17
no_list: true
superheading: "catalog_permission."
---



``list_available_assignees(workspace_id: str, dashboard_id: str) -> CatalogAvailableAssignees``

Provide list of users and groups available to assign some dashboard permission

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="workspace_id" p_type="str" >}}
Workspace identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="dashboard_id" p_type="str" >}}
Dashboard identification string. e.g. "campaign"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}

{{< parameter p_type="CatalogAvailableAssignees" >}}
Object containing users and user groups
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# list all assignees
possible_assignees = list_available_assignees(workspace_id="demo",dashboard_id="sales")
```
