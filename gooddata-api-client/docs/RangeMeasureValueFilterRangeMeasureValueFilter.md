# RangeMeasureValueFilterRangeMeasureValueFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**dimensionality** | [**List[AfmIdentifier]**](AfmIdentifier.md) | References to the attributes to be used when filtering. | [optional] 
**var_from** | **float** |  | 
**local_identifier** | **str** |  | [optional] 
**measure** | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**operator** | **str** |  | 
**to** | **float** |  | 
**treat_null_values_as** | **float** | A value that will be substituted for null values in the metric for the comparisons. | [optional] 

## Example

```python
from gooddata_api_client.models.range_measure_value_filter_range_measure_value_filter import RangeMeasureValueFilterRangeMeasureValueFilter

# TODO update the JSON string below
json = "{}"
# create an instance of RangeMeasureValueFilterRangeMeasureValueFilter from a JSON string
range_measure_value_filter_range_measure_value_filter_instance = RangeMeasureValueFilterRangeMeasureValueFilter.from_json(json)
# print the JSON string representation of the object
print(RangeMeasureValueFilterRangeMeasureValueFilter.to_json())

# convert the object into a dict
range_measure_value_filter_range_measure_value_filter_dict = range_measure_value_filter_range_measure_value_filter_instance.to_dict()
# create an instance of RangeMeasureValueFilterRangeMeasureValueFilter from a dict
range_measure_value_filter_range_measure_value_filter_from_dict = RangeMeasureValueFilterRangeMeasureValueFilter.from_dict(range_measure_value_filter_range_measure_value_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


