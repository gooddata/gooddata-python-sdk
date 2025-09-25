# PopDateMeasureDefinition

Period over period type of metric.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**over_period_measure** | [**PopDateMeasureDefinitionOverPeriodMeasure**](PopDateMeasureDefinitionOverPeriodMeasure.md) |  | 

## Example

```python
from gooddata_api_client.models.pop_date_measure_definition import PopDateMeasureDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of PopDateMeasureDefinition from a JSON string
pop_date_measure_definition_instance = PopDateMeasureDefinition.from_json(json)
# print the JSON string representation of the object
print(PopDateMeasureDefinition.to_json())

# convert the object into a dict
pop_date_measure_definition_dict = pop_date_measure_definition_instance.to_dict()
# create an instance of PopDateMeasureDefinition from a dict
pop_date_measure_definition_from_dict = PopDateMeasureDefinition.from_dict(pop_date_measure_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


