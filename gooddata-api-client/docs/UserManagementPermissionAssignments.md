# UserManagementPermissionAssignments


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sources** | [**List[UserManagementDataSourcePermissionAssignment]**](UserManagementDataSourcePermissionAssignment.md) |  | 
**workspaces** | [**List[UserManagementWorkspacePermissionAssignment]**](UserManagementWorkspacePermissionAssignment.md) |  | 

## Example

```python
from gooddata_api_client.models.user_management_permission_assignments import UserManagementPermissionAssignments

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementPermissionAssignments from a JSON string
user_management_permission_assignments_instance = UserManagementPermissionAssignments.from_json(json)
# print the JSON string representation of the object
print(UserManagementPermissionAssignments.to_json())

# convert the object into a dict
user_management_permission_assignments_dict = user_management_permission_assignments_instance.to_dict()
# create an instance of UserManagementPermissionAssignments from a dict
user_management_permission_assignments_from_dict = UserManagementPermissionAssignments.from_dict(user_management_permission_assignments_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


