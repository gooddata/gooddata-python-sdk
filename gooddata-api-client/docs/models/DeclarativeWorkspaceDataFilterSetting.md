# gooddata_api_client.model.declarative_workspace_data_filter_setting.DeclarativeWorkspaceDataFilterSetting

Workspace Data Filters serving the filtering of what data users can see in workspaces.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Workspace Data Filters serving the filtering of what data users can see in workspaces. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[filterValues](#filterValues)** | list, tuple,  | tuple,  | Only those rows are returned, where columnName from filter matches those values. | 
**workspace** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | 
**id** | str,  | str,  | Workspace Data Filters ID. This ID is further used to refer to this instance. | 
**title** | str,  | str,  | Workspace Data Filters setting title. | 
**description** | str,  | str,  | Workspace Data Filters setting description. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# filterValues

Only those rows are returned, where columnName from filter matches those values.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Only those rows are returned, where columnName from filter matches those values. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Only those rows are returned, where columnName from filter matches those values. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

