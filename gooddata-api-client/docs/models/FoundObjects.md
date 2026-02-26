# gooddata_api_client.model.found_objects.FoundObjects

List of objects found by similarity search and post-processed by LLM.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | List of objects found by similarity search and post-processed by LLM. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[objects](#objects)** | list, tuple,  | tuple,  | List of objects found with a similarity search. | 
**reasoning** | str,  | str,  | DEPRECATED: Use top-level reasoning.steps instead. Reasoning from LLM. Description of how and why the answer was generated. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# objects

List of objects found with a similarity search.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of objects found with a similarity search. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**SearchResultObject**](SearchResultObject.md) | [**SearchResultObject**](SearchResultObject.md) | [**SearchResultObject**](SearchResultObject.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

