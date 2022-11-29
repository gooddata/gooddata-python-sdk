---
title: "load_declarative_data_sources"
linkTitle: "load_declarative_data_sources"
weight: 100
superheading: "catalog_data_source."
---

<!-- TODO -->

``load_declarative_data_sources(layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeDataSources*.

Load declarative data sources layout, which was stored using [store_declarative_data_sources](../store_declarative_data_sources).

## Example

```python
# Get Declarative data sources
declarative_data_sources = sdk.catalog_data_source.get_declarative_data_sources()
```
