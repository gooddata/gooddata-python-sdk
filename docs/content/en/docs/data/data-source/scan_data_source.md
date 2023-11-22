---
title: "scan_data_source"
linkTitle: "scan_data_source"
weight: 190
superheading: "catalog_data_source."
---

``scan_data_source(data_source_id: str, scan_request: CatalogScanModelRequest = CatalogScanModelRequest(), report_warnings: bool = False)``

Scans the data source specified by its id and optionally by specified scan request.

*CatalogScanResultPdm* contains PDM and warnings. Warnings contain information about columns which were not added to the PDM because their data types are not supported.

Additional parameter *report_warnings* can be passed to suppress or to report warnings.

By default warnings are returned but not reported to STDOUT. If you set *report_warnings* to True, warnings are reported to STDOUT.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}

{{< parameter p_name="scan_request" p_type="Optional[CatalogScanModelRequest]" >}}
Options for the Scan Request. Defaults to CatalogScanModelRequest().
{{< /parameter >}}

{{< parameter p_name="report_warnings" p_type="Optional[bool]" >}}
Switch to turn on warnings. Defaults to False.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="CatalogScanResultPdm" >}}
Physical Data Model scan result object.
{{< /parameter >}}

{{% /parameters-block %}}

## Example
```python
# Scan data source
scan_result_pdm = sdk.catalog_data_source.scan_data_source(data_source_id="demo-test-ds")
```
