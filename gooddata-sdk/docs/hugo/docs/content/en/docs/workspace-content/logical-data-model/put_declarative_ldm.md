---
title: "put_declarative_ldm"
linkTitle: "put_declarative_ldm"
weight: 90
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``put_declarative_ldm(workspace_id: str, ldm: CatalogDeclarativeModel, validator: Optional[DataSourceValidator])``

Put a logical data model into a given workspace. You can pass an additional validator parameter which checks that for every data source id in the logical data model the corresponding data source exists.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{< parameter p_name="ldm" p_type="CatalogDeclarativeModel" >}}
TODO hkad98
{{< /parameter >}}
{{< parameter p_name="validator" p_type="Optional[DataSourceValidator]" >}}
TODO hkad98
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```Python
# Generate logical data model
logical_model = sdk.catalog_data_source.generate_logical_model(data_source_id="demo-test-ds")

# Do some changes
# ...

# Put logical data model
sdk.catalog_workspace_content.put_declarative_ldm(workspace_id="demo", ldm=logical_model)
```
