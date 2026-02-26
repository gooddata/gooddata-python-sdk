# gooddata_api_client.model.route_result.RouteResult

Question -> Use Case routing. May contain final answer is a special use case is not required.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Question -&gt; Use Case routing. May contain final answer is a special use case is not required. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**useCase** | str,  | str,  | Use case where LLM routed based on question. | must be one of ["INVALID", "GENERAL", "SEARCH", "CREATE_VISUALIZATION", "EXTEND_VISUALIZATION", "HOWTO", "CHANGE_ANALYSIS", "ALERT", ] 
**reasoning** | str,  | str,  | Explanation why LLM picked this use case. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

