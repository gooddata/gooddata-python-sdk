# WorkspacePermissionAssignment

Workspace permission assignments

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee_identifier** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**hierarchy_permissions** | **List[str]** |  | [optional] 
**permissions** | **List[str]** |  | [optional] 

## Example

```python
from gooddata_api_client.models.workspace_permission_assignment import WorkspacePermissionAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspacePermissionAssignment from a JSON string
workspace_permission_assignment_instance = WorkspacePermissionAssignment.from_json(json)
# print the JSON string representation of the object
print(WorkspacePermissionAssignment.to_json())

# convert the object into a dict
workspace_permission_assignment_dict = workspace_permission_assignment_instance.to_dict()
# create an instance of WorkspacePermissionAssignment from a dict
workspace_permission_assignment_from_dict = WorkspacePermissionAssignment.from_dict(workspace_permission_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


