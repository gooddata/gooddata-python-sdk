---
title: "load_declarative_ldm"
linkTitle: "load_declarative_ldm"
weight: 110
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``load_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd())``

Returns *CatalogDeclarativeModel*.

Load declarative LDM layout, which was stored using [store_declarative_ldm](./store_declarative_ldm).

## Example

```Python
# Load stored declarative Logical Data Model
logical_model = sdk.catalog_workspace_content.load_declarative_ldm(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
