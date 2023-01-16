---
title: "get_declarative_workspace"
linkTitle: "get_declarative_workspace"
weight: 100
superheading: "catalog_workspace."
---

<!-- TODO -->

``get_declarative_workspace(workspace_id: str)``

Get all workspaces in the current organization in a declarative form.

{{% parameters-block title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeWorkspaces" >}}
Declarative Workspaces object including all the workspaces for given organization.
{{< /parameter >}}
{{% /parameters-block %}}


## Example

```python
#Retrieve declarative workspace
declarative_workspace = sdk.catalog_workspace.get_declarative_workspace(workspace_id="123")
```
