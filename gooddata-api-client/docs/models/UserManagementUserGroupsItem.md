# gooddata_api_client.model.user_management_user_groups_item.UserManagementUserGroupsItem

List of groups

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | List of groups | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**userCount** | decimal.Decimal, int,  | decimal.Decimal,  | The number of users belonging to the group | value must be a 32 bit integer
**id** | str,  | str,  |  | 
**[workspaces](#workspaces)** | list, tuple,  | tuple,  |  | 
**[dataSources](#dataSources)** | list, tuple,  | tuple,  |  | 
**organizationAdmin** | bool,  | BoolClass,  | Is group organization admin | 
**name** | str,  | str,  | Group name | [optional] 
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

