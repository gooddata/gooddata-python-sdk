---
title: "list_data_source_tables"
linkTitle: "list_data_source_tables"
weight: 60
superheading: "catalog_data_source."
---



``list_data_source_tables(data_source_id: str)``

Lists all the data source tables for a given data source.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string e.g. "demo"
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="List[CatalogDataSourceTable]" >}}
List of data source table objects
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# List data source tables
source_tables = sdk.catalog_data_source.list_data_source_tables(data_source_id="123")


# [
#    CatalogDataSourceTable(
#        id='campaign_channels',
#        type='dataSourceTable',
#        attributes=CatalogDataSourceTableAttributes(
#            columns=[
#                CatalogDataSourceTableColumn(
#                    name='budget',
#                    data_type='NUMERIC',
#                    is_primary_key=False,
#                    referenced_table_column=None,
#                    referenced_table_id=None
#                ),
#                CatalogDataSourceTableColumn(
#                    name='campaign_channel_id',
#                    data_type='STRING',
#                    is_primary_key=True,
#                    referenced_table_column=None,
#                    referenced_table_id=None
#                ),
#                CatalogDataSourceTableColumn(
#                    name='campaign_id',
#                    data_type='INT',
#                    is_primary_key=False,
#                    referenced_table_column='campaign_id',
#                    referenced_table_id='campaigns'
#                ),
#                CatalogDataSourceTableColumn(
#                    name='category',
#                    data_type='STRING',
#                    is_primary_key=False,
#                    referenced_table_column=None,
#                    referenced_table_id=None
#                ),
#                ...
#            ],
#            name_prefix=None,
#            path=[
#                'demo',
#                'campaign_channels'
#            ],
#            type='TABLE'
#        )
#    ),
#    ...
# ]
```
