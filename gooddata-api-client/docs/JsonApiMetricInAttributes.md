# JsonApiMetricInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | [**JsonApiMetricInAttributesContent**](JsonApiMetricInAttributesContent.md) |  | 
**description** | **str** |  | [optional] 
**is_hidden** | **bool** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_metric_in_attributes import JsonApiMetricInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricInAttributes from a JSON string
json_api_metric_in_attributes_instance = JsonApiMetricInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricInAttributes.to_json())

# convert the object into a dict
json_api_metric_in_attributes_dict = json_api_metric_in_attributes_instance.to_dict()
# create an instance of JsonApiMetricInAttributes from a dict
json_api_metric_in_attributes_from_dict = JsonApiMetricInAttributes.from_dict(json_api_metric_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


