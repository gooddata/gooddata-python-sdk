# gooddata_api_client.model.chat_usage_response.ChatUsageResponse

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**interactionLimit** | decimal.Decimal, int,  | decimal.Decimal,  | Maximum number of interactions in the time window any user can do in the workspace | value must be a 32 bit integer
**timeWindowHours** | decimal.Decimal, int,  | decimal.Decimal,  | Time window in hours | value must be a 32 bit integer
**interactionCount** | decimal.Decimal, int,  | decimal.Decimal,  | Number of interactions in the time window | value must be a 32 bit integer
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

