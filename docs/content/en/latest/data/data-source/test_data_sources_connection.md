---
title: "test_data_sources_connection"
linkTitle: "test_data_sources_connection"
weight: 220
superheading: "catalog_data_source."
---

{{< api-ref "sdk.CatalogDataSourceService.test_data_sources_connection" >}}

## Example

```python
# Get data sources
declarative_data_sources = sdk.catalog_data_source.get_declarative_data_sources()

# Test data source connection
sdk.catalog_data_source.test_data_sources_connection(
    declarative_data_sources=declarative_data_sources,
    credentials_path=Path("credentials")
)
```
