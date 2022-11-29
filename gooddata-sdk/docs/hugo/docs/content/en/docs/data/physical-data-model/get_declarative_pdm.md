---
title: "get_declarative_pdm"
linkTitle: "get_declarative_pdm"
weight: 120
superheading: "catalog_data_source."
---

<!-- TODO -->

``get_declarative_pdm(data_source_id: str)``

Returns *CatalogDeclarativeTables*.

Retrieve physical data model for a given data source.

## Example

```Python
# Get Physical Data Model in declarative form
declarative_tables = sdk.catalog_data_source.get_declarative_pdm(data_source_id="123")
```
