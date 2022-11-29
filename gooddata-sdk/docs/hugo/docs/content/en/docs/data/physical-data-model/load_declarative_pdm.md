---
title: "load_declarative_pdm"
linkTitle: "load_declarative_pdm"
weight: 150
superheading: "catalog_data_source."
---

<!-- TODO -->

``load_declarative_pdm(data_source_id: str, layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeTables*.

Load declarative physical data model layout, which was stored using [store_declarative_pdm](../store_declarative_pdm) for a given data source.

## Example

```Python
# Load declarative Physical Data model
declarative_tables = sdk.catalog_data_source.load_declarative_pdm(
    data_source_id="123",
    layout_root_path=Path.cwd()
)
```
