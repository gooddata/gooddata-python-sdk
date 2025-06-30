---
title: "put_declarative_data_sources"
linkTitle: "put_declarative_data_sources"
weight: 80
superheading: "catalog_data_source."
---

{{< api-ref "sdk.CatalogDataSourceService.put_declarative_data_sources" >}}

## Example

```python
# get declarative data sources.
data_sources = sdk.catalog_data_source.get_declarative_data_sources()

# Modification
data_sources.data_sources.clear()

# Put data sources back on server
sdk.catalog_data_source.put_declarative_data_sources(declarative_data_sources=data_sources)
```
