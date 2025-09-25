# JsonApiMetricPatch

JSON:API representation of patching metric entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiMetricPatchAttributes**](JsonApiMetricPatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_metric_patch import JsonApiMetricPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricPatch from a JSON string
json_api_metric_patch_instance = JsonApiMetricPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricPatch.to_json())

# convert the object into a dict
json_api_metric_patch_dict = json_api_metric_patch_instance.to_dict()
# create an instance of JsonApiMetricPatch from a dict
json_api_metric_patch_from_dict = JsonApiMetricPatch.from_dict(json_api_metric_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


