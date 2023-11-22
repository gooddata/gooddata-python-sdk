---
title: "store_declarative_workspace_data_filters"
linkTitle: "store_declarative_workspace_dat..."
weight: 160
superheading: "catalog_workspace."
---



``store_declarative_workspace_data_filters(layout_root_path: Path = Path.cwd())``

Stores workspace data filters in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── workspaces_data_filters
                    ├── filter_1.yaml
                    └── filter_2.yaml

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}


## Example

```python
# Store the workspace filters
sdk.catalog_workspace.store_declarative_workspace_data_filters(layout_root_path=Path.cwd())
```
