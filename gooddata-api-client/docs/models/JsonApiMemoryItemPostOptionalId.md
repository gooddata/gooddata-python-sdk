# gooddata_api_client.model.json_api_memory_item_post_optional_id.JsonApiMemoryItemPostOptionalId

JSON:API representation of memoryItem entity.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | JSON:API representation of memoryItem entity. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attributes](#attributes)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**type** | str,  | str,  | Object type | must be one of ["memoryItem", ] 
**id** | str,  | str,  | API identifier of an object | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**instruction** | str,  | str,  | The text that will be injected into the system prompt | 
**strategy** | str,  | str,  | Strategy defining when the memory item should be applied | must be one of ["ALWAYS", "AUTO", ] 
**areRelationsValid** | bool,  | BoolClass,  |  | [optional] 
**description** | str,  | str,  |  | [optional] 
**isDisabled** | bool,  | BoolClass,  | Whether memory item is disabled | [optional] 
**[keywords](#keywords)** | list, tuple,  | tuple,  | Set of unique strings used for semantic similarity filtering | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  |  | [optional] 
**title** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# keywords

Set of unique strings used for semantic similarity filtering

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Set of unique strings used for semantic similarity filtering | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# tags

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

