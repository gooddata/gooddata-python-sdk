---
title: "scan_pdm_and_generate_logical_model"
linkTitle: "scan_pdm_and_generate_logical_model"
weight: 190
superheading: "catalog_data_source."
---

``scan_pdm_and_generate_logical_model(data_source_id: str, generate_ldm_request: Optional[CatalogGenerateLdmRequest] = None, scan_request: CatalogScanModelRequest = CatalogScanModelRequest(), report_warnings: bool = False) -> tuple[CatalogDeclarativeModel, CatalogScanResultPdm]``

Scan data source and use returned PDM to generate logical data model. If generate_ldm_request
contains PDM already, PDM tables received from the scan are appended without deduplication.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data Source identification string. e.g. "demo"
{{< /parameter >}}

{{< parameter p_name="generate_ldm_request" p_type="Optional[CatalogGenerateLdmRequest]" >}}
LDM options. Defaults to CatalogGenerateLdmRequest(separator="__", wdf_prefix="wdf")
{{< /parameter >}}

{{< parameter p_name="scan_request" p_type="Optional[CatalogScanModelRequest]" >}}
Options for the Scan Request. Defaults to CatalogScanModelRequest().
{{< /parameter >}}

{{< parameter p_name="report_warnings" p_type="bool" >}}
Switch to turn on warnings. Defaults to False.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="CatalogDeclarativeModel" >}}
Object Containing declarative Logical Data Model.
{{< /parameter >}}

{{< parameter p_type="CatalogScanResultPdm" >}}
An instance of CatalogScanResultPdm.
Containing pdm itself and a list of warnings that occurred during scanning.
{{< /parameter >}}

{{% /parameters-block %}}

## Example

```python
# Scan and generate logical model
ldm, pdm = sdk.catalog_data_source.scan_pdm_and_generate_logical_model(data_source_id="demo-test-ds")
```
