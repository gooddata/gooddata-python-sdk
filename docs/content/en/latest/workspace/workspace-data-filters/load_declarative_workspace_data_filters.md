---
title: "load_declarative_workspace_data_filters"
linkTitle: "load_declarative_workspace_data_..."
weight: 170
superheading: "catalog_workspace."
---



``load_declarative_workspace_data_filters(layout_root_path: Path = Path.cwd())``

Loads the declarative workspaces layout, which was stored using [store_declarative_workspace_data_filters](../store_declarative_workspace_data_filters/).

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeWorkspaceDataFilters" >}}
Object containing List of declarative workspace data filters.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Load the workspace data filters
declarative_workspace_filters = sdk.catalog_workspace.load_declarative_workspace_data_filters(
    layout_root_path=Path.cwd()
)
```
