# gooddata_api_client.model.declarative_table.DeclarativeTable

A database table.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A database table. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[path](#path)** | list, tuple,  | tuple,  | Path to table. | 
**[columns](#columns)** | list, tuple,  | tuple,  | An array of physical columns | 
**id** | str,  | str,  | Table id. | 
**type** | str,  | str,  | Table type: TABLE or VIEW. | 
**namePrefix** | str,  | str,  | Table or view name prefix used in scan. Will be stripped when generating LDM. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# columns

An array of physical columns

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of physical columns | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeColumn**](DeclarativeColumn.md) | [**DeclarativeColumn**](DeclarativeColumn.md) | [**DeclarativeColumn**](DeclarativeColumn.md) |  | 

# path

Path to table.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Path to table. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

