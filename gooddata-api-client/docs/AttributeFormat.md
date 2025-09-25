# AttributeFormat

Attribute format describes formatting information to effectively format attribute values when needed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locale** | **str** | Format locale code like &#39;en-US&#39;, &#39;cs-CZ&#39;, etc. | 
**pattern** | **str** | ICU formatting pattern like &#39;y&#39;, &#39;dd.MM.y&#39;, etc. | 
**timezone** | **str** | Timezone for date formatting like &#39;America/New_York&#39;, &#39;Europe/Prague&#39;, etc. | [optional] 

## Example

```python
from gooddata_api_client.models.attribute_format import AttributeFormat

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeFormat from a JSON string
attribute_format_instance = AttributeFormat.from_json(json)
# print the JSON string representation of the object
print(AttributeFormat.to_json())

# convert the object into a dict
attribute_format_dict = attribute_format_instance.to_dict()
# create an instance of AttributeFormat from a dict
attribute_format_from_dict = AttributeFormat.from_dict(attribute_format_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


