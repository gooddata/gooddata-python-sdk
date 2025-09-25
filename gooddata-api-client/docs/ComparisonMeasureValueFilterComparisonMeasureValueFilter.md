# ComparisonMeasureValueFilterComparisonMeasureValueFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**dimensionality** | [**List[AfmIdentifier]**](AfmIdentifier.md) | References to the attributes to be used when filtering. | [optional] 
**local_identifier** | **str** |  | [optional] 
**measure** | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**operator** | **str** |  | 
**treat_null_values_as** | **float** | A value that will be substituted for null values in the metric for the comparisons. | [optional] 
**value** | **float** |  | 

## Example

```python
from gooddata_api_client.models.comparison_measure_value_filter_comparison_measure_value_filter import ComparisonMeasureValueFilterComparisonMeasureValueFilter

# TODO update the JSON string below
json = "{}"
# create an instance of ComparisonMeasureValueFilterComparisonMeasureValueFilter from a JSON string
comparison_measure_value_filter_comparison_measure_value_filter_instance = ComparisonMeasureValueFilterComparisonMeasureValueFilter.from_json(json)
# print the JSON string representation of the object
print(ComparisonMeasureValueFilterComparisonMeasureValueFilter.to_json())

# convert the object into a dict
comparison_measure_value_filter_comparison_measure_value_filter_dict = comparison_measure_value_filter_comparison_measure_value_filter_instance.to_dict()
# create an instance of ComparisonMeasureValueFilterComparisonMeasureValueFilter from a dict
comparison_measure_value_filter_comparison_measure_value_filter_from_dict = ComparisonMeasureValueFilterComparisonMeasureValueFilter.from_dict(comparison_measure_value_filter_comparison_measure_value_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


