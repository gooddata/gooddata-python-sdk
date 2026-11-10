---
title: "delete_custom_application_setting"
linkTitle: "delete_custom_application_setting"
weight: 330
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.delete_custom_application_setting"
---



``delete_custom_application_setting(workspace_id: str, custom_application_setting_id: str)``

Deletes a custom application setting. Deleting a setting that does not exist does nothing.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="custom_application_setting_id" p_type="string" >}}
Custom application setting identification string e.g. "my_app_version"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_workspace.delete_custom_application_setting(workspace_id="demo", custom_application_setting_id="my_app_version")
```
