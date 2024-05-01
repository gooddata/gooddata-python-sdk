---
title: "get_declarative_workspace_data_filters"
linkTitle: "get_declarative_workspace_data_f..."
weight: 140
superheading: "catalog_workspace."
---

``get_declarative_workspace_data_filters()``

Gets a workspace data filers layout.

{{% parameters-block  title="Parameters" None="yes"%}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeWorkspaceDataFilters" >}}
Object containing List of declarative workspace data filters.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Fetch the workspace data filters
declarative_workspace_filters = sdk.catalog_workspace.get_declarative_workspace_data_filters()
# CatalogDeclarativeWorkspaceDataFilters(
#    workspace_data_filters=[
#        CatalogDeclarativeWorkspaceDataFilter(
#            id='wdf__region',
#            title='Customer region',
#            column_name='wdf__region',
#            workspace_data_filter_settings=[
#                CatalogDeclarativeWorkspaceDataFilterSetting(
#                    id='region_west',
#                    title='Region West',
#                    filter_values=['West'],
#                    workspace=CatalogWorkspaceIdentifier(id='demo_west'),
#                    description=None
#                )
#            ],
#            description=None,
#            workspace=CatalogWorkspaceIdentifier(id='demo')
#        ),
#        CatalogDeclarativeWorkspaceDataFilter(
#            id='wdf__state',
#            title='Customer state',
#            column_name='wdf__state',
#            workspace_data_filter_settings=[
#                CatalogDeclarativeWorkspaceDataFilterSetting(
#                    id='region_west_california',
#                    title='Region West California',
#                    filter_values=['California'],
#                    workspace=CatalogWorkspaceIdentifier(
#                        id='demo_west_california'
#                    ),
#                    description=None
#                )
#            ],
#            description=None,
#            workspace=CatalogWorkspaceIdentifier(id='demo_west')
#        )
#    ]
# )
```
