---
title: "get_declarative_organization_permissions"
linkTitle: "get_declarative_organization_permissions"
weight: 10
no_list: true
superheading: "catalog_permission."
---



``get_declarative_organization_permissions()``

Gets the current set of permissions of the workspace in a declarative form.

{{% parameters-block  title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="List[CatalogDeclarativeOrganizationPermission]" >}}
List of Objects Containing Organization Permissions.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get organization permissions in declarative from
declarative_permissions = sdk.catalog_permission.get_declarative_organization_permissions()
```
