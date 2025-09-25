# AttributeResultHeader

Header containing the information related to attributes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_value** | **str** | A value of the current attribute label. | 
**primary_label_value** | **str** | A value of the primary attribute label. | 

## Example

```python
from gooddata_api_client.models.attribute_result_header import AttributeResultHeader

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeResultHeader from a JSON string
attribute_result_header_instance = AttributeResultHeader.from_json(json)
# print the JSON string representation of the object
print(AttributeResultHeader.to_json())

# convert the object into a dict
attribute_result_header_dict = attribute_result_header_instance.to_dict()
# create an instance of AttributeResultHeader from a dict
attribute_result_header_from_dict = AttributeResultHeader.from_dict(attribute_result_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


