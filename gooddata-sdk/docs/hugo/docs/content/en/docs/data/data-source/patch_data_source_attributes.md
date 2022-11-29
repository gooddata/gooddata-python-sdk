---
title: "patch_data_source_attributes"
linkTitle: "patch_data_source_attributes"
weight: 40
superheading: "catalog_data_source."
---

<!-- TODO -->

``patch_data_source_attributes(data_source_id: str, attributes: dict)``

Allows you to apply changes to the given data source.

## Example

```Python
# Patch data source attribute(s)
sdk.catalog_data_source.patch_data_source_attributes(data_source_id="test",attributes={"name": "Name2"})
```
