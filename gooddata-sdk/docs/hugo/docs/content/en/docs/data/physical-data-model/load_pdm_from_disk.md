---
title: "load_pdm_from_disk"
linkTitle: "load_pdm_from_disk"
weight: 140
superheading: "catalog_data_source."
---

``load_pdm_from_disk(path: Path = Path.cwd())``

This method is used to load pdm stored to disk using method `store_pdm_to_disk`.

## Example

```Python
# Load Physical Data Model from disk
sdk.catalog_data_source.load_pdm_from_disk(path=Path("xyz"))
```
