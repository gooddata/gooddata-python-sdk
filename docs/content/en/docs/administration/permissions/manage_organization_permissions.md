---
title: "manage_organization_permissions"
linkTitle: "manage_organization_permissions"
weight: 20
no_list: true
superheading: "catalog_permission."
---



``manage_organization_permissions(organization_permission_assignments: List[CatalogOrganizationPermissionAssignment])``

Manage the permissions of the whole organization.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="organization_permission_assignments" p_type="List[CatalogOrganizationPermissionAssignment]" >}}
List of Organization Permission Assignments.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Update permissions on the server with your changes
sdk.catalog_permission.manage_organization_permissions(organization_permission_assignments=org_permissions_assignments)
```
