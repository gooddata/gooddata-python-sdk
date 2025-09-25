# FilterDefinition

Abstract filter definition type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inline** | [**InlineFilterDefinitionInline**](InlineFilterDefinitionInline.md) |  | 
**ranking_filter** | [**RankingFilterRankingFilter**](RankingFilterRankingFilter.md) |  | 
**comparison_measure_value_filter** | [**ComparisonMeasureValueFilterComparisonMeasureValueFilter**](ComparisonMeasureValueFilterComparisonMeasureValueFilter.md) |  | 
**range_measure_value_filter** | [**RangeMeasureValueFilterRangeMeasureValueFilter**](RangeMeasureValueFilterRangeMeasureValueFilter.md) |  | 
**absolute_date_filter** | [**AbsoluteDateFilterAbsoluteDateFilter**](AbsoluteDateFilterAbsoluteDateFilter.md) |  | 
**relative_date_filter** | [**RelativeDateFilterRelativeDateFilter**](RelativeDateFilterRelativeDateFilter.md) |  | 
**negative_attribute_filter** | [**NegativeAttributeFilterNegativeAttributeFilter**](NegativeAttributeFilterNegativeAttributeFilter.md) |  | 
**positive_attribute_filter** | [**PositiveAttributeFilterPositiveAttributeFilter**](PositiveAttributeFilterPositiveAttributeFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.filter_definition import FilterDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of FilterDefinition from a JSON string
filter_definition_instance = FilterDefinition.from_json(json)
# print the JSON string representation of the object
print(FilterDefinition.to_json())

# convert the object into a dict
filter_definition_dict = filter_definition_instance.to_dict()
# create an instance of FilterDefinition from a dict
filter_definition_from_dict = FilterDefinition.from_dict(filter_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


