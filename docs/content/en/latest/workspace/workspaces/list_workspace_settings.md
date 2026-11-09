---
title: "list_workspace_settings"
linkTitle: "list_workspace_settings"
weight: 200
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.list_workspace_settings"
---



``list_workspace_settings(workspace_id: str)``

Lists all settings of a workspace.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="list[CatalogWorkspaceSetting]" >}}
List of workspace settings.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
settings = sdk.catalog_workspace.list_workspace_settings(workspace_id="demo")
```
