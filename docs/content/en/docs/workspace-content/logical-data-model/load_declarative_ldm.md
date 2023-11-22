---
title: "load_declarative_ldm"
linkTitle: "load_declarative_ldm"
weight: 110
superheading: "catalog_workspace_content."
---



``load_declarative_ldm(workspace_id: str, layout_root_path: Path = Path.cwd())``

Loads declarative LDM layout, which was stored using [store_declarative_ldm](../store_declarative_ldm/).

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeModel" >}}
Object Containing declarative Logical Data Model
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Load stored declarative Logical Data Model
logical_model = sdk.catalog_workspace_content.load_declarative_ldm(
    workspace_id="123",
    layout_root_path=Path.cwd()
)
```
