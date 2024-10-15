---
title: "list_data_sources"
linkTitle: "list_data_sources"
weight: 50
superheading: "catalog_data_source."
---



``list_data_sources()``

Lists all data sources.


{{% parameters-block title="Parameters" None="yes"%}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{% parameter p_type="List[CatalogDataSource]" %}}
List of all data sources in the whole organization.
{{% /parameter %}}

{{% /parameters-block %}}

```python
# List all data sources
data_sources = sdk.catalog_data_source.list_data_sources()


# [
#    CatalogDataSource(
#        id='demo-test-ds',
#        name='demo-test-ds',
#        type='POSTGRESQL',
#        schema='demo',
#        url='jdbc:postgresql://localhost:5432/demo',
#        cache_path=None,
#        parameters=None,
#        decoded_parameters=None,
#        db_vendor='postgresql',
#        db_specific_attributes=None,
#        url_params=None
#    ),
# ...
# ]
```
