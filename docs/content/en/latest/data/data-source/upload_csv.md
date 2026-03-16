---
title: "upload_csv"
linkTitle: "upload_csv"
weight: 194
superheading: "catalog_data_source."
api_ref: "CatalogDataSourceService.upload_csv"
---



``upload_csv(data_source_id: str, csv_file: Path, table_name: str)``

Convenience method that uploads a CSV file and imports it into a GDSTORAGE data source in a single call. Orchestrates the full flow: staging_upload → analyze_csv → import_csv → register_upload_notification.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string for a GDSTORAGE data source.
{{< /parameter >}}

{{< parameter p_name="csv_file" p_type="Path" >}}
Path to the CSV file to upload.
{{< /parameter >}}

{{< parameter p_name="table_name" p_type="string" >}}
Name for the table to create or replace in the data source.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
from pathlib import Path

# Upload a CSV file end-to-end in a single call
sdk.catalog_data_source.upload_csv(
    data_source_id="my-gdstorage-ds",
    csv_file=Path("data.csv"),
    table_name="my_table",
)
```
