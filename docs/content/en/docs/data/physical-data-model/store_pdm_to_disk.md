---
title: "store_pdm_to_disk"
linkTitle: "store_pdm_to_disk"
weight: 140
superheading: "catalog_data_source."
---



``store_pdm_to_disk(data_source_id: str, path: Path = Path.cwd())``

Stores the physical data model layout in the directory for a given data source.
The directory structure below shows the output for the path set to `Path("pdm_location")`.

        pdm_location
            └── pdm
                 ├── table_A.yaml
                 └── table_B.yaml

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
# Store Physical Data Model to disk
sdk.catalog_data_source.store_pdm_to_disk(data_source_id="123",layour_root_path=Path.cwd())
```
