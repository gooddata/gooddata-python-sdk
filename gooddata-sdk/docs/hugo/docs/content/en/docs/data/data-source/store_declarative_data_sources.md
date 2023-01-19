---
title: "store_declarative_data_sources"
linkTitle: "store_declarative_data_sources"
weight: 90
superheading: "catalog_data_source."
---

``store_declarative_data_sources(layout_root_path: Path = Path.cwd())``

Stores the data sources layouts in a directory hierarchy.

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

{{% parameters-block title="Parameters"%}}
{{< parameter p_name="layout_root_path" p_type="Path" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Store declarative data sources
sdk.catalog_data_source.store_declarative_data_sources(layout_root_path: Path = Path.cwd())
```
