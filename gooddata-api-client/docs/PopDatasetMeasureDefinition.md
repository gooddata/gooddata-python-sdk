# PopDatasetMeasureDefinition

Previous period type of metric.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**previous_period_measure** | [**PopDatasetMeasureDefinitionPreviousPeriodMeasure**](PopDatasetMeasureDefinitionPreviousPeriodMeasure.md) |  | 

## Example

```python
from gooddata_api_client.models.pop_dataset_measure_definition import PopDatasetMeasureDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of PopDatasetMeasureDefinition from a JSON string
pop_dataset_measure_definition_instance = PopDatasetMeasureDefinition.from_json(json)
# print the JSON string representation of the object
print(PopDatasetMeasureDefinition.to_json())

# convert the object into a dict
pop_dataset_measure_definition_dict = pop_dataset_measure_definition_instance.to_dict()
# create an instance of PopDatasetMeasureDefinition from a dict
pop_dataset_measure_definition_from_dict = PopDatasetMeasureDefinition.from_dict(pop_dataset_measure_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


