---
title: "load_and_put_declarative_pdm"
linkTitle: "load_and_put_declarative_pdm"
weight: 160
superheading: "catalog_data_source."
---

<!-- TODO -->

``load_and_put_declarative_pdm(data_source_id: str, layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_pdm](../load_declarative_pdm) and [put_declarative_pdm](../put_declarative_pdm) methods to load and set layouts stored using [store_declarative_pdm](../store_declarative_pdm).

## Example

The load and put can be done two ways.

Either by one call:


```python
#Load and put data sources in one method
sdk.catalog_user.load_and_put_declarative_pdm(
    data_source_id="123",
    layout_root_path = Path.cwd()
)
```
Or by two separate calls:

```python
# Load declarative Physical Data model
declarative_tables = sdk.catalog_data_source.load_declarative_pdm(
    data_source_id="123",
    layout_root_path=Path.cwd()
)
# Put declarative tables back on server
sdk.catalog_data_source.put_declarative_pdm(
    data_source_id="123",
    declarative_tables
)
```

The result is identical.
