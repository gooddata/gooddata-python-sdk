---
title: "generate_logical_model"
linkTitle: "generate_logical_model"
weight: 170
superheading: "catalog_data_source."
---

<!-- TODO -->

``generate_logical_model(data_source_id: str, generate_ldm_request: CatalogGenerateLdmRequest)``

Returns *CatalogDeclarativeModel*.

Generate logical data model for a data source.

## Example

```Python
# Generate Logical data source
logical_model = sdk.catalog_data_source.generate_logical_model(data_source_id="demo-test-ds")
```
