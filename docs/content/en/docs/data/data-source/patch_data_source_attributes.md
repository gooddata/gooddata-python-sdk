---
title: "patch_data_source_attributes"
linkTitle: "patch_data_source_attributes"
weight: 40
superheading: "catalog_data_source."
---



``patch_data_source_attributes(data_source_id: str, attributes: dict)``

Applies changes to the specified data source.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string e.g. "demo"
{{< /parameter >}}

{{< parameter p_name="attributes" p_type="dictionary" >}}
A dictionary containing attributes of the data source to be changed.
{{< /parameter >}}

{{% /parameters-block %}}


{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
# Patch data source attribute(s)
sdk.catalog_data_source.patch_data_source_attributes(data_source_id="test",attributes={"name": "Name2"})
```
