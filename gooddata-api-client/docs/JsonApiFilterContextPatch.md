# JsonApiFilterContextPatch

JSON:API representation of patching filterContext entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardPatchAttributes**](JsonApiAnalyticalDashboardPatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_filter_context_patch import JsonApiFilterContextPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterContextPatch from a JSON string
json_api_filter_context_patch_instance = JsonApiFilterContextPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterContextPatch.to_json())

# convert the object into a dict
json_api_filter_context_patch_dict = json_api_filter_context_patch_instance.to_dict()
# create an instance of JsonApiFilterContextPatch from a dict
json_api_filter_context_patch_from_dict = JsonApiFilterContextPatch.from_dict(json_api_filter_context_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


