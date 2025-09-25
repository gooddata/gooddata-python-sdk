# AttributeItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | [**AfmObjectIdentifierLabel**](AfmObjectIdentifierLabel.md) |  | 
**local_identifier** | **str** | Local identifier of the attribute. This can be used to reference the attribute in other parts of the execution definition. | 
**show_all_values** | **bool** | Indicates whether to show all values of given attribute even if the data bound to those values is not available. | [optional] [default to False]

## Example

```python
from gooddata_api_client.models.attribute_item import AttributeItem

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeItem from a JSON string
attribute_item_instance = AttributeItem.from_json(json)
# print the JSON string representation of the object
print(AttributeItem.to_json())

# convert the object into a dict
attribute_item_dict = attribute_item_instance.to_dict()
# create an instance of AttributeItem from a dict
attribute_item_from_dict = AttributeItem.from_dict(attribute_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


