---
title: "put_declarative_data_sources"
linkTitle: "put_declarative_data_sources"
weight: 80
superheading: "catalog_data_source."
---



``put_declarative_data_sources(declarative_data_sources: CatalogDeclarativeDataSources, credentials_path: Optional[Path] = None, test_data_sources: bool = False)``

Sets all data sources, including their related physical data model.

{{% parameters-block title="Parameters"%}}

{{< parameter p_name="declarative_data_sources" p_type="CatalogDeclarativeDataSources" >}}
Declarative data source object. Can be retrieved by get_declarative_data_sources.
{{< /parameter >}}

{{< parameter p_name="credentials_path" p_type="Optional[Path]" >}}
Path to the Credentials. Optional, defaults to None.
{{< /parameter >}}

{{< parameter p_name="test_data_sources" p_type="Optional[bool]" >}}
If True, the connection of data sources is tested. Defaults to False.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}
## Example

```python
# get declarative data sources.
data_sources = sdk.catalog_data_source.get_declarative_data_sources()

# Modification
data_sources.data_sources.clear()

# Put data sources back on server
sdk.catalog_data_source.put_declarative_data_sources(declarative_data_sources=data_sources)
```
