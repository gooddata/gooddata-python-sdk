# gooddata_api_client.model.visible_filter.VisibleFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**isAllTimeDateFilter** | bool,  | BoolClass,  | Indicates if the filter is an all-time date filter. Such a filter is not included in report computation, so there is no filter with the same &#x27;localIdentifier&#x27; to be found. In such cases, this flag is used to inform the server to not search for the filter in the definitions and include it anyways. | [optional] if omitted the server will use the default value of False
**localIdentifier** | str,  | str,  |  | [optional] 
**title** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

