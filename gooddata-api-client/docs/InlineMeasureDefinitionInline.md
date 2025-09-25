# InlineMeasureDefinitionInline


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**maql** | **str** | MAQL query defining the metric. | 

## Example

```python
from gooddata_api_client.models.inline_measure_definition_inline import InlineMeasureDefinitionInline

# TODO update the JSON string below
json = "{}"
# create an instance of InlineMeasureDefinitionInline from a JSON string
inline_measure_definition_inline_instance = InlineMeasureDefinitionInline.from_json(json)
# print the JSON string representation of the object
print(InlineMeasureDefinitionInline.to_json())

# convert the object into a dict
inline_measure_definition_inline_dict = inline_measure_definition_inline_instance.to_dict()
# create an instance of InlineMeasureDefinitionInline from a dict
inline_measure_definition_inline_from_dict = InlineMeasureDefinitionInline.from_dict(inline_measure_definition_inline_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


