# FilterDefinitionForSimpleMeasure

Abstract filter definition type for simple metric.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**absolute_date_filter** | [**AbsoluteDateFilterAbsoluteDateFilter**](AbsoluteDateFilterAbsoluteDateFilter.md) |  | 
**relative_date_filter** | [**RelativeDateFilterRelativeDateFilter**](RelativeDateFilterRelativeDateFilter.md) |  | 
**negative_attribute_filter** | [**NegativeAttributeFilterNegativeAttributeFilter**](NegativeAttributeFilterNegativeAttributeFilter.md) |  | 
**positive_attribute_filter** | [**PositiveAttributeFilterPositiveAttributeFilter**](PositiveAttributeFilterPositiveAttributeFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.filter_definition_for_simple_measure import FilterDefinitionForSimpleMeasure

# TODO update the JSON string below
json = "{}"
# create an instance of FilterDefinitionForSimpleMeasure from a JSON string
filter_definition_for_simple_measure_instance = FilterDefinitionForSimpleMeasure.from_json(json)
# print the JSON string representation of the object
print(FilterDefinitionForSimpleMeasure.to_json())

# convert the object into a dict
filter_definition_for_simple_measure_dict = filter_definition_for_simple_measure_instance.to_dict()
# create an instance of FilterDefinitionForSimpleMeasure from a dict
filter_definition_for_simple_measure_from_dict = FilterDefinitionForSimpleMeasure.from_dict(filter_definition_for_simple_measure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


