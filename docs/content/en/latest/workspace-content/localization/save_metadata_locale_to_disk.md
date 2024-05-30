---
title: "save_metadata_locale_to_disk"
linkTitle: "save_metadata_locale_to_disk"
weight: 56
superheading: "catalog_workspace."
---

``save_metadata_locale_to_disk(workspace_id: str, target_language: str, file_path: Path) -> None``

Save the metadata localization for a workspace to a file.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the workspace.
{{< /parameter >}}
{{< parameter p_name="target_language" p_type="string" >}}
The target language for the metadata localization.
{{< /parameter >}}
{{< parameter p_name="file_path" p_type="Path" >}}
The path to the file where the XLIFF content will be saved.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Save the metadata localization for a workspace to a file.
sdk.catalog_workspace.save_metadata_locale_to_disk(
    workspace_id="123",
    target_language="de-DE",
    file_path=Path("/path/to/file.xliff")
)
