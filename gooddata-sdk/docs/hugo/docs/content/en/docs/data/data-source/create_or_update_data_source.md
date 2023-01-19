---
title: "create_or_update_data_source"
linkTitle: "create_or_update_data_source"
weight: 10
superheading: "catalog_data_source."
---



``create_or_update_data_source(data_source: CatalogDataSource)``

Pushes the data source to the GoodData environment. Automatically decides, whether to create or update.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source" p_type="CatalogDataSource" >}}
Catalog data source object
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

### Example

```python
# PostgreSQL example
sdk.catalog_data_source.create_or_update_data_source(
    CatalogDataSourcePostgres(
        id=data_source_id,
        name=data_source_name,
        db_specific_attributes=PostgresAttributes(
            host=os.environ["POSTGRES_HOST"],
            db_name=os.environ["POSTGRES_DBNAME"]
        ),
        schema=os.environ["POSTGRES_SCHEMA"],
        credentials=BasicCredentials(
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
        ),
    )
)
```
