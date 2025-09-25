# WorkspaceUserGroups


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_count** | **int** | Total number of groups | 
**user_groups** | [**List[WorkspaceUserGroup]**](WorkspaceUserGroup.md) |  | 

## Example

```python
from gooddata_api_client.models.workspace_user_groups import WorkspaceUserGroups

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceUserGroups from a JSON string
workspace_user_groups_instance = WorkspaceUserGroups.from_json(json)
# print the JSON string representation of the object
print(WorkspaceUserGroups.to_json())

# convert the object into a dict
workspace_user_groups_dict = workspace_user_groups_instance.to_dict()
# create an instance of WorkspaceUserGroups from a dict
workspace_user_groups_from_dict = WorkspaceUserGroups.from_dict(workspace_user_groups_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


