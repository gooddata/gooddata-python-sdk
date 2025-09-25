# RangeMeasureValueFilter

Filter the result by comparing specified metric to given range of values.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**range_measure_value_filter** | [**RangeMeasureValueFilterRangeMeasureValueFilter**](RangeMeasureValueFilterRangeMeasureValueFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.range_measure_value_filter import RangeMeasureValueFilter

# TODO update the JSON string below
json = "{}"
# create an instance of RangeMeasureValueFilter from a JSON string
range_measure_value_filter_instance = RangeMeasureValueFilter.from_json(json)
# print the JSON string representation of the object
print(RangeMeasureValueFilter.to_json())

# convert the object into a dict
range_measure_value_filter_dict = range_measure_value_filter_instance.to_dict()
# create an instance of RangeMeasureValueFilter from a dict
range_measure_value_filter_from_dict = RangeMeasureValueFilter.from_dict(range_measure_value_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


