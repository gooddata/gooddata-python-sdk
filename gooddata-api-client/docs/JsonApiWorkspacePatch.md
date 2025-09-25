# JsonApiWorkspacePatch

JSON:API representation of patching workspace entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiWorkspaceInAttributes**](JsonApiWorkspaceInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiWorkspaceInRelationships**](JsonApiWorkspaceInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_patch import JsonApiWorkspacePatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspacePatch from a JSON string
json_api_workspace_patch_instance = JsonApiWorkspacePatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspacePatch.to_json())

# convert the object into a dict
json_api_workspace_patch_dict = json_api_workspace_patch_instance.to_dict()
# create an instance of JsonApiWorkspacePatch from a dict
json_api_workspace_patch_from_dict = JsonApiWorkspacePatch.from_dict(json_api_workspace_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


