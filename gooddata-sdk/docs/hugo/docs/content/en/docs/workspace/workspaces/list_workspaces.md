---
title: "list_workspaces"
linkTitle: "list_workspaces"
weight: 40
superheading: "catalog_workspace."
---



``list_workspaces()``

Gets a list of all existing workspaces.

{{% parameters-block title="Parameters" None="yes"%}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="List[CatalogWorkspace]" >}}
List of workspaces in the current organization.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# List workspaces
workspaces = sdk.catalog_workspace.list_workspaces()

print(workspaces)
# [
#   CatalogWorkspace(id=demo, name=Demo),
#   CatalogWorkspace(id=demo_west, name=Demo West),
#   CatalogWorkspace(id=demo_west_california, name=Demo West California)
# ]
```
