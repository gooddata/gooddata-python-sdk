# JsonApiMetricOut

JSON:API representation of metric entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiMetricOutAttributes**](JsonApiMetricOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiMetricOutRelationships**](JsonApiMetricOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_metric_out import JsonApiMetricOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricOut from a JSON string
json_api_metric_out_instance = JsonApiMetricOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricOut.to_json())

# convert the object into a dict
json_api_metric_out_dict = json_api_metric_out_instance.to_dict()
# create an instance of JsonApiMetricOut from a dict
json_api_metric_out_from_dict = JsonApiMetricOut.from_dict(json_api_metric_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


