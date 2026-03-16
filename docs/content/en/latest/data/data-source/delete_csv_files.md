---
title: "delete_csv_files"
linkTitle: "delete_csv_files"
weight: 193
superheading: "catalog_data_source."
api_ref: "CatalogDataSourceService.delete_csv_files"
---



``delete_csv_files(data_source_id: str, file_names: list[str])``

Deletes files from a GDSTORAGE data source.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string.
{{< /parameter >}}

{{< parameter p_name="file_names" p_type="list[string]" >}}
List of file names to delete.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
# Delete specific files from a GDSTORAGE data source
sdk.catalog_data_source.delete_csv_files(
    data_source_id="my-gdstorage-ds",
    file_names=["my_table.csv"],
)
```
