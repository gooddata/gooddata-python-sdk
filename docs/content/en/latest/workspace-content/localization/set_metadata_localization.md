---
title: "set_metadata_localization"
linkTitle: "set_metadata_localization"
weight: 53
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.set_metadata_localization" >}}

## Example

```python
# Set the metadata localization for a workspace using encoded XML.
sdk.catalog_workspace.set_metadata_localization(
    workspace_id="123",
    encoded_xml=b"<xml>...</xml>"
)
