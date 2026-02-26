# gooddata_api_client.model.file.File

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[any](#any)** | list, tuple,  | tuple,  |  | [optional] 
**canResegment** | str,  | str,  |  | [optional] must be one of ["YES", "NO", ] 
**id** | str,  | str,  |  | [optional] 
**notes** | [**Notes**](Notes.md) | [**Notes**](Notes.md) |  | [optional] 
**original** | str,  | str,  |  | [optional] 
**[otherAttributes](#otherAttributes)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | [optional] 
**skeleton** | [**Skeleton**](Skeleton.md) | [**Skeleton**](Skeleton.md) |  | [optional] 
**space** | str,  | str,  |  | [optional] 
**srcDir** | str,  | str,  |  | [optional] must be one of ["LTR", "RTL", "AUTO", ] 
**translate** | str,  | str,  |  | [optional] must be one of ["YES", "NO", ] 
**trgDir** | str,  | str,  |  | [optional] must be one of ["LTR", "RTL", "AUTO", ] 
**[unitOrGroup](#unitOrGroup)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# any

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# otherAttributes

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type | [optional] 

# unitOrGroup

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

