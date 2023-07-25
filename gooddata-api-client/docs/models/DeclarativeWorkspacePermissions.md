# gooddata_api_client.model.declarative_workspace_permissions.DeclarativeWorkspacePermissions

Definition of permissions associated with a workspace.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Definition of permissions associated with a workspace. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[hierarchyPermissions](#hierarchyPermissions)** | list, tuple,  | tuple,  |  | [optional] 
**[permissions](#permissions)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

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

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

