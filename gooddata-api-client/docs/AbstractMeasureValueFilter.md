# AbstractMeasureValueFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comparison_measure_value_filter** | [**ComparisonMeasureValueFilterComparisonMeasureValueFilter**](ComparisonMeasureValueFilterComparisonMeasureValueFilter.md) |  | 
**range_measure_value_filter** | [**RangeMeasureValueFilterRangeMeasureValueFilter**](RangeMeasureValueFilterRangeMeasureValueFilter.md) |  | 
**ranking_filter** | [**RankingFilterRankingFilter**](RankingFilterRankingFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.abstract_measure_value_filter import AbstractMeasureValueFilter

# TODO update the JSON string below
json = "{}"
# create an instance of AbstractMeasureValueFilter from a JSON string
abstract_measure_value_filter_instance = AbstractMeasureValueFilter.from_json(json)
# print the JSON string representation of the object
print(AbstractMeasureValueFilter.to_json())

# convert the object into a dict
abstract_measure_value_filter_dict = abstract_measure_value_filter_instance.to_dict()
# create an instance of AbstractMeasureValueFilter from a dict
abstract_measure_value_filter_from_dict = AbstractMeasureValueFilter.from_dict(abstract_measure_value_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


