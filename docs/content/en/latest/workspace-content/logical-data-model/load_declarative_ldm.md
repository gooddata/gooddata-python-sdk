---
title: "load_declarative_ldm"
linkTitle: "load_declarative_ldm"
weight: 110
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.load_declarative_ldm" >}}

## Example

```python
# Load stored declarative Logical Data Model
logical_model = sdk.catalog_workspace_content.load_declarative_ldm(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
