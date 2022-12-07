---
title: "load_and_put_declarative_ldm"
linkTitle: "load_and_put_declarative_ldm"
weight: 120
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``load_and_put_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd(), validator: Optional[DataSourceValidator])``

This method combines [load_declarative_ldm](../load_declarative_ldm) and [put_declarative_ldm](../get_declarative_ldm) methods to load and set layouts stored using [store_declarative_ldm](../store_declarative_ldm). You can pass an additional validator parameter which checks that for every data source id in the logical data model the corresponding data source exists.

## Example

The load and put can be done two ways.

Either by one call:

```Python
# Load and  put logical data model.
sdk.catalog_workspace_content.load_and_put_declarative_ldm(
    workspace_id="123",
    layout_root_path=Path.cwd()
)

```

Or by two separate calls:

```Python
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
