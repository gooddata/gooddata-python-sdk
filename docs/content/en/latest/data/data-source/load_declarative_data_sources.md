---
title: "load_declarative_data_sources"
linkTitle: "load_declarative_data_sources"
weight: 100
superheading: "catalog_data_source."
---



``load_declarative_data_sources(layout_root_path: Path = Path.cwd())``

Loads declarative data sources layout, which was stored using [store_declarative_data_sources](../store_declarative_data_sources/).

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="declarative_data_sources" p_type="CatalogDeclarativeDataSources" >}}
 Declarative data sources object
{{< /parameter >}}
{{< parameter p_name="layout_root_path" p_type="Optional[Path]" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="CatalogDeclarativeDataSources" >}}
Declarative data sources object
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get Declarative data sources
declarative_data_sources = sdk.catalog_data_source.get_declarative_data_sources()
```
