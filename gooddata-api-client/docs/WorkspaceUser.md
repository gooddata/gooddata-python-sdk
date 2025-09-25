# WorkspaceUser

List of workspace users

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | User email address | [optional] 
**id** | **str** |  | 
**name** | **str** | User name | [optional] 

## Example

```python
from gooddata_api_client.models.workspace_user import WorkspaceUser

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceUser from a JSON string
workspace_user_instance = WorkspaceUser.from_json(json)
# print the JSON string representation of the object
print(WorkspaceUser.to_json())

# convert the object into a dict
workspace_user_dict = workspace_user_instance.to_dict()
# create an instance of WorkspaceUser from a dict
workspace_user_from_dict = WorkspaceUser.from_dict(workspace_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


