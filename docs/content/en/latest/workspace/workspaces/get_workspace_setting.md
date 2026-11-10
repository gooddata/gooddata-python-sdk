---
title: "get_workspace_setting"
linkTitle: "get_workspace_setting"
weight: 210
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.get_workspace_setting"
---



``get_workspace_setting(workspace_id: str, workspace_setting_id: str)``

Gets an individual workspace setting.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="workspace_setting_id" p_type="string" >}}
Workspace setting identification string e.g. "locale"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogWorkspaceSetting" >}}
Workspace setting object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
setting = sdk.catalog_workspace.get_workspace_setting(workspace_id="demo", workspace_setting_id="locale")
```
