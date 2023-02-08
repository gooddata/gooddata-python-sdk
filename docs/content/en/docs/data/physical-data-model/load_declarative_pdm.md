---
title: "load_declarative_pdm"
linkTitle: "load_declarative_pdm"
weight: 150
superheading: "catalog_data_source."
---



``load_declarative_pdm(data_source_id: str, layout_root_path: Path = Path.cwd())``

Loads declarative physical data model layout, which was stored using [store_declarative_pdm](../store_declarative_pdm/) for a given data source.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```Python
# Load declarative Physical Data model
declarative_tables = sdk.catalog_data_source.load_declarative_pdm(
    data_source_id="123",
    layout_root_path=Path.cwd()
)
```
