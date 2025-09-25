# AFMFiltersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comparison_measure_value_filter** | [**ComparisonMeasureValueFilterComparisonMeasureValueFilter**](ComparisonMeasureValueFilterComparisonMeasureValueFilter.md) |  | 
**range_measure_value_filter** | [**RangeMeasureValueFilterRangeMeasureValueFilter**](RangeMeasureValueFilterRangeMeasureValueFilter.md) |  | 
**ranking_filter** | [**RankingFilterRankingFilter**](RankingFilterRankingFilter.md) |  | 
**absolute_date_filter** | [**AbsoluteDateFilterAbsoluteDateFilter**](AbsoluteDateFilterAbsoluteDateFilter.md) |  | 
**relative_date_filter** | [**RelativeDateFilterRelativeDateFilter**](RelativeDateFilterRelativeDateFilter.md) |  | 
**negative_attribute_filter** | [**NegativeAttributeFilterNegativeAttributeFilter**](NegativeAttributeFilterNegativeAttributeFilter.md) |  | 
**positive_attribute_filter** | [**PositiveAttributeFilterPositiveAttributeFilter**](PositiveAttributeFilterPositiveAttributeFilter.md) |  | 
**inline** | [**InlineFilterDefinitionInline**](InlineFilterDefinitionInline.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_filters_inner import AFMFiltersInner

# TODO update the JSON string below
json = "{}"
# create an instance of AFMFiltersInner from a JSON string
afm_filters_inner_instance = AFMFiltersInner.from_json(json)
# print the JSON string representation of the object
print(AFMFiltersInner.to_json())

# convert the object into a dict
afm_filters_inner_dict = afm_filters_inner_instance.to_dict()
# create an instance of AFMFiltersInner from a dict
afm_filters_inner_from_dict = AFMFiltersInner.from_dict(afm_filters_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


