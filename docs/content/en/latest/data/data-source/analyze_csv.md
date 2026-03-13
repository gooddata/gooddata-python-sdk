---
title: "analyze_csv"
linkTitle: "analyze_csv"
weight: 191
superheading: "catalog_data_source."
---



``analyze_csv(location: str)``

Analyzes an uploaded CSV file in the staging area. Returns column metadata, detected types, preview data, and a config object that can be passed to import_csv.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="location" p_type="string" >}}
Location string returned by staging_upload.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="AnalyzeCsvResponse" >}}
Analysis result with columns, preview data, and config.
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# Analyze a previously uploaded CSV file
analysis = sdk.catalog_data_source.analyze_csv(location="staging/some-location")
for col in analysis["columns"]:
    print(f"{col['name']}: {col['type']}")
```
