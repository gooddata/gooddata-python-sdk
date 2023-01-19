---
title: "get_workspace"
linkTitle: "get_workspace"
weight: 20
superheading: "catalog_workspace."
---



``get_workspace(workspace_id: str)``

Gets an individual workspace.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogWorkspace" >}}
Catalog workspace object containing structure of the workspace.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get workspace
workspace = sdk.catalog_workspace.get_workspace(workspace_id="123")
```
