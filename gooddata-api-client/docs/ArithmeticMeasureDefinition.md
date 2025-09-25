# ArithmeticMeasureDefinition

Metric representing arithmetics between other metrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**arithmetic_measure** | [**ArithmeticMeasureDefinitionArithmeticMeasure**](ArithmeticMeasureDefinitionArithmeticMeasure.md) |  | 

## Example

```python
from gooddata_api_client.models.arithmetic_measure_definition import ArithmeticMeasureDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of ArithmeticMeasureDefinition from a JSON string
arithmetic_measure_definition_instance = ArithmeticMeasureDefinition.from_json(json)
# print the JSON string representation of the object
print(ArithmeticMeasureDefinition.to_json())

# convert the object into a dict
arithmetic_measure_definition_dict = arithmetic_measure_definition_instance.to_dict()
# create an instance of ArithmeticMeasureDefinition from a dict
arithmetic_measure_definition_from_dict = ArithmeticMeasureDefinition.from_dict(arithmetic_measure_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


