---
title: "get_declarative_pdm"
linkTitle: "get_declarative_pdm"
weight: 120
superheading: "catalog_data_source."
---

<!-- TODO -->

``get_declarative_pdm(data_source_id: str)``

Retrieve physical data model for a given data source.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="data_source_id" p_type="string" >}}
Data Source identification string. e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogDeclarativeTables" >}}
Physical Data Model object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```Python
# Get Physical Data Model in declarative form
declarative_tables = sdk.catalog_data_source.get_declarative_pdm(data_source_id="123")
```
