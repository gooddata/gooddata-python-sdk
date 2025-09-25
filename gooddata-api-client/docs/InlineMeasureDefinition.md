# InlineMeasureDefinition

Metric defined by the raw MAQL query.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inline** | [**InlineMeasureDefinitionInline**](InlineMeasureDefinitionInline.md) |  | 

## Example

```python
from gooddata_api_client.models.inline_measure_definition import InlineMeasureDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of InlineMeasureDefinition from a JSON string
inline_measure_definition_instance = InlineMeasureDefinition.from_json(json)
# print the JSON string representation of the object
print(InlineMeasureDefinition.to_json())

# convert the object into a dict
inline_measure_definition_dict = inline_measure_definition_instance.to_dict()
# create an instance of InlineMeasureDefinition from a dict
inline_measure_definition_from_dict = InlineMeasureDefinition.from_dict(inline_measure_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


