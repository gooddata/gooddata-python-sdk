---
title: "delete_workspace_setting"
linkTitle: "delete_workspace_setting"
weight: 230
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.delete_workspace_setting"
---



``delete_workspace_setting(workspace_id: str, workspace_setting_id: str)``

Deletes a workspace setting. Deleting a setting that does not exist does nothing.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="workspace_setting_id" p_type="string" >}}
Workspace setting identification string e.g. "locale"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_workspace.delete_workspace_setting(workspace_id="demo", workspace_setting_id="locale")
```
