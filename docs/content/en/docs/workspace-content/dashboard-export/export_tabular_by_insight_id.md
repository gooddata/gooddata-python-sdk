---
title: "export_tabular_by_insight_id"
linkTitle: "export_tabular_by_insight_id"
weight: 110
superheading: "export."
---

``export_tabular_by_insight_id(
        workspace_id: str,
        insight_id: str,
        file_format: str,
        use_labels: bool = True,
        file_name: Optional[str] = None,
        settings: Optional[ExportSettings] = None,
        custom_override: Optional[ExportCustomOverride] = None,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    )``

    Exports the tabular data for an Insight by its ID.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{< parameter p_name="insight_id" p_type="string" >}}
The ID of the GoodData Insight.
{{< /parameter >}}
{{< parameter p_name="file_name" p_type="String" >}}
The name of the PDF file (excluding the file extension). Defaults to Path.cwd()
{{< /parameter >}}
{{< parameter p_name="use_labels" p_type="Optional[bool]" >}}
Whether to use labels for the export. Defaults to True.
{{< /parameter >}}
{{< parameter p_name="settings" p_type="Optional[ExportSettings]" >}}
Configuration settings for the export. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="custom_override" p_type="Optional[ExportCustomOverride]" >}}
Custom settings to override the default settings. Defaults to None.
{{< /parameter >}}
{{< parameter p_name="store_path" p_type="Union[String, Path]" >}}
The name of the PDF file (excluding the file extension). Defaults to Path.cwd()
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

## TODO: Hkad98

```
