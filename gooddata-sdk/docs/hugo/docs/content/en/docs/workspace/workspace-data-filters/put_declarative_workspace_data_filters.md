---
title: "put_declarative_workspace_data_filters"
linkTitle: "put_declarative_workspace_data_f..."
weight: 150
superheading: "catalog_workspace."
---

<!-- TODO -->

``put_declarative_workspace_data_filters(workspace_data_filters: CatalogDeclarativeWorkspaceDataFilters)``

Set a workspace data filter layout.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_data_filters" p_type="CatalogDeclarativeWorkspaceDataFilters" >}}
TODO hkad98
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```Python
# Fetch the workspace data filters
declarative_workspace_filters = sdk.catalog_workspace.get_declarative_workspace_data_filters()

# Do changes
#....

# Put the filters back on server
sdk.catalog_workspace.put_declarative_workspace_data_filters(
    workspace_data_filters= declarative_workspace_filters
)
```
