# JsonApiMetricIn

JSON:API representation of metric entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiMetricInAttributes**](JsonApiMetricInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_metric_in import JsonApiMetricIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricIn from a JSON string
json_api_metric_in_instance = JsonApiMetricIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricIn.to_json())

# convert the object into a dict
json_api_metric_in_dict = json_api_metric_in_instance.to_dict()
# create an instance of JsonApiMetricIn from a dict
json_api_metric_in_from_dict = JsonApiMetricIn.from_dict(json_api_metric_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


