---
title: "add_metadata_locale"
linkTitle: "add_metadata_locale"
weight: 25
superheading: "catalog_workspace."
---

{{< api-ref "sdk.CatalogWorkspaceService.add_metadata_locale" >}}

## Example

```python
# Add and set the metadata localization for a workspace using a translation function.
sdk.catalog_workspace.add_metadata_locale(
    workspace_id="123",
    target_language="de-DE",
    translator_func=my_translation_function,
    set_locale=True
)
