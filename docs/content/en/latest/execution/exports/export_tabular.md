---
title: "export_tabular"
linkTitle: "export_tabular"
weight: 110
superheading: "export."
---

{{< api-ref "sdk.ExportService.export_tabular" >}}

## Example

```python
host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

workspace_id = "demo"
exec_def = ExecutionDefinition(
        attributes=[Attribute(local_id="region", label="region"), Attribute(local_id="state", label="state")],
        metrics=[
            SimpleMetric(local_id="price", item=ObjId(id="price", type="fact")),
            SimpleMetric(local_id="order_amount", item=ObjId(id="order_amount", type="metric")),
        ],
        filters=[],
        dimensions=[
            TableDimension(item_ids=["state", "region"]),
            TableDimension(item_ids=["measureGroup"]),
        ],
    )
execution_result=sdk.compute.for_exec_def(workspace_id, exec_def).result_id
export_request = ExportRequest(
        format="CSV",
        execution_result=execution_result,
        file_name="my_file",
        custom_override=ExportCustomOverride(
            labels={"region": ExportCustomLabel(title="Custom Title Region")},
            metrics={
                "price": ExportCustomMetric(title="Sum Of Price", format=""),
                "order_amount": ExportCustomMetric(title="Order Amount Metric", format="#,##0.00"),
            },
        ),
    )


sdk.export.export_tabular(workspace_id, export_request, _exports_dir)
```
