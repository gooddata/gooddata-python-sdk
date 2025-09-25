# CustomMetric

Custom metric object override.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | **str** | Format override. | 
**title** | **str** | Metric title override. | 

## Example

```python
from gooddata_api_client.models.custom_metric import CustomMetric

# TODO update the JSON string below
json = "{}"
# create an instance of CustomMetric from a JSON string
custom_metric_instance = CustomMetric.from_json(json)
# print the JSON string representation of the object
print(CustomMetric.to_json())

# convert the object into a dict
custom_metric_dict = custom_metric_instance.to_dict()
# create an instance of CustomMetric from a dict
custom_metric_from_dict = CustomMetric.from_dict(custom_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


