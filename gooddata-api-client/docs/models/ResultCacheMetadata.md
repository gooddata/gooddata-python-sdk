# gooddata_api_client.model.result_cache_metadata.ResultCacheMetadata

All execution result's metadata used for calculation including ExecutionResponse

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | All execution result&#x27;s metadata used for calculation including ExecutionResponse | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**executionResponse** | [**ExecutionResponse**](ExecutionResponse.md) | [**ExecutionResponse**](ExecutionResponse.md) |  | 
**resultSpec** | [**ResultSpec**](ResultSpec.md) | [**ResultSpec**](ResultSpec.md) |  | 
**resultSize** | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 64 bit integer
**afm** | [**AFM**](AFM.md) | [**AFM**](AFM.md) |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

