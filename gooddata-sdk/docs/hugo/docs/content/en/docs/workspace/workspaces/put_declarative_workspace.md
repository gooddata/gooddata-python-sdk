---
title: "put_declarative_workspace"
linkTitle: "put_declarative_workspace"
weight: 110
superheading: "catalog_workspace."
---

<!-- TODO -->

``put_declarative_workspace(workspace_id: str, workspace: CatalogDeclarativeWorkspaceModel)``

Set a workspace layout.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="workspace" p_type="CatalogDeclarativeWorkspaceModel" >}}
TODO hkad98
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```Python
# Get workspace
declarative_workspace = sdk.catalog_workspace.get_workspace(workspace_id="123")

# Do some changes
# ...

# Set the layout
sdk.catalog_workspace.put_declarative_workspace(
    workspace_id="123",
    workspace=declarative_workspace
)
```
