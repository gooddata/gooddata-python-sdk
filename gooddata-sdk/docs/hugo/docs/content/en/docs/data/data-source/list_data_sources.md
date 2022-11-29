---
title: "list_data_sources"
linkTitle: "list_data_sources"
weight: 50
superheading: "catalog_data_source."
---

<!-- TODO -->

``list_data_sources()``

Returns *List[CatalogDataSource]*.

Lists all data sources.

```Python
# List all data sources
data_sources = sdk.catalog_data_sources.list_data_sources()


#[
#    CatalogDataSource(
#        id='demo-test-ds',
#        name='demo-test-ds',
#        type='POSTGRESQL',
#        schema='demo',
#        url='jdbc:postgresql://localhost:5432/demo',
#        enable_caching=False,
#        cache_path=None,
#        parameters=None,
#        decoded_parameters=None,
#        db_vendor='postgresql',
#        db_specific_attributes=None,
#        url_params=None
#    ),
#...
#]
```
