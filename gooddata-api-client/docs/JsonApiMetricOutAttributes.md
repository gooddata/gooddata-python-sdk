# JsonApiMetricOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | [**JsonApiMetricInAttributesContent**](JsonApiMetricInAttributesContent.md) |  | 
**created_at** | **datetime** |  | [optional] 
**description** | **str** |  | [optional] 
**is_hidden** | **bool** |  | [optional] 
**modified_at** | **datetime** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_metric_out_attributes import JsonApiMetricOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricOutAttributes from a JSON string
json_api_metric_out_attributes_instance = JsonApiMetricOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricOutAttributes.to_json())

# convert the object into a dict
json_api_metric_out_attributes_dict = json_api_metric_out_attributes_instance.to_dict()
# create an instance of JsonApiMetricOutAttributes from a dict
json_api_metric_out_attributes_from_dict = JsonApiMetricOutAttributes.from_dict(json_api_metric_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


