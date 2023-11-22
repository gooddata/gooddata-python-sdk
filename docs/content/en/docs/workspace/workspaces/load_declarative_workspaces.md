---
title: "load_declarative_workspaces"
linkTitle: "load_declarative_workspaces"
weight: 80
superheading: "catalog_workspace."
---



``load_declarative_workspaces(layout_root_path: Path = Path.cwd())``

Loads declarative workspaces layout, which was stored using [store_declarative_workspaces](../store_declarative_workspaces/).

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="CatalogDeclarativeWorkspaceModel" >}}
Object Containing declarative Logical Data Model and declarative Analytical Model.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Load declarative workspaces
declarative_workspaces = sdk.catalog_workspace.load_declarative_workspaces(
    layout_root_path=Path.cwd()
)
```
