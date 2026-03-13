---
title: "staging_upload"
linkTitle: "staging_upload"
weight: 190
superheading: "catalog_data_source."
---



``staging_upload(csv_file: Path)``

Uploads a CSV file to the staging area and returns a location string that can be used in subsequent calls to analyze_csv and import_csv.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="csv_file" p_type="Path" >}}
Path to the CSV file to upload.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="string" >}}
Location string referencing the uploaded file in staging.
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
from pathlib import Path

# Upload a CSV file to staging
location = sdk.catalog_data_source.staging_upload(csv_file=Path("data.csv"))
```
