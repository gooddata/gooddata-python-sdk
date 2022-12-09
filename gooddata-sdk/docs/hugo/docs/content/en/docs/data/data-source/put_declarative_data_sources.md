---
title: "put_declarative_data_sources"
linkTitle: "put_declarative_data_sources"
weight: 80
superheading: "catalog_data_source."
---

<!-- TODO -->

``put_declarative_data_sources(declarative_data_sources: CatalogDeclarativeDataSources, credentials_path: Optional[Path] = None, test_data_sources: bool = False)``

Set all data sources, including their related physical data model.

## Example

```python
#get declarative data sources.
data_sources = sdk.catalog_data_source.get_declarative_data_sources()

# Modification
data_sources.data_sources.clear()

# Put data sources back on server
sdk.catalog_data_source.put_declarative_data_sources(declarative_data_sources=data_sources)
```
