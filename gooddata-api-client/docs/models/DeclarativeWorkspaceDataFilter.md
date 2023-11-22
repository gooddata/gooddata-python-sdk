# gooddata_api_client.model.declarative_workspace_data_filter.DeclarativeWorkspaceDataFilter

Workspace Data Filters serving the filtering of what data users can see in workspaces.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Workspace Data Filters serving the filtering of what data users can see in workspaces. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[workspaceDataFilterSettings](#workspaceDataFilterSettings)** | list, tuple,  | tuple,  | Filter settings specifying values of filters valid for the workspace. | 
**id** | str,  | str,  | Workspace Data Filters ID. This ID is further used to refer to this instance. | 
**title** | str,  | str,  | Workspace Data Filters title. | 
**columnName** | str,  | str,  | Workspace Data Filters column name. Data are filtered using this physical column. | 
**description** | str,  | str,  | Workspace Data Filters description. | [optional] 
**workspace** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# workspaceDataFilterSettings

Filter settings specifying values of filters valid for the workspace.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Filter settings specifying values of filters valid for the workspace. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeWorkspaceDataFilterSetting**](DeclarativeWorkspaceDataFilterSetting.md) | [**DeclarativeWorkspaceDataFilterSetting**](DeclarativeWorkspaceDataFilterSetting.md) | [**DeclarativeWorkspaceDataFilterSetting**](DeclarativeWorkspaceDataFilterSetting.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

