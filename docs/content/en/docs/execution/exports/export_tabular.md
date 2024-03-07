---
title: "export_tabular"
linkTitle: "export_tabular"
weight: 110
superheading: "export."
---

``export_tabular(workspace_id: str,
        export_request: ExportRequest,
        file_name: str,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    )``

    Export Tabular (CSV, XLSX) data from the specified GoodData Dashboard report, saved to the specified file path.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{< parameter p_name="export_request" p_type="ExportRequest" >}}
An instance of ExportRequest containing the required information for the tabular export.
{{< /parameter >}}
{{< parameter p_name="store_path" p_type="Union[String, Path]" >}}
The path to save the exported tabular data. Defaults to Path.cwd().
{{< /parameter >}}
{{< parameter p_name="timeout" p_type="float" >}}
The maximum amount of time (in seconds) to wait for the server to process the export. Defaults to 60.0.
{{< /parameter >}}
{{< parameter p_name="retry" p_type="float" >}}
Initial wait time (in seconds) before retrying to get the exported content. Defaults to 0.2.
{{< /parameter >}}
{{< parameter p_name="max_retry" p_type="float" >}}
The maximum retry wait time (in seconds). Defaults to 5.0.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="true"%}}
{{% /parameters-block %}}


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
