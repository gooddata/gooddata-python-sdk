---
title: "set_metadata_locale_from_disk"
linkTitle: "set_metadata_locale_from_disk"
weight: 57
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.set_metadata_locale_from_disk" >}}

## Example

```python
# Load and set the metadata localization for a workspace from a file.
from pathlib import Path

sdk.catalog_workspace.set_metadata_locale_from_disk(
    workspace_id="123",
    file_path=Path("/path/to/file.xliff")
)
