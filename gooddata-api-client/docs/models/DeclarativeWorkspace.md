# gooddata_api_client.model.declarative_workspace.DeclarativeWorkspace

A declarative form of a particular workspace.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A declarative form of a particular workspace. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  | Name of a workspace to view. | 
**id** | str,  | str,  | Identifier of a workspace | 
**[customApplicationSettings](#customApplicationSettings)** | list, tuple,  | tuple,  | A list of workspace custom settings. | [optional] 
**description** | str,  | str,  | Description of the workspace | [optional] 
**earlyAccess** | str,  | str,  | Early access defined on level Workspace | [optional] 
**[hierarchyPermissions](#hierarchyPermissions)** | list, tuple,  | tuple,  |  | [optional] 
**model** | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md) | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md) |  | [optional] 
**parent** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | [optional] 
**[permissions](#permissions)** | list, tuple,  | tuple,  |  | [optional] 
**prefix** | str,  | str,  | Custom prefix of entity identifiers in workspace | [optional] 
**[settings](#settings)** | list, tuple,  | tuple,  | A list of workspace settings. | [optional] 
**[userDataFilters](#userDataFilters)** | list, tuple,  | tuple,  | A list of workspace user data filters. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# customApplicationSettings

A list of workspace custom settings.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of workspace custom settings. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeCustomApplicationSetting**](DeclarativeCustomApplicationSetting.md) | [**DeclarativeCustomApplicationSetting**](DeclarativeCustomApplicationSetting.md) | [**DeclarativeCustomApplicationSetting**](DeclarativeCustomApplicationSetting.md) |  | 

# hierarchyPermissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeWorkspaceHierarchyPermission**](DeclarativeWorkspaceHierarchyPermission.md) | [**DeclarativeWorkspaceHierarchyPermission**](DeclarativeWorkspaceHierarchyPermission.md) | [**DeclarativeWorkspaceHierarchyPermission**](DeclarativeWorkspaceHierarchyPermission.md) |  | 

# permissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeSingleWorkspacePermission**](DeclarativeSingleWorkspacePermission.md) | [**DeclarativeSingleWorkspacePermission**](DeclarativeSingleWorkspacePermission.md) | [**DeclarativeSingleWorkspacePermission**](DeclarativeSingleWorkspacePermission.md) |  | 

# settings

A list of workspace settings.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of workspace settings. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeSetting**](DeclarativeSetting.md) | [**DeclarativeSetting**](DeclarativeSetting.md) | [**DeclarativeSetting**](DeclarativeSetting.md) |  | 

# userDataFilters

A list of workspace user data filters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of workspace user data filters. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeUserDataFilter**](DeclarativeUserDataFilter.md) | [**DeclarativeUserDataFilter**](DeclarativeUserDataFilter.md) | [**DeclarativeUserDataFilter**](DeclarativeUserDataFilter.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

