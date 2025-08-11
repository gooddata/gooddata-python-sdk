---
title: "put_declarative_workspace_data_filters"
linkTitle: "put_declarative_workspace_data_f..."
weight: 150
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.put_declarative_workspace_data_filters" >}}

## Example

```python
# Fetch the workspace data filters
declarative_workspace_filters = sdk.catalog_workspace.get_declarative_workspace_data_filters()

# Do changes
# ...

# Put the filters back on server
sdk.catalog_workspace.put_declarative_workspace_data_filters(
    workspace_data_filters= declarative_workspace_filters
)
```
