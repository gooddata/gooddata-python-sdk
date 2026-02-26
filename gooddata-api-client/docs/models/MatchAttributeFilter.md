# gooddata_api_client.model.match_attribute_filter.MatchAttributeFilter

Filter via label with given match type and literal value.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Filter via label with given match type and literal value. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[matchAttributeFilter](#matchAttributeFilter)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# matchAttributeFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**matchType** | str,  | str,  | Requested match type. | must be one of ["STARTS_WITH", "ENDS_WITH", "CONTAINS", ] 
**label** | [**AfmIdentifier**](AfmIdentifier.md) | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**literal** | str,  | str,  | Literal used to limit label values. | 
**applyOnResult** | bool,  | BoolClass,  |  | [optional] 
**caseSensitive** | bool,  | BoolClass,  | Indicates whether the filter match is evaluated in case-sensitive mode or not. | [optional] if omitted the server will use the default value of False
**localIdentifier** | str,  | str,  |  | [optional] 
**negate** | bool,  | BoolClass,  | Indicates whether the filter should negate the match. | [optional] if omitted the server will use the default value of False
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

