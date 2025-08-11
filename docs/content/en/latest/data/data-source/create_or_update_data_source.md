---
title: "create_or_update_data_source"
linkTitle: "create_or_update_data_source"
weight: 10
superheading: "catalog_data_source."
---

{{< api-ref "sdk.CatalogDataSourceService.create_or_update_data_source" >}}

## Example

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
