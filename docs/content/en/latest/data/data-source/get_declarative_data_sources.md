---
title: "get_declarative_data_sources"
linkTitle: "get_declarative_data_sources"
weight: 70
superheading: "catalog_data_source."
---



``get_declarative_data_sources()``


Gets all data sources, including their related physical data model.


{{% parameters-block title="Parameters" None="yes" %}}
{{% /parameters-block %}}
{{% parameters-block title="Returns"%}}
{{< parameter p_type="CatalogDeclarativeDataSources" >}}
Data source object, including physical data model.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get Declarative data sources
declarative_data_sources = sdk.catalog_data_source.get_declarative_data_sources()
```
