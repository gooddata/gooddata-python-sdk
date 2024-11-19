---
title: "get_declarative_workspace_data_filters"
linkTitle: "get_declarative_workspace_data_f..."
weight: 140
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.get_declarative_workspace_data_filters" >}}

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
