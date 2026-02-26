# gooddata_api_client.model.execution_result_metadata.ExecutionResultMetadata

Additional metadata for the particular execution result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Additional metadata for the particular execution result. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[dataSourceMessages](#dataSourceMessages)** | list, tuple,  | tuple,  | Additional information sent by the underlying data source. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# dataSourceMessages

Additional information sent by the underlying data source.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Additional information sent by the underlying data source. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExecutionResultDataSourceMessage**](ExecutionResultDataSourceMessage.md) | [**ExecutionResultDataSourceMessage**](ExecutionResultDataSourceMessage.md) | [**ExecutionResultDataSourceMessage**](ExecutionResultDataSourceMessage.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

