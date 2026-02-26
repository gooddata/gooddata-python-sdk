# gooddata_api_client.model.entity_search_body.EntitySearchBody

Request body for entity search operations

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Request body for entity search operations | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**filter** | None, str,  | NoneClass, str,  | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#x27;Some Title&#x27;;description&#x3D;&#x3D;&#x27;desc&#x27;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#x27;Value 123&#x27;). | [optional] 
**[include](#include)** | list, tuple, None,  | tuple, NoneClass,  | List of related entities to include in the response | [optional] 
**[metaInclude](#metaInclude)** | list, tuple, None,  | tuple, NoneClass,  | Set of metadata fields to include in the response | [optional] 
**page** | [**EntitySearchPage**](EntitySearchPage.md) | [**EntitySearchPage**](EntitySearchPage.md) |  | [optional] 
**[sort](#sort)** | list, tuple, None,  | tuple, NoneClass,  | Sorting criteria (can specify multiple sort orders) | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# include

List of related entities to include in the response

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  | List of related entities to include in the response | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# metaInclude

Set of metadata fields to include in the response

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  | Set of metadata fields to include in the response | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# sort

Sorting criteria (can specify multiple sort orders)

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  | Sorting criteria (can specify multiple sort orders) | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**EntitySearchSort**](EntitySearchSort.md) | [**EntitySearchSort**](EntitySearchSort.md) | [**EntitySearchSort**](EntitySearchSort.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

