# JsonApiUserGroupPatch

JSON:API representation of patching userGroup entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserGroupInAttributes**](JsonApiUserGroupInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiUserGroupInRelationships**](JsonApiUserGroupInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_user_group_patch import JsonApiUserGroupPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserGroupPatch from a JSON string
json_api_user_group_patch_instance = JsonApiUserGroupPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserGroupPatch.to_json())

# convert the object into a dict
json_api_user_group_patch_dict = json_api_user_group_patch_instance.to_dict()
# create an instance of JsonApiUserGroupPatch from a dict
json_api_user_group_patch_from_dict = JsonApiUserGroupPatch.from_dict(json_api_user_group_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


