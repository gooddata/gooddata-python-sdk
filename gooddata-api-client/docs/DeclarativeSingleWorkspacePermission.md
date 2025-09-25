# DeclarativeSingleWorkspacePermission


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**name** | **str** | Permission name. | 

## Example

```python
from gooddata_api_client.models.declarative_single_workspace_permission import DeclarativeSingleWorkspacePermission

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeSingleWorkspacePermission from a JSON string
declarative_single_workspace_permission_instance = DeclarativeSingleWorkspacePermission.from_json(json)
# print the JSON string representation of the object
print(DeclarativeSingleWorkspacePermission.to_json())

# convert the object into a dict
declarative_single_workspace_permission_dict = declarative_single_workspace_permission_instance.to_dict()
# create an instance of DeclarativeSingleWorkspacePermission from a dict
declarative_single_workspace_permission_from_dict = DeclarativeSingleWorkspacePermission.from_dict(declarative_single_workspace_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


