# UserManagementWorkspacePermissionAssignment

Workspace permission assignments for users and userGroups

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hierarchy_permissions** | **List[str]** |  | 
**id** | **str** |  | 
**name** | **str** |  | [optional] [readonly] 
**permissions** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.user_management_workspace_permission_assignment import UserManagementWorkspacePermissionAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementWorkspacePermissionAssignment from a JSON string
user_management_workspace_permission_assignment_instance = UserManagementWorkspacePermissionAssignment.from_json(json)
# print the JSON string representation of the object
print(UserManagementWorkspacePermissionAssignment.to_json())

# convert the object into a dict
user_management_workspace_permission_assignment_dict = user_management_workspace_permission_assignment_instance.to_dict()
# create an instance of UserManagementWorkspacePermissionAssignment from a dict
user_management_workspace_permission_assignment_from_dict = UserManagementWorkspacePermissionAssignment.from_dict(user_management_workspace_permission_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


