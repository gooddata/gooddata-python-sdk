---
title: "Data Source"
linkTitle: "Data Source"
weight: 10
no_list: true
---

Manage data sources.

See [Connect Data](https://www.gooddata.com/docs/cloud/connect-data/) to learn how data sources work in GoodData.


### Entity Methods

* [create_or_update_data_source](./create_or_update_data_source/)
* [get_data_source](./get_data_source/)
* [delete_data_source](./delete_data_source/)
* [list_data_sources](./list_data_sources/)
* [patch_data_source_attributes](./patch_data_source_attributes/)

### Declarative Methods

* [get_declarative_data_sources](./get_declarative_data_sources/)
* [put_declarative_data_sources](./put_declarative_data_sources/)
* [store_declarative_data_sources](./store_declarative_data_sources/)
* [load_declarative_data_sources](./load_declarative_data_sources/)
* [load_and_put_declarative_data_sources](./load_and_put_declarative_data_sources/)


### Action Methods

* [test_data_sources_connection](./test_data_sources_connection/)
* [generate_logical_model](./generate_logical_model/)
* [register_upload_notification](./register_upload_notification/)
* [scan_data_source](./scan_data_source/)
* [scan_schemata](./scan_schemata/)
* [scan_sql](./scan_sql/)


## Example

Since there are multiple data source types, here are examples of how to initialize each of them:

### Postgres

```python
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
```

### Redshift

```python
CatalogDataSourceRedshift(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=RedshiftAttributes(
        host=os.environ["REDSHIFT_HOST"],
        db_name=os.environ["REDSHIFT_DBNAME"]
    ),
    schema=os.environ["REDSHIFT_SCHEMA"],
    credentials=BasicCredentials(
        username=os.environ["REDSHIFT_USER"],
        password=os.environ["REDSHIFT_PASSWORD"],
    ),
)
```
### Snowflake

Using basic credentials (username + password):
```python
CatalogDataSourceSnowflake(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=SnowflakeAttributes(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        db_name=os.environ["SNOWFLAKE_DBNAME"]
    ),
    schema=os.environ["SNOWFLAKE_SCHEMA"],
    credentials=BasicCredentials(
        username=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
    ),
)
```

Using key-pair authentication (username + private_key, optionally private_key_passphrase):
```python
CatalogDataSourceSnowflake(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=SnowflakeAttributes(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        db_name=os.environ["SNOWFLAKE_DBNAME"]
    ),
    schema=os.environ["SNOWFLAKE_SCHEMA"],
    credentials=KeyPairCredentials(
        username=os.environ["SNOWFLAKE_USER"],
        private_key=os.environ["SNOWFLAKE_PRIVATE_KEY"],
    ),
)
```

### Vertica

```python
CatalogDataSourceVertica(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=VerticaAttributes(
        host=os.environ["VERTICA_HOST"],
        db_name=os.environ["VERTICA_DBNAME"]
    ),
    schema=os.environ["VERTICA_SCHEMA"],
    credentials=BasicCredentials(
        username=os.environ["VERTICA_USER"],
        password=os.environ["VERTICA_PASSWORD"],
    ),
)
```

### BigQuery

```python
CatalogDataSourceBigQuery(
    id=data_source_id,
    name=data_source_name,
    schema=os.environ["BIGQUERY_SCHEMA"],
    credentials=TokenCredentialsFromFile(
        file_path=Path(os.environ["BIGQUERY_CREDENTIALS"])
    ),
    parameters=[{"name": "projectId", "value": "abc"}],
)
```
### Greenplum

```python
CatalogDataSourceGreenplum(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=GreenplumAttributes(
        host=os.environ["GREENPLUM_HOST"],
        db_name=os.environ["GREENPLUM_DBNAME"]
    ),
    schema=os.environ["GREENPLUM_SCHEMA"],
    credentials=BasicCredentials(
        username=os.environ["GREENPLUM_USER"],
        password=os.environ["GREENPLUM_PASSWORD"],
    ),
)
```

### Microsoft SQL Server

```python
CatalogDataSourceMsSql(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=MsSqlAttributes(
        host=os.environ["MSSQL_HOST"],
        db_name=os.environ["MSSQL_DBNAME"]
    ),
    schema=os.environ["MSSQL_SCHEMA"],
    credentials=BasicCredentials(
        username=os.environ["MSSQL_USER"],
        password=os.environ["MSSQL_PASSWORD"],
    ),
)
```

### Databricks

Using Machine-to-Machine (M2M) authentication (client_id + client_secret):
```python
CatalogDataSourceDatabricks(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=DatabricksAttributes(
        host=os.environ["DATABRICKS_HOST"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"]
    ),
    schema=xyz,
    parameters=[{"name":"catalog", "value": os.environ["DATABRICKS_CATALOG"]}],
    credentials=ClientSecretCredentials(
        client_id=os.environ["DATABRICKS_CLIENT_ID"],
        client_secret=os.environ["DATABRICKS_CLIENT_SECRET"],
    ),
)
```

Using personal access token authentication:
```python
CatalogDataSourceDatabricks(
    id=data_source_id,
    name=data_source_name,
    db_specific_attributes=DatabricksAttributes(
        host=os.environ["DATABRICKS_HOST"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"]
    ),
    schema=xyz,
    parameters=[{"name":"catalog", "value": os.environ["DATABRICKS_CATALOG"]}],
    credentials=TokenCredentials(
        token=os.environ["DATABRICKS_PERSONAL_ACCESS_TOKEN"]
    ),
)
```
