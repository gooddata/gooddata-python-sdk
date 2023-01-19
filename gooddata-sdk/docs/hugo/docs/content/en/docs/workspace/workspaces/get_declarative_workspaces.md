---
title: "get_declarative_workspaces"
linkTitle: "get_declarative_workspaces"
weight: 50
superheading: "catalog_workspace."
---

``get_declarative_workspaces()``

Gets the layout of all workspaces and their hierarchy.

{{% parameters-block title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeWorkspaces" >}}
Declarative Workspaces object including all the workspaces for given organization.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get declarative workspace
declarative_workspaces = sdk.catalog_workspace.get_declarative_workspaces()
```
