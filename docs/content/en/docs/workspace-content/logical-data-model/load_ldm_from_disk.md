---
title: "load_ldm_from_disk"
linkTitle: "load_ldm_from_disk"
weight: 101
superheading: "catalog_workspace_content."
---

``load_ldm_from_disk( path: Path = Path.cwd())``

Loads the logical data model stored to disk using [store_ldm_to_disk](../store_ldm_to_disk/).

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeModel" >}}
Object Containing declarative Logical Data Model.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get the stored Logical Data model
logical_model = sdk.catalog_workspace_content.load_ldm_from_disk(path=Path.cwd())
```
