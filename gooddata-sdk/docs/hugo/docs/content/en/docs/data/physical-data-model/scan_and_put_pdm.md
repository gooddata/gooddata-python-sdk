---
title: "scan_and_put_pdm"
linkTitle: "scan_and_put_pdm"
weight: 200
superheading: "catalog_data_source."
---



``scan_and_put_pdm(data_source_id: str, scan_request: CatalogScanModelRequest = CatalogScanModelRequest())``

This method combines [scan_data_source](../../data-source/scan_data_source) and [put_declarative_pdm](../put_declarative_pdm) methods.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="scan_request" p_type="Optional[CatalogScanModelRequest]" >}}
Options for the Scan Request. Defaults to CatalogScanModelRequest().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```Python
# scan and put Physical Data Model to server
sdk.catalog_data_source.scan_and_put_pdm(data_source_id="demo-test-ds")
```
