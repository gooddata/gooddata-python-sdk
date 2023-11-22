# gooddata_api_client.model.declarative_reference.DeclarativeReference

A dataset reference.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A dataset reference. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**identifier** | [**ReferenceIdentifier**](ReferenceIdentifier.md) | [**ReferenceIdentifier**](ReferenceIdentifier.md) |  | 
**[sourceColumns](#sourceColumns)** | list, tuple,  | tuple,  | An array of source column names for a given reference. | 
**multivalue** | bool,  | BoolClass,  | The multi-value flag enables many-to-many cardinality for references. | 
**[sourceColumnDataTypes](#sourceColumnDataTypes)** | list, tuple,  | tuple,  | An array of source column data types for a given reference. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# sourceColumns

An array of source column names for a given reference.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of source column names for a given reference. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# sourceColumnDataTypes

An array of source column data types for a given reference.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of source column data types for a given reference. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

