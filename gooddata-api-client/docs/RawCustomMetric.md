# RawCustomMetric

Custom metric object override.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Metric title override. | 

## Example

```python
from gooddata_api_client.models.raw_custom_metric import RawCustomMetric

# TODO update the JSON string below
json = "{}"
# create an instance of RawCustomMetric from a JSON string
raw_custom_metric_instance = RawCustomMetric.from_json(json)
# print the JSON string representation of the object
print(RawCustomMetric.to_json())

# convert the object into a dict
raw_custom_metric_dict = raw_custom_metric_instance.to_dict()
# create an instance of RawCustomMetric from a dict
raw_custom_metric_from_dict = RawCustomMetric.from_dict(raw_custom_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


