---
title: "delete_data_source"
linkTitle: "delete_data_source"
weight: 30
superheading: "catalog_data_source."
---



``delete_data_source(data_source_id: str)``

Deletes data source using data source id.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string e.g. "demo"
{{< /parameter >}}

{{< /parameters-block >}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

### Example

```python
# Delete a data source via source id.
sdk.catalog_data_source.delete_data_source(data_source_id="123")
```
