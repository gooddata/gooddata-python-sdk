---
title: "put_declarative_ldm"
linkTitle: "put_declarative_ldm"
weight: 90
superheading: "catalog_workspace_content."
---



``put_declarative_ldm(workspace_id: str, ldm: CatalogDeclarativeModel, validator: Optional[DataSourceValidator])``

Puts a logical data model into a given workspace.

Optional validator checks that for every data_source_id in the logical data model there exists corresponding data source.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{< parameter p_name="ldm" p_type="CatalogDeclarativeModel" >}}
Object Containing declarative Logical Data Model
{{< /parameter >}}
{{< parameter p_name="validator" p_type="Optional[DataSourceValidator]" >}}
Object that manages validation, whether each data_source_id in LDM corresponds to existing data source. Defaults to None.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Generate logical data model
logical_model = sdk.catalog_data_source.generate_logical_model(data_source_id="demo-test-ds")

# Do some changes
# ...

# Put logical data model
sdk.catalog_workspace_content.put_declarative_ldm(workspace_id="demo", ldm=logical_model)
```
