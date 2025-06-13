---
title: "export_pdf"
linkTitle: "export_pdf"
weight: 110
superheading: "export."
---

{{< api-ref "sdk.ExportService.export_pdf" >}}

## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)


sdk.export.export_pdf(workspace_id="demo",  dashboard_id="campaign", file_name="test")
```
