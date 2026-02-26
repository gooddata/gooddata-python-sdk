# gooddata_api_client.model.user_management_permission_assignments.UserManagementPermissionAssignments

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[workspaces](#workspaces)** | list, tuple,  | tuple,  |  | 
**[dataSources](#dataSources)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# dataSources

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**UserManagementDataSourcePermissionAssignment**](UserManagementDataSourcePermissionAssignment.md) | [**UserManagementDataSourcePermissionAssignment**](UserManagementDataSourcePermissionAssignment.md) | [**UserManagementDataSourcePermissionAssignment**](UserManagementDataSourcePermissionAssignment.md) |  | 

# workspaces

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**UserManagementWorkspacePermissionAssignment**](UserManagementWorkspacePermissionAssignment.md) | [**UserManagementWorkspacePermissionAssignment**](UserManagementWorkspacePermissionAssignment.md) | [**UserManagementWorkspacePermissionAssignment**](UserManagementWorkspacePermissionAssignment.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

