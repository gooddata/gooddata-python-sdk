# JsonApiFilterViewPatch

JSON:API representation of patching filterView entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiFilterViewPatchAttributes**](JsonApiFilterViewPatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiFilterViewInRelationships**](JsonApiFilterViewInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_filter_view_patch import JsonApiFilterViewPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewPatch from a JSON string
json_api_filter_view_patch_instance = JsonApiFilterViewPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewPatch.to_json())

# convert the object into a dict
json_api_filter_view_patch_dict = json_api_filter_view_patch_instance.to_dict()
# create an instance of JsonApiFilterViewPatch from a dict
json_api_filter_view_patch_from_dict = JsonApiFilterViewPatch.from_dict(json_api_filter_view_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


