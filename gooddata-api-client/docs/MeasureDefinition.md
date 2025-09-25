# MeasureDefinition

Abstract metric definition type

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inline** | [**InlineMeasureDefinitionInline**](InlineMeasureDefinitionInline.md) |  | 
**arithmetic_measure** | [**ArithmeticMeasureDefinitionArithmeticMeasure**](ArithmeticMeasureDefinitionArithmeticMeasure.md) |  | 
**measure** | [**SimpleMeasureDefinitionMeasure**](SimpleMeasureDefinitionMeasure.md) |  | 
**previous_period_measure** | [**PopDatasetMeasureDefinitionPreviousPeriodMeasure**](PopDatasetMeasureDefinitionPreviousPeriodMeasure.md) |  | 
**over_period_measure** | [**PopDateMeasureDefinitionOverPeriodMeasure**](PopDateMeasureDefinitionOverPeriodMeasure.md) |  | 

## Example

```python
from gooddata_api_client.models.measure_definition import MeasureDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureDefinition from a JSON string
measure_definition_instance = MeasureDefinition.from_json(json)
# print the JSON string representation of the object
print(MeasureDefinition.to_json())

# convert the object into a dict
measure_definition_dict = measure_definition_instance.to_dict()
# create an instance of MeasureDefinition from a dict
measure_definition_from_dict = MeasureDefinition.from_dict(measure_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


