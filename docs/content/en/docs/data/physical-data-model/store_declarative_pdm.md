---
title: "store_declarative_pdm"
linkTitle: "store_declarative_pdm"
weight: 139
superheading: "catalog_data_source."
---



``store_declarative_pdm(data_source_id: str, layout_root_path: Path = Path.cwd())``

Stores the physical data model layout in directory hierarchy for a given data source.

    gooddata_layouts
    └── organization_id
            └── data_sources
                    └── data_source_a
                            └── pdm
                                ├── table_A.yaml
                                └── table_B.yaml


{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```Python
# Store declarative PDM in directory hierarchy
sdk.catalog_data_source.store_declarative_pdm(data_source_id="123",layour_root_path=Path.cwd())
```
