# ArithmeticMeasureDefinitionArithmeticMeasure


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure_identifiers** | [**List[AfmLocalIdentifier]**](AfmLocalIdentifier.md) | List of metrics to apply arithmetic operation by chosen operator. | 
**operator** | **str** | Arithmetic operator describing operation between metrics. | 

## Example

```python
from gooddata_api_client.models.arithmetic_measure_definition_arithmetic_measure import ArithmeticMeasureDefinitionArithmeticMeasure

# TODO update the JSON string below
json = "{}"
# create an instance of ArithmeticMeasureDefinitionArithmeticMeasure from a JSON string
arithmetic_measure_definition_arithmetic_measure_instance = ArithmeticMeasureDefinitionArithmeticMeasure.from_json(json)
# print the JSON string representation of the object
print(ArithmeticMeasureDefinitionArithmeticMeasure.to_json())

# convert the object into a dict
arithmetic_measure_definition_arithmetic_measure_dict = arithmetic_measure_definition_arithmetic_measure_instance.to_dict()
# create an instance of ArithmeticMeasureDefinitionArithmeticMeasure from a dict
arithmetic_measure_definition_arithmetic_measure_from_dict = ArithmeticMeasureDefinitionArithmeticMeasure.from_dict(arithmetic_measure_definition_arithmetic_measure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


