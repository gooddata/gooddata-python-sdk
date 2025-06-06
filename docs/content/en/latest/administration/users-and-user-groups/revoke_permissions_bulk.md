---
title: "revoke_permissions_bulk"
linkTitle: "revoke_permissions_bulk"
weight: 10
no_list: true
superheading: "catalog_user."
---



``revoke_permissions_bulk(permissions_assignment: CatalogPermissionsAssignment) -> None``

Revoke permissions in bulk to users or user groups.

{{% parameters-block title="Parameters"%}}
{{< parameter p_name="permissions_assignment" p_type="CatalogPermissionsAssignment" >}}
Object containing permission assignments for workspaces and data sources to be assigned.
{{< /parameter >}}
{{% /parameters-block %}}
