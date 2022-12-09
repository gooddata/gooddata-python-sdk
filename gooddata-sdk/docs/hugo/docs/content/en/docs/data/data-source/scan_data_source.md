---
title: "scan_data_source"
linkTitle: "scan_data_source"
weight: 190
superheading: "catalog_data_source."
---

``scan_data_source(data_source_id: str, scan_request: CatalogScanModelRequest = CatalogScanModelRequest(), report_warnings: bool = False)``

Returns *CatalogScanResultPdm*.

Scan data source specified by its id and optionally by specified scan request. *CatalogScanResultPdm* contains PDM and warnings. Warnings contain information about columns which were not added to the PDM because their data types are not supported. Additional parameter *report_warnings* can be passed to suppress or to report warnings. By default warnings are returned but not reported to STDOUT. If you set *report_warnings* to True, warnings are reported to STDOUT.

## Example
```Python
# Scan data source
scan_result_pdm = sdk.catalog_data_source.scan_data_source(data_source_id="demo-test-ds")
```
