# gooddata_api_client.model.workspace_data_source.WorkspaceDataSource

The data source used for the particular workspace instead of the one defined in the LDM inherited from its parent workspace. Such data source cannot be defined for a single or a top-parent workspace.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The data source used for the particular workspace instead of the one defined in the LDM inherited from its parent workspace. Such data source cannot be defined for a single or a top-parent workspace. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | The ID of the used data source. | 
**[schemaPath](#schemaPath)** | list, tuple,  | tuple,  | The full schema path as array of its path parts. Will be rendered as subPath1.subPath2... | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# schemaPath

The full schema path as array of its path parts. Will be rendered as subPath1.subPath2...

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The full schema path as array of its path parts. Will be rendered as subPath1.subPath2... | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | The part of the schema path. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

