---
title: "import_csv"
linkTitle: "import_csv"
weight: 192
superheading: "catalog_data_source."
---



``import_csv(data_source_id: str, table_name: str, location: str, config: Optional[dict] = None)``

Imports a CSV file from the staging area into a GDSTORAGE data source.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string.
{{< /parameter >}}

{{< parameter p_name="table_name" p_type="string" >}}
Name for the table to create or replace.
{{< /parameter >}}

{{< parameter p_name="location" p_type="string" >}}
Location string returned by staging_upload.
{{< /parameter >}}

{{< parameter p_name="config" p_type="Optional[dict]" >}}
Source config dict, typically from analyze_csv response. Optional.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
# Import a CSV into a GDSTORAGE data source using config from analysis
analysis = sdk.catalog_data_source.analyze_csv(location=location)
config = analysis.to_dict().get("config")
sdk.catalog_data_source.import_csv(
    data_source_id="my-gdstorage-ds",
    table_name="my_table",
    location=location,
    config=config,
)
```
