# InlineFilterDefinition

Filter in form of direct MAQL query.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inline** | [**InlineFilterDefinitionInline**](InlineFilterDefinitionInline.md) |  | 

## Example

```python
from gooddata_api_client.models.inline_filter_definition import InlineFilterDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of InlineFilterDefinition from a JSON string
inline_filter_definition_instance = InlineFilterDefinition.from_json(json)
# print the JSON string representation of the object
print(InlineFilterDefinition.to_json())

# convert the object into a dict
inline_filter_definition_dict = inline_filter_definition_instance.to_dict()
# create an instance of InlineFilterDefinition from a dict
inline_filter_definition_from_dict = InlineFilterDefinition.from_dict(inline_filter_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


