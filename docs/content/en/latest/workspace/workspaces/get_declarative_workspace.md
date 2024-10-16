---
title: "get_declarative_workspace"
linkTitle: "get_declarative_workspace"
weight: 100
superheading: "catalog_workspace."
---


``get_declarative_workspace(workspace_id: str, exclude: Optional[list[str]])``

Get all workspaces in the current organization in a declarative form.
This method combines
`sdk.catalog_workspace_content.get_declarative_ldm` and `sdk.catalog_workspace_content.get_declarative_analytics_model`
methods and returns a declarative workspace object.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="exclude" p_type="Optional[list[str]]" >}}
Defines properties which should not be included in the payload.
E.g.: ["ACTIVITY_INFO"]
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeWorkspaces" >}}
Declarative Workspaces object including all the workspaces for given organization.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get declarative workspace
declarative_workspace = sdk.catalog_workspace.get_declarative_workspace(workspace_id="123")
```
