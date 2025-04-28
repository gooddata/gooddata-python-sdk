---
title: "put_declarative_organization_permissions"
linkTitle: "put_declarative_organization_permissions"
weight: 20
no_list: true
superheading: "catalog_permission."
---

{{< api-ref "sdk.CatalogPermissionService.put_declarative_organization_permissions" >}}

## Example

```python
declarative_org_permissions = [CatalogDeclarativeOrganizationPermission(name="MANAGE", assignee=CatalogAssigneeIdentifier(id="user1", type="user"))]

# Update permissions on the server with your changes
sdk.catalog_permission.put_declarative_organization_permissions(org_permissions=declarative_org_permissions)
```
