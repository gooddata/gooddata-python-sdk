---
title: "load_and_put_declarative_pdm"
linkTitle: "load_and_put_declarative_pdm"
weight: 160
superheading: "catalog_data_source."
---



``load_and_put_declarative_pdm(data_source_id: str, layout_root_path: Path = Path.cwd())``

This method combines [load_declarative_pdm](../load_declarative_pdm) and [put_declarative_pdm](../put_declarative_pdm) methods to load and set layouts stored using [store_declarative_pdm](../store_declarative_pdm).

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

The load and put can be done two ways.

Either by one call:


```python
# Load and put data sources in one method
sdk.catalog_user.load_and_put_declarative_pdm(
    data_source_id="123",
    layout_root_path = Path.cwd()
)
```
Or by two separate calls:

```python
# Load declarative Physical Data model
declarative_tables = sdk.catalog_data_source.load_declarative_pdm(
    data_source_id="123",
    layout_root_path=Path.cwd()
)
# Put declarative tables back on server
sdk.catalog_data_source.put_declarative_pdm(
    data_source_id="123",
    declarative_tables
)
```

The result is identical.
