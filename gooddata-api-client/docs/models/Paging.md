# gooddata_api_client.model.paging.Paging

Current page description.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Current page description. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**total** | decimal.Decimal, int,  | decimal.Decimal,  | Count of returnable items ignoring paging. | value must be a 32 bit integer
**offset** | decimal.Decimal, int,  | decimal.Decimal,  | Offset of this page. | value must be a 32 bit integer
**count** | decimal.Decimal, int,  | decimal.Decimal,  | Count of items in this page. | value must be a 32 bit integer
**next** | str,  | str,  | Link to next page, or null if this is last page. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

