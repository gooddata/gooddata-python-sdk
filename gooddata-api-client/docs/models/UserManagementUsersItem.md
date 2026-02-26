# gooddata_api_client.model.user_management_users_item.UserManagementUsersItem

List of users

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | List of users | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[userGroups](#userGroups)** | list, tuple,  | tuple,  |  | 
**id** | str,  | str,  |  | 
**[workspaces](#workspaces)** | list, tuple,  | tuple,  |  | 
**[dataSources](#dataSources)** | list, tuple,  | tuple,  |  | 
**organizationAdmin** | bool,  | BoolClass,  | Is user organization admin | 
**email** | str,  | str,  | User email address | [optional] 
**name** | str,  | str,  | User name | [optional] 
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

# userGroups

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**UserGroupIdentifier**](UserGroupIdentifier.md) | [**UserGroupIdentifier**](UserGroupIdentifier.md) | [**UserGroupIdentifier**](UserGroupIdentifier.md) |  | 

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

