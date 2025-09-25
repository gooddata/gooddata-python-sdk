# JsonApiWorkspaceIn

JSON:API representation of workspace entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiWorkspaceInAttributes**](JsonApiWorkspaceInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiWorkspaceInRelationships**](JsonApiWorkspaceInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_in import JsonApiWorkspaceIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceIn from a JSON string
json_api_workspace_in_instance = JsonApiWorkspaceIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceIn.to_json())

# convert the object into a dict
json_api_workspace_in_dict = json_api_workspace_in_instance.to_dict()
# create an instance of JsonApiWorkspaceIn from a dict
json_api_workspace_in_from_dict = JsonApiWorkspaceIn.from_dict(json_api_workspace_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


