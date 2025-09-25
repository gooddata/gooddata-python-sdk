# ArithmeticMeasure


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**left** | [**LocalIdentifier**](LocalIdentifier.md) |  | 
**operator** | **str** | Arithmetic operator. DIFFERENCE - m₁−m₂ - the difference between two metrics. CHANGE - (m₁−m₂)÷m₂ - the relative difference between two metrics.  | 
**right** | [**LocalIdentifier**](LocalIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.arithmetic_measure import ArithmeticMeasure

# TODO update the JSON string below
json = "{}"
# create an instance of ArithmeticMeasure from a JSON string
arithmetic_measure_instance = ArithmeticMeasure.from_json(json)
# print the JSON string representation of the object
print(ArithmeticMeasure.to_json())

# convert the object into a dict
arithmetic_measure_dict = arithmetic_measure_instance.to_dict()
# create an instance of ArithmeticMeasure from a dict
arithmetic_measure_from_dict = ArithmeticMeasure.from_dict(arithmetic_measure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


