# MetricRecord


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**formatted_value** | **str** |  | [optional] 
**value** | **float** |  | 

## Example

```python
from gooddata_api_client.models.metric_record import MetricRecord

# TODO update the JSON string below
json = "{}"
# create an instance of MetricRecord from a JSON string
metric_record_instance = MetricRecord.from_json(json)
# print the JSON string representation of the object
print(MetricRecord.to_json())

# convert the object into a dict
metric_record_dict = metric_record_instance.to_dict()
# create an instance of MetricRecord from a dict
metric_record_from_dict = MetricRecord.from_dict(metric_record_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


