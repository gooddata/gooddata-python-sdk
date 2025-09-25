# SimpleMeasureDefinition

Metric defined by referencing a MAQL metric or an LDM fact object with aggregation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure** | [**SimpleMeasureDefinitionMeasure**](SimpleMeasureDefinitionMeasure.md) |  | 

## Example

```python
from gooddata_api_client.models.simple_measure_definition import SimpleMeasureDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of SimpleMeasureDefinition from a JSON string
simple_measure_definition_instance = SimpleMeasureDefinition.from_json(json)
# print the JSON string representation of the object
print(SimpleMeasureDefinition.to_json())

# convert the object into a dict
simple_measure_definition_dict = simple_measure_definition_instance.to_dict()
# create an instance of SimpleMeasureDefinition from a dict
simple_measure_definition_from_dict = SimpleMeasureDefinition.from_dict(simple_measure_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


