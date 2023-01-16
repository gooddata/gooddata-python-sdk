---
title: "get_declarative_permissions"
linkTitle: "get_declarative_permissions"
weight: 10
no_list: true
superheading: "catalog_permission."
---

<!-- TODO -->

``get_declarative_permissions(workspace_id: str)``

Retrieve current set of permissions of the workspace in a declarative form.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string. e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="CatalogDeclarativeWorkspacePermissions" >}}
TODO hkad98
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get permissions in declarative from
declarative_permissions = sdk.catalog_permission.get_declarative_permissions(workspace_id=workspace_id)
```
