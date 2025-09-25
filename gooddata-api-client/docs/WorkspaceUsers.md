# WorkspaceUsers


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_count** | **int** | The total number of users is based on applied filters. | 
**users** | [**List[WorkspaceUser]**](WorkspaceUser.md) |  | 

## Example

```python
from gooddata_api_client.models.workspace_users import WorkspaceUsers

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceUsers from a JSON string
workspace_users_instance = WorkspaceUsers.from_json(json)
# print the JSON string representation of the object
print(WorkspaceUsers.to_json())

# convert the object into a dict
workspace_users_dict = workspace_users_instance.to_dict()
# create an instance of WorkspaceUsers from a dict
workspace_users_from_dict = WorkspaceUsers.from_dict(workspace_users_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


