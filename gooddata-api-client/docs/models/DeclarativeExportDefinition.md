# gooddata_api_client.model.declarative_export_definition.DeclarativeExportDefinition

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Export definition id. | 
**title** | str,  | str,  | Export definition object title. | 
**createdAt** | None, str,  | NoneClass, str,  | Time of the entity creation. | [optional] 
**createdBy** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | str,  | str,  | Export definition object description. | [optional] 
**modifiedAt** | None, str,  | NoneClass, str,  | Time of the last entity modification. | [optional] 
**modifiedBy** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**[requestPayload](#requestPayload)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# requestPayload

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[TabularExportRequest](TabularExportRequest.md) | [**TabularExportRequest**](TabularExportRequest.md) | [**TabularExportRequest**](TabularExportRequest.md) |  | 
[VisualExportRequest](VisualExportRequest.md) | [**VisualExportRequest**](VisualExportRequest.md) | [**VisualExportRequest**](VisualExportRequest.md) |  | 

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

