---
title: "delete_workspace"
linkTitle: "delete_workspace"
weight: 30
superheading: "catalog_workspace."
---



``delete_workspace(workspace_id: str)``

Deletes a workspace with all its content - logical model and analytics model.

This method is implemented according to our implementation of delete workspace, which returns HTTP 204 no matter if the workspace_id exists.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Raises" %}}
{{< parameter p_type="Value Error" >}}
Workspace does not exist.
{{< /parameter >}}
{{< parameter p_type="Value Error" >}}
Workspace is a parent of a workspace.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Delete workspace
sdk.catalog_workspace.delete_workspace(workspace_id="test_demo")
```
