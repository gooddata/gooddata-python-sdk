# MeasureItemDefinition


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**arithmetic_measure** | [**ArithmeticMeasureDefinitionArithmeticMeasure**](ArithmeticMeasureDefinitionArithmeticMeasure.md) |  | 
**inline** | [**InlineMeasureDefinitionInline**](InlineMeasureDefinitionInline.md) |  | 
**previous_period_measure** | [**PopDatasetMeasureDefinitionPreviousPeriodMeasure**](PopDatasetMeasureDefinitionPreviousPeriodMeasure.md) |  | 
**over_period_measure** | [**PopDateMeasureDefinitionOverPeriodMeasure**](PopDateMeasureDefinitionOverPeriodMeasure.md) |  | 
**measure** | [**SimpleMeasureDefinitionMeasure**](SimpleMeasureDefinitionMeasure.md) |  | 

## Example

```python
from gooddata_api_client.models.measure_item_definition import MeasureItemDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureItemDefinition from a JSON string
measure_item_definition_instance = MeasureItemDefinition.from_json(json)
# print the JSON string representation of the object
print(MeasureItemDefinition.to_json())

# convert the object into a dict
measure_item_definition_dict = measure_item_definition_instance.to_dict()
# create an instance of MeasureItemDefinition from a dict
measure_item_definition_from_dict = MeasureItemDefinition.from_dict(measure_item_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


