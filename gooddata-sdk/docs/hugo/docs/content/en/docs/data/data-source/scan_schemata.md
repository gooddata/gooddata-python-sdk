---
title: "scan_schemata"
linkTitle: "scan_schemata"
weight: 210
superheading: "catalog_data_source."
---

<!-- TODO -->

``scan_schemata(data_source_id: str)``

Returns *list[str]*.

Returns a list of schemas that exist in the database and can be configured in the data source entity. Data source managers like Dremio or Drill can work with multiple schemas and schema names can be injected into scan_request to filter out tables stored in the different schemas.

## Example

```Python
# Scan schemata
sdk.catalog_data_source.scan_schemata(data_source_id="123")
#[
#   'demo',
# ...
# ]
````
