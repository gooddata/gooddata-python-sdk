---
title: "store_declarative_data_sources"
linkTitle: "store_declarative_data_sources"
weight: 90
superheading: "catalog_data_source."
---

<!-- TODO -->

``store_declarative_data_sources(layout_root_path: Path = Path.cwd())``

Store data sources layouts in directory hierarchy.

    gooddata_layouts
    └── organization_id
            └── data_sources
                    ├── data_source_a
                    │       ├── pdm
                    │       │   ├── table_A.yaml
                    │       │   └── table_B.yaml
                    │       └── data_source_a.yaml
                    └── data_source_b
                            └── pdm
                            │   ├── table_X.yaml
                            │   └── table_Y.yaml
                            └── data_source_b.yaml

## Example

```python
# Store declarative data sources
sdk.catalog_data_source.store_declarative_data_sources(layout_root_path: Path = Path.cwd())
```
