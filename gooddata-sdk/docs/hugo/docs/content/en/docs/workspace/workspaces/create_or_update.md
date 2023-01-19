---
title: "create_or_update"
linkTitle: "create_or_update"
weight: 10
superheading: "catalog_workspace."
---

``create_or_update(workspace: CatalogWorkspace)``

Creates a new workspace or overwrite an existing workspace with the same id.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace" p_type="CatalogWorkspace" >}}
Data source Object, including physical data model.
{{< /parameter >}}
{{% /parameters-block %}}
{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}
{{% parameters-block title="Raises" %}}
{{< parameter p_type="Value Error" >}}
Workspace parent can not be updated.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Create workspace
sdk.catalog_workspace.create_or_update(
    CatalogWorkspace(
        workspace_id="123",
        name="Test demo",
        parent_id="demo"
    )
)
```
