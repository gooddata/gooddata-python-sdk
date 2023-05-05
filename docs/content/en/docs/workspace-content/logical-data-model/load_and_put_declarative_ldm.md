---
title: "load_and_put_declarative_ldm"
linkTitle: "load_and_put_declarative_ldm"
weight: 120
superheading: "catalog_workspace_content."
---



``load_and_put_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd(), validator: Optional[DataSourceValidator])``

This method combines [load_declarative_ldm](../load_declarative_ldm/) and [put_declarative_ldm](../get_declarative_ldm/) methods to load and set layouts stored using [store_declarative_ldm](../store_declarative_ldm/). You can pass an additional validator parameter which checks that for every data source id in the logical data model the corresponding data source exists.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{< parameter p_name="validator" p_type="Optional[DataSourceValidator]" >}}
Object that manages validation, whether each data_source_id in LDM corresponds to existing data source. Defaults to None.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

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
