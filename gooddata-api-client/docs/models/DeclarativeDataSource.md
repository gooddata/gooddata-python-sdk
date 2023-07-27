# gooddata_api_client.model.declarative_data_source.DeclarativeDataSource

A data source and its properties.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A data source and its properties. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**schema** | str,  | str,  | A scheme/database with the data. | 
**name** | str,  | str,  | Name of the data source. | 
**id** | str,  | str,  | Data source ID. | 
**type** | str,  | str,  | Type of database. | must be one of ["POSTGRESQL", "REDSHIFT", "VERTICA", "SNOWFLAKE", "ADS", "BIGQUERY", "MSSQL", "PRESTO", "DREMIO", "DRILL", "GREENPLUM", "AZURESQL", "SYNAPSESQL", "DATABRICKS", ] 
**[cachePath](#cachePath)** | list, tuple,  | tuple,  | Path to schema, where intermediate caches are stored. | [optional] 
**[decodedParameters](#decodedParameters)** | list, tuple,  | tuple,  |  | [optional] 
**enableCaching** | bool,  | BoolClass,  | Enable caching of intermediate results. | [optional] 
**[parameters](#parameters)** | list, tuple,  | tuple,  |  | [optional] 
**password** | str,  | str,  | Password for the data-source user, property is never returned back. | [optional] 
**pdm** | [**DeclarativeTables**](DeclarativeTables.md) | [**DeclarativeTables**](DeclarativeTables.md) |  | [optional] 
**[permissions](#permissions)** | list, tuple,  | tuple,  |  | [optional] 
**token** | str,  | str,  | Token as an alternative to username and password. | [optional] 
**url** | str,  | str,  | An connection string relevant to type of database. | [optional] 
**username** | str,  | str,  | User with permission connect the data source/database. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# cachePath

Path to schema, where intermediate caches are stored.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Path to schema, where intermediate caches are stored. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# decodedParameters

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Parameter**](Parameter.md) | [**Parameter**](Parameter.md) | [**Parameter**](Parameter.md) |  | 

# parameters

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Parameter**](Parameter.md) | [**Parameter**](Parameter.md) | [**Parameter**](Parameter.md) |  | 

# permissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeDataSourcePermission**](DeclarativeDataSourcePermission.md) | [**DeclarativeDataSourcePermission**](DeclarativeDataSourcePermission.md) | [**DeclarativeDataSourcePermission**](DeclarativeDataSourcePermission.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

