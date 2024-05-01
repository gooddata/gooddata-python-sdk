---
title: "load_and_put_declarative_workspace"
linkTitle: "load_and_put_declarative_work..."
weight: 130
superheading: "catalog_workspace."
---



``load_and_put_declarative_workspace(workspace_id: str, layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_workspace](../load_declarative_workspace/) and [put_declarative_workspace](../put_declarative_workspace/) methods to load and
set layouts stored using [store_declarative_workspace](../store_declarative_workspace/).

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put on server the stored layout
sdk.catalog_workspace.load_and_put_declarative_workspace(
    workspace_id="demo",
    layout_root_path=Path.cwd()
)
```

Or by two separate calls:

```python
# Load a declarative workspace
declarative_workspaces = sdk.catalog_workspace.load_declarative_workspace(
    workspace_id="demo",
    layout_root_path=Path.cwd()
)
# Set the layout
sdk.catalog_workspace.put_declarative_workspace(
    workspace_id="demo",
    workspace=declarative_workspaces
)
```

The result is identical.
