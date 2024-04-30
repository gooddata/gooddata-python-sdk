---
title: "load_pdm_from_disk"
linkTitle: "load_pdm_from_disk"
weight: 140
superheading: "catalog_data_source."
---

``load_pdm_from_disk(path: Path = Path.cwd())``

This method is used to load pdm stored to disk using method [store_pdm_to_disk](../store_pdm_to_disk/).


{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="path" p_type="Optiona[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeTables" >}}
Physical Data Model object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Load Physical Data Model from disk
sdk.catalog_data_source.load_pdm_from_disk(path=Path("xyz"))
```
