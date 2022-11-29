---
title: "store_declarative_pdm"
linkTitle: "store_declarative_pdm"
weight: 139
superheading: "catalog_data_source."
---

<!-- TODO -->

``store_declarative_pdm(data_source_id: str, layout_root_path: Path = Path.cwd())``

Store physical data model layout in directory hierarchy for a given data source.

    gooddata_layouts
    └── organization_id
            └── data_sources
                    └── data_source_a
                            └── pdm
                                ├── table_A.yaml
                                └── table_B.yaml

## Example

```Python
# Store declarative PDM in directory hierarchy
sdk.catalog_data_source.store_declarative_pdm(data_source_id="123",layour_root_path=Path.cwd())
```
