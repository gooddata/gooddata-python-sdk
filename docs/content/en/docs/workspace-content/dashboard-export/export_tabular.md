---
title: "export_tabular"
linkTitle: "export_tabular"
weight: 110
superheading: "export."
---

``export_tabular(workspace_id: str,
        dashboard_id: str,
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
{{< parameter p_name="dashboard_id" p_type="string" >}}
The ID of the GoodData Dashboard.
{{< /parameter >}}
{{< parameter p_name="file_name" p_type="String" >}}
The name of the PDF file (excluding the file extension). Defaults to Path.cwd()
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

{{% parameters-block title="Returns" None="true"%}}
{{% /parameters-block %}}


## Example

```python

## TODO: Hkad98

```
