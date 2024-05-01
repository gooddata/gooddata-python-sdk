---
title: "scan_schemata"
linkTitle: "scan_schemata"
weight: 210
superheading: "catalog_data_source."
---



``scan_schemata(data_source_id: str)``

Returns a list of schemas that exist in the database and can be configured in the data source entity.

Data source managers like Dremio or Drill can work with multiple schemas and schema names can be injected into scan_request to filter out tables stored in the different schemas.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="list[string]" >}}
List of schema names for the given data source specified by its id.
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# Scan schemata
sdk.catalog_data_source.scan_schemata(data_source_id="123")
# [
#   'demo',
# ...
# ]
````
