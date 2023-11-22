---
title: "load_declarative_workspace"
linkTitle: "load_declarative_workspace"
weight: 120
superheading: "catalog_workspace."
---



``load_declarative_workspace(workspace_id: str, layout_root_path: Path = Path.cwd())``

Loads declarative workspaces layout, which was stored using [store_declarative_workspace](../store_declarative_workspace/).

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
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
# Load a declarative workspace
declarative_workspace = sdk.catalog_workspace.load_declarative_workspace(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
