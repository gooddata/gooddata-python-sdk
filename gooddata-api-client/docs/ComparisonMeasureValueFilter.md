# ComparisonMeasureValueFilter

Filter the result by comparing specified metric to given constant value, using given comparison operator.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comparison_measure_value_filter** | [**ComparisonMeasureValueFilterComparisonMeasureValueFilter**](ComparisonMeasureValueFilterComparisonMeasureValueFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.comparison_measure_value_filter import ComparisonMeasureValueFilter

# TODO update the JSON string below
json = "{}"
# create an instance of ComparisonMeasureValueFilter from a JSON string
comparison_measure_value_filter_instance = ComparisonMeasureValueFilter.from_json(json)
# print the JSON string representation of the object
print(ComparisonMeasureValueFilter.to_json())

# convert the object into a dict
comparison_measure_value_filter_dict = comparison_measure_value_filter_instance.to_dict()
# create an instance of ComparisonMeasureValueFilter from a dict
comparison_measure_value_filter_from_dict = ComparisonMeasureValueFilter.from_dict(comparison_measure_value_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


