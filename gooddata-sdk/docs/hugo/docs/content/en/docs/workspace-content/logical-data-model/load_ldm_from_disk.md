---
title: "load_ldm_from_disk"
linkTitle: "load_ldm_from_disk"
weight: 101
superheading: "catalog_workspace_content."
---

``load_ldm_from_disk( path: Path = Path.cwd())``

Returns *CatalogDeclarativeModel*.

The method is used to load ldm stored to disk using method `store_ldm_to_disk`.

## Example

```Python
# Retrieve the stored Logical Data model
logical_model = sdk.catalog_workspace_content.load_ldm_from_disk(path=Path.cwd())
```
