---
title: "generate_logical_model"
linkTitle: "generate_logical_model"
weight: 170
superheading: "catalog_data_source."
---



``generate_logical_model(data_source_id: str, generate_ldm_request: CatalogGenerateLdmRequest)``

Generates logical data model for a data source.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string e.g. "demo"
{{< /parameter >}}

{{< parameter p_name="generate_ldm_request" p_type="Optional[CatalogGenerateLdmRequest]" >}}
LDM options. Defaults to CatalogGenerateLdmRequest(separator="__", wdf_prefix="wdf")
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="CatalogDeclarativeModel" >}}
Object Containing declarative Logical Data Model
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# Generate Logical data source
logical_model = sdk.catalog_data_source.generate_logical_model(data_source_id="demo-test-ds")
```
