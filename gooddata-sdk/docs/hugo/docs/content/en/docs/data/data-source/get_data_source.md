---
title: "get_data_source"
linkTitle: "get_data_source"
weight: 20
superheading: "catalog_data_source."
---



``get_data_source(data_source_id: str)``

Gets data source using data source id.


{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="str" >}}
Data source identification string e.g. "demo"
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="CatalogDataSource" >}}
Data source object.
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# Get a data source via source id.
data_source = sdk.catalog_data_source.get_data_source(data_source_id="123")
```
