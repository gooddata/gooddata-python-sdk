---
title: "put_declarative_pdm"
linkTitle: "put_declarative_pdm"
weight: 130
superheading: "catalog_data_source."
---

<!-- TODO -->

``put_declarative_pdm(data_source_id: str, declarative_tables: CatalogDeclarativeTables)``

Set physical data model for a given data source.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="data_source_id" p_type="string" >}}
Data Source identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="declarative_tables" p_type="CatalogDeclarativeTables" >}}Physical Data Model object. Can be obtained via get_declarative_pdm.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```Python
# Load declarative tables
declarative_tables = sdk.catalog_data_source.load_declarative_pdm(
    data_source_id="123",
    layout_root_path=Path.cwd()
)

# Do changes
#...

# Put declarative tables back on server
sdk.catalog_data_source.put_declarative_pdm(
    data_source_id="123",
    declarative_tables
)
```
