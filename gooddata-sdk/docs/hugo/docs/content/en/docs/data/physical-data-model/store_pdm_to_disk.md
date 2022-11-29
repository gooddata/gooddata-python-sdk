---
title: "store_pdm_to_disk"
linkTitle: "store_pdm_to_disk"
weight: 140
superheading: "catalog_data_source."
---

<!-- TODO -->

``store_pdm_to_disk(data_source_id: str, path: Path = Path.cwd())``

Store the physical data model layout in the directory for a given data source.
The directory structure below shows the output for the path set to `Path("pdm_location")`.

        pdm_location
            └── pdm
                 ├── table_A.yaml
                 └── table_B.yaml

## Example

```Python
# Store Physical Data Model to disk
sdk.catalog_data_source.store_pdm_to_disk(data_source_id="123",layour_root_path=Path.cwd())
```
