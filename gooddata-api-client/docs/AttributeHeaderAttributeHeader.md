# AttributeHeaderAttributeHeader


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**attribute_name** | **str** | Attribute name. | 
**format** | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**granularity** | **str** | Date granularity of the attribute, only filled for date attributes. | [optional] 
**label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**label_name** | **str** | Label name. | 
**local_identifier** | **str** | Local identifier of the attribute this header relates to. | 
**primary_label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**value_type** | **str** | Attribute value type. | [optional] 

## Example

```python
from gooddata_api_client.models.attribute_header_attribute_header import AttributeHeaderAttributeHeader

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeHeaderAttributeHeader from a JSON string
attribute_header_attribute_header_instance = AttributeHeaderAttributeHeader.from_json(json)
# print the JSON string representation of the object
print(AttributeHeaderAttributeHeader.to_json())

# convert the object into a dict
attribute_header_attribute_header_dict = attribute_header_attribute_header_instance.to_dict()
# create an instance of AttributeHeaderAttributeHeader from a dict
attribute_header_attribute_header_from_dict = AttributeHeaderAttributeHeader.from_dict(attribute_header_attribute_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


