# JsonApiWorkspaceOut

JSON:API representation of workspace entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiWorkspaceInAttributes**](JsonApiWorkspaceInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiWorkspaceOutMeta**](JsonApiWorkspaceOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiWorkspaceInRelationships**](JsonApiWorkspaceInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_out import JsonApiWorkspaceOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceOut from a JSON string
json_api_workspace_out_instance = JsonApiWorkspaceOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceOut.to_json())

# convert the object into a dict
json_api_workspace_out_dict = json_api_workspace_out_instance.to_dict()
# create an instance of JsonApiWorkspaceOut from a dict
json_api_workspace_out_from_dict = JsonApiWorkspaceOut.from_dict(json_api_workspace_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


