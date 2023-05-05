---
title: "put_declarative_workspaces"
linkTitle: "put_declarative_workspaces"
weight: 60
superheading: "catalog_workspace."
---

``put_declarative_workspaces(workspace: CatalogDeclarativeWorkspaces)``

Sets the layout of all workspaces and their hierarchy.

{{% parameters-block title="Parameters" %}}
{{< parameter p_type="CatalogDeclarativeWorkspaces" p_name="workspace" >}}
Declarative Workspaces object including all the workspaces for given organization.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Load declarative workspaces
declarative_workspaces = sdk.catalog_workspace.get_declarative_workspaces()

# Do changes
# ...

# Set the layout and hierachy
sdk.catalog_workspace.put_declarative_workspaces(declarative_workspaces)
```
