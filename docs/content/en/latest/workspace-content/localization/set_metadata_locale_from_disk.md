---
title: "set_metadata_locale_from_disk"
linkTitle: "set_metadata_locale_from_disk"
weight: 57
superheading: "catalog_workspace."
---

``set_metadata_locale_from_disk(workspace_id: str, file_path: Path) -> None``

Load and set the metadata localization for a workspace from a file.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the workspace to which the metadata localization applies.
{{< /parameter >}}
{{< parameter p_name="file_path" p_type="Path" >}}
The path to the file containing the encoded XML metadata.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Load and set the metadata localization for a workspace from a file.
from pathlib import Path

sdk.catalog_workspace.set_metadata_locale_from_disk(
    workspace_id="123",
    file_path=Path("/path/to/file.xliff")
)
