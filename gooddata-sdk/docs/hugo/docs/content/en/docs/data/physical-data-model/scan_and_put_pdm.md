---
title: "scan_and_put_pdm"
linkTitle: "scan_and_put_pdm"
weight: 200
superheading: "catalog_data_source."
---

<!-- TODO -->

``scan_and_put_pdm(data_source_id: str, scan_request: CatalogScanModelRequest = CatalogScanModelRequest())``

This method combines [scan_data_source](../../data-source/scan_data_source) and [put_declarative_pdm](../put_declarative_pdm) methods.

## Example

```Python
# scand and put Physical Data Model to server
sdk.catalog_data_source.scan_and_put_pdm(data_source_id="demo-test-ds")
```
