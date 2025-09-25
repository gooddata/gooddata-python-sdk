# InlineFilterDefinitionInline


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**filter** | **str** | MAQL query representing the filter. | 
**local_identifier** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.inline_filter_definition_inline import InlineFilterDefinitionInline

# TODO update the JSON string below
json = "{}"
# create an instance of InlineFilterDefinitionInline from a JSON string
inline_filter_definition_inline_instance = InlineFilterDefinitionInline.from_json(json)
# print the JSON string representation of the object
print(InlineFilterDefinitionInline.to_json())

# convert the object into a dict
inline_filter_definition_inline_dict = inline_filter_definition_inline_instance.to_dict()
# create an instance of InlineFilterDefinitionInline from a dict
inline_filter_definition_inline_from_dict = InlineFilterDefinitionInline.from_dict(inline_filter_definition_inline_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


