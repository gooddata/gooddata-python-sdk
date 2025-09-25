# PermissionsAssignment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignees** | [**List[AssigneeIdentifier]**](AssigneeIdentifier.md) |  | 
**data_sources** | [**List[UserManagementDataSourcePermissionAssignment]**](UserManagementDataSourcePermissionAssignment.md) |  | [optional] 
**workspaces** | [**List[UserManagementWorkspacePermissionAssignment]**](UserManagementWorkspacePermissionAssignment.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.permissions_assignment import PermissionsAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of PermissionsAssignment from a JSON string
permissions_assignment_instance = PermissionsAssignment.from_json(json)
# print the JSON string representation of the object
print(PermissionsAssignment.to_json())

# convert the object into a dict
permissions_assignment_dict = permissions_assignment_instance.to_dict()
# create an instance of PermissionsAssignment from a dict
permissions_assignment_from_dict = PermissionsAssignment.from_dict(permissions_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


