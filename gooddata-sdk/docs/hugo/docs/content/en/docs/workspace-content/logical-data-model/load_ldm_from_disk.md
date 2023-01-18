---
title: "load_ldm_from_disk"
linkTitle: "load_ldm_from_disk"
weight: 101
superheading: "catalog_workspace_content."
---

``load_ldm_from_disk( path: Path = Path.cwd())``

The method is used to load ldm stored to disk using method `store_ldm_to_disk`.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeModel" >}}
TODO hkad98
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```Python
# Retrieve the stored Logical Data model
logical_model = sdk.catalog_workspace_content.load_ldm_from_disk(path=Path.cwd())
```
