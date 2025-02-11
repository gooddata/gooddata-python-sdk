---
title: "save_metadata_locale_to_disk"
linkTitle: "save_metadata_locale_to_disk"
weight: 56
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.save_metadata_locale_to_disk" >}}

## Example

```python
# Save the metadata localization for a workspace to a file.
sdk.catalog_workspace.save_metadata_locale_to_disk(
    workspace_id="123",
    target_language="de-DE",
    file_path=Path("/path/to/file.xliff")
)
