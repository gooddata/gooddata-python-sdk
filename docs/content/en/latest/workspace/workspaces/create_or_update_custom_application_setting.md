---
title: "create_or_update_custom_application_setting"
linkTitle: "create_or_update_custom_application_setting"
weight: 320
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.create_or_update_custom_application_setting"
---



``create_or_update_custom_application_setting(workspace_id: str, custom_application_setting: CatalogCustomApplicationSetting)``

Creates a new custom application setting or overwrites an existing one with the same id. If the setting has no id, the server generates one.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="custom_application_setting" p_type="CatalogCustomApplicationSetting" >}}
Custom application setting object to be created or updated. `content` can be any JSON object.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="UpsertOutcome" >}}
CREATED if the setting did not exist yet, UPDATED if it did.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
from gooddata_sdk import CatalogCustomApplicationSetting

setting = CatalogCustomApplicationSetting(
    id="my_app_version",
    application_name="my_app",
    content={"version": "1.2.0"},
)
sdk.catalog_workspace.create_or_update_custom_application_setting(
    workspace_id="demo", custom_application_setting=setting
)
```
