# PopMeasureDefinition


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**previous_period_measure** | [**PopDatasetMeasureDefinitionPreviousPeriodMeasure**](PopDatasetMeasureDefinitionPreviousPeriodMeasure.md) |  | 
**over_period_measure** | [**PopDateMeasureDefinitionOverPeriodMeasure**](PopDateMeasureDefinitionOverPeriodMeasure.md) |  | 

## Example

```python
from gooddata_api_client.models.pop_measure_definition import PopMeasureDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of PopMeasureDefinition from a JSON string
pop_measure_definition_instance = PopMeasureDefinition.from_json(json)
# print the JSON string representation of the object
print(PopMeasureDefinition.to_json())

# convert the object into a dict
pop_measure_definition_dict = pop_measure_definition_instance.to_dict()
# create an instance of PopMeasureDefinition from a dict
pop_measure_definition_from_dict = PopMeasureDefinition.from_dict(pop_measure_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


