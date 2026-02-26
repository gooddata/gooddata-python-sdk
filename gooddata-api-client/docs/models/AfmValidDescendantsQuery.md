# gooddata_api_client.model.afm_valid_descendants_query.AfmValidDescendantsQuery

Entity describing the valid descendants request.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Entity describing the valid descendants request. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attributes](#attributes)** | list, tuple,  | tuple,  | List of identifiers of the attributes to get the valid descendants for. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

List of identifiers of the attributes to get the valid descendants for.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of identifiers of the attributes to get the valid descendants for. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AfmObjectIdentifierAttribute**](AfmObjectIdentifierAttribute.md) | [**AfmObjectIdentifierAttribute**](AfmObjectIdentifierAttribute.md) | [**AfmObjectIdentifierAttribute**](AfmObjectIdentifierAttribute.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

