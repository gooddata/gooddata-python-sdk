---
title: "list_data_source_tables"
linkTitle: "list_data_source_tables"
weight: 60
superheading: "catalog_data_source."
---

<!-- TODO -->

``list_data_source_tables(data_source_id: str)``

Returns *List[CatalogDataSourceTable]*

Lists all tables for a data source specified by id.

## Example

```Python
# List data source tables
source_tables = sdk.catalog_data_source.list_data_source_tables(data_source_id="123")


#[
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
#]
```
