# gooddata_api_client.model.declarative_memory_item.DeclarativeMemoryItem

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**instruction** | str,  | str,  | The text that will be injected into the system prompt. | 
**id** | str,  | str,  | Memory item ID. | 
**strategy** | str,  | str,  | Strategy defining when the memory item should be applied | must be one of ["ALWAYS", "AUTO", ] 
**title** | str,  | str,  | Memory item title. | 
**createdAt** | None, str,  | NoneClass, str,  | Time of the entity creation. | [optional] 
**createdBy** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | str,  | str,  | Memory item description. | [optional] 
**isDisabled** | bool,  | BoolClass,  | Whether memory item is disabled. | [optional] 
**[keywords](#keywords)** | list, tuple,  | tuple,  | Set of unique strings used for semantic similarity filtering. | [optional] 
**modifiedAt** | None, str,  | NoneClass, str,  | Time of the last entity modification. | [optional] 
**modifiedBy** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# keywords

Set of unique strings used for semantic similarity filtering.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Set of unique strings used for semantic similarity filtering. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# tags

A list of tags.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of tags. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | A list of tags. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

