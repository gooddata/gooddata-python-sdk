---
title: "create_or_update_workspace_setting"
linkTitle: "create_or_update_workspace_setting"
weight: 220
superheading: "catalog_workspace."
api_ref: "CatalogWorkspaceService.create_or_update_workspace_setting"
---



``create_or_update_workspace_setting(workspace_id: str, workspace_setting: CatalogWorkspaceSetting)``

Creates a new workspace setting or overwrites an existing workspace setting with the same id.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="workspace_setting" p_type="CatalogWorkspaceSetting" >}}
Workspace setting object to be created or updated.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="UpsertOutcome" >}}
CREATED if the setting did not exist yet, UPDATED if it did.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
from gooddata_sdk import CatalogWorkspaceSetting

setting = CatalogWorkspaceSetting(id="locale", setting_type="LOCALE", content={"value": "fr-FR"})
sdk.catalog_workspace.create_or_update_workspace_setting(workspace_id="demo", workspace_setting=setting)
```
