---
title: "export_tabular_by_visualization_id"
linkTitle: "export_tabular_by_visualization_id"
weight: 110
superheading: "export."
---

``export_tabular_by_visualization_id(
        workspace_id: str,
        visualization_id: str,
        file_format: str,
        file_name: Optional[str] = None,
        settings: Optional[ExportSettings] = None,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    )``

    Exports the tabular data for an visualization by its ID.



{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{< parameter p_name="visualization_id" p_type="string" >}}
The ID of the GoodData visualization.
{{< /parameter >}}
{{< parameter p_name="file_format" p_type="string" >}}
The format of the file to be exported.
{{< /parameter >}}
{{< parameter p_name="file_name" p_type="String" >}}
The name which the exported file should have. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="settings" p_type="Optional[ExportSettings]" >}}
Any additional settings for the export. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="store_path" p_type="Union[String, Path]" >}}
The path to store the exported file. Defaults to Path.cwd().
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

{{% parameters-block title="Returns" None="true" %}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

sdk.export.export_tabular_by_visualization_id(
        workspace_id="demo", visualization_id="campaign_spend", file_format="CSV")

```
