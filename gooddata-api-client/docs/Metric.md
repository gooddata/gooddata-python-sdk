# Metric

List of metrics to be used in the new visualization

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agg_function** | **str** | Agg function. Empty if a stored metric is used. | [optional] 
**id** | **str** | ID of the object | 
**title** | **str** | Title of metric. | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.metric import Metric

# TODO update the JSON string below
json = "{}"
# create an instance of Metric from a JSON string
metric_instance = Metric.from_json(json)
# print the JSON string representation of the object
print(Metric.to_json())

# convert the object into a dict
metric_dict = metric_instance.to_dict()
# create an instance of Metric from a dict
metric_from_dict = Metric.from_dict(metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


