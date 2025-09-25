# WorkspaceUserGroup

List of workspace groups

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** | Group name | [optional] 

## Example

```python
from gooddata_api_client.models.workspace_user_group import WorkspaceUserGroup

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceUserGroup from a JSON string
workspace_user_group_instance = WorkspaceUserGroup.from_json(json)
# print the JSON string representation of the object
print(WorkspaceUserGroup.to_json())

# convert the object into a dict
workspace_user_group_dict = workspace_user_group_instance.to_dict()
# create an instance of WorkspaceUserGroup from a dict
workspace_user_group_from_dict = WorkspaceUserGroup.from_dict(workspace_user_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


