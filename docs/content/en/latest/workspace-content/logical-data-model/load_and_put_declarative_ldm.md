---
title: "load_and_put_declarative_ldm"
linkTitle: "load_and_put_declarative_ldm"
weight: 120
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.load_and_put_declarative_ldm" >}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and  put logical data model.
sdk.catalog_workspace_content.load_and_put_declarative_ldm(
    workspace_id="123",
    layout_root_path=Path.cwd()
)

```

Or by two separate calls:

```python
# Load stored declarative Logical Data Model
logical_model = sdk.catalog_workspace_content.load_declarative_ldm(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
# Put logical data model
sdk.catalog_workspace_content.put_declarative_ldm(
    workspace_id="123",
    ldm=logical_model
)
```

The result is identical.
