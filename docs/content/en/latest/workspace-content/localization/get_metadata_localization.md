---
title: "get_metadata_localization"
linkTitle: "get_metadata_localization"
weight: 52
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.get_metadata_localization" >}}

## Example

```python
# Retrieve metadata localization for a workspace in the specified language.
localization = sdk.catalog_workspace.get_metadata_localization(
    workspace_id="123",
    target_language="de-DE"
)
