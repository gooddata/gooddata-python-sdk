---
title: "get_custom_application_setting"
linkTitle: "get_custom_application_setting"
weight: 310
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.get_custom_application_setting"
---



``get_custom_application_setting(workspace_id: str, custom_application_setting_id: str)``

Gets an individual custom application setting.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="custom_application_setting_id" p_type="string" >}}
Custom application setting identification string e.g. "my_app_version"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogCustomApplicationSetting" >}}
Custom application setting object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
setting = sdk.catalog_workspace.get_custom_application_setting(workspace_id="demo", custom_application_setting_id="my_app_version")
```
