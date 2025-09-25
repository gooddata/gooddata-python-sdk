# JsonApiMetricPatchAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | [**JsonApiMetricInAttributesContent**](JsonApiMetricInAttributesContent.md) |  | [optional] 
**description** | **str** |  | [optional] 
**is_hidden** | **bool** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_metric_patch_attributes import JsonApiMetricPatchAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricPatchAttributes from a JSON string
json_api_metric_patch_attributes_instance = JsonApiMetricPatchAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricPatchAttributes.to_json())

# convert the object into a dict
json_api_metric_patch_attributes_dict = json_api_metric_patch_attributes_instance.to_dict()
# create an instance of JsonApiMetricPatchAttributes from a dict
json_api_metric_patch_attributes_from_dict = JsonApiMetricPatchAttributes.from_dict(json_api_metric_patch_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


