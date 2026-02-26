# gooddata_api_client.model.user_management_workspace_permission_assignment.UserManagementWorkspacePermissionAssignment

Workspace permission assignments for users and userGroups

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Workspace permission assignments for users and userGroups | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[permissions](#permissions)** | list, tuple,  | tuple,  |  | 
**id** | str,  | str,  |  | 
**[hierarchyPermissions](#hierarchyPermissions)** | list, tuple,  | tuple,  |  | 
**name** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# hierarchyPermissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["MANAGE", "ANALYZE", "EXPORT", "EXPORT_TABULAR", "EXPORT_PDF", "CREATE_AUTOMATION", "USE_AI_ASSISTANT", "WRITE_KNOWLEDGE_DOCUMENTS", "READ_KNOWLEDGE_DOCUMENTS", "CREATE_FILTER_VIEW", "VIEW", ] 

# permissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["MANAGE", "ANALYZE", "EXPORT", "EXPORT_TABULAR", "EXPORT_PDF", "CREATE_AUTOMATION", "USE_AI_ASSISTANT", "WRITE_KNOWLEDGE_DOCUMENTS", "READ_KNOWLEDGE_DOCUMENTS", "CREATE_FILTER_VIEW", "VIEW", ] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

