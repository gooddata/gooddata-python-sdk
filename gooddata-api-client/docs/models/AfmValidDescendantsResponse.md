# gooddata_api_client.model.afm_valid_descendants_response.AfmValidDescendantsResponse

Entity describing the valid descendants response.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Entity describing the valid descendants response. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[validDescendants](#validDescendants)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of attribute identifiers to list of valid descendants identifiers. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# validDescendants

Map of attribute identifiers to list of valid descendants identifiers.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of attribute identifiers to list of valid descendants identifiers. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[any_string_name](#any_string_name)** | list, tuple,  | tuple,  | any string name can be used but the value must be the correct type Map of attribute identifiers to list of valid descendants identifiers. | [optional] 

# any_string_name

Map of attribute identifiers to list of valid descendants identifiers.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Map of attribute identifiers to list of valid descendants identifiers. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AfmObjectIdentifierAttribute**](AfmObjectIdentifierAttribute.md) | [**AfmObjectIdentifierAttribute**](AfmObjectIdentifierAttribute.md) | [**AfmObjectIdentifierAttribute**](AfmObjectIdentifierAttribute.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

