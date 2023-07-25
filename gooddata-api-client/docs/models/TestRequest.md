# gooddata_api_client.model.test_request.TestRequest

A request containing all information for testing existing data source.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A request containing all information for testing existing data source. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[cachePath](#cachePath)** | list, tuple,  | tuple,  |  | [optional] 
**enableCaching** | bool,  | BoolClass,  | Enable caching of intermediate results. | [optional] 
**[parameters](#parameters)** | list, tuple,  | tuple,  |  | [optional] 
**password** | str,  | str,  | Database user password. | [optional] 
**schema** | str,  | str,  | Database schema. | [optional] 
**token** | str,  | str,  | Secret for token based authentication for data sources which supports it. | [optional] 
**url** | str,  | str,  | URL to database in JDBC format, where test should connect to. | [optional] 
**username** | str,  | str,  | Database user name. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# cachePath

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# parameters

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DataSourceParameter**](DataSourceParameter.md) | [**DataSourceParameter**](DataSourceParameter.md) | [**DataSourceParameter**](DataSourceParameter.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

