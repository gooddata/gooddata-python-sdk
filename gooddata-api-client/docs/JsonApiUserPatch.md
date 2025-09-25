# JsonApiUserPatch

JSON:API representation of patching user entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserInAttributes**](JsonApiUserInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiUserInRelationships**](JsonApiUserInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_user_patch import JsonApiUserPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserPatch from a JSON string
json_api_user_patch_instance = JsonApiUserPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserPatch.to_json())

# convert the object into a dict
json_api_user_patch_dict = json_api_user_patch_instance.to_dict()
# create an instance of JsonApiUserPatch from a dict
json_api_user_patch_from_dict = JsonApiUserPatch.from_dict(json_api_user_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


