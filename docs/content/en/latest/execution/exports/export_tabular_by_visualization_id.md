---
title: "export_tabular_by_visualization_id"
linkTitle: "export_tabular_by_visualization_id"
weight: 110
superheading: "export."
---

{{< api-ref "sdk.ExportService.export_tabular_by_visualization_id" >}}

## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

sdk.export.export_tabular_by_visualization_id(
        workspace_id="demo", visualization_id="campaign_spend", file_format="CSV")

```
