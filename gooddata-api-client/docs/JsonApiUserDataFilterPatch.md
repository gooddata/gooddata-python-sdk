# JsonApiUserDataFilterPatch

JSON:API representation of patching userDataFilter entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserDataFilterPatchAttributes**](JsonApiUserDataFilterPatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiUserDataFilterInRelationships**](JsonApiUserDataFilterInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_patch import JsonApiUserDataFilterPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterPatch from a JSON string
json_api_user_data_filter_patch_instance = JsonApiUserDataFilterPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterPatch.to_json())

# convert the object into a dict
json_api_user_data_filter_patch_dict = json_api_user_data_filter_patch_instance.to_dict()
# create an instance of JsonApiUserDataFilterPatch from a dict
json_api_user_data_filter_patch_from_dict = JsonApiUserDataFilterPatch.from_dict(json_api_user_data_filter_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


