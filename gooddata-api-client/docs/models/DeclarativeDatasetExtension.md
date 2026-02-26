# gooddata_api_client.model.declarative_dataset_extension.DeclarativeDatasetExtension

A dataset extension properties.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A dataset extension properties. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | The Dataset ID. This ID is further used to refer to this instance of dataset. | 
**[workspaceDataFilterReferences](#workspaceDataFilterReferences)** | list, tuple,  | tuple,  | An array of explicit workspace data filters. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# workspaceDataFilterReferences

An array of explicit workspace data filters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of explicit workspace data filters. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeWorkspaceDataFilterReferences**](DeclarativeWorkspaceDataFilterReferences.md) | [**DeclarativeWorkspaceDataFilterReferences**](DeclarativeWorkspaceDataFilterReferences.md) | [**DeclarativeWorkspaceDataFilterReferences**](DeclarativeWorkspaceDataFilterReferences.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

