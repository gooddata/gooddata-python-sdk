# MeasureValueFilter

Abstract filter definition type filtering by the value of the metric.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comparison_measure_value_filter** | [**ComparisonMeasureValueFilterComparisonMeasureValueFilter**](ComparisonMeasureValueFilterComparisonMeasureValueFilter.md) |  | 
**range_measure_value_filter** | [**RangeMeasureValueFilterRangeMeasureValueFilter**](RangeMeasureValueFilterRangeMeasureValueFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.measure_value_filter import MeasureValueFilter

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureValueFilter from a JSON string
measure_value_filter_instance = MeasureValueFilter.from_json(json)
# print the JSON string representation of the object
print(MeasureValueFilter.to_json())

# convert the object into a dict
measure_value_filter_dict = measure_value_filter_instance.to_dict()
# create an instance of MeasureValueFilter from a dict
measure_value_filter_from_dict = MeasureValueFilter.from_dict(measure_value_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


