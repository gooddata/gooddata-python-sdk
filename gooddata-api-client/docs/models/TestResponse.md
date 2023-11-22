# gooddata_api_client.model.test_response.TestResponse

Response from data source testing.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Response from data source testing. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**successful** | bool,  | BoolClass,  | A flag indicating whether test passed or not. | 
**error** | str,  | str,  | Field containing more details in case of a failure. Details are available to a privileged user only. | [optional] 
**queryDurationMillis** | [**TestQueryDuration**](TestQueryDuration.md) | [**TestQueryDuration**](TestQueryDuration.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

