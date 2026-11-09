---
title: "list_custom_application_settings"
linkTitle: "list_custom_application_settings"
weight: 300
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.list_custom_application_settings"
---



``list_custom_application_settings(workspace_id: str)``

Lists the settings of all custom applications in a workspace.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="list[CatalogCustomApplicationSetting]" >}}
List of custom application settings.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
settings = sdk.catalog_workspace.list_custom_application_settings(workspace_id="demo")

# Keep only the settings of one application
my_app_settings = [s for s in settings if s.application_name == "my_app"]
```
