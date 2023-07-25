# gooddata_api_client.model.result_spec.ResultSpec

Specifies how the result data will be formatted (```dimensions```) and which additional data shall be computed (```totals```).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Specifies how the result data will be formatted (&#x60;&#x60;&#x60;dimensions&#x60;&#x60;&#x60;) and which additional data shall be computed (&#x60;&#x60;&#x60;totals&#x60;&#x60;&#x60;). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[dimensions](#dimensions)** | list, tuple,  | tuple,  |  | 
**[totals](#totals)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# dimensions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Dimension**](Dimension.md) | [**Dimension**](Dimension.md) | [**Dimension**](Dimension.md) |  | 

# totals

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Total**](Total.md) | [**Total**](Total.md) | [**Total**](Total.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

